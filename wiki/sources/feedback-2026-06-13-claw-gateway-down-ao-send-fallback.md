---
title: "/claw: hermes gateway status CLI is broken — use curl :8642/health (2026-06-13)"
type: source
tags: [feedback, claw, hermes, gateway-status, ao-send, worldarchitect-ai, pre-flight]
date: 2026-06-13
source_file: raw/feedback_2026-06-13_claw_gateway_down_ao_send_fallback.md
---

## Summary
`hermes gateway status` CLI is broken — it mis-reports "Gateway is not running" with phantom "drain / PID 3168" output even when the gateway is up. The actual health is `curl http://127.0.0.1:8642/health` returning `{"status": "ok", "platform": "hermes-agent"}`. As of 2026-06-13 07:30Z, `/claw` is patched — pre-flight uses `curl :8642/health` (not the broken CLI) and dispatch is now Slack-based. This memory serves as the historical record of the bug + the **MANDATORY `ao send` message template** (still relevant for driving existing AO workers).

## Key Claims
- The `/claw` skill body (`~/.claude/skills/claw-dispatch/SKILL.md`) hard-fails unless `hermes gateway status` outputs "Gateway is running" (lines 89–98). That gate is the only blocker; the chat path (lines 250–256, `nohup hermes chat -q "$task" --yolo --max-turns 90 -Q --source tool`) is fine.
- `hermes gateway status` reports a phantom "Discord bot token already in use (PID 3168). Stop the other gateway first." + "Gateway draining for shutdown (1 active agent(s))" — but `~/.hermes_prod/gateway_state.json` says `gateway_state: "running"` and `curl :8642/health` returns OK (PID 71789 listening on 8642).
- **Trust the curl, not the CLI.** All platforms (api_server, slack, discord, telegram) show `connected` in `gateway_state.json`.
- `ao send` is **NOT** a fallback for `/claw` — it's a different path (drive existing worker vs spawn new chat). Use `ao send` when the user wants to drive an already-attached AO worker (e.g. wa-2310 on PR #7509).
- Ad-hoc prose in `ao send` causes worker confusion (wa-2310 wandered 30 min on a message that mentioned #7506 + #7509 ambiguously). Use the **MANDATORY `ao send` message template** below.

## Recipe: run /claw when the status CLI is broken
```bash
export HERMES_HOME=/Users/jleechan/.hermes_prod
export HERMES_LOG_LEVEL=INFO
curl -sS -m 3 http://127.0.0.1:8642/health  # expect: {"status": "ok", "platform": "hermes-agent"}

# Then spawn hermes chat (same as /claw body line 250) — no status check needed
nohup /opt/homebrew/bin/hermes chat \
  -q "<task>" --yolo --max-turns 90 -Q --source tool \
  >/tmp/hermes/claw-<ts>.log 2>&1 &
```
Notes: `-Q` and `--source tool` mean the log stays empty during normal operation (streamed output suppressed, persisted at session end). Don't rely on the 15s ACK pattern from the skill body — verify the process is alive and has child processes (`pgrep -P <PID>`) instead.

## MANDATORY `ao send` message template
```
WORKTREE: <absolute path>     # where this worker should cd
BRANCH:   <branch name>       # what git rev-parse --abbrev-ref HEAD must show
HEAD_SHA: <short SHA>         # what git rev-parse HEAD must show before edits
PR:       #<N>                # the PR this worker owns
JOB:      <one sentence, imperative, no other PR# in the body>
STEPS:
  1. cd <worktree>
  2. git fetch origin
  3. git rev-parse --abbrev-ref HEAD  # MUST equal BRANCH
  4. git rev-parse HEAD              # MUST equal HEAD_SHA
  5. <single concrete next step>
  6. report
DO NOT:
  - call `ao session claim-pr` for any PR other than <N>
  - run `git worktree add` (worktree already exists at <worktree>)
  - explore unrelated repos or run br list / header_check.py
  - mention or act on any other PR number
Sender: claude, project: <project-key>
```
Verify: `tmux capture-pane -t <session> -p -S -20 | grep -E "WORKTREE|BRANCH|HEAD_SHA"`. If those tokens are not echoed, the worker is still on the previous turn — wait, do not re-send.

## Source-of-truth order (extends dashboard-lags-tmux)
1. `git -C <worktree> log --oneline -5` (real commits)
2. `tmux capture-pane -t <name> -p -S -40` (real conversation)
3. `gh pr view <N> --json headRefOid` (real PR head)
4. `ao status` (lifecycle state — useful but lagging)
5. AO dashboard (decorative, do not drive decisions off it)
6. **`hermes gateway status` CLI — LIES, do not trust** (use `curl :8642/health` instead)

## Key Quotes
> "The original memory said 'gateway is down, fall back to ao send.' User said no — the gateway was up the whole time, the status CLI is the thing that's broken. Do not bypass /claw; bypass the status check."

## Connections
- [[feedback-2026-06-13-claw-slack-dispatch]] — the new Slack-based dispatcher (replaces the old status-CLI-gated path)
- [[feedback-2026-06-10-ao-spawn-dispatch-sequence]] — pre-flight + post-spawn verification pattern that `ao send` template extends
- [[feedback-2026-06-11-bash-cwd-does-not-persist-across-invocations]] — `cd` doesn't persist between Bash calls (relevant for STEPS that include `cd <worktree>`)
- [[ClawGatewayHealthCheck]] / [[HermesGatewayStatusCLI]] — concept pages that should document `curl :8642/health` as the canonical pre-flight

## Bead / PR / Roadmap

- Target PRs: BQ PRs #7506 / #7509 / #7510
- Status: /claw is patched as of 2026-06-13 07:30Z (pre-flight uses curl, dispatch is Slack-based). Memory retained for the MANDATORY `ao send` template and source-of-truth order.
- Origin session: `33b6218a-1fc0-42b9-b4f8-1814474904eb`

## [[jeffrey-oracle]]

Not affected. This is a `/claw` / `ao send` ops discipline learning specific to worldarchitect.ai.

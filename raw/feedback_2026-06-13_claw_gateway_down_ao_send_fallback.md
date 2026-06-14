---
name: feedback-2026-06-13-claw-status-cli-broken-skip-check
description: hermes gateway status CLI mis-reports; verify Hermes via curl :8642/health (the /claw pre-flight is now patched to use this). See [[feedback-2026-06-13-claw-slack-dispatch]] for the new Slack-based dispatcher.
metadata:
  node_type: memory
  type: feedback
  originSessionId: 33b6218a-1fc0-42b9-b4f8-1814474904eb
---

# /claw: `hermes gateway status` CLI is broken; verify via curl :8642/health instead

**Date**: 2026-06-13 (corrected 23:00Z from earlier wrong "fallback to ao send" version)
**Context**: BQ PRs #7506 / #7509 / #7510 — user said "/claw them" then corrected "Hermes was not down"
**Lesson**: the original memory said "gateway is down, fall back to ao send." User said no — the gateway was up the whole time, the status CLI is the thing that's broken. Do not bypass /claw; bypass the status check.

> **Status (2026-06-13 07:30Z)**: /claw is now patched — both the pre-flight and the dispatch path are fixed. The pre-flight uses `curl :8642/health` (not the broken CLI), and the dispatch is Slack-based (posts to #claw-dispatch). See [[feedback-2026-06-13-claw-slack-dispatch]] for the full new architecture. This memory now serves as the historical record of the bug + the MANDATORY `ao send` template, which is still relevant for driving existing AO workers.

## What the /claw script does (skill body `~/.claude/skills/claw-dispatch/SKILL.md`)

1. Lines 89-98: hard-fail unless `hermes gateway status` outputs the string "Gateway is running"
2. Lines 250-256: spawn `nohup hermes chat -q "$task" --yolo --max-turns 90 -Q --source tool`

The status check is the only blocker. The chat path is fine without it.

## Why the status CLI is broken (verified 2026-06-13 23:00Z)

- `hermes gateway status` reports:
  ```
  ✗ Gateway is not running
  Recent gateway health:
    ⚠ discord: Discord bot token already in use (PID 3168). Stop the other gateway first.
    ⏳ Gateway draining for shutdown (1 active agent(s))
  ```
- BUT the actual gateway is up: `curl http://127.0.0.1:8642/health` returns `{"status": "ok", "platform": "hermes-agent"}` (PID 71789 listening on 8642)
- `~/.hermes_prod/gateway_state.json` says `gateway_state: "running"` and all platforms (api_server, slack, discord, telegram) are `connected`
- The status CLI checks some "drain" / "phantom PID 3168" condition that disagrees with reality

**Trust the curl, not the CLI.**

## Recipe: run /claw when the status CLI is broken

```bash
# 1. Env from launchd plist (or use HERMES_HOME=/Users/jleechan/.hermes_prod directly)
export HERMES_HOME=/Users/jleechan/.hermes_prod
export HERMES_LOG_LEVEL=INFO

# 2. Verify the gateway is actually up
curl -sS -m 3 http://127.0.0.1:8642/health
# expect: {"status": "ok", "platform": "hermes-agent"}

# 3. Build the task file
TASK="<task description>"
LOGDIR=/tmp/hermes
mkdir -p "$LOGDIR" && chmod 700 "$LOGDIR"
TASK_FILE=$(mktemp "$LOGDIR/.claw-task-XXXXXXXX")
chmod 600 "$TASK_FILE"
printf '%s' "$TASK" >"$TASK_FILE"

# 4. Spawn hermes chat (same as /claw body line 250)
LOGFILE="$LOGDIR/claw-$(date +%s).log"
nohup /opt/homebrew/bin/hermes chat \
  -q "$(cat "$TASK_FILE")" \
  --yolo --max-turns 90 -Q --source tool \
  >"$LOGFILE" 2>&1 &
echo "PID=$!, log=$LOGFILE"
```

Notes:
- `-Q` and `--source tool` mean the log stays empty during normal operation (streamed output suppressed, persisted at session end). Don't rely on the 15s ACK pattern from the skill body — verify the process is alive and has child processes (`pgrep -P <PID>`) instead.
- The chat session will have bash + MCP tools (slack, etc.) as children. Activity = children of the chat PID doing real work.

## When to use `ao send` to existing workers (the original lesson, still valid)

- When the user wants to drive an already-attached AO worker (e.g. wa-2310 on PR #7509) rather than spawn a fresh chat session, `ao send <session> "<task>"` is the right tool.
- `ao send` messages should follow the MANDATORY template (see below) — raw prose causes worker confusion.
- `ao send` is NOT a fallback for /claw — it's a different path (drive existing vs spawn new).

## MANDATORY `ao send` message template

Ad-hoc prose causes worker confusion (wa-2310 wandered for 30 min on a message that mentioned #7506 + #7509 ambiguously). Any direct `ao send` to an existing worker MUST use this structure:

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

Verify the worker read the message: `tmux capture-pane -t <session> -p -S -20 | grep -E "WORKTREE|BRANCH|HEAD_SHA"`. If those tokens are not echoed, the worker is still on the previous turn — wait, do not re-send.

## Related

- [[feedback-2026-06-12-bd-qw6-measured-section-warning]] — different skeptic catch pattern
- [[feedback-2026-06-10-ao-spawn-dispatch-sequence]] — pre-flight + post-spawn verification
- [[feedback-2026-06-11-bash-cwd-does-not-persist-across-invocations]] — `cd` doesn't persist between Bash calls

## Source-of-truth order (extends dashboard-lags-tmux)

1. `git -C <worktree> log --oneline -5` (real commits)
2. `tmux capture-pane -t <name> -p -S -40` (real conversation)
3. `gh pr view <N> --json headRefOid` (real PR head)
4. `ao status` (lifecycle state — useful but lagging)
5. AO dashboard (decorative, do not drive decisions off it)
6. **`hermes gateway status` CLI — LIES, do not trust** (use `curl :8642/health` instead)

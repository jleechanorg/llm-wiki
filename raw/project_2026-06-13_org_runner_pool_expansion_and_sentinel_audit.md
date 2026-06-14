---
name: project-2026-06-13-org-runner-pool-expansion-and-sentinel-audit
description: "Today (2026-06-13) the jleechanorg runner pool grew from 6 to 15 online+busy (launchd supervisor re-spun previously-offline bare-org-runner-N); active run pile-up subsided 50→29 as 4 hot PRs settled; empirical audit confirmed .ci-retrigger sentinel is a write-only memo, not a state machine."
metadata: 
  node_type: memory
  type: project
  originSessionId: 73be4e82-d635-4fd2-96b7-639072ec7448
---

# Org runner pool expansion + sentinel empirical audit (2026-06-13)

## What happened

Today (2026-06-13) the jleechanorg GitHub Actions self-hosted runner pool grew substantially and a 50-active-run pile-up subsided. Investigation confirmed that the `.ci-retrigger` sentinel flip performed during the session was a **no-op** (no code reads the file).

## Runner pool state change

| Snapshot | bare-org-runner-N (Linux X64) | org-runner-mac-N (Linux ARM64) | wa-oss-runner-local (macOS) | Total online+busy |
|---|---|---|---|---|
| Earlier in this session (2026-06-12 ~22:52) | 5× **offline** (IDs 77708-77713) | 6× online+busy | 1× online+busy (id 9911) | **6** |
| Now (2026-06-13 ~07:00) | **9× online+busy** (1, 3, 4, 5, 6, 7, 8, 9, 10) | 6× online+busy | not in latest API snapshot | **15** (14 busy + 1 idle) |

The previously-offline `bare-org-runner-N` instances were re-spun by the **launchd supervisor at `/Users/jleechan/Library/LaunchAgents/com.worldarchitect.org-runners.plist`** (verified; the supervisor periodically reconnects offline runners). 2.5× capacity increase.

## Pile-up: 50 → 29 active runs

- 50 active runs cancelled in two sweeps earlier in the session; 7 new runs re-queued in 5 sec
- Hot PRs driving the loop: `fix-stale-complete-preserve-fresh-rewards` (10 runs), `fix/7364-level-up-modal-choices-atomic-pair` (10), `fix/banned-names-prompt-injection-7482` (9), `main` (9)
- **By 2026-06-13 ~07:00, the 4 hot PRs settled** (merges, push cadence dropped) and 29 active runs remain. **No re-queue loop.** The remaining 29 are mostly legitimate `MCP Smoke Tests` (workflow_run, fired by recent merges).

## `.ci-retrigger` empirical audit (3 subagents, all NOT FOUND)

**Verdict**: `.ci-retrigger` is a **write-only memo, not a state machine**. The `printf 'idle' > .ci-retrigger` step in the 2026-06-12 kill recipe is ceremonial.

Evidence:
- 87 re-trigger commits in 71 days on agent-orchestrator repo, **82/87 (94.3%) empty** `git commit --allow-empty`
- File touched only 3 times in 71 days (1 file creation, 1 test side effect, 1 sentinel-flip on a feature branch) — uncorrelated with commit cadence
- Inter-arrival times show **NO cron signature** (11 within-60-sec bursts, hour distribution is human-shaped)
- On `main`, file has been `trigger` continuously since 2026-04-16 while re-trigger commits continue
- **No code on `/Users/jleechan` reads it** — searched exhaustively: agent-orchestrator's `packages/*/src/` + `node_modules` + `dist`, `~/.hermes`, `~/.hermes_prod`, `~/.worktrees`, `~/.config`, `~/.local/bin`, `/opt/homebrew`, `/usr/local`, all `*.sh/*.py/*.ts/*.js/*.yaml/*.json/*.md` in project trees, every `ai.*` and `com.*` launchd plist, all cron jobs, all running Docker containers
- The intended reader is **on a different host** (the AO cron respawn loop, likely on a non-mac runner or VM) — out of scope for single-host search

## Action taken

- **Reverted `.ci-retrigger` to its HEAD value (`trigger`)** with `git checkout HEAD -- .ci-retrigger` in agent-orchestrator repo. Working tree is now clean of my no-op flip.
- **Updated 2026-06-12 memory entry** (`feedback_2026-06-12_local_claude_session_can_runaway_push.md`) to add a "Correction (2026-06-13)" section clarifying the file is a write-only memo, the kill recipe's step 2 is cosmetic, and the actual stop is `kill -9 <PID>`.
- **Did not create a real reader for the sentinel** — that would be net-new automation, out of scope for "runner stuff as needed".

## Why this matters

Future agents reading the 2026-06-12 memory entry should not propagate the false claim that "the AO cron respects `.ci-retrigger`". The empirical audit (and the updated memory entry) make this clear. The 2026-06-12 instruction-level fix (rewriting `/wakebugbot` + `git-pr-conflict-resolve/SKILL.md:64` to use `gh workflow run`) remains the correct root-cause fix; the file flip is a backstop signal for humans, not a control.

The 15-runner effective pool is the real win from this session — that gives worldarchitect.ai meaningful headroom for the next push burst.

## Reference

- Date: 2026-06-13
- Project: jleechanorg (org-wide) / worldarchitect.ai (one consumer repo)
- Verified via: 3 subagent investigations (a4b628fcba93df6e3 code search, af35f4e03535d0788 launchd/cron audit, a544a5665c584c4e2 git log empirical analysis)
- Related: see also `[[feedback_2026-06-12_github_org_runner_registration_vs_group_access]]` (org runner pool is 7 effective runners as of 2026-06-12; this update bumps to 15) and `[[feedback-2026-06-12-local-claude-session-can-runaway-push]]` (the 2026-06-12 kill recipe, now corrected to remove the cosmetic sentinel-flip step)

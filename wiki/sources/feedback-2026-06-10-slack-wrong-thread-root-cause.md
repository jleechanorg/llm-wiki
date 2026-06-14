---
title: "Slack wrong-thread root cause: 4 paths (2026-06-10 → 2026-06-13)"
type: source
tags: [feedback, slack, wrong-thread, watchdog, ao-progress-reporter, dropped-thread, human_channel_bridge, root-cause, paths, umbrella-pattern, squash-merge]
date: 2026-06-10
source_file: raw/feedback_2026-06-10_slack_wrong_thread_root_cause.md
---

## Summary
Hermes "wrong-thread" Slack posts have **four distinct causes** — diagnose by script, not by symptom. The 2026-06-10 investigation found 27 top-level watchdog alerts in `#all-jleechan-ai` (C09GRLXF9GR) and split them by code path. All 4 paths have since been resolved across 7 PRs (#601, #604, #605, #606, #607, #608, #609) plus the umbrella fix in PR #687 (2026-06-13) for the cross-repo watchdog flooding caused by PR #681's regression.

## The 4 Paths

### Path 1 — Watchdog / health-guardian (intended top-level, wrong channel)
- `project_agento/agent-orchestrator/scripts/hermes-watchdog.sh`
- `project_agento/agent-orchestrator/scripts/ai.agento.health-guardian.sh`
- **Always post top-level** (`thread_ts` never set). Posts flood `#all-jleechan-ai`.
- **Real bug**: not the threading — the channel. Should route to `#ops-alerts` or thread under a daily "ops" root.
- Spam pattern: dedup window 30 min × log mtime threshold 300s → 27 messages/12h.
- **Resolution (PR #687, 2026-06-13):** restored PR #615 umbrella pattern. Root cause was PR #681 regression: hardcoded `HERMES_OPS_SLACK_CHANNEL="${HERMES_OPS_SLACK_CHANNEL:-C0AJ3SD5C79}"` (design default in an ops var) + back-ass guard that UNSETS the correct `C09GRLXF9GR` plist value + plist template that dropped the per-job env. New bead: `jleechan-5mkt`.

### Path 2 — ao-progress-reporter.sh (currently CORRECT)
- Uses per-day thread in `C0ALSKLU9KM`; `resolve_thread_ts()` creates it once.
- Failure mode: if Slack API fails at thread creation, silently falls back to channel root with **no retry**.
- Root: lines 169 / 257 — empty `response` on first-call error → `echo ""` → no `thread_ts`.
- **Resolution (PR #608, jleechanclaw ac8b20013):** suppress no-op/unchanged status posts + prune terminal sessions. This is the fix for "AO status updates go forever" — terminal sessions were being re-reported indefinitely.

### Path 3 — dropped-thread-followup.sh (no persistent thread state)
- Escalations always post to C09GRLXF9GR top-level; no memory of which Slack thread triggered them.
- **Resolution (PR #607, jleechanclaw a3d3e18ca):** per-channel cooldown + per-incident give-up cap (`DROP_MAX_NUDGES`, `channel_in_cooldown`), `_migrate_nudge` migrates legacy bare-string `.nudged` state → object form.

### Path 4 — human_channel_bridge.py (stale worker_threads dict)
- First spawn message creates top-level root; subsequent updates thread to it.
- If `worker_threads` dict loses session (process crash), exit messages post to channel root.
- **Resolution (PR #604 squash, verified on main):** `os.replace` ×3, `_save_thread_state` / `_load_thread_state`, `worker_threads` persistence ×18, `BRIDGE_THREAD_STATE_FILE` override ×3. The 4 commit SHAs (c659f82d3e, 9ebe85b643, f6b1a5a907, 19c758fbf4) are NOT ancestors of main by SHA — squash-merge artifact only. **Verify divergence by file CONTENT (`git show <ref>:<path>`), not SHA ancestry, after squash merges.**

### Path 4b — Gateway status-thread leak (PR #27, fork f4841cc3f)
- Gateway `_status_thread_metadata` channel-root leak: fix carries reply-anchor `thread_id` + skips `lifecycle_hidden` events. Prod gateway (port 8642) restarted via `launchctl kickstart -k gui/$UID/ai.hermes.prod`.

## How to apply
- When debugging wrong-thread posts, grep logs for which script/process posted.
- Watchdog alerts that flood #all-jleechan-ai → fix the channel, not the threading.
- ao-progress-reporter failures → look for API errors in `resolve_thread_ts()`.
- AO exit messages in wrong thread → check `human_channel_bridge.py` state persistence.

## Reusable pattern
Any Slack post with no `thread_ts` defaults to top-level. Every status/alert script should require an explicit decision: "what thread does this reply to?" If no thread exists yet, create a daily/weekly root message first and persist its `ts`.

## Branch Reconciliation Gotchas (2026-06-12)
- `~/.hermes` was parked on stale branch `fix/dropped-thread-escalation-persistence`; merged scripts were surgically deployed via `git checkout origin/main -- <file>` (no branch switch). launchd jobs read the working tree → picked up on next run.
- After #610, switch back to main hit: working-tree `agent-orchestrator.yaml` showed a 473/324 raw diff vs main but was **semantically identical** (pure reformatting). Verify config equivalence by parsing YAML and comparing normalized dumps, NOT raw line diff.
- Surgically-deployed scripts were *staged*, so `git checkout -- <f>` didn't clear them; needed `git checkout HEAD -- <f>` (index+worktree).
- `git pull --ff-only` failed under `pull.rebase=true`; use `git merge --ff-only origin/main` instead.
- Path-reconciliation FLIPPED from the original plan: main's `~/projects/jleechanclaw` is a non-git stub and `~/.worktrees/jleechanclaw-main` is missing, so #610 promoted the working-tree's live-correct values TO main rather than reconciling to main's broken ones.

## Key Quotes
> Any Slack post with no `thread_ts` defaults to top-level. Every status/alert script should require an explicit decision: "what thread does this reply to?"

> Lesson for the umbrella skill: consolidation refactors that hardcode a default value regress the same class of bug they meant to fix.

## Connections
- [[Slack]] — Slack dispatch infrastructure
- [[UmbrellaPattern]] — empty default + plist-as-source-of-truth (PR #615 / #687)
- [[SlackThreadRouting]] — daily thread anchor + dedupe pattern
- [[Path-by-Path Diagnosis]] — debug by script, not by symptom
- [[SquashMergeDivergence]] — verify file CONTENT, not SHA ancestry, after squash merges
- [[BranchReconciliation]] — surgical `git checkout origin/main -- <f>` deploy pattern
- [[SlackWrongThread]] — older parent topic

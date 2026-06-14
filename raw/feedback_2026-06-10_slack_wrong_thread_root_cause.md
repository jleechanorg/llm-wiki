---
name: slack-wrong-thread-root-cause
description: Four Hermes/AO code paths that post to wrong Slack threads; watchdog/health scripts are top-level by design; ao-progress-reporter is correct
metadata: 
  node_type: memory
  type: feedback
  bead: jleechan-owka
  originSessionId: 0045c60d-afe5-4e07-84a6-54dde9b7d8b0
---

## Rule

Hermes "wrong-thread" Slack posts have four distinct causes — diagnose by script, not by symptom.

## Why

2026-06-10 investigation found 27 top-level watchdog alerts in #all-jleechan-ai (C09GRLXF9GR) and identified the root causes.

## The four paths

### 1. Watchdog / health-guardian (intended top-level, wrong channel)
- `project_agento/agent-orchestrator/scripts/hermes-watchdog.sh`
- `project_agento/agent-orchestrator/scripts/ai.agento.health-guardian.sh`
- Always post **top-level** — `thread_ts` never set. Posts flood #all-jleechan-ai.
- Fix: route to a dedicated `#ops-alerts` channel, or thread under a daily "ops" root message.
- Spam pattern: dedup window 30 min × log mtime threshold 300s → 27 messages/12h.

### 2. ao-progress-reporter.sh (currently CORRECT)
- Uses per-day thread in C0ALSKLU9KM; `resolve_thread_ts()` creates it once.
- Failure mode: if Slack API fails at thread creation, silently falls back to channel root with no retry.
- Root: lines 169 / 257 — empty `response` on first-call error → `echo ""` → no thread_ts.

### 3. dropped-thread-followup.sh (no persistent thread state)
- Escalations always post to C09GRLXF9GR top-level; no memory of which Slack thread triggered them.
- Fix: write `DROP_THREAD_TS` to a state file when the dropped-thread is first detected, read it on escalation.

### 4. human_channel_bridge.py (stale worker_threads dict)
- First spawn message creates top-level root; subsequent updates thread to it.
- If `worker_threads` dict loses session (process crash), exit messages post to channel root.
- Fix: persist `worker_threads` to disk; reload on startup.

## How to apply

- When debugging wrong-thread posts, grep logs for which script/process posted.
- Watchdog alerts that flood #all-jleechan-ai → fix the channel, not the threading.
- ao-progress-reporter failures → look for API errors in `resolve_thread_ts()`.
- AO exit messages in wrong thread → check `human_channel_bridge.py` state persistence.

## References

- Subagent investigation 2026-06-10, session `0045c60d`
- Skill: `skills/devops/slack-thread-routing-investigation/SKILL.md`
- Bead: jleechan-owka

## Reusable pattern

Any Slack post with no `thread_ts` defaults to top-level. Every status/alert script should require an explicit decision: "what thread does this reply to?" If no thread exists yet, create a daily/weekly root message first and persist its `ts`.

## Resolution (2026-06-11)

Three PRs merged (admin merge after local tests green; skeptic-cron auto-merge was moot):
- **Path 2 (#608, jleechanclaw ac8b20013)** — `ao-progress-reporter.sh`: suppress no-op/unchanged status posts + prune terminal sessions. **This is the fix for "AO status updates go forever"** — terminal sessions were being re-reported indefinitely. daily_threads persistence retained.
- **Path 3 (#607, jleechanclaw a3d3e18ca)** — `dropped-thread-followup.sh`: per-channel cooldown + per-incident give-up cap (`DROP_MAX_NUDGES`, `channel_in_cooldown`), `_migrate_nudge` migrates legacy bare-string `.nudged` state → object form. Designed successor to the live escalation logic.
- **Path 4 gateway leak (#27, fork f4841cc3f)** — gateway `_status_thread_metadata` channel-root leak: carry reply-anchor `thread_id` + skip `lifecycle_hidden` events. Prod gateway (runs from `~/projects_other/hermes-agent`, port 8642) restarted via `launchctl kickstart -k gui/$UID/ai.hermes.prod`; verified single-instance, healthy, fix on disk.

**Deploy note:** `~/.hermes` was parked on unmerged branch `fix/dropped-thread-escalation-persistence`; the two merged scripts were surgically deployed via `git checkout origin/main -- scripts/dropped-thread-followup.sh scripts/ao-progress-reporter.sh` (no branch switch). launchd jobs read the working tree → picked up on next run.

**~/.hermes returned to main (2026-06-12):** after #610 (admin-merged on explicit user instruction: worldarchitect `skepticCron` per-PR throttle + jleechanclaw path fixes), `~/.hermes` was switched off the stale `fix/dropped-thread-escalation-persistence` branch back to `main` (HEAD 2fe2e5fa32). Switch mechanics that bit: working-tree `agent-orchestrator.yaml` showed a 473/324 *raw* diff vs main but was **semantically identical** (pure reformatting) — verify config equivalence by parsing YAML and comparing normalized dumps, NOT raw line diff. The two surgically-deployed scripts were *staged*, so `git checkout -- <f>` didn't clear them; needed `git checkout HEAD -- <f>` (index+worktree). `git pull --ff-only` failed under `pull.rebase=true`; use `git merge --ff-only origin/main` instead. Path-reconciliation FLIPPED from the original plan: main's `~/projects/jleechanclaw` is a non-git stub and `~/.worktrees/jleechanclaw-main` is missing, so #610 promoted the working-tree's live-correct values TO main rather than reconciling to main's broken ones. Preserved runtime drift (docs/context/*.md, gateway_state.json) across the switch.

**Outstanding follow-up — RESOLVED (2026-06-12):** the `human_channel_bridge.py` atomicity refinements are **on main via #604's squash** (verified: `git show origin/main:src/orchestration/human_channel_bridge.py` has `os.replace` ×3, `_save_thread_state`/`_load_thread_state`, `worker_threads` persistence ×18, `BRIDGE_THREAD_STATE_FILE` override ×3). The four commit SHAs (c659f82d3e, 9ebe85b643, f6b1a5a907, 19c758fbf4) are not ancestors of main *by SHA* — squash-merge artifact only; their CONTENT landed and main is in fact NEWER than the stale `fix/dropped-thread-escalation-persistence` branch `~/.hermes` is parked on (origin/main..HEAD = 408 ins / 1151 del, i.e. the local branch would UNDO merged work). All 7 Slack-routing PRs merged: #601, #604, #605, #606, #607, #608, #609. Lesson: verify divergence by file CONTENT (`git show <ref>:<path>` / content diff), not SHA ancestry, after squash merges.

**Path 1 (cross-repo watchdog flooding) — RESOLVED via PR #687 (2026-06-13):** the `project_agento/agent-orchestrator` watchdogs (hermes-watchdog, ai.agento.health-guardian) were misrouting because of **PR #681 (d8940175b) regression** that:
1. Hardcoded `HERMES_OPS_SLACK_CHANNEL="${HERMES_OPS_SLACK_CHANNEL:-C0AJ3SD5C79}"` (wrong: design channel default)
2. Added a back-ass guard: `if [ "${HEALTH_GUARDIAN_ALERT_CHANNEL:-}" = "C09GRLXF9GR" ]; then HEALTH_GUARDIAN_ALERT_CHANNEL=""` — actively UNSETS the correct plist value
3. Removed the `HEALTH_GUARDIAN_ALERT_CHANNEL` env from the plist template

PR #687 fix: restored PR #615 umbrella pattern (empty default > wrong default), rewrote the watchdog-routing test (7/11 fail on pre-fix), added empty-channel fail-soft guard. New bead: jleechan-5mkt. **Lesson for the umbrella skill:** consolidation refactors that hardcode a default value regress the same class of bug they meant to fix. The umbrella pattern (PR #615 / jleechanclaw `lib/slack_thread_lib.sh`) is "empty default + plist-as-source-of-truth" precisely because hardcoded defaults drift toward the wrong channel over time. Tests that assert the post-refactor behavior are useless unless they also assert the desired behavior (here: `C09GRLXF9GR` pass-through).

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

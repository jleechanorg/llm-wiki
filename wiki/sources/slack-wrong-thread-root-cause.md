# Slack Wrong-Thread Root Cause

**Source**: `~/.claude/projects/-Users-jleechan--hermes/memory/feedback_2026-06-10_slack_wrong_thread_root_cause.md`
**Ingested**: 2026-06-10
**Bead**: jleechan-owka

## Summary

Four Hermes/AO code paths that post to Slack without a valid `thread_ts`, causing messages to land in wrong threads or as top-level channel messages.

## The four paths

| Script / Module | Failure mode | Fix |
|---|---|---|
| `hermes-watchdog.sh` + `ai.agento.health-guardian.sh` | Always top-level; floods `#all-jleechan-ai` with 27 msgs/12h | Route to `#ops-alerts` or thread under daily root |
| `ao-progress-reporter.sh` lines 169/257 | No retry on `resolve_thread_ts()` fail → channel root | Add retry + persistence |
| `dropped-thread-followup.sh` | No state file for escalation thread | Persist `DROP_THREAD_TS` when first detected |
| `human_channel_bridge.py` lines 264/567-599 | `worker_threads` dict lost on crash → exit msgs top-level | Persist dict to disk |

## Key observation

Watchdog alert spam is not a routing bug — it is working as designed (no `thread_ts`). Fix requires a design decision: dedicated channel or threaded daily root.

`ao-progress-reporter.sh` is correct today but silently falls back to channel root on Slack API error.

## References

- Skill: `skills/devops/slack-thread-routing-investigation/SKILL.md`
- Session: 0045c60d (2026-06-10)

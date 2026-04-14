---
title: "Proactive Session Recovery"
type: concept
tags: [agento, session-recovery, respawn, ao, stuck, killed, merge-completed]
last_updated: 2026-03-14
sources: [jleechanclaw-agento-proactive-recovery]
---

## Summary
Proactive session recovery is the set of mechanisms that automatically clean up or respawn AO sessions when they reach problematic states — merged PRs, stuck sessions, killed sessions — without requiring manual developer intervention. The design uses a layered approach: polling fallback (ao-backfill.sh), event-driven recovery (openclaw /ao-notify handler), and a long-term upstream AO respawn action type.

## Session Failure Modes and Recovery Paths

| Failure Mode | Immediate Recovery | Event-Driven Recovery | Long-Term Fix |
|---|---|---|---|
| PR merged, session still running | ao-backfill.sh (15min poll) | /ao-notify handler on `merge.completed` | AO respawn action |
| Session stuck, PR still open | ao-backfill.sh (read metadata) | /ao-notify handler on `session.stuck` | AO respawn action |
| Session killed, blocking respawn | Clear `pr` field in metadata, then spawn | Same via handler | AO deduplication fix |
| Session stuck, escalateAfter exhausted | Manual intervention | Webhook handler force-respawns | AO respawn action |

## Event-Driven Recovery via /ao-notify

The openclaw gateway (`agento-notifier.py` on port 18800) already receives AO lifecycle events via `POST /ao-notify`. Currently it posts to Slack; the recovery handler extends this with:

| AO event type | Recovery action |
|---|---|
| `merge.completed` | `ao stop <project>` — kill orphaned session |
| `session.stuck` + PR still open | `ao spawn <project> --claim-pr <N>` — force fresh session |
| `session.killed` | Same as stuck if PR still open |

**Anti-loop guard**: `_ao_respawn_cooldown` per project, minimum 60s between respawns.

## Reading Session State from Metadata Files

AO session metadata lives at:
```
~/.agent-orchestrator/<machine-id>-<project>/sessions/<session-id>
```
Format is plain `key=value`:
```
worktree=/Users/jleechan/.worktrees/...
branch=session/w38-12
status=stuck
tmuxName=5128cfae53d7-w38-12
project=worldai-pr5938
agent=claude-code
createdAt=2026-03-14T19:06:47.664Z
```

To detect stuck sessions old enough to respawn: compare `createdAt` to now. AO doesn't write a `stuckAt` timestamp, so using `createdAt` is a conservative proxy — a session could get stuck seconds after creation but will get multiple nudge cycles first.

## Clearing Stale PR Ownership

`STALE_PR_OWNERSHIP_STATUSES` in AO's session-manager.ts only includes PR-tracking statuses plus `merged` — NOT `stuck` or `killed`. Before force-respawning, clear the `pr` field:
```bash
sed -i '' 's/^pr=.*/pr=/' "$STUCK_META"
```

This prevents the new session from racing with the stale stuck session's PR claim.

## Escalation Ceiling Workaround

Raising `escalateAfter: 3` → `20` in `agent-orchestrator.yaml` gives 20 nudges (10min intervals = ~3.3 hours) before escalation fires. Pair with webhook handler for proper respawn on escalation.

## Why Not Just ao-backfill.sh?

ao-backfill.sh handles cleanup and basic liveness, but:
- Has 15-minute polling lag
- Cannot respawn on escalation (no event-driven trigger)
- Bash complexity grows with more logic

The layered approach: ao-backfill.sh as fallback when gateway is down; webhook handler for <60s event-driven recovery; upstream respawn action for declarative config.

## Related Concepts
- [[LayeredRecoveryArchitecture]]
- [[AutonomousAgentLoop]]
- [[DailyBugHunt]]
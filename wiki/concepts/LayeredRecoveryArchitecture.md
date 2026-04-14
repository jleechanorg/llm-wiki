---
title: "Layered Recovery Architecture"
type: concept
tags: [layered-approach, ao-backfill, webhook, event-driven, polling, respawn]
last_updated: 2026-03-14
sources: [jleechanclaw-agento-proactive-recovery]
---

## Summary
Layered Recovery Architecture addresses session lifecycle failures through three layers with different latencies and mechanisms: polling scripts (immediate, resilient), event-driven webhooks (fast, stateful), and upstream declarative actions (clean, maintainable). No single layer handles all cases; together they provide complete coverage.

## The Three Layers

### Layer 1: Polling Fallback (ao-backfill.sh)

**Role**: Immediate cleanup and liveness, works even if gateway is down
**Mechanism**: 15-minute cron, reads AO session metadata and GitHub PR state directly
**Latency**: Up to 15 minutes after state change
**Scope**:
- Kill sessions for merged/closed PRs
- Force-respawn sessions in stuck/killed state older than 30min

**Why first**: Zero AO repo changes, shell script, easy to audit, works as fallback when webhook handler misses events

### Layer 2: Event-Driven Webhook Handler (openclaw /ao-notify)

**Role**: Fast reaction to lifecycle events (<60s from event to action)
**Mechanism**: `agento-notifier.py` (Python http.server on port 18800) receives AO `POST /ao-notify`, dispatches to recovery handlers
**Latency**: Seconds from event
**Scope**:
- `merge.completed` → `ao stop`
- `session.stuck` + PR open → `ao spawn --fresh`
- `session.killed` → same as stuck if PR open

**Anti-loop**: `_ao_respawn_cooldown` per project (60s minimum)
**Why second**: Event-driven reaction without polling lag; uses existing infrastructure; logic can be arbitrary (check PR state via gh, conditional respawn, alerting)

### Layer 3: Declarative Upstream Action (AO respawn type)

**Role**: Clean declarative config for session recovery, upstreamable
**Mechanism**: In `jleechanorg/agent-orchestrator` fork, add `respawn` action type in `lifecycle-manager.ts`; file PR to ComposioHQ
**Latency**: Same as any AO reaction (near-immediate on event)
**Scope**: `agent-stuck` reaction → respawn action

**Why third**: Declarative YAML config (no external script, no webhook handler logic), inside AO lifecycle loop, no fork maintenance for the immediate fixes

## Latency and Coverage Matrix

| Layer | Latency | Gateway-down survival | Scope |
|---|---|---|---|
| ao-backfill.sh | ~15 min | Yes (polls directly) | cleanup + liveness respawn |
| /ao-notify handler | <60s | No (fire-and-forget) | cleanup + forced respawn |
| AO respawn action | ~immediate | Yes (inside AO) | agent-stuck respawn |

## Why All Three Are Needed

**Layer 1 alone**: 15-min lag is acceptable for cleanup but too slow for recovery. Also, polling-only cannot react to escalation exhaustion without additional logic.

**Layer 2 alone**: Event-driven but fire-and-forget — if gateway is down, events are lost. No queue, no retry.

**Layer 3 alone**: Declarative config handles stuck sessions but doesn't handle merge-completed cleanup (that's ao-backfill's job). Also, upstream PR may take time to merge.

Together: Layer 2 is primary (fast), Layer 1 is fallback (resilient), Layer 3 is long-term (clean).

## Implementation Priority

1. **Layer 1** (implement first) — immediate improvement, no AO repo changes, works today
2. **Layer 2** (implement second) — event-driven, significant latency improvement
3. **Layer 3** (file upstream PR) — long-term, clean, upstreamable

## Related Concepts
- [[ProactiveSessionRecovery]]
- [[AutonomousAgentLoop]]
- [[HarnessEngineering]]
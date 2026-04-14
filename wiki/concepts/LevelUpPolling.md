---
title: "LevelUpPolling"
type: concept
tags: [level-up, polling, worldarchitect, game-state, rewards-pending, streaming, MCP]
sources: [polling-vs-streaming-architecture, worldarchitect-rewards-polling-analysis]
last_updated: 2026-04-14
---

## Summary

`LevelUpPolling` is the pattern where the system detects when a level-up is available. It has **three distinct paths** — SSE streaming (primary, push-based), HTTP GET (page load only), and MCP polling (external clients). Polling must project from the canonical `game_state.rewards_pending` field, NOT from story-entry snapshots.

## The Three Paths

### Path A: Streaming (Primary — SSE Push)
POST `/api/campaigns/<id>/interaction/stream` → SSE stream → `rewards_box` returned inline in SSE `done` event. **Frontend does NOT poll** — this is push. The done event contains the full rewards_box payload.

### Path B: HTTP GET — Page Load Only
GET `/api/campaigns/<id>` → `get_campaign_state_unified` → returns campaign state including pending rewards. **Used only for initial page load**. After page load, SSE connection (Path A) takes over.

### Path C: MCP Polling — External Clients
External clients (mobile, integrations) call `get_campaign_state` MCP tool → calls `get_campaign_state_unified` → builds rewards_box from `game_state.rewards_pending`. **This is true polling.** The idempotency of `rewards_engine.canonicalize_rewards()` is critical — repeated calls with the same game_state must produce identical results.

## Trigger Condition

Path C triggers when a story entry has `rewards_pending` set but no `rewards_box` in `game_state` (stale story recovery scenario).

## The Polling Call Chain

```
get_campaign_state_unified()
  └→ _project_level_up_ui_from_game_state()
       └→ game_state.resolve_level_progression_state()
       └→ game_state.resolve_level_up_signal()
       └→ game_state.ensure_level_up_rewards_pending()
       └→ rewards_engine.build_level_up_rewards_box()
       └→ _enforce_rewards_box_planning_atomicity()
```

## DeferredRewardsProtocol — LLM Instruction, Not Timer

`DeferredRewardsProtocol` is NOT a server-side timer or cron job. It is an **LLM prompt instruction**: "Every 10 player turns, check whether any rewards have been missed and synthesize appropriate rewards." The LLM itself counts turns and triggers the check.

## Correct Pattern

```python
# Polling reads from canonical game_state, not story entry
rewards_pending = game_state.get("rewards_pending", {})
if rewards_pending.get("level_up_available"):
    # Show level-up modal
```

## Related

- [[LevelUpCodeArchitecture]] — Full architecture including all 3 paths and v4 design
- [[DeferredRewardsProtocol]] — LLM-driven deferred rewards mechanism
- [[RewardsBoxAtomicity]] — rewards_box and planning_block consistency
- [[LevelUpBug]] — Full bug chain context
- [[StreamingOrchestrator]] — SSE streaming entry point

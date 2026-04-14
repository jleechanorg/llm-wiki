---
title: "Polling vs Streaming Architecture"
type: source
tags: [streaming, polling, SSE, HTTP, MCP, worldarchitect, world_logic, rewards-engine]
sources: [worldarchitect-rewards-polling-analysis, pr-6265-streaming-passthrough-normalization]
last_updated: 2026-04-14
---

## Summary

The rewards pipeline has **three distinct paths** — two push-based and one pull-based. The frontend does NOT poll via HTTP GET after page load. SSE streaming delivers rewards_box inline. MCP polling is for external clients only.

## The Three Paths

### Path A: Streaming (Primary — SSE Push)

```
Frontend → POST /api/campaigns/<id>/interaction/stream → SSE stream
         ← rewards_box returned inline in SSE "done" event ←
```

**How it works:**
1. Frontend POSTs to `/interaction/stream` with story payload
2. Backend processes via `llm_parser.py` (v4) or `streaming_orchestrator.py` (current)
3. LLM response is parsed and rewards are computed
4. SSE stream delivers story chunks as they arrive
5. **Final `done` event contains the `rewards_box`** — no separate request needed
6. Frontend reads `rewards_box` from the done event payload

**Key point:** This is **push**, not pull. The frontend never calls `get_campaign_state` after receiving an SSE done event to check for rewards.

**Source:** `streaming_orchestrator.py:709` — done event handler extracts `rewards_box` from the response dict.

### Path B: HTTP GET — Page Load Only

```
Frontend → GET /api/campaigns/<id> → get_campaign_state_unified
```

**How it works:**
1. User navigates to a campaign page (full page load)
2. Frontend calls `GET /api/campaigns/<id>` via REST
3. Backend runs `get_campaign_state_unified()` (world_logic.py:7454-7596)
4. Returns full campaign state including any pending `rewards_box`
5. Frontend renders the page with current rewards_box state

**Key point:** This path is for **initial page load only**. After the page renders, the frontend establishes an SSE connection (Path A). It does NOT repeatedly poll this endpoint.

**Source:** `world_logic.py:get_campaign_state_unified` lines 7454-7596.

### Path C: MCP Polling — External Clients

```
External Client (mobile, integrations) → get_campaign_state MCP tool → Firestore → game_state
```

**How it works:**
1. External MCP client calls `get_campaign_state` tool
2. Tool calls `get_campaign_state_unified()` with the campaign_id
3. If `game_state.rewards_pending` has a pending `rewards_box`, it's returned
4. If story entries have pending rewards but `rewards_box` is empty (stale story), the polling path builds one from scratch

**Key point:** This is **true polling**. The MCP client repeatedly calls this tool. The idempotency of `rewards_engine.canonicalize_rewards()` is critical here — repeated calls with the same game_state must produce identical results.

**Trigger condition:** When a story entry has `rewards_pending` set but no `rewards_box` in `game_state` (stale story recovery scenario).

## DeferredRewardsProtocol — LLM Instruction, Not Timer

**Critical finding:** `DeferredRewardsProtocol` is NOT a server-side timer or cron job.

The protocol is an **LLM prompt instruction** embedded in the system prompt:

> "Every 10 player turns, check whether any rewards have been missed and synthesize appropriate rewards."

**How it works:**
1. The LLM counts player turns from the story narrative
2. At approximately every 10 turns, the LLM generates a special "check" turn
3. The backend recognizes this pattern and calls `rewards_engine.canonicalize_rewards()` to fill in any missed rewards
4. Because `rewards_engine` uses `rewards_processed` flags, it won't double-count

**Why this matters:** There is no server-side polling loop. The LLM itself is the clock. This makes the protocol lightweight but dependent on LLM turn-counting accuracy.

**Source:** System prompt fragments in `streaming_orchestrator.py` and `world_logic.py` — look for "every 10 turns" / "deferred rewards" in prompt strings.

## v4 Convergence Point

In the v4 design, all 3 paths converge on the same rewards engine entry points:

```
Path A (SSE):  llm_parser.py → rewards_engine.canonicalize_rewards()
Path B (GET):  llm_parser.py → rewards_engine.project_level_up_ui()
Path C (MCP):  llm_parser.py → rewards_engine.project_level_up_ui()
```

Both `canonicalize_rewards()` and `project_level_up_ui()` converge on `_canonicalize_core()`. This means every path produces identical rewards_box output for the same game state.

## Polling Path Detail (Path C / Path B)

The polling path (`project_level_up_ui`) specifically handles:

```
get_campaign_state_unified()
  └→ _project_level_up_ui_from_game_state()
       └→ game_state.resolve_level_progression_state()
       └→ game_state.resolve_level_up_signal()
       └→ game_state.ensure_level_up_rewards_pending()
       └→ rewards_engine.build_level_up_rewards_box()
       └→ _enforce_rewards_box_planning_atomicity()
```

This path is used when the frontend needs to check for missed rewards (stale story recovery) or when an external client polls for state.

## Connections

- [[LevelUpPolling]] — Concept page for the polling pattern
- [[LevelUpCodeArchitecture]] — Full architecture including all 3 paths
- [[DeferredRewardsProtocol]] — LLM-driven deferred rewards mechanism
- [[RewardsBoxAtomicity]] — rewards_box and planning_block consistency
- [[StreamingOrchestrator]] — SSE streaming entry point

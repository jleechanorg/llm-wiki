---
title: "Living World"
type: concept
tags: [game-feature, world-simulation, state-tracking]
sources: []
last_updated: 2026-04-08
---

## Definition
World simulation system that tracks player_turn counters, generates world_events with turn_generated timestamps, and maintains faction_updates, time_events, rumors, scene_events, and complications. The Living World persists across sessions and is serialized through GameState.to_model()/from_model().

## Key Components
- **player_turn**: Counter that increments on non-GOD actions
- **world_events**: Background events annotated with turn_generated
- **custom_campaign_state**: Container for living world data
- **_has_visible_living_world_data()**: Server-side visibility helper

## Related Tests
- [[Living World End-to-End Integration Tests]] — validates E2E behavior
- [[Living World Round-trip Tests]] — validates serialization preservation

## Connections
- [[GameState]] — serializes living world data
- [[God Mode]] — does not increment player_turn

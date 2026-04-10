---
title: "World Data"
type: concept
tags: [world-data, game-state, time, data-extraction]
sources: [session-header-utilities]
last_updated: 2026-04-08
---

## Definition
A dictionary within game_state containing world-level information including current time, world time details (year, month, day, hour, minute, second), and other world state.

## Extraction Pattern
```python
def _get_world_data(game_state):
    if isinstance(game_state, dict):
        world_data = game_state.get("world_data", {}) or {}
        return world_data if isinstance(world_data, dict) else {}
    if hasattr(game_state, "world_data"):
        world_data = game_state.world_data or {}
        return world_data if isinstance(world_data, dict) else {}
    return {}
```

## Key Fields
- current_time — string representation of current time
- world_time — dict with year, month, day, hour, minute, second

## Related Concepts
- [[GameState]] — parent structure
- [[SessionHeader]] — uses timestamp from world data

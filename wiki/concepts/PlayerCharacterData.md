---
title: "Player Character Data"
type: concept
tags: [player-character, game-state, data-extraction]
sources: [session-header-utilities]
last_updated: 2026-04-08
---

## Definition
A dictionary within game_state containing player-specific information including location, status, conditions, and resources.

## Extraction Pattern
```python
def _get_player_character_data(game_state):
    if isinstance(game_state, dict):
        pc_data = game_state.get("player_character_data", {}) or {}
        return pc_data if isinstance(pc_data, dict) else {}
    if hasattr(game_state, "player_character_data"):
        pc_data = game_state.player_character_data or {}
        return pc_data if isinstance(pc_data, dict) else {}
    return {}
```

## Key Fields
- Location — current player location
- Status — current player status
- Conditions — active conditions affecting player
- Resources — player resources (health, mana, etc.)

## Related Concepts
- [[GameState]] — parent structure
- [[SessionHeader]] — uses this data for display

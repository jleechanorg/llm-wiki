---
title: "State Updates"
type: concept
tags: [game-state, mutation, persistence, firestore]
sources: []
last_updated: 2026-04-08
---

## Summary
A dictionary field in the structured response schema that contains game state mutations to apply. The primary mechanism for the LLM to modify persistent game state.

## Structure
```python
state_updates = {
    "npc_data": {
        "goblin_1": {"hp_current": 3}
    }
}
```

## Key Features
- **Nested Dictionaries**: State organized by entity type (npc_data, player_data, etc.)
- **Entity Keys**: Individual entity IDs as keys (e.g., "goblin_1")
- **Field Updates**: Specific fields to update (e.g., hp_current)

## Related Concepts
- [[StructuredResponseSchema]] — parent schema containing state_updates
- [[NPCData]] — NPC state container
- [[GameStatePersistence]] — Firestore storage of state

## Usage
Parsed from LLM response and applied to game state in Firestore, advancing the campaign based on AI-driven narrative.

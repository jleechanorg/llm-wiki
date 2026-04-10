---
title: "GameState"
type: concept
tags: [data-model, game-state, state-management]
sources: []
last_updated: 2026-04-08
---

## Description
Data model representing the complete state of a campaign game session including player characters, NPCs, world data, and combat state.

## Components
- player_character_data: Name, level, HP, string_id
- npc_data: NPCs with roles, HP, presence, consciousness
- world_data: Current location, world time (year, month, day)
- combat_state: In-combat flag
- debug_mode: Debug toggle

## Related
- [[GameState]] (entity) - the implementation
- [[StoryEntry]] - entries recorded in the game

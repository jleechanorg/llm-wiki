---
title: "Game State Schema"
type: concept
tags: [schema, game-state, data-structure, worldarchitect]
sources: ["game-state-schema-field-constants"]
last_updated: 2026-04-08
---

## Definition
The JSON schema defining all possible fields in WorldArchitect.AI's game state. Located at `game_state.schema.json`, it specifies 33 top-level fields and numerous nested object definitions for characters, combat, factions, and world data.

## Key Fields
- **Player Data**: `player_character_data`, `npc_data`, `companion_arc`
- **Gameplay State**: `combat_state`, `encounter_state`, `faction_minigame`
- **World State**: `world_data`, `world_events`, `location`
- **System State**: `user_settings`, `game_state_version`, `session_id`

## Usage
The schema serves as the source of truth for field names. Run `scripts/schema/generate_field_constants.py` after modifying the schema to regenerate Python constants in `field_constants.py`.

## Related Concepts
- [[GameStateSchemaFieldConstants]] — the generated Python constants
- [[DefensiveNumericConverter]] — validates numeric fields in the schema
- [[EntityTrackingSystem]] — tracks entities defined in the schema

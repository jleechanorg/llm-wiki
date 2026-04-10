---
title: "GameStateSchema"
type: entity
tags: [schema, json-schema, game-state]
sources: [schema-strictness-schema-coverage-guard-tests]
last_updated: 2026-04-08
---

JSON Schema definition for game state at mvp_site/schemas/game_state.schema.json. Defines EncounterState, RewardsPending, CustomCampaignState, CombatState, Character, and other types with explicit property definitions.

## Key Definitions
- $defs/EncounterState: encounter_completed, encounter_summary
- $defs/RewardsPending: processed, level_up_available
- $defs/CustomCampaignState: level_up_pending, level_up_in_progress, character_creation_completed, success_streak, core_memories, world_events, last_location
- $defs/CombatState: rewards_processed, budget_warnings_shown

## Related
- [[SchemaStrictness]] — property-level schema enforcement
- [[CheckSchemaCoverage]] — validates code exercises schema paths

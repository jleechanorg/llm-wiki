---
title: "Schema Strictness"
type: concept
tags: [schema, validation, strictness]
sources: [schema-strictness-schema-coverage-guard-tests]
last_updated: 2026-04-08
---

Enforcement that JSON schemas have explicit property definitions rather than allowing arbitrary keys. Tests validate that routing objects (EncounterState, RewardsPending, CustomCampaignState, CombatState) define all required properties explicitly in the schema, preventing runtime state corruption.

## Enforced Properties
- encounter_completed, encounter_summary
- rewards_processed, level_up_available
- level_up_pending, level_up_in_progress, character_creation_completed
- last_location, last_story_mode_sequence_id

## Related
- [[JSONSchema]] — the validation mechanism
- [[GameStateSchema]] — applies strictness to game state

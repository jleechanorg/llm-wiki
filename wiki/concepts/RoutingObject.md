---
title: "Routing Object"
type: concept
tags: [game-state, routing, architecture]
sources: [schema-strictness-schema-coverage-guard-tests]
last_updated: 2026-04-08
---

Game state objects that control flow between game phases (combat, encounters, rewards, character creation). Defined in game_state.schema.json as EncounterState, RewardsPending, CustomCampaignState, and CombatState. Properties in these objects determine which UI modal or game phase activates.

## Routing Properties
- encounter_completed → triggers rewards/next encounter
- rewards_processed → enables combat resolution
- level_up_pending / level_up_in_progress → shows level-up modal
- character_creation_completed → exits character creation

## Related
- [[GameStateSchema]] — defines routing objects
- [[SchemaStrictness]] — validates routing object properties

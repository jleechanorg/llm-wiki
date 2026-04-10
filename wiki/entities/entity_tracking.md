---
title: "entity_tracking"
type: entity
tags: [module, validation, entity-extraction]
sources: [pydantic-validation-entity-tracking-tests]
last_updated: 2026-04-08
---

## Description
Module within mvp_site that handles entity extraction from game state using Pydantic validation. Creates SceneManifest objects from player character data, NPC data, and location information.

## Key Functions
- `create_from_game_state()` — creates SceneManifest from game state dict
- `get_validation_info()` — returns validation type and Pydantic availability

## Data Structures
- [[SceneManifest]] — main output model
- PlayerCharacter — validated player data
- NPC — validated NPC data

## Performance
~333 ops/sec for 100 iterations with full validation pipeline

## Connections
- Uses: [[Pydantic]] for validation
- Related: [[DefensiveNumericConverter]]

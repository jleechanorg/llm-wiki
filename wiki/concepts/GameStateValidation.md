---
title: "Game State Validation"
type: concept
tags: [validation, game-state, schema]
sources: [validation-module-coverage-tests]
last_updated: 2026-04-08
---

## Definition
Validation of game state objects in the mvp_site system. Uses is_valid_game_state() to check validity, validates game_state_version presence, and ensures proper structure through JSON Schema validation.

## Validation Functions
- is_valid_game_state(): Boolean check for valid game state
- get_game_state_top_level_properties(): Extract top-level properties
- get_common_field_paths(): Identify shared field paths

## Related Concepts
- [[JSONSchemaValidation]] — underlying validation mechanism
- [[SchemaValidation]] — general validation concept
- [[FirestoreDataValidation]] — persistence layer validation

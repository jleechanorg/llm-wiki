---
title: "EntityInstructionGenerator"
type: entity
tags: [class, entity-tracking]
sources: [generic-entity-tracking-tests]
last_updated: 2026-04-08
---

Class responsible for generating entity instruction text for the LLM context. After refactoring, uses semantic understanding rather than hardcoded entity-specific methods.

## Key Methods
- `generate_entity_instructions()` - Main method generating instructions from entity lists
- `_is_player_character()` - Returns False for all entities (no hardcoding)
- `_is_location_owner()` - Returns False for all location/entity pairs (disabled)

## Known Test Coverage
- [[Generic Entity TrackingTests]] - Tests for hardcoded reference removal

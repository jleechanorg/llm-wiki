---
title: "Pydantic Schema Models for Entity Tracking"
type: source
tags: [python, pydantic, entity-tracking, schema, validation, game-mechanics]
source_file: "raw/pydantic-entity-schema.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module defining Pydantic schema models for entity tracking in WorldArchitect.AI Milestone 0.4. Uses sequence ID format `{type}_{name}_{sequence}` with defensive numeric conversion for robust data handling. Provides type-safe enums for entity types, combat disposition, status, and visibility.

## Key Claims
- **Sequence ID Format**: `{type}_{name}_{sequence}` pattern for unique entity identification
- **Defensive Conversion**: Field validators use DefensiveNumericConverter for robust data handling
- **Type-Safe Enums**: CombatDisposition provides schema-level safety vs legacy string-based classification
- **Name Sanitization**: `sanitize_entity_name_for_id()` converts special characters to underscores
- **D&D Stats**: Stats model with six ability scores (1-30 range) with field validation

## Key Technical Details
- EntityType enum: PLAYER_CHARACTER, NPC, CREATURE, LOCATION, ITEM, FACTION, OBJECT
- CombatDisposition: FRIENDLY, HOSTILE, NEUTRAL with `from_type_string()` converter
- EntityStatus: CONSCIOUS, UNCONSCIOUS, DEAD, HIDDEN, INVISIBLE, PARALYZED, STUNNED
- Visibility: VISIBLE, HIDDEN, INVISIBLE, OBSCURED, DARKNESS
- Imports: defensive_numeric_converter, constants (FRIENDLY_COMBATANT_TYPES, NEUTRAL_COMBATANT_TYPES)

## Connections
- [[DefensiveNumericConverter]] — imported and used for field validation
- [[SharedConstantsConfiguration]] — provides FRIENDLY_COMBATANT_TYPES and NEUTRAL_COMBATANT_TYPES

## Contradictions
- []

---
title: "EntitySchema"
type: concept
tags: [entity-tracking, schema, pydantic, validation, id-generation]
sources: [mvp-site-entities-pydantic]
last_updated: 2026-04-14
---

## Summary

Pydantic-based schema system for entity tracking in WorldAI campaigns. Defines entity types, combat disposition classification, and sanitized ID generation. Ensures entity data conforms to a validated structure across the application with type-safe field definitions and robust numeric handling via DefensiveNumericConverter.

## Key Claims

### EntityType Enum
- `PLAYER_CHARACTER` — user-controlled characters
- `NPC` — non-player characters
- `CREATURE` — monsters and beasts
- `LOCATION` — places and areas
- `ITEM` — objects and equipment
- `FACTION` — organizations and groups
- `OBJECT` — misc physical objects

### CombatDisposition Classification
- `FRIENDLY`: PC/companions — preserved on defeat
- `HOSTILE`: enemies — removed on defeat
- `NEUTRAL`: bystanders — unaffected by combat resolution

### ID Sanitization
- `sanitize_entity_name_for_id()` converts entity names to valid ID format
- Output: lowercase with underscores (e.g., "Goblin Archer" → "goblin_archer")

## Connections

- [[EntityTracking]] — entity lifecycle management
- [[SceneManifest]] — scene-level entity tracking
- [[CombatSystem]] — combat disposition applied during encounters
- [[mvp-site-entities-pydantic]] — Pydantic model implementation
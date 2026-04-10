---
title: "DefensiveNumericConverter"
type: entity
tags: [schema, pydantic, validation]
sources: ["defensive-numeric-converter-tests"]
last_updated: 2026-04-08
---

Defensive numeric conversion schema class that safely handles unknown/invalid values by applying sensible defaults. Part of the mvp_site.schemas.defensive_numeric_converter module.

## Key Behavior
- **HP fields** (hp, hp_max): defaults to 1 for unknown values
- **temp_hp**: defaults to 0 for unknown values
- **Ability scores** (strength, dexterity, constitution, intelligence, wisdom, charisma): defaults to 10
- **Level**: defaults to 1
- **Resource fields** (gold, initiative): defaults to 0

## Range Constraints
- HP minimum: 1
- temp_hp minimum: 0
- Ability scores: clamped 1-30

## Methods
- `convert_value(field_name, value)` — converts a single value with field-specific logic
- `convert_dict(data)` — recursively processes dictionaries, preserving non-numeric fields

## Used By
- [[EntitiesPydantic]] — Character and NPC schema validation

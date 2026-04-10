---
title: "Literal Types"
type: concept
tags: [python, typing, validation]
sources: [shared-type-definitions]
last_updated: 2026-04-08
---

## Description
Python Literal type restricts a value to a specific set of constant values, enabling compile-time validation.

## Usage in WorldArchitect.AI
Three Literal constants:
- VALID_ENTITY_TYPES: character, npc, creature, location, item
- VALID_CAMPAIGN_STATES: active, paused, completed, archived
- VALID_LOG_LEVELS: DEBUG, INFO, WARNING, ERROR, CRITICAL

## Benefits
- Catches invalid values at type-check time
- Self-documenting validation rules
- IDE autocomplete for allowed values

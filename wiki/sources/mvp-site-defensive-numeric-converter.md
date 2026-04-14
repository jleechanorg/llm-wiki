---
title: "mvp_site defensive_numeric_converter"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/defensive_numeric_converter.py
---

## Summary
Defensive numeric field converter handling unknown and invalid values in game state fields. Converts numeric fields with safe defaults for HP, ability scores, gold, experience, and combat statistics.

## Key Claims
- DefensiveNumericConverter.convert_value() with defensive handling of unknown/invalid values
- HP_FIELDS: hp, hp_current, hp_max, level (minimum 1 for living entities)
- NON_NEGATIVE_FIELDS: temp_hp, xp, gold, damage, healing, initiative
- ABILITY_SCORE_FIELDS: strength, dexterity, constitution, intelligence, wisdom, charisma
- FIELD_DEFAULTS provides safe defaults for all numeric fields

## Connections
- [[GameState]] — defensive numeric conversion for game state fields
- [[Validation]] — input validation for numeric fields

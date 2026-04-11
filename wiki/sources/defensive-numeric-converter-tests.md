---
title: "DefensiveNumericConverter Tests"
type: source
tags: [python, testing, validation, schema, pydantic]
source_file: "raw/test_defensive_numeric_converter.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests for the `DefensiveNumericConverter` schema class that provides defensive conversion of numeric values with sensible defaults. Tests validate handling of unknown/invalid values across HP, ability scores, level, and resource fields.

## Key Claims
- **HP Unknown Values**: "unknown", None, or invalid strings convert to 1 for hp/hp_max, 0 for temp_hp
- **Ability Score Defaults**: Unknown values default to 10 (standard D&D baseline)
- **Level Default**: Unknown values default to 1
- **Resource Fields**: gold and initiative default to 0 for unknown values
- **Range Validation**: HP minimum 1, temp_hp minimum 0, ability scores clamped 1-30
- **Dictionary Conversion**: `convert_dict()` recursively processes nested dictionaries

## Key Test Cases
- `test_hp_unknown_values` — validates hp, hp_max, temp_hp with unknown/None/invalid inputs
- `test_stats_unknown_values` — validates all six ability scores (STR, DEX, CON, INT, WIS, CHA)
- `test_level_unknown_values` — validates level field default
- `test_non_hp_defaults` — validates gold and initiative defaults
- `test_numeric_string_conversion` — validates valid numeric strings convert correctly
- `test_range_validation` — validates clamping behavior for out-of-range values
- `test_dict_conversion` — validates recursive dictionary processing

## Connections
- [[DefensiveNumericConverter]] — the schema class being tested
- [[EntitiesPydantic]] — contains Character, EntityType, HealthStatus, Stats classes

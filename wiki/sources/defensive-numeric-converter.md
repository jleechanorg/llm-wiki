---
title: "Defensive Numeric Converter"
type: source
tags: [python, validation, type-conversion, defensive-programming, worldarchitect]
source_file: "raw/defensive-numeric-converter.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python utility class that defensively converts numeric fields with fallback defaults for unknown/invalid values. Handles D&D-style game fields including HP, ability scores, resources, and combat statistics with field-specific validation rules ensuring values stay within valid ranges.

## Key Claims
- **Field-Specific Defaults**: Provides safe default values for different field categories (HP defaults to 1, resources default to 0, ability scores default to 10)
- **Field Category Validation**: Groups fields into HP_FIELDS, NON_NEGATIVE_FIELDS, and ABILITY_SCORE_FIELDS with different validation rules
- **Range Enforcement**: HP fields minimum 1, non-negative fields minimum 0, ability scores clamped to 1-30
- **Recursive Processing**: `convert_dict()` handles nested dictionaries and lists

## Key Quotes
> "When invalid values are encountered, logs warnings and uses safe defaults." — docstring

## Connections
- [[WorldArchitect.AI]] — part of the MVP site codebase
- [[DefensiveProgramming]] — concept of handling invalid values gracefully

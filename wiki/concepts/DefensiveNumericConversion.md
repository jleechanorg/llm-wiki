---
title: "DefensiveNumericConversion"
type: concept
tags: [validation, schema, defaults]
sources: ["defensive-numeric-converter-tests"]
last_updated: 2026-04-08
---

A defensive programming pattern where numeric fields gracefully handle unknown/invalid input by applying sensible defaults rather than raising errors.

## Pattern Details
- Unknown string values ("unknown", "invalid", None) convert to field-specific defaults
- Numeric strings ("5") convert to actual integers
- Out-of-range values get clamped to valid bounds

## Default Mapping
| Field Type | Default | Notes |
|------------|---------|-------|
| HP, HP_MAX | 1 | Minimum 1 |
| temp_hp | 0 | Minimum 0 |
| Ability Scores | 10 | Clamped 1-30 |
| Level | 1 | Minimum 1 |
| gold, initiative | 0 | Minimum 0 |

## Benefits
- Prevents crashes from malformed data
- Provides predictable fallback behavior
- Enables partial data loading with sensible defaults

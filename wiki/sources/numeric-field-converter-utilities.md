---
title: "Numeric Field Converter Utilities"
type: source
tags: [python, utilities, type-coercion, data-layer, firestore]
source_file: "raw/numeric-field-converter-utilities.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python utility class providing simple string-to-integer conversion for data layer operations, particularly Firestore. Offers both field-specific and general-purpose conversion methods with nested structure support.

## Key Claims
- **Field-Specific Conversion**: `convert_dict_with_fields()` only converts specified numeric fields
- **General Conversion**: `convert_all_possible_ints()` auto-detects and converts any integer-like strings
- **Nested Structure Support**: Handles nested dictionaries and lists recursively
- **Backward Compatibility**: Legacy methods delegate to new implementations

## Key Methods
- `try_convert_to_int()` — Attempts conversion, returns original on failure
- `convert_dict_with_fields()` — Converts only named fields to integers
- `convert_all_possible_ints()` — Auto-converts all integer-like string values

## Connections
- Related to [[Centralized Numeric Conversion Utilities]] — this is the simpler counterpart for basic needs
- Used in data layer for [[Firestore]] document field processing

## Contradictions
- []

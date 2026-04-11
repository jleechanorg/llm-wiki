---
title: "NumericFieldConverter Tests"
type: source
tags: [python, testing, type-conversion, dictionary-processing]
source_file: "raw/test_numeric_field_converter.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests for the refactored NumericFieldConverter class. Tests validate string-to-int conversion, nested dictionary processing, list handling, and the convert_all_possible_ints utility method that automatically converts all integer-string values in a dictionary.

## Key Claims
- **Type conversion**: String values like "123" convert to integers while preserving non-numeric strings
- **Field-specific conversion**: convert_dict_with_fields converts only specified fields (hp, level, strength)
- **Nested processing**: Handles deeply nested dictionaries and lists recursively
- **Auto-conversion**: convert_all_possible_ints converts all valid integer strings without specifying fields
- **Non-string preservation**: Non-string values (int, None, list, dict) returned unchanged

## Key Tests
- `test_try_convert_to_int_success`: Validates "123" → 123, "0" → 0, "-42" → -42
- `test_try_convert_to_int_failure`: Validates "abc" → "abc", "12.5" → "12.5" return unchanged
- `test_convert_dict_with_fields`: Validates targeted field conversion (hp, level, strength)
- `test_convert_dict_with_fields_nested`: Validates nested dict processing
- `test_convert_dict_with_fields_list`: Validates list item processing
- `test_convert_all_possible_ints`: Validates automatic conversion of all valid integer strings

## Connections
- [[NumericFieldConverter]] — the class under test
- [[Type Conversion]] — the concept of converting string values to integers

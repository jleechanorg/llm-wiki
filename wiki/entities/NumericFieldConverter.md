---
title: "NumericFieldConverter"
type: entity
tags: [python, utility, type-conversion]
sources: ["numeric-field-converter-tests"]
last_updated: 2026-04-08
---

## Description
Python utility class for converting string values to integers in dictionaries. Provides both field-specific conversion (convert_dict_with_fields) and automatic conversion (convert_all_possible_ints).

## Key Methods
- `try_convert_to_int(value)`: Attempts to convert string to int, returns original value on failure
- `convert_dict_with_fields(dictionary, numeric_fields)`: Converts only specified fields
- `convert_all_possible_ints(dictionary)`: Automatically converts all valid integer strings

## Test Coverage
Validated by unit tests covering success cases, failure cases, nested structures, and list processing.

---
title: "mvp_site numeric_field_converter"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/numeric_field_converter.py
---

## Summary
Numeric field converter utilities for Firestore data layer operations. Provides simple string-to-integer conversion without smart defaults. For robust entity conversion with fallbacks, use DefensiveNumericConverter instead.

## Key Claims
- NumericFieldConverter.try_convert_to_int() returns original if conversion fails
- convert_dict_with_fields() recursively converts specified numeric fields in dictionaries
- Firestore data layer focused (simpler than defensive converter)

## Connections
- [[GameState]] — numeric field conversion for Firestore
- [[Serialization]] — data type conversion

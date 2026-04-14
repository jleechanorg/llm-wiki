---
title: "mvp_site numeric_converters"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/numeric_converters.py
---

## Summary
Centralized numeric conversion utilities providing safe type coercion for various input types (str, float, bool) from JSON/LLM responses. Guards against NaN and Infinity edge cases.

## Key Claims
- coerce_int_safe() safely coerces value to int, handling strings, floats, booleans
- Guards against NaN (ValueError) and Infinity (OverflowError)
- Returns default value (default: 0) if coercion fails

## Connections
- [[Serialization]] — numeric conversion for JSON data

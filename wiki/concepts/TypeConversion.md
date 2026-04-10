---
title: "Type Conversion"
type: concept
tags: [python, programming, data-processing]
sources: ["numeric-field-converter-tests"]
last_updated: 2026-04-08
---

## Description
The process of converting a value from one data type to another. In Python, type conversion can be implicit (automatic) or explicit (using functions like int(), str(), float()).

## Related Patterns
- **NumericFieldConverter**: Applies type conversion to dictionary fields
- **String to int**: Converting string representations ("123") to integer values (123)
- **Safe conversion**: Converting with fallback to original value on failure

## Examples from Tests
- "123" → 123 (successful conversion)
- "abc" → "abc" (failed conversion returns original)
- None → None (non-string returned unchanged)

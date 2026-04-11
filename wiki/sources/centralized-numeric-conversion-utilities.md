---
title: "Centralized Numeric Conversion Utilities"
type: source
tags: [python, utilities, type-coercion, validation, error-handling]
source_file: "raw/numeric-conversion-utilities.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module providing safe type coercion functions for handling various input types (str, float, bool) with guards against edge cases like NaN and Infinity. Used for processing LLM responses and JSON data.

## Key Claims
- **Safe Int Coercion**: `coerce_int_safe()` handles string numbers from JSON/LLM responses, floats, and booleans
- **Edge Case Guards**: Explicitly catches ValueError, TypeError, and OverflowError to handle NaN and Infinity
- **Configurable Defaults**: Allows nullable returns or custom default values
- **Boolean Handling**: Explicitly excludes bool from int isinstance check (since bool is subclass of int in Python)

## Key Functions
- `coerce_int_safe(value, default)` — Safely coerce any value to int with default fallback

## Connections
- [[JSONParsingUtilities]] — related JSON parsing utilities for LLM responses
- [[InputValidationUtilities]] — broader input validation context

## Contradictions
- None identified

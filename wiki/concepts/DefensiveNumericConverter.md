---
title: "DefensiveNumericConverter"
type: concept
tags: [utility, type-coercion, error-handling]
sources: [pydantic-validation-entity-tracking-tests]
last_updated: 2026-04-08
---

## Description
Utility class that handles defensive type conversion for numeric fields. Converts invalid types (strings like "unknown", "invalid") to sensible defaults rather than raising exceptions.

## Behavior
- Input: "unknown", "invalid", or non-numeric strings
- Output: Default numeric values (0 for ints, 0.0 for floats)
- Purpose: Graceful degradation when game state contains malformed data

## Test Validation
test_invalid_data_handling verifies that Pydantic validation combined with DefensiveNumericConverter handles:
- hp: "unknown" (string)
- hp_max: "unknown" (string)
- level: "invalid" (string)

Without crashing the validation pipeline.

## Related Concepts
- [[Pydantic]] — works in conjunction with validation
- [[SceneManifest]] — benefits from defensive conversion

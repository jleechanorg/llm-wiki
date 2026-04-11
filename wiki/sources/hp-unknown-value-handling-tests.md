---
title: "HP Unknown Value Handling in HealthStatus"
type: source
tags: [python, testing, pydantic, health-status, validation, defensive-programming]
source_file: "raw/test_hp_unknown_values.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite validating HealthStatus pydantic model handles unknown/invalid HP values gracefully. Tests verify string values like "unknown", "not_a_number", empty strings, None, and negative numbers get converted to safe defaults (1) via DefensiveNumericConverter.

## Key Claims
- **String "unknown" converts to 1**: HP="unknown" becomes hp=1
- **None converts to 1**: HP=None becomes hp=1
- **Invalid strings convert to 1**: "not_a_number", "" convert to 1
- **Numeric strings work**: "5" properly converts to 5
- **Zero gets clamped to 1**: HP=0 gets clamped to minimum of 1
- **Negative values convert to 1**: -5 becomes 1 (DefensiveNumericConverter)
- **HP clamping after conversion**: HP that exceeds converted hp_max gets clamped

## Key Quotes
> "hp must be <= hp_max after conversion" — validation ensures HP never exceeds hp_max after string conversion

## Connections
- [[HealthStatus]] — pydantic model being tested
- [[DefensiveNumericConverter]] — converter that handles unknown value conversion

## Contradictions
- None identified

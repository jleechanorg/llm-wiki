---
title: "Entity Schema Classes Unit Tests"
type: source
tags: [python, testing, pydantic, validation, schemas, entities]
source_file: "raw/mvp_site_all/test_entities_pydantic_integration.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests validating Pydantic entity schema classes including Stats, HealthStatus, Location, and other entity models. Tests defensive conversion, field validation, range clamping, and error handling for invalid inputs.

## Key Claims
- **Entity ID Validation**: Invalid entity ID formats are rejected with ValidationError
- **Defensive Field Conversion**: String numeric values are converted to integers; unknown values fall back to defaults
- **Stats Range Clamping**: Strength, dexterity, and other stats are clamped to valid range (1-30)
- **HP Validation**: HP is clamped to hp_max when exceeding maximum
- **Condition Handling**: HealthStatus tracks conditions like "poisoned", "blinded"
- **Death Saves**: HealthStatus tracks death saves with successes/failures counters

## Key Test Classes
- `TestPydanticValidation`: Entity ID format validation, field validation with defensive conversion
- `TestStats`: Default/custom values, string conversion, unknown value handling, range clamping
- `TestHealthStatus`: Basic creation, conditions, HP clamping, unknown value handling

## Connections
- [[PydanticEntityIntegration]] — schema validation framework used
- [[Stats]] — D&D ability score entity
- [[HealthStatus]] — character health tracking entity
- [[DefensiveNumericConverter]] — converts unknown values to safe defaults

## Contradictions
- None identified

---
title: "Pydantic Validation"
type: concept
tags: [python, validation, pydantic, schemas]
sources: ["entity-schema-classes-unit-tests"]
last_updated: 2026-04-08
---

## Definition
Pydantic is a Python data validation library using Python type annotations to define schema constraints. Used in this codebase for entity schemas (NPC, PlayerCharacter, Stats, HealthStatus).

## Key Patterns
- **Field Validation**: Automatically validates input types and ranges
- **Defensive Conversion**: Converts invalid values to safe defaults
- **Error Raising**: Raises ValidationError for invalid entity ID formats
- **Range Clamping**: Numeric values clamped to min/max bounds

## Related Concepts
- [[DefensiveNumericConverter]] — handles unknown value conversion
- [[EntitySchemas]] — concrete entity models using Pydantic

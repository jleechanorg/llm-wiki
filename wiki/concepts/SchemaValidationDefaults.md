---
title: "SchemaValidationDefaults"
type: concept
tags: [pydantic, validation, defaults]
sources: ["defensive-numeric-converter-tests"]
last_updated: 2026-04-08
---

Pydantic schema pattern where validation includes implicit default values for missing or invalid fields rather than strict type checking.

## Related Concepts
- [[DefensiveNumericConversion]] — specific implementation for numeric fields
- Schema field validators — custom validation logic in Pydantic models
- Field coercion — automatic type conversion during validation

## Comparison
- **Strict validation**: rejects invalid input with errors
- **Validation with defaults**: converts invalid input to sensible defaults (this pattern)

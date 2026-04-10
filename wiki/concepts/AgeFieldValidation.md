---
title: "Age Field Validation"
type: concept
tags: [concept, validation, pydantic, character-schema]
sources: [age-field-validation-character-classes]
last_updated: 2026-04-08
---

Pydantic-based validation for character age fields. Enforces integer type and 0-50000 range.

## Validation Rules
- Must be integer (no floats, strings, objects)
- Must be >= 0
- Must be <= 50000
- Optional field (defaults to None)

## Use Cases
- Historical characters (50-100)
- Fantasy beings (100-5000)
- Immortal entities (50000)

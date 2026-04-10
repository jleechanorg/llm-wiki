---
title: "Schema-Derived Enums"
type: concept
tags: [schema-validation, enums, architecture, code-quality]
sources: []
last_updated: 2026-04-08
---

## Definition
A pattern where enum values are dynamically imported from a schema validation module rather than hardcoded in application code. Ensures consistency between validation rules and runtime values.

## Key Principles
- Single source of truth for valid values
- Runtime imports prevent drift between schema and code
- Enables dynamic validation without code changes

## Related Patterns
- [[Schema Validation]]
- [[Enum Normalization]]

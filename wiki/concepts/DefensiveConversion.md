---
title: "Defensive Conversion"
type: concept
tags: [python, validation, defensive-programming, type-conversion]
sources: ["entity-schema-classes-unit-tests"]
last_updated: 2026-04-08
---

## Definition
Pattern where invalid or unknown input values are converted to safe defaults rather than raising errors. Used throughout entity schemas to handle malformed data gracefully.

## Key Behaviors
- **String to Int**: "15" → 15
- **Unknown Values**: "unknown", null → default (e.g., 10 for Stats)
- **Range Clamping**: Values outside 1-30 → 1 or 30
- **HP Clamping**: hp > hp_max → hp_max

## Related Concepts
- [[PydanticValidation]] — underlying validation framework
- [[Stats]] — entity using defensive conversion
- [[HealthStatus]] — entity using defensive conversion

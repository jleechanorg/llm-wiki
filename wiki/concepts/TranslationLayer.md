---
title: "Translation Layer"
type: concept
tags: [architecture, translation, data-transformation]
sources: [field-format-validation-red-green-test]
last_updated: 2026-04-08
---

## Summary
Architecture pattern where an intermediate layer transforms data between producer and consumer. Translation layers are common sources of field format mismatches.

## Key Principles
- **Data Transformation**: Translates between different field formats or data structures
- **Field Mapping**: Must document expected input/output field names
- **Mismatch Risk**: Producer fields must match translator expectations

## Related Patterns
- [[FieldFormatValidation]] — testing approach for translation correctness

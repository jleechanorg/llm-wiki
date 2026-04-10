---
title: "Field Format Validation"
type: concept
tags: [testing, data-validation, field-consistency]
sources: [field-format-validation-red-green-test]
last_updated: 2026-04-08
---

## Summary
Testing approach ensuring consistent field formats between data producers and consumers. Field format validation catches mismatches early by testing expected vs actual field names.

## Key Principles
- **Producer-Consumer Contracts**: Data producers (world_logic.py) and consumers (main.py) must agree on field names
- **Early Detection**: Unit tests validate field format before integration errors occur
- **Field Mismatch Symptoms**: Wrong field names result in empty/null data despite valid data existing under different field names

## Related Patterns
- [[RedGreenTesting]] — test-first approach to validation
- [[TranslationLayer]] — data transformation between layers

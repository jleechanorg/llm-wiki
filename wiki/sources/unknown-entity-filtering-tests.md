---
title: "Unknown Entity Filtering Tests"
type: source
tags: [testing, entity-validation, tdd, mvp-site]
source_file: "raw/unknown_entity_filtering_test.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests verifying that "Unknown" is properly filtered from entity validation in the EntityValidator class. Tests ensure that placeholder entities don't trigger false validation failures when expected entities contain only placeholder values.

## Key Claims
- **Placeholder Filtering**: "Unknown" entity is filtered out during validation so it doesn't count as a missing entity
- **Empty Validation Pass**: When only "Unknown" is in expected entities, validation should pass since no real entities are expected
- **Real Entity Reporting**: Only actual missing entities (like "Sir Galahad", "Dragon") are reported as missing
- **Case Insensitive**: Filtering works for both "Unknown" and "unknown"

## Test Coverage
- `test_unknown_filtered_from_validation`: Verifies Unknown is filtered from missing_entities list
- `test_empty_expected_entities_after_filtering`: Verifies validation passes when only Unknown is expected

## Connections
- [[EntityValidator]] — class being tested
- [[EntityValidation]] — concept of validating entity presence in narratives

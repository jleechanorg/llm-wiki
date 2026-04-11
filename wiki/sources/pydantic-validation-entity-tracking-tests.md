---
title: "Pydantic Validation Entity Tracking Tests"
type: source
tags: [testing, pydantic, validation, entity-tracking, performance, tdd]
source_file: "raw/pydantic_validation_test.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests validating Pydantic-based entity tracking in the mvp_site module. Tests cover validation performance (100 ops/sec), SceneManifest structure, defensive data conversion, and graceful handling of invalid input types.

## Key Claims
- **Validation Type**: entity_tracking module uses Pydantic for schema validation with VALIDATION_TYPE = "Pydantic"
- **Performance**: 100 iterations complete in under 1 second with defensive numeric conversion
- **Data Structure**: SceneManifest contains player_characters, NPCs, and current_location fields
- **Defensive Conversion**: DefensiveNumericConverter gracefully handles invalid types (string "unknown" → sensible defaults)

## Test Cases
- `test_pydantic_validation_performance`: 100 iterations benchmark with scene manifest creation
- `test_validation_info`: Validates get_validation_info() returns Pydantic settings
- `test_entity_creation_with_validation`: Verifies SceneManifest structure and type annotations
- `test_invalid_data_handling`: Tests graceful handling of malformed game state data

## Key Outputs
```
Pydantic validation: 100 iterations in ~0.3s (333 ops/sec)
Pydantic: Handled invalid data gracefully
```

## Connections
- [[mvp_site]] — containing module for entity_tracking
- [[entity_tracking]] — core module being tested
- [[Pydantic]] — validation framework in use
- [[SceneManifest]] — main data structure
- [[DefensiveNumericConverter]] — handles type coercion for invalid data

## Contradictions
- None identified

---
title: "Architecture Decision Tests (ADTs) - Pydantic Validation"
type: source
tags: [python, testing, unittest, architecture, pydantic, validation]
source_file: "raw/architecture-decision-tests-pydantic-validation.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest suite verifying architectural decisions about Pydantic validation usage in WorldArchitect.AI. Tests confirm that Pydantic is the sole implementation for entity validation, validating that Simple implementation was removed and DefensiveNumericConverter handles edge cases like "unknown" values.

## Key Claims
- **ADT-001**: Entity validation uses Pydantic implementation for robust data validation
- **ADT-002**: Only Pydantic implementation exists — Simple version removed
- **ADT-003**: entity_tracking.py imports from Pydantic module
- **ADT-004**: Pydantic validation actually rejects invalid data (e.g., gender required for NPCs)
- **ADT-005**: DefensiveNumericConverter handles "unknown" values gracefully
- **ADT-006**: No environment variable switching — Pydantic is always used

## Key Test Cases
1. test_adt_001_pydantic_validation_is_used — Verifies Pydantic is used
2. test_adt_002_only_pydantic_implementation_exists — Confirms Simple removed
3. test_adt_003_entity_tracking_imports_pydantic_module — Checks imports
4. test_adt_004_pydantic_validation_actually_rejects_bad_data — Tests rejection
5. test_adt_005_defensive_numeric_conversion_works — Tests edge case handling
6. test_adt_006_no_environment_variable_switching — Tests no env-based switching

## Key Modules Tested
- mvp_site.schemas.entities_pydantic — Primary entity schema implementation
- mvp_site.schemas.defensive_numeric_converter — Edge case numeric conversion
- mvp_site.entity_tracking — Entity state management
- mvp_site.arch — Architecture module

## Connections
- [[PydanticValidation]] — Core validation framework used
- [[DefensiveNumericConverter]] — Handles unknown value conversion
- [[EntityTracking]] — Entity state persistence layer

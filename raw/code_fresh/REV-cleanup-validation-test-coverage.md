# REV: Missing Test Coverage for Cleanup Path Validation Failure

**Status:** COMPLETED
**Priority:** MEDIUM
**Component:** Testing, schema validation
**Created:** 2026-02-08
**Completed:** 2026-02-17

## Problem

The cleanup path validation fallback behavior at `world_logic.py:2003-2012` lacks test coverage. There are no tests verifying what happens when:
- Cleanup path encounters invalid state
- Schema validation fails during cleanup
- Fallback to unvalidated state persists to Firestore

## Impact

**Medium** - Testing gap:
- Behavior is untested and could break silently
- No verification that fallback actually works as intended
- No regression detection if fallback behavior changes
- Harder to refactor with confidence

## Current Test Coverage

`test_schema_validation_enforcement.py` tests:
- ✅ Fresh GameState validation
- ✅ Populated GameState validation
- ✅ Invalid state rejection before Firestore write
- ✅ Production code uses to_validated_dict()
- ✅ Datetime preservation
- ✅ validate_and_correct_state() enforces schema
- ❌ Cleanup path validation failure scenario (MISSING)

## Recommended Solution

Add test to `test_schema_validation_enforcement.py`:

```python
def test_cleanup_path_validation_failure_fallback():
    """
    Verify cleanup path behavior when schema validation fails.

    This documents the current fallback behavior where invalid states
    are persisted with error logging rather than aborting the operation.
    """
    # Setup: Create state that will fail validation after cleanup
    # Expected: Error logged but state persisted anyway
    # OR: Remove fallback and expect ValueError to propagate
```

## Acceptance Criteria

- [x] Test coverage for cleanup path validation failure (verified via test_cleanup_path_validates_non_blocking_behavior)
- [x] Test verifies actual behavior (fallback or strict enforcement)
- [x] Test fails if behavior changes unexpectedly

## Related

- REV-cleanup-validation-fallback: The untested fallback code
- PR #4534: Schema Validation Enforcement
- `test_schema_validation_enforcement.py`: Test file needing coverage

# REV: Inconsistent Validation Enforcement Across Persistence Paths

**Status:** IN PROGRESS
**Priority:** MEDIUM
**Component:** world_logic.py, schema validation
**Created:** 2026-02-08
**Updated:** 2026-02-17

## Problem

Schema validation is documented inconsistently across different persistence paths in world_logic.py:

**Original claim (incorrect):**
- Strict Enforcement (raises ValueError on failure): God Mode SET, God Mode UPDATE, Main narrative
- Fallback Allowed (logs error, persists anyway): Cleanup path (line 2003)

**Actual behavior (all paths non-blocking):**
- God Mode SET: Non-blocking (logs warnings, persists anyway)
- God Mode UPDATE: Non-blocking (logs warnings, persists anyway)
- Main narrative flow: Non-blocking (logs warnings, persists anyway)
- Cleanup path: Non-blocking (logs warnings, persists anyway)

The try/except block in cleanup path (world_logic.py:2003) is defensive but **never triggered** since `validate_and_correct_state()` never raises exceptions.

## Impact

**Medium** - Creates unpredictable behavior:
- Developers don't know which paths enforce validation
- Some invalid states can reach Firestore while others can't
- Debugging is harder when behavior differs by code path
- Users may experience different error handling for the same invalid state

## Root Cause

Ad-hoc error handling added to different paths without consistent policy.

## Recommended Solution

**Option 1:** Standardize on strict enforcement everywhere
- Remove try/except fallback from cleanup path
- All paths raise ValueError on validation failure

**Option 2:** Add explicit `enforce_validation` parameter to validation function
```python
def validate_and_correct_state(
    state_dict: dict[str, Any],
    previous_world_time: dict[str, Any] | None = None,
    return_corrections: bool = False,
    enforce_validation: bool = True,  # New parameter
) -> dict[str, Any] | tuple[dict[str, Any], list[str]]:
```

**Option 3:** Document which paths allow fallback and why

## Acceptance Criteria

- [x] All persistence paths have documented validation behavior (non-blocking everywhere)
- [x] Policy is explicit: validation is non-blocking (warnings only) across ALL paths
- [x] Test coverage for non-blocking behavior (REV-cleanup-validation-test-coverage)

## Resolution

**Chosen: Option 3 - Document the behavior (Non-Blocking Validation)**

Schema validation is **non-blocking by design** across ALL persistence paths:
- Generates `logging_util.warning()` to GCP logs
- Appends to corrections list (if `return_corrections=True`)
- Does NOT raise exceptions
- Does NOT block persistence to Firestore
- Prioritizes gameplay continuity over strict data integrity

This is an architectural decision (not a bug) to allow invalid states to be debugged via logs without disrupting active sessions.

## Related

- REV-cleanup-validation-fallback: Specific instance in cleanup path
- PR #4534: Schema Validation Enforcement
- REV-cleanup-validation-test-coverage: Test coverage for non-blocking behavior

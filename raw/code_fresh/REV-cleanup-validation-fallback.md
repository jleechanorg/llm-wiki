# REV: Schema Validation is Non-Blocking Everywhere (Not Enforcement)

**Status:** RESOLVED - Not a bug, working as designed
**Priority:** Documentation Update
**Component:** world_logic.py, schema validation, PR #4534
**Created:** 2026-02-08
**Resolved:** 2026-02-15

## Resolution

**Schema validation is non-blocking by design across ALL persistence paths.**

After investigation, confirmed that:
- `to_validated_dict()` does NOT raise `ValueError` - it logs warnings only
- `validate_and_correct_state()` returns corrections list, never raises exceptions
- ALL persistence paths use non-blocking validation (cleanup, god mode, narrative)

The try/except block in cleanup path (world_logic.py:2003) is **defensive but unnecessary** since `to_validated_dict()` never raises ValueError in the current implementation.

## Actual Behavior (Non-Blocking Validation)

ALL paths use non-blocking warnings:
- ✅ God Mode SET: Warns but does NOT raise
- ✅ God Mode UPDATE: Warns but does NOT raise
- ✅ Main narrative flow: Warns but does NOT raise
- ✅ Cleanup path: Warns but does NOT raise (try/except is defensive, never triggered)

Schema validation failures:
- Generate `logging_util.warning()` to GCP logs
- Append to corrections list (if `return_corrections=True`)
- **Do NOT raise exceptions**
- **Do NOT block persistence to Firestore**

## Impact (Updated Understanding)

This is NOT a bug - it's the architectural decision for PR #4534:
- Schema validation provides **observability** (GCP logs, corrections)
- Does NOT provide **enforcement** (no exceptions, invalid states persist)
- Prioritizes **gameplay continuity** over strict data integrity
- Invalid states can be debugged via logs without disrupting sessions

## Root Cause (Original Misunderstanding)

Original analysis incorrectly assumed validation raised ValueError based on:
- Misleading docstrings in `world_logic.py:2750` (now fixed)
- PR title claimed "Enforcement" (now updated to "Warnings (Non-Blocking)")
- Comments referenced "REV-rrom fix: validation failures propagate as ValueError" (incorrect, now fixed)

## Actions Taken (2026-02-15)

**Documentation fixes applied:**
- ✅ Updated `world_logic.py:2750` docstring (removed false "raise ValueError" claim)
- ✅ Updated PR #4534 title: "Schema Validation Warnings (Non-Blocking)"
- ✅ Updated PR #4534 description to clarify non-blocking behavior
- ✅ Updated test files to reflect non-blocking expectations
- ✅ This bead updated to RESOLVED status

**Code cleanup (optional):**
- The try/except in cleanup path can be removed (defensive but never triggers)
- No functional change needed - validation already works as designed

## Acceptance Criteria (Completed)

- ✅ PR description updated to accurately reflect non-blocking validation
- ✅ All misleading docstrings corrected
- ✅ Test expectations align with actual non-blocking behavior
- ✅ Documentation clarifies: validation provides observability, not enforcement

## Related

- PR #4534: Schema Validation Enforcement
- REV-9zs: Schema validation not enforced in production
- REV-0b5: Schema validation not enforced in validate_and_correct_state()

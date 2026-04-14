# REV-1qu: PlanningBlock.choices Format Mismatch (dict vs array)

**Status**: CLOSED
**Priority**: HIGH
**Category**: Schema Compliance / Bug Fix
**Related**: PR #4534, docs/pr-4534-comment-resolution.md

## Problem Statement

Different code paths output `planning_block.choices` in inconsistent formats (dict OR array), causing runtime validation failures and type errors in choice processing. This bug was identified in PR #4534 comment analysis.

### Root Cause

The validation code in `narrative_response_schema.py` (lines 2897-3055) had logic to "preserve list format" for choices with colon prefixes (god:/think: style keys), leading to inconsistent output format:
- Some code paths returned `dict` (choice_id → choice_object)
- Other code paths returned `array` of choice objects
- Downstream code expected dict format (using `.items()` iteration)

## Solution Implemented

**Canonical Format**: `planning_block.choices` is ALWAYS a dict (choice_id → PlanningChoice object)

### Code Changes

1. **mvp_site/narrative_response_schema.py**:
   - Removed `preserve_list_format` logic (lines 2899-2904)
   - Always normalize to dict format in validation (line 2947)
   - Always normalize to dict format in sanitization (line 3107-3194)
   - Removed unused `validated_choices_list` variable

2. **mvp_site/campaign_upgrade.py**:
   - `normalize_planning_block_choices()` already converts list to dict (no changes needed)

3. **mvp_site/tests/test_god_mode_planning_blocks.py**:
   - Updated tests to iterate over `choices.values()` instead of `choices` directly
   - Updated tests to use `choices.items()` for dict iteration
   - Tests now correctly expect dict format

4. **mvp_site/tests/test_planning_block_choices_format.py** (NEW):
   - Comprehensive TDD test suite for format standardization
   - 9 tests covering dict/array input, god mode, normalization, round-trip

### Schema Consistency

The JSON schema already defined choices as dict format:
```json
"choices": {
  "type": "object",
  "additionalProperties": { "$ref": "#/$defs/PlanningChoice" }
}
```

Implementation now matches schema (no schema changes needed).

## Testing Evidence

All tests pass with 100% success rate:
- `test_planning_block_choices_format.py`: 9/9 passed
- `test_god_mode_planning_blocks.py`: 6/6 passed
- `test_planning_block_robustness.py`: 11/11 passed

**Total**: 26 tests passed, 0 failures

### Test Coverage

- ✅ Dict format input → dict output
- ✅ Array format input → dict output (conversion)
- ✅ God mode choices with colon prefixes
- ✅ Think mode choices with colon prefixes
- ✅ Auto-generation of missing IDs
- ✅ JSON string input normalization
- ✅ Round-trip serialization
- ✅ Downstream code iteration patterns

## Impact

### Fixed Issues
- ✅ Runtime type errors when iterating choices
- ✅ Validation failures due to format mismatch
- ✅ Inconsistent behavior across response types
- ✅ God mode/think mode choice format instability

### Backwards Compatibility
- **Breaking Change**: Code expecting array format will break
- **Mitigation**: All existing tests updated to use dict format
- **Risk Level**: Low (internal API, no external consumers)

## Related Issues

From `docs/pr-4534-comment-resolution.md`:

> #### Issue 2.1: PlanningBlock.choices Format Inconsistency
> - **Reported**: 4+ times across multiple chunks
> - **File**: `mvp_site/narrative_response_schema.py`
> - **Problem**: Code outputs choices as **dict OR list**, but Pydantic schema expects **array only**
> - **Impact**: Validation failures, runtime type errors
> - **Root Cause**: Duplicated choice format conversion logic (lines 2872-3167)

**Resolution**: Fixed by standardizing to dict format (NOT array as originally stated in report - the schema actually expects dict).

## Verification Commands

```bash
# Run TDD tests
TESTING_AUTH_BYPASS=true python3 -m pytest mvp_site/tests/test_planning_block_choices_format.py -v

# Run god mode tests
TESTING_AUTH_BYPASS=true python3 -m pytest mvp_site/tests/test_god_mode_planning_blocks.py -v

# Run robustness tests
TESTING_AUTH_BYPASS=true python3 -m pytest mvp_site/tests/test_planning_block_robustness.py -v

# Run all planning block tests
TESTING_AUTH_BYPASS=true python3 -m pytest mvp_site/tests/test_planning_block*.py mvp_site/tests/test_god_mode_planning_blocks.py -v
```

## Files Changed

### Modified
- `mvp_site/narrative_response_schema.py` - Standardized to dict format
- `mvp_site/tests/test_god_mode_planning_blocks.py` - Updated for dict iteration

### Added
- `mvp_site/tests/test_planning_block_choices_format.py` - TDD test suite

### No Changes Required
- `mvp_site/campaign_upgrade.py` - Already normalizes to dict
- `mvp_site/schemas/game_state.schema.json` - Already expects dict format

## Lessons Learned

1. **Preserve Single Format**: Don't try to preserve input format when output format should be canonical
2. **Test Coverage**: TDD approach caught edge cases (god mode colons, missing IDs)
3. **Schema First**: Implementation should match schema, not vice versa
4. **Document Intent**: Clear comments about canonical format prevent future bugs

## Closed By

Commit: [To be added after commit]
Date: 2026-02-06

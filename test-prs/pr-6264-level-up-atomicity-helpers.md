# PR #6264: Level-Up Atomicity Helpers + Postcondition Assertions

**URL:** https://github.com/jleechanorg/worldarchitect.ai/pull/6264
**Author:** jleechanorg
**State:** OPEN
**Date:** 2026-04-14

## Summary

Extracts inline stuck-completion reconciliation into `ensure_level_up_rewards_box` and `ensure_level_up_planning_block` module-level helpers. Adds postcondition assertions verifying rewards_box exists whenever level_up_complete=True. TDD: RED tests written first, then GREEN implementation.

## Changes

### Production Code
- `world_logic.py`: `ensure_level_up_rewards_box()` and `ensure_level_up_planning_block()` at module level
- Refactored `_resolve_canonical_level_up_ui_pair` to call helpers
- XP parsing/normalization improvements
- ASI injection extended to full choice sets at ASI levels
- Optional `_process_rewards_followup` for pending rewards surfacing

### Tests
- `mvp_site/tests/test_level_up_atomicity.py`: New file, 9 tests covering stuck-state synthesis and atomicity postconditions
- All new tests pass (RED → GREEN)
- 74 tests total (no regression to existing test_level_up_stale_flags.py and test_level_up_stale_guards.py)

## Key Pattern
**Stuck-Completion Reconciliation**: When `level_up_complete=True` but `rewards_box` is absent, synthesize missing field from canonical game state to satisfy the atomic pair contract.

## Test Impact

Run: `python3 -m pytest mvp_site/tests/test_level_up_atomicity.py -v`

## Risk

Medium — touches core game-loop response assembly (rewards/level-up UI canonicalization), regressions could affect turn processing, UI rendering, or latency.

## Relationship to PRs #6275, #6276
PR #6264 is the predecessor to PR #6275 (stuck-level-up synthesis). PR #6276 (Layer 3 CLEAN) refactors the rewards detection to use rewards_engine public API. Review all three together for atomicity contract compliance.

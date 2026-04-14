# PR #6275: Fix Stuck Level-Up Completion Rewards Box Synthesis

**URL:** https://github.com/jleechanorg/worldarchitect.ai/pull/6275
**Author:** jleechanorg
**State:** OPEN
**Date:** 2026-04-14

## Summary

Fixes stuck level-up: `level_up_complete=True` but `rewards_box` is absent. Adds server-side ASI (Ability Score Improvement) injection at D&D 5e ASI levels (4, 8, 12, 14, 16, 19) and `ensure_level_up_rewards_box` / `ensure_level_up_planning_block` helpers.

## Changes

### Helpers added
- `ensure_level_up_rewards_box()` — ensures rewards_box is present when level_up_complete=True
- `ensure_level_up_planning_block()` — ensures planning_block is present for level-up states

### ASI Injection
- D&D 5e ASI levels: 4, 8, 12, 14, 16, 19
- `_is_asi_level(level)` — checks if level is an ASI level
- `TestLevelUpASIInjection` class — 14 new tests for ASI injection

### Tests
- 14 new tests across 4 test classes in `test_level_up_stale_flags.py`
- Fixes assertion to use field-level comparison rather than object equality

## Test Impact

New unit tests for ASI injection and rewards_box synthesis. Run: `python3 -m pytest mvp_site/tests/test_level_up_stale_flags.py -v`

## Risk

Low — adds new functionality with test coverage.

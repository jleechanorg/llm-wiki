# PR #6272: Stabilize TestStoryPagination Tests Against Real Firestore Fallback

**URL:** https://github.com/jleechanorg/worldarchitect.ai/pull/6272
**Author:** jleechanorg
**State:** OPEN
**Date:** 2026-04-14

## Summary

Replaces `skipTest` guards with explicit `fail()` in TestStoryPagination tests, making precondition violations loud rather than silent skips. Uses FakeFirestore guard pattern and `_coerce_first_valid` helper with DefensiveNumericConverter for robust rewards parsing.

## Changes

### Core Fix
- `_coerce_first_valid(*values)` — tries each value in order, returns first that passes validity check (finite, non-zero-like for numerics)
- `DefensiveNumericConverter` backing for rewards parsing
- Consistent fallback precedence: `rewards_pending` → combat → encounter

### Test Changes
- `test_api_routes.py` — 2 guards changed from `skipTest` → `fail()`
- `test_rewards_box_normalizer_sentinel.py` — +N tests for noisy reward fields and precedence
- `test_rewards_box_robustness.py` — MCP E2E rewards robustness test (real unittest suite)
- `base_test.py` — MCP server shutdown wrapped in try/except

## Key Pattern: FakeFirestore Guard
```python
if not IS_USING_FAKE_FIRESTORE:
    self.fail("Test requires FakeFirestore — real Firestore cannot be used in CI")
```

## Test Impact

Run: `python3 -m pytest mvp_site/tests/test_api_routes.py -v -k "story_pagination" --tb=short`

## Risk

Medium — changes reward extraction/coercion logic affecting what rewards are shown to users.

## Cycle 20 Score

42/100 — BLOCKER: committed merge conflict markers (`<<<<<<< HEAD`) in world_logic.py (FIXED)

## C7 Pattern
**Failed Merge Leaves Committed Conflict Markers** — GitHub shows MERGEABLE but Python would SyntaxError on `<<<<<<<`

# PR #6277: RewardsBox TypedDict + validate_rewards_box() Schema Enforcement

**URL:** https://github.com/jleechanorg/worldarchitect.ai/pull/6277
**Author:** jleechanorg
**State:** OPEN
**Date:** 2026-04-14

## Summary

Adds `RewardsBox` TypedDict and `validate_rewards_box()` strict validator to `mvp_site/custom_types.py`. Establishes canonical schema for the `rewards_box` field structure used throughout the level-up and rewards pipeline.

## Changes

### Files Changed (2)
- `mvp_site/custom_types.py` — +46 lines (RewardsBox TypedDict + validate_rewards_box)
- `mvp_site/tests/test_rewards_box_schema.py` — +174 lines (10/10 tests passing)

### RewardsBox TypedDict
```python
class RewardsBox(TypedDict, total=False):
    level_up_available: bool
    xp_gained: int
    current_xp: int
    next_level_xp: int
    gold: int
    loot: list[str]
    source: str
    progress_percent: float  # optional — total=False
```

### validate_rewards_box()
- Strict validator: rejects string "100", bool "true", wrong types
- Returns `bool` — `False` on any failure
- Uses `RewardsBox.__annotations__` for DRY schema derivation

### Dual-Validator Architecture
- `custom_types.validate_rewards_box` — **strict** validator (post-coercion assertion)
- `narrative_response_schema._validate_rewards_box` — **coercing** validator (input normalization)
- These serve different purposes and are intentionally separate

## Test Impact

10/10 new tests pass in 0.08s. No regressions to existing rewards_box tests. All field names match exactly what `narrative_response_schema.py` and `world_logic.py` use.

Run: `python3 -m pytest mvp_site/tests/test_rewards_box_schema.py -v`

## Risk

Low — schema definition only, not wired to call sites yet. Follow-up PR should wire `validate_rewards_box` into `normalize_rewards_box_for_ui` or `narrative_response_schema`.

## Score (Cycle 22 Self-Critique)

| Dimension | Score |
|-----------|-------|
| Naming & Consistency | PASS |
| Error Handling | MARGINAL (undocumented dual-validator distinction) |
| Type Safety | PASS |
| Test Coverage | PASS |
| Documentation | MARGINAL (no usage examples) |
| Evidence | PASS |

**Overall: 92.5/100 — MERGE**

## Improvement Suggestions

1. Document dual-validator distinction in docstring
2. Wire `validate_rewards_box` into call sites in future PR
3. Remove unused `import typing` in test file

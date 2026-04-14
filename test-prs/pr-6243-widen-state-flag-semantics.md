---
title: "PR #6243: [antig] fix(game-state): widen state flag semantics to accept LLM numeric booleans"
type: test-pr
date: 2026-04-13
pr_number: 6243
files_changed: [game_state.py, test_game_state.py]
---

## Summary
Widens state flag semantics in `game_state.py` so `_is_state_flag_true` also accepts `int(1)` and `"1"` alongside `True` and `"true"`, and `_is_state_flag_false` accepts `int(0)` and `"0"` alongside `False` and `"false"`. Free-text strings like "yes"/"no" remain rejected.

## Key Changes
- **game_state.py**: Added `1` and `"1"` as accepted truthy values, `0` and `"0"` as accepted falsy values
- **test_game_state.py**: Added `StateFlagSemanticsTest` with 5 test methods covering accepted/rejected values, whitespace variants, and bool-subclass edge case

## Diff Snippets
```python
# game_state.py - widened flag semantics
def _is_state_flag_true(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, int) and value == 1:
        return True
    if isinstance(value, str) and value.strip().lower() in ("true", "1"):
        return True
    return False
```

## Motivation
PR #6233 tightened semantics to only accept `True` and `"true"`, but LLM output is unpredictable and commonly uses `1` / `"1"` for boolean fields. This was causing silent level-up stall.
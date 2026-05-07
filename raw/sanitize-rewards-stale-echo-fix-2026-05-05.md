# sanitize_rewards_state_for_context: Level-Up Early-Return Was Stale-Echo Trigger

**Date:** 2026-05-05  
**Bead:** rev-zzxp  
**PR:** investigate-duplicate-xp-rewards (HEAD 08634244e)  
**File:** `mvp_site/rewards_engine.py`

## Problem

`sanitize_rewards_state_for_context()` was supposed to strip `rewards_box` and
`rewards_pending` from game_state before sending to the LLM. However, it contained an
early-return that defeated its own purpose:

```python
if is_level_up_active(game_state_dict):
    rewards_pending = game_state_dict.get("rewards_pending")
    if rewards_pending is None:
        return game_state_dict
    if not isinstance(rewards_pending, dict):
        ...strip rewards_pending only...
    return game_state_dict   # BUG: returns with rewards_box intact
```

When `is_level_up_active()` was True AND `rewards_pending` was a dict, the function
returned the original state unchanged — meaning `rewards_box` (with XP data) stayed in the
LLM prompt. The LLM would then echo this back, causing the backend to award XP a second
time (duplicate XP).

## Fix

Remove the entire level-up-active branch. Strip unconditionally:

```python
sanitized = copy.deepcopy(game_state_dict)
sanitized.pop("rewards_box", None)
sanitized.pop("rewards_pending", None)
return sanitized
```

Level-up state is communicated via `level_up_pending` / `level_up_in_progress` in
`custom_campaign_state`, NOT via `rewards_box` / `rewards_pending` presence.

## TDD Lessons

1. Two unit tests encoded the buggy "preservation" behavior and had to be renamed+inverted:
   - `test_sanitize_rewards_state_preserves_active_level_up` → `test_sanitize_rewards_state_strips_rewards_during_active_level_up`
   - `test_llm_context_preserves_active_level_up_rewards` → `test_llm_context_strips_rewards_during_active_level_up`

2. Red-state test (`testing_mcp/test_stale_echo_red_state.py`) falsely claimed sanitization
   was disabled via `get_server_env_overrides()`. That method only sets streaming/real-mode
   env vars. Fixed: updated docstring to describe PASSES=bug-present, FAILS=fix-working.

## Reusable Pattern

When a "sanitize" function has an early-return bypassing sanitization for a specific state,
that early-return is almost certainly the bug. Sanitization must be unconditional.

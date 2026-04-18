---
title: "Level-Up Atomicity Root Cause Fixes 2026-04-17"
type: source
tags: [worldarchitect-ai, level-up, rewards-engine, world-logic, atomicity, pr6351]
date: 2026-04-17
source_file: raw/level-up-atomicity-root-cause-2026-04-17.md
sources: [level-up-pr6339-verification-status-2026-04-17.md]
last_updated: 2026-04-17
applied_pr: "https://github.com/jleechanorg/worldarchitect.ai/pull/6351"
---

## Summary

Two root-cause bugs in `mvp_site/world_logic.py` caused "LEVEL UP AVAILABLE!" text without clickable planning_block choices. Bug 1: `_enforce_rewards_box_planning_atomicity` unconditionally suppressed `rewards_box` when injection returned None — but XP-driven level-up bypasses the injection path, so suppression was incorrect. Bug 2: `process_action_unified` canonicalizer wiped `planning_block` when `_canon_pb` was None, destroying already-validated injected choices.

## Key Claims

- **Bug 1 (XP-driven bypass)**: `_enforce_rewards_box_planning_atomicity` suppresses `rewards_box` when `_inject_levelup_choices_if_needed` returns None or partial choices. But XP-driven level-up does NOT use injection — it creates `rewards_box` directly from XP threshold crossing. Injection returning None/partial does NOT mean XP-driven level-up is invalid.
- **Fix 1 (5-signal check)**: Before suppressing `rewards_box`, check all 5 level-up signals: `rb_has_level_up`, `_lu_in_progress`, `_lu_pending`, `_lu_complete`, `_xp_driven`. If any is active, keep `rewards_box`.
- **Bug 2 (canonicalizer wipe)**: In `process_action_unified`, when `_canon_pb` is None, the code unconditionally pops `planning_block` from `structured_fields`. This wipes injected level-up choices that were already validated by `_enforce_rewards_box_planning_atomicity`.
- **Fix 2 (level-up signal guard)**: Before popping `planning_block`, check if any level-up signal is active (`_lu_in_progress`, `_lu_pending`, `_lu_complete`, `rewards_pending.level_up_available`). If active, preserve `planning_block`.
- **LLM choices format**: `planning_block.choices` is returned as a LIST of choice objects (each with `id`, `text`, `description` fields), NOT as a dict keyed by choice ID. Test code must normalize.

## Key Quotes

> "Injection failure ≠ XP-driven level-up invalid. The injection function only handles explicit-level-up flows. XP-driven creates rewards_box directly from XP crossing. Check all signals before suppressing."

> "The canonicalizer runs on raw LLM output and may return None for paths where the level-up was injected server-side. The canonicalizer doesn't know about server-side injection."

## Technical Details

### _enforce_rewards_box_planning_atomicity fix (world_logic.py ~2869)

```python
# Before: unconditional suppression
if planning_block is None or not _planning_has_level_up_choices(planning_block):
    rewards_box = None  # WRONG for XP-driven

# After: check all 5 signals
if planning_block is None or not _planning_has_level_up_choices(planning_block):
    _custom = game_state_dict.get("custom_campaign_state") or {}
    _lu_in_progress = _is_state_flag_true(_custom.get("level_up_in_progress"))
    _lu_pending = _is_state_flag_true(_custom.get("level_up_pending"))
    _lu_complete = _is_state_flag_true(_custom.get("level_up_complete"))
    _progression = resolve_level_progression(game_state_dict)
    _xp_driven = _progression.level_up_available
    any_level_up_signal = (
        rb_has_level_up or _lu_in_progress or _lu_pending or
        _lu_complete or _xp_driven
    )
    if not any_level_up_signal:
        rewards_box = None
```

### process_action_unified canonicalizer fix (world_logic.py ~6925)

```python
# Before: unconditional pop
else:
    structured_fields.pop("planning_block", None)  # WRONG

# After: level-up signal guard
else:
    _custom = updated_game_state_dict.get("custom_campaign_state") or {}
    _lu_signals_active = (
        _is_state_flag_true(_custom.get("level_up_in_progress"))
        or _is_state_flag_true(_custom.get("level_up_pending"))
        or _is_state_flag_true(_custom.get("level_up_complete"))
        or _is_state_flag_true(
            updated_game_state_dict.get("rewards_pending", {}).get("level_up_available")
        )
    )
    if not _lu_signals_active:
        structured_fields.pop("planning_block", None)
```

### Choices normalization for tests

```python
if isinstance(choices_raw, list):
    choice_ids = {c.get("id") for c in choices_raw if isinstance(c, dict) and c.get("id")}
elif isinstance(choices_raw, dict):
    choice_ids = set(choices_raw.keys())
else:
    choice_ids = set()
```

## Connections

- [[RewardsEngine]] — canonical rewards computation (`rewards_engine.py`)
- [[WorldLogic]] — modal injection and state management (`world_logic.py`)
- [[LevelUpModalRouting]] — level-up modal flow routing
- [[LevelUpStaleFlagGuards]] — stale flag behavior
- [[PR6339]] — PR containing these fixes
- [[TestingMCP]] — `testing_mcp/test_levelup_strict_repro.py` for strict E2E validation

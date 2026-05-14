# Pre-Modal State Gap in rewards_box Postcondition Enforcement

**Date**: 2026-05-13
**Bead**: rev-cl195
**Commit**: f289b8782fb2393ee11847db4b9dbf956aeaa39d
**PR**: https://github.com/jleechanorg/worldarchitect.ai/pull/6908
**Bug campaign**: iDDyaHbevKSqQHoMUHnu (copied repro: 5sbgLhPsFtqxwfhqLxNq)

## Learning

`_enforce_primary_rewards_box_postcondition` tests with `rewards_pending.level_up_available=True`
must cover all three modal states. The pre-modal state (all flags=None) was the missing gap.

### Modal State Test Matrix

| State | `level_up_pending` | `level_up_in_progress` | Must synthesize rewards_box? |
|-------|--------------------|------------------------|------------------------------|
| pre-modal | None | None | YES — XP threshold crossed |
| active-modal | True | True | YES |
| post-modal/stale | False | False | Only if XP still above threshold |

### Root Cause

Campaign iDDyaHbevKSqQHoMUHnu, turn 8:
- Player level=1, experience.current=396 (above level-2 threshold of 300)
- LLM set `rewards_pending.level_up_available=True, new_level=2` but did NOT emit `rewards_box`
- Deployed version had a stale-suppression path that incorrectly fired when `level_up_pending=None`
  (pre-modal — flags never set yet, not explicitly False)
- `rewards_box=null` was burned into the story entry
- All existing postcondition tests used `level_up_in_progress=True` — none covered pre-modal

### Fix Applied

- Added `test_synthesizes_level_up_rewards_box_in_pre_modal_state` to `test_world_logic.py`
- Added modal state test matrix to `.claude/skills/zfc-leveling-roadmap/SKILL.md`
- Memory: `feedback_2026-05-13_postcondition_modal_state_coverage.md`

### Pattern

Stale-suppression logic uses `is_state_flag_false(value)` which returns False for None.
This means None (unset/pre-modal) DOES NOT trigger suppression in correct code.
A regression that treats None as False burns null rewards_box.

### Verification

```bash
WORLDAI_DEV_MODE=true python -m pytest "mvp_site/tests/test_world_logic.py" \
  -k "test_synthesizes_level_up_rewards_box_in_pre_modal_state" -v
# Result: 1 passed
```

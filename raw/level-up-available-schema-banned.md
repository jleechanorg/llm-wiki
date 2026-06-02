---
name: level-up-available-schema-banned
description: Never add level_up_available to LLM output schema — backend-derived, not model-owned; causes circular dependency
type: feedback
bead: rev-1pmyg
---

## Rule

**Never add `level_up_available` to the LLM output schema (provider_utils.py `NARRATIVE_RESPONSE_SCHEMA`).**

**Why:** `level_up_available` is a backend-derived field — set by `normalize_rewards_box_for_ui()` / `rewards_engine.ensure_rewards_box()`. Adding it to the schema makes the LLM echo it back, and the backend then trusts the echo. This is a circular dependency: backend sets a field → LLM includes it in output → backend reads it as a "model-owned" signal → the field means nothing.

It was deliberately removed from the schema in commit `cf0f21da43` (2026-05-04) and again re-added in PR #7221, then re-removed in commit `20372341` (2026-06-02).

## How to apply

When any code change checks `rewards_box.level_up_available` from game_state as a secondary signal:
- If the game_state field is set by the backend (e.g. `ensure_rewards_box`), do NOT propagate it through the schema
- Replace with `target_level > current_level` using `rewards_box.new_level` / `rewards_box.resolved_target_level` vs `player_character_data.level`

**ZFC-correct signal:** `level_up_signal.target_level > level_up_signal.current_level` (schema fields the model fills in). Secondary backend confirmation: `rewards_box.new_level > player_character_data.level`.

## What was fixed (PR #7221)

**Removed from `provider_utils.py`:**
```python
# BANNED — do not re-add:
"level_up_available": {
    "type": "boolean",
    "description": "True when the player has earned enough XP to level up",
},
```

**Replaced in `rewards_engine.py` `is_level_up_active` lu_pending branch:**
```python
# Before (circular, banned):
rb_confirms = is_state_flag_true(rb.get("level_up_available"))
active = bool(rewards_confirms_level_up or rb_confirms)

# After (ZFC-correct):
rb_target = coerce_int(rb.get("new_level") or rb.get("resolved_target_level") or rb.get("target_level"), default=None)
player_level = coerce_int(player_data.get("level"), default=None)
rb_transition_confirms = rb_target is not None and player_level is not None and rb_target > player_level
active = bool(rewards_confirms_level_up or rb_transition_confirms)
```

## References

- PR: https://github.com/jleechanorg/worldarchitect.ai/pull/7221
- Commit removing it again: `20372341397403affbd4346014563d345c86ca53`
- Original removal commit: `cf0f21da43` (2026-05-04)
- Bead: rev-1pmyg (closed)
- Related: [[zfc-leveling-roadmap]], [[level-up-signal-contract]]

# GameState is NOT a dict — use getattr() not .get()

**Source:** `~/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-05-09_gamestate_not_dict.md`
**Ingested:** 2026-05-09
**Bead:** rev-gm1ax

## Summary

GameState is a custom class with attributes (`self.custom_campaign_state`, `self.combat_state`, `self.world_data`), NOT a dict. Never use `game_state.get("field")` — use `getattr(game_state, "field", default)` or direct attribute access.

## Context

`_ensure_modal_exclusivity()` in `preventive_guards.py` used `game_state.get("custom_campaign_state")` which threw `AttributeError: 'GameState' object has no attribute 'get'`, failing 18/19 tests. The function signature typed `game_state: GameState` but the code assumed dict interface.

## Rule

When writing guards in `preventive_guards.py` or `world_logic.py`, always use `getattr(game_state, "field_name", default)` for GameState objects. Follow patterns like `game_state.world_data`, `game_state.to_dict()` already in the codebase.

## Related Concepts

- [[AdminOverrideContract]]
- [[ModalIntersection]]

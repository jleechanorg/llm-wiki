---
name: GameState is NOT a dict — use getattr() not .get()
description: GameState objects in preventive_guards.py require attribute access (getattr) not dict access (.get); AttributeError regression caught in 18 tests
type: feedback
bead: rev-gm1ax
originSessionId: 16b500e1-a771-4453-b0ce-894c7b015a54
---
GameState is a custom class with attributes (`self.custom_campaign_state`, `self.combat_state`, `self.world_data`), NOT a dict. Never use `game_state.get("custom_campaign_state")` — use `getattr(game_state, "custom_campaign_state", None)` or direct attribute access `game_state.custom_campaign_state`.

**Why:** `_ensure_modal_exclusivity()` in preventive_guards.py used `game_state.get("custom_campaign_state")` which threw `AttributeError: 'GameState' object has no attribute 'get'`, failing 18/19 preventive_guards tests. The function signature said `game_state: GameState` but the code assumed dict interface.

**How to apply:** When writing new guards in preventive_guards.py or world_logic.py, always use `getattr(game_state, "field_name", default)` for GameState objects. Check `game_state.py:1234` for the class definition. Other functions in preventive_guards.py use `game_state.world_data`, `game_state.to_dict()` as patterns — follow those, not dict `.get()`.

**Reference:** `mvp_site/game_state.py:1234` — `self.custom_campaign_state = kwargs.get("custom_campaign_state", {})`

---
title: "Layer 3 CLEAN"
type: concept
tags: [tdd, refactor, cleanup, rewards-engine, level-up]
sources: ["pr6276_design_doc_v4_summary"]
last_updated: 2026-04-15
---

## Definition
Layer 3 CLEAN is the final phase of the RED→GREEN→WIRE→CLEAN TDD process for the v4 rewards engine refactor. After RED tests pass (Layer 0) and GREEN wiring is done (Layer 1-2), Layer 3 focuses on deleting deprecated code and ensuring `world_logic.py` becomes a thin modal wrapper (~1500 lines).

## CLEAN Process
Layer 3 CLEAN for PR #6276 involves:
1. **Delete** deprecated orchestration functions from `world_logic.py`
2. **Redirect** remaining `_is_state_flag_true` usages to `rewards_engine._is_state_flag_true`
3. **Strip** `agents.py` ~110-line `_is_character_creation_or_level_up_active` → 3-line delegate
4. **Add** integration tests from design doc Layer 2
5. **Add** CI gate for `world_logic.py` line count upper bound

## What Gets Deleted
From `world_logic.py`:
- `_maybe_trigger_level_up_modal()` — replaced by `rewards_engine` + thin `inject_modal_state()` wrapper
- `_resolve_canonical_level_up_ui_pair()` — **ALREADY DELETED** ✅
- `_project_level_up_ui_from_game_state()` — replaced by `rewards_engine.project_level_up_ui()`

From `constants.py`:
- `get_xp_for_level` — **DELETED** ✅
- `get_level_from_xp` — **DELETED** ✅

## Current Status (as of 2026-04-15)
- ✅ `_resolve_canonical_level_up_ui_pair` deleted
- ❌ `_maybe_trigger_level_up_modal` still exists (line ~4630)
- ❌ `_project_level_up_ui_from_game_state` still exists
- ❌ world_logic.py at 8729 lines (target ~1500)
- ❌ ~26 `_is_state_flag_true` usages in world_logic.py not redirected
- ❌ agents.py ~110-line function not refactored
- ❌ 4 integration tests not added

## Related Beads
- `rev-v4ci01`: strip world_logic.py to ~1500 lines
- `rev-v4ci02`: add design doc Layer 2 integration tests
- `rev-v4ci03`: agents.py refactor
- `rev-v4ci04`: add CI gate for line count

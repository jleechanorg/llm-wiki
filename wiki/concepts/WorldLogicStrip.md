---
title: "WorldLogic Strip"
type: concept
tags: [world-logic, refactor, rewards-engine, level-up, thin-wrapper]
sources: ["pr6276_design_doc_v4_summary"]
last_updated: 2026-04-15
---

## Definition
"WorldLogic Strip" refers to the Layer 3 CLEAN work of reducing `world_logic.py` from ~8700+ lines to ~1500 lines — a thin modal wrapper that only handles modal presentation logic, delegating all rewards/progression decisions to `rewards_engine.py`.

## Target State
`world_logic.py` should contain ONLY:
- Modal state management functions (`inject_modal_state()`, `dismiss_modal()`, etc.)
- Thin wrappers that call `rewards_engine.py` public API
- No `_is_state_flag_true` implementations (should call `rewards_engine._is_state_flag_true`)
- No direct `canonicalize_rewards`, `project_level_up_ui`, `resolve_level_up_signal` calls

## What Must Be Deleted/Redirected
| Item | Current Location | Action |
|------|-----------------|--------|
| `_maybe_trigger_level_up_modal()` | world_logic.py line ~4630 | DELETE |
| `_resolve_canonical_level_up_ui_pair()` | world_logic.py | **ALREADY DELETED** ✅ |
| `_project_level_up_ui_from_game_state()` | world_logic.py | DELETE |
| `~26 _is_state_flag_true refs` | world_logic.py | Redirect to rewards_engine |
| `_is_state_flag_true` def | game_state.py line 203 | Keep (class-body scope exception) |

## Metrics
- **Before Layer 3**: world_logic.py ~9094-9176 lines
- **After Layer 3 target**: ~1500 lines
- **Lines to remove**: ~7200

## Why It Matters
The scattered architecture (3 copies of `_is_state_flag_true`, 25+ functions) caused:
- Four open PRs (#6262, #6263, #6264, #6268) duplicating each other
- Double-canonicalization bug in non-streaming path
- No clear ownership of rewards/progression decisions

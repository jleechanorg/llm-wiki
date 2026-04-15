# PR #6276: Layer 3 CLEAN — Strip Old Rewards Detection Functions

**URL:** https://github.com/jleechanorg/worldarchitect.ai/pull/6276
**Author:** jleechanorg
**State:** OPEN
**Date:** 2026-04-14

## Summary

Refactors `world_logic.py` to remove deprecated rewards detection functions, wiring it strictly to `rewards_engine` public API. Deletes 91 lines of legacy code. Adds lazy-loading for `llm_service` (840ms cold-start improvement).

## Changes

### Deleted (91 lines removed)
- `build_level_up_rewards_box()` (54 lines) — replaced by `project_level_up_ui()`
- `_project_level_up_ui_from_game_state()` (37 lines) — replaced by `project_level_up_ui()`
- 7 call sites of `resolve_level_up_signal` — replaced by `is_level_up_active()` + `project_level_up_ui()`
- `ensure_rewards_box`, `normalize_rewards_box` from rewards_engine imports

### Added
- `llm_service = _lazy_module("mvp_site.llm_service")` — defers google.genai loading, cuts ~840ms cold-start
- MOCK_SERVICES_MODE guard around Firebase init
- `test_world_logic_no_rewards_detection_functions` (was SKIPPED) now PASSES

### Import changes
- Removed: `resolve_level_up_signal`, `ensure_rewards_box`, `normalize_rewards_box` from rewards_engine
- Kept: `is_level_up_active`, `project_level_up_ui`, `should_show_rewards_box`

## Status Update (2026-04-15)

After PR 6275 merge, PR 6276 is now **CONFLICTING** (mergeable: CONFLICTING, mergeStateStatus: DIRTY). Rebase needed.

- `feat/world-logic-clean-layer3` HEAD: `2e7b4e13f3` (cherry-pick from pr-6275, not rebased to latest main)
- Test failures: 19 failures in test_level_up_stale_flags.py on this branch vs 62/62 on `chore/auto-research-cycle19`
- CodeRabbit: CHANGES_REQUESTED (multiple unresolved threads)

## Architecture

This is Layer 3 of a multi-layer rewards engine single-responsibility refactor:
- Layer 0 RED: 15 failing contract tests for rewards_engine.py
- Layer 1 GREEN: single-responsibility rewards engine (rewards_engine.py owns all normalization)
- Layer 2 RED: integration wiring tests (failing, to be green after WIRE layer)
- Layer 3 CLEAN: world_logic.py strips old detection, uses rewards_engine public API

## Test Impact

`test_world_logic_no_rewards_detection_functions` — was SKIPPED, now passes after this PR.

## Risk

Medium — rewires level-up UI signaling/injection logic, adjusts cold-start initialization behavior.

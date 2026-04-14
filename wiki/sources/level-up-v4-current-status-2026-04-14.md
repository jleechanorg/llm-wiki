---
title: "Level-Up v4 Current Status (2026-04-14)"
type: source
tags: [level-up, rewards-engine, v4, TDD, worldarchitect, status]
date: 2026-04-14
source_file: roadmap/level-up-engine-single-responsibility-design-2026-04-14.md
---

## Summary

The Level-Up v4 single-responsibility refactor is **implemented and deployed**, but **not yet fully fixed**. PR #6273 (`feat/rewards-engine-single-responsibility`) merged all 4 TDD layers (RED → GREEN → WIRE → CLEAN) and deployed to production on 2026-04-14 — but introduced a semantic regression that suppressed all non-level-up XP progress `rewards_box` emissions. PR #6276 (`feat/world_logic: Layer 3 CLEAN`) is OPEN and not yet deployed.

## 4-Layer TDD Status: ALL 4 LAYERS COMPLETE ✅

The design was implemented using a 4-layer TDD methodology. All 4 layers are DONE:

| Layer | Name | Status | Description |
|-------|------|--------|-------------|
| **Layer 0** | RED | ✅ DONE | Contract tests written — all 8 tests FAIL on current main, proving the contract is unsatisfied |
| **Layer 1** | GREEN | ✅ DONE | Pure rewards_engine.py implementation — all 8 tests PASS |
| **Layer 2** | WIRE | ✅ DONE | llm_parser.py wired to rewards_engine (streaming + non-streaming + polling paths) |
| **Layer 3** | CLEAN | ✅ DONE | Deleted duplicate code: _is_state_flag_true (3 copies), duplicate XP math, agents.py 110→3 lines |

### Layer Details

**Layer 0 (RED)**: 8 failing contract tests in `mvp_site/tests/test_rewards_engine.py`:
1. `test_canonicalize_returns_atomic_pair` — both non-None or (None, None)
2. `test_project_level_up_ui_is_pure` — same input → same output, no Firestore writes
3. `test_resolve_level_up_signal_xp_boundary` — XP at threshold → detected
4. `test_canonicalize_core_convergence` — streaming and polling paths produce identical output
5. `test_level_xp_consistency_check` — stored_level vs XP-derived level mismatch warning
6. `test_concurrent_asi_rewards` — Fighter@6 + Rogue@10 in same action
7. `test_zero_xp_is_noop` — xp_gained=0 → no rewards_box emitted
8. `test_single_call_site_invariant` — grep llm_parser.py for exactly 1 canonicalize_rewards call site

**Layer 1 (GREEN)**: `rewards_engine.py` created with full public API. No imports from llm_parser or world_logic. All Layer 0 tests pass.

**Layer 2 (WIRE)**: `llm_parser.py` (renamed from `streaming_orchestrator.py`) wired to call `rewards_engine.canonicalize_rewards()` (streaming/non-streaming) or `rewards_engine.project_level_up_ui()` (polling). Single call site per path. Integration tests pass.

**Layer 3 (CLEAN)**: `world_logic.py` stripped of deprecated rewards detection functions. Deleted: `build_level_up_rewards_box()`, `_project_level_up_ui_from_game_state()`, 7 call sites of `resolve_level_up_signal`. Added lazy-loading for llm_service (saves ~840ms cold-start).

## Semantic Regression Bug

**Critical regression introduced in PR #6273.**

The old `normalize_rewards_box_for_ui()` emitted XP-progress boxes even when `level_up_available=False` (e.g., `xp_gained=50, current_xp=350`). The new `_canonicalize_core()` only emits `rewards_box` when `level_up_available=True` — suppressing all non-level-up XP progress.

### Root Cause

In `rewards_engine._canonicalize_core()` step 5+6:
```python
# Step 5: visibility gate
if normalized_rb and not should_show_rewards_box(normalized_rb):
    normalized_rb = None
    planning_block_data = None  # ← BOTH suppressed
```

`should_show_rewards_box()` only returns True when `level_up_available=True`. This changed the v3 semantic.

### Affected Production Bugs (4 of 6)

| Bug | Campaign | Environment | Symptom | Root Cause |
|-----|----------|-------------|---------|------------|
| Bug 2 | `WQEl4sJb7RqWLndJK4GU` | dev | XP gained, no rewards box | `should_show_rewards_box` suppression |
| Bug 3 | `WQEl4sJb7RqWLndJK4GU` | s10 | Rewards box + planning_block suppressed | Same + step 6 atomicity enforcement |
| Bug 4 | `3JM2gKc3eTFZHQnBtO8m` | s10 | `(None, None)` on non-level-up turns | `_canonicalize_core` early return |
| Bug 6 | `KtKlU0rOV6MmG3b6cOxd` | s10 | Rewards box not showing | `should_show_rewards_box` suppression |

Bug 1 (`wOhBvrJ0gYA2Ox9g1kLC`): "Need to level up to level 1" (should be level 2) — **NOT v4 related**, it's an off-by-one in UI text prompt.

Bug 5 (`gufBO3EVc0GAp5LmVzWG`): Hardcoded HP values in `ensure_planning_block` — partially v4 related (hardcoded values + suppression combined).

## Remaining Work (Post-Deploy)

### Bug 1: Fix should_show_rewards_box XP-Progress Regression

`should_show_rewards_box()` must allow non-level-up XP progress boxes through. Fix: restore XP-progress visibility or rename the function to reflect its new `level_up_available`-only semantics.

**Status**: Open. Fix must be folded into PR #6276 (OPEN) before it merges, or issued as a separate PR.

### Bug 2: Fix project_level_up_ui Void Return

`llm_parser.py:617`: `project_level_up_ui()` is called but its return value is discarded. Commit `8024eba8f` restored the call but it became dead code — the tuple is never captured.

Fix: either capture and use the return value, or remove the dead call.

**Status**: Open.

### Bug 3: Fix Hardcoded HP Values in ensure_planning_block

`ensure_planning_block()` uses hardcoded HP values `{"fighter": 7, "rogue": 6, "wizard": 4}` instead of actual class data. Should query `player_class` from game state.

**Status**: Open.

## PR Status

| PR | Title | Status | Notes |
|----|-------|--------|-------|
| #6273 | feat: rewards engine single-responsibility | **DEPLOYED** — contains regression | All 4 TDD layers complete. Deployed 2026-04-14. |
| #6276 | feat(world_logic): Layer 3 CLEAN — strip old rewards detection | **OPEN** — NOT yet deployed | Strips world_logic.py of deprecated functions. Fix #6273 regression must be folded in here or in a separate PR. |

### Superseded PRs (closed via #6273)
- PR #6262, #6263, #6264, #6268 — all closed with comment linking to v4 design

## Connections

- [[RewardsEngine]] — `should_show_rewards_box`, `_canonicalize_core`, semantic regression
- [[LevelUpCodeArchitecture]] — full architecture, v4 regression analysis
- [[SingleResponsibilityPipeline]] — 7-stage pipeline, single forward pass
- [[Layer3CleanRefactor]] — Layer 3 CLEAN details
- [[LevelUpBugInvestigation]] — prior bug chain (v1-v3 regressions)
- [[FrontendRewardsBoxGate]] — frontend visibility gate for xp_gained

---
title: "Level-Up v4 Semantic Regression: 6 Production Bugs"
type: source
tags: [level-up, rewards-engine, semantic-regression, bugs, worldarchitect]
date: 2026-04-14
source_file: memory/project_2026-04-14_levelup_v4_bug_analysis.md
---

## Summary

PR #6273 deployed a semantic regression in the rewards engine that suppresses ALL non-level-up XP progress `rewards_box` emissions. The old `normalize_rewards_box_for_ui()` emitted XP-progress boxes even when `level_up_available=False`; the new `_canonicalize_core()` only emits when `level_up_available=True`. This caused 4 of 6 production bugs.

## Key Claims

- `_canonicalize_core()` step 5+6 suppresses both `rewards_box` AND `planning_block` when `should_show_rewards_box()` returns False
- `should_show_rewards_box()` only returns True when `level_up_available=True`, blocking all non-level-up XP progress boxes
- `project_level_up_ui()` at `llm_parser.py:617` discards its return value — dead code from rebase restoration
- `ensure_planning_block()` uses hardcoded HP values `{"fighter": 7, "rogue": 6, "wizard": 4}` instead of actual class data
- PR #6273 (GREEN/wired) is deployed to prod; PR #6276 (CLEAN/layer 3) is still OPEN

## Key Quotes

> `_canonicalize_core()` step 5 (line 405): `if normalized_rb and not should_show_rewards_box(normalized_rb):` — when gate returns False, BOTH normalized_rb AND planning_block_data are set to None.

> `llm_parser.py:617`: `rewards_engine.project_level_up_ui(current_game_state.to_dict())` — return value discarded, dead code.

## Bug Table

| Bug | Campaign ID | Environment | Symptom | Root Cause |
|-----|------------|-------------|---------|------------|
| 2 | `WQEl4sJb7RqWLndJK4GU` | dev | XP gained, no rewards box | `should_show_rewards_box` suppression |
| 3 | `WQEl4sJb7RqWLndJK4GU` | s10 | Rewards box + planning_block suppressed | Same + step 6 atomicity |
| 4 | `3JM2gKc3eTFZHQnBtO8m` | s10 | `(None, None)` on non-level-up turns | `_canonicalize_core` early return |
| 5 | `gufBO3EVc0GAp5LmVzWG` | s10 | Hardcoded level-up planning block not showing | Hardcoded HP values + suppression |
| 6 | `KtKlU0rOV6MmG3b6cOxd` | s10 | Rewards box not showing | `should_show_rewards_box` suppression |
| 1 | `wOhBvrJ0gYA2Ox9g1kLC` | dev | "Need to level up to level 1" (should be 2) | Off-by-one in UI text prompt — NOT v4 related |

## Connections

- [[LevelUpCodeArchitecture]] — v4 architecture, single-responsibility pipeline
- [[RewardsEngine]] — `should_show_rewards_box`, `_canonicalize_core`
- [[LevelUpPolling]] — `project_level_up_ui` dead code issue
- [[FrontendRewardsBoxGate]] — frontend visibility gate for xp_gained

## What Needs Fixing

1. `should_show_rewards_box` must allow non-level-up XP progress boxes through
2. `project_level_up_ui()` return value must be captured and used, or call removed
3. Hardcoded HP values in `ensure_planning_block` should use actual class data
4. Fix must fold into PR #6276 (OPEN) before it merges, or issue as separate PR

## PR Status

| PR | Title | Status |
|----|-------|--------|
| #6273 | feat: rewards engine single-responsibility | DEPLOYED — contains regression |
| #6276 | feat(world_logic): Layer 3 CLEAN — strip old rewards detection | OPEN — NOT yet deployed |

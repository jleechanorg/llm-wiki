---
title: "PR #6350 autor ET level-up atomicity helpers"
type: source
tags: [autor, et, worldarchitect-ai]
sources: []
last_updated: 2026-04-17
---

## Summary

PR #6350 is an AI-generated autor PR using the ET (Extended Thinking) technique to add level-up atomicity helpers to world_logic.py. The autor PR receives a quality score of 59/100 — the ET reasoning process is well-documented, but the diff includes junk worktree subproject commits as artifacts.

## Key Claims

- ET step-by-step reasoning guides the extraction of helper functions from the stuck completion state problem
- Added `_XP_PER_LEVEL = 300` constant for XP calculations
- Added `_calculate_next_level_xp()` helper function
- Added `ensure_level_up_rewards_box()` and `ensure_level_up_planning_block()` helpers for postcondition assertion

## Score Breakdown

| Dimension | Score | Max | Notes |
|-----------|-------|-----|-------|
| Naming | 12 | 15 | Good function names throughout |
| Error Handling | 14 | 20 | None handling, level_up_complete checks present |
| Type Safety | 13 | 20 | Type annotations present; Any for dynamic game state |
| Architecture | 7 | 20 | MAJOR: Diff includes junk worktree subproject commits |
| Test Coverage | 5 | 15 | No test files added in this autor PR |
| Documentation | 8 | 10 | ET step-by-step reasoning comments (3 steps) visible |
| **Total** | **59** | **100** | |

## Connections

- [[PR6264]] — original PR (fix: remove anchor in skeptic verdict regex)
- [[ETExtendedThinking]] — technique used

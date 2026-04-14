---
title: "PR #6262: Stale Flag Recovery + Atomicity Enforcement"
type: source
tags: [worldarchitect, level-up, stale-flag, atomicity, bug-fix]
date: 2026-04-14
source_file: raw/pr-6262-stale-flag-recovery-atomicity.md
---

## Summary
PR #6262 fixes stale flag recovery in `_project_level_up_ui_from_game_state` and adds atomicity enforcement for level-up badge/planning consistency. Fixes production bug where `rewards_box` never emits despite level-up completing.

## Key Claims
- **Stale flag recovery**: Fallback path checks `level_up_complete=true` OR XP-level mismatch when `resolve_level_up_signal` returns inactive
- **New helper**: `_enforce_level_up_rewards_planning_atomicity` for level-up-specific badge/planning enforcement
- **Stale guard fix**: `resolve_level_up_signal` now correctly allows `in_progress=False + pending=True` state
- **Suppressed flag preservation**: When `allow_injection=False`, preserve `rewards_box` with `level_up_available=False`

## Test Results
| Test | Result |
|------|--------|
| atomicity_e2e | PASS |
| atomicity_contract | PASS |
| god_mode_reward_visibility | PASS |
| projected_level_up_button_text | PASS |
| multi_level_organic_progression | PASS |

## Connections
- [[LevelUpBug]] — bug chain
- [[StaleFlag]] — level-up specific flags
- [[RewardsBoxAtomicity]] — atomicity invariant

---
title: "Level-Up Stale Flag Tests"
type: source
tags: [python, testing, tdd, state-management, bug-fix]
source_file: "raw/test_level_up_stale_flags.py"
sources: []
last_updated: 2026-04-08
---

## Summary
TDD test suite verifying stale flag handling in level-up modal and state transitions. Tests expose bugs where level_up_in_progress and character_creation_in_progress flags are not properly cleared, blocking future level-ups and causing UI retrigger issues.

## Key Claims
- **level_up_in_progress not cleared on new level-up**: Bug in world_logic.py:1025 clears level_up_complete/level_up_cancelled but NOT level_up_in_progress
- **rewards_pending not fully cleared on exit**: Level-up modal exit sets rewards_pending = {level_up_available: False} but doesn't remove stale keys
- **character_creation_in_progress not cleared on level-up exit**: Bug in world_logic.py:1427 leaves flag set, blocking character creation mode

## Key Test Cases
| Test | Scenario | Expected |
|------|----------|----------|
| test_level_up_in_progress_cleared_when_new_level_up_available | State has stale flag from previous level-up, new XP triggers level 2 | level_up_in_progress should be None, not False |
| test_rewards_pending_cleared_on_level_up_exit | Exit level-up modal with existing rewards_pending | rewards_pending should be DELETE_TOKEN |
| test_character_creation_flags_cleared_on_level_up_exit | Exit level-up modal | character_creation_in_progress should be cleared |

## Connections
- [[LevelUpStateManagement]] — concept page for level-up state flags
- [[TDDWorkflow]] — red-green testing methodology used

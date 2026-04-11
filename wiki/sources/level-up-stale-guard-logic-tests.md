---
title: "TDD Test Coverage for Level-Up Stale Guard Logic"
type: source
tags: [python, testing, tdd, state-management, bug-fix]
source_file: "raw/test_level_up_stale_guard_logic.py"
sources: []
last_updated: 2026-04-08
---

## Summary
TDD test suite providing coverage for the stale flag guard logic added in PR #5282 to prevent level-up modal from reactivating when explicit False flags are set. Tests validate should_activate_for_state and get_agent_for_input guards.

## Key Claims
- **Explicit False overrides stale rewards_pending**: When level_up_in_progress=False (explicit), modal does NOT reactivate even with rewards_pending.level_up_available=True
- **level_up_pending=False guard**: When level_up_pending=False AND level_up_in_progress is not True, the agent deactivates
- **in_progress takes precedence**: When level_up_in_progress=True, it overrides level_up_pending=False

## Key Test Cases
| Test | Scenario | Expected |
|------|----------|----------|
| test_should_activate_returns_false_when_level_up_in_progress_explicitly_false | level_up_in_progress=False, rewards_pending.level_up_available=True | should_activate=False |
| test_should_activate_returns_false_when_level_up_pending_false_and_not_in_progress | level_up_pending=False, level_up_in_progress not set | should_activate=False |
| test_should_activate_allows_pending_false_when_in_progress_true | level_up_pending=False, level_up_in_progress=True | should_activate=True |

## Connections
- [[LevelUpAgent]] — component being tested
- [[LevelUpStaleFlagTests]] — prior work on stale flag clearing
- [[StateManagement]] — underlying pattern

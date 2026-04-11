---
title: "TDD Test Coverage for World Logic Modal Lock Functions"
type: source
tags: [testing, tdd, modal-lock, world-logic, level-up, character-creation, python]
source_file: "raw/tdd-test-coverage-modal-lock.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests providing TDD coverage for modal lock logic added in PR #5282. Tests target _check_and_set_level_up_pending stale flag clearing and _enforce_character_creation_modal_lock with level-up paths, exit choices, and protected flags.

## Key Claims
- **Coverage Target**: mvp_site/world_logic.py:1031-1035, 1377, 1427-1445, 1480, 1516
- **PR Reference**: PR #5282 adds modal lock enforcement
- **Stale Flag Clearing**: Tests clear level_up_complete and level_up_cancelled stale flags when new level-up available
- **Level-Up Paths**: Tests level_up_modal_active label logging, exit choice handling, protected flag preservation

## Key Test Cases
- test_clears_stale_level_up_complete_when_new_level_up_available:
  - Clears level_up_complete when XP sufficient for next level
- test_clears_stale_level_up_cancelled_when_new_level_up_available:
  - Clears level_up_cancelled when new level-up becomes available
- test_level_up_modal_active_label_added_to_list:
  - Logs level_up label when modal active
- test_level_up_exit_choice_sets_completion_flags:
  - Sets completion flags on exit choice selection

## Connections
- [[PR5282]] — PR that adds modal lock logic
- [[LevelUp]] — game mechanic being tested
- [[ModalLock]] — concept being enforced

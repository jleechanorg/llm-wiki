---
title: "TDD Test for REV-0g1y: Inconsistent level-up active-state logic"
type: source
tags: [python, testing, tdd, level-up, state-management, stale-flags, modal-injection]
source_file: "raw/test_rev_0g1y_level_up_active_state.py"
sources: []
last_updated: 2026-04-08
---

## Summary
TDD tests validating that both `get_agent_for_input` and `_inject_modal_finish_choice_if_needed` use consistent logic to determine if level-up is active, including proper stale flag guards (`level_up_in_progress=False`, `level_up_pending=False`).

## Key Claims
- **Inconsistent detection**: `get_agent_for_input` and `_inject_modal_finish_choice_if_needed` use different logic to determine if level-up is active
- **Stale flag guards**: Both should respect `level_up_in_progress=False` and `level_up_pending=False` stale guards
- **Modal injection bug**: Current `_inject_modal_finish_choice_if_needed` may inject finish choice even when stale flags are false
- **Routing vs injection mismatch**: Routing logic may not activate modal while injection logic adds finish choice, causing inconsistency

## Test Scenarios
1. **stale_in_progress_false_flag**: When `level_up_in_progress=False` explicitly, finish choice should NOT inject even if `rewards_pending.level_up_available=True`
2. **stale_pending_false_flag**: When `level_up_pending=False` and `level_up_in_progress` not True, finish choice should NOT inject

## Connections
- [[LevelUpActiveStateLogic]] — the concept being fixed
- [[StaleFlagGuard]] — guard pattern for stale state detection
- [[ModalInjection]] — mechanism for injecting choices into planning blocks

## Contradictions
- Contradicts current implementation on: `_inject_modal_finish_choice_if_needed` does not check `level_up_in_progress` stale flag like `get_agent_for_input` does

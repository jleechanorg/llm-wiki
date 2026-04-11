---
title: "TDD Test for REV-439p: Level-up modal lock bypass with level_up_pending"
type: source
tags: [python, testing, tdd, level-up, modal-lock, state-management, pr-reviews]
source_file: "raw/test_rev_439p_level_up_modal_lock_bypass.py"
sources: []
last_updated: 2026-04-08
---

## Summary
TDD tests validating that `get_agent_for_input` properly activates the level-up modal lock when `level_up_pending=True` or `rewards_pending.level_up_available=True`, even without `level_up_in_progress` being set. Tests cover two scenarios: pending level-up flag and available rewards flag.

## Key Claims
- **Modal lock bypass**: Current implementation may allow bypassing the level-up modal when only `level_up_pending=True` is set
- **Incomplete flag check**: `level_up_in_progress` check alone is insufficient for modal lock activation
- **Rewards flag**: `rewards_pending.level_up_available=True` should also activate modal lock
- **Priority routing**: Modal lock should set routing priority to `3_modal_level_up`

## Key Test Cases
- `test_level_up_pending_true_activates_modal_lock`: Validates `level_up_pending=True` triggers `LevelUpAgent`
- `test_level_up_rewards_available_activates_modal_lock`: Validates `rewards_pending.level_up_available=True` triggers `LevelUpAgent`

## Connections
- [[REV-0g1y]] — related stale flag handling issue
- [[LevelUpAgent]] — agent that handles level-up modal flow
- [[GameState]] — game state manager with custom_campaign_state
- [[ModalLock]] — concept describing the modal bypass prevention mechanism

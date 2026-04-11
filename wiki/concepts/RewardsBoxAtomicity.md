---
title: "RewardsBoxAtomicity"
type: concept
tags: [worldarchitect-ai, atomicity, rewards-box, planning-block, world-logic]
sources: [pr-6161-fix-rewards-box-planning-block-atomicity-and-get-c, pr-6161-bug-hunt-report]
last_updated: 2026-04-11
---

## Summary

`RewardsBoxAtomicity` is the invariant that `rewards_box` and `planning_block` must be consistent with each other and with actual game state. Violations cause badge-without-buttons UI, stale choices, and silently dropped user inputs.

## The Invariant

1. `rewards_box.level_up_available` and `planning_block` level-up choices must agree
2. Both fields must be written back to `unified_response` after enforcement, regardless of each other's state
3. Polling path must not discard valid non-level-up choices when detecting stale level-up signals
4. `_inject_modal_finish_choice_if_needed` must not be called after `planning_block` is suppressed to None

## Bugs Found (PR #6161 Bug Hunt)

### Bug 1: Stale planning_block Not Written Back
- **File:** `world_logic.py:7071-7078`
- **Bug:** When `rewards_box is None` and `planning_block` had no level-up choices, enforced `planning_block` NOT written back
- **Fix:** Always write back enforced `planning_block` regardless of `rewards_box` state

### Bug 2: Polling Path Discarded Valid Choices
- **File:** `world_logic.py:7385-7387`
- **Bug:** Polling detected stale `level_up_available` → nulled BOTH `rewards_box` AND `planning_block`, discarding valid non-level-up choices
- **Fix:** Preserve non-level-up choices before atomicity enforcement

### Bug 3: False-Positive Level-Up Scrubbing in Think Mode
- **File:** `world_logic.py:2759-2807`
- **Bug:** When `rewards_box` had no level-up but `planning_block` did, ALL level-up choices scrubbed even when game state supported level-up
- **Fix:** Check rewards_box internal consistency using `xp_needed_for_level()` thresholds

### Bug 4: Spurious Modal Finish Injection
- **File:** `world_logic.py:7395-7400`
- **Bug:** `_inject_modal_finish_choice_if_needed(None, game_state_dict)` called after `planning_block` suppressed to None
- **Fix:** Guard on `planning_block is not None` before injection

## Key Functions

- `_enforce_rewards_box_planning_atomicity()` — Core atomicity enforcement helper
- `_process_rewards_followup()` — Uses sentinel contract with `normalize_rewards_box_for_ui`
- `normalize_rewards_box_for_ui()` — Returns `None` for empty payloads, normalized dict otherwise
- `_infer_level_up_target_from_xp()` — Uses `xp_needed_for_level()` canonical thresholds

## Connections

- [[LevelUpBug]] — Full bug chain context
- [[StructureDriftPattern]] — Related structural issue
- [[RewardsBox]] — rewards_box JSON structure
- [[LevelUpStateManagement]] — Level-up flag management

---
title: "Modal State Lifecycle Tests"
type: source
tags: [python, testing, modal-agent, state-transitions, tdd]
source_file: "raw/test_modal_state_lifecycle.py"
sources: ["modal-state-management-integration-tests", "modal-state-management-test-utilities", "modal-agent-intent-classifier-tdd-tests"]
last_updated: 2026-04-08
---

## Summary
Test suite validating state transitions for all three modals (Character Creation, Level-Up, Campaign Upgrade) in the game system, ensuring proper flag lifecycle management and stale flag removal.

## Key Claims
- **Flag clearing on new modal availability**: When a new modal becomes available, any stale flags from previous sessions should be cleared
- **Proper state transitions**: Modals follow activate → in_progress → complete/cancel lifecycle
- **Stale flag removal**: Stale flags should be REMOVED from dict, not just set to False
- **Level-up clears stale completion flags**: level_up_complete, level_up_cancelled should be cleared when new level-up becomes available
- **Exit sets complete flag**: Exiting level-up via finish choice sets level_up_complete=True

## Connections
- [[LevelUpAgent]] — tests state transitions for level-up modal
- [[CharacterCreationAgent]] — tests character creation modal lifecycle
- [[CampaignUpgrade]] — tests campaign upgrade modal
- [[Modal State Management Test Utilities]] — uses ModalTestBase and ModalTestScenario
- [[Integration Tests for Modal State Management]] — cross-modal interaction tests

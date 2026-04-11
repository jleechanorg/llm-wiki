---
title: "Fixture-driven routing and modal invariants for agent selection"
type: source
tags: [python, testing, modal-agent, tdd, fixtures]
source_file: "raw/test_modal_routing_fixtures.py"
sources: ["modal-state-management-integration-tests", "modal-state-management-test-utilities", "modal-agent-intent-classifier-tdd-tests"]
last_updated: 2026-04-08
---

## Summary
Test suite using machine-checkable JSON fixtures to validate routing and finish-choice injection invariants for modal agents (LevelUpAgent and CharacterCreationAgent) in the game system.

## Key Claims
- **Fixture-based testing**: Uses `modal_routing_fixtures.json` for declarative test scenarios
- **Routing-injection invariant**: Routing logic and finish-choice injection must agree on modal active state
- **Modal agent mapping**: Tests `_MODAL_AGENT_BY_NAME` dictionary mapping agent names to classes
- **State simulation**: Mocks game state with custom_campaign_state, rewards_pending, and player_character_data
- **Choice ID validation**: Verifies "finish_character_creation_start_game" and "finish_level_up_return_to_game" choice IDs

## Key Connections
- Related to [[Modal State Management Integration Tests]] — integration tests for cross-modal flag clearing
- Related to [[Modal State Management Test Utilities]] — provides ModalTestBase base class
- Related to [[TDD Tests for Modal Agent & Intent Classifier Bugs]] — captures modal agent bugs
- Uses [[get_agent_for_input]] function from mvp_site.agents
- Uses [[_inject_modal_finish_choice_if_needed]] function from world_logic

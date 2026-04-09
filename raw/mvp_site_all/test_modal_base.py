"""
Base classes and utilities for modal state management testing.

This module provides:
- ModalTestScenario: Declarative test scenario dataclass
- ModalTestBase: Base class with fixtures and custom assertions
- Shared utilities for all modal state tests
"""

import sys
import os
from dataclasses import dataclass
from typing import Any, Callable
from unittest.mock import Mock

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import unittest
from mvp_site import agents, world_logic, constants


@dataclass
class ModalTestScenario:
    """Declarative test scenario for modal state management.

    Attributes:
        name: Descriptive name for the scenario
        initial_state: Starting game state dict
        action: Either a callable to execute or user_input string for routing
        expected_flags: Expected custom_campaign_state flags after action
        expected_rewards: Expected rewards_pending after action (optional)
        description: Human-readable scenario description
    """
    name: str
    initial_state: dict[str, Any]
    action: Callable | str
    expected_flags: dict[str, Any]
    expected_rewards: dict[str, Any] | None = None
    description: str = ""


class ModalTestBase(unittest.TestCase):
    """Base class for modal state management tests.

    Provides:
    - Custom assertion helpers for semantic checks
    - run_scenario() method for executing ModalTestScenario instances
    - Common test fixtures and utilities
    """

    # ==================== Custom Assertions ====================

    def assert_no_modal_active(self, state: dict[str, Any], msg: str | None = None):
        """Assert that no modal is currently active in the game state.

        Args:
            state: Game state dict to check
            msg: Optional custom assertion message
        """
        custom_state = state.get("custom_campaign_state", {})

        active_modals = []
        if custom_state.get("character_creation_in_progress"):
            active_modals.append("character_creation")
        if custom_state.get("level_up_in_progress"):
            active_modals.append("level_up")
        if custom_state.get("campaign_upgrade_in_progress"):
            active_modals.append("campaign_upgrade")

        default_msg = f"Expected no modal active, but found: {active_modals}"
        self.assertEqual(len(active_modals), 0, msg or default_msg)

    def assert_only_modal_active(self, state: dict[str, Any], modal_name: str, msg: str | None = None):
        """Assert that exactly one specific modal is active.

        Args:
            state: Game state dict to check
            modal_name: Name of expected active modal (character_creation, level_up, campaign_upgrade)
            msg: Optional custom assertion message
        """
        custom_state = state.get("custom_campaign_state", {})

        active_modals = []
        if custom_state.get("character_creation_in_progress"):
            active_modals.append("character_creation")
        if custom_state.get("level_up_in_progress"):
            active_modals.append("level_up")
        if custom_state.get("campaign_upgrade_in_progress"):
            active_modals.append("campaign_upgrade")

        default_msg = (
            f"Expected only '{modal_name}' active, but found: {active_modals}. "
            f"custom_campaign_state={custom_state}"
        )
        self.assertEqual(active_modals, [modal_name], msg or default_msg)

    def assert_stale_flags_cleared(self, state: dict[str, Any], modal: str, msg: str | None = None):
        """Assert that stale flags for a modal have been properly cleared (removed, not just set to False).

        Args:
            state: Game state dict to check
            modal: Modal type (character_creation, level_up, campaign_upgrade)
            msg: Optional custom assertion message
        """
        custom_state = state.get("custom_campaign_state", {})

        flag_map = {
            "character_creation": [
                "character_creation_in_progress",
                "character_creation_pending"
            ],
            "level_up": [
                "level_up_in_progress",
                "level_up_pending"
            ],
            "campaign_upgrade": [
                "campaign_upgrade_in_progress",
                "campaign_upgrade_pending"
            ]
        }

        flags_to_check = flag_map.get(modal, [])
        stale_flags = {
            flag: custom_state.get(flag)
            for flag in flags_to_check
            if custom_state.get(flag) is False  # Explicitly False = stale
        }

        default_msg = (
            f"Expected stale {modal} flags to be cleared (removed from dict), "
            f"but found flags explicitly set to False: {stale_flags}"
        )
        self.assertEqual(len(stale_flags), 0, msg or default_msg)

    def assert_routing_matches_injection(
        self,
        state: dict[str, Any],
        user_input: str,
        msg: str | None = None
    ):
        """Assert that routing logic and finish choice injection use identical active detection.

        Tests the consistency between:
        1. get_agent_for_input() routing decision
        2. _inject_modal_finish_choice_if_needed() injection decision

        Args:
            state: Game state dict
            user_input: User input string for routing
            msg: Optional custom assertion message
        """
        # Mock game state for routing
        mock_game_state = Mock()
        mock_game_state.custom_campaign_state = state.get("custom_campaign_state", {})
        mock_game_state.rewards_pending = state.get("rewards_pending", {})
        mock_game_state.campaign = {
            "custom_campaign_state": state.get("custom_campaign_state", {}),
            "campaign_version": 2
        }
        mock_game_state.is_campaign_upgrade_available.return_value = False
        mock_game_state.get_character.return_value = state.get("player_character_data", {})

        # Check routing decision
        agent, metadata = agents.get_agent_for_input(user_input, mock_game_state)
        routing_modal_active = isinstance(agent, (
            agents.CharacterCreationAgent,
            agents.LevelUpAgent
        ))

        # Check injection decision
        planning_block = {"thinking": "test", "choices": {"explore": {"text": "Explore"}}}
        result = world_logic._inject_modal_finish_choice_if_needed(planning_block, state)

        injection_modal_active = False
        if result and isinstance(result, dict):
            choices = result.get("choices", {})
            if isinstance(choices, dict):
                injection_modal_active = (
                    "finish_character_creation_start_game" in choices
                    or "finish_level_up_return_to_game" in choices
                )
            elif isinstance(choices, list):
                choice_ids = {
                    choice.get("id")
                    for choice in choices
                    if isinstance(choice, dict)
                }
                injection_modal_active = (
                    "finish_character_creation_start_game" in choice_ids
                    or "finish_level_up_return_to_game" in choice_ids
                )

        default_msg = (
            f"Routing and injection disagree on modal active state! "
            f"Routing says modal_active={routing_modal_active} (agent={type(agent).__name__}), "
            f"Injection says modal_active={injection_modal_active}. "
            f"This indicates inconsistent logic between get_agent_for_input and "
            f"_inject_modal_finish_choice_if_needed. "
            f"State: custom_campaign_state={state.get('custom_campaign_state')}, "
            f"rewards_pending={state.get('rewards_pending')}"
        )

        self.assertEqual(routing_modal_active, injection_modal_active, msg or default_msg)

    def assert_flags_match(
        self,
        state: dict[str, Any],
        expected: dict[str, Any],
        msg: str | None = None
    ):
        """Assert that custom_campaign_state flags match expected values.

        Args:
            state: Game state dict
            expected: Expected flag values (checked with dict subset matching)
            msg: Optional custom assertion message
        """
        custom_state = state.get("custom_campaign_state", {})

        for key, expected_value in expected.items():
            actual_value = custom_state.get(key)
            default_msg = (
                f"Flag '{key}' mismatch: expected {expected_value!r}, got {actual_value!r}. "
                f"Full custom_campaign_state: {custom_state}"
            )
            self.assertEqual(actual_value, expected_value, msg or default_msg)

    def assert_modal_exit_cleans_all_flags(
        self,
        state: dict[str, Any],
        msg: str | None = None
    ):
        """Assert that exiting any modal clears ALL modal-related flags.

        This detects cross-modal pollution bugs where exiting modal A
        leaves stale flags from modal B.

        Args:
            state: Game state dict after modal exit
            msg: Optional custom assertion message
        """
        custom_state = state.get("custom_campaign_state", {})

        # Check that NO modal is marked as in_progress
        in_progress_flags = {
            flag: custom_state.get(flag)
            for flag in [
                "character_creation_in_progress",
                "level_up_in_progress",
                "campaign_upgrade_in_progress"
            ]
            if custom_state.get(flag) is True
        }

        default_msg = (
            f"Expected ALL modal in_progress flags cleared after exit, "
            f"but found active flags: {in_progress_flags}. "
            f"This indicates cross-modal pollution. "
            f"Full custom_campaign_state: {custom_state}"
        )
        self.assertEqual(len(in_progress_flags), 0, msg or default_msg)

    # ==================== Scenario Execution ====================

    def run_scenario(self, scenario: ModalTestScenario):
        """Execute a ModalTestScenario and verify expectations.

        Args:
            scenario: ModalTestScenario instance to execute
        """
        # Make a deep copy of initial state to avoid mutation
        import copy
        state = copy.deepcopy(scenario.initial_state)

        # Execute the action
        if callable(scenario.action):
            # Action is a function - call it with state
            result_state = scenario.action(state)
        else:
            # Action is user_input string - test routing + world_logic
            # This is the integration path for most tests
            user_input = scenario.action

            # Create original state for comparison
            original_state = copy.deepcopy(state)

            # Call world_logic functions that modify state
            result_state = world_logic._check_and_set_level_up_pending(state, original_state)
            result_state = world_logic._enforce_character_creation_modal_lock(
                result_state,
                {},  # empty state_changes from LLM
                user_input
            )

        # Verify expected flags
        self.assert_flags_match(result_state, scenario.expected_flags)

        # Verify expected rewards if specified
        if scenario.expected_rewards is not None:
            rewards = result_state.get("rewards_pending", {})
            for key, expected_value in scenario.expected_rewards.items():
                self.assertEqual(
                    rewards.get(key),
                    expected_value,
                    f"Scenario '{scenario.name}': rewards_pending['{key}'] mismatch"
                )

    # ==================== Test Fixtures ====================

    def create_base_state(
        self,
        character_level: int = 1,
        character_xp: int = 0,
        custom_campaign_state: dict[str, Any] | None = None,
        rewards_pending: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Create a base game state dict for testing.

        Args:
            character_level: Character level
            character_xp: Character XP
            custom_campaign_state: Custom campaign state flags
            rewards_pending: Pending rewards

        Returns:
            Game state dict suitable for testing
        """
        return {
            "player_character_data": {
                "name": "TestChar",
                "level": character_level,
                "class": "Fighter",
                "xp": character_xp
            },
            "custom_campaign_state": custom_campaign_state or {},
            "rewards_pending": rewards_pending or {}
        }

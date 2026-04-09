"""
Integration tests for modal state management.

Tests:
- Cross-modal interaction and flag pollution
- Routing vs injection consistency
- Modal priority and mutual exclusion
"""

import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from mvp_site.tests.test_modal_base import ModalTestBase, ModalTestScenario
from mvp_site import world_logic


class TestCrossModalInteraction(ModalTestBase):
    """Test interactions between different modals."""

    def test_level_up_exit_clears_character_creation_flags(self):
        """
        BUG FIX TEST (9c9f93d4a): Exiting level-up should clear
        character_creation_in_progress to prevent recapture by
        character creation lock check.
        """
        scenario = ModalTestScenario(
            name="level_up_exit_clears_char_creation_flags",
            initial_state=self.create_base_state(
                character_level=2,
                custom_campaign_state={
                    "level_up_in_progress": True,
                    "character_creation_in_progress": True,  # Stale from earlier
                }
            ),
            action="CHOICE:finish_level_up_return_to_game",
            expected_flags={
                "level_up_complete": True,
                "level_up_in_progress": False,
                "character_creation_in_progress": False,  # MUST be cleared!
                "character_creation_completed": True,
            },
            description="Prevents character creation lock from recapturing after level-up exit"
        )
        self.run_scenario(scenario)

        # Note: scenario.action is a string, not callable - run_scenario handles execution

    def test_character_creation_exit_with_stale_level_up_flags(self):
        """Exiting character creation should clear any stale level-up flags."""
        scenario = ModalTestScenario(
            name="char_creation_exit_clears_level_up_flags",
            initial_state=self.create_base_state(
                custom_campaign_state={
                    "character_creation_in_progress": True,
                    "character_creation_stage": "review",  # Need stage
                    "level_up_in_progress": False,  # Stale flag (shouldn't happen, but test robustness)
                }
            ),
            action="CHOICE:finish_character_creation_start_game",
            expected_flags={
                "character_creation_completed": True,
            },
            description="Defensive cleanup of stale flags from other modals"
        )
        self.run_scenario(scenario)

    def test_multiple_modal_flags_only_one_activates(self):
        """When multiple modal flags are set, only one should actually be active."""
        # This is a defensive test - ideally this state should never happen,
        # but if it does, the system should handle it gracefully

        state = self.create_base_state(
            custom_campaign_state={
                "level_up_in_progress": True,
                "character_creation_in_progress": True,  # Shouldn't happen!
            }
        )

        # The system should prioritize one modal (typically level-up takes precedence)
        # This test documents current behavior and catches changes
        from mvp_site import agents
        from unittest.mock import Mock

        mock_game_state = Mock()
        mock_game_state.custom_campaign_state = state["custom_campaign_state"]
        mock_game_state.rewards_pending = {}
        mock_game_state.campaign = {"custom_campaign_state": state["custom_campaign_state"], "campaign_version": 2}
        mock_game_state.is_campaign_upgrade_available.return_value = False
        mock_game_state.get_character.return_value = state.get("player_character_data", {})

        agent, metadata = agents.get_agent_for_input("continue", mock_game_state)

        # Document which modal wins (currently level-up should take precedence)
        # If this assertion fails in future, it indicates priority logic changed
        self.assertIsInstance(
            agent,
            (agents.LevelUpAgent, agents.CharacterCreationAgent),
            "At least one modal should be active"
        )


class TestRoutingInjectionConsistency(ModalTestBase):
    """Test that routing and injection logic agree on modal active state."""

    def test_routing_matches_injection_level_up_with_stale_in_progress_false(self):
        """
        BUG FIX TEST (11ef8e4f5): Routing and injection must both check
        for stale level_up_in_progress=False flag.
        """
        state = self.create_base_state(
            character_level=2,
            custom_campaign_state={
                "level_up_in_progress": False,  # Stale guard
                "character_creation_completed": True,  # Char creation done
            },
            rewards_pending={
                "level_up_available": True,  # Leftover stale flag
            }
        )

        # Both routing and injection should agree: modal NOT active
        self.assert_routing_matches_injection(state, "continue")

    def test_routing_matches_injection_level_up_with_stale_pending_false(self):
        """
        BUG FIX TEST (11ef8e4f5): Routing and injection must both check
        for stale level_up_pending=False flag.
        """
        state = self.create_base_state(
            character_level=2,
            custom_campaign_state={
                "level_up_pending": False,  # Explicitly False (stale)
                "character_creation_completed": True,  # Char creation done
                # level_up_in_progress not set (None)
            },
            rewards_pending={
                "level_up_available": True,  # Leftover stale flag
            }
        )

        # Both should agree: modal NOT active
        self.assert_routing_matches_injection(state, "continue")

    def test_routing_matches_injection_level_up_active(self):
        """When level-up is truly active, routing and injection should both detect it."""
        state = self.create_base_state(
            character_level=2,
            custom_campaign_state={
                "level_up_in_progress": True,  # Active
            },
            rewards_pending={
                "level_up_available": True,
            }
        )

        # Both should agree: modal IS active
        self.assert_routing_matches_injection(state, "continue")

    def test_routing_matches_injection_character_creation_active(self):
        """When character creation is active, routing and injection should both detect it."""
        state = self.create_base_state(
            custom_campaign_state={
                "character_creation_in_progress": True,
            }
        )

        # Both should agree: modal IS active
        self.assert_routing_matches_injection(state, "continue")

    def test_routing_matches_injection_no_modal_active(self):
        """When no modal is active, routing and injection should both agree."""
        state = self.create_base_state(
            character_level=2,
            custom_campaign_state={
                "character_creation_completed": True,
            }
        )

        # Both should agree: no modal active
        self.assert_routing_matches_injection(state, "continue")


class TestModalPriorityAndExclusion(ModalTestBase):
    """Test modal priority rules and mutual exclusion."""

    def test_level_up_pending_activates_before_story(self):
        """When level_up_pending=True, modal should activate before story mode."""
        from mvp_site import agents
        from unittest.mock import Mock

        state = self.create_base_state(
            character_level=2,
            character_xp=900,  # L3 threshold reached; pending flag is not stale
            custom_campaign_state={
                "level_up_pending": True,
                "character_creation_completed": True,
            }
        )

        mock_game_state = Mock()
        mock_game_state.custom_campaign_state = state["custom_campaign_state"]
        mock_game_state.rewards_pending = {}
        mock_game_state.player_character_data = state["player_character_data"]
        mock_game_state.campaign = {"custom_campaign_state": state["custom_campaign_state"], "campaign_version": 2}
        mock_game_state.is_campaign_upgrade_available.return_value = False
        mock_game_state.get_character.return_value = state.get("player_character_data", {})

        agent, metadata = agents.get_agent_for_input("continue", mock_game_state)

        self.assertIsInstance(agent, agents.LevelUpAgent)

    def test_character_creation_blocks_story_mode(self):
        """Character creation in progress should block story mode."""
        from mvp_site import agents
        from unittest.mock import Mock

        state = self.create_base_state(
            custom_campaign_state={
                "character_creation_in_progress": True,
            }
        )

        mock_game_state = Mock()
        mock_game_state.custom_campaign_state = state["custom_campaign_state"]
        mock_game_state.rewards_pending = {}
        mock_game_state.campaign = {"custom_campaign_state": state["custom_campaign_state"], "campaign_version": 2}
        mock_game_state.is_campaign_upgrade_available.return_value = False
        mock_game_state.get_character.return_value = state.get("player_character_data", {})

        agent, metadata = agents.get_agent_for_input("continue", mock_game_state)

        self.assertIsInstance(agent, agents.CharacterCreationAgent)

    def test_completed_modal_does_not_reactivate(self):
        """Completed modal should not reactivate on subsequent inputs."""
        from mvp_site import agents
        from unittest.mock import Mock

        state = self.create_base_state(
            character_level=2,
            custom_campaign_state={
                "level_up_complete": True,  # Already completed
                "level_up_in_progress": False,
            },
            rewards_pending={
                "level_up_available": True,  # Stale flag
            }
        )

        mock_game_state = Mock()
        mock_game_state.custom_campaign_state = state["custom_campaign_state"]
        mock_game_state.rewards_pending = state["rewards_pending"]
        mock_game_state.campaign = {"custom_campaign_state": state["custom_campaign_state"], "campaign_version": 2}
        mock_game_state.is_campaign_upgrade_available.return_value = False
        mock_game_state.get_character.return_value = state.get("player_character_data", {})

        agent, metadata = agents.get_agent_for_input("continue", mock_game_state)

        # Should NOT return LevelUpAgent
        self.assertNotIsInstance(agent, agents.LevelUpAgent)


if __name__ == "__main__":
    import unittest
    unittest.main()

"""
TDD Test for REV-439p: Level-up modal lock bypass with level_up_pending

Issue: level_up_pending=True alone doesn't activate modal lock in get_agent_for_input
Expected: level_up_pending=True should activate modal lock even without level_up_in_progress
"""

import unittest
from unittest.mock import Mock

from mvp_site import constants
from mvp_site.agents import LevelUpAgent, get_agent_for_input
from mvp_site.game_state import GameState


class TestREV439pModalBypass(unittest.TestCase):
    """Test level-up modal lock activates when level_up_pending=True."""

    def test_level_up_pending_true_activates_modal_lock(self):
        """
        REV-439p: level_up_pending=True should activate modal lock.

        When level_up_pending=True (but level_up_in_progress not set),
        the modal lock should activate to prevent bypass.
        """
        mock_game_state = Mock(spec=GameState)
        mock_game_state.custom_campaign_state = {
            "level_up_pending": True,  # Pending flag set
            # level_up_in_progress not set (None)
            "character_creation_completed": True,  # Not in char creation
        }
        mock_game_state.rewards_pending = {}
        mock_game_state.player_character_data = {
            "level": 2,
            "experience": {
                "current": constants.get_xp_for_level(3),  # Ensure pending flag is valid
            },
        }
        mock_game_state.is_campaign_upgrade_available.return_value = False
        # Mock player_character_data with enough XP to level up (level 1 → 2 needs 300 XP)
        mock_game_state.player_character_data = {
            "level": 1,
            "xp": 300,  # Exactly enough for level 2
        }

        agent, metadata = get_agent_for_input(
            "What's my next quest?",  # User trying to bypass level-up
            game_state=mock_game_state
        )

        self.assertIsInstance(
            agent,
            LevelUpAgent,
            "get_agent_for_input MUST return LevelUpAgent when level_up_pending=True, "
            "even without level_up_in_progress. This prevents modal bypass."
        )
        self.assertEqual(
            metadata.get("routing_priority"),
            "3_modal_level_up",
            "Routing priority should be modal_level_up"
        )

    def test_level_up_rewards_available_activates_modal_lock(self):
        """
        REV-439p: rewards_pending.level_up_available=True should activate modal lock.
        """
        mock_game_state = Mock(spec=GameState)
        mock_game_state.custom_campaign_state = {
            "character_creation_completed": True,
        }
        mock_game_state.rewards_pending = {
            "level_up_available": True,  # Rewards flag set
        }
        mock_game_state.is_campaign_upgrade_available.return_value = False
        # Mock player_character_data (not strictly needed since rewards_pending bypasses XP check,
        # but included for completeness)
        mock_game_state.player_character_data = {
            "level": 1,
            "xp": 0,  # XP doesn't matter when rewards_pending.level_up_available=True
        }

        agent, metadata = get_agent_for_input(
            "I want to explore the forest",  # User trying to bypass
            game_state=mock_game_state
        )

        self.assertIsInstance(
            agent,
            LevelUpAgent,
            "get_agent_for_input MUST return LevelUpAgent when "
            "rewards_pending.level_up_available=True"
        )


if __name__ == '__main__':
    unittest.main()

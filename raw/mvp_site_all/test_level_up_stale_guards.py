"""
TDD Test Coverage for Level-Up Stale Guard Logic

These tests provide coverage for the stale flag guard logic added in PR #5282
to prevent level-up modal from reactivating when explicit False flags are set.

Coverage targets:
- mvp_site/agents.py:1257-1262 (LevelUpAgent.should_activate_for_state)
- mvp_site/agents.py:2849-2852 (get_agent_for_input level_up_pending=False guard)
"""

import unittest
from unittest.mock import Mock

from mvp_site.agents import LevelUpAgent, get_agent_for_input
from mvp_site.game_state import GameState


class TestLevelUpAgentShouldActivateStaleGuards(unittest.TestCase):
    """Test LevelUpAgent.should_activate_for_state stale flag guards."""

    def test_should_activate_returns_false_when_level_up_in_progress_explicitly_false(self):
        """
        Coverage: mvp_site/agents.py:1257-1259

        When level_up_in_progress is explicitly set to False (not just missing),
        the agent should not activate even if rewards_pending.level_up_available=True.
        This prevents reactivation after a previous level-up completion.
        """
        mock_game_state = Mock(spec=GameState)
        mock_game_state.custom_campaign_state = {
            "level_up_in_progress": False,  # Explicitly False (not None/missing)
        }
        mock_game_state.rewards_pending = {
            "level_up_available": True,  # Leftover stale flag
        }

        result = LevelUpAgent.matches_game_state(mock_game_state)

        self.assertFalse(
            result,
            "matches_game_state must return False when level_up_in_progress=False, "
            "even if rewards_pending.level_up_available=True"
        )

    def test_should_activate_returns_false_when_level_up_pending_false_and_not_in_progress(self):
        """
        Coverage: mvp_site/agents.py:1261-1263

        When level_up_pending is explicitly False AND level_up_in_progress is not True,
        the agent should not activate. This prevents leftover pending flags from
        reactivating the modal after user has dismissed it.
        """
        mock_game_state = Mock(spec=GameState)
        mock_game_state.custom_campaign_state = {
            "level_up_pending": False,  # Explicitly False
            # level_up_in_progress is not set (None) - so not True
        }
        mock_game_state.rewards_pending = {
            "level_up_available": True,  # Leftover stale flag
        }

        result = LevelUpAgent.matches_game_state(mock_game_state)

        self.assertFalse(
            result,
            "matches_game_state must return False when level_up_pending=False "
            "and level_up_in_progress is not True"
        )

    def test_should_activate_allows_pending_false_when_in_progress_true(self):
        """
        When level_up_in_progress=True, the agent SHOULD activate even if
        level_up_pending=False. The in_progress flag takes precedence.
        """
        mock_game_state = Mock(spec=GameState)
        mock_game_state.custom_campaign_state = {
            "level_up_pending": False,  # Pending is false
            "level_up_in_progress": True,  # But in_progress overrides
        }
        mock_game_state.rewards_pending = {}

        result = LevelUpAgent.matches_game_state(mock_game_state)

        self.assertTrue(
            result,
            "matches_game_state must return True when level_up_in_progress=True, "
            "even if level_up_pending=False"
        )


class TestGetAgentForInputLevelUpPendingGuard(unittest.TestCase):
    """Test get_agent_for_input stale level_up_pending guard."""

    def test_level_up_pending_false_deactivates_modal_when_not_in_progress(self):
        """
        Coverage: mvp_site/agents.py:2847-2852

        When level_up_pending=False and level_up_in_progress is not True,
        get_agent_for_input should NOT return LevelUpAgent even if
        rewards_pending.level_up_available=True.
        """
        mock_game_state = Mock(spec=GameState)
        mock_game_state.custom_campaign_state = {
            "level_up_pending": False,  # Explicitly False
            # level_up_in_progress not set (None)
            "character_creation_completed": True,  # Not in char creation
        }
        mock_game_state.rewards_pending = {
            "level_up_available": True,  # Leftover stale flag
        }
        mock_game_state.is_campaign_upgrade_available.return_value = False

        agent, metadata = get_agent_for_input(
            "What's my next quest?",
            game_state=mock_game_state
        )

        self.assertNotIsInstance(
            agent,
            LevelUpAgent,
            "get_agent_for_input must NOT return LevelUpAgent when "
            "level_up_pending=False and level_up_in_progress is not True"
        )

    def test_level_up_pending_false_allows_modal_when_in_progress_true(self):
        """
        When level_up_in_progress=True, the modal SHOULD activate even if
        level_up_pending=False. The in_progress flag takes precedence.
        """
        mock_game_state = Mock(spec=GameState)
        mock_game_state.custom_campaign_state = {
            "level_up_pending": False,  # Pending is false
            "level_up_in_progress": True,  # But in_progress overrides
            "character_creation_completed": True,
        }
        mock_game_state.rewards_pending = {}
        mock_game_state.is_campaign_upgrade_available.return_value = False

        agent, metadata = get_agent_for_input(
            "I want to choose my level-up options",
            game_state=mock_game_state
        )

        self.assertIsInstance(
            agent,
            LevelUpAgent,
            "get_agent_for_input must return LevelUpAgent when level_up_in_progress=True, "
            "even if level_up_pending=False"
        )


if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import Mock

from mvp_site import constants, intent_classifier
from mvp_site.agents import (
    CharacterCreationAgent,
    CombatAgent,
    InfoAgent,
    PlanningAgent,
    RewardsAgent,
    StoryModeAgent,
    get_agent_for_input,
)


def create_mock_state():
    mock_state = Mock()
    mock_state.is_in_combat.return_value = False
    mock_state.custom_campaign_state = {"faction_minigame": {"enabled": False}}
    mock_state.get_combat_state.return_value = {"in_combat": False}
    # Ensure CampaignUpgradeAgent doesn't match
    mock_state.is_campaign_upgrade_available.return_value = False
    mock_state.get_pending_upgrade_type.return_value = None
    # Ensure CharacterCreationAgent doesn't match
    mock_state.is_in_character_creation.return_value = False
    # Ensure RewardsAgent doesn't match
    mock_state.get_encounter_state.return_value = {}
    mock_state.get_rewards_pending.return_value = None
    # Ensure FactionManagementAgent doesn't match
    # (relies on custom_campaign_state above)
    # Ensure CharacterCreationAgent doesn't match (needs name and completed flag)
    mock_state.player_character_data = {"name": "Test Hero", "class": "Fighter"}
    mock_state.custom_campaign_state["character_creation_completed"] = True
    mock_state.custom_campaign_state["character_creation_in_progress"] = False
    return mock_state


class TestInternalModeRejection(unittest.TestCase):
    """
    Verify that INTERNAL modes cannot be forced via the API 'mode' parameter.
    Internal modes must be selected automatically by the system (state or classifier).
    """

    def setUp(self):
        # Reset classifier singleton to avoid interference from other tests
        intent_classifier.LocalIntentClassifier._instance = None

    def test_reject_combat_mode_forcing(self):
        """Verify mode='combat' is rejected and falls back to StoryMode."""
        mock_state = create_mock_state()
        agent, _ = get_agent_for_input(
            "generic_action", mock_state, mode=constants.MODE_COMBAT
        )
        self.assertIsInstance(agent, StoryModeAgent)
        self.assertNotIsInstance(agent, CombatAgent)

    def test_reject_rewards_mode_forcing(self):
        """Verify mode='rewards' is rejected and falls back to StoryMode."""
        mock_state = create_mock_state()
        agent, _ = get_agent_for_input(
            "generic_action", mock_state, mode=constants.MODE_REWARDS
        )
        self.assertIsInstance(agent, StoryModeAgent)
        self.assertNotIsInstance(agent, RewardsAgent)

    def test_reject_info_mode_forcing(self):
        """Verify mode='info' is rejected and falls back to StoryMode."""
        mock_state = create_mock_state()
        agent, _ = get_agent_for_input(
            "generic_action", mock_state, mode=constants.MODE_INFO
        )
        self.assertIsInstance(agent, StoryModeAgent)
        self.assertNotIsInstance(agent, InfoAgent)

    def test_reject_character_creation_mode_forcing(self):
        """Verify mode='character_creation' is rejected and falls back to StoryMode."""
        mock_state = create_mock_state()
        agent, _ = get_agent_for_input(
            "generic_action", mock_state, mode=constants.MODE_CHARACTER_CREATION
        )
        self.assertIsInstance(agent, StoryModeAgent)
        self.assertNotIsInstance(agent, CharacterCreationAgent)

    def test_reject_dialog_heavy_mode_forcing(self):
        """Verify mode='dialog_heavy' is rejected and falls back to StoryMode."""
        mock_state = create_mock_state()
        agent, _ = get_agent_for_input(
            "generic_action", mock_state, mode=constants.MODE_DIALOG_HEAVY
        )
        self.assertIsInstance(agent, StoryModeAgent)

    def test_reject_case_insensitive_forcing(self):
        """Verify internal modes are rejected even with different casing."""
        mock_state = create_mock_state()
        agent, _ = get_agent_for_input("generic_action", mock_state, mode="COMBAT")
        self.assertIsInstance(agent, StoryModeAgent)

    def test_allow_valid_user_modes(self):
        """Verify user-facing modes (think, god) ARE allowed."""
        mock_state = create_mock_state()

        # Think mode allowed
        from mvp_site.agents import PlanningAgent

        agent, _ = get_agent_for_input("plan", mock_state, mode=constants.MODE_THINK)
        self.assertIsInstance(agent, PlanningAgent)

        # God mode allowed
        from mvp_site.agents import GodModeAgent

        agent, _ = get_agent_for_input("fix", mock_state, mode=constants.MODE_GOD)
        self.assertIsInstance(agent, GodModeAgent)

    def test_think_mode_requires_explicit_mode(self):
        """Think mode requires explicit mode='think'; prefix text alone is no longer sufficient."""
        mock_state = create_mock_state()

        story_agent, _ = get_agent_for_input(
            "Please think carefully about this scene.",
            mock_state,
        )
        self.assertIsInstance(story_agent, StoryModeAgent)

        prefix_only_agent, _ = get_agent_for_input(
            "THINK: What are my options?",
            mock_state,
        )
        self.assertIsInstance(prefix_only_agent, StoryModeAgent)

        explicit_mode_agent, _ = get_agent_for_input(
            "What are my options?",
            mock_state,
            mode=constants.MODE_THINK,
        )
        self.assertIsInstance(explicit_mode_agent, PlanningAgent)

        explicit_mode_with_prefix_agent, _ = get_agent_for_input(
            "THINK: What are my options?",
            mock_state,
            mode=constants.MODE_THINK,
        )
        self.assertIsInstance(explicit_mode_with_prefix_agent, PlanningAgent)


if __name__ == "__main__":
    unittest.main()

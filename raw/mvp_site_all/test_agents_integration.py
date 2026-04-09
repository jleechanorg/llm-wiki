"""
Integration tests for Agent architecture in WorldArchitect.AI.

This test suite verifies the complete flow of agent-based mode handling,
including mode detection, system instruction building, and integration
with the PromptBuilder class.

Tests cover:
- End-to-end agent selection based on user input
- System instruction building with actual prompt files
- Mode-specific prompt sets (story mode vs god mode)
- Integration between agents and PromptBuilder
"""

# ruff: noqa: E402, PT009

import os
import sys
import unittest
from unittest.mock import MagicMock, Mock, patch

# Add the project root to the Python path so we can import modules
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.insert(0, project_root)

from mvp_site import constants
from mvp_site.agents import (
    BaseAgent,
    DialogAgent,
    GodModeAgent,
    StoryModeAgent,
    get_agent_for_input,
)


class TestAgentModeDetectionIntegration(unittest.TestCase):
    """Integration tests for agent mode detection flow."""

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_story_mode_flow_with_various_inputs(self, mock_classify):
        """Test complete story mode flow with various input types."""
        # Ensure classifier returns MODE_CHARACTER for these narrative inputs to avoid
        # flakiness depending on model environment (e.g. if onnx missing vs present)
        mock_classify.return_value = (constants.MODE_CHARACTER, 1.0)

        input_expected_agent_map = {
            "I attack the goblin with my sword!": "StoryModeAgent",
            "Let me think about my options here...": "StoryModeAgent",
            "Search the room for hidden traps": "StoryModeAgent",
            "Cast fireball at the enemies": "StoryModeAgent",
            "What do I see around me?": "StoryModeAgent",
            "Rest for the night at the inn": "StoryModeAgent",
        }

        for user_input, expected_agent_name in input_expected_agent_map.items():
            with self.subTest(input=user_input):
                agent, _ = get_agent_for_input(user_input)
                self.assertIsInstance(
                    agent,
                    StoryModeAgent,
                    f"Expected {expected_agent_name} (StoryModeAgent) for input: {user_input} with no game state",
                )

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_god_mode_flow_with_various_inputs(self, mock_classify):
        """Test complete god mode flow with various input types."""
        # God mode inputs generally bypass classifier due to prefix priority,
        # but mocking ensures safety.
        mock_classify.return_value = (constants.MODE_CHARACTER, 1.0)
        god_inputs = [
            "GOD MODE: Set my HP to 50",
            "god mode: Add 100 gold to my inventory",
            "GOD MODE: Change my level to 10",
            "God Mode: Reset the combat encounter",
            "GOD MODE: Teleport me to the tavern",
            "  GOD MODE: Fix the broken quest state",
        ]

        for user_input in god_inputs:
            with self.subTest(input=user_input):
                agent, _ = get_agent_for_input(user_input)
                self.assertIsInstance(agent, GodModeAgent)
                self.assertEqual(agent.MODE, constants.MODE_GOD)

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_mode_boundary_cases(self, mock_classify):
        """Test edge cases in mode detection."""
        # Force character mode for these to ensure we fallback to StoryModeAgent
        mock_classify.return_value = (constants.MODE_CHARACTER, 1.0)
        # These should NOT trigger god mode
        not_god_mode = [
            "god",  # Just the word
            "god mode please",  # Not at start with colon
            "Tell me about god mode",
            "How does god mode work?",
            "GOD_MODE: test",  # Wrong format (underscore)
            "GODMODE: test",  # Missing space
        ]

        for user_input in not_god_mode:
            with self.subTest(input=user_input):
                agent, _ = get_agent_for_input(user_input)
                self.assertIsInstance(
                    agent,
                    StoryModeAgent,
                    f"Expected StoryModeAgent for: {user_input}",
                )


class TestAgentInstructionBuildingIntegration(unittest.TestCase):
    """Integration tests for agent instruction building."""

    @patch("mvp_site.agent_prompts._load_instruction_file")
    def test_story_mode_instruction_building_flow(self, mock_load):
        """Test complete story mode instruction building flow."""
        # Mock instruction file loading
        mock_load.return_value = "Mock instruction content"

        agent = StoryModeAgent()
        instructions = agent.build_system_instructions(
            selected_prompts=[
                constants.PROMPT_TYPE_NARRATIVE,
                constants.PROMPT_TYPE_MECHANICS,
            ],
            use_default_world=False,
            include_continuation_reminder=True,
        )

        # Verify instruction building
        self.assertIsInstance(instructions, str)
        self.assertGreater(len(instructions), 0)

        # Verify that instruction files were loaded
        self.assertTrue(mock_load.called)

    @patch("mvp_site.agent_prompts._load_instruction_file")
    def test_god_mode_instruction_building_flow(self, mock_load):
        """Test complete god mode instruction building flow."""
        # Mock instruction file loading
        mock_load.return_value = "Mock instruction content"

        agent = GodModeAgent()
        instructions = agent.build_system_instructions()

        # Verify instruction building
        self.assertIsInstance(instructions, str)
        self.assertGreater(len(instructions), 0)

        # Verify that instruction files were loaded
        self.assertTrue(mock_load.called)

    @patch("mvp_site.agent_prompts._load_instruction_file")
    def test_story_mode_without_continuation_reminder(self, mock_load):
        """Test story mode instruction building for initial story (no continuation reminder)."""
        mock_load.return_value = "Mock instruction content"

        agent = StoryModeAgent()
        instructions = agent.build_system_instructions(
            selected_prompts=[constants.PROMPT_TYPE_NARRATIVE],
            use_default_world=False,
            include_continuation_reminder=False,  # For initial story
        )

        self.assertIsInstance(instructions, str)
        self.assertGreater(len(instructions), 0)


class TestAgentGameStateIntegration(unittest.TestCase):
    """Integration tests for agents with game state."""

    def test_agent_with_game_state(self):
        """Test that agents properly receive and use game state."""
        # Create mock game state with properly configured combat helper methods
        mock_game_state = Mock()
        mock_game_state.world_data = {
            "world_time": {"year": 1492, "month": "Mirtul", "day": 15},
            "current_location_name": "Waterdeep",
        }
        mock_game_state.combat_state = {"in_combat": False}
        # Explicitly mark character creation as complete to avoid CharacterCreationAgent
        mock_game_state.custom_campaign_state = {"character_creation_completed": True}
        # Populate character data to simulate completed character creation
        mock_game_state.player_character_data = {
            "name": "Test Character",
            "class": "Fighter",
            "hp": 10,
            "max_hp": 10,
        }
        # CombatAgent.matches_game_state() calls is_in_combat() and get_combat_state()
        mock_game_state.is_in_combat.return_value = False
        mock_game_state.get_combat_state.return_value = {"in_combat": False}
        # CampaignUpgradeAgent.matches_game_state() calls is_campaign_upgrade_available()
        mock_game_state.is_campaign_upgrade_available.return_value = False

        # Test story mode agent
        story_agent, _ = get_agent_for_input(
            "I look around", game_state=mock_game_state
        )
        self.assertEqual(story_agent.game_state, mock_game_state)
        self.assertIsInstance(story_agent, StoryModeAgent)

        # Test god mode agent
        god_agent, _ = get_agent_for_input("GOD MODE: test", game_state=mock_game_state)
        self.assertEqual(god_agent.game_state, mock_game_state)
        self.assertIsInstance(god_agent, GodModeAgent)

    def test_agent_without_game_state(self):
        """Test that agents work correctly without game state."""
        story_agent, _ = get_agent_for_input("Hello world", game_state=None)
        self.assertIsNone(story_agent.game_state)
        self.assertIsNotNone(story_agent.prompt_builder)


class TestAgentPromptSetIntegration(unittest.TestCase):
    """Integration tests for agent prompt sets."""

    def test_story_mode_prompt_set_completeness(self):
        """Test that story mode has all required prompts for storytelling."""
        all_prompts = StoryModeAgent.REQUIRED_PROMPTS | StoryModeAgent.OPTIONAL_PROMPTS

        # Must have core prompts
        self.assertIn(constants.PROMPT_TYPE_MASTER_DIRECTIVE, all_prompts)
        self.assertIn(constants.PROMPT_TYPE_GAME_STATE, all_prompts)

        # Must have storytelling prompts
        self.assertIn(constants.PROMPT_TYPE_NARRATIVE, all_prompts)
        self.assertIn(constants.PROMPT_TYPE_DND_SRD, all_prompts)

        # Should NOT have god mode prompt
        self.assertNotIn(constants.PROMPT_TYPE_GOD_MODE, all_prompts)

    def test_god_mode_prompt_set_completeness(self):
        """Test that god mode has all required prompts for administration."""
        all_prompts = GodModeAgent.REQUIRED_PROMPTS | GodModeAgent.OPTIONAL_PROMPTS

        # Must have core prompts
        self.assertIn(constants.PROMPT_TYPE_MASTER_DIRECTIVE, all_prompts)
        self.assertIn(constants.PROMPT_TYPE_GAME_STATE, all_prompts)
        self.assertIn(constants.PROMPT_TYPE_GOD_MODE, all_prompts)

        # Must have mechanics knowledge for proper corrections
        self.assertIn(constants.PROMPT_TYPE_DND_SRD, all_prompts)
        self.assertIn(constants.PROMPT_TYPE_MECHANICS, all_prompts)

        # Should NOT have narrative prompt
        self.assertNotIn(constants.PROMPT_TYPE_NARRATIVE, all_prompts)
        self.assertNotIn(constants.PROMPT_TYPE_CHARACTER_TEMPLATE, all_prompts)

    def test_prompt_set_overlap(self):
        """Test that both agents share appropriate core prompts."""
        story_prompts = (
            StoryModeAgent.REQUIRED_PROMPTS | StoryModeAgent.OPTIONAL_PROMPTS
        )
        god_prompts = GodModeAgent.REQUIRED_PROMPTS | GodModeAgent.OPTIONAL_PROMPTS

        # Both should have these fundamental prompts
        shared_required = {
            constants.PROMPT_TYPE_MASTER_DIRECTIVE,
            constants.PROMPT_TYPE_GAME_STATE,
            constants.PROMPT_TYPE_DND_SRD,
        }

        for prompt in shared_required:
            self.assertIn(prompt, story_prompts, f"StoryMode missing: {prompt}")
            self.assertIn(prompt, god_prompts, f"GodMode missing: {prompt}")


class TestAgentBackwardCompatibility(unittest.TestCase):
    """Integration tests for backward compatibility."""

    def test_import_from_llm_service(self):
        """Test that agents can still be imported from llm_service."""
        # This tests backward compatibility
        from mvp_site.llm_service import (
            BaseAgent as LLMBaseAgent,
            GodModeAgent as LLMGodModeAgent,
            StoryModeAgent as LLMStoryModeAgent,
            get_agent_for_input as llm_get_agent,
        )

        # Verify they are the same classes
        self.assertIs(LLMBaseAgent, BaseAgent)
        self.assertIs(LLMStoryModeAgent, StoryModeAgent)
        self.assertIs(LLMGodModeAgent, GodModeAgent)
        self.assertIs(llm_get_agent, get_agent_for_input)

    def test_import_from_agents_module(self):
        """Test that agents can be imported from agents module."""
        from mvp_site.agents import (
            BaseAgent,
            GodModeAgent,
            StoryModeAgent,
            get_agent_for_input,
        )

        # Verify classes are properly defined
        self.assertTrue(hasattr(BaseAgent, "REQUIRED_PROMPTS"))
        self.assertTrue(hasattr(StoryModeAgent, "build_system_instructions"))
        self.assertTrue(hasattr(GodModeAgent, "matches_input"))
        self.assertTrue(callable(get_agent_for_input))


class TestAgentPreprocessingIntegration(unittest.TestCase):
    """Integration tests for agent input preprocessing."""

    def test_story_mode_preserves_input(self):
        """Test that story mode agent preserves user input."""
        agent = StoryModeAgent()
        test_input = "I attack the goblin!"
        processed = agent.preprocess_input(test_input)
        self.assertEqual(processed, test_input)

    def test_god_mode_preserves_prefix(self):
        """Test that god mode agent inserts warning AFTER GOD MODE prefix."""
        agent = GodModeAgent()
        test_input = "GOD MODE: Set HP to 50"
        processed = agent.preprocess_input(test_input)
        # CRITICAL: Must preserve "GOD MODE:" at the start for system instruction pattern matching
        self.assertTrue(
            processed.startswith("GOD MODE:"),
            f"Expected 'GOD MODE:' prefix preserved at start, got: {processed[:50]}...",
        )
        # Should contain the warning reminder (stripped because it's inserted inline)
        self.assertIn(constants.GOD_MODE_WARNING_PREFIX.strip(), processed)
        # Should preserve the command content
        self.assertIn("Set HP to 50", processed)


class TestAgentsEdgeCasesIntegration(unittest.TestCase):
    """Integration tests for edge cases and coverage details in agents."""

    def setUp(self):
        self.mock_game_state = MagicMock()
        # Basic defaults
        self.mock_game_state.is_in_combat.return_value = False
        self.mock_game_state.data = {}
        self.mock_game_state.last_action_type = "move"
        self.mock_game_state.planning_block = None

        # Disable high-priority agents via patching
        # This is safer than relying on mock state properties
        patcher_upgrade = patch(
            "mvp_site.agents.CampaignUpgradeAgent.matches_game_state",
            return_value=False,
        )
        self.mock_upgrade_matches = patcher_upgrade.start()
        self.addCleanup(patcher_upgrade.stop)

        patcher_faction = patch(
            "mvp_site.agents.FactionManagementAgent.matches_game_state",
            return_value=False,
        )
        self.mock_faction_matches = patcher_faction.start()
        self.addCleanup(patcher_faction.stop)

        patcher_creation = patch(
            "mvp_site.agents.CharacterCreationAgent.matches_game_state",
            return_value=False,
        )
        self.mock_creation_matches = patcher_creation.start()
        self.addCleanup(patcher_creation.stop)

        patcher_combat = patch(
            "mvp_site.agents.CombatAgent.matches_game_state", return_value=False
        )
        self.mock_combat_matches = patcher_combat.start()
        self.addCleanup(patcher_combat.stop)

        patcher_rewards = patch(
            "mvp_site.agents.RewardsAgent.matches_game_state", return_value=False
        )
        self.mock_rewards_matches = patcher_rewards.start()
        self.addCleanup(patcher_rewards.stop)

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    @patch("mvp_site.agents.DialogAgent.matches_game_state")
    @patch("mvp_site.agents.logging_util")
    def test_intent_dialog_initiating(self, mock_logging, mock_matches, mock_classify):
        """Test intent MODE_DIALOG when context is NOT active (initiating)."""
        # Line 2416 coverage
        mock_classify.return_value = (constants.MODE_DIALOG, 0.9)
        mock_matches.return_value = False  # Not active context

        get_agent_for_input("Talk to him", self.mock_game_state)

        # Check logs for "initiating dialog"
        infos = [call.args[0] for call in mock_logging.info.call_args_list]
        self.assertTrue(any("initiating dialog" in i for i in infos))

    def test_dialog_agent_matches_choices_dict(self):
        """Test matches_game_state with choices as a dictionary."""
        # Line 2300 coverage (implied logic in matches_game_state or get_agent_for_input)
        self.mock_game_state.planning_block = {
            "choices": {
                "1": {"text": "Ask about the quest", "description": "Speak to him"},
                "2": {"text": "Attack", "description": "Fight"},
            }
        }
        # DialogAgent now checks dialog_context, not just choices presence
        self.mock_game_state.dialog_context = {"active": True}

        # Should match "Ask" keyword or explicit context
        self.assertTrue(DialogAgent.matches_game_state(self.mock_game_state))

    def test_dialog_agent_matches_choices_invalid(self):
        """Test matches_game_state with invalid choices type."""
        # Line 1618 coverage (approximate)
        self.mock_game_state.planning_block = {"choices": "not_a_list_or_dict"}

        # Should handle gracefully and return False (unless other criteria match)
        self.assertFalse(DialogAgent.matches_game_state(self.mock_game_state))

    def test_get_agent_input_choice_matching_dict(self):
        """Test fuzzy choice matching in get_agent_for_input with dict choices."""
        # Coverage for choice matching logic in get_agent_for_input
        self.mock_game_state.data = {
            "planning_block": {
                "choices": {
                    "a": {"text": "Ask about the dragon", "description": "Dialog"},
                    "b": {"text": "Leave", "description": "Exit"},
                }
            }
        }
        self.mock_game_state.dialog_context = {"active": True}

        # User input matches choice text exactly
        agent, _ = get_agent_for_input("Ask about the dragon", self.mock_game_state)
        self.assertIsInstance(agent, DialogAgent)

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_get_agent_input_data_none(self, mock_classify):
        """Test get_agent_for_input when game_state.data is None."""
        # Stub classify intent to avoid external call
        mock_classify.return_value = (constants.MODE_CHARACTER, 1.0)

        # Line 2289 coverage
        self.mock_game_state.data = None

        # Should not crash
        agent, _ = get_agent_for_input("Hello", self.mock_game_state)
        self.assertIsNotNone(agent)


if __name__ == "__main__":
    unittest.main()

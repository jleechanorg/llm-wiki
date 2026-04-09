"""
Test-Driven Development: Tests for Agent classes (StoryModeAgent, GodModeAgent, CombatAgent, CharacterCreationAgent)

These tests verify the behavior of the agent architecture that manages
different interaction modes (story mode vs god mode vs combat mode vs character creation mode) in WorldArchitect.AI.

Agent Architecture:
- BaseAgent: Abstract base class with common functionality
- StoryModeAgent: Handles narrative storytelling (character mode)
- GodModeAgent: Handles administrative commands (god mode)
- CharacterCreationAgent: Handles focused character creation (highest priority except god mode)
- CombatAgent: Handles active combat encounters (combat mode)
"""

from __future__ import annotations

# ruff: noqa: E402, PT009, PT027
import io
import json
import os
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import MagicMock, Mock, patch

# Add the project root to the Python path so we can import modules
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.insert(0, project_root)

from mvp_site import constants
from mvp_site.agent_prompts import (
    PromptBuilder,
    _generate_example_from_def,
    _inject_schema_placeholders,
    _load_instruction_file,
    _loaded_instructions_cache,
)

# PromptBuilder lives with agent prompt utilities
# Import from agents module (canonical location)
from mvp_site.agents import (
    ALL_AGENT_CLASSES,
    FACTION_FORCE_THRESHOLD,
    GAME_STATE_PLANNING_PAIR,
    MANDATORY_FIRST_PROMPT,
    BaseAgent,
    CampaignUpgradeAgent,
    CharacterCreationAgent,
    CombatAgent,
    DeferredRewardsAgent,
    DialogAgent,
    FactionManagementAgent,
    FixedPromptAgent,
    GodModeAgent,
    HeavyDialogAgent,
    InfoAgent,
    LevelUpAgent,
    PlanningAgent,
    RewardsAgent,
    SpicyModeAgent,
    StoryModeAgent,
    get_agent_for_input,
    mode_advances_time,
    validate_all_agent_prompt_orders,
    validate_prompt_order,
)
from mvp_site.narrative_response_schema import VALID_RISK_LEVELS


def create_mock_game_state(
    in_combat=False,
    combat_state_dict=None,
    character_creation_completed=True,
    character_name="Test Character",
    character_class="Fighter",
):
    """Helper to create a mock GameState with required methods.

    Args:
        in_combat: Whether the game is in combat mode
        combat_state_dict: Optional combat state dict
        character_creation_completed: Whether character creation is done (default True)
            to avoid triggering CharacterCreationAgent in existing tests
        character_name: Name of the character (empty string triggers character creation)
        character_class: Class of the character (empty string triggers character creation)
    """
    mock_state = Mock()
    mock_state.is_in_combat.return_value = in_combat

    if combat_state_dict is None:
        combat_state_dict = {"in_combat": in_combat}

    mock_state.get_combat_state.return_value = combat_state_dict
    mock_state.combat_state = combat_state_dict

    # Mock custom_campaign_state for CharacterCreationAgent checks
    mock_state.custom_campaign_state = {
        "character_creation_completed": character_creation_completed,
    }

    # Mock player_character_data for CharacterCreationAgent checks
    mock_state.player_character_data = {
        "name": character_name,
        "class": character_class,
    }

    # Ensure campaign upgrade is not triggered in tests
    mock_state.is_campaign_upgrade_available.return_value = False
    return mock_state


def create_rewards_game_state(
    combat_state: dict | None = None,
    encounter_state: dict | None = None,
    rewards_pending: dict | None = None,
):
    """Helper to create a mock GameState for rewards detection tests."""

    mock_state = Mock()
    mock_state.get_combat_state.return_value = combat_state or {"in_combat": False}
    mock_state.get_encounter_state.return_value = encounter_state or {
        "encounter_active": False
    }
    mock_state.get_rewards_pending.return_value = rewards_pending
    mock_state.is_in_combat.return_value = mock_state.get_combat_state.return_value.get(
        "in_combat", False
    )

    # Mock attributes for CharacterCreationAgent checks (character creation completed)
    mock_state.custom_campaign_state = {"character_creation_completed": True}
    mock_state.player_character_data = {"name": "Test Character", "class": "Fighter"}

    # Ensure campaign upgrade is not triggered in tests
    mock_state.is_campaign_upgrade_available.return_value = False

    return mock_state


def create_character_creation_game_state(
    character_creation_completed=False,
    character_name="",
    character_class="",
    level_up_pending=False,
    level_up_available=False,
    level=1,
    experience_current=0,
):
    """Helper to create a mock GameState for character creation/level-up mode tests.

    Args:
        character_creation_completed: Whether character creation is done
        character_name: Name of the character (empty triggers creation mode)
        character_class: Class of the character (empty triggers creation mode)
        level_up_pending: Legacy flag for pending level-up on custom_campaign_state
        level_up_available: Whether rewards_pending indicates a level-up is available
    """
    mock_state = Mock()
    mock_state.is_in_combat.return_value = False
    mock_state.get_combat_state.return_value = {"in_combat": False}
    mock_state.combat_state = {"in_combat": False}

    in_progress = not character_creation_completed and (
        not character_name or not character_class
    )

    mock_state.custom_campaign_state = {
        "character_creation_completed": character_creation_completed,
        "level_up_pending": level_up_pending,
        "character_creation_in_progress": in_progress,
    }
    mock_state.player_character_data = {
        "name": character_name,
        "class": character_class,
        "level": level,
        "experience": {"current": experience_current},
    }

    mock_state.rewards_pending = {"level_up_available": level_up_available}

    # Ensure campaign upgrade is not triggered in tests
    mock_state.is_campaign_upgrade_available.return_value = False

    return mock_state


class TestBaseAgent(unittest.TestCase):
    """Test cases for BaseAgent abstract class."""

    def test_base_agent_is_abstract(self):
        """BaseAgent cannot be instantiated directly."""
        with self.assertRaises(TypeError) as context:
            BaseAgent()
        self.assertIn("abstract", str(context.exception).lower())

    def test_base_agent_class_attributes(self):
        """BaseAgent has required class attributes."""
        self.assertTrue(hasattr(BaseAgent, "REQUIRED_PROMPTS"))
        self.assertTrue(hasattr(BaseAgent, "OPTIONAL_PROMPTS"))

    def test_base_agent_advances_time_default_true(self):
        """BaseAgent.advances_time defaults to True for time-advancing agents.

        This test verifies only the advances_time flag default on concrete agents.
        """
        # Test concrete agents that should advance time
        for agent_class in [
            StoryModeAgent,
            CombatAgent,
            DialogAgent,
            HeavyDialogAgent,
            FactionManagementAgent,
        ]:
            agent = agent_class()
            self.assertTrue(
                agent.advances_time,
                f"{agent_class.__name__}.advances_time should be True (advances game time)",
            )

    def test_non_time_advancing_agents(self):
        """Administrative/planning/build agents do not advance time.

        These agents query/plan/build without world-time progression.
        """
        for agent_class in [
            GodModeAgent,
            InfoAgent,
            PlanningAgent,
            CharacterCreationAgent,
            RewardsAgent,
            DeferredRewardsAgent,
        ]:
            agent = agent_class()
            self.assertFalse(
                agent.advances_time,
                f"{agent_class.__name__}.advances_time should be False (no time advancement)",
            )

    def test_mode_advances_time_mapping(self):
        """Mode-based helper should align with agent time-advancement semantics."""
        self.assertTrue(mode_advances_time(constants.MODE_CHARACTER))
        self.assertTrue(mode_advances_time(constants.MODE_DIALOG))
        self.assertTrue(mode_advances_time(constants.MODE_DIALOG_HEAVY))
        self.assertTrue(mode_advances_time(constants.MODE_COMBAT))
        self.assertTrue(mode_advances_time(constants.MODE_FACTION))
        self.assertTrue(mode_advances_time(constants.MODE_SPICY))

        self.assertFalse(mode_advances_time(constants.MODE_GOD))
        self.assertFalse(mode_advances_time(constants.MODE_THINK))
        self.assertFalse(mode_advances_time(constants.MODE_INFO))
        self.assertFalse(mode_advances_time(constants.MODE_CHARACTER_CREATION))
        self.assertFalse(mode_advances_time(constants.MODE_REWARDS))
        self.assertFalse(mode_advances_time(constants.MODE_DEFERRED_REWARDS))


class TestDialogAgentBasics(unittest.TestCase):
    """Test cases for DialogAgent configuration and behavior."""

    def test_dialog_agent_mode(self):
        """DialogAgent has correct mode identifier."""
        self.assertEqual(DialogAgent.MODE, constants.MODE_DIALOG)

    def test_heavy_dialog_agent_mode(self):
        """HeavyDialogAgent has correct mode identifier."""
        self.assertEqual(HeavyDialogAgent.MODE, constants.MODE_DIALOG_HEAVY)

    def test_dialog_agent_required_prompts(self):
        """DialogAgent REQUIRED_PROMPTS matches REQUIRED_PROMPT_ORDER."""
        # Directly derive from class attributes to avoid duplication
        expected_prompts = frozenset(DialogAgent.REQUIRED_PROMPT_ORDER)
        self.assertEqual(DialogAgent.REQUIRED_PROMPTS, expected_prompts)

        # Verify critical prompts are present
        self.assertIn(
            constants.PROMPT_TYPE_MASTER_DIRECTIVE, DialogAgent.REQUIRED_PROMPTS
        )
        self.assertIn(constants.PROMPT_TYPE_DIALOG, DialogAgent.REQUIRED_PROMPTS)
        self.assertIn(
            constants.PROMPT_TYPE_NARRATIVE_LITE, DialogAgent.REQUIRED_PROMPTS
        )  # Not NARRATIVE

    def test_dialog_agent_prompt_order_invariants(self):
        """DialogAgent prompt order follows required invariants."""
        order = DialogAgent.REQUIRED_PROMPT_ORDER
        self.assertEqual(order[0], constants.PROMPT_TYPE_MASTER_DIRECTIVE)

        game_idx = order.index(constants.PROMPT_TYPE_GAME_STATE)
        planning_idx = order.index(constants.PROMPT_TYPE_PLANNING_PROTOCOL)
        self.assertEqual(planning_idx, game_idx + 1)

    def test_dialog_agent_in_all_agent_classes(self):
        """DialogAgent should be registered in ALL_AGENT_CLASSES."""
        self.assertIn(DialogAgent, ALL_AGENT_CLASSES)

    def test_heavy_dialog_agent_in_all_agent_classes(self):
        """HeavyDialogAgent should be registered in ALL_AGENT_CLASSES."""
        self.assertIn(HeavyDialogAgent, ALL_AGENT_CLASSES)

    def test_heavy_dialog_agent_inherits_dialog_agent(self):
        """HeavyDialogAgent should inherit DialogAgent defaults and behavior."""
        self.assertTrue(issubclass(HeavyDialogAgent, DialogAgent))


class TestDialogAgentRouting(unittest.TestCase):
    """Test cases for DialogAgent routing in get_agent_for_input."""

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_dialog_context_triggers_dialog(self, mock_classify):
        """Active dialog_context should route to DialogAgent via classifier."""
        mock_classify.return_value = (constants.MODE_DIALOG, 0.9)
        mock_state = create_mock_game_state(in_combat=False)
        mock_state.dialog_context = {"active": True}

        agent, _ = get_agent_for_input("continue", game_state=mock_state)
        self.assertIsInstance(agent, DialogAgent)

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_enable_faction_minigame_overrides_dialog(self, mock_classify):
        """Enable faction minigame should route via semantic intent even with dialog context."""
        mock_classify.return_value = (constants.MODE_FACTION, 0.9)
        mock_state = create_mock_game_state(in_combat=False)
        mock_state.dialog_context = {"active": True}

        agent, metadata = get_agent_for_input(
            "enable_faction_minigame", game_state=mock_state
        )
        self.assertIsInstance(agent, FactionManagementAgent)
        self.assertEqual(metadata["classifier_source"], "semantic_intent")

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_enable_faction_minigame_overrides_dialog_even_with_low_confidence(
        self, mock_classify
    ):
        """Exact 'enable_faction_minigame' should override dialog even with LOW classifier confidence.

        Regression test: Ensures exact enable command is deterministic, not confidence-gated.
        If classifier returns MODE_FACTION with confidence < 0.7, the enable command should
        still route to FactionManagementAgent (deterministic override).
        """
        # LOW confidence - would normally NOT override dialog
        mock_classify.return_value = (constants.MODE_FACTION, 0.5)
        mock_state = create_mock_game_state(in_combat=False)
        mock_state.dialog_context = {"active": True}

        agent, metadata = get_agent_for_input(
            "enable_faction_minigame", game_state=mock_state
        )

        # Should STILL route to FactionManagementAgent (deterministic override for exact command)
        self.assertIsInstance(agent, FactionManagementAgent)
        self.assertEqual(metadata["classifier_source"], "semantic_intent")

    def test_combat_state_overrides_dialog_context(self):
        """Combat state takes priority over dialog context."""
        mock_state = create_mock_game_state(in_combat=True)
        mock_state.dialog_context = {"active": True}

        agent, _ = get_agent_for_input("continue", game_state=mock_state)
        self.assertIsInstance(agent, CombatAgent)

    def test_explicit_mode_dialog_rejected(self):
        """Forcing mode='dialog' is rejected - falls through to automatic selection."""
        # DialogAgent is an INTERNAL mode - users cannot force it
        # Attempting to force it should fall through to automatic selection
        with patch(
            "mvp_site.agents.intent_classifier.classify_intent"
        ) as mock_classify:
            mock_classify.return_value = (constants.MODE_CHARACTER, 0.1)
            agent, _ = get_agent_for_input("any input", mode="dialog")
        # Should NOT be DialogAgent (no dialog context in game state)
        # Should fall through to StoryModeAgent (default)
        self.assertIsInstance(agent, StoryModeAgent)

    def test_dialog_agent_builder_flags(self):
        """DialogAgent.builder_flags() returns correct debug flag."""
        mock_state = create_mock_game_state(in_combat=False)
        agent = DialogAgent(mock_state)
        flags = agent.builder_flags()
        self.assertIsInstance(flags, dict)
        self.assertEqual(flags.get("include_debug"), False)

    def test_heavy_dialog_agent_builder_flags(self):
        """HeavyDialogAgent.builder_flags() returns correct debug flag."""
        mock_state = create_mock_game_state(in_combat=False)
        agent = HeavyDialogAgent(mock_state)
        flags = agent.builder_flags()
        self.assertIsInstance(flags, dict)
        self.assertEqual(flags.get("include_debug"), False)

    def test_dialog_agent_matches_input_always_false(self):
        """DialogAgent.matches_input() always returns False (no mode forcing)."""
        # DialogAgent cannot be triggered through input patterns or mode forcing
        # Selection happens only through semantic classifier or game state continuity
        self.assertFalse(DialogAgent.matches_input("any text", _mode="dialog"))
        self.assertFalse(DialogAgent.matches_input("talk", _mode="DIALOG"))
        self.assertFalse(DialogAgent.matches_input("talk", _mode="combat"))
        self.assertFalse(DialogAgent.matches_input("talk", _mode=None))
        self.assertFalse(
            DialogAgent.matches_input("negotiate with the merchant", _mode=None)
        )

    def test_dialog_agent_matches_game_state_last_action(self):
        """DialogAgent.matches_game_state() detects last_action_type='dialog'."""
        mock_state = create_mock_game_state(in_combat=False)
        mock_state.last_action_type = "dialog"
        self.assertTrue(DialogAgent.matches_game_state(mock_state))

        mock_state.last_action_type = "talk"
        self.assertTrue(DialogAgent.matches_game_state(mock_state))

        mock_state.last_action_type = "conversation"
        self.assertTrue(DialogAgent.matches_game_state(mock_state))

        mock_state.last_action_type = "attack"
        self.assertFalse(DialogAgent.matches_game_state(mock_state))

    def test_dialog_agent_matches_game_state_null_safety(self):
        """DialogAgent.matches_game_state() safely handles None in choice fields."""
        mock_state = create_mock_game_state(in_combat=False)
        # Setup a planning block with None values in choices
        mock_state.planning_block = {
            "choices": [
                {"text": None, "description": "some desc"},
                {"text": "some text", "description": None},
                {"text": None, "description": None},
            ]
        }

        # This should NOT crash with AttributeError
        # and should return False (no match found)
        self.assertFalse(DialogAgent.matches_game_state(mock_state))

    def test_dialog_agent_substring_false_positives(self):
        """DialogAgent filters substring false positives (e.g. 'flask' matching 'ask')."""
        mock_state = create_mock_game_state(in_combat=False)
        # Setup choices that contain "ask" as substring but are NOT dialog
        mock_state.planning_block = {
            "choices": [
                {"text": "Use the healing flask", "description": "Drink it"},
                {"text": "Complete the task", "description": "Finish the work"},
                {"text": "Wear the mask", "description": "Hide your face"},
            ]
        }

        # Should return False (word boundary check prevents match)
        self.assertFalse(DialogAgent.matches_game_state(mock_state))

    def test_dialog_agent_matches_game_state_planning_block_no_keywords(self):
        """DialogAgent.matches_game_state() NO LONGER uses keyword matching on planning blocks.

        Per CLAUDE.md: "NO KEYWORD MATCHING for dialog detection"
        Dialog routing ONLY goes through the semantic classifier (classify_intent).
        Planning block choices do NOT trigger DialogAgent via matches_game_state.
        """
        mock_state = create_mock_game_state(in_combat=False)
        # Planning block with multiple dialog-like choices (using dict format)
        # NOTE: Keyword matching REMOVED - should return False
        mock_state.planning_block = {
            "choices": {
                "1": {
                    "text": "Talk to the merchant",
                    "description": "Negotiate a better price",
                },
                "2": {
                    "text": "Persuade the guard",
                    "description": "Convince him to let you pass",
                },
                "3": {"text": "Attack immediately", "description": "No time for talk"},
            }
        }
        # UPDATED: Keyword matching removed - now returns False
        # Dialog detection uses classifier only (test_semantic_intent_dialog_routing)
        self.assertFalse(DialogAgent.matches_game_state(mock_state))

        # Planning block with list format
        mock_state.planning_block = {
            "choices": [
                {"text": "Ask about rumors", "description": "Gather information"},
                {
                    "text": "Discuss the quest",
                    "description": "Speak with the innkeeper",
                },
            ]
        }
        # UPDATED: Keyword matching removed - now returns False
        self.assertFalse(DialogAgent.matches_game_state(mock_state))

        # Single choice - also no keyword matching
        mock_state.planning_block = {
            "choices": [{"text": "Talk to them", "description": "Start conversation"}]
        }
        # UPDATED: Keyword matching removed - now returns False
        self.assertFalse(DialogAgent.matches_game_state(mock_state))

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_semantic_intent_dialog_routing(self, mock_classify):
        """Semantic intent MODE_DIALOG routes to DialogAgent."""
        mock_classify.return_value = (constants.MODE_DIALOG, 0.85)
        mock_state = create_mock_game_state(in_combat=False)

        agent, _ = get_agent_for_input("talk to the innkeeper", game_state=mock_state)
        self.assertIsInstance(agent, DialogAgent)

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_semantic_intent_dialog_stays_on_dialog_agent_no_heuristic_escalation(
        self, mock_classify
    ):
        """MODE_DIALOG stays on DialogAgent even for companion-heavy wording (no heuristic escalation)."""
        mock_classify.return_value = (constants.MODE_DIALOG, 0.92)
        mock_state = create_mock_game_state(in_combat=False)
        mock_state.dialog_context = {"active": True, "active_npc": "lyra"}
        mock_state.npc_data = {
            "lyra": {"name": "Lyra", "relationship": "companion"},
        }

        agent, _ = get_agent_for_input(
            "this is a major conversation with Lyra about her companion arc",
            game_state=mock_state,
        )
        self.assertIsInstance(agent, DialogAgent)
        self.assertNotIsInstance(agent, HeavyDialogAgent)

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_semantic_intent_dialog_does_not_use_major_phrase_keywords_for_heavy(
        self, mock_classify
    ):
        """Major-phrase wording alone should not escalate to HeavyDialogAgent."""
        mock_classify.return_value = (constants.MODE_DIALOG, 0.92)
        mock_state = create_mock_game_state(in_combat=False)
        mock_state.dialog_context = {"active": True}
        mock_state.npc_data = {}

        agent, _ = get_agent_for_input(
            "this is a major conversation with serious talk and a confession",
            game_state=mock_state,
        )
        self.assertIsInstance(agent, DialogAgent)
        self.assertNotIsInstance(agent, HeavyDialogAgent)

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_semantic_intent_dialog_heavy_routes_to_heavy_dialog_agent(
        self, mock_classify
    ):
        """Semantic MODE_DIALOG_HEAVY should route directly to HeavyDialogAgent."""
        mock_classify.return_value = (constants.MODE_DIALOG_HEAVY, 0.93)
        mock_state = create_mock_game_state(in_combat=False)

        agent, metadata = get_agent_for_input(
            "help my companion through a major emotional crisis",
            game_state=mock_state,
        )
        self.assertIsInstance(agent, HeavyDialogAgent)
        self.assertEqual(metadata["intent"], constants.MODE_DIALOG_HEAVY)

    def test_api_explicit_mode_dialog_rejected(self):
        """API explicit mode='dialog' is rejected - falls through to automatic selection."""
        mock_state = create_mock_game_state(in_combat=False)
        # Attempting to force mode="dialog" should be rejected and fall through
        agent, _ = get_agent_for_input("continue", mode="dialog", game_state=mock_state)
        # Should NOT be DialogAgent (internal mode cannot be forced)
        self.assertIsInstance(agent, StoryModeAgent)

        # Test case-insensitive rejection
        agent, _ = get_agent_for_input("continue", mode="DIALOG", game_state=mock_state)
        self.assertIsInstance(agent, StoryModeAgent)

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_mode_dialog_heavy_overrides_active_dialog_context_regardless_of_confidence(
        self, mock_classify
    ):
        """MODE_DIALOG_HEAVY should route to HeavyDialogAgent even during active dialog, regardless of confidence.

        Regression test for bead PR-mde:
        When classifier returns MODE_DIALOG_HEAVY while dialog context is active,
        the request should route to HeavyDialogAgent, not DialogAgent, even if
        confidence < 0.7. Heavy dialog is a semantic routing decision that should
        override state-based dialog continuity.
        """
        # Setup: Active dialog context (would normally route to DialogAgent)
        mock_state = create_mock_game_state(in_combat=False)
        mock_state.last_action_type = "dialog"

        # Test 1: High confidence MODE_DIALOG_HEAVY (>= 0.7)
        mock_classify.return_value = (constants.MODE_DIALOG_HEAVY, 0.85)
        agent, metadata = get_agent_for_input(
            "I need to have a deep conversation with my companion about their past",
            game_state=mock_state,
        )
        self.assertIsInstance(
            agent,
            HeavyDialogAgent,
            "High-confidence MODE_DIALOG_HEAVY should route to HeavyDialogAgent",
        )
        self.assertEqual(metadata["intent"], constants.MODE_DIALOG_HEAVY)

        # Test 2: Low confidence MODE_DIALOG_HEAVY (< 0.7)
        # This is the regression scenario: should still route to HeavyDialogAgent
        mock_classify.return_value = (constants.MODE_DIALOG_HEAVY, 0.5)
        agent, metadata = get_agent_for_input(
            "Let's discuss something important",
            game_state=mock_state,
        )
        self.assertIsInstance(
            agent,
            HeavyDialogAgent,
            "Low-confidence MODE_DIALOG_HEAVY should still route to HeavyDialogAgent, "
            "not downgrade to DialogAgent during active dialog",
        )
        self.assertEqual(metadata["intent"], constants.MODE_DIALOG_HEAVY)


class TestBaseAgentCampaignTierPrompts(unittest.TestCase):
    """Test cases for BaseAgent campaign tier-specific prompt loading."""

    def _create_mock_game_state_with_tier(self, campaign_tier: str | None):
        """Helper to create mock game state with campaign tier."""
        mock_state = Mock()
        mock_state.get_campaign_tier = Mock(return_value=campaign_tier)
        # Add attributes needed by build_character_identity_block() and build_god_mode_directives_block()
        # These methods check hasattr() and return empty strings if attributes don't exist
        # So we don't need to set them - the methods will return "" when attributes are missing
        # But we need to ensure Mock doesn't auto-create attributes that return Mock objects
        mock_state.player_character_data = {}
        mock_state.custom_campaign_state = {}
        mock_state.debug_info = {}
        mock_state.npc_data = {}
        mock_state.world_data = {}
        # Ensure get_character_identity_block doesn't exist (so it uses fallback)
        if hasattr(mock_state, "get_character_identity_block"):
            delattr(mock_state, "get_character_identity_block")
        return mock_state

    @patch("mvp_site.agent_prompts._load_instruction_file")
    def test_base_agent_loads_divine_prompt_when_tier_divine(self, mock_load):
        """Verify Divine Leverage prompt loads when campaign_tier == CAMPAIGN_TIER_DIVINE."""

        # Mock must return strings for all calls, not just the divine one
        def mock_load_side_effect(prompt_type):
            if prompt_type == constants.PROMPT_TYPE_DIVINE_SYSTEM:
                return "Divine Leverage System Prompt"
            return f"Mock prompt for {prompt_type}"

        mock_load.side_effect = mock_load_side_effect
        mock_state = self._create_mock_game_state_with_tier(
            constants.CAMPAIGN_TIER_DIVINE
        )
        agent = StoryModeAgent(game_state=mock_state)

        instructions = agent.build_system_instructions()

        mock_load.assert_called_with(constants.PROMPT_TYPE_DIVINE_SYSTEM)
        # build_system_instructions() returns a string, check if divine prompt is in it
        self.assertIn("Divine Leverage System Prompt", instructions)

    @patch("mvp_site.agent_prompts._load_instruction_file")
    def test_base_agent_loads_sovereign_prompt_when_tier_sovereign(self, mock_load):
        """Verify Sovereign Protocol prompt loads when campaign_tier == CAMPAIGN_TIER_SOVEREIGN."""

        # Mock must return strings for all calls, not just the sovereign one
        def mock_load_side_effect(prompt_type):
            if prompt_type == constants.PROMPT_TYPE_SOVEREIGN_SYSTEM:
                return "Sovereign Protocol System Prompt"
            return f"Mock prompt for {prompt_type}"

        mock_load.side_effect = mock_load_side_effect
        mock_state = self._create_mock_game_state_with_tier(
            constants.CAMPAIGN_TIER_SOVEREIGN
        )
        agent = StoryModeAgent(game_state=mock_state)

        instructions = agent.build_system_instructions()

        mock_load.assert_called_with(constants.PROMPT_TYPE_SOVEREIGN_SYSTEM)
        # build_system_instructions() returns a string, check if sovereign prompt is in it
        self.assertIn("Sovereign Protocol System Prompt", instructions)

    @patch("mvp_site.agent_prompts._load_instruction_file")
    def test_base_agent_no_tier_prompt_when_tier_normal(self, mock_load):
        """Verify no tier prompt loads for normal campaigns."""
        # Mock must return strings for all calls
        mock_load.return_value = "Mock prompt content"
        mock_state = self._create_mock_game_state_with_tier("normal")
        agent = StoryModeAgent(game_state=mock_state)

        agent.build_system_instructions()

        # Should not call divine or sovereign prompt loading
        # (get_campaign_tier is called, but tier doesn't match divine/sovereign)
        # Verify neither divine nor sovereign prompts were loaded
        divine_calls = [
            call
            for call in mock_load.call_args_list
            if len(call[0]) > 0 and call[0][0] == constants.PROMPT_TYPE_DIVINE_SYSTEM
        ]
        sovereign_calls = [
            call
            for call in mock_load.call_args_list
            if len(call[0]) > 0 and call[0][0] == constants.PROMPT_TYPE_SOVEREIGN_SYSTEM
        ]
        self.assertEqual(len(divine_calls), 0)
        self.assertEqual(len(sovereign_calls), 0)

    @patch("mvp_site.agent_prompts._load_instruction_file")
    def test_base_agent_no_tier_prompt_when_game_state_none(self, mock_load):
        """Verify no tier prompt loads when game_state is None."""
        # Mock must return strings for all calls (build_system_instructions still loads other prompts)
        mock_load.return_value = "Mock prompt content"
        agent = StoryModeAgent(game_state=None)

        agent.build_system_instructions()

        # Should not call divine or sovereign prompt loading (no game_state means no tier check)
        divine_calls = [
            call
            for call in mock_load.call_args_list
            if len(call[0]) > 0 and call[0][0] == constants.PROMPT_TYPE_DIVINE_SYSTEM
        ]
        sovereign_calls = [
            call
            for call in mock_load.call_args_list
            if len(call[0]) > 0 and call[0][0] == constants.PROMPT_TYPE_SOVEREIGN_SYSTEM
        ]
        self.assertEqual(len(divine_calls), 0)
        self.assertEqual(len(sovereign_calls), 0)

    @patch("mvp_site.agent_prompts._load_instruction_file")
    @patch("mvp_site.agent_prompts.logging_util")
    def test_base_agent_handles_missing_divine_prompt_gracefully(
        self, mock_logging, mock_load
    ):
        """Verify warning logged when divine prompt file missing."""

        # Mock must return strings for all calls, empty string for divine indicates missing file
        def mock_load_side_effect(prompt_type):
            if prompt_type == constants.PROMPT_TYPE_DIVINE_SYSTEM:
                return ""  # Empty string indicates missing file
            return f"Mock prompt for {prompt_type}"

        mock_load.side_effect = mock_load_side_effect
        mock_state = self._create_mock_game_state_with_tier(
            constants.CAMPAIGN_TIER_DIVINE
        )
        agent = StoryModeAgent(game_state=mock_state)

        agent.build_system_instructions()

        mock_load.assert_called_with(constants.PROMPT_TYPE_DIVINE_SYSTEM)
        mock_logging.warning.assert_called()
        self.assertIn("DIVINE_TIER", str(mock_logging.warning.call_args))

    @patch("mvp_site.agent_prompts._load_instruction_file")
    @patch("mvp_site.agent_prompts.logging_util")
    def test_base_agent_handles_missing_sovereign_prompt_gracefully(
        self, mock_logging, mock_load
    ):
        """Verify warning logged when sovereign prompt file missing."""

        # Mock must return strings for all calls, empty string for sovereign indicates missing file
        def mock_load_side_effect(prompt_type):
            if prompt_type == constants.PROMPT_TYPE_SOVEREIGN_SYSTEM:
                return ""  # Empty string indicates missing file
            return f"Mock prompt for {prompt_type}"

        mock_load.side_effect = mock_load_side_effect
        mock_state = self._create_mock_game_state_with_tier(
            constants.CAMPAIGN_TIER_SOVEREIGN
        )
        agent = StoryModeAgent(game_state=mock_state)

        agent.build_system_instructions()

        mock_load.assert_called_with(constants.PROMPT_TYPE_SOVEREIGN_SYSTEM)
        mock_logging.warning.assert_called()
        self.assertIn("SOVEREIGN_TIER", str(mock_logging.warning.call_args))

    @patch("mvp_site.agent_prompts._load_instruction_file")
    def test_fixed_prompt_agent_includes_tier_prompts(self, mock_load):
        """Verify fixed-prompt agents also receive tier system prompts."""

        def mock_load_side_effect(prompt_type):
            if prompt_type == constants.PROMPT_TYPE_DIVINE_SYSTEM:
                return "Divine Leverage System Prompt"
            return f"Mock prompt for {prompt_type}"

        mock_load.side_effect = mock_load_side_effect
        mock_state = self._create_mock_game_state_with_tier(
            constants.CAMPAIGN_TIER_DIVINE
        )
        agent = InfoAgent(game_state=mock_state)

        instructions = agent.build_system_instructions()

        mock_load.assert_called_with(constants.PROMPT_TYPE_DIVINE_SYSTEM)
        self.assertIn("Divine Leverage System Prompt", instructions)

    @patch("mvp_site.agent_prompts._load_instruction_file")
    def test_all_agents_include_tier_prompts(self, mock_load):
        """Verify every agent receives divine/sovereign system prompts."""

        def mock_load_side_effect(prompt_type):
            if prompt_type == constants.PROMPT_TYPE_DIVINE_SYSTEM:
                return "Divine Leverage System Prompt"
            if prompt_type == constants.PROMPT_TYPE_SOVEREIGN_SYSTEM:
                return "Sovereign Protocol System Prompt"
            return f"Mock prompt for {prompt_type}"

        mock_load.side_effect = mock_load_side_effect

        divine_state = self._create_mock_game_state_with_tier(
            constants.CAMPAIGN_TIER_DIVINE
        )
        sovereign_state = self._create_mock_game_state_with_tier(
            constants.CAMPAIGN_TIER_SOVEREIGN
        )

        agent_classes = [
            StoryModeAgent,
            GodModeAgent,
            CharacterCreationAgent,
            PlanningAgent,
            InfoAgent,
            CombatAgent,
            RewardsAgent,
            DeferredRewardsAgent,
            DialogAgent,
            SpicyModeAgent,
            FactionManagementAgent,
            CampaignUpgradeAgent,
        ]

        for agent_cls in agent_classes:
            with self.subTest(agent=agent_cls.__name__, tier="divine"):
                agent = agent_cls(game_state=divine_state)
                instructions = agent.build_system_instructions()
                self.assertIn("Divine Leverage System Prompt", instructions)

            with self.subTest(agent=agent_cls.__name__, tier="sovereign"):
                agent = agent_cls(game_state=sovereign_state)
                instructions = agent.build_system_instructions()
                self.assertIn("Sovereign Protocol System Prompt", instructions)

    @patch("mvp_site.agent_prompts._load_instruction_file")
    def test_prompt_builder_resolves_tier_from_dict_state(self, mock_load):
        """Verify tier resolution works for dict-based game_state."""

        def mock_load_side_effect(prompt_type):
            if prompt_type == constants.PROMPT_TYPE_DIVINE_SYSTEM:
                return "Divine Leverage System Prompt"
            return f"Mock prompt for {prompt_type}"

        mock_load.side_effect = mock_load_side_effect
        builder = PromptBuilder()
        builder.game_state = {
            "custom_campaign_state": {"campaign_tier": constants.CAMPAIGN_TIER_DIVINE}
        }

        parts = ["# File: master_directive.md"]
        instructions = builder.finalize_instructions(parts, use_default_world=False)

        self.assertIn("Divine Leverage System Prompt", instructions)


class TestStoryModeAgent(unittest.TestCase):
    """Test cases for StoryModeAgent class."""

    def test_story_mode_agent_creation(self):
        """StoryModeAgent can be instantiated."""
        agent = StoryModeAgent()
        self.assertIsInstance(agent, BaseAgent)
        self.assertIsInstance(agent, StoryModeAgent)

    def test_story_mode_agent_with_game_state(self):
        """StoryModeAgent accepts game_state parameter."""
        mock_game_state = create_mock_game_state()
        agent = StoryModeAgent(game_state=mock_game_state)
        self.assertEqual(agent.game_state, mock_game_state)

    def test_story_mode_agent_required_prompts(self):
        """StoryModeAgent has correct required prompts.

        PROMPT_TYPE_LIVING_WORLD is intentionally absent from REQUIRED_PROMPTS.
        It uses the always-on injection path (fires after narrative/mechanics)
        to reduce prompt competition with the large game_state block. (rev-m36u)
        """
        expected_prompts = {
            constants.PROMPT_TYPE_MASTER_DIRECTIVE,
            constants.PROMPT_TYPE_GAME_STATE,
            constants.PROMPT_TYPE_PLANNING_PROTOCOL,  # Canonical planning block schema
            constants.PROMPT_TYPE_DND_SRD,
        }
        self.assertEqual(StoryModeAgent.REQUIRED_PROMPTS, frozenset(expected_prompts))
        # LW is injected via always-on path, not in REQUIRED_PROMPTS
        self.assertNotIn(
            constants.PROMPT_TYPE_LIVING_WORLD, StoryModeAgent.REQUIRED_PROMPTS
        )

    def test_story_mode_agent_optional_prompts(self):
        """StoryModeAgent has correct optional prompts."""
        expected_prompts = {
            constants.PROMPT_TYPE_NARRATIVE,
            constants.PROMPT_TYPE_MECHANICS,
            constants.PROMPT_TYPE_CHARACTER_TEMPLATE,
        }
        self.assertEqual(StoryModeAgent.OPTIONAL_PROMPTS, frozenset(expected_prompts))

    def test_story_mode_agent_mode(self):
        """StoryModeAgent has correct mode identifier."""
        self.assertEqual(StoryModeAgent.MODE, constants.MODE_CHARACTER)

    def test_story_mode_matches_regular_input(self):
        """StoryModeAgent matches regular story inputs."""
        test_inputs = [
            "I attack the goblin!",
            "Let me think about this",
            "Search the room for traps",
            "god",  # Not "GOD MODE:" - should match story mode
            "Tell me about god mode",
            "What is god?",
        ]
        for user_input in test_inputs:
            self.assertTrue(
                StoryModeAgent.matches_input(user_input),
                f"StoryModeAgent should match: {user_input}",
            )

    def test_story_mode_does_not_match_god_mode_input(self):
        """StoryModeAgent does not match god mode inputs."""
        test_inputs = [
            "GOD MODE: Set my HP to 50",
            "god mode: heal me",
            "  GOD MODE: fix my stats",
            "GOD MODE:",
        ]
        for user_input in test_inputs:
            self.assertFalse(
                StoryModeAgent.matches_input(user_input),
                f"StoryModeAgent should NOT match: {user_input}",
            )

    def test_story_mode_agent_has_prompt_builder(self):
        """StoryModeAgent provides access to its PromptBuilder."""
        agent = StoryModeAgent()
        self.assertIsInstance(agent.prompt_builder, PromptBuilder)

    def test_story_mode_agent_get_all_prompts(self):
        """StoryModeAgent.get_all_prompts returns union of required and optional."""
        agent = StoryModeAgent()
        all_prompts = agent.get_all_prompts()
        self.assertEqual(
            all_prompts,
            StoryModeAgent.REQUIRED_PROMPTS | StoryModeAgent.OPTIONAL_PROMPTS,
        )

    def test_story_mode_agent_repr(self):
        """StoryModeAgent has informative repr."""
        agent = StoryModeAgent()
        repr_str = repr(agent)
        self.assertIn("StoryModeAgent", repr_str)
        self.assertIn("mode=", repr_str)


class TestGodModeAgent(unittest.TestCase):
    """Test cases for GodModeAgent class."""

    def test_god_mode_agent_creation(self):
        """GodModeAgent can be instantiated."""
        agent = GodModeAgent()
        self.assertIsInstance(agent, BaseAgent)
        self.assertIsInstance(agent, GodModeAgent)

    def test_god_mode_agent_with_game_state(self):
        """GodModeAgent accepts game_state parameter."""
        mock_game_state = create_mock_game_state()
        agent = GodModeAgent(game_state=mock_game_state)
        self.assertEqual(agent.game_state, mock_game_state)

    def test_god_mode_agent_required_prompts(self):
        """GodModeAgent has correct required prompts (faction details in god_mode_instruction.md)."""
        expected_prompts = {
            constants.PROMPT_TYPE_MASTER_DIRECTIVE,
            constants.PROMPT_TYPE_GOD_MODE,
            constants.PROMPT_TYPE_GAME_STATE,
            constants.PROMPT_TYPE_PLANNING_PROTOCOL,  # Canonical planning block schema
            constants.PROMPT_TYPE_DND_SRD,
            constants.PROMPT_TYPE_MECHANICS,
        }
        self.assertEqual(GodModeAgent.REQUIRED_PROMPTS, frozenset(expected_prompts))

    def test_god_mode_agent_optional_prompts(self):
        """GodModeAgent has faction prompts as optional (load when needed)."""
        expected_optional = {
            constants.PROMPT_TYPE_FACTION_MANAGEMENT,  # When armies present
            constants.PROMPT_TYPE_FACTION_MINIGAME,  # When faction_minigame.enabled
        }
        self.assertEqual(GodModeAgent.OPTIONAL_PROMPTS, frozenset(expected_optional))

    def test_god_mode_agent_mode(self):
        """GodModeAgent has correct mode identifier."""
        self.assertEqual(GodModeAgent.MODE, constants.MODE_GOD)

    def test_god_mode_matches_god_mode_input(self):
        """GodModeAgent matches god mode inputs."""
        test_inputs = [
            "GOD MODE: Set my HP to 50",
            "god mode: heal me",
            "  GOD MODE: fix my stats",
            "GOD MODE:",
            "GOD MODE: anything",
        ]
        for user_input in test_inputs:
            self.assertTrue(
                GodModeAgent.matches_input(user_input),
                f"GodModeAgent should match: {user_input}",
            )

    def test_god_mode_does_not_match_regular_input(self):
        """GodModeAgent does not match regular story inputs."""
        test_inputs = [
            "I attack the goblin!",
            "Let me think about this",
            "god",  # Not "GOD MODE:"
            "Tell me about god mode",
            "god mode but not at start",
            "This is not GOD MODE: command",
        ]
        for user_input in test_inputs:
            self.assertFalse(
                GodModeAgent.matches_input(user_input),
                f"GodModeAgent should NOT match: {user_input}",
            )

    def test_god_mode_agent_has_prompt_builder(self):
        """GodModeAgent provides access to its PromptBuilder."""
        agent = GodModeAgent()
        self.assertIsInstance(agent.prompt_builder, PromptBuilder)

    def test_god_mode_agent_preprocess_input(self):
        """GodModeAgent.preprocess_input inserts warning AFTER GOD MODE prefix."""
        agent = GodModeAgent()
        test_input = "GOD MODE: Set HP to 50"
        processed = agent.preprocess_input(test_input)

        # CRITICAL: Must preserve "GOD MODE:" at the start for system instruction pattern matching
        self.assertTrue(
            processed.startswith("GOD MODE:"),
            f"Expected 'GOD MODE:' prefix preserved at start, got: {processed[:50]}...",
        )
        warning = constants.GOD_MODE_WARNING_PREFIX.strip()
        warning_index = processed.find(warning)
        command_index = processed.find("Set HP to 50")
        prefix_index = processed.find("GOD MODE:")

        # Warning must be present and appear after the prefix, before the command
        self.assertNotEqual(warning_index, -1, "Expected warning in processed input")
        self.assertNotEqual(command_index, -1, "Expected command in processed input")
        self.assertEqual(prefix_index, 0, "Expected 'GOD MODE:' at column 0")
        self.assertLess(prefix_index, warning_index)
        self.assertLess(warning_index, command_index)

    def test_god_mode_agent_preprocess_input_without_prefix(self):
        """GodModeAgent.preprocess_input prepends warning when no GOD MODE prefix."""
        agent = GodModeAgent()
        # Input without prefix (triggered via mode=god parameter)
        test_input = "Increase Theron's HP by 10"
        processed = agent.preprocess_input(test_input)

        # When no prefix, warning should be prepended
        self.assertTrue(processed.startswith(constants.GOD_MODE_WARNING_PREFIX))
        # Should preserve original input
        self.assertIn("Increase Theron's HP by 10", processed)
        # Full expected format (prepend when no GOD MODE: prefix)
        expected = constants.GOD_MODE_WARNING_PREFIX + test_input
        self.assertEqual(processed, expected)

    def test_god_mode_agent_preprocess_input_strips_leading_whitespace(self):
        """GodModeAgent.preprocess_input strips leading whitespace before GOD MODE prefix."""
        agent = GodModeAgent()
        test_input = "   GOD MODE: Set HP to 50"
        processed = agent.preprocess_input(test_input)

        # Must start with GOD MODE: at column 0 for instruction matching
        self.assertTrue(
            processed.startswith("GOD MODE:"),
            f"Expected 'GOD MODE:' at start, got: {processed[:50]}...",
        )
        warning = constants.GOD_MODE_WARNING_PREFIX.strip()
        warning_index = processed.find(warning)
        command_index = processed.find("Set HP to 50")
        prefix_index = processed.find("GOD MODE:")

        # Warning must be present and appear after the prefix, before the command
        self.assertNotEqual(warning_index, -1, "Expected warning in processed input")
        self.assertNotEqual(command_index, -1, "Expected command in processed input")
        self.assertEqual(prefix_index, 0, "Expected 'GOD MODE:' at column 0")
        self.assertLess(prefix_index, warning_index)
        self.assertLess(warning_index, command_index)

    def test_god_mode_agent_repr(self):
        """GodModeAgent has informative repr."""
        agent = GodModeAgent()
        repr_str = repr(agent)
        self.assertIn("GodModeAgent", repr_str)
        self.assertIn("mode=", repr_str)

    def test_god_mode_agent_prompt_order_no_faction_systems(self):
        """GodModeAgent.prompt_order returns only required prompts when no faction systems active."""
        mock_game_state = {"custom_campaign_state": {}, "army_data": {}}
        agent = GodModeAgent(game_state=mock_game_state)
        order = agent.prompt_order()

        # Should only have required prompts
        self.assertEqual(order, GodModeAgent.REQUIRED_PROMPT_ORDER)
        self.assertNotIn(constants.PROMPT_TYPE_FACTION_MANAGEMENT, order)
        self.assertNotIn(constants.PROMPT_TYPE_FACTION_MINIGAME, order)

    def test_god_mode_agent_prompt_order_with_armies(self):
        """GodModeAgent.prompt_order includes FACTION_MANAGEMENT when armies present."""
        mock_game_state = {
            "custom_campaign_state": {},
            "army_data": {"total_strength": 100},  # >= 20 triggers faction management
        }
        agent = GodModeAgent(game_state=mock_game_state)
        order = agent.prompt_order()

        # Should include faction management
        self.assertIn(constants.PROMPT_TYPE_FACTION_MANAGEMENT, order)
        self.assertNotIn(constants.PROMPT_TYPE_FACTION_MINIGAME, order)
        # Faction management should come after required prompts
        self.assertTrue(
            order.index(constants.PROMPT_TYPE_FACTION_MANAGEMENT)
            >= len(GodModeAgent.REQUIRED_PROMPT_ORDER)
        )

    def test_god_mode_agent_prompt_order_with_faction_minigame(self):
        """GodModeAgent.prompt_order includes FACTION_MINIGAME when enabled."""
        mock_game_state = {
            "custom_campaign_state": {"faction_minigame": {"enabled": True}},
            "army_data": {},
        }
        agent = GodModeAgent(game_state=mock_game_state)
        order = agent.prompt_order()

        # Should include faction minigame
        self.assertIn(constants.PROMPT_TYPE_FACTION_MINIGAME, order)
        self.assertNotIn(constants.PROMPT_TYPE_FACTION_MANAGEMENT, order)
        # Faction minigame should come after required prompts
        self.assertTrue(
            order.index(constants.PROMPT_TYPE_FACTION_MINIGAME)
            >= len(GodModeAgent.REQUIRED_PROMPT_ORDER)
        )

    def test_god_mode_agent_prompt_order_with_both_faction_systems(self):
        """GodModeAgent.prompt_order includes both faction prompts when both active."""
        mock_game_state = {
            "custom_campaign_state": {"faction_minigame": {"enabled": True}},
            "army_data": {"total_strength": 100},
        }
        agent = GodModeAgent(game_state=mock_game_state)
        order = agent.prompt_order()

        # Should include both faction prompts
        self.assertIn(constants.PROMPT_TYPE_FACTION_MANAGEMENT, order)
        self.assertIn(constants.PROMPT_TYPE_FACTION_MINIGAME, order)
        # Both should come after required prompts
        self.assertTrue(
            order.index(constants.PROMPT_TYPE_FACTION_MANAGEMENT)
            >= len(GodModeAgent.REQUIRED_PROMPT_ORDER)
        )
        self.assertTrue(
            order.index(constants.PROMPT_TYPE_FACTION_MINIGAME)
            >= len(GodModeAgent.REQUIRED_PROMPT_ORDER)
        )

    def test_god_mode_agent_prompt_order_below_army_threshold(self):
        """GodModeAgent.prompt_order excludes FACTION_MANAGEMENT when army below threshold."""
        mock_game_state = {
            "custom_campaign_state": {},
            "army_data": {"total_strength": 15},  # < 20, should not load
        }
        agent = GodModeAgent(game_state=mock_game_state)
        order = agent.prompt_order()

        # Should not include faction management
        self.assertNotIn(constants.PROMPT_TYPE_FACTION_MANAGEMENT, order)
        self.assertEqual(order, GodModeAgent.REQUIRED_PROMPT_ORDER)

    def test_god_mode_agent_prompt_order_handles_string_total_strength(self):
        """GodModeAgent.prompt_order safely converts string total_strength to int."""
        mock_game_state = {
            "custom_campaign_state": {},
            "army_data": {"total_strength": "100"},  # String that converts to >= 20
        }
        agent = GodModeAgent(game_state=mock_game_state)
        order = agent.prompt_order()

        # Should include faction management (string "100" converts to int 100)
        self.assertIn(constants.PROMPT_TYPE_FACTION_MANAGEMENT, order)

    def test_god_mode_agent_prompt_order_handles_none_total_strength(self):
        """GodModeAgent.prompt_order treats None total_strength as 0."""
        mock_game_state = {
            "custom_campaign_state": {},
            "army_data": {"total_strength": None},  # None should default to 0
        }
        agent = GodModeAgent(game_state=mock_game_state)
        order = agent.prompt_order()

        # Should not include faction management (None converts to 0)
        self.assertNotIn(constants.PROMPT_TYPE_FACTION_MANAGEMENT, order)

    def test_god_mode_agent_prompt_order_handles_invalid_total_strength(self):
        """GodModeAgent.prompt_order treats invalid total_strength as 0."""
        mock_game_state = {
            "custom_campaign_state": {},
            "army_data": {"total_strength": "invalid"},  # Can't convert to int
        }
        agent = GodModeAgent(game_state=mock_game_state)
        order = agent.prompt_order()

        # Should not include faction management (invalid converts to 0)
        self.assertNotIn(constants.PROMPT_TYPE_FACTION_MANAGEMENT, order)

    def test_god_mode_agent_includes_divine_prompts_when_divine_tier(self):
        """GodModeAgent includes divine_system prompt when campaign_tier is divine."""
        mock_game_state = {
            "custom_campaign_state": {"campaign_tier": "divine"},
            "army_data": {},
        }
        agent = GodModeAgent(game_state=mock_game_state)

        # Build system instructions to trigger finalize_instructions
        instructions = agent.build_system_instructions()

        # Should include divine leverage system file marker
        self.assertIn("divine_leverage_system.md", instructions)

    def test_god_mode_agent_includes_sovereign_prompts_when_sovereign_tier(self):
        """GodModeAgent includes sovereign_system prompt when campaign_tier is sovereign."""
        mock_game_state = {
            "custom_campaign_state": {"campaign_tier": "sovereign"},
            "army_data": {},
        }
        agent = GodModeAgent(game_state=mock_game_state)

        # Build system instructions to trigger finalize_instructions
        instructions = agent.build_system_instructions()

        # Should include sovereign system file marker
        self.assertIn("sovereign_system.md", instructions)

    def test_god_mode_agent_excludes_tier_prompts_when_mortal(self):
        """GodModeAgent does NOT include divine/sovereign prompts when campaign_tier is mortal."""
        mock_game_state = {
            "custom_campaign_state": {"campaign_tier": "mortal"},
            "army_data": {},
        }
        agent = GodModeAgent(game_state=mock_game_state)

        # Build system instructions to trigger finalize_instructions
        instructions = agent.build_system_instructions()

        # Should NOT include divine or sovereign system files
        self.assertNotIn("divine_leverage_system.md", instructions)
        self.assertNotIn("sovereign_system.md", instructions)

    def test_god_mode_agent_excludes_tier_prompts_when_no_campaign_tier(self):
        """GodModeAgent does NOT include divine/sovereign prompts when no campaign_tier set."""
        mock_game_state = {"custom_campaign_state": {}, "army_data": {}}
        agent = GodModeAgent(game_state=mock_game_state)

        # Build system instructions to trigger finalize_instructions
        instructions = agent.build_system_instructions()

        # Should NOT include divine or sovereign system files
        self.assertNotIn("divine_leverage_system.md", instructions)
        self.assertNotIn("sovereign_system.md", instructions)


class TestCombatAgent(unittest.TestCase):
    """Test cases for CombatAgent class."""

    def test_combat_agent_creation(self):
        """CombatAgent can be instantiated."""
        agent = CombatAgent()
        self.assertIsInstance(agent, BaseAgent)
        self.assertIsInstance(agent, CombatAgent)

    def test_combat_agent_with_game_state(self):
        """CombatAgent accepts game_state parameter."""
        mock_game_state = create_mock_game_state(in_combat=True)
        agent = CombatAgent(game_state=mock_game_state)
        self.assertEqual(agent.game_state, mock_game_state)

    def test_combat_agent_required_prompts(self):
        """CombatAgent has correct required prompts."""
        expected_prompts = {
            constants.PROMPT_TYPE_MASTER_DIRECTIVE,
            constants.PROMPT_TYPE_COMBAT,
            constants.PROMPT_TYPE_GAME_STATE,
            constants.PROMPT_TYPE_PLANNING_PROTOCOL,  # Canonical planning block schema
            constants.PROMPT_TYPE_NARRATIVE,
            constants.PROMPT_TYPE_DND_SRD,
            constants.PROMPT_TYPE_MECHANICS,
            constants.PROMPT_TYPE_LIVING_WORLD,  # Auto-include for time-advancing agents
        }
        self.assertEqual(CombatAgent.REQUIRED_PROMPTS, frozenset(expected_prompts))

    def test_combat_agent_includes_living_world(self):
        """CombatAgent must include PROMPT_TYPE_LIVING_WORLD for background events.

        For CombatAgent, this is currently enforced by explicit prompt ordering.
        """
        self.assertIn(
            constants.PROMPT_TYPE_LIVING_WORLD,
            CombatAgent.REQUIRED_PROMPTS,
            "CombatAgent missing PROMPT_TYPE_LIVING_WORLD in REQUIRED_PROMPTS.",
        )

    def test_combat_agent_optional_prompts(self):
        """CombatAgent has no optional prompts (focused combat mode)."""
        self.assertEqual(CombatAgent.OPTIONAL_PROMPTS, frozenset())

    def test_combat_agent_mode(self):
        """CombatAgent has correct mode identifier."""
        self.assertEqual(CombatAgent.MODE, constants.MODE_COMBAT)

    def test_combat_agent_matches_input_always_false(self):
        """CombatAgent.matches_input always returns False (uses game state instead)."""
        test_inputs = [
            "I attack the goblin!",
            "Roll for initiative",
            "combat start",
            "COMBAT MODE:",
        ]
        for user_input in test_inputs:
            self.assertFalse(
                CombatAgent.matches_input(user_input),
                f"CombatAgent.matches_input should always be False: {user_input}",
            )

    def test_combat_agent_matches_game_state_true_when_in_combat(self):
        """CombatAgent.matches_game_state returns True when in_combat is True."""
        mock_game_state = create_mock_game_state(in_combat=True)
        self.assertTrue(CombatAgent.matches_game_state(mock_game_state))

    def test_combat_agent_matches_game_state_false_when_not_in_combat(self):
        """CombatAgent.matches_game_state returns False when in_combat is False."""
        mock_game_state = create_mock_game_state(in_combat=False)
        self.assertFalse(CombatAgent.matches_game_state(mock_game_state))

    def test_combat_agent_matches_game_state_false_when_none(self):
        """CombatAgent.matches_game_state returns False when game_state is None."""
        self.assertFalse(CombatAgent.matches_game_state(None))

    def test_combat_agent_matches_game_state_false_when_combat_state_missing(self):
        """CombatAgent.matches_game_state returns False when combat_state missing."""
        mock_game_state = Mock(spec=[])  # Empty spec - no attributes
        # Can't use create_mock_game_state because we need spec=[] to fail attribute access
        # But our new code calls is_in_combat() method, so spec=[] mock fails that call
        # We need a mock that HAS is_in_combat but returns something that indicates missing state?
        # Actually, if is_in_combat() exists, it handles missing state internally.
        # The test intends to check what happens if game_state object is malformed?
        # With new interface, we expect game_state to have is_in_combat().
        # If it doesn't, it raises AttributeError, which is acceptable for invalid objects.
        # So we'll skip this test or update it to verify is_in_combat is called.

        # Updated test: Verify matches_game_state relies on is_in_combat
        mock_game_state = Mock()
        # If is_in_combat raises error (simulating missing method), matches_game_state propagates it
        del mock_game_state.is_in_combat
        with self.assertRaises(AttributeError):
            CombatAgent.matches_game_state(mock_game_state)

    def test_combat_agent_matches_game_state_false_when_combat_state_not_dict(self):
        """CombatAgent.matches_game_state returns False when combat_state not dict."""
        # With new implementation, is_in_combat() handles the check.
        # We mock is_in_combat to return False (simulating internal check failure)
        mock_game_state = create_mock_game_state(
            in_combat=False, combat_state_dict=None
        )
        self.assertFalse(CombatAgent.matches_game_state(mock_game_state))


class TestRewardsAgent(unittest.TestCase):
    """Test cases for RewardsAgent class."""

    def test_rewards_agent_creation(self):
        """RewardsAgent can be instantiated."""
        agent = RewardsAgent()
        self.assertIsInstance(agent, BaseAgent)
        self.assertIsInstance(agent, RewardsAgent)

    def test_rewards_agent_required_prompts(self):
        """RewardsAgent has correct required prompts."""
        expected_prompts = {
            constants.PROMPT_TYPE_MASTER_DIRECTIVE,
            constants.PROMPT_TYPE_REWARDS,
            constants.PROMPT_TYPE_GAME_STATE,
            constants.PROMPT_TYPE_PLANNING_PROTOCOL,  # Canonical planning block schema
            constants.PROMPT_TYPE_DND_SRD,
            constants.PROMPT_TYPE_MECHANICS,
        }
        self.assertEqual(RewardsAgent.REQUIRED_PROMPTS, frozenset(expected_prompts))
        self.assertEqual(RewardsAgent.OPTIONAL_PROMPTS, frozenset())
        self.assertEqual(RewardsAgent.MODE, constants.MODE_REWARDS)

    def test_rewards_agent_matches_input_always_false(self):
        """RewardsAgent.matches_input always returns False (state-driven)."""
        self.assertFalse(RewardsAgent.matches_input("any input"))

    def test_rewards_agent_matches_game_state_combat_end(self):
        """RewardsAgent triggers when combat ended with summary and not processed."""
        combat_state = {
            "in_combat": False,
            "combat_phase": "ended",
            "combat_summary": {"result": "victory"},
            "rewards_processed": False,
        }
        mock_state = create_rewards_game_state(combat_state=combat_state)

        self.assertTrue(RewardsAgent.matches_game_state(mock_state))

    def test_rewards_agent_matches_game_state_combat_finished_variants(self):
        """RewardsAgent handles alternate finished combat phases."""
        combat_state = {
            "in_combat": False,
            "combat_phase": "finished",
            "combat_summary": {"result": "victory"},
            "rewards_processed": False,
        }
        mock_state = create_rewards_game_state(combat_state=combat_state)

        self.assertTrue(RewardsAgent.matches_game_state(mock_state))

        combat_state["combat_phase"] = "victory"
        self.assertTrue(RewardsAgent.matches_game_state(mock_state))

    def test_rewards_agent_matches_game_state_combat_phase_not_finished(self):
        """RewardsAgent ignores combat states that are not finished."""
        combat_state = {
            "in_combat": False,
            "combat_phase": "in_progress",
            "combat_summary": {"result": "pending"},
            "rewards_processed": False,
        }
        mock_state = create_rewards_game_state(combat_state=combat_state)

        self.assertFalse(RewardsAgent.matches_game_state(mock_state))

    def test_rewards_agent_matches_game_state_encounter_completed(self):
        """RewardsAgent triggers when encounter is completed and not processed."""
        encounter_state = {
            "encounter_completed": True,
            "rewards_processed": False,
            "encounter_summary": {"result": "success", "xp_awarded": 120},
        }
        mock_state = create_rewards_game_state(encounter_state=encounter_state)

        self.assertTrue(RewardsAgent.matches_game_state(mock_state))

    def test_rewards_agent_matches_game_state_encounter_missing_summary(self):
        """RewardsAgent does not trigger when encounter summary is missing."""
        encounter_state = {
            "encounter_completed": True,
            "rewards_processed": False,
            # Missing encounter_summary should prevent rewards processing
        }
        mock_state = create_rewards_game_state(encounter_state=encounter_state)

        self.assertFalse(RewardsAgent.matches_game_state(mock_state))

    def test_rewards_agent_matches_game_state_encounter_missing_xp(self):
        """RewardsAgent does not trigger when encounter_summary lacks xp_awarded."""
        encounter_state = {
            "encounter_completed": True,
            "rewards_processed": False,
            "encounter_summary": {"result": "success"},
        }
        mock_state = create_rewards_game_state(encounter_state=encounter_state)

        self.assertFalse(RewardsAgent.matches_game_state(mock_state))

    def test_rewards_agent_matches_game_state_rewards_pending(self):
        """RewardsAgent triggers when rewards_pending exists and not processed."""
        rewards_pending = {"source": "quest", "xp": 100, "processed": False}
        mock_state = create_rewards_game_state(rewards_pending=rewards_pending)

        self.assertTrue(RewardsAgent.matches_game_state(mock_state))

    def test_rewards_agent_matches_game_state_returns_false_when_processed(self):
        """RewardsAgent does not trigger when rewards are already processed."""
        rewards_pending = {"source": "quest", "xp": 50, "processed": True}
        mock_state = create_rewards_game_state(rewards_pending=rewards_pending)

        self.assertFalse(RewardsAgent.matches_game_state(mock_state))

    def test_rewards_agent_matches_game_state_returns_false_for_none(self):
        """RewardsAgent returns False when game_state is None."""
        self.assertFalse(RewardsAgent.matches_game_state(None))

    @patch("mvp_site.agent_prompts._load_instruction_file")
    def test_rewards_agent_builds_instructions(self, mock_load):
        """RewardsAgent.build_system_instructions returns instruction string."""
        mock_load.return_value = "Test instruction content"

        agent = RewardsAgent()
        instructions = agent.build_system_instructions()

        self.assertIsInstance(instructions, str)
        self.assertGreater(len(instructions), 0)


class TestDeferredRewardsAgent(unittest.TestCase):
    """Test cases for DeferredRewardsAgent class."""

    def test_deferred_rewards_agent_creation(self):
        """DeferredRewardsAgent can be instantiated and subclasses RewardsAgent."""

        agent = DeferredRewardsAgent()

        self.assertIsInstance(agent, RewardsAgent)
        self.assertIsInstance(agent, BaseAgent)

    def test_deferred_rewards_required_prompts(self):
        """DeferredRewardsAgent includes deferred rewards prompt in required set."""

        expected_prompts = {
            constants.PROMPT_TYPE_MASTER_DIRECTIVE,
            constants.PROMPT_TYPE_GAME_STATE,
            constants.PROMPT_TYPE_PLANNING_PROTOCOL,
            constants.PROMPT_TYPE_DEFERRED_REWARDS,
            constants.PROMPT_TYPE_REWARDS,
            constants.PROMPT_TYPE_DND_SRD,
            constants.PROMPT_TYPE_MECHANICS,
        }

        self.assertEqual(
            DeferredRewardsAgent.REQUIRED_PROMPTS, frozenset(expected_prompts)
        )
        self.assertEqual(DeferredRewardsAgent.MODE, constants.MODE_REWARDS)

    @patch.object(PromptBuilder, "should_include_deferred_rewards")
    def test_should_run_deferred_check_delegates(self, mock_should_include):
        """should_run_deferred_check delegates interval logic to PromptBuilder."""

        mock_should_include.return_value = True

        self.assertTrue(DeferredRewardsAgent.should_run_deferred_check(10))
        mock_should_include.assert_called_once_with(10)

    @patch.object(PromptBuilder, "finalize_instructions")
    @patch.object(PromptBuilder, "build_from_order")
    def test_build_system_instructions_forces_deferred_prompt(
        self,
        mock_build_from_order,
        mock_finalize,
    ):
        """DeferredRewardsAgent always includes deferred instruction via build_from_order."""

        mock_build_from_order.return_value = ["BASE", "DEFERRED"]
        mock_finalize.return_value = "FINAL"

        agent = DeferredRewardsAgent()
        result = agent.build_system_instructions(turn_number=5)

        self.assertEqual(result, "FINAL")
        mock_build_from_order.assert_called_once_with(
            agent.REQUIRED_PROMPT_ORDER,
            include_debug=True,
            turn_number=5,
            advances_time=agent.advances_time,
        )
        mock_finalize.assert_called_once_with(
            ["BASE", "DEFERRED"], use_default_world=False
        )

    @patch.object(PromptBuilder, "finalize_instructions")
    @patch.object(PromptBuilder, "build_from_order")
    def test_build_system_instructions_accepts_dice_roll_strategy(
        self,
        mock_build_from_order,
        mock_finalize,
    ):
        """DeferredRewardsAgent.build_system_instructions accepts dice_roll_strategy.

        This test ensures signature compatibility with parent class (FixedPromptAgent).
        llm_service.py passes dice_roll_strategy to all agents, so DeferredRewardsAgent
        must accept it even though it doesn't use dice instructions.
        """
        mock_build_from_order.return_value = ["BASE", "DEFERRED"]
        mock_finalize.return_value = "FINAL"

        agent = DeferredRewardsAgent()
        # This should NOT raise TypeError - bug fix for chi-square test failures
        result = agent.build_system_instructions(
            turn_number=5,
            dice_roll_strategy="code_execution",
        )

        self.assertEqual(result, "FINAL")
        # dice_roll_strategy is accepted but not passed to build_from_order
        # (deferred rewards doesn't need dice instructions)
        mock_build_from_order.assert_called_once_with(
            agent.REQUIRED_PROMPT_ORDER,
            include_debug=True,
            turn_number=5,
            advances_time=agent.advances_time,
        )


class TestCampaignUpgradeAgent(unittest.TestCase):
    """Test cases for CampaignUpgradeAgent class."""

    def create_campaign_upgrade_game_state(
        self,
        divine_upgrade_available=False,
        multiverse_upgrade_available=False,
        campaign_tier="mortal",
        divine_potential=0,
        universe_control=0,
        level=1,
    ):
        """Helper to create a mock GameState for campaign upgrade tests."""
        mock_state = Mock()
        mock_state.is_in_combat.return_value = False
        mock_state.get_combat_state.return_value = {"in_combat": False}
        mock_state.combat_state = {"in_combat": False}

        # Mock campaign upgrade availability
        mock_state.is_campaign_upgrade_available.return_value = (
            divine_upgrade_available or multiverse_upgrade_available
        )
        mock_state.is_divine_upgrade_available.return_value = divine_upgrade_available
        mock_state.is_multiverse_upgrade_available.return_value = (
            multiverse_upgrade_available
        )

        # Mock get_pending_upgrade_type
        if multiverse_upgrade_available:
            mock_state.get_pending_upgrade_type.return_value = "multiverse"
        elif divine_upgrade_available:
            mock_state.get_pending_upgrade_type.return_value = "divine"
        else:
            mock_state.get_pending_upgrade_type.return_value = None

        # Mock custom_campaign_state
        mock_state.custom_campaign_state = {
            "campaign_tier": campaign_tier,
            "divine_potential": divine_potential,
            "universe_control": universe_control,
            "character_creation_completed": True,
        }

        # Mock player_character_data
        mock_state.player_character_data = {
            "name": "Test Character",
            "class": "Fighter",
            "level": level,
        }

        return mock_state

    def test_campaign_upgrade_agent_creation(self):
        """CampaignUpgradeAgent can be instantiated."""
        agent = CampaignUpgradeAgent()
        self.assertIsInstance(agent, BaseAgent)
        self.assertIsInstance(agent, CampaignUpgradeAgent)

    def test_campaign_upgrade_agent_with_game_state(self):
        """CampaignUpgradeAgent accepts game_state parameter."""
        mock_game_state = self.create_campaign_upgrade_game_state(
            divine_upgrade_available=True
        )
        agent = CampaignUpgradeAgent(game_state=mock_game_state)
        self.assertEqual(agent.game_state, mock_game_state)
        self.assertEqual(agent._upgrade_type, "divine")

    def test_campaign_upgrade_agent_with_none_game_state(self):
        """CampaignUpgradeAgent handles None game_state correctly."""
        agent = CampaignUpgradeAgent(game_state=None)
        self.assertIsNone(agent.game_state)
        self.assertIsNone(agent._upgrade_type)

    def test_campaign_upgrade_agent_required_prompts(self):
        """CampaignUpgradeAgent has correct required prompts."""
        expected_prompts = {
            constants.PROMPT_TYPE_MASTER_DIRECTIVE,
            constants.PROMPT_TYPE_GAME_STATE,
            constants.PROMPT_TYPE_PLANNING_PROTOCOL,
            constants.PROMPT_TYPE_DND_SRD,
            constants.PROMPT_TYPE_MECHANICS,
            constants.PROMPT_TYPE_LIVING_WORLD,
        }
        self.assertEqual(
            CampaignUpgradeAgent.REQUIRED_PROMPTS, frozenset(expected_prompts)
        )

    def test_campaign_upgrade_agent_no_optional_prompts(self):
        """CampaignUpgradeAgent has no optional prompts (ceremony prompts are dynamic)."""
        self.assertEqual(CampaignUpgradeAgent.OPTIONAL_PROMPTS, frozenset())

    def test_campaign_upgrade_agent_mode(self):
        """CampaignUpgradeAgent has correct mode identifier."""
        self.assertEqual(CampaignUpgradeAgent.MODE, constants.MODE_CAMPAIGN_UPGRADE)

    def test_campaign_upgrade_agent_matches_input_always_false(self):
        """CampaignUpgradeAgent.matches_input always returns False (state-driven)."""
        test_inputs = [
            "I want to upgrade",
            "ascend to divinity",
            "become a god",
            "multiverse upgrade",
        ]
        for user_input in test_inputs:
            self.assertFalse(
                CampaignUpgradeAgent.matches_input(user_input),
                f"CampaignUpgradeAgent.matches_input should always be False: {user_input}",
            )

    def test_campaign_upgrade_agent_matches_game_state_true_when_divine_available(self):
        """CampaignUpgradeAgent.matches_game_state returns True when divine upgrade available."""
        mock_game_state = self.create_campaign_upgrade_game_state(
            divine_upgrade_available=True
        )
        self.assertTrue(CampaignUpgradeAgent.matches_game_state(mock_game_state))

    def test_campaign_upgrade_agent_matches_game_state_true_when_multiverse_available(
        self,
    ):
        """CampaignUpgradeAgent.matches_game_state returns True when multiverse upgrade available."""
        mock_game_state = self.create_campaign_upgrade_game_state(
            multiverse_upgrade_available=True
        )
        self.assertTrue(CampaignUpgradeAgent.matches_game_state(mock_game_state))

    def test_campaign_upgrade_agent_matches_game_state_false_when_no_upgrade(self):
        """CampaignUpgradeAgent.matches_game_state returns False when no upgrade available."""
        mock_game_state = self.create_campaign_upgrade_game_state(
            divine_upgrade_available=False,
            multiverse_upgrade_available=False,
        )
        self.assertFalse(CampaignUpgradeAgent.matches_game_state(mock_game_state))

    def test_campaign_upgrade_agent_matches_game_state_false_when_none(self):
        """CampaignUpgradeAgent.matches_game_state returns False when game_state is None."""
        self.assertFalse(CampaignUpgradeAgent.matches_game_state(None))

    def test_campaign_upgrade_agent_captures_divine_upgrade_type(self):
        """CampaignUpgradeAgent captures divine upgrade type in __init__."""
        mock_game_state = self.create_campaign_upgrade_game_state(
            divine_upgrade_available=True
        )
        agent = CampaignUpgradeAgent(game_state=mock_game_state)
        self.assertEqual(agent._upgrade_type, "divine")

    def test_campaign_upgrade_agent_captures_multiverse_upgrade_type(self):
        """CampaignUpgradeAgent captures multiverse upgrade type in __init__."""
        mock_game_state = self.create_campaign_upgrade_game_state(
            multiverse_upgrade_available=True
        )
        agent = CampaignUpgradeAgent(game_state=mock_game_state)
        self.assertEqual(agent._upgrade_type, "multiverse")

    def test_campaign_upgrade_agent_captures_none_when_no_upgrade(self):
        """CampaignUpgradeAgent captures None upgrade type when no upgrade available."""
        mock_game_state = self.create_campaign_upgrade_game_state(
            divine_upgrade_available=False,
            multiverse_upgrade_available=False,
        )
        agent = CampaignUpgradeAgent(game_state=mock_game_state)
        self.assertIsNone(agent._upgrade_type)

    def test_campaign_upgrade_agent_multiverse_priority_over_divine(self):
        """CampaignUpgradeAgent prioritizes multiverse over divine upgrade."""
        mock_game_state = self.create_campaign_upgrade_game_state(
            divine_upgrade_available=True,
            multiverse_upgrade_available=True,
        )
        agent = CampaignUpgradeAgent(game_state=mock_game_state)
        # Multiverse should take priority
        self.assertEqual(agent._upgrade_type, "multiverse")

    @patch("mvp_site.agents._load_instruction_file")
    @patch("mvp_site.agents.PromptBuilder")
    def test_campaign_upgrade_agent_builds_instructions_divine(
        self, mock_builder_class, mock_load
    ):
        """CampaignUpgradeAgent.build_system_instructions includes divine ascension prompt."""
        mock_load.return_value = "Test instruction content"
        mock_builder = Mock()
        mock_builder_class.return_value = mock_builder
        mock_builder.build_from_order.return_value = ["core1", "core2"]
        mock_builder.finalize_instructions.return_value = "finalized instructions"

        mock_game_state = self.create_campaign_upgrade_game_state(
            divine_upgrade_available=True
        )
        agent = CampaignUpgradeAgent(game_state=mock_game_state)
        instructions = agent.build_system_instructions()

        self.assertIsInstance(instructions, str)
        # Verify build_from_order was called with REQUIRED_PROMPT_ORDER
        mock_builder.build_from_order.assert_called_once_with(
            CampaignUpgradeAgent.REQUIRED_PROMPT_ORDER,
            include_debug=True,
            dice_roll_strategy=None,
            turn_number=0,
            advances_time=agent.advances_time,
        )
        # Verify divine ascension prompt was loaded
        mock_load.assert_any_call(constants.PROMPT_TYPE_DIVINE_ASCENSION)

    @patch("mvp_site.agents._load_instruction_file")
    @patch("mvp_site.agents.PromptBuilder")
    def test_campaign_upgrade_agent_builds_instructions_multiverse(
        self, mock_builder_class, mock_load
    ):
        """CampaignUpgradeAgent.build_system_instructions includes sovereign ascension prompt."""
        mock_load.return_value = "Test instruction content"
        mock_builder = Mock()
        mock_builder_class.return_value = mock_builder
        mock_builder.build_from_order.return_value = ["core1", "core2"]
        mock_builder.finalize_instructions.return_value = "finalized instructions"

        mock_game_state = self.create_campaign_upgrade_game_state(
            multiverse_upgrade_available=True
        )
        agent = CampaignUpgradeAgent(game_state=mock_game_state)
        instructions = agent.build_system_instructions()

        self.assertIsInstance(instructions, str)
        # Verify build_from_order was called with REQUIRED_PROMPT_ORDER
        mock_builder.build_from_order.assert_called_once_with(
            CampaignUpgradeAgent.REQUIRED_PROMPT_ORDER,
            include_debug=True,
            dice_roll_strategy=None,
            turn_number=0,
            advances_time=agent.advances_time,
        )
        # Verify sovereign ascension prompt was loaded
        mock_load.assert_any_call(constants.PROMPT_TYPE_SOVEREIGN_ASCENSION)

    @patch("mvp_site.agents._load_instruction_file")
    @patch("mvp_site.agents.PromptBuilder")
    def test_campaign_upgrade_agent_builds_instructions_no_upgrade_type(
        self, mock_builder_class, mock_load
    ):
        """CampaignUpgradeAgent.build_system_instructions handles None upgrade type gracefully."""
        mock_load.return_value = "Test instruction content"
        mock_builder = Mock()
        mock_builder_class.return_value = mock_builder
        mock_builder.build_from_order.return_value = ["core1", "core2"]
        mock_builder.finalize_instructions.return_value = "finalized instructions"

        # Create agent with no upgrade available
        mock_game_state = self.create_campaign_upgrade_game_state(
            divine_upgrade_available=False,
            multiverse_upgrade_available=False,
        )
        agent = CampaignUpgradeAgent(game_state=mock_game_state)
        instructions = agent.build_system_instructions()

        self.assertIsInstance(instructions, str)
        # Should still build core instructions
        mock_builder.build_from_order.assert_called_once_with(
            CampaignUpgradeAgent.REQUIRED_PROMPT_ORDER,
            include_debug=True,
            dice_roll_strategy=None,
            turn_number=0,
            advances_time=agent.advances_time,
        )
        # Should not load any ascension prompt (only core instructions)
        # Note: build_from_order may call _load_instruction_file internally, so we check
        # that divine/sovereign ascension prompts were NOT called
        divine_calls = [
            call
            for call in mock_load.call_args_list
            if len(call[0]) > 0 and call[0][0] == constants.PROMPT_TYPE_DIVINE_ASCENSION
        ]
        sovereign_calls = [
            call
            for call in mock_load.call_args_list
            if len(call[0]) > 0
            and call[0][0] == constants.PROMPT_TYPE_SOVEREIGN_ASCENSION
        ]
        self.assertEqual(
            len(divine_calls),
            0,
            "Should not load divine ascension prompt when no upgrade",
        )
        self.assertEqual(
            len(sovereign_calls),
            0,
            "Should not load sovereign ascension prompt when no upgrade",
        )

    def test_campaign_upgrade_agent_has_prompt_builder(self):
        """CampaignUpgradeAgent provides access to its PromptBuilder."""
        agent = CampaignUpgradeAgent()

        self.assertIsInstance(agent.prompt_builder, PromptBuilder)

    def test_campaign_upgrade_agent_get_all_prompts(self):
        """CampaignUpgradeAgent.get_all_prompts returns required prompts only."""
        agent = CampaignUpgradeAgent()
        all_prompts = agent.get_all_prompts()
        self.assertEqual(
            all_prompts,
            CampaignUpgradeAgent.REQUIRED_PROMPTS
            | CampaignUpgradeAgent.OPTIONAL_PROMPTS,
        )
        # OPTIONAL_PROMPTS is empty, so should equal REQUIRED_PROMPTS
        self.assertEqual(all_prompts, CampaignUpgradeAgent.REQUIRED_PROMPTS)

    def test_campaign_upgrade_agent_repr(self):
        """CampaignUpgradeAgent has informative repr."""
        agent = CampaignUpgradeAgent()
        repr_str = repr(agent)
        self.assertIn("CampaignUpgradeAgent", repr_str)
        self.assertIn("mode=", repr_str)


class TestCharacterCreationAgent(unittest.TestCase):
    """Test cases for CharacterCreationAgent class."""

    def test_character_creation_agent_creation(self):
        """CharacterCreationAgent can be instantiated."""
        agent = CharacterCreationAgent()
        self.assertIsInstance(agent, BaseAgent)
        self.assertIsInstance(agent, CharacterCreationAgent)

    def test_character_creation_agent_with_game_state(self):
        """CharacterCreationAgent accepts game_state parameter."""
        mock_game_state = create_character_creation_game_state()
        agent = CharacterCreationAgent(game_state=mock_game_state)
        self.assertEqual(agent.game_state, mock_game_state)

    def test_character_creation_agent_required_prompts(self):
        """CharacterCreationAgent has correct required prompts for creation and level-up."""
        expected_prompts = {
            constants.PROMPT_TYPE_MASTER_DIRECTIVE,
            # Canonical schema reference for equipment/spells/stats during creation.
            constants.PROMPT_TYPE_GAME_STATE,
            constants.PROMPT_TYPE_CHARACTER_CREATION,
            constants.PROMPT_TYPE_DND_SRD,
            constants.PROMPT_TYPE_MECHANICS,  # Full D&D rules for level-up
        }
        self.assertEqual(
            CharacterCreationAgent.REQUIRED_PROMPTS, frozenset(expected_prompts)
        )

    def test_character_creation_agent_no_optional_prompts(self):
        """CharacterCreationAgent has no optional prompts (minimal focused mode)."""
        self.assertEqual(CharacterCreationAgent.OPTIONAL_PROMPTS, frozenset())

    def test_character_creation_agent_mode(self):
        """CharacterCreationAgent has correct mode identifier."""
        self.assertEqual(CharacterCreationAgent.MODE, constants.MODE_CHARACTER_CREATION)

    def test_character_creation_matches_game_state_new_campaign(self):
        """CharacterCreationAgent matches when character has no name/class."""
        mock_state = create_character_creation_game_state(
            character_creation_completed=False,
            character_name="",
            character_class="",
        )
        self.assertTrue(CharacterCreationAgent.matches_game_state(mock_state))

    def test_character_creation_matches_game_state_no_stdout(self):
        """CharacterCreationAgent.matches_game_state should not write to stdout."""
        mock_state = create_character_creation_game_state(
            character_creation_completed=False,
            character_name="",
            character_class="",
        )

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            CharacterCreationAgent.matches_game_state(mock_state)

        self.assertEqual(buffer.getvalue(), "")

    def test_character_creation_matches_game_state_partial_character(self):
        """CharacterCreationAgent matches when character has name but no class."""
        mock_state = create_character_creation_game_state(
            character_creation_completed=False,
            character_name="Test Hero",
            character_class="",
        )
        self.assertTrue(CharacterCreationAgent.matches_game_state(mock_state))

    def test_character_creation_does_not_match_completed(self):
        """CharacterCreationAgent does not match when creation is completed."""
        mock_state = create_character_creation_game_state(
            character_creation_completed=True,
            character_name="Test Hero",
            character_class="Fighter",
        )
        self.assertFalse(CharacterCreationAgent.matches_game_state(mock_state))

    def test_character_creation_does_not_match_full_character(self):
        """CharacterCreationAgent does not match when character has name and class."""
        mock_state = create_character_creation_game_state(
            character_creation_completed=False,
            character_name="Test Hero",
            character_class="Wizard",
        )
        self.assertFalse(CharacterCreationAgent.matches_game_state(mock_state))

    def test_character_creation_does_not_match_none(self):
        """CharacterCreationAgent does not match when game_state is None."""
        self.assertFalse(CharacterCreationAgent.matches_game_state(None))

    def test_character_creation_matches_level_up_pending(self):
        """CharacterCreationAgent matches when level_up_pending is True and creation not completed."""
        mock_state = create_character_creation_game_state(
            character_creation_completed=False,  # Creation NOT done
            character_name="Test Hero",
            character_class="Fighter",
            level_up_pending=True,  # Level-up pending
            level=1,
            experience_current=300,  # L2 threshold reached
        )
        self.assertTrue(CharacterCreationAgent.matches_game_state(mock_state))

    def test_character_creation_ignores_stale_level_up_pending(self):
        """CharacterCreationAgent ignores level_up_pending when character_creation_completed=True."""
        mock_state = create_character_creation_game_state(
            character_creation_completed=True,  # Creation done
            character_name="Test Hero",
            character_class="Fighter",
            level_up_pending=True,  # Stale flag — should be ignored
        )
        self.assertFalse(CharacterCreationAgent.matches_game_state(mock_state))

    def test_character_creation_ignores_subthreshold_stale_level_up_pending(self):
        """Ignore level_up_pending when XP is below next-level threshold and no rewards signal."""
        mock_state = create_character_creation_game_state(
            character_creation_completed=False,
            character_name="Test Hero",
            character_class="Fighter",
            level_up_pending=True,
            level_up_available=False,
            level=7,
            experience_current=32300,  # Below L8 threshold (34,000)
        )
        self.assertFalse(CharacterCreationAgent.matches_game_state(mock_state))

    def test_level_up_agent_ignores_subthreshold_stale_level_up_pending(self):
        """LevelUpAgent should not activate from stale pending flag alone below threshold."""
        mock_state = create_character_creation_game_state(
            character_creation_completed=True,
            character_name="Test Hero",
            character_class="Fighter",
            level_up_pending=True,
            level_up_available=False,
            level=7,
            experience_current=32300,  # Below L8 threshold (34,000)
        )
        self.assertFalse(LevelUpAgent.matches_game_state(mock_state))

    def test_level_up_agent_accepts_pending_flag_at_threshold(self):
        """Pending level-up remains valid at threshold XP even without rewards_pending."""
        mock_state = create_character_creation_game_state(
            character_creation_completed=True,
            character_name="Test Hero",
            character_class="Fighter",
            level_up_pending=True,
            level_up_available=False,
            level=7,
            experience_current=34000,  # L8 threshold reached
        )
        self.assertTrue(LevelUpAgent.matches_game_state(mock_state))

    def test_character_creation_matches_rewards_level_up_available(self):
        """CharacterCreationAgent matches when rewards_pending level_up_available is True.

        REV-0g1y fix: Explicit False flags take precedence over stale rewards_pending data.
        To activate level-up modal when rewards_pending.level_up_available=True, we must
        NOT have explicit level_up_pending=False (which indicates a stale guard).
        """
        mock_state = create_character_creation_game_state(
            character_creation_completed=True,
            character_name="Test Hero",
            character_class="Fighter",
            level_up_available=True,
            level_up_pending=None,  # Not explicitly False, so no stale guard
        )
        self.assertTrue(CharacterCreationAgent.matches_game_state(mock_state))

    def test_character_creation_does_not_match_no_level_up(self):
        """CharacterCreationAgent does not match when creation done and no level-up."""
        mock_state = create_character_creation_game_state(
            character_creation_completed=True,
            character_name="Test Hero",
            character_class="Fighter",
            level_up_pending=False,
        )
        self.assertFalse(CharacterCreationAgent.matches_game_state(mock_state))

    def test_character_creation_matches_input_done_phrases(self):
        """CharacterCreationAgent.matches_input detects completion phrases."""
        done_phrases = [
            # Character creation completion
            "I'm done",
            "im done",
            "start the story",
            "begin the adventure",
            "let's play",
            "ready to play",
            "character complete",
            # Level-up completion
            "level-up complete",
            "done leveling",
            "back to adventure",
        ]
        for phrase in done_phrases:
            self.assertTrue(
                CharacterCreationAgent.matches_input(phrase),
                f"Should match done phrase: {phrase}",
            )

    def test_character_creation_ignores_negated_done_phrases(self):
        """Negated phrases should not exit character creation."""
        negated_inputs = [
            "I'm not done yet",
            "not ready to start the story",
            "don't start adventure",
            "I'm not finished",
        ]
        for phrase in negated_inputs:
            self.assertFalse(
                CharacterCreationAgent.matches_input(phrase),
                f"Should not match negated phrase: {phrase}",
            )

    def test_character_creation_does_not_match_regular_input(self):
        """CharacterCreationAgent.matches_input returns False for regular creation input."""
        regular_inputs = [
            "I want to be a wizard",
            "Make me a half-elf",
            "What classes are available?",
            "I choose high elf",
        ]
        for user_input in regular_inputs:
            self.assertFalse(
                CharacterCreationAgent.matches_input(user_input),
                f"Should NOT match regular input: {user_input}",
            )

    @patch("mvp_site.agent_prompts._load_instruction_file")
    def test_character_creation_agent_builds_instructions(self, mock_load):
        """CharacterCreationAgent.build_system_instructions returns minimal instruction string."""
        mock_load.return_value = "Test instruction content"

        agent = CharacterCreationAgent()
        instructions = agent.build_system_instructions()

        self.assertIsInstance(instructions, str)
        self.assertGreater(len(instructions), 0)

    def test_character_creation_agent_includes_living_world_instruction(self):
        """CharacterCreationAgent must include living world instruction during character creation.

        The living world must keep updating even while the player is in character
        creation flow. Time does not advance, but the game world continues.

        Regression test for bead rev-wa1u5.
        """
        with (
            patch("mvp_site.agent_prompts._load_instruction_file", return_value="BASE"),
            patch.object(
                PromptBuilder,
                "build_living_world_instruction",
                return_value="LW_CONTENT",
            ) as mock_lw,
        ):
            agent = CharacterCreationAgent()
            instructions = agent.build_system_instructions(turn_number=3)

        self.assertIn("LW_CONTENT", instructions)
        mock_lw.assert_called_once_with(3)


class TestPromptBuilderCharacterCreation(unittest.TestCase):
    """Tests for PromptBuilder character creation instruction order."""

    @patch("mvp_site.agent_prompts._load_instruction_file")
    def test_prompt_builder_character_creation_includes_game_state(self, mock_load):
        """PromptBuilder.build_character_creation_instructions includes GAME_STATE early."""

        mock_load.side_effect = lambda prompt_type: f"INSTR:{prompt_type}"

        builder = PromptBuilder()
        parts = builder.build_character_creation_instructions()

        self.assertEqual(len(parts), 5)
        # Second prompt should be the canonical game state schema reference.
        self.assertEqual(
            mock_load.call_args_list[1].args[0],
            constants.PROMPT_TYPE_GAME_STATE,
        )

    def test_character_creation_prompt_injects_canonical_spell_field_docs(self):
        """Character creation prompt should pull spell field docs from canonical schema."""
        _loaded_instructions_cache.clear()

        content = _load_instruction_file(constants.PROMPT_TYPE_CHARACTER_CREATION)

        self.assertIn("### PlayerCharacter Schema Fields", content)
        self.assertIn("`spells_prepared` (array):", content)
        self.assertIn("Today's prepared spells for prepared-caster classes", content)
        self.assertIn("`spells` (array): Character's spells list", content)
        self.assertNotIn("{{SCHEMA_FIELDS:", content)


class TestGetAgentForInput(unittest.TestCase):
    """Test cases for get_agent_for_input factory function."""

    def test_get_agent_returns_god_mode_for_god_mode_input(self):
        """get_agent_for_input returns GodModeAgent for god mode inputs."""
        test_inputs = [
            "GOD MODE: Set my HP to 50",
            "god mode: heal me",
            "GOD MODE:",
        ]
        for user_input in test_inputs:
            agent, _ = get_agent_for_input(user_input)
            self.assertIsInstance(
                agent, GodModeAgent, f"Should return GodModeAgent for: {user_input}"
            )

    def test_get_agent_returns_god_mode_for_mode_parameter(self):
        """get_agent_for_input returns GodModeAgent when mode='god' even without prefix.

        This is critical for UI-based god mode switching where the mode is passed
        as a parameter rather than requiring "GOD MODE:" prefix in user text.
        """
        # These inputs do NOT have the "GOD MODE:" prefix but should still
        # route to GodModeAgent when mode="god" is passed from the UI
        test_inputs = [
            "stop ignoring me",
            "what are my army numbers?",
            "fix this state",
            "regular text without prefix",
        ]
        for user_input in test_inputs:
            agent, _ = get_agent_for_input(user_input, mode="god")
            self.assertIsInstance(
                agent,
                GodModeAgent,
                f"Should return GodModeAgent for mode='god' with input: {user_input}",
            )

    def test_get_agent_god_mode_case_insensitive(self):
        """get_agent_for_input handles mode parameter case-insensitively.

        Users or clients may send 'God', 'GOD', 'god', etc. All should work.
        """
        mode_variations = ["god", "God", "GOD", "gOd", "goD"]
        for mode in mode_variations:
            agent, _ = get_agent_for_input("set HP to 100", mode=mode)
            self.assertIsInstance(
                agent,
                GodModeAgent,
                f"Should return GodModeAgent for mode='{mode}' (case-insensitive)",
            )

    def test_get_agent_returns_story_mode_for_regular_input(self):
        """get_agent_for_input returns StoryModeAgent for regular inputs."""
        test_inputs = [
            "I attack the goblin!",
            "Think about my options",
            "god",
            "What is god mode?",
        ]
        with patch(
            "mvp_site.agents.intent_classifier.classify_intent"
        ) as mock_classify:
            mock_classify.return_value = (constants.MODE_CHARACTER, 0.1)
            for user_input in test_inputs:
                agent, _ = get_agent_for_input(user_input)
                self.assertIsInstance(
                    agent,
                    StoryModeAgent,
                    f"Should return StoryModeAgent for: {user_input}",
                )

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_get_agent_returns_story_mode_for_spicy_toggle_commands(
        self, mock_classify
    ):
        """Spicy mode toggle commands should not trigger classifier routing."""
        mock_classify.return_value = (constants.MODE_CHARACTER, 0.0)
        mock_game_state = create_mock_game_state(in_combat=False)
        test_inputs = [
            "Enable Spicy Mode",
            "Activate Spicy Mode",
            "Exit Spicy Mode",
            "Disable Spicy Mode",
            "Return from Spicy Mode",
            "Enable Spicy Mode - Switch to a mature content mode",
            "Enable Spicy Mode — Switch to a mature content mode",
            "Enable Spicy Mode – Switch to a mature content mode",
        ]

        for user_input in test_inputs:
            agent, _ = get_agent_for_input(user_input, game_state=mock_game_state)
            self.assertIsInstance(
                agent,
                StoryModeAgent,
                f"Should return StoryModeAgent for toggle command: {user_input}",
            )

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_get_agent_includes_raw_classifier_metadata_for_spicy_toggle(
        self, mock_classify
    ):
        """Spicy toggle commands should preserve raw classifier intent in metadata."""
        mock_classify.return_value = (constants.MODE_SPICY, 0.9)
        mock_game_state = create_mock_game_state(in_combat=False)

        agent, metadata = get_agent_for_input(
            "Enable Spicy Mode", game_state=mock_game_state
        )

        self.assertIsInstance(agent, StoryModeAgent)
        self.assertEqual(metadata.get("raw_classifier_intent"), constants.MODE_SPICY)
        self.assertEqual(metadata.get("raw_classifier_confidence"), 0.9)

    def test_get_agent_passes_game_state(self):
        """get_agent_for_input passes game_state to the agent."""
        mock_game_state = create_mock_game_state(in_combat=False)

        # Test with story mode
        story_agent, _ = get_agent_for_input("hello", game_state=mock_game_state)
        self.assertEqual(story_agent.game_state, mock_game_state)

        # Test with god mode
        god_agent, _ = get_agent_for_input("GOD MODE: test", game_state=mock_game_state)
        self.assertEqual(god_agent.game_state, mock_game_state)

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_get_agent_passes_context_to_classifier(self, mock_classify):
        """get_agent_for_input passes last_ai_response context to the intent classifier."""
        mock_classify.return_value = (constants.MODE_CHARACTER, 0.0)

        last_ai_response = "What would you like to ask the merchant?"
        user_input = "About his family."

        get_agent_for_input(user_input, last_ai_response=last_ai_response)

        # Verify classifier was called with both input and context
        mock_classify.assert_called_once_with(
            user_input, context=last_ai_response, spicy_bias=False
        )

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_get_agent_returns_combat_agent_when_in_combat(self, mock_classify):
        """get_agent_for_input returns CombatAgent when in_combat is True and semantic classifier routes to combat."""
        mock_classify.return_value = (constants.MODE_COMBAT, 0.85)
        mock_game_state = create_mock_game_state(in_combat=True)

        # Regular input during combat should use CombatAgent (semantic classifier + state validation)
        agent, _ = get_agent_for_input(
            "I attack the goblin!", game_state=mock_game_state
        )
        self.assertIsInstance(agent, CombatAgent)

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_get_agent_returns_combat_agent_when_combat_intent_but_not_in_combat(
        self, mock_classify
    ):
        """get_agent_for_input returns CombatAgent when semantic classifier returns MODE_COMBAT even if combat is not active (agent can initiate combat)."""
        mock_classify.return_value = (constants.MODE_COMBAT, 0.85)
        mock_game_state = create_mock_game_state(in_combat=False)

        # Semantic classifier says combat -> route to CombatAgent (agent can initiate combat)
        agent, _ = get_agent_for_input(
            "I attack the goblin!", game_state=mock_game_state
        )
        self.assertIsInstance(agent, CombatAgent)

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_get_agent_returns_rewards_agent_when_rewards_intent_but_no_rewards_pending(
        self, mock_classify
    ):
        """get_agent_for_input returns RewardsAgent when semantic classifier returns MODE_REWARDS even if no rewards pending (agent can check for missed rewards)."""
        mock_classify.return_value = (constants.MODE_REWARDS, 0.80)
        mock_game_state = create_mock_game_state(in_combat=False)

        # Semantic classifier says rewards -> route to RewardsAgent (agent can check for missed rewards)
        agent, _ = get_agent_for_input("claim my rewards", game_state=mock_game_state)
        self.assertIsInstance(agent, RewardsAgent)

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_get_agent_suppresses_character_creation_misfire_when_not_active(
        self, mock_classify
    ):
        """Semantic char-creation intent should fall back to story when request is not explicit."""
        mock_classify.return_value = (constants.MODE_CHARACTER_CREATION, 0.75)
        # Create game state with character creation NOT active (character completed, no level-up pending)
        mock_game_state = create_mock_game_state(
            in_combat=False,
            character_creation_completed=True,
            character_name="Test Character",
            character_class="Fighter",
        )

        # Non-explicit request should not be hijacked into CharacterCreationAgent
        agent, _ = get_agent_for_input(
            "Assume I long rest and continue the mission",
            game_state=mock_game_state,
        )
        self.assertIsInstance(
            agent,
            StoryModeAgent,
            "CharacterCreationAgent suppressed when inactive and input not explicit",
        )

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_get_agent_returns_character_creation_agent_when_intent_and_active(
        self, mock_classify
    ):
        """get_agent_for_input returns CharacterCreationAgent when semantic classifier returns MODE_CHARACTER_CREATION and character creation is active."""
        mock_classify.return_value = (constants.MODE_CHARACTER_CREATION, 0.75)
        # Create game state with character creation active
        mock_game_state = create_character_creation_game_state()

        # Semantic classifier says character creation -> route to CharacterCreationAgent
        agent, _ = get_agent_for_input("level up", game_state=mock_game_state)
        self.assertIsInstance(agent, CharacterCreationAgent)

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_get_agent_routes_character_creation_when_explicit_request_not_active(
        self, mock_classify
    ):
        """Explicit level-up wording should still allow CharacterCreationAgent when not active."""
        # Use confidence meeting the explicit threshold (>= 0.8)
        # This replaces legacy regex-based keyword detection in tests
        mock_classify.return_value = (constants.MODE_CHARACTER_CREATION, 0.85)
        mock_game_state = create_mock_game_state(
            in_combat=False,
            character_creation_completed=True,
            character_name="Test Character",
            character_class="Fighter",
        )

        agent, _ = get_agent_for_input(
            "level up to level 9",
            game_state=mock_game_state,
        )
        self.assertIsInstance(agent, CharacterCreationAgent)

    def test_get_agent_rejects_character_creation_on_explicit_mode_without_state(
        self,
    ):
        """get_agent_for_input rejects explicit mode='character_creation' (internal mode)."""
        # Create game state with character creation NOT active
        mock_game_state = create_mock_game_state(
            in_combat=False,
            character_creation_completed=True,
            character_name="Test Character",
            character_class="Fighter",
        )

        # Explicit mode parameter should be rejected and fall through to StoryModeAgent
        agent, _ = get_agent_for_input(
            "continue",
            mode=constants.MODE_CHARACTER_CREATION,
            game_state=mock_game_state,
        )
        self.assertIsInstance(
            agent,
            StoryModeAgent,
            "Internal mode 'character_creation' cannot be forced via API",
        )

    def test_get_agent_mode_parameter_case_insensitive(self):
        """get_agent_for_input handles mode parameter case-insensitively (consistent with Priority 1 and 4)."""
        mock_game_state = create_mock_game_state(in_combat=False)

        # Test uppercase mode values (should match lowercase constants)
        # Use GOD mode as it's an allowed user-facing mode
        god_agent_upper, _ = get_agent_for_input(
            "continue", mode="GOD", game_state=mock_game_state
        )
        self.assertIsInstance(
            god_agent_upper, GodModeAgent, "mode='GOD' should match MODE_GOD"
        )

        # Test think mode
        think_agent_upper, _ = get_agent_for_input(
            "continue", mode="THINK", game_state=mock_game_state
        )
        self.assertIsInstance(
            think_agent_upper,
            PlanningAgent,
            "mode='THINK' should match MODE_THINK",
        )

        # Test mixed case
        god_agent_mixed, _ = get_agent_for_input(
            "continue", mode="God", game_state=mock_game_state
        )
        self.assertIsInstance(
            god_agent_mixed, GodModeAgent, "mode='God' should match MODE_GOD"
        )

    def test_get_agent_god_mode_overrides_combat(self):
        """GOD MODE takes priority over combat mode."""
        mock_game_state = create_mock_game_state(in_combat=True)

        # GOD MODE should still work even during combat
        agent, _ = get_agent_for_input(
            "GOD MODE: Set HP to 100", game_state=mock_game_state
        )
        self.assertIsInstance(agent, GodModeAgent)

    def test_get_agent_priority_order(self):
        """Verify agent priority: GOD MODE > CharacterCreation > Combat > Rewards > Story."""
        # Priority 1: GOD MODE always wins (even during character creation)
        char_creation_state = create_character_creation_game_state()
        god_agent, _ = get_agent_for_input(
            "GOD MODE: test", game_state=char_creation_state
        )
        self.assertIsInstance(god_agent, GodModeAgent)

        # Priority 2: Character Creation when character not complete
        char_agent, _ = get_agent_for_input(
            "I want to be a wizard", game_state=char_creation_state
        )
        self.assertIsInstance(char_agent, CharacterCreationAgent)

        # Priority 2b: Completion phrases transition out of character creation
        done_agent, _ = get_agent_for_input("I'm done", game_state=char_creation_state)
        self.assertIsInstance(done_agent, StoryModeAgent)
        self.assertFalse(
            char_creation_state.custom_campaign_state.get(
                "character_creation_in_progress", True
            )
        )
        self.assertTrue(
            char_creation_state.custom_campaign_state.get(
                "character_creation_completed", False
            )
        )

        # Priority 3: Combat when in_combat=True (semantic classifier + state validation)
        with patch(
            "mvp_site.agents.intent_classifier.classify_intent"
        ) as mock_classify:
            mock_classify.return_value = (constants.MODE_COMBAT, 0.85)
            combat_state = create_mock_game_state(in_combat=True)
            combat_agent, _ = get_agent_for_input(
                "attack the goblin", game_state=combat_state
            )
            self.assertIsInstance(combat_agent, CombatAgent)

        # Priority 4: Rewards mode when rewards are pending (semantic classifier + state validation)
        with patch(
            "mvp_site.agents.intent_classifier.classify_intent"
        ) as mock_classify:
            mock_classify.return_value = (constants.MODE_REWARDS, 0.80)
            rewards_state = create_rewards_game_state(
                combat_state={
                    "in_combat": False,
                    "combat_phase": "ended",
                    "combat_summary": {"result": "victory"},
                    "rewards_processed": False,
                }
            )
            rewards_agent, _ = get_agent_for_input(
                "claim my rewards", game_state=rewards_state
            )
            self.assertIsInstance(rewards_agent, RewardsAgent)

        # Priority 5: Story mode as default
        no_combat_state = create_mock_game_state(in_combat=False)
        with patch(
            "mvp_site.agents.intent_classifier.classify_intent"
        ) as mock_classify:
            mock_classify.return_value = (constants.MODE_CHARACTER, 0.1)
            story_agent, _ = get_agent_for_input("attack", game_state=no_combat_state)
            self.assertIsInstance(story_agent, StoryModeAgent)

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_get_agent_returns_rewards_agent_when_encounter_rewards_pending(
        self, mock_classify
    ):
        """get_agent_for_input returns RewardsAgent when encounter rewards pending and semantic classifier routes to rewards."""
        mock_classify.return_value = (constants.MODE_REWARDS, 0.80)
        rewards_state = create_rewards_game_state(
            encounter_state={
                "encounter_completed": True,
                "rewards_processed": False,
                "encounter_summary": {"result": "success", "xp_awarded": 50},
            }
        )

        agent, _ = get_agent_for_input("claim my rewards", game_state=rewards_state)
        self.assertIsInstance(agent, RewardsAgent)


class TestAgentInstructionBuilding(unittest.TestCase):
    """Test cases for agent system instruction building."""

    @patch("mvp_site.agent_prompts._load_instruction_file")
    def test_story_mode_agent_builds_instructions(self, mock_load):
        """StoryModeAgent.build_system_instructions returns instruction string."""
        mock_load.return_value = "Test instruction content"

        agent = StoryModeAgent()
        instructions = agent.build_system_instructions(
            selected_prompts=[constants.PROMPT_TYPE_NARRATIVE],
            use_default_world=False,
            include_continuation_reminder=False,
        )

        self.assertIsInstance(instructions, str)
        self.assertGreater(len(instructions), 0)

    @patch("mvp_site.agent_prompts._load_instruction_file")
    def test_god_mode_agent_builds_instructions(self, mock_load):
        """GodModeAgent.build_system_instructions returns instruction string."""
        mock_load.return_value = "Test instruction content"

        agent = GodModeAgent()
        instructions = agent.build_system_instructions()

        self.assertIsInstance(instructions, str)
        self.assertGreater(len(instructions), 0)

    @patch("mvp_site.agent_prompts._load_instruction_file")
    def test_god_mode_ignores_selected_prompts(self, mock_load):
        """GodModeAgent ignores selected_prompts parameter."""
        mock_load.return_value = "Test instruction content"

        agent = GodModeAgent()

        # Call with various selected_prompts - should all produce same result
        result1 = agent.build_system_instructions(selected_prompts=None)
        result2 = agent.build_system_instructions(
            selected_prompts=[constants.PROMPT_TYPE_NARRATIVE]
        )

        # Both should work without error - god mode uses fixed prompt set
        self.assertIsInstance(result1, str)
        self.assertIsInstance(result2, str)

    @patch("mvp_site.agent_prompts._load_instruction_file")
    def test_combat_agent_builds_instructions(self, mock_load):
        """CombatAgent.build_system_instructions returns instruction string."""
        mock_load.return_value = "Test instruction content"

        agent = CombatAgent()
        instructions = agent.build_system_instructions()

        self.assertIsInstance(instructions, str)
        self.assertGreater(len(instructions), 0)

    @patch("mvp_site.agent_prompts._load_instruction_file")
    def test_combat_mode_ignores_selected_prompts(self, mock_load):
        """CombatAgent ignores selected_prompts parameter (uses fixed combat set)."""
        mock_load.return_value = "Test instruction content"

        agent = CombatAgent()

        # Call with various selected_prompts - should all produce same result
        result1 = agent.build_system_instructions(selected_prompts=None)
        result2 = agent.build_system_instructions(
            selected_prompts=[constants.PROMPT_TYPE_NARRATIVE]
        )

        # Both should work without error - combat mode uses fixed prompt set
        self.assertIsInstance(result1, str)
        self.assertIsInstance(result2, str)


class TestAgentPromptSets(unittest.TestCase):
    """Test cases verifying agents have correct prompt subsets."""

    def test_story_mode_does_not_include_god_mode_prompt(self):
        """StoryModeAgent prompt set does not include god_mode prompt."""
        all_prompts = StoryModeAgent.REQUIRED_PROMPTS | StoryModeAgent.OPTIONAL_PROMPTS
        self.assertNotIn(constants.PROMPT_TYPE_GOD_MODE, all_prompts)

    def test_god_mode_includes_god_mode_prompt(self):
        """GodModeAgent prompt set includes god_mode prompt."""
        self.assertIn(constants.PROMPT_TYPE_GOD_MODE, GodModeAgent.REQUIRED_PROMPTS)

    def test_god_mode_does_not_include_narrative_prompt(self):
        """GodModeAgent prompt set does not include narrative prompt."""
        all_prompts = GodModeAgent.REQUIRED_PROMPTS | GodModeAgent.OPTIONAL_PROMPTS
        self.assertNotIn(constants.PROMPT_TYPE_NARRATIVE, all_prompts)

    def test_all_agents_share_core_prompts(self):
        """All agents share essential core prompts."""
        shared_prompts = {
            constants.PROMPT_TYPE_MASTER_DIRECTIVE,
            constants.PROMPT_TYPE_GAME_STATE,
            constants.PROMPT_TYPE_DND_SRD,
        }

        story_all = StoryModeAgent.REQUIRED_PROMPTS | StoryModeAgent.OPTIONAL_PROMPTS
        combat_all = CombatAgent.REQUIRED_PROMPTS | CombatAgent.OPTIONAL_PROMPTS
        god_all = GodModeAgent.REQUIRED_PROMPTS | GodModeAgent.OPTIONAL_PROMPTS

        for prompt in shared_prompts:
            self.assertIn(
                prompt, story_all, f"StoryModeAgent missing shared prompt: {prompt}"
            )
            self.assertIn(
                prompt, god_all, f"GodModeAgent missing shared prompt: {prompt}"
            )
            self.assertIn(
                prompt, combat_all, f"CombatAgent missing shared prompt: {prompt}"
            )

    def test_combat_agent_includes_combat_prompt(self):
        """CombatAgent prompt set includes combat prompt."""
        self.assertIn(constants.PROMPT_TYPE_COMBAT, CombatAgent.REQUIRED_PROMPTS)

    def test_combat_agent_does_not_include_god_mode_prompt(self):
        """CombatAgent prompt set does not include god_mode prompt."""
        all_prompts = CombatAgent.REQUIRED_PROMPTS | CombatAgent.OPTIONAL_PROMPTS
        self.assertNotIn(constants.PROMPT_TYPE_GOD_MODE, all_prompts)

    def test_story_and_god_mode_do_not_include_combat_prompt(self):
        """StoryModeAgent and GodModeAgent do not include combat prompt."""
        story_all = StoryModeAgent.REQUIRED_PROMPTS | StoryModeAgent.OPTIONAL_PROMPTS
        god_all = GodModeAgent.REQUIRED_PROMPTS | GodModeAgent.OPTIONAL_PROMPTS

        self.assertNotIn(constants.PROMPT_TYPE_COMBAT, story_all)
        self.assertNotIn(constants.PROMPT_TYPE_COMBAT, god_all)


class TestSchemaInjection(unittest.TestCase):
    """Tests for dynamic schema injection in prompts."""

    def test_game_state_instruction_has_risk_levels_injected(self):
        """game_state_instruction.md should have VALID_RISK_LEVELS injected."""

        # Clear cache to force fresh load
        _loaded_instructions_cache.clear()

        content = _load_instruction_file(constants.PROMPT_TYPE_GAME_STATE)

        # Placeholder should be replaced
        self.assertNotIn(
            "{{VALID_RISK_LEVELS}}",
            content,
            "Placeholder was not replaced with actual values",
        )

        # Actual values should be present
        for level in VALID_RISK_LEVELS:
            self.assertIn(
                f'"{level}"',
                content,
                f"Risk level '{level}' not found in injected content",
            )

    def test_game_state_instruction_includes_full_canonical_schema(self):
        """game_state_instruction.md should inject the full canonical root schema."""

        _loaded_instructions_cache.clear()

        content = _load_instruction_file(constants.PROMPT_TYPE_GAME_STATE)

        self.assertNotIn("{{FULL_CANONICAL_GAME_STATE_SCHEMA}}", content)
        self.assertIn(
            '"$schema":"https://json-schema.org/draft/2020-12/schema"', content
        )
        self.assertIn('"title":"GameState"', content)
        self.assertIn('"properties"', content)

    def test_schema_injection_replaces_all_placeholders(self):
        """All schema placeholders should be replaced when loading prompts."""

        test_content = """
        Risk levels: {{VALID_RISK_LEVELS}}
        Confidence: {{VALID_CONFIDENCE_LEVELS}}
        Quality: {{VALID_QUALITY_TIERS}}
        Choice: {{CHOICE_SCHEMA}}
        Planning: {{PLANNING_BLOCK_SCHEMA}}
        """

        result = _inject_schema_placeholders(test_content)

        # All placeholders should be replaced
        self.assertNotIn("{{", result, "Unreplaced placeholder found")
        self.assertNotIn("}}", result, "Unreplaced placeholder found")

        # Check some expected values are present
        self.assertIn('"high"', result)  # From VALID_RISK_LEVELS
        self.assertIn('"string"', result)  # From schema type conversion

    def test_validation_uses_same_risk_levels_as_prompt(self):
        """Backend validation should use the same risk levels as injected into prompts."""

        # Clear cache
        _loaded_instructions_cache.clear()

        # Get the injected content

        content = _load_instruction_file(constants.PROMPT_TYPE_GAME_STATE)

        # The injected risk levels should match VALID_RISK_LEVELS exactly
        expected_json = json.dumps(sorted(VALID_RISK_LEVELS))
        self.assertIn(
            expected_json,
            content,
            f"Injected risk levels don't match VALID_RISK_LEVELS: {expected_json}",
        )

    def test_key_prompt_files_do_not_contain_literal_placeholder_tokens(self):
        """Regression guard: replaced prompt examples must never leave {placeholder} literals."""
        prompt_files = [
            "mvp_site/prompts/combat_system_instruction.md",
            "mvp_site/prompts/god_mode_instruction.md",
            "mvp_site/prompts/living_world_instruction.md",
            "mvp_site/prompts/faction_management_instruction.md",
            "mvp_site/prompts/faction_minigame_instruction.md",
            "mvp_site/prompts/deferred_rewards_instruction.md",
            "mvp_site/prompts/relationship_instruction.md",
            "mvp_site/prompts/reputation_instruction.md",
            "mvp_site/prompts/mechanics_system_instruction.md",
            "mvp_site/prompts/mechanics_system_instruction_code_execution.md",
            "mvp_site/prompts/game_state_instruction.md",
        ]
        for prompt_path in prompt_files:
            with self.subTest(prompt_path=prompt_path):
                with open(prompt_path, encoding="utf-8") as f:
                    content = f.read()
                self.assertNotIn("{placeholder}", content)

    def test_game_state_prompt_keeps_full_canonical_schema_placeholder(self):
        """Guard against replacing FULL_CANONICAL_GAME_STATE_SCHEMA with invalid placeholder text."""
        with open("mvp_site/prompts/game_state_instruction.md", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("{{FULL_CANONICAL_GAME_STATE_SCHEMA}}", content)

    def test_faction_management_prompt_keeps_step_7_9_definition(self):
        """Guard against deleting mandatory incomplete-enablement instructions."""
        with open(
            "mvp_site/prompts/faction_management_instruction.md", encoding="utf-8"
        ) as f:
            content = f.read()
        self.assertIn("STEP 7.9: Incomplete State Check", content)
        self.assertIn("enabled=true but units missing", content)

    def test_god_mode_prompt_uses_full_response_format_not_god_mode_directive(self):
        """Guard against replacing god-mode response schema with GodModeDirective example."""
        with open("mvp_site/prompts/god_mode_instruction.md", encoding="utf-8") as f:
            content = f.read()
        self.assertIn('"god_mode_response"', content)
        self.assertNotIn("{{STATE_EXAMPLE:GodModeDirective}}", content)

    def test_generate_example_handles_anyof_oneof_non_ref_options(self):
        """anyOf/oneOf branches with inline types should still produce concrete examples."""
        definitions = {
            "InnerObj": {
                "type": "object",
                "properties": {"value": {"type": "integer"}},
            },
        }
        schema = {
            "type": "object",
            "properties": {
                "inline_object": {
                    "anyOf": [
                        {"type": "object", "properties": {"name": {"type": "string"}}},
                        {"type": "null"},
                    ]
                },
                "inline_string": {"oneOf": [{"type": "string"}, {"type": "null"}]},
                "array_ref": {
                    "anyOf": [
                        {"type": "array", "items": {"$ref": "#/$defs/InnerObj"}},
                        {"type": "null"},
                    ]
                },
            },
        }
        example = _generate_example_from_def(schema, definitions)
        self.assertIsInstance(example["inline_object"], dict)
        self.assertIn("name", example["inline_object"])
        self.assertEqual(example["inline_string"], "<string>")
        self.assertIsInstance(example["array_ref"], list)
        self.assertEqual(example["array_ref"][0]["value"], 0)


class TestPromptOrderInvariants(unittest.TestCase):
    """
    Tests for prompt order invariants (Phase 0 of prompt-builder refactor).

    These tests verify that:
    1. Each agent has an explicit REQUIRED_PROMPT_ORDER tuple
    2. master_directive is always first
    3. game_state and planning_protocol are always consecutive
    """

    def test_all_agents_have_required_prompt_order(self):
        """Every agent class must define REQUIRED_PROMPT_ORDER."""

        for agent_cls in ALL_AGENT_CLASSES:
            with self.subTest(agent=agent_cls.__name__):
                self.assertTrue(
                    hasattr(agent_cls, "REQUIRED_PROMPT_ORDER"),
                    f"{agent_cls.__name__} missing REQUIRED_PROMPT_ORDER",
                )
                self.assertIsInstance(
                    agent_cls.REQUIRED_PROMPT_ORDER,
                    tuple,
                    f"{agent_cls.__name__}.REQUIRED_PROMPT_ORDER must be a tuple",
                )
                self.assertGreater(
                    len(agent_cls.REQUIRED_PROMPT_ORDER),
                    0,
                    f"{agent_cls.__name__}.REQUIRED_PROMPT_ORDER is empty",
                )

    def test_required_prompts_matches_order(self):
        """REQUIRED_PROMPTS frozenset must match REQUIRED_PROMPT_ORDER tuple."""

        for agent_cls in ALL_AGENT_CLASSES:
            with self.subTest(agent=agent_cls.__name__):
                order_set = frozenset(agent_cls.REQUIRED_PROMPT_ORDER)
                self.assertEqual(
                    agent_cls.REQUIRED_PROMPTS,
                    order_set,
                    f"{agent_cls.__name__}: REQUIRED_PROMPTS != frozenset(REQUIRED_PROMPT_ORDER)",
                )

    def test_master_directive_is_first(self):
        """master_directive must be the first prompt in every agent's order."""

        for agent_cls in ALL_AGENT_CLASSES:
            with self.subTest(agent=agent_cls.__name__):
                self.assertEqual(
                    agent_cls.REQUIRED_PROMPT_ORDER[0],
                    MANDATORY_FIRST_PROMPT,
                    f"{agent_cls.__name__}: First prompt must be {MANDATORY_FIRST_PROMPT!r}, "
                    f"got {agent_cls.REQUIRED_PROMPT_ORDER[0]!r}",
                )

    def test_game_state_and_planning_protocol_consecutive(self):
        """game_state and planning_protocol must be consecutive in order."""

        game_state, planning_protocol = GAME_STATE_PLANNING_PAIR

        for agent_cls in ALL_AGENT_CLASSES:
            # Skip CharacterCreationAgent - minimal prompt set intentionally omits these
            if agent_cls.__name__ == "CharacterCreationAgent":
                continue

            with self.subTest(agent=agent_cls.__name__):
                order = agent_cls.REQUIRED_PROMPT_ORDER

                # Both must be present
                self.assertIn(
                    game_state,
                    order,
                    f"{agent_cls.__name__}: Missing {game_state} in order",
                )
                self.assertIn(
                    planning_protocol,
                    order,
                    f"{agent_cls.__name__}: Missing {planning_protocol} in order",
                )

                # planning_protocol must immediately follow game_state
                game_idx = order.index(game_state)
                planning_idx = order.index(planning_protocol)
                self.assertEqual(
                    planning_idx,
                    game_idx + 1,
                    f"{agent_cls.__name__}: planning_protocol (at {planning_idx}) must "
                    f"immediately follow game_state (at {game_idx})",
                )

    def test_validate_all_agent_prompt_orders_succeeds(self):
        """validate_all_agent_prompt_orders() should return empty dict (all valid)."""

        errors = validate_all_agent_prompt_orders()
        self.assertEqual(
            errors,
            {},
            f"Validation errors found: {errors}",
        )

    def test_validate_prompt_order_catches_wrong_first_prompt(self):
        """validate_prompt_order should catch when first prompt is wrong."""

        bad_order = (
            constants.PROMPT_TYPE_DND_SRD,  # Wrong! Should be master_directive
            constants.PROMPT_TYPE_GAME_STATE,
            constants.PROMPT_TYPE_PLANNING_PROTOCOL,
        )
        errors = validate_prompt_order(bad_order, "TestAgent")

        self.assertEqual(len(errors), 1)
        self.assertIn("First prompt must be", errors[0])

    def test_validate_prompt_order_catches_non_consecutive_pair(self):
        """validate_prompt_order should catch when game_state and planning_protocol aren't consecutive."""

        bad_order = (
            constants.PROMPT_TYPE_MASTER_DIRECTIVE,
            constants.PROMPT_TYPE_GAME_STATE,
            constants.PROMPT_TYPE_DND_SRD,  # Wrong! planning_protocol should be here
            constants.PROMPT_TYPE_PLANNING_PROTOCOL,
        )
        errors = validate_prompt_order(bad_order, "TestAgent")

        self.assertEqual(len(errors), 1)
        self.assertIn("planning_protocol must immediately follow game_state", errors[0])

    def test_validate_prompt_order_reports_missing_required_prompts(self):
        """Missing game_state or planning_protocol should be reported explicitly."""

        order_missing_both = (
            constants.PROMPT_TYPE_MASTER_DIRECTIVE,
            "think",
        )

        errors = validate_prompt_order(order_missing_both, "TestAgent")

        self.assertEqual(len(errors), 1)
        self.assertIn("Missing required prompt(s) in order", errors[0])
        self.assertIn(constants.PROMPT_TYPE_GAME_STATE, errors[0])
        self.assertIn(constants.PROMPT_TYPE_PLANNING_PROTOCOL, errors[0])

    def test_validate_prompt_order_detects_duplicate_prompt_types(self):
        """Duplicate prompt types in REQUIRED_PROMPT_ORDER should be detected with indices."""

        duplicate_order = (
            constants.PROMPT_TYPE_MASTER_DIRECTIVE,
            constants.PROMPT_TYPE_GAME_STATE,
            constants.PROMPT_TYPE_GAME_STATE,
            constants.PROMPT_TYPE_PLANNING_PROTOCOL,
        )

        errors = validate_prompt_order(duplicate_order, "TestAgent")

        self.assertTrue(errors)
        self.assertIn("Duplicate prompt type", errors[0])

    def test_runtime_validation_raises_on_invalid_order(self):
        """Instantiating an agent with invalid order should raise at runtime."""

        class BadAgent(FixedPromptAgent):
            REQUIRED_PROMPT_ORDER = (
                constants.PROMPT_TYPE_DND_SRD,  # Wrong: master must be first
                constants.PROMPT_TYPE_GAME_STATE,
                constants.PROMPT_TYPE_PLANNING_PROTOCOL,
            )
            REQUIRED_PROMPTS = frozenset(REQUIRED_PROMPT_ORDER)
            MODE = "bad"

        with self.assertRaises(ValueError) as ctx:
            BadAgent()

        self.assertIn("Invalid REQUIRED_PROMPT_ORDER", str(ctx.exception))


class TestGenericPromptBuilder(unittest.TestCase):
    """
    Tests for the generic build_from_order() method (Phase 1).

    Verifies that the generic builder produces the same output as
    the mode-specific builders.
    """

    def test_build_from_order_matches_god_mode_builder(self):
        """build_from_order should produce same output as build_god_mode_instructions."""
        builder = PromptBuilder(None)

        old_parts = builder.build_god_mode_instructions()
        new_parts = builder.build_from_order(
            GodModeAgent.REQUIRED_PROMPT_ORDER, include_debug=False
        )

        self.assertEqual(
            len(old_parts),
            len(new_parts),
            f"Part count mismatch: old={len(old_parts)}, new={len(new_parts)}",
        )
        for i, (old, new) in enumerate(zip(old_parts, new_parts, strict=False)):
            self.assertEqual(
                old, new, f"Part {i} mismatch between old and new builders"
            )

    def test_build_from_order_matches_info_mode_builder(self):
        """build_from_order should produce same output as build_info_mode_instructions."""

        builder = PromptBuilder(None)

        old_parts = builder.build_info_mode_instructions()
        new_parts = builder.build_from_order(
            InfoAgent.REQUIRED_PROMPT_ORDER, include_debug=False
        )

        self.assertEqual(len(old_parts), len(new_parts))
        for i, (old, new) in enumerate(zip(old_parts, new_parts, strict=False)):
            self.assertEqual(old, new, f"Part {i} mismatch")

    def test_build_from_order_with_debug_flag(self):
        """include_debug=True should append debug instructions."""

        builder = PromptBuilder(None)

        without_debug = builder.build_from_order(
            InfoAgent.REQUIRED_PROMPT_ORDER, include_debug=False
        )
        with_debug = builder.build_from_order(
            InfoAgent.REQUIRED_PROMPT_ORDER, include_debug=True
        )

        self.assertEqual(
            len(with_debug),
            len(without_debug) + 1,
            "include_debug=True should add exactly 1 part",
        )

    def test_build_from_order_preserves_order(self):
        """Prompts should be loaded in the exact order specified."""

        builder = PromptBuilder(None)
        parts = builder.build_from_order(
            CombatAgent.REQUIRED_PROMPT_ORDER, include_debug=False, turn_number=3
        )

        # Expected count: one part per prompt type
        self.assertEqual(
            len(parts),
            len(CombatAgent.REQUIRED_PROMPT_ORDER),
            "Should have one part per prompt type",
        )

    def test_build_from_order_appends_lw_for_time_advancing_agents(self):
        """Global LW append should run for time-advancing agents when missing in order."""
        with (
            patch("mvp_site.agent_prompts._load_instruction_file", return_value="BASE"),
            patch.object(
                PromptBuilder, "build_living_world_instruction", return_value="LW"
            ) as mock_lw,
        ):
            builder = PromptBuilder(None)
            parts = builder.build_from_order(
                (constants.PROMPT_TYPE_MASTER_DIRECTIVE,),
                turn_number=3,
                advances_time=True,
            )
        self.assertEqual(parts[-1], "LW")
        mock_lw.assert_called_once_with(3)

    def test_build_from_order_skips_lw_for_non_time_advancing_agents(self):
        """Global LW append should not run for non-time-advancing agents."""
        with (
            patch("mvp_site.agent_prompts._load_instruction_file", return_value="BASE"),
            patch.object(
                PromptBuilder, "build_living_world_instruction", return_value="LW"
            ) as mock_lw,
        ):
            builder = PromptBuilder(None)
            parts = builder.build_from_order(
                (constants.PROMPT_TYPE_MASTER_DIRECTIVE,),
                turn_number=3,
                advances_time=False,
            )
        self.assertNotIn("LW", parts)
        mock_lw.assert_not_called()

    def test_combat_prompt_order_includes_living_world(self):
        """CombatAgent should include living world prompts.

        Inclusion is explicit through REQUIRED_PROMPT_ORDER.
        """

        self.assertIn(
            constants.PROMPT_TYPE_LIVING_WORLD,
            CombatAgent.REQUIRED_PROMPT_ORDER,
            "CombatAgent should include living world prompts in REQUIRED_PROMPT_ORDER",
        )

    def test_resolve_campaign_tier_from_custom_state_dict(self):
        """PromptBuilder should resolve tier from custom_campaign_state dict."""
        builder = PromptBuilder(None)
        builder.game_state = {
            "custom_campaign_state": {"campaign_tier": constants.CAMPAIGN_TIER_DIVINE}
        }

        self.assertEqual(
            builder._resolve_campaign_tier(), constants.CAMPAIGN_TIER_DIVINE
        )

    def test_resolve_campaign_tier_from_top_level_dict(self):
        """PromptBuilder should resolve tier from top-level campaign_tier."""
        builder = PromptBuilder(None)
        builder.game_state = {"campaign_tier": constants.CAMPAIGN_TIER_SOVEREIGN}

        self.assertEqual(
            builder._resolve_campaign_tier(), constants.CAMPAIGN_TIER_SOVEREIGN
        )

    def test_resolve_campaign_tier_from_object_method(self):
        """PromptBuilder should resolve tier via get_campaign_tier method."""

        class _FakeGameState:
            def get_campaign_tier(self):
                return constants.CAMPAIGN_TIER_DIVINE

        builder = PromptBuilder(None)
        builder.game_state = _FakeGameState()

        self.assertEqual(
            builder._resolve_campaign_tier(), constants.CAMPAIGN_TIER_DIVINE
        )


class TestBuildForAgent(unittest.TestCase):
    """
    Tests for the single entry point build_for_agent() method (Phase 3).

    Verifies that build_for_agent correctly uses agent's prompt_order()
    and builder_flags() to build instructions.
    """

    def test_build_for_agent_uses_prompt_order(self):
        """build_for_agent should use agent's prompt_order()."""

        agent = InfoAgent(None)
        builder = PromptBuilder(None)

        parts = builder.build_for_agent(agent)

        # InfoAgent has 3 prompts, no debug
        self.assertEqual(
            len(parts),
            len(InfoAgent.REQUIRED_PROMPT_ORDER),
            "Should have one part per prompt in order",
        )

    def test_build_for_agent_respects_include_debug(self):
        """build_for_agent should respect agent's builder_flags()['include_debug']."""

        builder = PromptBuilder(None)

        # InfoAgent has include_debug=False (default)
        info_agent = InfoAgent(None)
        info_parts = builder.build_for_agent(info_agent)
        self.assertEqual(len(info_parts), len(InfoAgent.REQUIRED_PROMPT_ORDER))

        # CombatAgent has include_debug=True
        combat_agent = CombatAgent(None)
        combat_parts = builder.build_for_agent(combat_agent, turn_number=3)
        self.assertEqual(
            len(combat_parts),
            len(CombatAgent.REQUIRED_PROMPT_ORDER) + 1,  # +1 for debug
            "CombatAgent should include debug instructions",
        )

    def test_builder_flags_defaults(self):
        """BaseAgent.builder_flags() should default to include_debug=False."""

        # InfoAgent inherits default builder_flags
        info_agent = InfoAgent(None)
        self.assertEqual(info_agent.builder_flags(), {"include_debug": False})

        # PlanningAgent also inherits default
        planning_agent = PlanningAgent(None)
        self.assertEqual(planning_agent.builder_flags(), {"include_debug": False})

    def test_builder_flags_overrides(self):
        """Agents with debug should override builder_flags()."""

        # These agents should include debug
        story_agent = StoryModeAgent(None)
        self.assertEqual(story_agent.builder_flags(), {"include_debug": True})

        combat_agent = CombatAgent(None)
        self.assertEqual(combat_agent.builder_flags(), {"include_debug": True})

        rewards_agent = RewardsAgent(None)
        self.assertEqual(rewards_agent.builder_flags(), {"include_debug": True})

    def test_build_for_agent_matches_legacy_builder(self):
        """build_for_agent should match legacy mode-specific builders."""
        builder = PromptBuilder(None)

        # Test GodModeAgent (no debug)
        god_agent = GodModeAgent(None)
        new_parts = builder.build_for_agent(god_agent)
        old_parts = builder.build_god_mode_instructions()

        self.assertEqual(len(new_parts), len(old_parts))
        for i, (new, old) in enumerate(zip(new_parts, old_parts, strict=False)):
            self.assertEqual(new, old, f"GodMode part {i} mismatch")


class TestPromptOrderDriftGuards(unittest.TestCase):
    """
    Drift-guard tests to ensure Story/Combat agents don't silently diverge
    from REQUIRED_PROMPT_ORDER invariants.

    These tests verify that the beginning of the prompt output matches
    build_from_order(REQUIRED_PROMPT_ORDER), preventing silent drift
    from the validated order over time.
    """

    def test_combat_agent_uses_build_from_order(self):
        """CombatAgent output should match build_from_order(REQUIRED_PROMPT_ORDER)."""

        builder = PromptBuilder(None)
        combat_agent = CombatAgent(None)

        # Get what build_from_order produces (source of truth)
        expected_parts = builder.build_from_order(
            CombatAgent.REQUIRED_PROMPT_ORDER, include_debug=True
        )

        # Get what build_for_agent produces
        actual_parts = builder.build_for_agent(combat_agent)

        # Should match exactly
        self.assertEqual(
            len(actual_parts),
            len(expected_parts),
            f"CombatAgent part count mismatch: expected {len(expected_parts)}, got {len(actual_parts)}",
        )
        for i, (expected, actual) in enumerate(
            zip(expected_parts, actual_parts, strict=False)
        ):
            self.assertEqual(
                expected,
                actual,
                f"CombatAgent part {i} drifted from REQUIRED_PROMPT_ORDER",
            )

    def test_story_mode_agent_starts_with_invariant_head(self):
        """StoryModeAgent output should start with master → game_state+planning."""

        story_agent = StoryModeAgent(None)

        # Get the instruction parts (before finalization)
        parts = story_agent.build_system_instruction_parts()

        # Verify invariant head: must start with master_directive
        self.assertGreater(len(parts), 0, "StoryModeAgent produced no parts")

        # First part must contain master_directive content
        self.assertIn(
            "master",
            parts[0].lower(),
            f"First part should be master_directive, got: {parts[0][:100]}...",
        )

        # The game_state and planning_protocol should appear early (parts 1-2)
        # They're loaded together via _append_game_state_with_planning
        self.assertGreater(
            len(parts), 2, "StoryModeAgent needs at least 3 parts for core"
        )

        # Verify game_state appears (contains the planning block schema reference)
        combined_early_parts = " ".join(parts[:3]).lower()
        self.assertIn(
            "planning_block",
            combined_early_parts,
            "Early parts should reference planning_block schema",
        )

    def test_combat_agent_parity_with_legacy_builder(self):
        """CombatAgent build_from_order should match legacy build_combat_mode_instructions."""

        builder = PromptBuilder(None)

        # Legacy builder
        legacy_parts = builder.build_combat_mode_instructions()

        # New approach via build_from_order
        new_parts = builder.build_from_order(
            CombatAgent.REQUIRED_PROMPT_ORDER, include_debug=True
        )

        self.assertEqual(
            len(legacy_parts),
            len(new_parts),
            f"Part count mismatch: legacy={len(legacy_parts)}, new={len(new_parts)}",
        )
        for i, (legacy, new) in enumerate(zip(legacy_parts, new_parts, strict=False)):
            self.assertEqual(
                legacy,
                new,
                f"Combat part {i} mismatch between legacy and build_from_order",
            )


class FactionManagementAgentTests(unittest.TestCase):
    """Tests for FactionManagementAgent.matches_game_state() behavior."""

    def _create_mock_state_with_army_data(self, enabled, total_strength):
        """Helper to create mock state with proper army_data structure."""

        # Create a simple object that behaves like GameState
        class MockGameState:
            def __init__(self):
                self.custom_campaign_state = {"faction_minigame": {"enabled": enabled}}
                self.army_data = {"total_strength": total_strength}

        return MockGameState()

    def test_faction_agent_matches_game_state_enabled_false_returns_false(self):
        """FactionManagementAgent.matches_game_state returns False when enabled=False, regardless of forces."""
        mock_state = self._create_mock_state_with_army_data(
            enabled=False, total_strength=5000
        )

        self.assertFalse(FactionManagementAgent.matches_game_state(mock_state))

    def test_faction_agent_matches_game_state_enabled_false_with_low_forces(self):
        """FactionManagementAgent.matches_game_state returns False when enabled=False, even with low forces."""
        mock_state = self._create_mock_state_with_army_data(
            enabled=False, total_strength=10
        )

        self.assertFalse(FactionManagementAgent.matches_game_state(mock_state))

    def test_faction_agent_matches_game_state_enabled_true_with_sufficient_forces(self):
        """FactionManagementAgent.matches_game_state returns True when enabled=True and forces >= threshold."""
        mock_state = self._create_mock_state_with_army_data(
            enabled=True, total_strength=FACTION_FORCE_THRESHOLD
        )

        self.assertTrue(FactionManagementAgent.matches_game_state(mock_state))

    def test_faction_agent_matches_game_state_enabled_true_with_high_forces(self):
        """FactionManagementAgent.matches_game_state returns True when enabled=True and forces > threshold."""
        mock_state = self._create_mock_state_with_army_data(
            enabled=True, total_strength=5000
        )

        self.assertTrue(FactionManagementAgent.matches_game_state(mock_state))

    def test_faction_agent_matches_game_state_enabled_true_insufficient_forces(self):
        """FactionManagementAgent.matches_game_state returns False when enabled=True but forces < threshold."""
        mock_state = self._create_mock_state_with_army_data(
            enabled=True, total_strength=FACTION_FORCE_THRESHOLD - 1
        )

        self.assertFalse(FactionManagementAgent.matches_game_state(mock_state))

    def test_faction_agent_matches_game_state_enabled_true_no_army_data(self):
        """FactionManagementAgent.matches_game_state returns False when enabled=True but no army_data."""
        mock_state = Mock()
        mock_state.custom_campaign_state = {"faction_minigame": {"enabled": True}}
        # Don't set army_data attribute at all
        delattr(mock_state, "army_data") if hasattr(mock_state, "army_data") else None

        self.assertFalse(FactionManagementAgent.matches_game_state(mock_state))

    def test_faction_agent_matches_game_state_enabled_false_no_force_paths(self):
        """FactionManagementAgent.matches_game_state does NOT force selection for suggestions when enabled=False."""
        # Test that high forces (>= 500) don't trigger selection when enabled=False
        mock_state = Mock()
        mock_state.custom_campaign_state = {
            "faction_minigame": {
                "enabled": False,
                "suggestion_given": False,
                "strong_suggestion_given": False,
            }
        }
        mock_state.army_data = {
            "total_strength": 500
        }  # Should trigger suggestion, but disabled

        # Should return False - no force paths when disabled
        self.assertFalse(FactionManagementAgent.matches_game_state(mock_state))

    def test_faction_agent_matches_game_state_enabled_false_100_forces_no_suggestion(
        self,
    ):
        """FactionManagementAgent.matches_game_state does NOT force selection at 100 forces when enabled=False."""
        mock_state = Mock()
        mock_state.custom_campaign_state = {
            "faction_minigame": {
                "enabled": False,
                "suggestion_given": False,  # Suggestion not given, but still disabled
            }
        }
        mock_state.army_data = {"total_strength": 100}

        # Should return False - no force paths when disabled
        self.assertFalse(FactionManagementAgent.matches_game_state(mock_state))

    def test_faction_agent_matches_game_state_none_returns_false(self):
        """FactionManagementAgent.matches_game_state returns False when game_state is None."""
        self.assertFalse(FactionManagementAgent.matches_game_state(None))

    def test_faction_agent_matches_game_state_no_faction_minigame_returns_false(self):
        """FactionManagementAgent.matches_game_state returns False when faction_minigame missing."""
        mock_state = Mock()
        mock_state.custom_campaign_state = {}
        mock_state.army_data = {"total_strength": 5000}

        self.assertFalse(FactionManagementAgent.matches_game_state(mock_state))

    def test_faction_agent_matches_game_state_enabled_true_exactly_at_threshold(self):
        """FactionManagementAgent.matches_game_state returns True when enabled=True and forces exactly at threshold."""
        mock_state = self._create_mock_state_with_army_data(
            enabled=True, total_strength=FACTION_FORCE_THRESHOLD
        )

        self.assertTrue(FactionManagementAgent.matches_game_state(mock_state))

    def test_faction_agent_string_false_treated_as_disabled(self):
        """String 'false' should be treated as disabled (not truthy)."""
        # Use spec=[] to prevent auto-generation of faction_minigame attribute
        mock_state = Mock(spec=["custom_campaign_state", "army_data"])
        mock_state.custom_campaign_state = {"faction_minigame": {"enabled": "false"}}
        mock_state.army_data = {"total_strength": 5000}

        # String "false" is truthy in Python, but should be treated as False
        self.assertFalse(FactionManagementAgent.matches_game_state(mock_state))

    def test_faction_agent_string_true_treated_as_disabled(self):
        """String 'true' should be treated as disabled (only boolean True is valid)."""
        # Use spec=[] to prevent auto-generation of faction_minigame attribute
        mock_state = Mock(spec=["custom_campaign_state", "army_data"])
        mock_state.custom_campaign_state = {"faction_minigame": {"enabled": "true"}}
        mock_state.army_data = {"total_strength": 5000}

        # Only boolean True should enable, not string "true"
        self.assertFalse(FactionManagementAgent.matches_game_state(mock_state))

    def test_faction_agent_none_treated_as_disabled(self):
        """None value should be treated as disabled."""
        # Use spec=[] to prevent auto-generation of faction_minigame attribute
        mock_state = Mock(spec=["custom_campaign_state", "army_data"])
        mock_state.custom_campaign_state = {"faction_minigame": {"enabled": None}}
        mock_state.army_data = {"total_strength": 5000}

        self.assertFalse(FactionManagementAgent.matches_game_state(mock_state))

    def test_faction_agent_zero_treated_as_disabled(self):
        """Zero should be treated as disabled."""
        # Use spec=[] to prevent auto-generation of faction_minigame attribute
        mock_state = Mock(spec=["custom_campaign_state", "army_data"])
        mock_state.custom_campaign_state = {"faction_minigame": {"enabled": 0}}
        mock_state.army_data = {"total_strength": 5000}

        self.assertFalse(FactionManagementAgent.matches_game_state(mock_state))

    def test_detect_minigame_enabled_string_false_returns_false(self):
        """_detect_minigame_enabled should treat string 'false' as disabled."""
        # Use spec=[] to prevent auto-generation of faction_minigame attribute
        mock_state = Mock(spec=["custom_campaign_state", "user_settings"])
        mock_state.custom_campaign_state = {"faction_minigame": {"enabled": "false"}}
        mock_state.user_settings = {}

        agent = FactionManagementAgent(mock_state)
        self.assertFalse(agent._minigame_enabled)

    def test_detect_minigame_enabled_string_true_returns_false(self):
        """_detect_minigame_enabled should treat string 'true' as disabled."""
        # Use spec=[] to prevent auto-generation of faction_minigame attribute
        mock_state = Mock(spec=["custom_campaign_state", "user_settings"])
        mock_state.custom_campaign_state = {"faction_minigame": {"enabled": "true"}}
        mock_state.user_settings = {}

        agent = FactionManagementAgent(mock_state)
        self.assertFalse(agent._minigame_enabled)

    def test_detect_minigame_enabled_none_returns_false(self):
        """_detect_minigame_enabled should treat None as disabled."""
        # Use spec=[] to prevent auto-generation of faction_minigame attribute
        mock_state = Mock(spec=["custom_campaign_state", "user_settings"])
        mock_state.custom_campaign_state = {"faction_minigame": {"enabled": None}}
        mock_state.user_settings = {}

        agent = FactionManagementAgent(mock_state)
        self.assertFalse(agent._minigame_enabled)

    def test_detect_minigame_enabled_boolean_true_returns_true(self):
        """_detect_minigame_enabled should only return True for boolean True."""
        # Use spec=[] to prevent auto-generation of faction_minigame attribute
        mock_state = Mock(spec=["custom_campaign_state", "user_settings"])
        mock_state.custom_campaign_state = {"faction_minigame": {"enabled": True}}
        mock_state.user_settings = {}

        agent = FactionManagementAgent(mock_state)
        self.assertTrue(agent._minigame_enabled)

    def test_detect_minigame_enabled_boolean_false_returns_false(self):
        """_detect_minigame_enabled should return False for boolean False."""
        # Use spec=[] to prevent auto-generation of faction_minigame attribute
        mock_state = Mock(spec=["custom_campaign_state", "user_settings"])
        mock_state.custom_campaign_state = {"faction_minigame": {"enabled": False}}
        mock_state.user_settings = {}

        agent = FactionManagementAgent(mock_state)
        self.assertFalse(agent._minigame_enabled)


class TestFactionManagementAgentMatchesInput(unittest.TestCase):
    """Test cases for FactionManagementAgent.matches_input() behavior."""

    def _create_mock_state_with_army_data(self, enabled, total_strength):
        """Helper to create mock state with proper army_data structure."""

        class MockGameState:
            def __init__(self):
                self.custom_campaign_state = {"faction_minigame": {"enabled": enabled}}
                self.army_data = {"total_strength": total_strength}

        return MockGameState()

    def test_matches_input_returns_true_for_minigame_patterns(self):
        """Verify FACTION_MINIGAME_PATTERNS trigger even when disabled."""
        # Test with a minigame pattern
        mock_state = self._create_mock_state_with_army_data(
            enabled=False, total_strength=10
        )

        # Use a pattern that should match FACTION_MINIGAME_PATTERNS
        self.assertTrue(
            FactionManagementAgent.matches_input("faction minigame", mock_state)
        )
        self.assertTrue(
            FactionManagementAgent.matches_input("enable faction mode", mock_state)
        )

    def test_matches_input_enable_faction_minigame_command(self):
        """Enable command should match even when minigame is disabled."""
        self.assertTrue(
            FactionManagementAgent.matches_input("enable_faction_minigame", None)
        )

    def test_matches_input_requires_enabled_for_query_patterns(self):
        """Verify FACTION_QUERY_PATTERNS require enabled=True."""
        mock_state = self._create_mock_state_with_army_data(
            enabled=False, total_strength=5000
        )

        # Query patterns should not match when disabled
        # Note: "faction status" is in FACTION_MINIGAME_PATTERNS so it matches even when disabled
        # Use a pattern that's only in FACTION_QUERY_PATTERNS
        self.assertFalse(
            FactionManagementAgent.matches_input("army status", mock_state)
        )
        self.assertFalse(
            FactionManagementAgent.matches_input("recruit soldiers", mock_state)
        )

    def test_matches_input_returns_false_when_disabled_and_no_minigame_pattern(self):
        """Verify returns False when disabled and no minigame pattern."""
        mock_state = self._create_mock_state_with_army_data(
            enabled=False, total_strength=5000
        )

        self.assertFalse(
            FactionManagementAgent.matches_input("check my inventory", mock_state)
        )
        self.assertFalse(
            FactionManagementAgent.matches_input("attack the goblin", mock_state)
        )

    def test_matches_input_case_insensitive(self):
        """Verify pattern matching is case-insensitive."""
        mock_state = self._create_mock_state_with_army_data(
            enabled=True, total_strength=5000
        )

        # Should match regardless of case
        self.assertTrue(FactionManagementAgent.matches_input("ARMY STATUS", mock_state))
        self.assertTrue(
            FactionManagementAgent.matches_input("Faction Status", mock_state)
        )
        self.assertTrue(
            FactionManagementAgent.matches_input("faction status", mock_state)
        )

    def test_matches_input_handles_none_game_state(self):
        """Verify handles None game_state gracefully."""
        # Minigame patterns should still work with None game_state
        self.assertTrue(FactionManagementAgent.matches_input("faction minigame", None))

        # Query patterns should return False with None game_state
        self.assertFalse(FactionManagementAgent.matches_input("army status", None))

    def test_operational_patterns_blocked_when_disabled(self):
        """Verify operational patterns are blocked when minigame is disabled.

        BUG FIX: When faction_minigame.enabled=False, operational commands
        like "deploy spies", "assault", "skirmish" should NOT trigger the
        faction agent. Only explicit enablement patterns like "enable faction
        mode" should bypass the enabled check.
        """
        mock_state = self._create_mock_state_with_army_data(
            enabled=False, total_strength=5000
        )

        # These operational patterns should NOT match when disabled
        self.assertFalse(
            FactionManagementAgent.matches_input(
                "deploy spies to the north", mock_state
            ),
            "deploy spies should NOT match when minigame is disabled",
        )
        self.assertFalse(
            FactionManagementAgent.matches_input(
                "assault the enemy fortress", mock_state
            ),
            "assault should NOT match when minigame is disabled",
        )
        self.assertFalse(
            FactionManagementAgent.matches_input("skirmish with raiders", mock_state),
            "skirmish should NOT match when minigame is disabled",
        )
        self.assertFalse(
            FactionManagementAgent.matches_input("pillage the village", mock_state),
            "pillage should NOT match when minigame is disabled",
        )
        self.assertFalse(
            FactionManagementAgent.matches_input("intel report on enemies", mock_state),
            "intel report should NOT match when minigame is disabled",
        )

        # BUT enablement patterns SHOULD still match (to allow users to enable)
        self.assertTrue(
            FactionManagementAgent.matches_input("enable faction mode", mock_state),
            "enable faction mode SHOULD match to allow enabling the feature",
        )


class TestFactionManagementAgentEnablementLogic(unittest.TestCase):
    """Test cases for FactionManagementAgent enablement logic requiring three conditions."""

    def _create_mock_state(
        self, campaign_enabled, total_strength, user_setting_enabled=True
    ):
        """Helper to create mock state with faction settings and user settings."""

        class MockGameState:
            def __init__(self):
                self.custom_campaign_state = {
                    "faction_minigame": {"enabled": campaign_enabled}
                }
                self.army_data = {"total_strength": total_strength}
                # Store user settings in game state for agent access
                self.user_settings = {"faction_minigame_enabled": user_setting_enabled}

        return MockGameState()

    def test_minigame_disabled_when_user_setting_off(self):
        """Verify minigame disabled when user setting is off, even if campaign setting is on."""
        mock_state = self._create_mock_state(
            campaign_enabled=True, total_strength=500, user_setting_enabled=False
        )
        agent = FactionManagementAgent(game_state=mock_state)

        self.assertFalse(
            agent.minigame_enabled,
            "Minigame should be disabled when user setting is off",
        )

    def test_minigame_disabled_when_campaign_setting_off(self):
        """Verify minigame disabled when campaign setting is off, even if user setting is on."""
        mock_state = self._create_mock_state(
            campaign_enabled=False, total_strength=500, user_setting_enabled=True
        )
        agent = FactionManagementAgent(game_state=mock_state)

        self.assertFalse(
            agent.minigame_enabled,
            "Minigame should be disabled when campaign setting is off",
        )

    def test_minigame_enabled_when_units_below_threshold(self):
        """Verify minigame enabled when campaign is on, even if units < 100."""
        mock_state = self._create_mock_state(
            campaign_enabled=True,
            total_strength=50,  # Below threshold
            user_setting_enabled=True,
        )
        agent = FactionManagementAgent(game_state=mock_state)

        self.assertTrue(
            agent.minigame_enabled,
            "Minigame should be enabled when campaign is on regardless of units",
        )

    def test_minigame_enabled_when_all_requirements_met(self):
        """Verify minigame enabled when user setting ON, campaign setting ON, and units >= 100."""
        mock_state = self._create_mock_state(
            campaign_enabled=True,
            total_strength=100,  # At threshold
            user_setting_enabled=True,
        )
        agent = FactionManagementAgent(game_state=mock_state)

        self.assertTrue(
            agent.minigame_enabled,
            "Minigame should be enabled when all requirements are met",
        )

    def test_minigame_enabled_when_units_above_threshold(self):
        """Verify minigame enabled when units > 100 and both settings on."""
        mock_state = self._create_mock_state(
            campaign_enabled=True,
            total_strength=500,  # Above threshold
            user_setting_enabled=True,
        )
        agent = FactionManagementAgent(game_state=mock_state)

        self.assertTrue(
            agent.minigame_enabled,
            "Minigame should be enabled when units > 100 and both settings on",
        )

    def test_minigame_enabled_when_user_settings_missing(self):
        """Verify minigame enabled when user_settings missing but campaign enabled (backwards compat)."""

        class MockGameStateNoUserSettings:
            def __init__(self):
                self.custom_campaign_state = {"faction_minigame": {"enabled": True}}
                self.army_data = {"total_strength": 500}
                # No user_settings attribute

        mock_state = MockGameStateNoUserSettings()
        agent = FactionManagementAgent(game_state=mock_state)

        self.assertTrue(
            agent.minigame_enabled,
            "Minigame should be enabled when campaign is on even if user_settings missing",
        )

    def test_minigame_disabled_when_dict_game_state_user_setting_off(self):
        """Dict game_state should honor embedded user_settings override."""
        game_state = {
            "custom_campaign_state": {"faction_minigame": {"enabled": True}},
            "user_settings": {"faction_minigame_enabled": False},
        }
        agent = FactionManagementAgent(game_state=game_state)

        self.assertFalse(
            agent.minigame_enabled,
            "Minigame should be disabled when dict user_settings disables it",
        )

    def test_minigame_enabled_with_data_dict_structure(self):
        """Verify minigame works with game_state.data.game_state.army_data structure."""

        class MockGameStateWithDataDict:
            def __init__(self):
                self.user_settings = {"faction_minigame_enabled": True}
                self.data = {
                    "game_state": {
                        "faction_minigame": {"enabled": True},
                        "army_data": {"total_strength": 150},
                    }
                }

        mock_state = MockGameStateWithDataDict()
        agent = FactionManagementAgent(game_state=mock_state)

        self.assertTrue(
            agent.minigame_enabled,
            "Minigame should work with data.game_state structure",
        )

    def test_minigame_enabled_when_army_data_missing(self):
        """Verify minigame enabled when campaign is on even if army_data missing."""

        class MockGameStateNoArmyData:
            def __init__(self):
                self.user_settings = {"faction_minigame_enabled": True}
                self.custom_campaign_state = {"faction_minigame": {"enabled": True}}
                # No army_data attribute

        mock_state = MockGameStateNoArmyData()
        agent = FactionManagementAgent(game_state=mock_state)

        self.assertTrue(
            agent.minigame_enabled,
            "Minigame should be enabled when campaign is on even if army_data missing",
        )

    def test_minigame_enabled_when_army_data_not_dict(self):
        """Verify minigame enabled when campaign is on even if army_data is not a dict."""

        class MockGameStateInvalidArmyData:
            def __init__(self):
                self.user_settings = {"faction_minigame_enabled": True}
                self.custom_campaign_state = {"faction_minigame": {"enabled": True}}
                self.army_data = "not a dict"  # Invalid type

        mock_state = MockGameStateInvalidArmyData()
        agent = FactionManagementAgent(game_state=mock_state)

        self.assertTrue(
            agent.minigame_enabled,
            "Minigame should be enabled when campaign is on even if army_data is not a dict",
        )


class TestFactionManagementAgentBuildInstructions(unittest.TestCase):
    """Test cases for FactionManagementAgent.build_system_instructions()."""

    def _create_mock_state_with_minigame(self, enabled):
        """Helper to create mock state with minigame enabled/disabled."""

        class MockGameState:
            def __init__(self):
                self.custom_campaign_state = {"faction_minigame": {"enabled": enabled}}
                self.army_data = {"total_strength": 5000}
                # Add user_settings to pass new enablement logic
                self.user_settings = {"faction_minigame_enabled": True}

        return MockGameState()

    @patch("mvp_site.agents._load_instruction_file")
    def test_build_instructions_includes_minigame_prompt_when_enabled(self, mock_load):
        """Verify faction minigame prompt included when enabled=True."""
        mock_load.return_value = "Faction Minigame Prompt"
        mock_state = self._create_mock_state_with_minigame(enabled=True)
        agent = FactionManagementAgent(game_state=mock_state)

        agent.build_system_instructions()

        # Should have called _load_instruction_file for faction minigame
        minigame_calls = [
            call
            for call in mock_load.call_args_list
            if len(call[0]) > 0 and call[0][0] == constants.PROMPT_TYPE_FACTION_MINIGAME
        ]
        self.assertGreater(len(minigame_calls), 0)

    @patch("mvp_site.agents._load_instruction_file")
    def test_build_instructions_excludes_minigame_prompt_when_disabled(self, mock_load):
        """Verify faction minigame prompt excluded when enabled=False."""
        mock_state = self._create_mock_state_with_minigame(enabled=False)
        agent = FactionManagementAgent(game_state=mock_state)

        agent.build_system_instructions()

        # Should not have called _load_instruction_file for faction minigame
        minigame_calls = [
            call
            for call in mock_load.call_args_list
            if len(call[0]) > 0 and call[0][0] == constants.PROMPT_TYPE_FACTION_MINIGAME
        ]
        self.assertEqual(len(minigame_calls), 0)

    @patch("mvp_site.agents._load_instruction_file")
    def test_build_instructions_includes_minigame_prompt_when_forced(self, mock_load):
        """Verify faction minigame prompt included when force_minigame_prompt=True."""
        mock_load.return_value = "Faction Minigame Prompt"
        mock_state = self._create_mock_state_with_minigame(enabled=False)
        agent = FactionManagementAgent(
            game_state=mock_state,
            force_minigame_prompt=True,
        )

        agent.build_system_instructions()

        minigame_calls = [
            call
            for call in mock_load.call_args_list
            if len(call[0]) > 0 and call[0][0] == constants.PROMPT_TYPE_FACTION_MINIGAME
        ]
        self.assertGreater(len(minigame_calls), 0)

    @patch("mvp_site.agents._load_instruction_file")
    def test_build_instructions_includes_required_prompts(self, mock_load):
        """Verify all required prompts are included."""
        # Mock must return strings for all calls
        mock_load.return_value = "Mock prompt content"
        mock_state = self._create_mock_state_with_minigame(enabled=True)
        agent = FactionManagementAgent(game_state=mock_state)

        instructions = agent.build_system_instructions()

        # Instructions should be a string (finalized)
        self.assertIsInstance(instructions, str)
        self.assertGreater(len(instructions), 0)

    @patch("mvp_site.agents._load_instruction_file")
    def test_build_instructions_prompt_order(self, mock_load):
        """Verify prompts are in correct order."""
        # Mock must return strings for all calls
        mock_load.return_value = "Mock prompt content"
        mock_state = self._create_mock_state_with_minigame(enabled=True)
        agent = FactionManagementAgent(game_state=mock_state)

        instructions = agent.build_system_instructions()

        # Basic check that instructions are generated
        self.assertIsInstance(instructions, str)
        self.assertGreater(len(instructions), 0)


class TestGetAgentForInputCampaignUpgrade(unittest.TestCase):
    """Test cases for CampaignUpgradeAgent routing in get_agent_for_input()."""

    def _create_mock_state_with_upgrade(self, upgrade_type: str | None):
        """Helper to create mock state with upgrade available."""
        mock_state = Mock()
        mock_state.get_pending_upgrade_type = Mock(return_value=upgrade_type)
        mock_state.is_campaign_upgrade_available = Mock(
            return_value=upgrade_type is not None
        )
        mock_state.custom_campaign_state = {}
        mock_state.player_character_data = {"name": "Test", "class": "Fighter"}
        return mock_state

    @patch("mvp_site.agents.CampaignUpgradeAgent.matches_game_state")
    def test_get_agent_campaign_upgrade_state_based(self, mock_matches):
        """Verify CampaignUpgradeAgent selected when upgrade available (priority 3)."""
        mock_matches.return_value = True
        mock_state = self._create_mock_state_with_upgrade("divine")

        agent, _ = get_agent_for_input("continue story", mock_state)

        self.assertIsInstance(agent, CampaignUpgradeAgent)

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    @patch("mvp_site.agents.CampaignUpgradeAgent.matches_game_state")
    def test_get_agent_campaign_upgrade_semantic_intent(
        self, mock_matches, mock_classify
    ):
        """Verify CampaignUpgradeAgent selected via semantic classifier."""
        mock_classify.return_value = (constants.MODE_CAMPAIGN_UPGRADE, 0.85)
        mock_matches.return_value = False  # State doesn't match, but semantic does
        mock_state = self._create_mock_state_with_upgrade(None)

        agent, _ = get_agent_for_input("i want to become a god", mock_state)

        self.assertIsInstance(agent, CampaignUpgradeAgent)

    @patch("mvp_site.agents.CampaignUpgradeAgent.matches_game_state")
    def test_get_agent_rejects_campaign_upgrade_explicit_mode(self, mock_matches):
        """Verify explicit mode='campaign_upgrade' is rejected."""
        mock_matches.return_value = False
        mock_state = self._create_mock_state_with_upgrade(None)

        agent, _ = get_agent_for_input(
            "continue", mock_state, mode=constants.MODE_CAMPAIGN_UPGRADE
        )

        # Internal mode cannot be forced
        self.assertIsInstance(agent, StoryModeAgent)

    @patch("mvp_site.agents.CampaignUpgradeAgent.matches_game_state")
    @patch("mvp_site.agents.CharacterCreationAgent.matches_game_state")
    def test_get_agent_campaign_upgrade_priority_over_character_creation(
        self, mock_char, mock_upgrade
    ):
        """Verify CampaignUpgradeAgent takes precedence over CharacterCreationAgent."""
        mock_upgrade.return_value = True
        mock_char.return_value = True
        mock_state = self._create_mock_state_with_upgrade("divine")

        agent, _ = get_agent_for_input("continue", mock_state)

        self.assertIsInstance(agent, CampaignUpgradeAgent)
        self.assertNotIsInstance(agent, CharacterCreationAgent)


class TestGetAgentForInputFaction(unittest.TestCase):
    """Test cases for FactionManagementAgent routing in get_agent_for_input()."""

    def _create_mock_state_with_faction(self, enabled, total_strength):
        """Helper to create mock state with faction minigame."""

        class MockGameState:
            def __init__(self):
                self.custom_campaign_state = {"faction_minigame": {"enabled": enabled}}
                self.army_data = {"total_strength": total_strength}
                self.player_character_data = {"name": "Test", "class": "Fighter"}
                # Add method needed by get_agent_for_input
                self.is_campaign_upgrade_available = Mock(return_value=False)

        return MockGameState()

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    @patch("mvp_site.agents.FactionManagementAgent.matches_game_state")
    def test_get_agent_faction_state_based_defers_to_classifier(
        self, mock_matches, mock_classify
    ):
        """Verify FactionManagementAgent NOT auto-selected when minigame enabled.

        PR #4084 changed behavior: faction minigame being enabled no longer FORCES
        FactionManagementAgent. Instead, the classifier routes based on user intent.
        This prevents all inputs being routed to faction agent (exploration, dialog, etc).
        """
        mock_matches.return_value = True
        mock_classify.return_value = (
            constants.MODE_CHARACTER,
            0.8,
        )  # Character (story) intent
        mock_state = self._create_mock_state_with_faction(
            enabled=True, total_strength=5000
        )

        agent, _ = get_agent_for_input("continue story", mock_state)

        # With classifier-first routing, character intent → StoryModeAgent, not FactionManagementAgent
        self.assertIsInstance(agent, StoryModeAgent)

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    @patch("mvp_site.agents.FactionManagementAgent.matches_game_state")
    def test_get_agent_faction_semantic_intent(self, mock_matches, mock_classify):
        """Verify FactionManagementAgent selected via semantic classifier."""
        mock_classify.return_value = (constants.MODE_FACTION, 0.85)
        mock_matches.return_value = False  # State doesn't match, but semantic does
        mock_state = self._create_mock_state_with_faction(
            enabled=False, total_strength=10
        )

        agent, _ = get_agent_for_input("check my faction status", mock_state)

        self.assertIsInstance(agent, FactionManagementAgent)

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_get_agent_faction_enable_uses_classifier_not_keywords(self, mock_classify):
        """Verify enable text does not bypass classifier via keyword routing."""
        mock_classify.return_value = (constants.MODE_CHARACTER, 0.2)
        mock_state = self._create_mock_state_with_faction(
            enabled=False, total_strength=10
        )

        agent, metadata = get_agent_for_input("enable faction minigame", mock_state)

        self.assertIsInstance(agent, StoryModeAgent)
        self.assertEqual(metadata["classifier_source"], "semantic_intent")

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_get_agent_faction_semantic_intent_forces_prompt_when_disabled(
        self, mock_classify
    ):
        """Verify semantic faction intent forces minigame prompt when disabled."""
        mock_classify.return_value = (constants.MODE_FACTION, 0.9)
        mock_state = self._create_mock_state_with_faction(
            enabled=False, total_strength=10
        )

        agent, _ = get_agent_for_input("check my faction status", mock_state)

        self.assertIsInstance(agent, FactionManagementAgent)
        self.assertTrue(agent._force_minigame_prompt)

    @patch("mvp_site.agents.FactionManagementAgent.matches_game_state")
    def test_get_agent_rejects_faction_explicit_mode(self, mock_matches):
        """Verify explicit mode='faction' is rejected."""
        mock_matches.return_value = False
        mock_state = self._create_mock_state_with_faction(
            enabled=False, total_strength=10
        )

        agent, _ = get_agent_for_input(
            "continue", mock_state, mode=constants.MODE_FACTION
        )

        # Internal mode cannot be forced
        self.assertIsInstance(agent, StoryModeAgent)

    @patch("mvp_site.agents.FactionManagementAgent.matches_game_state")
    @patch("mvp_site.agents.CharacterCreationAgent.matches_game_state")
    def test_get_agent_faction_priority_after_character_creation(
        self, mock_char, mock_faction
    ):
        """Verify FactionManagementAgent doesn't interrupt character creation."""
        mock_char.return_value = True
        mock_faction.return_value = True
        mock_state = self._create_mock_state_with_faction(
            enabled=True, total_strength=5000
        )

        agent, _ = get_agent_for_input("continue", mock_state)

        # Character creation should take precedence
        self.assertIsInstance(agent, CharacterCreationAgent)
        self.assertNotIsInstance(agent, FactionManagementAgent)


class TestStoryModeAgentPromptFixes(unittest.TestCase):
    """
    Regression tests for PR #3750:
    1. StoryModeAgent must not mutate the input selected_prompts list.
    2. StoryModeAgent must ensure PROMPT_TYPE_NARRATIVE is present (for default campaigns).
    """

    def test_story_mode_agent_prompt_mutation(self):
        """Verify StoryModeAgent does not mutate the input prompts list."""
        mock_game_state = MagicMock()
        # Mock PromptBuilder to avoid filesystem access during tests
        with patch("mvp_site.agents.PromptBuilder"):
            agent = StoryModeAgent(mock_game_state)

            # Case 1: Empty list passed
            input_prompts = []
            agent.build_system_instruction_parts(selected_prompts=input_prompts)

            # Input list should remain empty (no mutation)
            self.assertEqual(
                input_prompts,
                [],
                "Input list was mutated! StoryModeAgent must use a local copy.",
            )

            # Verify the builder received the modified list (with NARRATIVE)
            mock_builder_instance = agent._prompt_builder
            call_args = mock_builder_instance.add_selected_prompt_instructions.call_args
            passed_prompts = call_args[0][1]
            self.assertIn(constants.PROMPT_TYPE_NARRATIVE, passed_prompts)
            self.assertIsNot(
                passed_prompts,
                input_prompts,
                "Builder received the original list reference!",
            )

    def test_story_mode_agent_prompt_injection(self):
        """Verify Narrative prompt injection logic for StoryModeAgent."""
        mock_game_state = MagicMock()
        with patch("mvp_site.agents.PromptBuilder"):
            agent = StoryModeAgent(mock_game_state)

            # Case 1: None -> Narrative added
            agent.build_system_instruction_parts(selected_prompts=None)
            mock_builder_instance = agent._prompt_builder
            call_args = mock_builder_instance.add_selected_prompt_instructions.call_args
            passed_prompts = call_args[0][1]
            self.assertIn(constants.PROMPT_TYPE_NARRATIVE, passed_prompts)

            # Case 2: Mechanics only -> Narrative ADDED (mandatory for StoryModeAgent)
            mechanics_list = [constants.PROMPT_TYPE_MECHANICS]
            agent.build_system_instruction_parts(selected_prompts=mechanics_list)
            call_args = mock_builder_instance.add_selected_prompt_instructions.call_args
            passed_prompts = call_args[0][1]
            self.assertIn(constants.PROMPT_TYPE_NARRATIVE, passed_prompts)
            self.assertIn(constants.PROMPT_TYPE_MECHANICS, passed_prompts)


class TestAgentRequiresActionResolution(unittest.TestCase):
    """
    Test the requires_action_resolution property for all agent types.

    This property determines whether the agent requires action_resolution
    in the LLM response for audit trail purposes.

    - Story/Combat modes: require action_resolution (True)
    - God Mode, Character Creation, Planning, Info, Rewards, Campaign Upgrade: exempt (False)
    """

    def test_story_mode_agent_requires_action_resolution(self):
        """StoryModeAgent requires action_resolution for gameplay audit trails."""
        agent = StoryModeAgent(game_state=None)
        self.assertTrue(agent.requires_action_resolution)

    def test_combat_agent_requires_action_resolution(self):
        """CombatAgent requires action_resolution for combat audit trails."""
        mock_gs = create_mock_game_state(in_combat=True)
        agent = CombatAgent(game_state=mock_gs)
        self.assertTrue(agent.requires_action_resolution)

    def test_god_mode_agent_exempt_from_action_resolution(self):
        """GodModeAgent is administrative and does not require action_resolution."""
        agent = GodModeAgent(game_state=None)
        self.assertFalse(agent.requires_action_resolution)

    def test_character_creation_agent_exempt_from_action_resolution(self):
        """CharacterCreationAgent is setup phase and does not require action_resolution."""
        agent = CharacterCreationAgent(game_state=None)
        self.assertFalse(agent.requires_action_resolution)

    def test_planning_agent_exempt_from_action_resolution(self):
        """PlanningAgent (Think Mode) is for planning and does not require action_resolution."""
        agent = PlanningAgent(game_state=None)
        self.assertFalse(agent.requires_action_resolution)

    def test_info_agent_exempt_from_action_resolution(self):
        """InfoAgent is for data retrieval and does not require action_resolution."""
        agent = InfoAgent(game_state=None)
        self.assertFalse(agent.requires_action_resolution)

    def test_rewards_agent_exempt_from_action_resolution(self):
        """RewardsAgent is administrative and does not require action_resolution."""
        agent = RewardsAgent(game_state=None)
        self.assertFalse(agent.requires_action_resolution)

    def test_campaign_upgrade_agent_exempt_from_action_resolution(self):
        """CampaignUpgradeAgent (ascension ceremonies) does not require action_resolution."""
        mock_gs = create_mock_game_state()
        agent = CampaignUpgradeAgent(game_state=mock_gs)
        self.assertFalse(agent.requires_action_resolution)

    def test_base_agent_default_requires_action_resolution(self):
        """BaseAgent default is True (require action_resolution)."""
        # StoryModeAgent inherits from BaseAgent and doesn't override, so it should be True
        agent = StoryModeAgent(game_state=None)
        # Verify it's inherited from BaseAgent correctly
        self.assertTrue(hasattr(agent, "requires_action_resolution"))
        self.assertTrue(agent.requires_action_resolution)


class TestSpicyModeAgentPrompts(unittest.TestCase):
    """Test SpicyModeAgent prompt loading to ensure NARRATIVE is not double-loaded."""

    def test_spicy_mode_agent_loads_spicy_mode_prompt_and_narrative(self):
        """
        SpicyModeAgent should load SPICY_MODE prompt (and narrative for living world support).
        """
        mock_gs = create_mock_game_state()
        # Configure mock to return strings instead of Mock objects for prompt building
        mock_gs.get_character_identity_block.return_value = ""
        mock_gs.god_mode_directives = None
        agent = SpicyModeAgent(game_state=mock_gs)

        # Build system instructions
        all_content = agent.build_system_instructions()

        # Verify SPICY_MODE content is present (check for unique marker from spicy_mode_instruction.md)
        self.assertIn(
            "Spicy Mode",
            all_content,
            "SpicyModeAgent should load SPICY_MODE instruction",
        )

        # Verify NARRATIVE content is present (required for living world integration)
        self.assertIn(
            "# Narrative Directives",
            all_content,
            "SpicyModeAgent should load NARRATIVE instruction",
        )


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Unit tests for `structured_fields_utils.extract_structured_fields`."""

import unittest
from unittest.mock import Mock

from mvp_site import constants, structured_fields_utils
from mvp_site.llm_response import LLMResponse
from mvp_site.narrative_response_schema import NarrativeResponse
from mvp_site.structured_fields_utils import (
    _audit_trim_state_update,
    _build_state_updates_audit_subset,
)


class TestStructuredFieldsUtils(unittest.TestCase):
    """Test cases for structured_fields_utils.extract_structured_fields function."""

    def setUp(self):
        """Set up test fixtures for each test."""
        # Sample structured response data
        self.sample_structured_data = {
            "session_header": "Turn 3 - Combat Phase\nHP: 25/30 | AC: 16 | Status: Engaged",
            "planning_block": "What would you like to do next?\n1. Attack with sword\n2. Cast spell\n3. Use item\n4. Retreat",
            "dice_rolls": [
                "Initiative: d20+2 = 15",
                "Attack roll: d20+5 = 18",
                "Damage: 1d8+3 = 7",
            ],
            "resources": "HP: 25/30, SP: 8/12, Gold: 150, Arrows: 24",
            "debug_info": {
                "turn_number": 3,
                "combat_active": True,
                "dm_notes": "Player chose aggressive approach",
                "dice_rolls": ["d20+5", "1d8+3"],
                "enemy_hp": 12,
            },
        }

        # Create a mock structured response object
        self.mock_structured_response = Mock(spec=NarrativeResponse)
        self.mock_structured_response.session_header = self.sample_structured_data[
            "session_header"
        ]
        self.mock_structured_response.planning_block = self.sample_structured_data[
            "planning_block"
        ]
        self.mock_structured_response.dice_rolls = self.sample_structured_data[
            "dice_rolls"
        ]
        self.mock_structured_response.resources = self.sample_structured_data[
            "resources"
        ]
        self.mock_structured_response.debug_info = self.sample_structured_data[
            "debug_info"
        ]
        self.mock_structured_response.directives = {}

    def test_extract_structured_fields_with_full_data(self):
        """Test extraction with complete structured response data."""
        # Create a mock LLMResponse with structured_response
        mock_gemini_response = Mock(spec=LLMResponse, agent_mode=constants.MODE_CHARACTER)
        mock_gemini_response.structured_response = self.mock_structured_response

        # Extract structured fields
        result = structured_fields_utils.extract_structured_fields(mock_gemini_response)

        # Verify all fields are extracted correctly
        assert (
            result[constants.FIELD_SESSION_HEADER]
            == self.sample_structured_data["session_header"]
        )
        assert (
            result[constants.FIELD_PLANNING_BLOCK]
            == self.sample_structured_data["planning_block"]
        )
        assert (
            result[constants.FIELD_DICE_ROLLS]
            == self.sample_structured_data["dice_rolls"]
        )
        assert (
            result[constants.FIELD_RESOURCES]
            == self.sample_structured_data["resources"]
        )
        assert (
            result[constants.FIELD_DEBUG_INFO]
            == self.sample_structured_data["debug_info"]
        )

    def test_extract_structured_fields_with_empty_fields(self):
        """Test extraction with empty structured response fields."""
        # Create a mock structured response with empty fields
        mock_structured_response = Mock(spec=NarrativeResponse)
        mock_structured_response.session_header = ""
        mock_structured_response.planning_block = ""
        mock_structured_response.dice_rolls = []
        mock_structured_response.resources = ""
        mock_structured_response.debug_info = {}
        mock_structured_response.directives = {}

        mock_gemini_response = Mock(spec=LLMResponse, agent_mode=constants.MODE_CHARACTER)
        mock_gemini_response.structured_response = mock_structured_response

        # Extract structured fields
        result = structured_fields_utils.extract_structured_fields(mock_gemini_response)

        # Verify all fields are empty but present
        assert result[constants.FIELD_SESSION_HEADER] == ""
        assert result[constants.FIELD_PLANNING_BLOCK] == ""
        assert result[constants.FIELD_DICE_ROLLS] == []
        assert result[constants.FIELD_RESOURCES] == ""
        assert result[constants.FIELD_DEBUG_INFO] == {}

    def test_extract_structured_fields_with_missing_attributes(self):
        """Test extraction when structured response lacks some attributes."""
        # Create a mock structured response with missing attributes
        mock_structured_response = Mock(spec=NarrativeResponse)
        mock_structured_response.session_header = "Available header"
        mock_structured_response.planning_block = "Available planning"
        # dice_rolls, resources, debug_info are missing (will use getattr default)

        mock_gemini_response = Mock(spec=LLMResponse, agent_mode=constants.MODE_CHARACTER)
        mock_gemini_response.structured_response = mock_structured_response

        # Extract structured fields
        result = structured_fields_utils.extract_structured_fields(mock_gemini_response)

        # Verify available fields are extracted, missing ones default to empty
        assert result[constants.FIELD_SESSION_HEADER] == "Available header"
        assert result[constants.FIELD_PLANNING_BLOCK] == "Available planning"
        assert result[constants.FIELD_DICE_ROLLS] == []  # Default empty list
        assert result[constants.FIELD_RESOURCES] == ""  # Default empty string
        assert result[constants.FIELD_DEBUG_INFO] == {}  # Default empty dict

    def test_extract_structured_fields_with_no_structured_response(self):
        """Test extraction when LLMResponse has no structured_response."""
        # Create a mock LLMResponse without structured_response
        mock_gemini_response = Mock(spec=LLMResponse, agent_mode=constants.MODE_CHARACTER)
        mock_gemini_response.structured_response = None

        # Extract structured fields
        result = structured_fields_utils.extract_structured_fields(mock_gemini_response)

        # Verify result is empty dict
        assert result == {}

    def test_extract_structured_fields_with_none_values(self):
        """Test extraction when structured response has None values."""
        # Create a mock structured response with None values
        mock_structured_response = Mock(spec=NarrativeResponse)
        mock_structured_response.session_header = None
        mock_structured_response.planning_block = None
        mock_structured_response.dice_rolls = None
        mock_structured_response.resources = None
        mock_structured_response.debug_info = None
        mock_structured_response.directives = None

        mock_gemini_response = Mock(spec=LLMResponse, agent_mode=constants.MODE_CHARACTER)
        mock_gemini_response.structured_response = mock_structured_response

        # Extract structured fields
        result = structured_fields_utils.extract_structured_fields(mock_gemini_response)

        # Verify all fields use defaults when None
        assert result[constants.FIELD_SESSION_HEADER] == ""
        assert result[constants.FIELD_PLANNING_BLOCK] == ""
        assert result[constants.FIELD_DICE_ROLLS] == []
        assert result[constants.FIELD_RESOURCES] == ""
        assert result[constants.FIELD_DEBUG_INFO] == {}
        assert result[constants.FIELD_DIRECTIVES] == {}

    def test_extract_structured_fields_constants_mapping(self):
        """Test that function uses correct constants for field names."""
        # Create a mock response with data
        mock_structured_response = Mock(spec=NarrativeResponse)
        mock_structured_response.session_header = "Test session"
        mock_structured_response.planning_block = "Test planning"
        mock_structured_response.dice_rolls = ["Test roll"]
        mock_structured_response.resources = "Test resources"
        mock_structured_response.debug_info = {"test": "data"}
        mock_structured_response.directives = {}

        mock_gemini_response = Mock(spec=LLMResponse, agent_mode=constants.MODE_CHARACTER)
        mock_gemini_response.structured_response = mock_structured_response

        # Extract structured fields
        result = structured_fields_utils.extract_structured_fields(mock_gemini_response)

        # Verify all constants are used as keys
        # Note: world_events is only included when state_updates.world_events exists
        # action_resolution and outcome_resolution are always included (even if empty) for audit trail
        expected_keys = {
            constants.FIELD_SESSION_HEADER,
            constants.FIELD_PLANNING_BLOCK,
            constants.FIELD_DICE_ROLLS,
            constants.FIELD_DICE_AUDIT_EVENTS,
            constants.FIELD_RESOURCES,
            constants.FIELD_DEBUG_INFO,
            constants.FIELD_GOD_MODE_RESPONSE,
            constants.FIELD_DIRECTIVES,
            "action_resolution",
            "outcome_resolution",
        }
        assert set(result.keys()) == expected_keys

    def test_extract_structured_fields_with_complex_debug_info(self):
        """Test extraction with complex debug info structure."""
        complex_debug_info = {
            "turn_number": 5,
            "combat_active": True,
            "dm_notes": "Player used clever strategy",
            "dice_rolls": ["d20+3", "2d6+2"],
            "enemy_status": {
                "goblin_1": {"hp": 8, "status": "wounded"},
                "goblin_2": {"hp": 12, "status": "healthy"},
            },
            "environmental_factors": ["heavy_rain", "difficult_terrain"],
        }

        mock_structured_response = Mock(spec=NarrativeResponse)
        mock_structured_response.session_header = "Complex Combat Turn"
        mock_structured_response.planning_block = "Multiple options available"
        mock_structured_response.dice_rolls = [
            "Attack: d20+3 = 16",
            "Damage: 2d6+2 = 8",
        ]
        mock_structured_response.resources = "HP: 30/30, SP: 15/20"
        mock_structured_response.debug_info = complex_debug_info
        mock_structured_response.directives = {}

        mock_gemini_response = Mock(spec=LLMResponse, agent_mode=constants.MODE_CHARACTER)
        mock_gemini_response.structured_response = mock_structured_response

        # Extract structured fields
        result = structured_fields_utils.extract_structured_fields(mock_gemini_response)

        # Verify complex debug info is preserved
        assert result[constants.FIELD_DEBUG_INFO] == complex_debug_info
        assert result[constants.FIELD_DEBUG_INFO]["enemy_status"]["goblin_1"]["hp"] == 8
        assert result[constants.FIELD_DEBUG_INFO]["environmental_factors"] == [
            "heavy_rain",
            "difficult_terrain",
        ]

    def test_extract_structured_fields_with_long_text_fields(self):
        """Test extraction with longer text content."""
        long_session_header = """Turn 7 - Dungeon Exploration
=====================================
Current Location: Ancient Temple - Main Chamber
Party Status: All members healthy
Light Sources: 2 torches remaining (30 minutes)
Detected Threats: None visible
Recent Actions: Successfully disarmed pressure plate trap
Next Objective: Investigate the glowing altar"""

        long_planning_block = """The ancient chamber holds many secrets. What would you like to do?

1. Approach the glowing altar carefully
2. Search the walls for hidden passages
3. Cast Detect Magic on the altar
4. Have the rogue check for additional traps
5. Examine the hieroglyphs on the walls
6. Rest and tend to wounds before proceeding
7. Retreat to the previous chamber
8. Use a different approach (describe your action)"""

        mock_structured_response = Mock(spec=NarrativeResponse)
        mock_structured_response.session_header = long_session_header
        mock_structured_response.planning_block = long_planning_block
        mock_structured_response.dice_rolls = [
            "Perception: d20+4 = 18",
            "Investigation: d20+2 = 14",
        ]
        mock_structured_response.resources = "HP: 28/30, SP: 12/15, Torch time: 30 min"
        mock_structured_response.debug_info = {
            "location": "temple_chamber",
            "trap_disarmed": True,
        }
        mock_structured_response.directives = {}

        mock_gemini_response = Mock(spec=LLMResponse, agent_mode=constants.MODE_CHARACTER)
        mock_gemini_response.structured_response = mock_structured_response

        # Extract structured fields
        result = structured_fields_utils.extract_structured_fields(mock_gemini_response)

        # Verify long text fields are preserved
        assert result[constants.FIELD_SESSION_HEADER] == long_session_header
        assert result[constants.FIELD_PLANNING_BLOCK] == long_planning_block
        assert "Ancient Temple - Main Chamber" in result[constants.FIELD_SESSION_HEADER]
        assert "different approach" in result[constants.FIELD_PLANNING_BLOCK]

    def test_extract_structured_fields_with_world_events(self):
        """Test extraction of world_events from state_updates."""
        world_events_data = {
            "background_events": [
                {"description": "A caravan arrives", "turn_generated": 5}
            ],
            "rumors": [
                {"description": "Strange sounds from the forest", "turn_generated": 5}
            ],
            "faction_updates": {
                "merchant_guild": {"activity": "Trading routes expanded"}
            },
        }
        state_updates = {"world_events": world_events_data, "other_data": "ignored"}

        mock_structured_response = Mock(spec=NarrativeResponse)
        mock_structured_response.session_header = "Turn 5"
        mock_structured_response.planning_block = "Options"
        mock_structured_response.dice_rolls = []
        mock_structured_response.dice_audit_events = []
        mock_structured_response.resources = {}
        mock_structured_response.debug_info = {}
        mock_structured_response.god_mode_response = ""
        mock_structured_response.state_updates = state_updates
        mock_structured_response.directives = {}

        mock_gemini_response = Mock(spec=LLMResponse, agent_mode=constants.MODE_CHARACTER)
        mock_gemini_response.structured_response = mock_structured_response

        result = structured_fields_utils.extract_structured_fields(mock_gemini_response)

        # Verify world_events is extracted and state_updates is filtered
        assert "world_events" in result
        assert result["world_events"] == world_events_data
        assert result[constants.FIELD_STATE_UPDATES] == {
            "world_events": world_events_data
        }
        # other_data from state_updates should NOT be present
        assert "other_data" not in result

    def test_extract_structured_fields_includes_state_updates_audit_subset(self):
        """Persist a safe subset of state_updates for postmortem debugging."""
        state_updates = {
            "player_character_data": {"name": "Test", "equipment": {"armor": "Chainmail"}},
            "custom_campaign_state": {"character_creation_in_progress": True},
            "item_registry": {"item_1": {"name": "Sword", "stats": "+1"}},
            # Living-world keys should still be filtered into FIELD_STATE_UPDATES
            "world_events": {"rumors": [{"description": "hi"}]},
        }

        mock_structured_response = Mock(spec=NarrativeResponse)
        mock_structured_response.session_header = "Turn 1"
        mock_structured_response.planning_block = ""
        mock_structured_response.dice_rolls = []
        mock_structured_response.dice_audit_events = []
        mock_structured_response.resources = {}
        mock_structured_response.debug_info = {}
        mock_structured_response.god_mode_response = ""
        mock_structured_response.state_updates = state_updates
        mock_structured_response.directives = {}

        mock_gemini_response = Mock(spec=LLMResponse)
        mock_gemini_response.structured_response = mock_structured_response

        result = structured_fields_utils.extract_structured_fields(mock_gemini_response)

        # Filtered state_updates remains living-world only.
        assert result[constants.FIELD_STATE_UPDATES] == {
            "world_events": state_updates["world_events"]
        }
        # Audit subset includes character creation critical keys.
        assert "state_updates_audit" in result
        assert result["state_updates_audit"]["player_character_data"]["name"] == "Test"
        assert result["state_updates_audit"]["custom_campaign_state"]["character_creation_in_progress"] is True
        assert result["state_updates_audit"]["item_registry"]["_count"] == 1
        assert "item_1" in result["state_updates_audit"]["item_registry"]["_sample_keys"]

    def test_extract_structured_fields_without_world_events(self):
        """Test extraction when state_updates has no world_events."""
        state_updates = {"some_other_field": "value"}

        mock_structured_response = Mock(spec=NarrativeResponse)
        mock_structured_response.session_header = "Turn 1"
        mock_structured_response.planning_block = ""
        mock_structured_response.dice_rolls = []
        mock_structured_response.dice_audit_events = []
        mock_structured_response.resources = {}
        mock_structured_response.debug_info = {}
        mock_structured_response.god_mode_response = ""
        mock_structured_response.state_updates = state_updates
        mock_structured_response.directives = {}

        mock_gemini_response = Mock(spec=LLMResponse, agent_mode=constants.MODE_CHARACTER)
        mock_gemini_response.structured_response = mock_structured_response

        result = structured_fields_utils.extract_structured_fields(mock_gemini_response)

        # world_events should NOT be in result if not present in state_updates
        assert "world_events" not in result
        assert constants.FIELD_STATE_UPDATES not in result

    def test_regression_dice_rolls_backfilled_from_action_resolution_mechanics(self):
        """Backward compat: dice_rolls are backfilled from action_resolution.mechanics.rolls."""
        # This matches the real Firestore data where LLM correctly puts dice in action_resolution
        action_resolution_data = {
            "interpreted_as": "Deception check",
            "audit_flags": [],
            "narrative_outcome": "Success",
            "mechanics": {
                "rolls": [
                    {
                        "success": True,
                        "result": 32,
                        "notation": "1d20+19",
                        "purpose": "Deception (The Absolute's Harvest)",
                        "dc": 15,
                    }
                ],
                "type": "skill_check",
            },
            "reinterpreted": False,
            "player_input": "some input",
        }

        mock_structured_response = Mock(spec=NarrativeResponse)
        mock_structured_response.session_header = "Turn 1"
        mock_structured_response.planning_block = {"choices": {"1": "option"}}
        mock_structured_response.dice_rolls = []  # LLM correctly leaves this empty
        mock_structured_response.dice_audit_events = []
        mock_structured_response.resources = "HP: 49/49"
        mock_structured_response.debug_info = {}
        mock_structured_response.god_mode_response = ""
        mock_structured_response.action_resolution = action_resolution_data
        mock_structured_response.outcome_resolution = {}
        mock_structured_response.directives = {}

        mock_gemini_response = Mock(spec=LLMResponse, agent_mode=constants.MODE_CHARACTER)
        mock_gemini_response.structured_response = mock_structured_response

        result = structured_fields_utils.extract_structured_fields(mock_gemini_response)
        # dice_rolls should be backfilled from action_resolution when empty
        assert len(result[constants.FIELD_DICE_ROLLS]) == 1
        assert result[constants.FIELD_DICE_ROLLS][0]["roll"] == "1d20+19"
        assert result[constants.FIELD_DICE_ROLLS][0]["success"] is True

    def test_regression_dice_rolls_preserved_when_llm_provides_directly(self):
        """Test backward compatibility: if LLM provides dice_rolls directly, preserve them.

        Some older prompts may still have the LLM populate dice_rolls directly.
        This test ensures backward compatibility.
        """
        mock_structured_response = Mock(spec=NarrativeResponse)
        mock_structured_response.session_header = "Turn 1"
        mock_structured_response.planning_block = {}
        mock_structured_response.dice_rolls = [
            "Attack: d20+5 = 18"
        ]  # LLM provided directly
        mock_structured_response.dice_audit_events = []
        mock_structured_response.resources = {}
        mock_structured_response.debug_info = {}
        mock_structured_response.god_mode_response = ""
        mock_structured_response.action_resolution = {}  # Empty action_resolution
        mock_structured_response.outcome_resolution = {}
        mock_structured_response.directives = {}

        mock_gemini_response = Mock(spec=LLMResponse, agent_mode=constants.MODE_CHARACTER)
        mock_gemini_response.structured_response = mock_structured_response

        result = structured_fields_utils.extract_structured_fields(mock_gemini_response)

        # dice_rolls should be preserved from LLM response when action_resolution is empty
        assert result[constants.FIELD_DICE_ROLLS] == ["Attack: d20+5 = 18"]

    def test_regression_action_resolution_rolls_backfill_when_dice_rolls_empty(self):
        """If dice_rolls is empty, backfill from action_resolution.mechanics.rolls."""
        action_resolution_data = {
            "mechanics": {
                "rolls": [
                    {
                        "notation": "1d20+5",
                        "result": 17,
                        "total": 22,
                        "dc": 18,
                        "success": False,
                        "purpose": "Attack",
                    },
                    {
                        "notation": "1d8+3",
                        "result": 8,
                        "total": 11,
                        "purpose": "Damage",
                    },
                ],
            },
        }

        mock_structured_response = Mock(spec=NarrativeResponse)
        mock_structured_response.session_header = ""
        mock_structured_response.planning_block = {}
        mock_structured_response.dice_rolls = []  # Empty as per instruction
        mock_structured_response.dice_audit_events = []
        mock_structured_response.resources = {}
        mock_structured_response.debug_info = {}
        mock_structured_response.god_mode_response = ""
        mock_structured_response.action_resolution = action_resolution_data
        mock_structured_response.outcome_resolution = {}
        mock_structured_response.directives = {}

        mock_gemini_response = Mock(spec=LLMResponse, agent_mode=constants.MODE_CHARACTER)
        mock_gemini_response.structured_response = mock_structured_response

        result = structured_fields_utils.extract_structured_fields(mock_gemini_response)

        # dice_rolls should be backfilled from action_resolution when empty
        assert len(result[constants.FIELD_DICE_ROLLS]) == 2
        assert result[constants.FIELD_DICE_ROLLS][0]["roll"] == "1d20+5"
        assert result[constants.FIELD_DICE_ROLLS][1]["roll"] == "1d8+3"

    def test_think_mode_backwards_compat_dice_rolls_canonicalization(self):
        """Test backwards compatibility: old Think Mode dice_rolls dicts are canonicalized.

        This tests the fallback path for old Think Mode responses that used dice_rolls
        as a list of dicts. New Think Mode responses should use action_resolution directly.
        """
        # OLD Think Mode format: dice_rolls as a list of dicts (deprecated)
        think_mode_rolls = [
            {
                "type": "Intelligence Check (Planning)",
                "roll": "1d20+2",
                "result": 10,
                "dc": 12,
                "dc_category": "Requires Some Thought",
                "dc_reasoning": "Tactical assessment",
                "success": False,
                "margin": -2,
                "outcome": "Failed by 2",
            }
        ]

        mock_structured_response = Mock(spec=NarrativeResponse)
        mock_structured_response.session_header = "Turn 1 (Thinking)"
        mock_structured_response.planning_block = {}
        mock_structured_response.dice_rolls = think_mode_rolls
        mock_structured_response.dice_audit_events = []
        mock_structured_response.resources = {}
        mock_structured_response.debug_info = {}
        mock_structured_response.god_mode_response = ""
        mock_structured_response.action_resolution = {}  # Empty, so should use dice_rolls
        mock_structured_response.outcome_resolution = {}
        mock_structured_response.directives = {}

        mock_gemini_response = Mock(spec=LLMResponse, agent_mode=constants.MODE_CHARACTER)
        mock_gemini_response.structured_response = mock_structured_response

        result = structured_fields_utils.extract_structured_fields(mock_gemini_response)

        assert result[constants.FIELD_DICE_ROLLS] == think_mode_rolls

        # 2. Check that action_resolution was populated
        ar = result["action_resolution"]
        assert ar["mechanics"]["type"] == "planning_check"
        rolls = ar["mechanics"]["rolls"]
        assert len(rolls) == 1
        assert rolls[0]["notation"] == "1d20+2"
        assert rolls[0]["result"] == 10
        assert rolls[0]["dc"] == 12
        assert rolls[0]["success"] is False
        assert rolls[0]["purpose"] == "Intelligence Check (Planning)"
        # Check preserved extra fields
        assert rolls[0]["dc_category"] == "Requires Some Thought"
        assert rolls[0]["outcome"] == "Failed by 2"

    def test_think_mode_uses_action_resolution_directly(self):
        """Test current Think Mode behavior: dice in action_resolution.mechanics.rolls.

        This is the preferred/current behavior where Think Mode uses the same
        action_resolution.mechanics.rolls format as story mode (single source of truth).
        """
        # NEW Think Mode format: action_resolution.mechanics.rolls (same as story mode)
        action_resolution_data = {
            "mechanics": {
                "type": "planning_check",
                "rolls": [
                    {
                        "notation": "1d20+3",
                        "result": 18,
                        "dc": 15,
                        "success": True,
                        "purpose": "Wisdom Check (Planning)",
                        "dc_category": "Complicated Planning",
                        "dc_reasoning": "Complex multi-faction negotiation",
                        "margin": 3,
                        "outcome": "Success - Competent analysis",
                    }
                ],
            }
        }

        mock_structured_response = Mock(spec=NarrativeResponse)
        mock_structured_response.session_header = "Turn 1 (Thinking)"
        mock_structured_response.planning_block = {}
        mock_structured_response.dice_rolls = []  # Empty, as per new instruction
        mock_structured_response.dice_audit_events = []
        mock_structured_response.resources = {}
        mock_structured_response.debug_info = {}
        mock_structured_response.god_mode_response = ""
        mock_structured_response.action_resolution = action_resolution_data
        mock_structured_response.outcome_resolution = {}
        mock_structured_response.directives = {}

        mock_gemini_response = Mock(spec=LLMResponse, agent_mode=constants.MODE_CHARACTER)
        mock_gemini_response.structured_response = mock_structured_response
        result = structured_fields_utils.extract_structured_fields(mock_gemini_response)

        # In think mode, dice_rolls should ALSO be backfilled from action_resolution for UI consistency
        assert len(result[constants.FIELD_DICE_ROLLS]) == 1
        assert result[constants.FIELD_DICE_ROLLS][0]["roll"] == "1d20+3"

        # action_resolution should be preserved
        ar = result["action_resolution"]
        assert ar["mechanics"]["type"] == "planning_check"
        rolls = ar["mechanics"]["rolls"]
        assert len(rolls) == 1
        assert rolls[0]["notation"] == "1d20+3"
        assert rolls[0]["dc_category"] == "Complicated Planning"


class TestStateUpdatesAuditSubset(unittest.TestCase):
    """Test cases for state_updates audit subset functions."""

    def test_audit_trim_item_registry(self):
        """Coverage for line 42: _audit_trim_state_update with item_registry."""

        large_registry = {f"item_{i}": {"name": f"Item {i}"} for i in range(100)}
        result = _audit_trim_state_update("item_registry", large_registry)

        # Should summarize with count and sample
        self.assertIn("_count", result)
        self.assertEqual(result["_count"], 100)
        self.assertIn("_sample_keys", result)
        self.assertLessEqual(len(result["_sample_keys"]), 20)

    def test_build_audit_subset_with_empty_values(self):
        """Coverage for line 103: skip empty values in audit subset."""

        state_updates = {
            "player_character_data": {},  # Empty dict - should be skipped
            "item_registry": None,  # None - should be skipped
            "npc_data": {"npc1": {"name": "Guard"}},  # Non-empty - should be included
        }

        result = _build_state_updates_audit_subset(state_updates)

        # Empty/None values should be skipped
        self.assertNotIn("player_character_data", result)
        self.assertNotIn("item_registry", result)
        # Non-empty should be included
        self.assertIn("npc_data", result)

    def test_extract_with_think_mode_dice_rolls_no_action_resolution(self):
        """Coverage for line 164: Think Mode dice_rolls converted when no action_resolution."""

        # Simulate Think Mode response with dice_rolls but no action_resolution
        mock_structured_response = Mock(spec=NarrativeResponse)
        mock_structured_response.session_header = "Think Mode Turn"
        mock_structured_response.planning_block = {}
        mock_structured_response.dice_rolls = [
            {
                "roll": "1d20+5",
                "result": 18,
                "dc": 15,
                "success": True,
                "type": "perception_check",
                "dc_category": "Medium",
                "dc_reasoning": "Standard perception DC",
                "margin": 3,
                "outcome": "success"
            }
        ]
        mock_structured_response.dice_audit_events = []
        mock_structured_response.resources = {}
        mock_structured_response.debug_info = {}
        mock_structured_response.god_mode_response = ""
        mock_structured_response.action_resolution = None  # No action_resolution
        mock_structured_response.outcome_resolution = {}
        mock_structured_response.directives = {}

        mock_gemini_response = Mock(spec=LLMResponse)
        mock_gemini_response.structured_response = mock_structured_response

        result = structured_fields_utils.extract_structured_fields(mock_gemini_response)

        # Should have created action_resolution from dice_rolls
        self.assertIn("action_resolution", result)
        ar = result["action_resolution"]
        self.assertIn("mechanics", ar)
        self.assertIn("rolls", ar["mechanics"])
        self.assertEqual(len(ar["mechanics"]["rolls"]), 1)

        # Verify conversion from Think Mode format to action_resolution format
        roll = ar["mechanics"]["rolls"][0]
        self.assertEqual(roll["notation"], "1d20+5")  # roll -> notation
        self.assertEqual(roll["purpose"], "perception_check")  # type -> purpose
        self.assertEqual(roll["result"], 18)
        self.assertEqual(roll["dc"], 15)
        self.assertEqual(roll["success"], True)

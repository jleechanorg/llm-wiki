"""Test that god mode responses use the god_mode_response field correctly."""

import os
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from mvp_site import constants, firestore_service, world_logic
from mvp_site.narrative_response_schema import parse_structured_response
from mvp_site.tests.fake_llm import FakeLLMResponse


class TestGodModeResponseField(unittest.TestCase):
    """Test god_mode_response field handling."""

    def setUp(self):
        """Set up test environment"""
        # Set mock services mode to skip verification for unit tests
        os.environ["MOCK_SERVICES_MODE"] = "true"

    def tearDown(self):
        """Clean up test environment"""
        # Clean up environment variable
        if "MOCK_SERVICES_MODE" in os.environ:
            del os.environ["MOCK_SERVICES_MODE"]

    def test_god_mode_response_field_used(self):
        """Test that god_mode_response field is available in response object."""
        god_response = """{
            "narrative": "",
            "god_mode_response": "A mystical fog rolls in from the mountains. The temperature drops suddenly.",
            "entities_mentioned": [],
            "location_confirmed": "Unknown Forest",
            "state_updates": {
                "environment": {
                    "weather": "foggy",
                    "temperature": "cold"
                }
            },
            "debug_info": {}
        }"""

        narrative, response_obj = parse_structured_response(god_response)

        # Narrative should be empty - frontend uses god_mode_response directly
        assert narrative == ""
        # god_mode_response should be available in response object for frontend
        assert (
            response_obj.god_mode_response
            == "A mystical fog rolls in from the mountains. The temperature drops suddenly."
        )
        assert response_obj.narrative == ""

    def test_normal_response_without_god_mode(self):
        """Test that normal responses work without god_mode_response field."""
        normal_response = """{
            "narrative": "You enter the tavern and see a hooded figure in the corner.",
            "entities_mentioned": ["hooded figure"],
            "location_confirmed": "The Rusty Tankard Tavern",
            "state_updates": {},
            "debug_info": {}
        }"""

        narrative, response_obj = parse_structured_response(normal_response)

        # Should return the narrative content
        assert (
            narrative == "You enter the tavern and see a hooded figure in the corner."
        )
        assert (
            response_obj.narrative
            == "You enter the tavern and see a hooded figure in the corner."
        )
        assert response_obj.god_mode_response is None

    def test_god_mode_with_state_updates(self):
        """Test god mode response with complex state updates."""
        god_response = """{
            "narrative": "",
            "god_mode_response": "The ancient dragon Vermithrax awakens from his slumber. His eyes glow with malevolent intelligence.",
            "entities_mentioned": ["Vermithrax"],
            "location_confirmed": "Dragon's Lair",
            "state_updates": {
                "npc_data": {
                    "vermithrax": {
                        "name": "Vermithrax",
                        "type": "ancient_red_dragon",
                        "hp": 546,
                        "max_hp": 546,
                        "status": "hostile"
                    }
                }
            },
            "debug_info": {
                "dm_notes": ["Adding major boss encounter"]
            }
        }"""

        narrative, response_obj = parse_structured_response(god_response)

        # Narrative should be empty - frontend uses god_mode_response directly
        assert narrative == ""
        # god_mode_response should have the content
        assert "ancient dragon Vermithrax" in response_obj.god_mode_response
        assert response_obj.entities_mentioned == ["Vermithrax"]
        assert response_obj.state_updates is not None
        assert "npc_data" in response_obj.state_updates

    def test_god_mode_empty_response(self):
        """Test god mode with empty god_mode_response field."""
        empty_response = """{
            "narrative": "",
            "god_mode_response": "",
            "entities_mentioned": [],
            "location_confirmed": "Unknown",
            "state_updates": {},
            "debug_info": {}
        }"""

        narrative, response_obj = parse_structured_response(empty_response)

        # Should return empty string, not try to extract from elsewhere
        assert narrative == ""
        assert response_obj.god_mode_response == ""

    def test_malformed_god_mode_response(self):
        """Test that malformed JSON returns the standard error message."""
        malformed = (
            """{"god_mode_response": "The world shifts...", "state_updates": {"""
        )

        narrative, response_obj = parse_structured_response(malformed)

        # New strict behavior: returns standardized invalid JSON message
        assert "invalid json response" in narrative.lower()

    def test_backward_compatibility(self):
        """Test that old god mode responses without god_mode_response field still work."""
        old_style_response = """{
            "narrative": "The ancient tome glows with an eerie light as you speak the command.",
            "entities_mentioned": ["ancient tome"],
            "location_confirmed": "Library",
            "state_updates": {
                "inventory": {
                    "ancient_tome": {
                        "activated": true
                    }
                }
            },
            "debug_info": {}
        }"""

        narrative, response_obj = parse_structured_response(old_style_response)

        # Should use narrative field as before
        assert (
            narrative
            == "The ancient tome glows with an eerie light as you speak the command."
        )
        assert response_obj.god_mode_response is None

    def test_god_mode_with_empty_narrative(self):
        """Test god mode response when narrative is empty string."""
        response = """{
            "narrative": "",
            "god_mode_response": "The world trembles at your command.",
            "entities_mentioned": [],
            "location_confirmed": "Unknown",
            "state_updates": {},
            "debug_info": {}
        }"""

        narrative, response_obj = parse_structured_response(response)

        # Narrative should be empty - frontend uses god_mode_response directly
        assert narrative == ""
        # Response object should have god_mode_response for frontend to use
        assert response_obj.god_mode_response == "The world trembles at your command."

    def test_combined_god_mode_and_narrative(self):
        """Test that only narrative is returned when both god_mode_response and narrative are present."""
        both_fields_response = """{
            "narrative": "Meanwhile, in the mortal realm, the players sense a change...",
            "god_mode_response": "The deity grants your wish. A shimmering portal opens.",
            "entities_mentioned": ["shimmering portal"],
            "location_confirmed": "Unknown",
            "state_updates": {},
            "debug_info": {}
        }"""

        narrative, response_obj = parse_structured_response(both_fields_response)

        # Should return only narrative - god_mode_response is passed separately to frontend
        assert (
            narrative == "Meanwhile, in the mortal realm, the players sense a change..."
        )
        assert "The deity grants your wish" not in narrative
        # Response object should have both fields separately
        assert (
            response_obj.god_mode_response
            == "The deity grants your wish. A shimmering portal opens."
        )
        assert (
            response_obj.narrative
            == "Meanwhile, in the mortal realm, the players sense a change..."
        )

    def test_god_mode_response_saved_to_firestore(self):
        """Test that god_mode_response is saved to Firestore via add_story_entry."""
        god_response = {
            "narrative": "",
            "god_mode_response": "A test god mode response for Firestore.",
            "entities_mentioned": [],
            "location_confirmed": "Test Location",
            "state_updates": {},
            "debug_info": {},
        }
        with patch(
            "mvp_site.firestore_service.add_story_entry"
        ) as mock_add_story_entry:
            firestore_service.add_story_entry(
                "user123",
                "camp456",
                "gemini",
                god_response["god_mode_response"],
                structured_fields=god_response,
            )
            called_args, called_kwargs = mock_add_story_entry.call_args
            assert "god_mode_response" in called_kwargs["structured_fields"]
            assert (
                called_kwargs["structured_fields"]["god_mode_response"]
                == "A test god mode response for Firestore."
            )


class TestGodModeResponseIntegration(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        # Set mock services mode to skip verification for unit tests
        os.environ["MOCK_SERVICES_MODE"] = "true"

    def tearDown(self):
        """Clean up test environment"""
        # Clean up environment variable
        if "MOCK_SERVICES_MODE" in os.environ:
            del os.environ["MOCK_SERVICES_MODE"]

    def test_all_structured_fields_are_saved_in_firestore(self):
        # Patch the full Firestore chain
        mock_db = MagicMock()
        mock_users_collection = MagicMock()
        mock_user_doc = MagicMock()
        mock_campaigns_collection = MagicMock()
        mock_campaign_doc = MagicMock()
        mock_story_collection = MagicMock()

        # Chain the calls
        mock_db.collection.return_value = mock_users_collection
        mock_users_collection.document.return_value = mock_user_doc
        mock_user_doc.collection.return_value = mock_campaigns_collection
        mock_campaigns_collection.document.return_value = mock_campaign_doc
        mock_campaign_doc.collection.return_value = mock_story_collection

        with patch("mvp_site.firestore_service.get_db", return_value=mock_db):
            structured_fields = {
                constants.FIELD_SESSION_HEADER: "Session header value",
                constants.FIELD_PLANNING_BLOCK: "Planning block value",
                constants.FIELD_DICE_ROLLS: [1, 2, 3],
                constants.FIELD_RESOURCES: "Resource value",
                constants.FIELD_DEBUG_INFO: {"debug": True},
                constants.FIELD_GOD_MODE_RESPONSE: "Integration test god mode response",
            }
            firestore_service.add_story_entry(
                user_id="user123",
                campaign_id="camp456",
                actor=constants.ACTOR_GEMINI,
                text="Some narrative",
                structured_fields=structured_fields,
            )

            # Check that add() was called with all structured fields present
            assert mock_story_collection.add.called
            add_call_args, add_call_kwargs = mock_story_collection.add.call_args
            written_data = add_call_args[0]
            for field, value in structured_fields.items():
                assert field in written_data
                assert written_data[field] == value


class TestGodModeEmptyNarrativeHandling(unittest.TestCase):
    """Test empty narrative handling uses request-level mode.

    The empty narrative handler uses request-level mode to determine god mode
    fallback behavior, allowing clients to control when god mode applies.
    """

    def setUp(self):
        """Set up test environment"""
        os.environ["MOCK_SERVICES_MODE"] = "true"

    def tearDown(self):
        """Clean up test environment"""
        if "MOCK_SERVICES_MODE" in os.environ:
            del os.environ["MOCK_SERVICES_MODE"]

    def test_god_mode_request_empty_narrative_stays_empty(self):
        """When request mode is god and narrative is empty, narrative stays empty.

        God mode responses use god_mode_response field for display - the narrative
        field should NOT be populated with god_mode_response content. The frontend
        uses god_mode_response directly.
        """
        # Create fake LLM response with empty narrative
        mock_response = FakeLLMResponse("{}")
        mock_response.narrative_text = ""  # Empty narrative (expected for god mode)
        mock_response.structured_response = SimpleNamespace(
            god_mode_response="Weather changed to stormy.",
            narrative="",
        )

        # Request mode is god - narrative should stay empty
        request_mode = constants.MODE_GOD

        final_narrative = world_logic._resolve_empty_narrative(
            mock_response.narrative_text, mock_response, request_mode
        )

        # Narrative should be empty string - frontend uses god_mode_response directly
        assert final_narrative == ""

    def test_non_god_mode_request_empty_narrative_shows_error(self):
        """When request mode is not god, empty narrative shows error."""
        # Request mode is character (not god)
        request_mode = constants.MODE_CHARACTER

        # Create fake LLM response
        mock_response = FakeLLMResponse("{}")
        mock_response.narrative_text = (
            ""  # Empty narrative (unexpected for character mode)
        )

        # Create structured response without god_mode_response
        mock_response.structured_response = SimpleNamespace(
            god_mode_response=None,
            narrative="",
        )

        final_narrative = world_logic._resolve_empty_narrative(
            mock_response.narrative_text, mock_response, request_mode
        )

        # Should show error since request mode is not god
        assert final_narrative == "[Error: Empty narrative from LLM]"

    def test_god_mode_request_no_god_response_stays_empty(self):
        """When request is god mode but no god_mode_response, narrative stays empty.

        God mode empty narrative is expected - frontend handles display separately.
        """
        mock_response = FakeLLMResponse("{}")
        mock_response.narrative_text = ""

        mock_response.structured_response = SimpleNamespace(
            god_mode_response=None,
            narrative="",
        )

        # Request mode is god
        request_mode = constants.MODE_GOD

        final_narrative = world_logic._resolve_empty_narrative(
            mock_response.narrative_text, mock_response, request_mode
        )

        # Narrative stays empty - god mode doesn't need narrative
        assert final_narrative == ""


class TestResolveEmptyNarrativeCentralizedDetection(unittest.TestCase):
    """Test _resolve_empty_narrative() uses centralized is_god_mode() detection.

    These tests verify that the function properly uses constants.is_god_mode()
    for case-insensitive mode matching AND GOD MODE: prefix detection.
    """

    def setUp(self):
        """Set up test environment."""
        os.environ["MOCK_SERVICES_MODE"] = "true"

    def tearDown(self):
        """Clean up test environment."""
        if "MOCK_SERVICES_MODE" in os.environ:
            del os.environ["MOCK_SERVICES_MODE"]

    def _create_mock_response(self):
        """Create a mock LLM response with empty narrative."""
        mock_response = FakeLLMResponse("{}")
        mock_response.narrative_text = ""
        mock_response.structured_response = SimpleNamespace(
            god_mode_response=None,
            narrative="",
        )
        return mock_response

    def test_case_insensitive_mode_lowercase(self):
        """Mode 'god' (lowercase) should be detected as god mode."""
        mock_response = self._create_mock_response()

        final_narrative = world_logic._resolve_empty_narrative(
            "", mock_response, "god", user_input=""
        )

        assert final_narrative == "", (
            "Lowercase 'god' mode should return empty narrative"
        )

    def test_case_insensitive_mode_uppercase(self):
        """Mode 'GOD' (uppercase) should be detected as god mode."""
        mock_response = self._create_mock_response()

        final_narrative = world_logic._resolve_empty_narrative(
            "", mock_response, "GOD", user_input=""
        )

        assert final_narrative == "", (
            "Uppercase 'GOD' mode should return empty narrative"
        )

    def test_case_insensitive_mode_mixed_case(self):
        """Mode 'God' (mixed case) should be detected as god mode."""
        mock_response = self._create_mock_response()

        final_narrative = world_logic._resolve_empty_narrative(
            "", mock_response, "God", user_input=""
        )

        assert final_narrative == "", (
            "Mixed case 'God' mode should return empty narrative"
        )

    def test_prefix_detection_without_mode(self):
        """'GOD MODE:' prefix in user_input should detect god mode even without mode param."""
        mock_response = self._create_mock_response()

        final_narrative = world_logic._resolve_empty_narrative(
            "", mock_response, mode=None, user_input="GOD MODE: Change weather to sunny"
        )

        assert final_narrative == "", "GOD MODE: prefix should detect god mode"

    def test_prefix_detection_lowercase(self):
        """'god mode:' prefix (lowercase) should detect god mode."""
        mock_response = self._create_mock_response()

        final_narrative = world_logic._resolve_empty_narrative(
            "", mock_response, mode=None, user_input="god mode: Add a new NPC"
        )

        assert final_narrative == "", (
            "Lowercase 'god mode:' prefix should detect god mode"
        )

    def test_combined_mode_and_prefix(self):
        """Both mode and prefix should detect god mode."""
        mock_response = self._create_mock_response()

        final_narrative = world_logic._resolve_empty_narrative(
            "", mock_response, mode="god", user_input="GOD MODE: Test command"
        )

        assert final_narrative == "", "Both mode and prefix should detect god mode"

    def test_non_god_mode_shows_error(self):
        """Non-god mode with empty narrative should show error."""
        mock_response = self._create_mock_response()

        final_narrative = world_logic._resolve_empty_narrative(
            "", mock_response, mode="character", user_input="I attack the goblin"
        )

        assert final_narrative == "[Error: Empty narrative from LLM]"

    def test_non_empty_narrative_passthrough(self):
        """Non-empty narrative should pass through unchanged regardless of mode."""
        mock_response = self._create_mock_response()
        test_narrative = "The goblin attacks you!"

        final_narrative = world_logic._resolve_empty_narrative(
            test_narrative, mock_response, mode="character", user_input=""
        )

        assert final_narrative == test_narrative

    def test_user_input_none_handled(self):
        """user_input=None should be handled gracefully."""
        mock_response = self._create_mock_response()

        # With god mode set, should still work
        final_narrative = world_logic._resolve_empty_narrative(
            "", mock_response, mode="god", user_input=None
        )

        assert final_narrative == ""

    def test_fallback_to_structured_narrative(self):
        """Non-god mode should fallback to structured_response.narrative if available."""
        mock_response = self._create_mock_response()
        mock_response.structured_response = SimpleNamespace(
            god_mode_response=None,
            narrative="Fallback narrative from structured response",
        )

        final_narrative = world_logic._resolve_empty_narrative(
            "", mock_response, mode="character", user_input=""
        )

        assert final_narrative == "Fallback narrative from structured response"


if __name__ == "__main__":
    unittest.main()

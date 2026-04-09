"""
Tests for Gemini response validation and parsing in llm_service.py.
Focus on JSON parsing, schema validation, and field validation.
"""

import json
import os
import sys
import unittest

# Add the root directory (two levels up) to the Python path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set testing environment
os.environ["TESTING_AUTH_BYPASS"] = "true"


from mvp_site.llm_service import (
    _parse_gemini_response,
)
from mvp_site.narrative_response_schema import (
    NarrativeResponse,
    parse_structured_response,
)


class TestLLMResponseValidation(unittest.TestCase):
    """Test suite for Gemini API response validation and parsing."""

    def setUp(self):
        """Set up test fixtures."""
        self.maxDiff = None

    # Group 1 - JSON Parsing Tests

    def test_valid_json_parsing(self):
        """Test that valid JSON responses are parsed correctly."""
        # Create valid JSON response
        valid_json = {
            "narrative": "The wizard enters the room cautiously.",
            "entities_mentioned": ["wizard", "room"],
            "location_confirmed": "Dungeon Chamber",
            "turn_summary": "Wizard explores the chamber",
            "state_updates": {"position": "chamber_entrance"},
            "debug_info": {"rolls": ["perception: 18"]},
        }

        # Test with raw JSON
        response_text = json.dumps(valid_json, indent=2)
        parsed_text, structured = parse_structured_response(response_text)

        assert isinstance(structured, NarrativeResponse)
        assert structured.narrative == "The wizard enters the room cautiously."
        assert structured.entities_mentioned == ["wizard", "room"]
        assert structured.location_confirmed == "Dungeon Chamber"
        assert parsed_text == "The wizard enters the room cautiously."

        # Test with markdown-wrapped JSON
        markdown_response = f"```json\n{response_text}\n```"
        parsed_text, structured = parse_structured_response(markdown_response)

        assert isinstance(structured, NarrativeResponse)
        assert structured.narrative == "The wizard enters the room cautiously."

    def test_invalid_json_returns_error_response(self):
        """Test that malformed JSON returns error response (no recovery per PR #3458)."""
        # Test completely malformed JSON - recovery was intentionally removed
        malformed_json = (
            '{"narrative": "The story begins...", "entities_mentioned": ["hero"'
        )

        parsed_text, structured = parse_structured_response(malformed_json)

        # Should return error response (no partial recovery per PR #3458)
        assert isinstance(structured, NarrativeResponse)
        # Returns error message, not recovered content
        assert "Invalid JSON response" in parsed_text or "error" in parsed_text.lower()

    def test_extra_data_json_recovery(self):
        """Test that valid JSON followed by extra data IS recovered."""
        valid_json_part = {"narrative": "A complete story."}
        json_with_extra = json.dumps(valid_json_part) + " Some extra text after JSON"

        parsed_text, structured = parse_structured_response(json_with_extra)

        # Should recover the valid JSON portion
        assert isinstance(structured, NarrativeResponse)
        assert structured.narrative == "A complete story."
        # parsed_text should be the narrative
        assert parsed_text == "A complete story."

    def test_truncated_json_returns_error_response(self):
        """Test that truncated JSON returns error response (no recovery per PR #3458)."""
        # Simulate truncated response (common with token limits)
        # Per PR #3458, truncated JSON no longer attempts partial recovery
        truncated_json = """{
            "narrative": "The adventurer walks through the ancient forest...",
            "entities_mentioned": ["adventurer", "forest"],
            "location_confirmed": "Ancient Forest",
            "turn_summary": "Adventurer discovers mysterious"""

        parsed_text, structured = parse_structured_response(truncated_json)

        # Should return error response (no partial recovery per PR #3458)
        assert isinstance(structured, NarrativeResponse)
        # Returns error message, not recovered content
        assert "Invalid JSON response" in parsed_text or "error" in parsed_text.lower()

    def test_dice_audit_events_parsing(self):
        """dice_audit_events should parse as list[dict] and ignore invalid items."""
        response = {
            "narrative": "You lunge forward.",
            "entities_mentioned": ["hero"],
            "planning_block": {
                "thinking": "Attack!",
                "choices": {"attack": {"text": "Attack", "description": "Strike"}},
            },
            "dice_rolls": ["Attack: 1d20+5 = 12+5 = 17 vs AC 15 (Hit!)"],
            "dice_audit_events": [
                {
                    "source": "code_execution",
                    "label": "Attack",
                    "notation": "1d20+5",
                    "rolls": [12],
                    "modifier": 5,
                    "total": 17,
                },
                "not-a-dict",
            ],
        }

        parsed_text, structured = parse_structured_response(json.dumps(response))
        assert parsed_text == "You lunge forward."
        assert isinstance(structured, NarrativeResponse)
        assert structured.dice_rolls == ["Attack: 1d20+5 = 12+5 = 17 vs AC 15 (Hit!)"]
        assert structured.dice_audit_events == [
            {
                "source": "code_execution",
                "label": "Attack",
                "notation": "1d20+5",
                "rolls": [12],
                "modifier": 5,
                "total": 17,
            }
        ]

    # Group 2 - Required Fields Tests

    def test_missing_content_field(self):
        """Test response parsing when 'narrative' content field is missing."""
        # Response without narrative field
        missing_narrative = {
            "entities_mentioned": ["wizard", "goblin"],
            "location_confirmed": "Cave",
            "turn_summary": "Battle continues",
        }

        response_text = json.dumps(missing_narrative)

        # Parse response - should handle missing narrative gracefully
        parsed_text, structured = parse_structured_response(response_text)

        # Should still create a valid response
        assert isinstance(structured, NarrativeResponse)
        # When narrative is missing, it seems to return empty string for parsed_text
        # but the structured response should have the data
        assert parsed_text is not None  # Can be empty string
        assert structured.narrative is not None
        # Other fields should be parsed correctly
        assert structured.entities_mentioned == ["wizard", "goblin"]
        assert structured.location_confirmed == "Cave"

    def test_text_field_used_as_narrative_fallback(self):
        """`text` should be accepted as a narrative compatibility field."""
        text_only_payload = {
            "text": "A rustle in the trees makes you freeze in place.",
            "entities_mentioned": ["Kaelen"],
            "location_confirmed": "Ancient Forest",
            "planning_block": {
                "thinking": "The player noticed movement and should decide to investigate or hide.",
                "choices": {
                    "investigate": {
                        "text": "Investigate",
                        "description": "Step toward the sound and inspect the brush.",
                        "risk_level": "medium",
                    }
                },
            },
            "state_updates": {"world_data": {"world_time": {"minute": 1}}},
        }

        parsed_text, structured = parse_structured_response(json.dumps(text_only_payload))

        assert isinstance(structured, NarrativeResponse)
        assert parsed_text == text_only_payload["text"]
        assert structured.narrative == text_only_payload["text"]
        assert structured.location_confirmed == "Ancient Forest"

    def test_multi_element_json_array_selects_narrative_object(self):
        """Parser should recover when response is a mixed JSON array."""
        mixed_array_payload = [
            {"tool_code": "print('helper output')"},
            {
                "narrative": "Aric strikes first and forces the goblin back.",
                "entities_mentioned": ["Aric", "Goblin"],
                "location_confirmed": "Ancient Forest - North Clearing",
                "action_resolution": {
                    "player_input": "I attack the nearest goblin.",
                    "interpreted_as": "melee_attack",
                    "reinterpreted": False,
                    "mechanics": {
                        "type": "attack_roll",
                        "rolls": [
                            {"notation": "1d20+5", "result": 18, "total": 23, "dc": 13, "success": True},
                            {"notation": "1d8+3", "result": 4, "total": 7},
                        ],
                    },
                    "audit_flags": [],
                },
                "state_updates": {"combat_state": {"in_combat": True}},
            },
        ]

        parsed_text, structured = parse_structured_response(json.dumps(mixed_array_payload))

        assert isinstance(structured, NarrativeResponse)
        assert parsed_text == "Aric strikes first and forces the goblin back."
        assert structured.narrative == "Aric strikes first and forces the goblin back."
        assert structured.location_confirmed == "Ancient Forest - North Clearing"

    def test_missing_role_field(self):
        """Test response parsing when role-related fields are missing."""
        # Note: Based on the schema, there's no 'role' field, but we have entities_mentioned
        # Test missing entities_mentioned which is similar to role tracking
        missing_entities = {
            "narrative": "The battle rages on.",
            "location_confirmed": "Battlefield",
            "turn_summary": "Combat round",
        }

        response_text = json.dumps(missing_entities)
        parsed_text, structured = parse_structured_response(response_text)

        # Should handle missing entities_mentioned gracefully
        assert isinstance(structured, NarrativeResponse)
        assert structured.entities_mentioned == []  # Should default to empty list
        assert structured.narrative == "The battle rages on."

    def test_missing_parts_field(self):
        """Test response parsing when complex structure fields are missing."""
        # Test missing state_updates (which has parts/structure)
        missing_parts = {
            "narrative": "The hero ponders their next move.",
            "entities_mentioned": ["hero"],
        }

        response_text = json.dumps(missing_parts)
        parsed_text, structured = parse_structured_response(response_text)

        # Should handle missing fields gracefully
        assert isinstance(structured, NarrativeResponse)
        assert structured.state_updates == {}  # Should default to empty dict
        assert structured.location_confirmed == "Unknown"  # Should have default
        assert structured.turn_summary is None  # Optional field can be None

    # Group 3 - Type Validation Tests

    def test_invalid_content_type(self):
        """Test response parsing when content is wrong type (number not string)."""
        # Narrative as number instead of string
        invalid_type = {
            "narrative": 12345,  # Should be string
            "entities_mentioned": ["player"],
            "location_confirmed": "Town",
        }

        response_text = json.dumps(invalid_type)

        # Should handle type conversion or error appropriately
        try:
            parsed_text, structured = parse_structured_response(response_text)
            # If it succeeds, check that it converted to string
            assert isinstance(structured, NarrativeResponse)
            assert isinstance(structured.narrative, str)
            assert structured.narrative == "12345"
        except (ValueError, TypeError) as e:
            # If it fails, that's also acceptable
            assert "must be" in str(e).lower()

    def test_invalid_parts_structure(self):
        """Test response parsing when parts/list fields have wrong structure."""
        # entities_mentioned as string instead of list
        invalid_structure = {
            "narrative": "The adventure begins.",
            "entities_mentioned": "wizard,goblin",  # Should be list
            "location_confirmed": "Forest",
        }

        response_text = json.dumps(invalid_structure)

        # Should handle graceful recovery (default to empty list)
        parsed_text, structured = parse_structured_response(response_text)

        assert isinstance(structured, NarrativeResponse)
        assert structured.entities_mentioned == []

    def test_null_values_handling(self):
        """Test response parsing with null values in required fields."""
        # Test various null scenarios
        null_narrative = {
            "narrative": None,  # Null narrative
            "entities_mentioned": ["hero"],
            "location_confirmed": "Castle",
        }

        response_text = json.dumps(null_narrative)
        parsed_text, structured = parse_structured_response(response_text)

        # Should handle null narrative by using fallback
        assert isinstance(structured, NarrativeResponse)
        assert structured.narrative is not None
        # Should use fallback for null narrative - could be response_text or default message
        assert parsed_text is not None
        # For null narrative, we now return empty string which is acceptable
        # The important thing is that it doesn't crash and returns a valid structure
        assert isinstance(parsed_text, str)
        assert isinstance(structured.narrative, str)

        # Test null in list fields
        null_entities = {
            "narrative": "The quest continues.",
            "entities_mentioned": None,  # Will be converted to empty list
            "location_confirmed": "Town",
        }

        response_text2 = json.dumps(null_entities)

        # Parse and check - null entities_mentioned should become empty list
        parsed_text2, structured2 = parse_structured_response(response_text2)
        assert isinstance(structured2, NarrativeResponse)
        assert structured2.entities_mentioned == []  # Null becomes empty list
        assert structured2.narrative == "The quest continues."

    # Group 4 - Size Limits Tests

    def test_oversized_response(self):
        """Test handling of very large responses (simulating 10MB)."""
        # Create a large narrative (not actually 10MB for test efficiency)
        large_text = "Once upon a time... " * 10000  # ~200KB

        oversized_response = {
            "narrative": large_text,
            "entities_mentioned": ["hero"] * 1000,  # Large entity list
            "location_confirmed": "Kingdom",
            "state_updates": {
                "custom_campaign_state": {f"key_{i}": f"value_{i}" for i in range(1000)}
            },  # Large dict
        }

        response_text = json.dumps(oversized_response)

        # Should handle large responses without crashing
        parsed_text, structured = parse_structured_response(response_text)

        assert isinstance(structured, NarrativeResponse)
        # Narrative is stripped, so it will be slightly shorter
        assert len(structured.narrative) == len(large_text.strip())
        assert structured.narrative.startswith("Once upon a time...")
        # Large entity list should be preserved
        assert len(structured.entities_mentioned) == 1000
        # State updates should be preserved
        assert len(structured.state_updates["custom_campaign_state"]) == 1000

    def test_empty_content_handling(self):
        """Test handling of empty content fields."""
        # Test empty narrative
        empty_content = {
            "narrative": "",  # Empty string
            "entities_mentioned": [],
            "location_confirmed": "Void",
        }

        response_text = json.dumps(empty_content)
        parsed_text, structured = parse_structured_response(response_text)

        # Should handle empty narrative
        assert isinstance(structured, NarrativeResponse)
        assert structured.narrative == ""
        assert structured.entities_mentioned == []
        assert parsed_text == ""  # Empty narrative returns empty parsed_text

        # Test completely empty response
        empty_response = ""
        parsed_text2, structured2 = parse_structured_response(empty_response)

        # Should return default response
        assert isinstance(structured2, NarrativeResponse)
        assert structured2.narrative == "The story awaits your input..."
        assert parsed_text2 == "The story awaits your input..."

    def test_whitespace_only_content(self):
        """Test handling of whitespace-only content."""
        # Various whitespace scenarios
        whitespace_tests = [
            {
                "narrative": "   ",
                "entities_mentioned": ["ghost"],
                "location_confirmed": "Limbo",
            },
            {
                "narrative": "\n\n\n",
                "entities_mentioned": [],
                "location_confirmed": "Space",
            },
            {
                "narrative": "\t\t",
                "entities_mentioned": ["void"],
                "location_confirmed": "Tab Land",
            },
            {
                "narrative": " \n \t ",
                "entities_mentioned": [],
                "location_confirmed": "Mixed Space",
            },
        ]

        for test_case in whitespace_tests:
            response_text = json.dumps(test_case)
            parsed_text, structured = parse_structured_response(response_text)

            # Should preserve whitespace in narrative
            assert isinstance(structured, NarrativeResponse)
            # Narrative should be stripped in validation but original preserved
            assert len(structured.narrative.strip()) == 0
            assert structured.location_confirmed == test_case["location_confirmed"]

        # Test response with Unicode and emojis
        unicode_response = {
            "narrative": "The wizard casts a spell: ✨🔮✨ «Абракадабра!» 中文测试",
            "entities_mentioned": ["wizard", "spell"],
            "location_confirmed": "Magic Tower 🏰",
        }

        response_text = json.dumps(unicode_response, ensure_ascii=False)
        parsed_text, structured = parse_structured_response(response_text)

        # Should handle Unicode and emojis correctly
        assert isinstance(structured, NarrativeResponse)
        assert "✨" in structured.narrative
        assert "🔮" in structured.narrative
        assert "Абракадабра" in structured.narrative
        assert "中文测试" not in structured.narrative  # CJK should be stripped
        assert "🏰" in structured.location_confirmed


class TestParseGeminiResponse(unittest.TestCase):
    """Test suite for _parse_gemini_response function with requires_action_resolution parameter."""

    def test_parse_gemini_response_with_action_resolution_required(self):
        """Test _parse_gemini_response passes requires_action_resolution=True to parse_structured_response."""
        valid_json = {
            "narrative": "The warrior draws their sword.",
            "entities_mentioned": ["warrior"],
            "location_confirmed": "Battle Arena",
        }
        response_text = json.dumps(valid_json)

        # When requires_action_resolution=True (default), the NarrativeResponse
        # should have _requires_action_resolution=True
        parsed_text, structured = _parse_gemini_response(
            response_text, context="test", requires_action_resolution=True
        )

        assert isinstance(structured, NarrativeResponse)
        assert structured.narrative == "The warrior draws their sword."
        # The internal flag should be set
        assert structured._requires_action_resolution is True

    def test_parse_gemini_response_with_action_resolution_exempt(self):
        """Test _parse_gemini_response passes requires_action_resolution=False for exempt modes."""
        valid_json = {
            "narrative": "Welcome to character creation!",
            "entities_mentioned": [],
            "location_confirmed": "Character Setup",
        }
        response_text = json.dumps(valid_json)

        # When requires_action_resolution=False (for exempt agents like CharacterCreation)
        parsed_text, structured = _parse_gemini_response(
            response_text,
            context="character_creation",
            requires_action_resolution=False,
        )

        assert isinstance(structured, NarrativeResponse)
        assert structured.narrative == "Welcome to character creation!"
        # The internal flag should be False for exempt modes
        assert structured._requires_action_resolution is False

    def test_parse_gemini_response_default_requires_action_resolution(self):
        """Test _parse_gemini_response defaults to requires_action_resolution=True."""
        valid_json = {
            "narrative": "The story continues...",
            "entities_mentioned": ["hero"],
            "location_confirmed": "Unknown",
        }
        response_text = json.dumps(valid_json)

        # Default call without specifying requires_action_resolution
        parsed_text, structured = _parse_gemini_response(response_text, context="test")

        assert isinstance(structured, NarrativeResponse)
        # Default should be True
        assert structured._requires_action_resolution is True

    def test_parse_structured_response_with_requires_action_resolution_false(self):
        """Test parse_structured_response passes requires_action_resolution to NarrativeResponse."""
        valid_json = {
            "narrative": "God mode activated.",
            "entities_mentioned": [],
            "location_confirmed": "Admin Console",
            "god_mode_response": "Command executed.",
        }
        response_text = json.dumps(valid_json)

        # Call with requires_action_resolution=False (for God Mode)
        parsed_text, structured = parse_structured_response(
            response_text, requires_action_resolution=False
        )

        assert isinstance(structured, NarrativeResponse)
        # The internal flag should be False
        assert structured._requires_action_resolution is False


if __name__ == "__main__":
    unittest.main()

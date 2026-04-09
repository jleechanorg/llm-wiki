"""Test that God mode responses include planning blocks when offering choices."""

import os
import sys
import unittest

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from mvp_site.narrative_response_schema import parse_structured_response


class TestGodModePlanningBlocks(unittest.TestCase):
    """Test God mode planning block requirements."""

    def test_god_mode_with_planning_block(self):
        """Test that God mode responses can include planning blocks."""
        god_response_with_choices = """{
            "narrative": "",
            "god_mode_response": "As the omniscient game master, I present several plot directions for your campaign.",
            "planning_block": {
                "thinking": "As the omniscient game master, I'm presenting meta-narrative options for the campaign direction.",
                "context": "The player has requested god mode assistance with plot development.",
                "choices": [
                    {
                        "id": "god:plot_arc_1",
                        "text": "Implement Plot Arc 1",
                        "description": "The Silent Scars of Silverwood - investigate Alexiel's legacy",
                        "risk_level": "medium"
                    },
                    {
                        "id": "god:plot_arc_2",
                        "text": "Implement Plot Arc 2",
                        "description": "The Empyrean Whisper - corruption within the Imperial ranks",
                        "risk_level": "high"
                    },
                    {
                        "id": "god:return_story",
                        "text": "Return to Story",
                        "description": "Continue with the current narrative without implementing new plot elements",
                        "risk_level": "safe",
                        "switch_to_story_mode": "true"
                    },
                    {
                        "id": "god:custom_direction",
                        "text": "Custom Direction",
                        "description": "Describe a different plot direction or modification you'd like to explore",
                        "risk_level": "low"
                    }
                ]
            },
            "entities_mentioned": [],
            "location_confirmed": "Unknown",
            "state_updates": {},
            "debug_info": {}
        }"""

        narrative, response_obj = parse_structured_response(god_response_with_choices)

        # For god mode, narrative stays empty - frontend uses god_mode_response directly
        assert narrative == "", (
            f"narrative should be empty for god mode, got: {narrative}"
        )
        assert (
            response_obj.god_mode_response
            == "As the omniscient game master, I present several plot directions for your campaign."
        )

        # Should have planning block
        assert response_obj.planning_block is not None
        assert "thinking" in response_obj.planning_block
        assert "choices" in response_obj.planning_block

        # Verify all God mode choices have "god:" prefix
        choices = response_obj.planning_block.get("choices", [])
        for choice in choices:
            assert choice["id"].startswith("god:"), (
                f"Choice id '{choice['id']}' must start with 'god:' prefix"
            )

        # Verify mandatory "god:return_story" choice exists
        return_story = next(
            (choice for choice in choices if choice.get("id") == "god:return_story"),
            None,
        )
        assert return_story is not None, (
            "Must include 'god:return_story' as default choice"
        )
        assert return_story.get("switch_to_story_mode") is True, (
            "god:return_story should explicitly switch to story/character mode"
        )

    def test_god_mode_choices_all_have_prefix(self):
        """Test that all God mode choices use the god: prefix."""
        god_response = """{
            "narrative": "",
            "god_mode_response": "Multiple paths lie before you.",
            "planning_block": {
                "thinking": "Presenting campaign options",
                "choices": [
                    {
                        "id": "god:option_1",
                        "text": "Option 1",
                        "description": "First option"
                    },
                    {
                        "id": "god:option_2",
                        "text": "Option 2",
                        "description": "Second option"
                    },
                    {
                        "id": "god:return_story",
                        "text": "Return to Story",
                        "description": "Continue normal play"
                    }
                ]
            },
            "entities_mentioned": [],
            "location_confirmed": "Unknown",
            "state_updates": {},
            "debug_info": {}
        }"""

        narrative, response_obj = parse_structured_response(god_response)

        # All choices should have god: prefix
        choices = response_obj.planning_block.get("choices", [])
        assert all(choice.get("id", "").startswith("god:") for choice in choices)

    def test_think_mode_choices_allow_think_prefix(self):
        """Think mode choices should allow think: prefixes per schema regex."""
        think_response = """{
            "narrative": "",
            "planning_block": {
                "thinking": "Strategic options",
                "choices": [
                    {"id": "think:scout", "text": "Scout", "description": "Look around"},
                    {"id": "think:direct", "text": "Direct", "description": "Issue commands"},
                    {"id": "think:return_story", "text": "Return", "description": "Resume story"}
                ]
            },
            "entities_mentioned": [],
            "location_confirmed": "Unknown",
            "state_updates": {},
            "debug_info": {}
        }"""

        _, response_obj = parse_structured_response(think_response)

        choices = response_obj.planning_block.get("choices", [])
        assert choices, "Think mode choices should be parsed"
        assert all(choice.get("id", "").startswith("think:") for choice in choices), (
            f"All choices should use think: prefix, got: {choices}"
        )

    def test_god_mode_without_planning_block(self):
        """Test that God mode responses without choices don't require planning blocks."""
        god_response_no_choices = """{
            "narrative": "",
            "god_mode_response": "The ancient artifact has been placed in the dungeon as requested.",
            "entities_mentioned": ["ancient artifact"],
            "location_confirmed": "Dungeon",
            "state_updates": {
                "items": {
                    "ancient_artifact": {
                        "location": "dungeon_level_3"
                    }
                }
            },
            "debug_info": {}
        }"""

        narrative, response_obj = parse_structured_response(god_response_no_choices)

        # For god mode, narrative stays empty - frontend uses god_mode_response directly
        assert narrative == "", (
            f"narrative should be empty for god mode, got: {narrative}"
        )
        # god_mode_response should have the content
        assert (
            response_obj.god_mode_response
            == "The ancient artifact has been placed in the dungeon as requested."
        )
        # Planning block should be empty dict when not provided
        assert response_obj.planning_block == {}

    def test_missing_return_story_choice(self):
        """Test detection of missing god:return_story choice."""
        god_response_missing_default = """{
            "narrative": "",
            "god_mode_response": "Choose your path.",
            "planning_block": {
                "thinking": "Presenting options",
                "choices": {
                    "god:option_1": {
                        "text": "Option 1",
                        "description": "First option"
                    },
                    "god:option_2": {
                        "text": "Option 2",
                        "description": "Second option"
                    }
                }
            },
            "entities_mentioned": [],
            "location_confirmed": "Unknown",
            "state_updates": {},
            "debug_info": {}
        }"""

        narrative, response_obj = parse_structured_response(
            god_response_missing_default
        )

        # Should still parse successfully
        assert response_obj.planning_block is not None
        choices = response_obj.planning_block.get("choices", [])

        # But we can detect the missing default choice
        assert all(choice.get("id") != "god:return_story" for choice in choices)

    def test_planning_block_structure(self):
        """Test that God mode planning blocks follow the correct structure."""
        god_response = """{
            "narrative": "",
            "god_mode_response": "Several narrative paths are available.",
            "planning_block": {
                "thinking": "As the omniscient game master, I'm presenting meta-narrative options for the campaign direction.",
                "context": "The player has requested god mode assistance with plot development.",
                "choices": {
                    "god:plot_arc_1": {
                        "text": "Implement Plot Arc 1",
                        "description": "The Silent Scars of Silverwood - investigate Alexiel's legacy",
                        "risk_level": "medium"
                    },
                    "god:return_story": {
                        "text": "Return to Story",
                        "description": "Continue with the current narrative",
                        "risk_level": "safe"
                    }
                }
            },
            "entities_mentioned": [],
            "location_confirmed": "Unknown",
            "state_updates": {},
            "debug_info": {}
        }"""

        narrative, response_obj = parse_structured_response(god_response)

        # Verify planning block structure
        planning_block = response_obj.planning_block
        assert planning_block is not None
        assert "thinking" in planning_block
        assert "context" in planning_block
        assert "choices" in planning_block

        # Verify choice structure
        choices = planning_block["choices"]
        for choice_data in choices:
            assert "id" in choice_data
            assert "text" in choice_data
            assert "description" in choice_data
            # risk_level is optional but if present should be valid
            if "risk_level" in choice_data:
                assert choice_data["risk_level"] in ["safe", "low", "medium", "high"]


if __name__ == "__main__":
    unittest.main()

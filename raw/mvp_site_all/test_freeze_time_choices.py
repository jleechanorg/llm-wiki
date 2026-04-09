"""
Tests for freeze_time choice behavior.

When a planning block choice has freeze_time=true, selecting that choice should
cause time to advance by only 1 microsecond (like Think Mode), rather than
advancing normally.

This is used for meta-game decisions like level-up choices that don't represent
in-game time passing.
"""

import unittest

from mvp_site import constants, document_generator, world_logic
from mvp_site.narrative_response_schema import NarrativeResponse


def _get_choice_by_id(choices, choice_id):
    if not isinstance(choices, list):
        return None
    for choice in choices:
        if isinstance(choice, dict) and choice.get("id") == choice_id:
            return choice
    return None


class TestFreezeTimeChoiceValidation(unittest.TestCase):
    """Test freeze_time field validation in planning blocks."""

    def test_freeze_time_boolean_true_preserved(self):
        """freeze_time: true should be preserved in validated choice."""
        planning_block = {
            "thinking": "Should I level up now?",
            "choices": [
                {
                    "id": "level_up_now",
                    "text": "Level Up to Level 5",
                    "description": "Apply level 5 benefits immediately",
                    "risk_level": "safe",
                    "freeze_time": True,
                }
            ],
        }

        response = NarrativeResponse(
            narrative="You've gained enough experience to level up!",
            planning_block=planning_block,
        )

        validated = response.planning_block
        self.assertIn("choices", validated)
        choice = _get_choice_by_id(validated["choices"], "level_up_now")
        self.assertIsNotNone(choice)
        self.assertTrue(choice.get("freeze_time"))

    def test_freeze_time_boolean_false_preserved(self):
        """freeze_time: false should be preserved in validated choice."""
        planning_block = {
            "thinking": "Combat options",
            "choices": [
                {
                    "id": "attack",
                    "text": "Attack",
                    "description": "Attack the goblin",
                    "risk_level": "medium",
                    "freeze_time": False,
                }
            ],
        }

        response = NarrativeResponse(
            narrative="A goblin stands before you!",
            planning_block=planning_block,
        )

        validated = response.planning_block
        choice = _get_choice_by_id(validated["choices"], "attack")
        self.assertIsNotNone(choice)
        self.assertFalse(choice.get("freeze_time"))

    def test_freeze_time_string_true_coerced(self):
        """freeze_time: "true" (string) should be coerced to boolean True."""
        planning_block = {
            "thinking": "Level up decision",
            "choices": [
                {
                    "id": "level_up",
                    "text": "Level Up",
                    "description": "Level up now",
                    "risk_level": "safe",
                    "freeze_time": "true",  # String, not boolean
                }
            ],
        }

        response = NarrativeResponse(
            narrative="Level up available!",
            planning_block=planning_block,
        )

        validated = response.planning_block
        choice = _get_choice_by_id(validated["choices"], "level_up")
        self.assertIsNotNone(choice)
        self.assertTrue(choice.get("freeze_time"))

    def test_freeze_time_string_false_coerced(self):
        """freeze_time: "false" (string) should be coerced to boolean False."""
        planning_block = {
            "thinking": "Combat decision",
            "choices": [
                {
                    "id": "attack",
                    "text": "Attack",
                    "description": "Attack now",
                    "risk_level": "medium",
                    "freeze_time": "false",  # String, not boolean
                }
            ],
        }

        response = NarrativeResponse(
            narrative="Combat begins!",
            planning_block=planning_block,
        )

        validated = response.planning_block
        choice = _get_choice_by_id(validated["choices"], "attack")
        self.assertIsNotNone(choice)
        self.assertFalse(choice.get("freeze_time"))

    def test_freeze_time_missing_not_added(self):
        """When freeze_time is not present, it should not be added to validated choice."""
        planning_block = {
            "thinking": "What to do?",
            "choices": [
                {
                    "id": "explore",
                    "text": "Explore",
                    "description": "Look around",
                    "risk_level": "low",
                }
            ],
        }

        response = NarrativeResponse(
            narrative="You stand at a crossroads.",
            planning_block=planning_block,
        )

        validated = response.planning_block
        # freeze_time should not be in the choice since it wasn't provided
        choice = _get_choice_by_id(validated["choices"], "explore")
        self.assertIsNotNone(choice)
        self.assertNotIn("freeze_time", choice)


class TestExtractRecentPlanningBlocks(unittest.TestCase):
    """Test _extract_recent_planning_blocks helper function."""

    def test_extracts_planning_blocks_from_ai_responses(self):
        """Should extract planning blocks from AI responses in story context."""
        story_context = [
            {
                constants.KEY_ACTOR: constants.ACTOR_GEMINI,
                constants.FIELD_PLANNING_BLOCK: {
                    "thinking": "First planning block",
                    "choices": [
                        {"id": "option1", "text": "Option 1", "description": "First"}
                    ],
                },
            },
            {
                constants.KEY_ACTOR: "user",
                constants.KEY_TEXT: "I choose option 1",
            },
            {
                constants.KEY_ACTOR: constants.ACTOR_GEMINI,
                constants.FIELD_PLANNING_BLOCK: {
                    "thinking": "Second planning block",
                    "choices": [
                        {
                            "id": "level_up_now",
                            "text": "Level Up",
                            "description": "Level up now",
                            "freeze_time": True,
                        }
                    ],
                },
            },
        ]

        result = world_logic._extract_recent_planning_blocks(story_context)

        # Should return planning blocks in reverse order (most recent first)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["thinking"], "Second planning block")
        self.assertEqual(result[1]["thinking"], "First planning block")

    def test_skips_user_entries(self):
        """Should skip user entries when extracting planning blocks."""
        story_context = [
            {
                constants.KEY_ACTOR: "user",
                constants.KEY_TEXT: "Hello",
            },
            {
                constants.KEY_ACTOR: constants.ACTOR_GEMINI,
                constants.FIELD_PLANNING_BLOCK: {
                    "thinking": "AI response",
                    "choices": [],
                },
            },
        ]

        result = world_logic._extract_recent_planning_blocks(story_context)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["thinking"], "AI response")

    def test_handles_empty_context(self):
        """Should return empty list for empty story context."""
        result = world_logic._extract_recent_planning_blocks([])
        self.assertEqual(result, [])

        result = world_logic._extract_recent_planning_blocks(None)
        self.assertEqual(result, [])


class TestShouldFreezeTimeForSelectedChoice(unittest.TestCase):
    """Test _should_freeze_time_for_selected_choice function."""

    def test_returns_true_for_freeze_time_choice(self):
        """Should return True when user selects a choice with freeze_time=true."""
        story_context = [
            {
                constants.KEY_ACTOR: constants.ACTOR_GEMINI,
                constants.FIELD_PLANNING_BLOCK: {
                    "thinking": "Level up available",
                    "choices": {
                        "level_up_now": {
                            "text": "Level Up to Level 5",
                            "description": "Apply level 5 benefits",
                            "risk_level": "safe",
                            "freeze_time": True,
                        },
                        "continue_adventuring": {
                            "text": "Continue Adventuring",
                            "description": "Level up later",
                            "risk_level": "safe",
                            "freeze_time": True,
                        },
                    },
                },
            },
        ]

        # User selects "Level Up to Level 5"
        result = world_logic._should_freeze_time_for_selected_choice(
            "Level Up to Level 5", story_context
        )
        self.assertTrue(result)

        # User selects "Continue Adventuring"
        result = world_logic._should_freeze_time_for_selected_choice(
            "Continue Adventuring", story_context
        )
        self.assertTrue(result)


class TestFreezeTimeStateChanges(unittest.TestCase):
    """Test centralized freeze-time state change filtering."""

    def test_freeze_time_filters_time_and_preserves_state(self):
        original_world_time = {"microsecond": 41}
        state_changes = {
            "world_data": {
                "world_time": {"hour": 9},
                "timestamp": "2025-01-01T00:00:00Z",
            },
            "player_character_data": {"level": 5},
        }

        result = world_logic._apply_freeze_time_state_changes(
            state_changes,
            original_world_time=original_world_time,
            allow_state_changes=True,
        )

        self.assertEqual(result["player_character_data"]["level"], 5)
        self.assertEqual(result["world_data"]["world_time"]["microsecond"], 42)
        self.assertNotIn("timestamp", result["world_data"])

    def test_freeze_time_blocks_state_when_disallowed(self):
        original_world_time = {"microsecond": 7}
        state_changes = {
            "player_character_data": {"level": 5},
        }

        result = world_logic._apply_freeze_time_state_changes(
            state_changes,
            original_world_time=original_world_time,
            allow_state_changes=False,
        )

        self.assertNotIn("player_character_data", result)
        self.assertEqual(result["world_data"]["world_time"]["microsecond"], 8)

    def test_returns_false_for_non_freeze_time_choice(self):
        """Should return False when user selects a choice without freeze_time."""
        story_context = [
            {
                constants.KEY_ACTOR: constants.ACTOR_GEMINI,
                constants.FIELD_PLANNING_BLOCK: {
                    "thinking": "Combat options",
                    "choices": {
                        "attack": {
                            "text": "Attack the Goblin",
                            "description": "Swing your sword",
                            "risk_level": "medium",
                            # No freeze_time field
                        },
                    },
                },
            },
        ]

        result = world_logic._should_freeze_time_for_selected_choice(
            "Attack the Goblin", story_context
        )
        self.assertFalse(result)

    def test_returns_false_for_freeform_input(self):
        """Should return False for freeform input that doesn't match any choice."""
        story_context = [
            {
                constants.KEY_ACTOR: constants.ACTOR_GEMINI,
                constants.FIELD_PLANNING_BLOCK: {
                    "thinking": "Options",
                    "choices": {
                        "option1": {
                            "text": "Option 1",
                            "description": "First option",
                            "risk_level": "safe",
                            "freeze_time": True,
                        },
                    },
                },
            },
        ]

        # User types something that doesn't match any choice
        result = world_logic._should_freeze_time_for_selected_choice(
            "I do something completely different", story_context
        )
        self.assertFalse(result)

    def test_returns_false_for_empty_context(self):
        """Should return False for empty story context."""
        result = world_logic._should_freeze_time_for_selected_choice("Any input", [])
        self.assertFalse(result)

        result = world_logic._should_freeze_time_for_selected_choice("Any input", None)
        self.assertFalse(result)


class TestGetSelectedChoice(unittest.TestCase):
    """Test document_generator.get_selected_choice function."""

    def test_returns_choice_with_key(self):
        """Should return the choice dict with 'key' field included."""
        planning_blocks = [
            {
                "choices": {
                    "level_up_now": {
                        "text": "Level Up to Level 5",
                        "description": "Apply benefits",
                        "freeze_time": True,
                    }
                }
            }
        ]

        result = document_generator.get_selected_choice(
            "Level Up to Level 5", planning_blocks
        )

        self.assertIsNotNone(result)
        self.assertEqual(result["key"], "level_up_now")
        self.assertEqual(result["text"], "Level Up to Level 5")
        self.assertTrue(result["freeze_time"])

    def test_returns_none_for_freeform_input(self):
        """Should return None when input doesn't match any choice."""
        planning_blocks = [
            {
                "choices": {
                    "option1": {
                        "text": "Option 1",
                        "description": "First option",
                    }
                }
            }
        ]

        result = document_generator.get_selected_choice(
            "Something completely different", planning_blocks
        )

        self.assertIsNone(result)


class TestLevelUpChoiceInjectionHasFreezeTime(unittest.TestCase):
    """Test that level-up choice injection includes freeze_time=true."""

    def test_injected_level_up_now_has_freeze_time(self):
        """Injected level_up_now choice should have freeze_time=true."""
        game_state_dict = {
            "rewards_pending": {
                "level_up_available": True,
                "new_level": 5,
            },
            "player_character_data": {
                "class": "Fighter",
            },
        }

        # Start with empty planning block
        planning_block = {"thinking": "", "choices": {}}

        result = world_logic._inject_levelup_choices_if_needed(
            planning_block, game_state_dict
        )

        choices = result["choices"]
        level_up_now = next(
            (choice for choice in choices if choice.get("id") == "level_up_now"),
            None,
        )
        self.assertIsNotNone(level_up_now)
        self.assertTrue(level_up_now.get("freeze_time"))

    def test_injected_continue_adventuring_has_freeze_time(self):
        """Injected continue_adventuring choice should have freeze_time=true."""
        game_state_dict = {
            "rewards_pending": {
                "level_up_available": True,
                "new_level": 5,
            },
            "player_character_data": {
                "class": "Fighter",
            },
        }

        planning_block = {"thinking": "", "choices": {}}

        result = world_logic._inject_levelup_choices_if_needed(
            planning_block, game_state_dict
        )

        choices = result["choices"]
        continue_adventuring = next(
            (
                choice
                for choice in choices
                if choice.get("id") == "continue_adventuring"
            ),
            None,
        )
        self.assertIsNotNone(continue_adventuring)
        self.assertTrue(continue_adventuring.get("freeze_time"))

    def test_existing_levelup_choices_enforce_freeze_time_true(self):
        """Existing level-up choices should always be forced to freeze_time=true."""
        game_state_dict = {
            "rewards_pending": {
                "level_up_available": True,
                "new_level": 5,
            },
            "player_character_data": {
                "class": "Fighter",
            },
        }

        # LLM provided the required choice IDs but forgot freeze_time (or set it false).
        planning_block = {
            "thinking": "",
            "choices": {
                "level_up_now": {
                    "text": "Level Up to Level 5",
                    "description": "Apply benefits",
                },
                "continue_adventuring": {
                    "text": "Continue Adventuring",
                    "description": "Level up later",
                    "freeze_time": False,
                },
            },
        }

        result = world_logic._inject_levelup_choices_if_needed(
            planning_block, game_state_dict
        )

        choices = result["choices"]
        level_up_now = next(
            (choice for choice in choices if choice.get("id") == "level_up_now"),
            None,
        )
        continue_adventuring = next(
            (
                choice
                for choice in choices
                if choice.get("id") == "continue_adventuring"
            ),
            None,
        )
        self.assertIsNotNone(level_up_now)
        self.assertIsNotNone(continue_adventuring)
        self.assertTrue(level_up_now["freeze_time"])
        self.assertTrue(continue_adventuring["freeze_time"])


class TestModalFinishChoiceInjection(unittest.TestCase):
    """Test server-side modal finish choice injection and ordering."""

    def test_character_creation_finish_choice_injected_last(self):
        game_state_dict = {
            "custom_campaign_state": {
                "character_creation_in_progress": True,
                "character_creation_stage": "mechanics",
            }
        }
        planning_block = {
            "thinking": "Pick a class.",
            "choices": {
                "choose_class": {
                    "text": "Choose Class",
                    "description": "Pick your class.",
                },
            },
        }

        result = world_logic._inject_modal_finish_choice_if_needed(
            planning_block, game_state_dict
        )

        self.assertIsInstance(result, dict)
        choices = result["choices"]
        self.assertIsInstance(choices, list)
        self.assertEqual(choices[-1]["id"], "finish_character_creation_start_game")
        self.assertEqual(
            choices[-1]["text"],
            "Finish Character Creation and Start Game",
        )

    def test_level_up_finish_choice_injected_last(self):
        game_state_dict = {
            "custom_campaign_state": {
                "character_creation_in_progress": True,
                "character_creation_stage": "level_up",
                "level_up_in_progress": True,
            }
        }
        planning_block = {
            "thinking": "Choose feat.",
            "choices": {
                "adjust_choices": {
                    "text": "Adjust my level-up choices",
                    "description": "Change current picks.",
                },
            },
        }

        result = world_logic._inject_modal_finish_choice_if_needed(
            planning_block, game_state_dict
        )

        self.assertIsInstance(result, dict)
        choices = result["choices"]
        self.assertIsInstance(choices, list)
        self.assertEqual(choices[-1]["id"], "finish_level_up_return_to_game")
        self.assertEqual(
            choices[-1]["text"],
            "Finish Level-Up and Return to Game",
        )



class TestFreezeTimeMicrosecondTick(unittest.TestCase):
    """Test microsecond tick behavior for freeze_time choices."""

    def test_freeze_time_microsecond_tick_does_not_wrap(self):
        """When microsecond is already maxed, do not wrap backward to 0."""
        result = world_logic._filter_time_changes_for_freeze_time_choice(
            {"world_data": {"world_time": {"hour": 10, "microsecond": 999_999}}},
            original_world_time={"microsecond": 999_999},
        )
        self.assertEqual(
            result["world_data"]["world_time"]["microsecond"],
            999_999,
        )

    def test_freeze_time_microsecond_tick_increments(self):
        """When microsecond is below max, increment by 1."""
        result = world_logic._filter_time_changes_for_freeze_time_choice(
            {"world_data": {"world_time": {"hour": 10, "microsecond": 41}}},
            original_world_time={"microsecond": 41},
        )
        self.assertEqual(result["world_data"]["world_time"]["microsecond"], 42)


if __name__ == "__main__":
    unittest.main()

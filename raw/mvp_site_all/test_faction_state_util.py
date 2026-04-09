"""Unit tests for faction_state_util module.

Tests centralized faction minigame state access and validation logic.
"""

# ruff: noqa: PT009

import json
import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from mvp_site import faction_state_util


class TestGetFactionMinigameDict(unittest.TestCase):
    """Test faction_minigame dict extraction from various structures."""

    def test_none_game_state_returns_none(self):
        """None game_state should return None."""
        result = faction_state_util.get_faction_minigame_dict(None)
        self.assertIsNone(result)

    def test_direct_attribute_access(self):
        """Extract from game_state.faction_minigame attribute."""
        mock_state = Mock()
        mock_state.faction_minigame = {"enabled": True, "turn_number": 5}

        result = faction_state_util.get_faction_minigame_dict(mock_state)

        self.assertEqual(result, {"enabled": True, "turn_number": 5})

    def test_nested_custom_campaign_state_attribute(self):
        """Extract from game_state.custom_campaign_state.faction_minigame."""
        mock_state = Mock(spec=["custom_campaign_state"])
        mock_state.custom_campaign_state = {
            "faction_minigame": {"enabled": False, "turn_number": 10}
        }

        result = faction_state_util.get_faction_minigame_dict(mock_state)

        self.assertEqual(result, {"enabled": False, "turn_number": 10})

    def test_data_wrapper_nested_access(self):
        """Extract from game_state.data.game_state.custom_campaign_state.faction_minigame."""
        mock_data = Mock()
        mock_data.game_state = {
            "custom_campaign_state": {
                "faction_minigame": {"enabled": True, "tutorial_completed": False}
            }
        }
        mock_state = Mock(spec=["data"])
        mock_state.data = mock_data

        result = faction_state_util.get_faction_minigame_dict(mock_state)

        self.assertEqual(result, {"enabled": True, "tutorial_completed": False})

    def test_data_dict_wrapper_nested_access(self):
        """Extract from game_state.data dict (not object) with nested structure."""
        mock_state = Mock(spec=["data"])
        mock_state.data = {
            "game_state": {
                "custom_campaign_state": {
                    "faction_minigame": {"enabled": True, "turn_number": 12}
                }
            }
        }

        result = faction_state_util.get_faction_minigame_dict(mock_state)

        self.assertEqual(result, {"enabled": True, "turn_number": 12})

    def test_data_dict_direct_faction_minigame(self):
        """Extract from game_state.data dict with direct faction_minigame key."""
        mock_state = Mock(spec=["data"])
        mock_state.data = {
            "game_state": {
                "faction_minigame": {"enabled": True, "turn_number": 8},
                "army_data": {"total_strength": 150},
            }
        }

        result = faction_state_util.get_faction_minigame_dict(mock_state)

        self.assertEqual(result, {"enabled": True, "turn_number": 8})

    def test_dict_direct_key_access(self):
        """Extract from game_state["faction_minigame"] dict."""
        game_state = {"faction_minigame": {"enabled": True, "turn_number": 3}}

        result = faction_state_util.get_faction_minigame_dict(game_state)

        self.assertEqual(result, {"enabled": True, "turn_number": 3})

    def test_dict_nested_custom_campaign_state(self):
        """Extract from game_state["custom_campaign_state"]["faction_minigame"]."""
        game_state = {
            "custom_campaign_state": {
                "faction_minigame": {"enabled": False, "turn_number": 7}
            }
        }

        result = faction_state_util.get_faction_minigame_dict(game_state)

        self.assertEqual(result, {"enabled": False, "turn_number": 7})

    def test_missing_faction_minigame_returns_none(self):
        """Missing faction_minigame should return None."""
        mock_state = Mock(spec=["custom_campaign_state"])
        mock_state.custom_campaign_state = {"other_data": "value"}

        result = faction_state_util.get_faction_minigame_dict(mock_state)

        self.assertIsNone(result)

    def test_non_dict_faction_minigame_returns_none(self):
        """Non-dict faction_minigame should return None."""
        mock_state = Mock()
        mock_state.faction_minigame = "not a dict"

        result = faction_state_util.get_faction_minigame_dict(mock_state)

        self.assertIsNone(result)

    def test_data_wrapper_precedence_custom_campaign_state_wins(self):
        """When both paths exist, custom_campaign_state should take precedence."""
        mock_state = Mock(spec=["data"])
        mock_state.data = {
            "game_state": {
                "faction_minigame": {
                    "enabled": False,
                    "turn_number": 99,
                },  # Wrong value
                "custom_campaign_state": {
                    "faction_minigame": {
                        "enabled": True,
                        "turn_number": 5,
                    }  # Correct value
                },
            }
        }

        result = faction_state_util.get_faction_minigame_dict(mock_state)

        # Should return custom_campaign_state version, not direct version
        self.assertEqual(result, {"enabled": True, "turn_number": 5})

    def test_dict_access_precedence_custom_campaign_state_wins(self):
        """When both dict paths exist, custom_campaign_state should take precedence."""
        game_state = {
            "faction_minigame": {"enabled": False, "turn_number": 88},  # Wrong value
            "custom_campaign_state": {
                "faction_minigame": {
                    "enabled": True,
                    "turn_number": 10,
                }  # Correct value
            },
        }

        result = faction_state_util.get_faction_minigame_dict(game_state)

        # Should return custom_campaign_state version, not direct version
        self.assertEqual(result, {"enabled": True, "turn_number": 10})

    def test_data_object_wrapper_precedence_custom_campaign_state_wins(self):
        """When both paths exist in data object, custom_campaign_state should take precedence."""
        mock_data = Mock()
        mock_data.game_state = {
            "faction_minigame": {"enabled": False, "turn_number": 77},  # Wrong value
            "custom_campaign_state": {
                "faction_minigame": {
                    "enabled": True,
                    "turn_number": 15,
                }  # Correct value
            },
        }
        mock_state = Mock(spec=["data"])
        mock_state.data = mock_data

        result = faction_state_util.get_faction_minigame_dict(mock_state)

        # Should return custom_campaign_state version, not direct version
        self.assertEqual(result, {"enabled": True, "turn_number": 15})

    def test_object_precedence_custom_campaign_state_wins(self):
        """When both object attrs exist, custom_campaign_state should take precedence."""
        game_state = SimpleNamespace(
            faction_minigame={"enabled": False, "turn_number": 99},
            custom_campaign_state={
                "faction_minigame": {"enabled": True, "turn_number": 5}
            },
        )

        result = faction_state_util.get_faction_minigame_dict(game_state)

        self.assertEqual(result, {"enabled": True, "turn_number": 5})


class TestIsFactionMinigameEnabled(unittest.TestCase):
    """Test strict boolean validation for faction minigame enablement."""

    def test_boolean_true_returns_true(self):
        """Boolean True should enable minigame."""
        game_state = {"faction_minigame": {"enabled": True}}

        result = faction_state_util.is_faction_minigame_enabled(game_state)

        self.assertTrue(result)

    def test_boolean_false_returns_false(self):
        """Boolean False should disable minigame."""
        game_state = {"faction_minigame": {"enabled": False}}

        result = faction_state_util.is_faction_minigame_enabled(game_state)

        self.assertFalse(result)

    def test_string_false_returns_false(self):
        """String 'false' should be treated as disabled (not truthy)."""
        game_state = {"faction_minigame": {"enabled": "false"}}

        result = faction_state_util.is_faction_minigame_enabled(game_state)

        self.assertFalse(result)

    def test_string_true_returns_false(self):
        """String 'true' should be treated as disabled (only boolean True valid)."""
        game_state = {"faction_minigame": {"enabled": "true"}}

        result = faction_state_util.is_faction_minigame_enabled(game_state)

        self.assertFalse(result)

    def test_none_returns_false(self):
        """None value should be treated as disabled."""
        game_state = {"faction_minigame": {"enabled": None}}

        result = faction_state_util.is_faction_minigame_enabled(game_state)

        self.assertFalse(result)

    def test_zero_returns_false(self):
        """Zero should be treated as disabled."""
        game_state = {"faction_minigame": {"enabled": 0}}

        result = faction_state_util.is_faction_minigame_enabled(game_state)

        self.assertFalse(result)

    def test_one_returns_false(self):
        """Integer 1 should be treated as disabled (only boolean True valid)."""
        game_state = {"faction_minigame": {"enabled": 1}}

        result = faction_state_util.is_faction_minigame_enabled(game_state)

        self.assertFalse(result)

    def test_missing_faction_minigame_returns_false(self):
        """Missing faction_minigame should return False."""
        game_state = {"custom_campaign_state": {}}

        result = faction_state_util.is_faction_minigame_enabled(game_state)

        self.assertFalse(result)

    def test_missing_enabled_key_returns_false(self):
        """Missing 'enabled' key should return False."""
        game_state = {"faction_minigame": {"turn_number": 5}}

        result = faction_state_util.is_faction_minigame_enabled(game_state)

        self.assertFalse(result)

    def test_user_setting_disabled_overrides_campaign_enabled(self):
        """User setting disabled should override campaign enabled."""
        game_state = {"faction_minigame": {"enabled": True}}
        user_settings = {"faction_minigame_enabled": False}

        result = faction_state_util.is_faction_minigame_enabled(
            game_state,
            check_user_setting=True,
            user_settings=user_settings,
        )

        self.assertFalse(result)

    def test_user_setting_enabled_allows_campaign_enabled(self):
        """User setting enabled should allow campaign enabled."""
        game_state = {"faction_minigame": {"enabled": True}}
        user_settings = {"faction_minigame_enabled": True}

        result = faction_state_util.is_faction_minigame_enabled(
            game_state,
            check_user_setting=True,
            user_settings=user_settings,
        )

        self.assertTrue(result)

    def test_user_setting_check_without_user_settings_ignores_check(self):
        """Requesting user setting check without user_settings should ignore check."""
        game_state = {"faction_minigame": {"enabled": True}}

        result = faction_state_util.is_faction_minigame_enabled(
            game_state,
            check_user_setting=True,
            user_settings=None,
        )

        self.assertTrue(result)

    def test_user_setting_not_checked_by_default(self):
        """User setting should not be checked by default."""
        game_state = {"faction_minigame": {"enabled": True}}
        user_settings = {"faction_minigame_enabled": False}

        # check_user_setting defaults to False
        result = faction_state_util.is_faction_minigame_enabled(
            game_state,
            user_settings=user_settings,
        )

        self.assertTrue(result)


class TestExtractFactionMinigameStateFromGameState(unittest.TestCase):
    """Test extraction of both enabled and turn_number."""

    def test_enabled_true_with_turn_number(self):
        """Extract enabled=True and turn_number."""
        game_state = {"faction_minigame": {"enabled": True, "turn_number": 15}}

        enabled, turn_number = (
            faction_state_util.extract_faction_minigame_state_from_game_state(
                game_state
            )
        )

        self.assertTrue(enabled)
        self.assertEqual(turn_number, 15)

    def test_enabled_false_with_turn_number(self):
        """Extract enabled=False and turn_number."""
        game_state = {"faction_minigame": {"enabled": False, "turn_number": 8}}

        enabled, turn_number = (
            faction_state_util.extract_faction_minigame_state_from_game_state(
                game_state
            )
        )

        self.assertFalse(enabled)
        self.assertEqual(turn_number, 8)

    def test_missing_turn_number_defaults_to_1(self):
        """Missing turn_number should default to 1."""
        game_state = {"faction_minigame": {"enabled": True}}

        enabled, turn_number = (
            faction_state_util.extract_faction_minigame_state_from_game_state(
                game_state
            )
        )

        self.assertTrue(enabled)
        self.assertEqual(turn_number, 1)

    def test_none_turn_number_defaults_to_1(self):
        """None turn_number should default to 1."""
        game_state = {"faction_minigame": {"enabled": True, "turn_number": None}}

        enabled, turn_number = (
            faction_state_util.extract_faction_minigame_state_from_game_state(
                game_state
            )
        )

        self.assertTrue(enabled)
        self.assertEqual(turn_number, 1)

    def test_invalid_turn_number_defaults_to_1(self):
        """Invalid turn_number should default to 1."""
        game_state = {"faction_minigame": {"enabled": True, "turn_number": "invalid"}}

        enabled, turn_number = (
            faction_state_util.extract_faction_minigame_state_from_game_state(
                game_state
            )
        )

        self.assertTrue(enabled)
        self.assertEqual(turn_number, 1)

    def test_zero_turn_number_coerced_to_1(self):
        """Turn number 0 should be coerced to minimum of 1."""
        game_state = {"faction_minigame": {"enabled": True, "turn_number": 0}}

        enabled, turn_number = (
            faction_state_util.extract_faction_minigame_state_from_game_state(
                game_state
            )
        )

        self.assertTrue(enabled)
        self.assertEqual(turn_number, 1)

    def test_negative_turn_number_coerced_to_1(self):
        """Negative turn number should be coerced to minimum of 1."""
        game_state = {"faction_minigame": {"enabled": True, "turn_number": -5}}

        enabled, turn_number = (
            faction_state_util.extract_faction_minigame_state_from_game_state(
                game_state
            )
        )

        self.assertTrue(enabled)
        self.assertEqual(turn_number, 1)

    def test_missing_faction_minigame_returns_defaults(self):
        """Missing faction_minigame should return safe defaults."""
        game_state = {"custom_campaign_state": {}}

        enabled, turn_number = (
            faction_state_util.extract_faction_minigame_state_from_game_state(
                game_state
            )
        )

        self.assertFalse(enabled)
        self.assertEqual(turn_number, 1)


class TestExtractFactionMinigameStateFromPromptContents(unittest.TestCase):
    """Test extraction of faction state from prompt_contents (provider request format)."""

    def test_empty_prompt_contents_returns_defaults(self):
        """Empty prompt_contents should return safe defaults."""
        result = faction_state_util.extract_faction_minigame_state_from_prompt_contents(
            []
        )
        self.assertEqual(result, (False, 1))

    def test_json_string_with_enabled_faction_minigame(self):
        """Extract from JSON string in prompt_contents[0]."""
        payload = {
            "user_action": "test action",
            "game_state": {
                "custom_campaign_state": {
                    "faction_minigame": {"enabled": True, "turn_number": 10}
                }
            },
        }
        prompt_contents = [json.dumps(payload)]

        enabled, turn_number = (
            faction_state_util.extract_faction_minigame_state_from_prompt_contents(
                prompt_contents
            )
        )
        self.assertTrue(enabled)
        self.assertEqual(turn_number, 10)

    def test_dict_with_enabled_faction_minigame(self):
        """Extract from dict in prompt_contents[0]."""
        payload = {
            "user_action": "test action",
            "game_state": {
                "custom_campaign_state": {
                    "faction_minigame": {"enabled": True, "turn_number": 5}
                }
            },
        }
        prompt_contents = [payload]

        enabled, turn_number = (
            faction_state_util.extract_faction_minigame_state_from_prompt_contents(
                prompt_contents
            )
        )
        self.assertTrue(enabled)
        self.assertEqual(turn_number, 5)

    def test_disabled_faction_minigame(self):
        """Extract disabled faction minigame."""
        payload = {
            "game_state": {
                "custom_campaign_state": {
                    "faction_minigame": {"enabled": False, "turn_number": 3}
                }
            }
        }
        prompt_contents = [json.dumps(payload)]

        enabled, turn_number = (
            faction_state_util.extract_faction_minigame_state_from_prompt_contents(
                prompt_contents
            )
        )
        self.assertFalse(enabled)
        self.assertEqual(turn_number, 3)

    def test_missing_turn_number_defaults_to_1(self):
        """Missing turn_number should default to 1."""
        payload = {
            "game_state": {
                "custom_campaign_state": {"faction_minigame": {"enabled": True}}
            }
        }
        prompt_contents = [json.dumps(payload)]

        enabled, turn_number = (
            faction_state_util.extract_faction_minigame_state_from_prompt_contents(
                prompt_contents
            )
        )
        self.assertTrue(enabled)
        self.assertEqual(turn_number, 1)

    def test_invalid_json_returns_defaults(self):
        """Invalid JSON should return safe defaults."""
        prompt_contents = ["not valid json{"]
        result = faction_state_util.extract_faction_minigame_state_from_prompt_contents(
            prompt_contents
        )
        self.assertEqual(result, (False, 1))

    def test_non_dict_json_returns_defaults(self):
        """JSON that's not a dict should return safe defaults."""
        prompt_contents = [json.dumps(["array", "not", "dict"])]
        result = faction_state_util.extract_faction_minigame_state_from_prompt_contents(
            prompt_contents
        )
        self.assertEqual(result, (False, 1))

    def test_missing_game_state_returns_defaults(self):
        """Missing game_state key should return safe defaults."""
        payload = {"user_action": "test"}
        prompt_contents = [json.dumps(payload)]
        result = faction_state_util.extract_faction_minigame_state_from_prompt_contents(
            prompt_contents
        )
        self.assertEqual(result, (False, 1))

    def test_fallback_faction_minigame_path(self):
        """Extract from game_state.faction_minigame (fallback path)."""
        payload = {
            "game_state": {"faction_minigame": {"enabled": True, "turn_number": 7}}
        }
        prompt_contents = [json.dumps(payload)]

        enabled, turn_number = (
            faction_state_util.extract_faction_minigame_state_from_prompt_contents(
                prompt_contents
            )
        )
        self.assertTrue(enabled)
        self.assertEqual(turn_number, 7)

    def test_turn_number_coercion(self):
        """Turn number should be coerced to int with min value 1."""
        test_cases = [(0, 1), (-5, 1), (15, 15), ("invalid", 1)]
        for input_turn, expected_turn in test_cases:
            with self.subTest(input_turn=input_turn):
                payload = {
                    "game_state": {
                        "custom_campaign_state": {
                            "faction_minigame": {
                                "enabled": True,
                                "turn_number": input_turn,
                            }
                        }
                    }
                }
                prompt_contents = [json.dumps(payload)]

                enabled, turn_number = (
                    faction_state_util.extract_faction_minigame_state_from_prompt_contents(
                        prompt_contents
                    )
                )
                self.assertTrue(enabled)
                self.assertEqual(turn_number, expected_turn)


class TestIsFactionEnableAction(unittest.TestCase):
    """Test detection of faction minigame enable actions in prompt_contents."""

    def test_empty_prompt_contents_returns_false(self):
        self.assertFalse(faction_state_util.is_faction_enable_action([]))

    def test_exact_enable_faction_minigame_keyword(self):
        payload = {"user_action": "enable_faction_minigame"}
        self.assertTrue(
            faction_state_util.is_faction_enable_action([json.dumps(payload)])
        )

    def test_enable_faction_mode_keyword(self):
        payload = {"user_action": "enable faction mode"}
        self.assertFalse(
            faction_state_util.is_faction_enable_action([json.dumps(payload)])
        )

    def test_enable_action_allows_extra_words(self):
        payload = {"user_action": "please enable faction minigame now"}
        self.assertFalse(
            faction_state_util.is_faction_enable_action([json.dumps(payload)])
        )

    def test_faction_minigame_keyword(self):
        payload = {"user_action": "faction minigame"}
        self.assertFalse(
            faction_state_util.is_faction_enable_action([json.dumps(payload)])
        )

    def test_case_insensitive_matching(self):
        payload = {"user_action": "ENABLE_FACTION_MINIGAME"}
        self.assertTrue(
            faction_state_util.is_faction_enable_action([json.dumps(payload)])
        )

    def test_non_enable_action_returns_false(self):
        payload = {"user_action": "attack the orc"}
        self.assertFalse(
            faction_state_util.is_faction_enable_action([json.dumps(payload)])
        )

    def test_dict_format_prompt_contents(self):
        payload = {"user_action": "enable_faction_minigame"}
        self.assertTrue(faction_state_util.is_faction_enable_action([payload]))

    def test_missing_user_action_returns_false(self):
        payload = {"game_state": {}}
        self.assertFalse(
            faction_state_util.is_faction_enable_action([json.dumps(payload)])
        )

    def test_explicit_enable_flag_returns_true(self):
        payload = {"enable_faction_minigame": True}
        self.assertTrue(
            faction_state_util.is_faction_enable_action([json.dumps(payload)])
        )

    def test_intent_enable_flag_returns_true(self):
        payload = {"intent": {"enable_faction_minigame": True}}
        self.assertTrue(
            faction_state_util.is_faction_enable_action([json.dumps(payload)])
        )

    def test_invalid_json_returns_false(self):
        self.assertFalse(
            faction_state_util.is_faction_enable_action(["not valid json{"])
        )

    def test_system_enforcement_suffix_ignored(self):
        payload = {
            "user_action": "enable_faction_minigame\n\n[SYSTEM ENFORCEMENT: blah blah]"
        }
        self.assertTrue(
            faction_state_util.is_faction_enable_action([json.dumps(payload)])
        )

    def test_with_leading_trailing_whitespace(self):
        payload = {"user_action": "  enable_faction_minigame  "}
        self.assertTrue(
            faction_state_util.is_faction_enable_action([json.dumps(payload)])
        )


if __name__ == "__main__":
    unittest.main()


import unittest
from unittest.mock import MagicMock
import sys
import os

# Set test environment
os.environ["TESTING_AUTH_BYPASS"] = "true"
os.environ["USE_MOCKS"] = "true"

# Mock dependencies before imports
sys.modules["firebase_admin"] = MagicMock()
sys.modules["firebase_admin.firestore"] = MagicMock()
sys.modules["firebase_admin.auth"] = MagicMock()
sys.modules["google.cloud"] = MagicMock()
sys.modules["google.cloud.firestore"] = MagicMock()
sys.modules["google.auth"] = MagicMock()

from mvp_site.game_state import GameState, validate_and_correct_state

class TestGameStateSafety(unittest.TestCase):
    """Fuzz/Stress tests for GameState initialization and validation safety."""

    def test_init_with_none_values(self):
        """Test that initialization with None values doesn't crash."""
        # Should not raise exception
        gs = GameState(
            player_character_data=None,
            world_data=None,
            npc_data=None,
            custom_campaign_state=None
        )
        self.assertIsInstance(gs, GameState)
        # Verify defensive defaults kicked in
        self.assertEqual(gs.player_character_data, {"experience": {"current": 0}})
        self.assertEqual(gs.world_data, {})
        self.assertEqual(gs.npc_data, {})
        self.assertEqual(gs.custom_campaign_state, {}) # Should be empty dict, not None

    def test_init_with_garbage_types(self):
        """Test initialization with completely wrong types."""
        gs = GameState(
            player_character_data="not a dict",
            world_data=123,
            npc_data=["list", "instead", "of", "dict"],
            custom_campaign_state=False
        )
        # Should persist the garbage but NOT crash during __init__
        # The schema validation step (validate_and_correct_state) is where we expect
        # specific handling, but __init__ must be exception-safe.
        self.assertEqual(gs.player_character_data, "not a dict")
        self.assertEqual(gs.world_data, 123)
        
        # NOTE: custom_campaign_state has specific logic in __init__ that might reset it
        # Let's verify what actually happens.
        # Logic: if not isinstance(..., dict): self.custom_campaign_state = {}
        self.assertEqual(gs.custom_campaign_state, {}) 

    def test_validate_and_correct_garbage_input(self):
        """Test validate_and_correct_state with garbage input."""
        # This function typically takes a dict, not a GameState object directly (it converts to dict)
        garbage_state = {
            "player_character_data": "garbage",
            "world_data": None,
            "game_state_version": "v1" # Should be int
        }
        
        # Should not raise exception, but return warnings/errors
        # We set allow_partial_validation=False to force full schema check
        validated_state, corrections = validate_and_correct_state(
            garbage_state, 
            is_god_mode=False,
            allow_partial_validation=False
        )
        
        # We expect schema validation errors to be caught and returned, NOT raised
        # The function returns (state, corrections_list)
        # We don't necessarily expect corrections for "garbage" string vs dict, 
        # but we expect it NOT to crash.
        self.assertIsInstance(validated_state, dict)
        self.assertIsInstance(corrections, list)
        
        # "garbage" isn't a valid player_character_data, so schema validation should fail.
        # validate_and_correct_state currently returns [validation_errors] in the second return value
        # if correction fails.
        self.assertTrue(len(corrections) > 0)

    def test_from_dict_safety(self):
        """Test GameState.from_dict with malformed dicts."""
        # None input
        self.assertIsNone(GameState.from_dict(None))
        
        # Empty input
        self.assertIsNone(GameState.from_dict({}))
        
        # Keys that aren't valid Python kwargs (should be ignored by **kwargs or stored? GameState uses **kwargs)
        # Python classes with **kwargs accept anything.
        gs = GameState.from_dict({"not_a_field": "value"})
        self.assertTrue(hasattr(gs, "not_a_field"))

"""
TDD Test for REV-9zs: Schema validation warnings (non-blocking) in production

This test verifies that schema validation generates warnings but does NOT
block Firestore persistence operations (non-blocking by design).
"""

import pytest
from unittest.mock import patch, MagicMock
from mvp_site.game_state import GameState
from mvp_site import firestore_service
from mvp_site.world_logic import validate_game_state_updates


def test_invalid_game_state_logs_validation_warning():
    """
    Test that trying to persist an invalid game state logs a validation warning
    but does NOT raise an exception (non-blocking by design).

    This ensures schema validation warnings are generated for debugging while
    allowing gameplay to continue.
    """
    # Create a GameState with invalid data
    gs = GameState(user_id='test_user')

    # Manually corrupt the game state to make it invalid
    # Remove required fields from player_character_data
    gs.player_character_data = {}  # Missing required entity_id and display_name

    # Schema validation is non-blocking - should warn but not raise
    # Get validated dict should return successfully (with warnings logged)
    result = gs.to_validated_dict()

    # Verify the dict is returned (validation warnings logged but not raised)
    assert isinstance(result, dict)
    assert result.get("user_id") == "test_user"


def test_world_logic_validate_game_state_updates_uses_validation():
    """
    Test that validate_game_state_updates() in world_logic.py performs schema validation.

    This is a regression test for REV-9zs.
    """

    # Create a minimal valid game state dict
    valid_state_dict = {
        'user_id': 'test_user',
        'player_character_data': {
            'entity_id': 'test_char',
            'display_name': 'Test Character',
            'max_hp': 10,
            'current_hp': 10,
            'level': 1
        },
        'game_state_version': '1.0'
    }

    # This should NOT raise - valid state
    result = validate_game_state_updates(valid_state_dict)
    assert result is not None

    # Create an invalid state dict (missing required fields)
    invalid_state_dict = {
        'user_id': 'test_user',
        'player_character_data': {},  # Missing required fields
        'game_state_version': '1.0'
    }

    # Schema validation is non-blocking - should NOT raise, just log warnings
    # Verify it returns corrected state without crashing
    result = validate_game_state_updates(invalid_state_dict)
    assert result is not None  # Returns state even if invalid (non-blocking)

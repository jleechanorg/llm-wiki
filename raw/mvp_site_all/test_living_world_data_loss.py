"""
TDD Test for REV-a73: Living World data loss in to_model/from_model round-trip

This test verifies that last_living_world_turn and last_living_world_time
are preserved through the to_model()/from_model() round-trip.
"""

import pytest
from mvp_site.game_state import GameState


def test_living_world_fields_preserved_in_model_round_trip():
    """
    Test that last_living_world_turn and last_living_world_time are preserved
    through to_model() -> from_model() round-trip.

    This is a regression test for REV-a73.
    """
    # Create a GameState with living world tracking data
    original_gs = GameState(user_id='test_user')
    original_gs.player_character_data = {
        'entity_id': 'test_char',
        'display_name': 'Test Character',
        'max_hp': 10,
        'current_hp': 10,
        'level': 1
    }

    # Set living world tracking fields
    original_gs.last_living_world_turn = 42
    original_gs.last_living_world_time = {
        'day': 10,
        'hour': 14,
        'minute': 30,
        'second': 0,
        'microsecond': 0,
        'time_of_day': 'afternoon',
        'season': 'summer'
    }

    # Convert to model and back
    model = original_gs.to_model()
    restored_gs = GameState.from_model(model)

    # Verify living world fields are preserved
    assert restored_gs.last_living_world_turn == 42, \
        "last_living_world_turn should be preserved through round-trip"

    assert restored_gs.last_living_world_time is not None, \
        "last_living_world_time should not be None after round-trip"

    assert restored_gs.last_living_world_time['day'] == 10, \
        "last_living_world_time.day should be preserved"

    assert restored_gs.last_living_world_time['hour'] == 14, \
        "last_living_world_time.hour should be preserved"


def test_living_world_fields_in_to_dict():
    """
    Verify that last_living_world fields are included in to_dict() output.
    """
    gs = GameState(user_id='test_user')
    gs.last_living_world_turn = 100
    gs.last_living_world_time = {'day': 5, 'hour': 12}

    data = gs.to_dict()

    assert 'last_living_world_turn' in data, \
        "last_living_world_turn should be in to_dict() output"
    assert data['last_living_world_turn'] == 100

    assert 'last_living_world_time' in data, \
        "last_living_world_time should be in to_dict() output"
    assert data['last_living_world_time']['day'] == 5

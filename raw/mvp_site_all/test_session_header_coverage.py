"""
Test coverage for session_header_utils.py edge cases.
Addresses missing coverage identified in PR #3746.
"""


def test_coerce_int_edge_cases():
    """Test _coerce_int handles None, str, float, bool correctly."""
    from mvp_site.session_header_utils import _coerce_int

    # None returns default
    assert _coerce_int(None, 5) == 5
    assert _coerce_int(None) == 0

    # Valid int returns value
    assert _coerce_int(42) == 42

    # Bool (subclass of int) — coerce_int_safe converts bool to int
    assert _coerce_int(True) == 1  # int(True) == 1
    assert _coerce_int(False) == 0  # int(False) == 0

    # Valid numeric string
    assert _coerce_int("123") == 123

    # Invalid string returns default
    assert _coerce_int("not_a_number") == 0
    assert _coerce_int("") == 0

    # Float returns int
    assert _coerce_int(3.7) == 3
    assert _coerce_int(9.9) == 9


def test_get_player_character_data_fallbacks():
    """Test _get_player_character_data handles various game_state formats."""
    from mvp_site.session_header_utils import _get_player_character_data

    # Dict with player_character_data
    state = {"player_character_data": {"hp_current": 10}}
    assert _get_player_character_data(state) == {"hp_current": 10}

    # Object with player_character_data attribute
    class GameState:
        def __init__(self):
            self.player_character_data = {"hp_current": 20}

    assert _get_player_character_data(GameState()) == {"hp_current": 20}

    # Empty dict
    assert _get_player_character_data({}) == {}

    # Dict with None player_character_data
    assert _get_player_character_data({"player_character_data": None}) == {}

    # Object without player_character_data
    class EmptyState:
        pass

    assert _get_player_character_data(EmptyState()) == {}


def test_normalize_dict_with_conditions_and_resources():
    """Test normalize_session_header handles dict format with Conditions/Resources."""
    from mvp_site.session_header_utils import normalize_session_header

    dict_header = '{"Timestamp": "1492 DR", "Location": "Dungeon", "Status": "Lvl 1", "Conditions": "Poisoned", "Resources": "HD: 1/1"}'
    result = normalize_session_header(dict_header)

    assert "[SESSION_HEADER]" in result
    assert "Timestamp: 1492 DR" in result
    assert "Location: Dungeon" in result
    assert "Status: Lvl 1" in result
    assert "Conditions: Poisoned" in result
    assert "Resources: HD: 1/1" in result


def test_normalize_invalid_json_dict_format():
    """Test normalize_session_header handles invalid JSON gracefully."""
    from mvp_site.session_header_utils import normalize_session_header

    # Malformed JSON starting with { should not crash
    invalid_json = '{"Timestamp": "1492 DR", invalid}'
    result = normalize_session_header(invalid_json)

    # Should add prefix even if JSON parsing fails
    assert "[SESSION_HEADER]" in result


def test_generate_fallback_hit_dice_uses_total_fallback():
    """Test generate_session_header_fallback uses hit_dice.total when .max missing."""
    from mvp_site.session_header_utils import generate_session_header_fallback

    game_state = {
        "player_character_data": {
            "level": 3,
            "class": "Rogue",
            "hp_current": 18,
            "hp_max": 24,
            "resources": {
                "hit_dice": {"used": 1, "total": 3}  # No "max" key, should use "total"
            },
        },
        "world_data": {"current_location": "Tavern", "current_time": "Unknown"},
    }

    result = generate_session_header_fallback(game_state)

    assert "HD: 2/3" in result  # current = total - used = 3 - 1 = 2


def test_generate_fallback_class_features():
    """Test generate_session_header_fallback includes class features."""
    from mvp_site.session_header_utils import generate_session_header_fallback

    game_state = {
        "player_character_data": {
            "level": 5,
            "class": "Bard",
            "hp_current": 30,
            "hp_max": 30,
            "resources": {
                "hit_dice": {"used": 0, "max": 5},
                "class_features": {
                    "bardic_inspiration": {"used": 2, "max": 4},
                    "song_of_rest": {"used": 0, "max": 1},
                },
            },
        },
        "world_data": {},
    }

    result = generate_session_header_fallback(game_state)

    assert "Bardic Inspiration: 2/4" in result
    assert "Song Of Rest: 1/1" in result


def test_generate_fallback_with_none_resource_values():
    """Test generate_session_header_fallback handles None in used/max values (prevents TypeError)."""
    from mvp_site.session_header_utils import generate_session_header_fallback

    game_state = {
        "player_character_data": {
            "level": 2,
            "class": "Wizard",
            "hp_current": 12,
            "hp_max": 12,
            "resources": {
                "hit_dice": {"used": None, "max": 2},  # None should be coerced to 0
                "spell_slots": {"level_1": {"used": None, "max": 3}},
            },
        },
        "world_data": {},
    }

    result = generate_session_header_fallback(game_state)

    # Should not crash with TypeError, should treat None as 0
    assert "HD: 2/2" in result  # 2 - 0 = 2
    assert "L1 3/3" in result  # 3 - 0 = 3


def test_generate_fallback_empty_resources_shows_none():
    """Test generate_session_header_fallback shows 'Resources: None' when empty."""
    from mvp_site.session_header_utils import generate_session_header_fallback

    game_state = {
        "player_character_data": {
            "level": 1,
            "class": "Fighter",
            "hp_current": 10,
            "hp_max": 10,
            "resources": {},  # Empty resources
        },
        "world_data": {},
    }

    result = generate_session_header_fallback(game_state)

    assert "Resources: None" in result

import importlib
import sys
import types

import pytest


@pytest.fixture
def world_logic_module():
    modules_to_clear = ["mvp_site.world_logic", "mvp_site.session_header_utils"]
    backup_modules = {name: sys.modules.get(name) for name in modules_to_clear}
    firebase_backup = {
        "firebase_admin": sys.modules.get("firebase_admin"),
        "firebase_admin.credentials": sys.modules.get("firebase_admin.credentials"),
    }

    for name in modules_to_clear:
        sys.modules.pop(name, None)

    firebase_admin_mock = types.SimpleNamespace()

    def _raise_value_error():
        raise ValueError("app not initialized")

    firebase_admin_mock.get_app = _raise_value_error
    firebase_admin_mock.initialize_app = lambda *args, **kwargs: None

    credentials_module = types.SimpleNamespace(Certificate=lambda *args, **kwargs: None)
    firebase_admin_mock.credentials = credentials_module

    sys.modules["firebase_admin"] = firebase_admin_mock
    sys.modules["firebase_admin.credentials"] = credentials_module

    from mvp_site import world_logic

    # Reload the module to pick up any changes
    try:
        importlib.reload(world_logic)
    except (ImportError, KeyError):
        # If reload fails, the module was already removed, re-import it
        world_logic = importlib.import_module("mvp_site.world_logic")

    yield world_logic

    for name, module in firebase_backup.items():
        if module is not None:
            sys.modules[name] = module
        else:
            sys.modules.pop(name, None)

    for name, module in backup_modules.items():
        if module is not None:
            sys.modules[name] = module
        else:
            sys.modules.pop(name, None)


def test_enriches_empty_header_with_progress(world_logic_module):
    result = world_logic_module._enrich_session_header_with_progress(
        "",
        {
            "player_character_data": {
                "xp_current": 120,
                "xp_next_level": 200,
                "gold": 50,
            }
        },
    )

    assert result == "XP: 120/200 | Gold: 50gp"


def test_enriches_status_line(world_logic_module):
    header = "Status: Healthy"
    result = world_logic_module._enrich_session_header_with_progress(
        header,
        {"player_character_data": {"xp_current": 80, "xp_next_level": 100, "gold": 25}},
    )

    assert result == "Status: Healthy | XP: 80/100 | Gold: 25gp"


def test_appends_to_last_line_without_status(world_logic_module):
    header = "Session 1\nLocation: Forest"
    result = world_logic_module._enrich_session_header_with_progress(
        header,
        {"player_character_data": {"xp_current": 10, "xp_next_level": 20}},
    )

    assert result == "Session 1\nLocation: Forest | XP: 10/20"


def test_respects_existing_tokens(world_logic_module):
    header = "Status: XP: 5 | Gold: 10gp"
    result = world_logic_module._enrich_session_header_with_progress(
        header,
        {"player_character_data": {"xp_current": 99, "xp_next_level": 100, "gold": 30}},
    )

    assert result == header


def test_handles_zero_next_level(world_logic_module):
    result = world_logic_module._enrich_session_header_with_progress(
        "",
        {"player_character_data": {"xp_current": 5, "xp_next_level": 0}},
    )

    assert result == "XP: 5/0"


def test_skips_missing_progress_data(world_logic_module):
    header = "Session 2"
    result = world_logic_module._enrich_session_header_with_progress(
        header,
        {"player_character_data": {}},
    )

    assert result == header


# Tests for session_header normalization (worktree_missing-n4x)
def test_normalizes_dict_format_session_header(world_logic_module):
    """Test that dict-as-string format is converted to proper string format."""
    import json

    from mvp_site import constants

    dict_header = json.dumps(
        {
            "Timestamp": "1492 DR, Hammer 16, 15:15:00",
            "Location": "Moonrise Towers",
            "Status": "Lvl 5 Fighter | HP: 68/68",
        }
    )

    structured_fields = {constants.FIELD_SESSION_HEADER: dict_header}
    game_state = {"player_character_data": {}}

    result = world_logic_module._ensure_session_header_resources(
        structured_fields, game_state
    )

    normalized = result[constants.FIELD_SESSION_HEADER]
    assert "[SESSION_HEADER]" in normalized
    assert "Timestamp: 1492 DR, Hammer 16, 15:15:00" in normalized
    assert "Location: Moonrise Towers" in normalized


def test_adds_missing_session_header_prefix(world_logic_module):
    """Test that missing [SESSION_HEADER] prefix is added."""
    from mvp_site import constants

    header_without_prefix = "Timestamp: 1492 DR, Hammer 16, 15:15:00\nLocation: Moonrise Towers\nStatus: Lvl 5 Fighter | HP: 68/68"

    structured_fields = {constants.FIELD_SESSION_HEADER: header_without_prefix}
    game_state = {"player_character_data": {}}

    result = world_logic_module._ensure_session_header_resources(
        structured_fields, game_state
    )

    normalized = result[constants.FIELD_SESSION_HEADER]
    assert normalized.startswith("[SESSION_HEADER]")
    assert "Timestamp: 1492 DR, Hammer 16, 15:15:00" in normalized


def test_preserves_correctly_formatted_session_header(world_logic_module):
    """Test that correctly formatted headers are unchanged."""
    from mvp_site import constants

    correct_header = "[SESSION_HEADER]\nTimestamp: 1492 DR, Hammer 16, 15:15:00\nLocation: Moonrise Towers\nStatus: Lvl 5 Fighter | HP: 68/68"

    structured_fields = {constants.FIELD_SESSION_HEADER: correct_header}
    game_state = {"player_character_data": {}}

    result = world_logic_module._ensure_session_header_resources(
        structured_fields, game_state
    )

    assert result[constants.FIELD_SESSION_HEADER] == correct_header


def test_normalizes_empty_dict_session_header(world_logic_module):
    """Test that empty dict format is handled."""
    import json

    from mvp_site import constants

    empty_dict_header = json.dumps({})

    structured_fields = {constants.FIELD_SESSION_HEADER: empty_dict_header}
    game_state = {"player_character_data": {}}

    result = world_logic_module._ensure_session_header_resources(
        structured_fields, game_state
    )

    normalized = result[constants.FIELD_SESSION_HEADER]
    assert "[SESSION_HEADER]" in normalized or normalized == ""


# Tests for session_header fallback generation (worktree_missing-1cd)
def test_generates_fallback_when_session_header_empty(world_logic_module):
    """Test that empty session_header generates fallback from game_state."""
    from mvp_site import constants

    structured_fields = {constants.FIELD_SESSION_HEADER: ""}
    game_state = {
        "player_character_data": {
            "level": 5,
            "hp_current": 68,
            "hp_maximum": 68,
            "resources": {
                "hit_dice": {"used": 2, "max": 8},
                "spell_slots": {"level_1": {"used": 0, "max": 4}},
            },
        },
        "world_data": {
            "current_time": "1492 DR, Hammer 16, 15:15:00",
            "current_location": "Moonrise Towers",
        },
    }

    result = world_logic_module._ensure_session_header_resources(
        structured_fields, game_state
    )

    fallback = result[constants.FIELD_SESSION_HEADER]
    assert "[SESSION_HEADER]" in fallback
    assert "1492 DR, Hammer 16, 15:15:00" in fallback
    assert "Moonrise Towers" in fallback
    assert "Lvl 5" in fallback or "Level 5" in fallback
    assert "HP: 68/68" in fallback


def test_generates_fallback_when_session_header_none(world_logic_module):
    """Test that None session_header generates fallback from game_state."""
    from mvp_site import constants

    structured_fields = {constants.FIELD_SESSION_HEADER: None}
    game_state = {
        "player_character_data": {"level": 3, "hp_current": 25, "hp_maximum": 30},
        "world_data": {
            "current_time": "1492 DR, Mirtul 15, 14:30",
            "current_location": "Forest",
        },
    }

    result = world_logic_module._ensure_session_header_resources(
        structured_fields, game_state
    )

    fallback = result[constants.FIELD_SESSION_HEADER]
    assert "[SESSION_HEADER]" in fallback
    assert "HP: 25/30" in fallback


def test_does_not_generate_fallback_when_header_exists(world_logic_module):
    """Test that non-empty headers are not replaced with fallback."""
    from mvp_site import constants

    existing_header = "[SESSION_HEADER]\nTimestamp: 1492 DR\nLocation: Test"
    structured_fields = {constants.FIELD_SESSION_HEADER: existing_header}
    game_state = {
        "player_character_data": {"level": 5},
        "world_data": {
            "current_time": "Different time",
            "current_location": "Different location",
        },
    }

    result = world_logic_module._ensure_session_header_resources(
        structured_fields, game_state
    )

    # Should preserve existing header (may be enriched with XP/gold, but not replaced)
    assert result[constants.FIELD_SESSION_HEADER].startswith("[SESSION_HEADER]")
    assert "Test" in result[constants.FIELD_SESSION_HEADER]


# Tests for resources format preservation (worktree_missing-bh3)
# Note: Transformation logic was removed in favor of direct CURRENT/MAX prompting.
# These tests now verify that the format is preserved (no double-subtraction).
def test_preserves_resources_format(world_logic_module):
    """Test that Resources format is preserved (no transformation)."""
    from mvp_site import constants

    # Input is already CURRENT/MAX (e.g. 13/13). Should remain 13/13.
    # Previously this would have been transformed (13-13=0) if interpreted as used/max.
    header = "[SESSION_HEADER]\nTimestamp: 1492 DR\nLocation: Test\nResources: HD: 13/13 | Spells: L1 4/4, L2 3/3 | Bardic: 5/5"

    structured_fields = {constants.FIELD_SESSION_HEADER: header}
    game_state = {"player_character_data": {}}

    result = world_logic_module._ensure_session_header_resources(
        structured_fields, game_state
    )

    transformed = result[constants.FIELD_SESSION_HEADER]
    assert "HD: 13/13" in transformed
    assert "L1 4/4" in transformed
    assert "L2 3/3" in transformed
    assert "Bardic: 5/5" in transformed


def test_preserves_resources_format_partial(world_logic_module):
    """Test that partially used resources are preserved (no transformation)."""
    from mvp_site import constants

    # Input: "HD: 11/13" (11 current, 13 max). Should remain 11/13.
    header = "[SESSION_HEADER]\nResources: HD: 11/13 | Spells: L1 3/4"

    structured_fields = {constants.FIELD_SESSION_HEADER: header}
    game_state = {"player_character_data": {}}

    result = world_logic_module._ensure_session_header_resources(
        structured_fields, game_state
    )

    transformed = result[constants.FIELD_SESSION_HEADER]
    assert "HD: 11/13" in transformed
    assert "L1 3/4" in transformed


def test_preserves_exhaustion_format(world_logic_module):
    """Test that Exhaustion level (0-6) is preserved as-is."""
    from mvp_site import constants

    header = "[SESSION_HEADER]\nResources: HD: 0/13 | Exhaustion: 2"

    structured_fields = {constants.FIELD_SESSION_HEADER: header}
    game_state = {"player_character_data": {}}

    result = world_logic_module._ensure_session_header_resources(
        structured_fields, game_state
    )

    transformed = result[constants.FIELD_SESSION_HEADER]
    # Exhaustion should remain as-is (not a used/max format)
    assert "Exhaustion: 2" in transformed

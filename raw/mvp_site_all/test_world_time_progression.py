import copy
import unittest

from mvp_site import constants, world_logic, world_time
from mvp_site.game_state import GameState


def test_missing_world_time_is_not_inferred():
    state_changes = {"world_data": {}}

    updated = world_time.ensure_progressive_world_time(
        copy.deepcopy(state_changes),
        is_god_mode=False,
    )

    assert "world_time" not in updated["world_data"]


def test_parses_string_world_time_from_llm():
    state_changes = {"world_data": {"world_time": "2025-03-15T10:45:30.123456Z"}}

    updated = world_time.ensure_progressive_world_time(
        copy.deepcopy(state_changes),
        is_god_mode=False,
    )

    assert updated["world_data"]["world_time"] == {
        "year": 2025,
        "month": 3,
        "day": 15,
        "hour": 10,
        "minute": 45,
        "second": 30,
        "microsecond": 123456,
    }


def test_parse_timestamp_without_timezone_defaults_to_utc():
    parsed = world_time.parse_timestamp_to_world_time("2025-03-15T10:45:30.000001")

    assert parsed == {
        "year": 2025,
        "month": 3,
        "day": 15,
        "hour": 10,
        "minute": 45,
        "second": 30,
        "microsecond": 1,
    }


def test_keeps_partial_world_time_unchanged():
    partial_time = {"hour": 8, "minute": 15, "time_of_day": "Morning"}
    state_changes = {"world_data": {"world_time": partial_time}}

    updated = world_time.ensure_progressive_world_time(
        copy.deepcopy(state_changes),
        is_god_mode=False,
    )

    assert updated["world_data"]["world_time"] == partial_time


class TestWorldTimeCalculations(unittest.TestCase):
    """Test the calculate_hours_elapsed helper function."""

    def test_calculate_hours_elapsed_24_hours(self):
        """Should correctly calculate 24 hours elapsed."""
        old_time = {"year": 1492, "month": 6, "day": 15, "hour": 10, "minute": 0}
        new_time = {"year": 1492, "month": 6, "day": 16, "hour": 10, "minute": 0}

        hours = world_time.calculate_hours_elapsed(old_time, new_time)
        assert hours == 24.0

    def test_calculate_hours_elapsed_with_minutes(self):
        """Should correctly calculate hours with fractional minutes."""
        old_time = {"year": 1492, "month": 6, "day": 15, "hour": 10, "minute": 30}
        new_time = {"year": 1492, "month": 6, "day": 16, "hour": 11, "minute": 0}

        hours = world_time.calculate_hours_elapsed(old_time, new_time)
        assert hours == 24.5

    def test_calculate_hours_elapsed_returns_none_for_incomplete_time(self):
        """Should return None when time data is incomplete."""
        old_time = {"hour": 10, "minute": 0}  # Missing year, month, day
        new_time = {"year": 1492, "month": 6, "day": 16, "hour": 10, "minute": 0}

        hours = world_time.calculate_hours_elapsed(old_time, new_time)
        assert hours is None

    def test_calculate_hours_elapsed_returns_none_for_none_input(self):
        """Should return None when input is None."""
        hours = world_time.calculate_hours_elapsed(None, None)
        assert hours is None

    def test_calculate_hours_elapsed_across_month_boundary(self):
        """Should correctly calculate hours across month boundaries."""
        old_time = {"year": 1492, "month": 6, "day": 30, "hour": 23, "minute": 0}
        new_time = {"year": 1492, "month": 7, "day": 1, "hour": 23, "minute": 0}

        hours = world_time.calculate_hours_elapsed(old_time, new_time)
        # With 30-day month arithmetic, day 30 -> day 1 is 1 day difference
        assert hours == 24.0

    def test_calculate_hours_elapsed_negative(self):
        """Should return negative hours when new time is before old time."""
        old_time = {"year": 1492, "month": 2, "day": 10, "hour": 12, "minute": 0}
        new_time = {"year": 1492, "month": 2, "day": 10, "hour": 10, "minute": 0}

        hours = world_time.calculate_hours_elapsed(old_time, new_time)
        assert hours == -2.0

    def test_calculate_hours_elapsed_fantasy_date(self):
        """Should correctly calculate hours for dates invalid in Gregorian (e.g., Feb 30)."""
        # Feb 30 is valid in 30-day month/12-month fantasy calendar
        # But invalid in Gregorian (raises ValueError in datetime)
        old_time = {"year": 1492, "month": 2, "day": 30, "hour": 12, "minute": 0}
        new_time = {"year": 1492, "month": 3, "day": 1, "hour": 12, "minute": 0}

        hours = world_time.calculate_hours_elapsed(old_time, new_time)
        # Day 30 -> Day 1 of next month is 1 day difference (24 hours)
        assert hours == 24.0

    def test_calculate_hours_elapsed_invalid_month_returns_none(self):
        """Should return None for invalid month values."""
        old_time = {"year": 1492, "month": 13, "day": 1, "hour": 12, "minute": 0}
        new_time = {"year": 1492, "month": 13, "day": 2, "hour": 12, "minute": 0}

        hours = world_time.calculate_hours_elapsed(old_time, new_time)
        assert hours is None


def test_maybe_update_living_world_tracking_updates_state():
    """Should update tracking after response when living world triggers."""
    current_time = {"year": 1492, "month": 1, "day": 1, "hour": 0, "minute": 0}
    current_game_state = GameState(
        last_living_world_turn=0,
        last_living_world_time=None,
        world_data={"world_time": current_time},
        player_turn=2,
    )
    updated_state = {"player_turn": 2}

    result = world_logic._maybe_update_living_world_tracking(
        updated_state,
        current_game_state=current_game_state,
        turn_number=3,
        mode=constants.MODE_CHARACTER,
        is_god_mode=False,
        is_think_mode=False,
    )

    assert result["last_living_world_turn"] == 3
    assert result["last_living_world_time"] == current_time


def test_maybe_update_living_world_tracking_does_not_add_scene_cadence_tracking():
    """Living-world tracking should not manage separate scene cadence state."""
    current_time = {"year": 1492, "month": 1, "day": 1, "hour": 0, "minute": 0}
    current_game_state = GameState(
        last_living_world_turn=0,
        last_living_world_time=None,
        world_data={"world_time": current_time},
        player_turn=2,
    )
    updated_state = {
        "player_turn": 2,
        "scene_event": {
            "type": "messenger_arrival",
            "description": "A rider arrives with urgent news.",
            "actor": "Scout",
        },
    }

    result = world_logic._maybe_update_living_world_tracking(
        updated_state,
        current_game_state=current_game_state,
        turn_number=3,
        mode=constants.MODE_CHARACTER,
        is_god_mode=False,
        is_think_mode=False,
    )

    custom_state = result.get("custom_campaign_state", {})
    assert custom_state.get("last_scene_event_turn") is None
    assert custom_state.get("last_scene_event_type") is None
    assert custom_state.get("next_scene_event_turn") is None


def test_maybe_update_living_world_tracking_no_overdue_scene_warning():
    """Living-world tracking should not emit overdue scene-cadence warnings."""
    current_time = {"year": 1492, "month": 1, "day": 1, "hour": 0, "minute": 0}
    current_game_state = GameState(
        last_living_world_turn=0,
        last_living_world_time=None,
        world_data={"world_time": current_time},
        player_turn=2,
    )
    updated_state = {
        "player_turn": 2,
        "custom_campaign_state": {},
    }

    result = world_logic._maybe_update_living_world_tracking(
        updated_state,
        current_game_state=current_game_state,
        turn_number=3,
        mode=constants.MODE_CHARACTER,
        is_god_mode=False,
        is_think_mode=False,
    )

    pending = result.get("pending_system_corrections")
    assert pending is None


def test_maybe_update_living_world_tracking_updates_when_trigger_has_no_payload():
    """Trigger should still update tracking even if no living-world payload is emitted."""
    current_time = {"year": 1492, "month": 1, "day": 1, "hour": 0, "minute": 0}
    current_game_state = GameState(
        last_living_world_turn=0,
        last_living_world_time=None,
        world_data={"world_time": current_time},
        player_turn=2,
    )
    updated_state = {"player_turn": 3, "world_data": {"world_time": current_time}}

    result = world_logic._maybe_update_living_world_tracking(
        updated_state,
        current_game_state=current_game_state,
        turn_number=3,
        mode=constants.MODE_CHARACTER,
        is_god_mode=False,
        is_think_mode=False,
        state_changes_this_turn={},
    )

    assert result["last_living_world_turn"] == 3
    assert result["last_living_world_time"] == current_time


def test_maybe_update_living_world_tracking_updates_with_world_events_payload():
    """Trigger should be consumed when turn includes living-world payload."""
    current_time = {"year": 1492, "month": 1, "day": 1, "hour": 0, "minute": 0}
    current_game_state = GameState(
        last_living_world_turn=0,
        last_living_world_time=None,
        world_data={"world_time": current_time},
        player_turn=2,
    )
    updated_state = {"player_turn": 3, "world_data": {"world_time": current_time}}
    state_changes = {
        "world_events": {
            "background_events": [
                {"actor": "Guild", "action": "Moves assets", "event_type": "immediate"}
            ]
        }
    }

    result = world_logic._maybe_update_living_world_tracking(
        updated_state,
        current_game_state=current_game_state,
        turn_number=3,
        mode=constants.MODE_CHARACTER,
        is_god_mode=False,
        is_think_mode=False,
        state_changes_this_turn=state_changes,
    )

    assert result["last_living_world_turn"] == 3
    assert result["last_living_world_time"] == current_time


def test_maybe_update_living_world_tracking_skips_when_not_callable():
    """Should skip update if check_living_world_trigger is not callable."""

    class BadGameState:
        check_living_world_trigger = "not callable"

    updated_state = {"player_turn": 2}

    result = world_logic._maybe_update_living_world_tracking(
        updated_state,
        current_game_state=BadGameState(),
        turn_number=3,
        mode=constants.MODE_CHARACTER,
        is_god_mode=False,
        is_think_mode=False,
    )

    assert result == updated_state


def test_maybe_update_living_world_tracking_skips_invalid_return():
    """Should skip update if check_living_world_trigger returns invalid data."""

    class BadGameState:
        def check_living_world_trigger(self, current_turn, *, current_time=None):  # noqa: ARG002
            return "not a tuple"

    updated_state = {"player_turn": 2}

    result = world_logic._maybe_update_living_world_tracking(
        updated_state,
        current_game_state=BadGameState(),
        turn_number=3,
        mode=constants.MODE_CHARACTER,
        is_god_mode=False,
        is_think_mode=False,
    )

    assert result == updated_state


def test_maybe_update_living_world_tracking_updates_combat():
    """Combat turns should persist living-world tracking when triggered."""
    current_time = {"year": 1492, "month": 1, "day": 1, "hour": 0, "minute": 0}
    current_game_state = GameState(
        last_living_world_turn=0,
        last_living_world_time=None,
        world_data={"world_time": current_time},
        player_turn=2,
    )
    updated_state = {"player_turn": 2}

    result = world_logic._maybe_update_living_world_tracking(
        updated_state,
        current_game_state=current_game_state,
        turn_number=3,
        mode=constants.MODE_COMBAT,
        is_god_mode=False,
        is_think_mode=False,
    )

    assert result["last_living_world_turn"] == 3
    assert result["last_living_world_time"] == current_time


def test_maybe_update_living_world_tracking_recovers_corrupt_last_turn():
    """Corrupt future last_living_world_turn should recover and trigger."""
    current_time = {"year": 1492, "month": 1, "day": 2, "hour": 0, "minute": 0}
    current_game_state = GameState(
        last_living_world_turn=999,
        last_living_world_time=None,
        world_data={"world_time": current_time},
        player_turn=11,
    )
    updated_state = {"player_turn": 11, "world_data": {"world_time": current_time}}

    result = world_logic._maybe_update_living_world_tracking(
        updated_state,
        current_game_state=current_game_state,
        turn_number=12,
        mode=constants.MODE_CHARACTER,
        is_god_mode=False,
        is_think_mode=False,
    )

    assert result["last_living_world_turn"] == 12
    assert result["last_living_world_time"] == current_time


def test_maybe_update_living_world_tracking_skips_character_creation():
    """Character creation mode should not advance living-world tracking."""
    current_time = {"year": 1492, "month": 1, "day": 1, "hour": 0, "minute": 0}
    current_game_state = GameState(
        last_living_world_turn=0,
        last_living_world_time=None,
        world_data={"world_time": current_time},
        player_turn=2,
    )
    updated_state = {"player_turn": 3, "world_data": {"world_time": current_time}}

    result = world_logic._maybe_update_living_world_tracking(
        updated_state,
        current_game_state=current_game_state,
        turn_number=3,
        mode=constants.MODE_CHARACTER_CREATION,
        is_god_mode=False,
        is_think_mode=False,
    )

    assert "last_living_world_turn" not in result
    assert "last_living_world_time" not in result


def test_maybe_update_living_world_tracking_skips_info_mode():
    """Info mode should not advance living-world tracking."""
    current_time = {"year": 1492, "month": 1, "day": 1, "hour": 0, "minute": 0}
    current_game_state = GameState(
        last_living_world_turn=0,
        last_living_world_time=None,
        world_data={"world_time": current_time},
        player_turn=2,
    )
    updated_state = {"player_turn": 3, "world_data": {"world_time": current_time}}

    result = world_logic._maybe_update_living_world_tracking(
        updated_state,
        current_game_state=current_game_state,
        turn_number=3,
        mode=constants.MODE_INFO,
        is_god_mode=False,
        is_think_mode=False,
    )

    assert "last_living_world_turn" not in result
    assert "last_living_world_time" not in result


def test_maybe_update_living_world_tracking_skips_rewards_mode():
    """Rewards mode should not advance living-world tracking."""
    current_time = {"year": 1492, "month": 1, "day": 1, "hour": 0, "minute": 0}
    current_game_state = GameState(
        last_living_world_turn=0,
        last_living_world_time=None,
        world_data={"world_time": current_time},
        player_turn=2,
    )
    updated_state = {"player_turn": 3, "world_data": {"world_time": current_time}}

    result = world_logic._maybe_update_living_world_tracking(
        updated_state,
        current_game_state=current_game_state,
        turn_number=3,
        mode=constants.MODE_REWARDS,
        is_god_mode=False,
        is_think_mode=False,
    )

    assert "last_living_world_turn" not in result
    assert "last_living_world_time" not in result


def test_inject_persisted_living_world_fallback_adds_payload_to_latest_gemini_entry():
    story_entries = [
        {"actor": "user", "text": "Do something"},
        {
            "actor": "gemini",
            "text": "Narrative without LW",
            "user_scene_number": 1,
            "state_updates": {},
        },
    ]
    game_state = {
        "world_events": {
            "background_events": [
                {
                    "scene_generated": 1,
                    "actor": "Guild",
                    "action": "Secures bridge",
                    "event_type": "immediate",
                    "status": "pending",
                }
            ]
        }
    }

    result = world_logic.inject_persisted_living_world_fallback(
        story_entries, game_state, debug_mode=True
    )

    latest = result[-1]
    assert isinstance(latest.get("state_updates"), dict)
    assert latest["state_updates"].get("world_events") == game_state["world_events"]
    assert latest.get("world_events") == game_state["world_events"]


def test_inject_persisted_living_world_fallback_skips_when_entry_already_has_visible_data():
    story_entries = [
        {"actor": "user", "text": "Do something"},
        {
            "actor": "gemini",
            "text": "Narrative with LW",
            "user_scene_number": 1,
            "state_updates": {
                "scene_event": {
                    "type": "alert",
                    "description": "A warning appears",
                    "actor": "Scout",
                }
            },
        },
    ]
    game_state = {
        "world_events": {
            "background_events": [
                {"actor": "Guild", "action": "Secures bridge", "status": "pending"}
            ]
        }
    }

    result = world_logic.inject_persisted_living_world_fallback(
        story_entries, game_state, debug_mode=True
    )

    assert result == story_entries


def test_inject_persisted_living_world_fallback_skips_when_debug_mode_off():
    story_entries = [
        {
            "actor": "gemini",
            "text": "Narrative without LW",
            "user_scene_number": 1,
            "state_updates": {},
        }
    ]
    game_state = {
        "world_events": {
            "background_events": [
                {"actor": "Guild", "action": "Secures bridge", "status": "pending"}
            ]
        }
    }

    result = world_logic.inject_persisted_living_world_fallback(
        story_entries, game_state, debug_mode=False
    )

    assert result == story_entries


def test_inject_persisted_living_world_fallback_skips_when_latest_entry_has_no_scene_number():
    story_entries = [{"actor": "gemini", "text": "Narrative without LW", "state_updates": {}}]
    game_state = {
        "world_events": {
            "background_events": [
                {"actor": "Guild", "action": "Secures bridge", "scene_generated": 1}
            ]
        }
    }

    result = world_logic.inject_persisted_living_world_fallback(
        story_entries, game_state, debug_mode=True
    )

    assert result == story_entries


def test_normalize_world_events_for_story_payload_converts_append_payloads():
    world_events = {
        "background_events": {"append": {"actor": "Guild", "action": "Moves assets"}},
        "rumors": {"append": None},
    }

    normalized = world_logic.normalize_world_events_for_story_payload(world_events)

    assert normalized["background_events"] == [
        {"actor": "Guild", "action": "Moves assets"}
    ]
    assert normalized["rumors"] == []


def test_normalize_world_events_for_story_payload_converts_top_level_append_payloads():
    world_events = {"append": {"actor": "Guild", "action": "Moves assets"}}

    normalized = world_logic.normalize_world_events_for_story_payload(world_events)

    assert normalized["background_events"] == [
        {"actor": "Guild", "action": "Moves assets"}
    ]
    assert "append" not in normalized


def test_filter_story_entry_world_events_to_scene_filters_mismatched_scene_events():
    world_events = {
        "background_events": [
            {"actor": "A", "action": "old", "scene_generated": 2},
            {"actor": "B", "action": "current", "scene_generated": 4},
        ]
    }

    filtered = world_logic._filter_story_entry_world_events_to_scene(world_events, 4)

    assert filtered["background_events"] == [
        {"actor": "B", "action": "current", "scene_generated": 4}
    ]


def test_filter_story_entry_world_events_to_scene_uses_turn_generated_fallback():
    world_events = {
        "background_events": [
            {"actor": "A", "action": "old", "turn_generated": 3},
            {"actor": "B", "action": "current", "turn_generated": 4},
        ]
    }

    filtered = world_logic._filter_story_entry_world_events_to_scene(world_events, 4)

    assert filtered["background_events"] == [
        {
            "actor": "B",
            "action": "current",
            "turn_generated": 4,
            "scene_generated": 4,
        }
    ]


def test_filter_story_entry_world_events_to_scene_filters_faction_updates_dict_of_dicts():
    """Test that faction_updates (dict-of-dicts) is filtered by scene match."""
    world_events = {
        "faction_updates": {
            "Guild of Merchants": {"objective": "Trade expansion", "scene_generated": 2},
            "Thieves Guild": {"objective": "Steal the crown", "scene_generated": 4},
        }
    }

    filtered = world_logic._filter_story_entry_world_events_to_scene(world_events, 4)

    assert "Thieves Guild" in filtered["faction_updates"]
    assert "Guild of Merchants" not in filtered["faction_updates"]
    assert filtered["faction_updates"]["Thieves Guild"]["scene_generated"] == 4


def test_filter_story_entry_world_events_to_scene_filters_time_events_dict_of_dicts():
    """Test that time_events (dict-of-dicts) is filtered by scene match."""
    world_events = {
        "time_events": {
            "Festival": {"description": "Annual harvest festival", "scene_generated": 2},
            "Eclipse": {"description": "Total solar eclipse", "scene_generated": 4},
        }
    }

    filtered = world_logic._filter_story_entry_world_events_to_scene(world_events, 4)

    assert "Eclipse" in filtered["time_events"]
    assert "Festival" not in filtered["time_events"]
    assert filtered["time_events"]["Eclipse"]["scene_generated"] == 4


def test_filter_story_entry_world_events_to_scene_removes_mismatched_complications():
    """Test that complications (single dict) is removed when scene doesn't match."""
    world_events = {
        "complications": {"description": "Bandit attack", "scene_generated": 2}
    }

    filtered = world_logic._filter_story_entry_world_events_to_scene(world_events, 4)

    assert "complications" not in filtered


def test_filter_story_entry_world_events_to_scene_keeps_matching_complications():
    """Test that complications (single dict) is kept when scene matches."""
    world_events = {
        "complications": {"description": "Storm arrives", "scene_generated": 4}
    }

    filtered = world_logic._filter_story_entry_world_events_to_scene(world_events, 4)

    assert "complications" in filtered
    assert filtered["complications"]["scene_generated"] == 4


def test_filter_story_entry_world_events_to_scene_removes_mismatched_scene_event():
    """Test that scene_event (single dict) is removed when scene doesn't match."""
    world_events = {
        "scene_event": {"type": "encounter", "scene_generated": 2}
    }

    filtered = world_logic._filter_story_entry_world_events_to_scene(world_events, 4)

    assert "scene_event" not in filtered


def test_filter_story_entry_world_events_to_scene_keeps_matching_scene_event():
    """Test that scene_event (single dict) is kept when scene matches."""
    world_events = {
        "scene_event": {"type": "encounter", "scene_generated": 4}
    }

    filtered = world_logic._filter_story_entry_world_events_to_scene(world_events, 4)

    assert "scene_event" in filtered
    assert filtered["scene_event"]["scene_generated"] == 4


def test_annotate_world_events_with_turn_scene_ignores_non_list_append():
    game_state = {
        "world_events": {
            "background_events": {"append": {"actor": "Guild", "action": "Moves assets"}}
        }
    }

    result = world_logic.annotate_world_events_with_turn_scene(game_state, player_turn=3)

    assert result["world_events"]["background_events"] == {
        "append": {
            "actor": "Guild",
            "action": "Moves assets",
            "turn_generated": 3,
            "scene_generated": 3,
        }
    }


def test_has_visible_living_world_data_accepts_single_rumor_dict():
    assert world_logic._has_visible_living_world_data(
        world_events={},
        faction_updates={},
        time_events={},
        rumors={"speaker": "Scout", "text": "Road is blocked"},
        scene_event=None,
        complications=None,
    )


def test_has_visible_living_world_data_accepts_append_rumors_dict():
    assert world_logic._has_visible_living_world_data(
        world_events={},
        faction_updates={},
        time_events={},
        rumors={"append": {"speaker": "Scout", "text": "Road is blocked"}},
        scene_event=None,
        complications=None,
    )


def test_inject_persisted_living_world_fallback_returns_when_persisted_not_visible():
    story_entries = [
        {"actor": "gemini", "text": "Narrative", "user_scene_number": 1, "state_updates": {}}
    ]
    game_state = {"world_events": {"background_events": []}}

    result = world_logic.inject_persisted_living_world_fallback(
        story_entries, game_state, debug_mode=True
    )

    assert result == story_entries


def test_inject_persisted_living_world_fallback_returns_when_persisted_world_events_not_dict():
    story_entries = [
        {"actor": "gemini", "text": "Narrative", "user_scene_number": 1, "state_updates": {}}
    ]
    game_state = {"world_events": "invalid"}

    result = world_logic.inject_persisted_living_world_fallback(
        story_entries, game_state, debug_mode=True
    )

    assert result == story_entries


def test_inject_persisted_living_world_fallback_returns_when_no_gemini_entry():
    story_entries = [{"actor": "user", "text": "Hello"}]
    game_state = {
        "world_events": {
            "background_events": [{"actor": "Guild", "action": "Moves assets"}]
        }
    }

    result = world_logic.inject_persisted_living_world_fallback(
        story_entries, game_state, debug_mode=True
    )

    assert result == story_entries


def test_inject_persisted_living_world_fallback_handles_non_dict_state_updates():
    story_entries = [
        {
            "actor": "gemini",
            "text": "Narrative",
            "user_scene_number": 1,
            "state_updates": "invalid",
        }
    ]
    game_state = {
        "world_events": {
            "background_events": [
                {"actor": "Guild", "action": "Moves assets", "scene_generated": 1}
            ]
        }
    }

    result = world_logic.inject_persisted_living_world_fallback(
        story_entries, game_state, debug_mode=True
    )

    assert isinstance(result[-1]["state_updates"], dict)
    assert isinstance(result[-1]["state_updates"]["world_events"]["background_events"], list)


def test_inject_persisted_living_world_fallback_normalizes_persisted_append_world_events():
    story_entries = [
        {"actor": "gemini", "text": "Narrative", "user_scene_number": 1, "state_updates": {}}
    ]
    game_state = {
        "world_events": {
            "background_events": {
                "append": {
                    "actor": "Guild",
                    "action": "Secures bridge",
                    "scene_generated": 1,
                }
            }
        }
    }

    result = world_logic.inject_persisted_living_world_fallback(
        story_entries, game_state, debug_mode=True
    )

    injected = result[-1]["state_updates"]["world_events"]["background_events"]
    assert injected == [
        {"actor": "Guild", "action": "Secures bridge", "scene_generated": 1}
    ]


def test_inject_persisted_living_world_fallback_respects_state_updates_append_rumors():
    story_entries = [
        {
            "actor": "gemini",
            "text": "Narrative with rumors",
            "user_scene_number": 1,
            "state_updates": {"rumors": {"append": {"speaker": "Scout", "text": "Move now"}}},
        }
    ]
    game_state = {
        "world_events": {
            "background_events": [{"actor": "Guild", "action": "Secures bridge"}]
        }
    }

    result = world_logic.inject_persisted_living_world_fallback(
        story_entries, game_state, debug_mode=True
    )

    assert result == story_entries


def test_inject_persisted_living_world_fallback_normalizes_existing_entry_world_events():
    story_entries = [
        {
            "actor": "gemini",
            "text": "Narrative with world event",
            "user_scene_number": 1,
            "state_updates": {
                "world_events": {
                    "background_events": {
                        "append": {
                            "actor": "Guild",
                            "action": "Patrols",
                            "scene_generated": 1,
                        }
                    }
                }
            },
        }
    ]
    game_state = {
        "world_events": {
            "background_events": [{"actor": "Guild", "action": "Secures bridge"}]
        }
    }

    result = world_logic.inject_persisted_living_world_fallback(
        story_entries, game_state, debug_mode=True
    )

    assert result[-1]["state_updates"]["world_events"]["background_events"] == [
        {"actor": "Guild", "action": "Patrols", "scene_generated": 1}
    ]


def test_inject_persisted_living_world_fallback_normalizes_persisted_append_rumors():
    story_entries = [
        {"actor": "gemini", "text": "Narrative", "user_scene_number": 1, "state_updates": {}}
    ]
    game_state = {
        "world_events": {
            "background_events": [{"actor": "Guild", "action": "Secures bridge"}],
            "rumors": {
                "append": {
                    "speaker": "Scout",
                    "text": "Ambush near bridge",
                    "scene_generated": 1,
                }
            },
        }
    }

    result = world_logic.inject_persisted_living_world_fallback(
        story_entries, game_state, debug_mode=True
    )

    assert result[-1]["state_updates"]["rumors"] == [
        {"speaker": "Scout", "text": "Ambush near bridge", "scene_generated": 1}
    ]


def test_inject_persisted_living_world_fallback_normalizes_top_level_append_rumors():
    story_entries = [
        {"actor": "gemini", "text": "Narrative", "user_scene_number": 1, "state_updates": {}}
    ]
    game_state = {
        "world_events": {
            "background_events": [{"actor": "Guild", "action": "Secures bridge"}]
        },
        "rumors": {
            "append": {
                "speaker": "Scout",
                "text": "Ambush near bridge",
                "scene_generated": 1,
            }
        },
    }

    result = world_logic.inject_persisted_living_world_fallback(
        story_entries, game_state, debug_mode=True
    )

    assert result[-1]["state_updates"]["rumors"] == [
        {"speaker": "Scout", "text": "Ambush near bridge", "scene_generated": 1}
    ]


def test_inject_persisted_living_world_fallback_wraps_scalar_persisted_rumor():
    story_entries = [
        {"actor": "gemini", "text": "Narrative", "user_scene_number": 1, "state_updates": {}}
    ]
    game_state = {
        "world_events": {
            "background_events": [{"actor": "Guild", "action": "Secures bridge", "scene_generated": 1}],
            "rumors": "Ambush near bridge",
        }
    }

    result = world_logic.inject_persisted_living_world_fallback(
        story_entries, game_state, debug_mode=True
    )

    updates = result[0]["state_updates"]
    assert updates["world_events"]["background_events"] == [
        {"actor": "Guild", "action": "Secures bridge", "scene_generated": 1}
    ]


def test_inject_persisted_living_world_fallback_wraps_scalar_entry_rumor():
    story_entries = [
        {
            "actor": "gemini",
            "text": "Narrative with rumors",
            "user_scene_number": 1,
            "state_updates": {"rumors": "Move now"},
        }
    ]
    game_state = {
        "world_events": {
            "background_events": [{"actor": "Guild", "action": "Secures bridge", "scene_generated": 1}]
        }
    }

    result = world_logic.inject_persisted_living_world_fallback(
        story_entries, game_state, debug_mode=True
    )

    updates = result[0]["state_updates"]
    assert updates["rumors"] == "Move now"
    assert updates["world_events"]["background_events"] == [
        {"actor": "Guild", "action": "Secures bridge", "scene_generated": 1}
    ]


def test_inject_persisted_living_world_fallback_treats_single_entry_rumor_dict_as_visible():
    story_entries = [
        {
            "actor": "gemini",
            "text": "Narrative with rumors",
            "user_scene_number": 1,
            "state_updates": {"rumors": {"speaker": "Scout", "text": "Move now"}},
        }
    ]
    game_state = {
        "world_events": {
            "background_events": [{"actor": "Guild", "action": "Secures bridge"}]
        }
    }

    result = world_logic.inject_persisted_living_world_fallback(
        story_entries, game_state, debug_mode=True
    )

    assert result == story_entries


def test_inject_persisted_living_world_fallback_normalizes_non_list_persisted_rumor():
    story_entries = [
        {"actor": "gemini", "text": "Narrative", "user_scene_number": 1, "state_updates": {}}
    ]
    game_state = {
        "world_events": {
            "background_events": [{"actor": "Guild", "action": "Secures bridge"}],
            "rumors": {
                "speaker": "Scout",
                "text": "Ambush near bridge",
                "scene_generated": 1,
            },
        }
    }

    result = world_logic.inject_persisted_living_world_fallback(
        story_entries, game_state, debug_mode=True
    )

    assert result[-1]["state_updates"]["rumors"] == [
        {"speaker": "Scout", "text": "Ambush near bridge", "scene_generated": 1}
    ]


def test_inject_persisted_living_world_fallback_injects_all_optional_persisted_fields():
    story_entries = [
        {"actor": "gemini", "text": "Narrative", "user_scene_number": 1, "state_updates": {}}
    ]
    game_state = {
        "world_events": {
            "background_events": [
                {"actor": "Guild", "action": "Secures bridge", "scene_generated": 1}
            ]
        },
        "faction_updates": {"factions": {"name": "Guild", "scene_generated": 1}},
        "time_events": {"dawn": {"status": "arrived", "scene_generated": 1}},
        "rumors": [{"speaker": "Scout", "text": "Move now", "scene_generated": 1}],
        "scene_event": {"type": "alert", "scene_generated": 1},
        "complications": {"triggered": True, "scene_generated": 1},
    }

    result = world_logic.inject_persisted_living_world_fallback(
        story_entries, game_state, debug_mode=True
    )

    updates = result[-1]["state_updates"]
    assert updates["faction_updates"] == {"factions": {"name": "Guild", "scene_generated": 1}}
    assert updates["time_events"] == {"dawn": {"status": "arrived", "scene_generated": 1}}
    assert updates["rumors"] == [
        {"speaker": "Scout", "text": "Move now", "scene_generated": 1}
    ]
    assert updates["scene_event"] == {"type": "alert", "scene_generated": 1}
    assert updates["complications"] == {"triggered": True, "scene_generated": 1}


def test_inject_persisted_living_world_fallback_injects_per_scene_not_latest_only():
    story_entries = [
        {"actor": "gemini", "text": "Older scene", "user_scene_number": 1, "state_updates": {}},
        {"actor": "gemini", "text": "Latest scene", "user_scene_number": 2, "state_updates": {}},
    ]
    game_state = {
        "world_events": {
            "background_events": [
                {"actor": "Old", "action": "Old event", "scene_generated": 1},
                {"actor": "New", "action": "New event", "scene_generated": 2},
            ]
        }
    }

    result = world_logic.inject_persisted_living_world_fallback(
        story_entries, game_state, debug_mode=True
    )

    older_events = result[0]["state_updates"]["world_events"]["background_events"]
    latest_events = result[1]["state_updates"]["world_events"]["background_events"]
    assert older_events == [{"actor": "Old", "action": "Old event", "scene_generated": 1}]
    assert latest_events == [{"actor": "New", "action": "New event", "scene_generated": 2}]


def test_inject_persisted_living_world_fallback_shows_scene_50_updates_on_scene_50():
    story_entries = [
        {"actor": "gemini", "text": "Scene 50", "user_scene_number": 50, "state_updates": {}},
        {"actor": "gemini", "text": "Scene 100", "user_scene_number": 100, "state_updates": {}},
    ]
    game_state = {
        "world_events": {
            "background_events": [
                {"actor": "Harpers", "action": "Moved scouts", "scene_generated": 50},
                {"actor": "Cult", "action": "Raised alarm", "scene_generated": 100},
            ]
        }
    }

    result = world_logic.inject_persisted_living_world_fallback(
        story_entries, game_state, debug_mode=True
    )

    scene_50_events = result[0]["state_updates"]["world_events"]["background_events"]
    scene_100_events = result[1]["state_updates"]["world_events"]["background_events"]
    assert scene_50_events == [
        {"actor": "Harpers", "action": "Moved scouts", "scene_generated": 50}
    ]
    assert scene_100_events == [
        {"actor": "Cult", "action": "Raised alarm", "scene_generated": 100}
    ]


def test_prefix_scene_number_in_narrative_adds_prefix():
    result = world_logic._prefix_scene_number_in_narrative(
        "Night falls over the bridge.", 70
    )
    assert result == "Scene #70: Night falls over the bridge."


def test_prefix_scene_number_in_narrative_noop_without_scene_number():
    text = "Night falls over the bridge."
    result = world_logic._prefix_scene_number_in_narrative(text, None)
    assert result == text


def test_prefix_scene_number_in_narrative_avoids_double_prefix():
    text = "Scene #70: Night falls over the bridge."
    result = world_logic._prefix_scene_number_in_narrative(text, 70)
    assert result == text


def test_prefix_scene_number_in_narrative_strips_leading_whitespace():
    text = "\n  Night falls over the bridge."
    result = world_logic._prefix_scene_number_in_narrative(text, 70)
    assert result == "Scene #70: Night falls over the bridge."


if __name__ == "__main__":
    import sys

    import pytest

    sys.exit(pytest.main([__file__]))

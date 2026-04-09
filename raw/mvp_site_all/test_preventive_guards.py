import pytest

from mvp_site import constants, preventive_guards
from mvp_site.constants import MIN_RANK_FP
from mvp_site.faction.tools import execute_faction_tool
from mvp_site.game_state import GameState
from mvp_site.llm_response import LLMResponse
from mvp_site.narrative_response_schema import NarrativeResponse


@pytest.fixture
def base_game_state():
    state = GameState(user_id="user-123")
    # Seed time data so we can verify preservation
    state.world_data["world_time"] = {
        "hour": 10,
        "minute": 15,
        "time_of_day": "morning",
    }
    state.world_data["current_location_name"] = "Harbor"
    state.custom_campaign_state = {}
    return state


def _make_response(**kwargs):
    debug_info = kwargs.pop("debug_info", None)
    structured = NarrativeResponse(
        narrative=kwargs.pop("narrative", ""),
        entities_mentioned=[],
        location_confirmed=kwargs.pop("location_confirmed", "Unknown"),
        state_updates=kwargs.pop("state_updates", {}),
        dice_rolls=kwargs.pop("dice_rolls", []),
        resources=kwargs.pop("resources", ""),
    )
    # Inject debug_info into structured response if provided
    if debug_info is not None:
        structured.debug_info = debug_info
    return LLMResponse(
        narrative_text=structured.narrative,
        structured_response=structured,
    )


def test_enforces_god_mode_response_when_missing(base_game_state):
    response = _make_response(narrative="Repair the timeline.")

    state_changes, extras = preventive_guards.enforce_preventive_guards(
        base_game_state, response, constants.MODE_GOD
    )

    assert extras.get("god_mode_response") == "Repair the timeline."
    assert state_changes["world_data"]["current_location_name"] == "Harbor"


def test_infers_time_and_memory_from_dice_rolls(base_game_state):
    response = _make_response(
        narrative="You sprint across the deck as arrows fly.",
        dice_rolls=["1d20"],
        state_updates={},
    )

    state_changes, extras = preventive_guards.enforce_preventive_guards(
        base_game_state, response, constants.MODE_CHARACTER
    )

    # World time should be preserved to avoid regressions even if model forgot to emit it
    assert state_changes["world_data"]["world_time"]["hour"] == 10
    # A core memory entry should be recorded to anchor the turn
    core_memories = state_changes["custom_campaign_state"]["core_memories"]
    assert any("sprint across the deck" in entry for entry in core_memories)
    assert extras == {}


def test_tracks_location_when_missing_state_update(base_game_state):
    response = _make_response(
        narrative="You leave the harbor and arrive at the bridge.",
        location_confirmed="Bridge",
        state_updates={},
    )

    state_changes, _ = preventive_guards.enforce_preventive_guards(
        base_game_state, response, constants.MODE_CHARACTER
    )

    assert state_changes["world_data"]["current_location_name"] == "Bridge"
    assert state_changes["custom_campaign_state"]["last_location"] == "Bridge"


def test_falls_back_to_prior_time_when_missing(base_game_state):
    base_game_state.world_data.pop("world_time")
    response = _make_response(
        narrative="The sun hangs high as you rest.",
        dice_rolls=["1d6"],
        state_updates={},
    )

    state_changes, _ = preventive_guards.enforce_preventive_guards(
        base_game_state, response, constants.MODE_CHARACTER
    )

    world_time = state_changes["world_data"]["world_time"]
    assert world_time["hour"] == 12
    assert world_time["minute"] == 0
    assert world_time["time_of_day"] == "midday"


def test_tracks_resource_checkpoint_when_resources_present(base_game_state):
    response = _make_response(
        narrative="You gather herbs and stash them in your pack.",
        resources="inventory: herbs",
        state_updates={},
    )

    state_changes, _ = preventive_guards.enforce_preventive_guards(
        base_game_state, response, constants.MODE_CHARACTER
    )

    assert state_changes["world_resources"]["last_note"] == "inventory: herbs"


def test_preserves_prior_location_when_unknown_confirmed(base_game_state):
    response = _make_response(
        narrative="You circle back, no landmarks in sight.",
        location_confirmed="Unknown",
        state_updates={},
    )

    state_changes, _ = preventive_guards.enforce_preventive_guards(
        base_game_state, response, constants.MODE_CHARACTER
    )

    assert state_changes["world_data"]["current_location_name"] == "Harbor"
    assert state_changes["custom_campaign_state"]["last_location"] == "Harbor"


def test_faction_minigame_enablement_guard_autofills_units(base_game_state):
    base_game_state.custom_campaign_state = {"faction_minigame": {"enabled": False}}
    base_game_state.army_data = {
        "total_strength": 110,
        "forces": {
            "infantry_unit": {"type": "infantry", "blocks": 5},
            "archer_unit": {"type": "archers", "blocks": 3},
            "scout_unit": {"type": "scouts", "blocks": 2},
            "elite_guard_unit": {"type": "elite_guard", "blocks": 1},
        },
    }

    response = _make_response(
        narrative="Enable the faction minigame.",
        state_updates={
            "custom_campaign_state": {
                "faction_minigame": {
                    "enabled": True,
                    "turn_number": 1,
                    "tutorial_started": True,
                    "units": {"soldiers": 0, "spies": 0, "elites": 0},
                    "resources": {"territory": 0},
                    "buildings": {"fortifications": 0},
                    "faction_power": 0,
                    "ranking": 201,
                }
            }
        },
    )

    state_changes, _ = preventive_guards.enforce_preventive_guards(
        base_game_state, response, constants.MODE_CHARACTER
    )
    faction_updates = state_changes.get("custom_campaign_state", {}).get(
        "faction_minigame", {}
    )
    units = faction_updates.get("units", {})

    assert faction_updates.get("tutorial_started") is False
    assert units.get("soldiers") == 80
    assert units.get("spies") == 20
    assert units.get("elites") == 10

    power_result = execute_faction_tool(
        "faction_calculate_power",
        {
            "soldiers": 80,
            "spies": 20,
            "elites": 10,
            "elite_avg_level": 6.0,
            "territory": 0,
            "fortifications": 0,
        },
    )
    assert faction_updates.get("faction_power") == power_result.get("faction_power")
    if power_result.get("faction_power", 0) < MIN_RANK_FP:
        assert faction_updates.get("ranking") is None


def test_persists_dm_notes_from_debug_info(base_game_state):
    """Verify dm_notes are returned as persistence extras, not state_updates.

    This tests the fix for the issue where LLM writes dm_notes to debug_info but
    state_updates must remain canonical. Preventive guards now return merged
    dm_notes in extras for out-of-band persistence to game_state.debug_info.
    """
    response = _make_response(
        narrative="Power level adjusted for Tier 2.",
        debug_info={"dm_notes": ["Updating narrative tone to 'Tier 2 Heroic'"]},
        state_updates={},
    )

    state_changes, extras = preventive_guards.enforce_preventive_guards(
        base_game_state, response, constants.MODE_GOD
    )

    assert "debug_info" not in state_changes
    assert extras["persist_debug_info"]["dm_notes"] == [
        "Updating narrative tone to 'Tier 2 Heroic'"
    ]


def test_dm_notes_merged_with_existing(base_game_state):
    """Verify new dm_notes are appended to existing notes without duplicates."""
    # Set up existing dm_notes in game state
    base_game_state.debug_info = {"dm_notes": ["Previous note"]}

    response = _make_response(
        narrative="Another adjustment.",
        debug_info={"dm_notes": ["New note", "Previous note"]},  # One duplicate
        state_updates={},
    )

    state_changes, extras = preventive_guards.enforce_preventive_guards(
        base_game_state, response, constants.MODE_GOD
    )

    assert "debug_info" not in state_changes
    # Should have both notes, with duplicate removed
    dm_notes = extras["persist_debug_info"]["dm_notes"]
    assert "Previous note" in dm_notes
    assert "New note" in dm_notes
    assert dm_notes.count("Previous note") == 1  # No duplicate


def test_dm_notes_handles_string_input():
    """Verify dm_notes works when LLM returns a string instead of list."""
    game_state = GameState(user_id="user-123")

    response = _make_response(
        narrative="Single note test.",
        debug_info={"dm_notes": "Single note as string"},
        state_updates={},
    )

    state_changes, extras = preventive_guards.enforce_preventive_guards(
        game_state, response, constants.MODE_GOD
    )

    assert "debug_info" not in state_changes
    # String should be normalized to list
    assert extras["persist_debug_info"]["dm_notes"] == ["Single note as string"]


def test_time_based_cooldown_calculates_remaining_hours_correctly():
    """RED TEST: Demonstrates critical bug in time-based cooldown decrement logic.

    Bug Location: preventive_guards.py:493-500

    When a time-based cooldown is active and the player takes a non-damage action,
    the code should calculate cooldown_remaining from the time difference
    (cooldown_until_hour - current_hour), NOT decrement the old turn-based counter.

    Expected: cooldown_remaining = cooldown_until_hour - current_hour = 15 - 12 = 3
    Actual (BUG): cooldown_remaining = old_cd_original - 1 = 2 - 1 = 1
    """
    game_state = GameState(user_id="user-123")

    # Set up world time: current hour is 12
    game_state.world_data["world_time"] = {
        "hour": 12,
        "minute": 0,
        "time_of_day": "day",
    }

    # Set up existing time-based cooldown: expires at hour 15 (3 hours remaining)
    # Also has old turn-based counter of 2 (from before time-based was set)
    game_state.social_hp_challenge = {
        "npc_name": "Lord Valerius",
        "npc_tier": "lord",
        "objective": "Convince to support rebellion",
        "social_hp": 5,
        "social_hp_max": 7,
        "social_hp_damage": 0,  # No damage this turn
        "cooldown_until_hour": 15,  # Time-based: expires at hour 15
        "cooldown_remaining": 2,  # Old turn-based value (should be ignored)
        "status": "RESISTING",
        "skill_used": "Persuasion",
        "resistance_shown": "Lord Valerius listens politely but remains unconvinced.",
        "successes": 2,
        "successes_needed": 5,
    }

    # Player takes a non-damage action (e.g., "wait" or failed persuasion attempt with damage=0)
    response = _make_response(
        narrative="Lord Valerius politely declines to continue the conversation.",
        state_updates={
            "social_hp_challenge": {
                "npc_name": "Lord Valerius",
                "npc_tier": "lord",
                "objective": "Convince to support rebellion",
                "social_hp": 5,  # HP unchanged
                "social_hp_max": 7,
                "social_hp_damage": 0,  # No damage
                "cooldown_until_hour": 15,  # LLM preserves time-based cooldown
                "status": "RESISTING",
                "skill_used": "Persuasion",
                "resistance_shown": "Lord Valerius politely declines.",
                "successes": 2,
                "successes_needed": 5,
            }
        },
    )

    state_changes, _ = preventive_guards.enforce_preventive_guards(
        game_state, response, constants.MODE_CHARACTER
    )

    # CRITICAL ASSERTION: When time-based cooldowns are active, cooldown_until_hour
    # is the authority and should be preserved. The system should enforce time-based
    # cooldown behavior (cooldown_remaining may be removed/None or calculated from time diff).
    challenge = state_changes.get("social_hp_challenge", {})

    # Primary check: cooldown_until_hour must be preserved
    assert challenge.get("cooldown_until_hour") == 15, (
        f"Time-based cooldown_until_hour should be preserved, "
        f"but got {challenge.get('cooldown_until_hour')}"
    )

    # Secondary check: If cooldown_remaining exists, it must be correctly calculated
    # from time difference (not decremented from old turn-based value)
    # cooldown_remaining may be None (removed), or calculated as hours_remaining
    if (
        "cooldown_remaining" in challenge
        and challenge["cooldown_remaining"] is not None
    ):
        expected_remaining = 15 - 12  # cooldown_until_hour - current_hour = 3
        assert challenge["cooldown_remaining"] == expected_remaining, (
            f"If cooldown_remaining exists, it should equal "
            f"cooldown_until_hour(15) - current_hour(12) = {expected_remaining}, "
            f"but got {challenge['cooldown_remaining']}"
        )

    # Verify HP is unchanged (cooldown blocks damage)
    assert challenge["social_hp"] == 5, "HP should remain unchanged during cooldown"


def test_midnight_cooldown_wraparound_bug():
    """RED TEST: Demonstrates critical midnight wraparound bug.

    Bug: When cooldown is set at hour 23, cooldown_until_hour can be 24 (invalid).
    When time advances to hour 0 (midnight), comparison 0 < 24 is True,
    causing cooldown to remain "active" indefinitely.

    Expected: Cooldown should wrap to hour 0 and expire at midnight.
    Actual (BUG): cooldown_until_hour=24, locked out forever.
    """
    game_state = GameState(user_id="user-123")

    # Set up world time: hour 23 (11 PM)
    game_state.world_data["world_time"] = {
        "hour": 23,
        "minute": 45,
        "day": 5,
        "time_of_day": "night",
    }

    # No existing challenge - this will be first damage
    game_state.social_hp_challenge = {}

    # Player deals damage at hour 23 - should trigger cooldown
    response = _make_response(
        narrative="You persuade the guard with compelling arguments.",
        state_updates={
            "social_hp_challenge": {
                "npc_name": "Guard Marcus",
                "npc_tier": "guard",
                "objective": "Get past the gate",
                "social_hp": 2,  # Took 1 damage (was 3)
                "social_hp_max": 3,
                "social_hp_damage": 1,  # Damage dealt
                "status": "WAVERING",
                "skill_used": "Persuasion",
                "resistance_shown": "The guard considers your words.",
                "successes": 1,
                "successes_needed": 5,
            },
            "world_data": {
                "world_time": {
                    "hour": 23,
                    "minute": 50,
                    "day": 5,
                    "time_of_day": "night",
                }
            },
        },
    )

    state_changes, _ = preventive_guards.enforce_preventive_guards(
        game_state, response, constants.MODE_CHARACTER
    )

    challenge = state_changes.get("social_hp_challenge", {})

    # CRITICAL: cooldown_until_hour should wrap to valid 0-23 range
    cooldown_until = challenge.get("cooldown_until_hour")
    assert cooldown_until is not None, "Time-based cooldown should be set"
    assert 0 <= cooldown_until <= 23, (
        f"cooldown_until_hour must be in 0-23 range, got {cooldown_until}. "
        f"Setting cooldown at hour 23 should wrap to hour 0, not 24!"
    )

    # If cooldown_until is 0 (wrapped from 24), verify it works correctly at midnight
    # Simulate next turn at midnight (hour 0)
    game_state.world_data["world_time"] = {
        "hour": 0,
        "minute": 5,
        "day": 6,  # Next day
        "time_of_day": "night",
    }
    game_state.social_hp_challenge = challenge  # Persist the challenge with cooldown

    # Player attempts damage at midnight (cooldown should be expired)
    response2 = _make_response(
        narrative="At midnight, you make another attempt.",
        state_updates={
            "social_hp_challenge": {
                "npc_name": "Guard Marcus",
                "npc_tier": "guard",
                "objective": "Get past the gate",
                "social_hp": 1,  # Took 1 more damage (was 2)
                "social_hp_max": 3,
                "social_hp_damage": 1,  # DAMAGE DEALT - should be allowed since cooldown expired
                "cooldown_until_hour": cooldown_until,  # LLM preserves
                "status": "YIELDING",
                "skill_used": "Persuasion",
                "resistance_shown": "The guard is swayed by your words.",
                "successes": 2,
                "successes_needed": 5,
            },
            "world_data": {
                "world_time": {"hour": 0, "minute": 5, "day": 6, "time_of_day": "night"}
            },
        },
    )

    state_changes2, _ = preventive_guards.enforce_preventive_guards(
        game_state, response2, constants.MODE_CHARACTER
    )

    challenge2 = state_changes2.get("social_hp_challenge", {})

    # CRITICAL TEST: Cooldown expired at hour 0, damage should be ALLOWED
    # If cooldown was still active, damage would be reset to 0
    # If cooldown expired correctly, damage should be 1 (not blocked)
    assert challenge2["social_hp_damage"] == 1, (
        f"Cooldown expired at hour 0, damage should be ALLOWED (not blocked). "
        f"Got damage={challenge2.get('social_hp_damage')}, expected 1"
    )

    assert challenge2["social_hp"] == 1, (
        f"HP should be 1 (took damage after cooldown expired). "
        f"Got HP={challenge2.get('social_hp')}"
    )


def test_cooldown_blocks_damage_when_active():
    """Test that cooldown blocks damage and updates cooldown_remaining correctly.

    Coverage: preventive_guards.py lines 488-504 (cooldown enforcement)
    """
    game_state = GameState(user_id="user-123")
    game_state.world_data["world_time"] = {
        "hour": 10,
        "minute": 0,
        "time_of_day": "day",
    }

    # Set up existing turn-based cooldown (use guard tier with 3 HP)
    game_state.social_hp_challenge = {
        "npc_name": "City Guard",
        "npc_tier": "guard",
        "objective": "Convince to let us pass",
        "social_hp": 3,
        "social_hp_max": 3,
        "social_hp_damage": 0,
        "cooldown_remaining": 2,  # Active cooldown
        "status": "RESISTING",
        "skill_used": "Persuasion",
        "resistance_shown": "The guard is skeptical.",
        "successes": 0,
        "successes_needed": 5,
    }

    # LLM tries to deal damage despite cooldown
    response = _make_response(
        narrative="You make a compelling argument.",
        state_updates={
            "social_hp_challenge": {
                "npc_name": "City Guard",
                "npc_tier": "guard",
                "objective": "Convince to let us pass",
                "social_hp": 2,  # LLM thinks damage dealt
                "social_hp_max": 3,
                "social_hp_damage": 1,  # LLM tries to deal damage (SHOULD BE BLOCKED)
                "status": "WAVERING",
                "skill_used": "Persuasion",
                "resistance_shown": "The guard considers.",
                "successes": 1,
                "successes_needed": 5,
            }
        },
    )

    state_changes, _ = preventive_guards.enforce_preventive_guards(
        game_state, response, constants.MODE_CHARACTER
    )

    challenge = state_changes.get("social_hp_challenge", {})

    # CRITICAL: Damage should be blocked (reset to 0)
    assert challenge["social_hp_damage"] == 0, (
        f"Cooldown should block damage, but got damage={challenge.get('social_hp_damage')}"
    )

    # HP should remain unchanged (not decremented)
    assert challenge["social_hp"] == 3, (
        f"HP should remain 3 (damage blocked), got {challenge.get('social_hp')}"
    )

    # Cooldown should decrement by 1 turn
    assert challenge["cooldown_remaining"] == 1, (
        f"Cooldown should decrement to 1, got {challenge.get('cooldown_remaining')}"
    )


def test_next_day_cooldown_wraparound_detection():
    """Test wraparound detection when current_hour > cooldown_until_hour.

    Coverage: preventive_guards.py lines 458-464 (next-day wraparound logic)

    REAL wraparound scenario (per code comment line 457):
    - Cooldown set at hour 22-23, expires at hour 0 (midnight next day)
    - Current time is hour 23 (late night)
    - hours_diff = 23 - 0 = 23 > 12, so wraparound detected
    - Cooldown should still be ACTIVE until midnight
    """
    game_state = GameState(user_id="user-123")

    # Current time: hour 23 (late night)
    game_state.world_data["world_time"] = {
        "hour": 23,
        "minute": 30,
        "day": 10,
        "time_of_day": "Night",
    }

    # Cooldown set late at night, expires at hour 0 (midnight)
    game_state.social_hp_challenge = {
        "npc_name": "Night Guard",
        "npc_tier": "guard",
        "objective": "Get past checkpoint",
        "social_hp": 2,
        "social_hp_max": 3,
        "social_hp_damage": 0,
        "cooldown_until_hour": 0,  # Expires at midnight (hour 0)
        "status": "RESISTING",
        "skill_used": "Persuasion",
        "resistance_shown": "The guard is unmoved.",
        "successes": 1,
        "successes_needed": 5,
    }

    # Player tries to deal damage at hour 23 (before midnight)
    response = _make_response(
        narrative="You try again to convince the guard.",
        state_updates={
            "social_hp_challenge": {
                "npc_name": "Night Guard",
                "npc_tier": "guard",
                "objective": "Get past checkpoint",
                "social_hp": 1,  # LLM thinks damage dealt
                "social_hp_max": 3,
                "social_hp_damage": 1,  # LLM tries to deal damage
                "cooldown_until_hour": 0,  # LLM preserves cooldown
                "status": "WAVERING",
                "skill_used": "Persuasion",
                "resistance_shown": "The guard hesitates.",
                "successes": 2,
                "successes_needed": 5,
            }
        },
    )

    state_changes, _ = preventive_guards.enforce_preventive_guards(
        game_state, response, constants.MODE_CHARACTER
    )

    challenge = state_changes.get("social_hp_challenge", {})

    # CRITICAL: Damage should be blocked because cooldown is still active
    # Current hour (23) > cooldown_until_hour (0), hours_diff = 23 - 0 = 23 > 12
    # This indicates next-day wraparound (cooldown expires at midnight, not yet reached)
    assert challenge["social_hp_damage"] == 0, (
        f"Cooldown should block damage (next-day wraparound), but got damage={challenge.get('social_hp_damage')}"
    )

    # HP should remain unchanged
    assert challenge["social_hp"] == 2, (
        f"HP should remain 2 (damage blocked), got {challenge.get('social_hp')}"
    )

    # cooldown_until_hour should be preserved (time-based cooldown is still active)
    assert challenge.get("cooldown_until_hour") == 0, (
        f"cooldown_until_hour should be preserved as 0, got {challenge.get('cooldown_until_hour')}"
    )


def test_turn_based_cooldown_when_no_world_time():
    """Test turn-based cooldown is used when world_time doesn't exist.

    Coverage: preventive_guards.py lines 660-662 (turn-based cooldown fallback)

    When world_time is missing/invalid, use_time_based=False and turn-based cooldown
    is used instead.
    """
    game_state = GameState(user_id="user-123")

    # NO world_time set (or invalid world_time)
    # This makes use_time_based=False
    game_state.world_data.pop("world_time", None)

    # No existing challenge
    game_state.social_hp_challenge = {}

    # Player deals damage without world_time
    response = _make_response(
        narrative="You persuade the shopkeeper.",
        state_updates={
            "social_hp_challenge": {
                "npc_name": "Shopkeeper",
                "npc_tier": "guard",  # Use guard tier for 3 HP
                "objective": "Get discount",
                "social_hp": 2,  # Took 1 damage (was 3)
                "social_hp_max": 3,
                "social_hp_damage": 1,  # Damage dealt
                "status": "WAVERING",
                "skill_used": "Persuasion",
                "resistance_shown": "The shopkeeper considers your offer.",
                "successes": 1,
                "successes_needed": 5,
            }
        },
    )

    state_changes, _ = preventive_guards.enforce_preventive_guards(
        game_state, response, constants.MODE_CHARACTER
    )

    challenge = state_changes.get("social_hp_challenge", {})

    # CRITICAL: Since no world_time exists, turn-based cooldown should be used
    assert challenge.get("cooldown_remaining") == 2, (
        f"Turn-based cooldown should be 2 (no world_time), "
        f"got {challenge.get('cooldown_remaining')}"
    )

    # Should NOT have time-based cooldown
    assert "cooldown_until_hour" not in challenge, (
        "Should not have time-based cooldown when world_time doesn't exist"
    )


def test_hp_hallucination_correction():
    """Test that HP hallucinations are corrected to calculated value.

    Coverage: preventive_guards.py lines 740-743 (HP consistency enforcement)
    """
    game_state = GameState(user_id="user-123")

    # Set up existing challenge
    game_state.social_hp_challenge = {
        "npc_name": "Baron",
        "npc_tier": "lord",
        "objective": "Gain support",
        "social_hp": 5,
        "social_hp_max": 7,
        "social_hp_damage": 0,
        "status": "RESISTING",
        "skill_used": "Persuasion",
        "resistance_shown": "The Baron is skeptical.",
        "successes": 0,
        "successes_needed": 5,
    }

    # LLM deals damage but hallucinates the HP value
    response = _make_response(
        narrative="You make a compelling case.",
        state_updates={
            "social_hp_challenge": {
                "npc_name": "Baron",
                "npc_tier": "lord",
                "objective": "Gain support",
                "social_hp": 2,  # HALLUCINATION: Should be 3 (5 - 2 = 3, not 2)
                "social_hp_max": 7,
                "social_hp_damage": 2,  # Deals 2 damage
                "status": "WAVERING",
                "skill_used": "Persuasion",
                "resistance_shown": "The Baron listens carefully.",
                "successes": 1,
                "successes_needed": 5,
            }
        },
    )

    state_changes, _ = preventive_guards.enforce_preventive_guards(
        game_state, response, constants.MODE_CHARACTER
    )

    challenge = state_changes.get("social_hp_challenge", {})

    # CRITICAL: HP should be corrected to calculated value (5 - 2 = 3)
    assert challenge["social_hp"] == 3, (
        f"HP hallucination should be corrected from 2 to 3 (5 - 2), "
        f"got {challenge.get('social_hp')}"
    )

    # Damage should remain unchanged
    assert challenge["social_hp_damage"] == 2, (
        f"Damage should remain 2, got {challenge.get('social_hp_damage')}"
    )


def test_to_int_edge_cases():
    """Test _to_int helper function handles edge cases correctly.

    Coverage: preventive_guards.py lines 81-82 (exception handling)

    The _to_int function is used throughout preventive_guards.py to safely
    coerce values to integers. This test verifies it handles invalid types.
    """
    from mvp_site.preventive_guards import _to_int

    # Valid conversions
    assert _to_int(5) == 5
    assert _to_int("10") == 10
    assert _to_int(3.7) == 3
    assert _to_int(None, default=99) == 99

    # Invalid types should return default (lines 81-82)
    assert _to_int("invalid", default=0) == 0
    assert _to_int([], default=0) == 0
    assert _to_int({}, default=0) == 0
    assert _to_int(object(), default=42) == 42

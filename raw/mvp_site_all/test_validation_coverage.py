"""
Coverage tests for mvp_site.schemas.validation module.

These tests target the uncovered functions to bring coverage from 28% to 60%+.
Focus areas: check_datetime, _enrich_validation_message, is_valid_game_state,
get_common_field_paths, _normalize_dotted_state_update_keys, _normalize_for_similarity,
_get_near_match_suggestions, caching behavior, and property accessors.
"""

import pytest
from jsonschema import Draft202012Validator

from mvp_site.schemas.validation import (
    _enrich_validation_message,
    _get_near_match_suggestions,
    _normalize_dotted_state_update_keys,
    _normalize_for_similarity,
    check_datetime,
    get_canonical_equipment_slots,
    get_common_field_paths,
    get_game_state_top_level_properties,
    get_known_equipment_slots,
    get_legacy_equipment_slot_aliases,
    get_social_hp_request_severity_values,
    get_social_hp_skill_values,
    get_strict_overlay_nested_allowed_keys,
    get_story_entry_validator,
    get_validator,
    is_valid_game_state,
    load_schema,
    sanitize_state_updates_overlay,
    validate_story_entry,
)


# ---- check_datetime ----


class TestCheckDatetime:
    """Tests for the RFC 3339 date-time format checker."""

    def test_valid_rfc3339_utc(self):
        assert check_datetime("2024-01-01T00:00:00Z") is True

    def test_valid_rfc3339_positive_offset(self):
        assert check_datetime("2024-06-15T12:30:00+05:00") is True

    def test_valid_rfc3339_negative_offset(self):
        assert check_datetime("2024-06-15T12:30:00-08:00") is True

    def test_valid_with_microseconds(self):
        assert check_datetime("2024-01-15T10:20:30.123456Z") is True

    def test_invalid_format(self):
        with pytest.raises(ValueError, match="Invalid date-time"):
            check_datetime("not-a-date")

    def test_invalid_month(self):
        with pytest.raises(ValueError, match="Invalid date-time"):
            check_datetime("2024-13-01T00:00:00Z")

    def test_missing_timezone(self):
        with pytest.raises(ValueError, match="Invalid date-time"):
            check_datetime("2024-01-01T00:00:00")

    def test_non_string_returns_true(self):
        assert check_datetime(123) is True
        assert check_datetime(None) is True
        assert check_datetime({"date": "2024-01-01"}) is True

    def test_date_only_no_time(self):
        with pytest.raises(ValueError, match="Invalid date-time"):
            check_datetime("2024-01-01")

    def test_invalid_day_32(self):
        with pytest.raises(ValueError, match="Invalid date-time"):
            check_datetime("2024-01-32T00:00:00Z")


# ---- _enrich_validation_message ----


class TestEnrichValidationMessage:
    """Tests for the player_character_data validation hint enrichment."""

    def test_enriches_oneOf_player_character_data(self):
        result = _enrich_validation_message(
            "player_character_data",
            "1 is not valid under any of the given schemas",
            "oneOf",
        )
        assert "GOD_MODE_UPDATE_STATE" in result
        assert "'player_character_data' to null" in result
        assert "entity_id" in result

    def test_enriches_anyOf_player_character_data(self):
        result = _enrich_validation_message(
            "player_character_data",
            "1 is not valid under any of the given schemas",
            "anyOf",
        )
        assert "GOD_MODE_UPDATE_STATE" in result

    def test_no_enrichment_different_path(self):
        msg = "1 is not valid under any of the given schemas"
        assert _enrich_validation_message("other_data", msg, "oneOf") == msg

    def test_no_enrichment_different_validator(self):
        msg = "1 is not valid under any of the given schemas"
        assert _enrich_validation_message("player_character_data", msg, "required") == msg

    def test_no_enrichment_different_message(self):
        msg = "Field is required"
        assert _enrich_validation_message("player_character_data", msg, "oneOf") == msg


# ---- is_valid_game_state ----


class TestIsValidGameState:
    """Tests for the boolean validity check."""

    def test_empty_dict_invalid(self):
        assert is_valid_game_state({}) is False

    def test_returns_boolean(self):
        assert isinstance(is_valid_game_state({}), bool)
        assert isinstance(is_valid_game_state({"game_state_version": 1}), bool)


# ---- _normalize_for_similarity ----


class TestNormalizeForSimilarity:
    """Tests for the string normalization helper."""

    def test_lowercase(self):
        assert _normalize_for_similarity("HELLO") == "hello"

    def test_hyphens_to_underscores(self):
        assert _normalize_for_similarity("player-character") == "player_character"

    def test_spaces_to_underscores(self):
        assert _normalize_for_similarity("main hand") == "main_hand"

    def test_combined(self):
        assert _normalize_for_similarity("Main-Hand Slot") == "main_hand_slot"

    def test_strips_whitespace(self):
        assert _normalize_for_similarity("  item  ") == "item"

    def test_empty_string(self):
        assert _normalize_for_similarity("") == ""


# ---- _get_near_match_suggestions ----


class TestGetNearMatchSuggestions:
    """Tests for the typo-match suggestion helper."""

    def test_close_match(self):
        result = _get_near_match_suggestions("mainhand", {"main_hand", "off_hand", "head"})
        assert len(result) > 0

    def test_no_match(self):
        result = _get_near_match_suggestions("xyz_unknown", {"main_hand", "off_hand", "head"})
        assert result == []

    def test_empty_unknown(self):
        assert _get_near_match_suggestions("", {"main_hand", "off_hand"}) == []

    def test_empty_allowed(self):
        assert _get_near_match_suggestions("something", set()) == []

    def test_max_results(self):
        result = _get_near_match_suggestions(
            "test", {"test1", "test2", "test3", "test4"}, max_results=2
        )
        assert len(result) <= 2

    def test_exact_match(self):
        result = _get_near_match_suggestions("main_hand", {"main_hand", "off_hand"})
        assert isinstance(result, list)


# ---- load_schema / get_validator ----


class TestLoadSchemaAndValidator:
    """Tests for schema loading, caching, and validator creation."""

    def test_load_schema_nonexistent(self):
        with pytest.raises(FileNotFoundError, match="Schema file not found"):
            load_schema("nonexistent_schema_xyz_abc")

    def test_load_schema_game_state(self):
        schema = load_schema("game_state")
        assert isinstance(schema, dict)
        assert "$defs" in schema

    def test_load_schema_caching(self):
        s1 = load_schema("game_state")
        s2 = load_schema("game_state")
        assert s1 is s2

    def test_get_validator_type(self):
        validator = get_validator("game_state")
        assert isinstance(validator, Draft202012Validator)

    def test_get_validator_caching(self):
        v1 = get_validator("game_state")
        v2 = get_validator("game_state")
        assert v1 is v2


# ---- get_common_field_paths ----


class TestGetCommonFieldPaths:
    """Tests for schema-derived common field paths."""

    def test_returns_dict_of_strings(self):
        result = get_common_field_paths()
        assert isinstance(result, dict)
        for k, v in result.items():
            assert isinstance(k, str)
            assert isinstance(v, str)

    def test_pc_resources(self):
        result = get_common_field_paths()
        assert result["pc.resources"] == "player_character_data.resources"

    def test_pc_equipment(self):
        result = get_common_field_paths()
        assert result["pc.equipment"] == "player_character_data.equipment"

    def test_pc_stats(self):
        assert get_common_field_paths()["pc.stats"] == "player_character_data.stats"

    def test_pc_experience(self):
        assert "pc.experience" in get_common_field_paths()

    def test_pc_health(self):
        assert "pc.health" in get_common_field_paths()

    def test_pc_level(self):
        assert "pc.level" in get_common_field_paths()

    def test_world_time(self):
        assert get_common_field_paths()["world.time"] == "world_data.world_time"

    def test_combat_state(self):
        assert get_common_field_paths()["combat.state"] == "combat_state"

    def test_top_level_keys_exist(self):
        result = get_common_field_paths()
        top_keys = [k for k in result if k.startswith("top.")]
        assert len(top_keys) > 0

    def test_world_locations(self):
        assert "world.locations" in get_common_field_paths()

    def test_caching_returns_equal_but_different_objects(self):
        r1 = get_common_field_paths()
        r2 = get_common_field_paths()
        assert r1 == r2
        assert r1 is not r2


# ---- _normalize_dotted_state_update_keys ----


class TestNormalizeDottedStateUpdateKeys:
    """Tests for the dotted-key expansion utility."""

    def test_basic_expansion(self):
        state = {"player_character_data.experience.current": 123}
        corrections = []
        _normalize_dotted_state_update_keys(state, corrections)
        assert "player_character_data.experience.current" not in state
        assert state["player_character_data"]["experience"]["current"] == 123
        assert len(corrections) == 1
        assert "Expanded" in corrections[0]

    def test_strips_state_updates_prefix(self):
        state = {"state_updates.world_data.world_time": "2026-01-01T00:00:00Z"}
        corrections = []
        _normalize_dotted_state_update_keys(state, corrections)
        assert state["world_data"]["world_time"] == "2026-01-01T00:00:00Z"

    def test_non_dict_input_no_crash(self):
        corrections = []
        _normalize_dotted_state_update_keys(None, corrections)
        _normalize_dotted_state_update_keys("not a dict", corrections)
        _normalize_dotted_state_update_keys([], corrections)

    def test_conflict_intermediate_non_dict(self):
        state = {
            "player_character_data": "already_a_string",
            "player_character_data.experience.current": 123,
        }
        corrections = []
        _normalize_dotted_state_update_keys(state, corrections)
        assert "player_character_data.experience.current" in state
        assert state["player_character_data"] == "already_a_string"
        assert any("conflict" in c.lower() for c in corrections)

    def test_duplicate_target_kept(self):
        state = {
            "player_character_data": {"experience": {"current": 50}},
            "player_character_data.experience.current": 123,
        }
        corrections = []
        _normalize_dotted_state_update_keys(state, corrections)
        assert "player_character_data.experience.current" in state
        assert state["player_character_data"]["experience"]["current"] == 50
        assert any("already present" in c for c in corrections)

    def test_ignores_single_part_keys(self):
        state = {"player_character_data": {"name": "Test"}}
        corrections = []
        _normalize_dotted_state_update_keys(state, corrections)
        assert state == {"player_character_data": {"name": "Test"}}
        assert len(corrections) == 0

    def test_multiple_dotted_keys(self):
        state = {
            "player_character_data.experience.current": 100,
            "world_data.world_time": "2026-01-01T00:00:00Z",
            "combat_state.in_combat": True,
        }
        corrections = []
        _normalize_dotted_state_update_keys(state, corrections)
        assert state["player_character_data"]["experience"]["current"] == 100
        assert state["world_data"]["world_time"] == "2026-01-01T00:00:00Z"
        assert state["combat_state"]["in_combat"] is True
        assert len(corrections) == 3

    def test_empty_dict(self):
        state = {}
        corrections = []
        _normalize_dotted_state_update_keys(state, corrections)
        assert state == {}
        assert len(corrections) == 0


# ---- get_game_state_top_level_properties ----


class TestGetGameStateTopLevelProperties:
    """Tests for schema-derived top-level property keys."""

    def test_returns_set_of_strings(self):
        result = get_game_state_top_level_properties()
        assert isinstance(result, set)
        assert all(isinstance(k, str) for k in result)

    def test_contains_expected_keys(self):
        result = get_game_state_top_level_properties()
        assert {"game_state_version", "player_character_data", "world_data"}.issubset(result)

    def test_caching_defensive_copy(self):
        r1 = get_game_state_top_level_properties()
        r2 = get_game_state_top_level_properties()
        assert r1 == r2
        assert r1 is not r2


# ---- get_known_equipment_slots ----


class TestGetKnownEquipmentSlots:
    """Tests for equipment slot enumeration with legacy support."""

    def test_legacy_true_superset_of_false(self):
        with_legacy = get_known_equipment_slots(include_legacy=True)
        without_legacy = get_known_equipment_slots(include_legacy=False)
        assert without_legacy.issubset(with_legacy)
        assert len(with_legacy) >= len(without_legacy)

    def test_canonical_always_included(self):
        canonical = get_canonical_equipment_slots()
        assert canonical.issubset(get_known_equipment_slots(include_legacy=True))
        assert canonical.issubset(get_known_equipment_slots(include_legacy=False))

    def test_legacy_adds_extra_slots(self):
        extra = get_known_equipment_slots(include_legacy=True) - get_known_equipment_slots(
            include_legacy=False
        )
        assert len(extra) > 0


# ---- get_strict_overlay_nested_allowed_keys ----


class TestGetStrictOverlayNestedAllowedKeys:
    """Tests for strict nested key allowlists."""

    def test_returns_dict_of_sets(self):
        result = get_strict_overlay_nested_allowed_keys()
        assert isinstance(result, dict)
        assert all(isinstance(v, set) for v in result.values())

    def test_contains_combat_state(self):
        result = get_strict_overlay_nested_allowed_keys()
        assert "combat_state" in result
        assert len(result["combat_state"]) > 0

    def test_contains_all_expected_keys(self):
        result = get_strict_overlay_nested_allowed_keys()
        expected = {"combat_state", "encounter_state", "rewards_pending", "custom_campaign_state"}
        assert expected.issubset(result.keys())

    def test_caching_defensive_copy(self):
        r1 = get_strict_overlay_nested_allowed_keys()
        r2 = get_strict_overlay_nested_allowed_keys()
        assert r1 == r2
        assert r1 is not r2
        for key in r1:
            assert r1[key] is not r2[key]


# ---- get_social_hp_request_severity_values / get_social_hp_skill_values ----


class TestSocialHpEnumValues:
    """Tests for social HP enum value accessors."""

    def test_severity_returns_nonempty_set(self):
        result = get_social_hp_request_severity_values()
        assert isinstance(result, set) and len(result) > 0
        assert all(isinstance(v, str) and v.strip() for v in result)

    def test_severity_caching(self):
        r1 = get_social_hp_request_severity_values()
        r2 = get_social_hp_request_severity_values()
        assert r1 == r2
        assert r1 is not r2

    def test_skills_returns_nonempty_set(self):
        result = get_social_hp_skill_values()
        assert isinstance(result, set) and len(result) > 0
        assert all(isinstance(v, str) and v.strip() for v in result)

    def test_skills_caching(self):
        r1 = get_social_hp_skill_values()
        r2 = get_social_hp_skill_values()
        assert r1 == r2
        assert r1 is not r2


# ---- Integration: sanitize with dotted keys ----


class TestSanitizeDottedKeysIntegration:
    """Integration tests combining normalize + sanitize."""

    def test_sanitize_expands_dotted_keys(self):
        state = {
            "player_character_data.experience.current": 100,
            "world_data.world_time": "2026-01-01T00:00:00Z",
        }
        sanitized, corrections = sanitize_state_updates_overlay(state)
        assert "player_character_data" in sanitized
        assert "world_data" in sanitized
        assert len(corrections) > 0

    def test_sanitize_preserves_valid_nested(self):
        state = {"player_character_data": {"level": 5}}
        sanitized, corrections = sanitize_state_updates_overlay(state)
        assert sanitized["player_character_data"]["level"] == 5


# ---- get_legacy_equipment_slot_aliases ----


class TestLegacyEquipmentSlotAliases:
    """Tests for legacy equipment slot alias mapping."""

    def test_get_legacy_equipment_slot_aliases_returns_dict(self):
        """Test that legacy alias getter returns a dictionary."""
        aliases = get_legacy_equipment_slot_aliases()
        assert isinstance(aliases, dict)

    def test_get_legacy_equipment_slot_aliases_not_empty(self):
        """Test that there are some legacy aliases defined."""
        aliases = get_legacy_equipment_slot_aliases()
        assert len(aliases) > 0


# ---- validate_game_state performance path ----


class TestValidateGameStatePerformance:
    """Tests for validate_game_state to cover performance timing path."""

    def test_validate_game_state_with_warnings(self, monkeypatch):
        """Test validation when it takes longer than threshold."""
        import os
        import time
        from mvp_site.schemas.validation import validate_game_state

        # Set a very low threshold to trigger warning path
        monkeypatch.setenv("SCHEMA_VALIDATION_WARN_MS", "0")

        # Valid game state that will trigger validation
        valid_state = {
            "world": {"name": "Test World"},
            "player_character_data": {
                "name": "Test Player",
                "character_class": "Fighter",
                "level": 1,
            },
        }

        # This should complete without error (warning is logged, not raised)
        errors = validate_game_state(valid_state)
        assert isinstance(errors, list)


# ---- validate_story_entry and get_story_entry_validator ----


class TestStoryEntryValidation:
    """Tests for story entry validation functions."""

    def test_validate_story_entry_valid(self):
        """Test validation of a valid story entry."""
        valid_entry = {
            "actor": "gm",
            "text": "The party enters the tavern.",
            "timestamp": "2026-01-15T10:30:00Z",
            "part": 1,
        }
        errors = validate_story_entry(valid_entry)
        assert errors == []

    def test_validate_story_entry_not_dict(self):
        """Test validation rejects non-dict input."""
        errors = validate_story_entry("not a dict")
        assert errors == ["story_entry: must be a dict"]

    def test_validate_story_entry_none(self):
        """Test validation rejects None input."""
        errors = validate_story_entry(None)
        assert errors == ["story_entry: must be a dict"]

    def test_validate_story_entry_invalid(self):
        """Test validation catches schema violations."""
        invalid_entry = {"session_id": 123}  # Should be string
        errors = validate_story_entry(invalid_entry)
        assert len(errors) > 0

    def test_get_story_entry_validator_returns_validator(self):
        """Test that validator getter returns a Draft202012Validator."""
        validator = get_story_entry_validator()
        assert isinstance(validator, Draft202012Validator)

    def test_get_story_entry_validator_caching(self):
        """Test that validator is cached."""
        v1 = get_story_entry_validator()
        v2 = get_story_entry_validator()
        assert v1 is v2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

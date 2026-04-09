"""
Tests for JSON Schema validation warnings (PR #4534 critical issues).

This test suite verifies:
1. REV-3q63: Schema detects empty game states (empty required array)
2. REV-diq9: Schema detects invalid player_character_data (catch-all bypass)
3. REV-rrom: Validation failures surface in corrections (non-blocking warnings)

TDD Approach: These tests are written BEFORE fixes to ensure they fail first (Red phase).

NOTE: Schema validation is non-blocking by design. Invalid states generate GCP logs
and correction warnings but do NOT raise exceptions to avoid blocking gameplay.
"""

import pytest

from mvp_site.game_state import validate_and_correct_state
from mvp_site.narrative_response_schema import NarrativeResponse
from mvp_site.schemas.validation import (
    get_canonical_equipment_slots,
    get_legacy_equipment_slot_aliases,
    get_social_hp_request_severity_values,
    get_social_hp_skill_values,
    sanitize_state_updates_overlay,
    validate_game_state,
    validate_story_entry,
    validate_state_updates_overlay,
)


class TestSchemaValidationEnforcement:
    """Test that schema validation is properly enforced."""

    def test_empty_game_state_fails_validation(self):
        """
        REV-3q63: Empty game state should fail validation.

        The schema currently has "required": [] at top level, which allows
        empty objects. This test verifies the schema requires minimum fields.

        Expected to FAIL initially (Red phase).
        """
        empty_state = {}

        # Direct schema validation should fail
        schema_errors = validate_game_state(empty_state)
        assert len(schema_errors) > 0, (
            "Empty game state should fail schema validation. "
            "Schema 'required' array is likely empty."
        )
        assert any("game_state_version" in err or "required" in err for err in schema_errors), (
            "Schema errors should mention missing required fields like 'game_state_version'"
        )

    def test_minimal_valid_game_state_passes(self):
        """
        REV-3q63: Minimal valid game state with required fields should pass.

        This test defines what SHOULD be the minimum valid game state.
        Expected to FAIL initially until schema is fixed.
        """
        minimal_state = {
            "game_state_version": 2,
            "session_id": "test-session-123",
            "turn_number": 1,
        }

        schema_errors = validate_game_state(minimal_state)
        assert len(schema_errors) == 0, (
            f"Minimal valid game state should pass validation. Errors: {schema_errors}"
        )

    def test_invalid_player_character_data_fails(self):
        """
        REV-diq9: Invalid player_character_data should fail validation.

        The schema currently has a catch-all branch:
        {"type": "object", "minProperties": 1}

        This allows {"garbage": true} to pass. This test verifies the schema
        only accepts valid PlayerCharacter structure or null.

        Expected to FAIL initially (Red phase).
        """
        invalid_state = {
            "game_state_version": 2,
            "session_id": "test-session-123",
            "turn_number": 1,
            "player_character_data": {
                "garbage": True,
                "not_a_valid_field": "should fail"
            }
        }

        schema_errors = validate_game_state(invalid_state)
        assert len(schema_errors) > 0, (
            "Invalid player_character_data should fail schema validation. "
            "Schema likely has catch-all branch allowing any object."
        )
        assert any("player_character_data" in err for err in schema_errors), (
            "Schema errors should mention player_character_data validation failure"
        )

    def test_valid_player_character_data_passes(self):
        """
        REV-diq9: Valid player_character_data should pass validation.

        Note: This test is marked as expected to fail until we have a complete
        valid PlayerCharacter fixture that matches all schema requirements.
        The key fix (removing catch-all) is tested by test_invalid_player_character_data_fails.
        """
        pytest.skip(
            "Skipping until we have complete PlayerCharacter fixture. "
            "The critical fix (catch-all removal) is tested by test_invalid_player_character_data_fails"
        )

    def test_null_player_character_data_passes(self):
        """
        REV-diq9: null player_character_data should be allowed.

        During early initialization, player_character_data can be null.
        """
        state_with_null_pc = {
            "game_state_version": 2,
            "session_id": "test-session-123",
            "turn_number": 1,
            "player_character_data": None
        }

        schema_errors = validate_game_state(state_with_null_pc)
        assert len(schema_errors) == 0, (
            f"null player_character_data should be valid. Errors: {schema_errors}"
        )

    def test_validation_failures_surface_in_corrections(self):
        """
        REV-rrom: validate_and_correct_state surfaces schema failures in corrections list.

        Schema validation is non-blocking by design (warn, don't crash) to avoid
        blocking gameplay. Failures are surfaced in the corrections list so callers
        can log or display them.
        """
        invalid_state = {
            "garbage": True,
            "not_valid": "state"
        }

        result_state, corrections = validate_and_correct_state(
            invalid_state, return_corrections=True
        )
        schema_corrections = [c for c in corrections if "Schema validation" in c]
        assert len(schema_corrections) > 0, (
            "Schema validation errors should appear in corrections list, not be silently ignored"
        )

    def test_validation_failures_not_silently_ignored(self):
        """
        REV-rrom: Schema validation failures must not be silently ignored.

        Validation is non-blocking (no ValueError), but failures MUST appear
        in the corrections list when return_corrections=True.
        """
        completely_invalid = {
            "this": "should",
            "never": "work"
        }

        result_state, corrections = validate_and_correct_state(
            completely_invalid, return_corrections=True
        )
        schema_corrections = [c for c in corrections if "Schema validation" in c]
        assert len(schema_corrections) > 0, (
            "Schema failures must surface in corrections, not be silently swallowed"
        )

    def test_action_resolution_rolls_require_canonical_fields(self):
        """REV-8jgbe: malformed roll items should fail canonical schema validation."""
        state = {
            "game_state_version": 2,
            "session_id": "test-session-123",
            "turn_number": 1,
            "action_resolution": {
                "reinterpreted": False,
                "audit_flags": [],
                "mechanics": {
                    "type": "skill_check",
                    "rolls": [
                        {
                            "purpose": "Athletics Check",
                            "dc": 15,
                        }
                    ],
                },
            },
        }

        schema_errors = validate_game_state(state)
        assert any("action_resolution" in err for err in schema_errors), schema_errors
        assert any("rolls" in err for err in schema_errors), schema_errors

    def test_action_resolution_rolls_accept_canonical_shape(self):
        """REV-8jgbe: canonical roll items should pass schema validation."""
        state = {
            "game_state_version": 2,
            "session_id": "test-session-123",
            "turn_number": 1,
            "action_resolution": {
                "reinterpreted": False,
                "audit_flags": [],
                "mechanics": {
                    "type": "skill_check",
                    "rolls": [
                        {
                            "notation": "1d20+3",
                            "result": 17,
                            "success": True,
                            "purpose": "Athletics Check",
                            "dc": 15,
                            "die_type": "d20",
                        }
                    ],
                },
            },
        }

        schema_errors = validate_game_state(state)
        assert schema_errors == [], schema_errors


class TestSchemaValidationIntegration:
    """Integration tests for schema validation in the full pipeline."""

    def test_world_logic_validation_returns_warnings(self):
        """
        REV-rrom: Verify world_logic.py validation returns non-blocking warnings.

        This would test _validate_state_with_runtime_policy but that function
        is internal to world_logic. If it's exported, we should test it directly.

        For now, this is a placeholder for integration testing.
        """
        # TODO: Add integration test with world_logic._validate_state_with_runtime_policy
        # to verify it returns corrections without raising exceptions
        pytest.skip("Integration test placeholder - validation is non-blocking by design")


class TestStoryEntryContractValidation:
    """Contract tests for canonical Firestore story-entry validation."""

    def test_story_entry_rejects_missing_required_fields(self):
        errors = validate_story_entry({"actor": "gemini", "text": "hello"})
        assert any("timestamp" in err for err in errors), errors
        assert any("part" in err for err in errors), errors

    def test_story_entry_accepts_canonical_action_resolution(self):
        errors = validate_story_entry(
            {
                "actor": "gemini",
                "text": "You leap forward.",
                "timestamp": "2026-02-15T08:00:00Z",
                "part": 1,
                "action_resolution": {
                    "reinterpreted": False,
                    "audit_flags": [],
                    "mechanics": {
                        "type": "skill_check",
                        "rolls": [
                            {
                                "notation": "1d20+5",
                                "result": 19,
                                "success": True,
                                "purpose": "Athletics Check",
                            }
                        ],
                    },
                },
            }
        )
        assert errors == [], errors


class TestCanonicalEquipmentSlotContract:
    """Contract tests for canonical and legacy equipment slot vocabularies."""

    def test_canonical_equipment_slots_come_from_schema(self):
        slots = get_canonical_equipment_slots()

        assert "main_hand" in slots
        assert "off_hand" in slots
        assert "belt" in slots
        assert "instrument" in slots

    def test_legacy_slot_aliases_include_known_migrations(self):
        aliases = get_legacy_equipment_slot_aliases()

        assert aliases["weapon_main"] == "main_hand"
        assert aliases["boots"] == "feet"


class TestCanonicalSocialHpContract:
    """Contract tests for social HP enums sourced from canonical schema."""

    def test_request_severity_values_come_from_schema(self):
        assert get_social_hp_request_severity_values() == {
            "information",
            "favor",
            "submission",
        }

    def test_skill_values_come_from_schema(self):
        assert get_social_hp_skill_values() == {
            "Persuasion",
            "Deception",
            "Intimidation",
            "Insight",
        }


class TestStateUpdateOverlayValidation:
    """Strict overlay validation for high-risk additionalProperties regions."""

    def test_rejects_unknown_top_level_state_update_keys(self):
        _, errors = validate_state_updates_overlay({"made_up_key": 123})
        assert any("state_updates.made_up_key" in error for error in errors), errors

    def test_rejects_unknown_equipment_slots(self):
        updates = {
            "player_character_data": {
                "equipment": {
                    "mystery_slot": {"name": "Orb of Confusion", "type": "wondrous"}
                }
            }
        }
        warnings, _ = validate_state_updates_overlay(updates)
        assert any(
            "player_character_data.equipment.mystery_slot" in w for w in warnings
        ), warnings

    def test_rejects_unknown_resource_keys(self):
        updates = {"player_character_data": {"resources": {"mana_crystals": 5}}}
        warnings, _ = validate_state_updates_overlay(updates)
        assert any(
            "player_character_data.resources.mana_crystals" in w for w in warnings
        ), warnings

    def test_accepts_known_equipment_and_resource_keys(self):
        updates = {
            "player_character_data": {
                "equipment": {"belt": {"name": "Belt of Giant Strength"}},
                "resources": {"gold": 150, "hit_dice": {"used": 1, "total": 5}},
            }
        }
        _, errors = validate_state_updates_overlay(updates)
        assert errors == [], errors

    def test_accepts_living_world_top_level_state_update_keys(self):
        updates = {
            "world_events": {"background_events": [{"event_type": "test"}]},
            "faction_updates": {"thieves_guild": {"status": "active"}},
            "time_events": {"market_day": {"status": "scheduled"}},
            "rumors": [{"text": "Something stirs in the hills"}],
            "scene_event": {"type": "ambush", "description": "Bandits attack"},
            "complications": {"triggered": True, "description": "Storm intensifies"},
        }

        _, errors = validate_state_updates_overlay(updates)
        assert errors == [], errors

    def test_accepts_prompt_documented_equipment_slots(self):
        updates = {
            "player_character_data": {
                "equipment": {
                    "shoulders": {"name": "Cloak of Shadows"},
                    "chest": {"name": "Demon Plate Armor"},
                    "waist": {"name": "Belt of Fire Giant Strength"},
                    "legs": {"name": "Greaves of the Juggernaut"},
                }
            }
        }

        _, errors = validate_state_updates_overlay(updates)
        assert errors == [], errors

    def test_rejects_unknown_nested_state_update_keys_with_suggestions(self):
        updates = {
            "combat_state": {
                "combat_fase": "ended",
                "rewards_proceessed": False,
            },
            "custom_campaign_state": {
                "level_up_peding": True,
            },
        }

        warnings, _ = validate_state_updates_overlay(updates)

        assert any(
            "combat_state.combat_fase" in w and "combat_phase" in w
            for w in warnings
        ), warnings
        assert any(
            "combat_state.rewards_proceessed" in w and "rewards_processed" in w
            for w in warnings
        ), warnings
        assert any(
            "custom_campaign_state.level_up_peding" in w
            and "level_up_pending" in w
            for w in warnings
        ), warnings

    def test_sanitize_overlay_maps_unknown_nested_state_update_keys(self):
        updates = {
            "combat_state": {
                "combat_fase": "ended",
                "rewards_proceessed": False,
            },
            "custom_campaign_state": {
                "level_up_peding": True,
            },
        }

        sanitized, corrections = sanitize_state_updates_overlay(updates)

        combat_state = sanitized.get("combat_state", {})
        custom_campaign_state = sanitized.get("custom_campaign_state", {})
        assert "combat_fase" not in combat_state
        assert "rewards_proceessed" not in combat_state
        assert combat_state.get("combat_phase") == "ended"
        assert combat_state.get("rewards_processed") is False
        assert "level_up_peding" not in custom_campaign_state
        assert custom_campaign_state.get("level_up_pending") is True
        assert any(
            "Mapped state_updates.combat_state.combat_fase" in correction
            and "combat_phase" in correction
            for correction in corrections
        ), corrections
        assert any(
            "Mapped state_updates.combat_state.rewards_proceessed" in correction
            and "rewards_processed" in correction
            for correction in corrections
        ), corrections
        assert any(
            "Mapped state_updates.custom_campaign_state.level_up_peding" in correction
            and "level_up_pending" in correction
            for correction in corrections
        ), corrections

    def test_sanitize_overlay_keeps_unknown_keys_without_close_match(self):
        updates = {
            "made_up_key": 123,
            "player_character_data": {
                "equipment": {"mystery_slot": {"name": "Orb"}, "belt": {"name": "Belt"}},
                "resources": {"mana_crystals": 5, "gold": 100},
            },
        }
        sanitized, errors = sanitize_state_updates_overlay(updates)

        assert sanitized.get("made_up_key") == 123
        player_data = sanitized.get("player_character_data", {})
        equipment = player_data.get("equipment", {})
        resources = player_data.get("resources", {})
        assert "mystery_slot" in equipment
        assert "mana_crystals" in resources
        assert "belt" in equipment
        assert resources.get("gold") == 100
        assert errors, "Sanitization should report unknown keys"

    def test_validate_overlay_accepts_dotted_player_experience_key(self):
        updates = {
            "player_character_data.experience.progress_display": "95%",
        }

        _, errors = validate_state_updates_overlay(updates)
        assert errors == [], errors

    def test_validate_overlay_accepts_prefixed_dotted_world_time_key(self):
        updates = {
            "state_updates.world_data.world_time.microsecond": 1,
        }

        _, errors = validate_state_updates_overlay(updates)
        assert errors == [], errors

    def test_sanitize_overlay_expands_dotted_player_experience_key(self):
        updates = {
            "player_character_data.experience.progress_display": "95%",
        }

        sanitized, corrections = sanitize_state_updates_overlay(updates)
        player_data = sanitized.get("player_character_data", {})
        experience = player_data.get("experience", {})
        assert experience.get("progress_display") == "95%"
        assert (
            "player_character_data.experience.progress_display" not in sanitized
        )
        assert any(
            "Expanded state_updates.player_character_data.experience.progress_display"
            in correction
            for correction in corrections
        ), corrections

    def test_sanitize_overlay_expands_prefixed_dotted_world_time_key(self):
        updates = {
            "state_updates.world_data.world_time.microsecond": 1,
        }

        sanitized, corrections = sanitize_state_updates_overlay(updates)
        world_data = sanitized.get("world_data", {})
        world_time = world_data.get("world_time", {})
        assert world_time.get("microsecond") == 1
        assert "state_updates" not in sanitized
        assert any(
            "Expanded state_updates.world_data.world_time.microsecond"
            in correction
            for correction in corrections
        ), corrections

    def test_sanitize_overlay_canonicalizes_nested_frozen_plans(self):
        updates = {
            "state_updates.custom_campaign_state.frozen_plans": {
                "plan_a": {
                    "failed_at": "2026-02-18T00:00:00Z",
                    "freeze_until": "2026-02-19T00:00:00Z",
                    "original_dc": 15,
                    "freeze_hours": 24,
                    "description": "test",
                }
            }
        }

        sanitized, corrections = sanitize_state_updates_overlay(updates)
        assert "frozen_plans" in sanitized
        custom_state = sanitized.get("custom_campaign_state", {})
        assert isinstance(custom_state, dict)
        assert "frozen_plans" not in custom_state
        assert any(
            "Mapped state_updates.custom_campaign_state.frozen_plans -> state_updates.frozen_plans"
            in correction
            for correction in corrections
        ), corrections

    def test_validate_overlay_no_warning_for_canonicalized_nested_frozen_plans(self):
        updates = {
            "state_updates.custom_campaign_state.frozen_plans": {
                "plan_a": {
                    "failed_at": "2026-02-18T00:00:00Z",
                    "freeze_until": "2026-02-19T00:00:00Z",
                    "original_dc": 15,
                    "freeze_hours": 24,
                    "description": "test",
                }
            }
        }

        warnings, errors = validate_state_updates_overlay(updates)
        assert errors == [], errors
        assert not any("custom_campaign_state.frozen_plans" in w for w in warnings), warnings

    def test_narrative_response_applies_overlay_sanitization(self):
        updates = {
            "made_up_key": 123,
            "player_character_data": {
                "equipment": {"belt": {"name": "Belt"}, "mystery_slot": {"name": "Orb"}},
                "resources": {"gold": 50, "mana_crystals": 9},
            },
        }
        response = NarrativeResponse(narrative="ok", state_updates=updates)

        assert response.state_updates.get("made_up_key") == 123
        player_data = response.state_updates.get("player_character_data", {})
        assert "mystery_slot" in player_data.get("equipment", {})
        assert "mana_crystals" in player_data.get("resources", {})

        gate_errors = response.debug_info.get("_state_update_schema_gate_errors", [])
        assert gate_errors, "Expected state-update schema gate errors in debug_info"


class TestNonBlockingValidationBehavior:
    """
    Test the non-blocking validation behavior.

    Schema validation is non-blocking by design across ALL persistence paths:
    - Generates logging_util.warning() to GCP logs
    - Appends to corrections list (if return_corrections=True)
    - Does NOT raise exceptions
    - Does NOT block persistence to Firestore

    This test verifies the cleanup path behavior (and all other paths) when
    schema validation fails - they should log warnings but not raise.
    """

    def test_validate_and_correct_state_never_raises_on_invalid_state(self):
        """
        Verify validate_and_correct_state never raises exceptions on invalid state.

        This documents the non-blocking behavior used by cleanup path and all
        other persistence paths in world_logic.py.
        """
        # Completely invalid state - missing required fields
        invalid_state = {
            "completely": "invalid",
            "not_a": "valid_game_state",
        }

        # Should NOT raise - should return with corrections
        result_state, corrections = validate_and_correct_state(
            invalid_state, return_corrections=True
        )

        # Verify we get back a state (possibly with migrations applied)
        assert isinstance(result_state, dict)
        # Verify corrections contain validation errors
        assert len(corrections) > 0
        assert any("Schema validation" in c for c in corrections)

    def test_cleanup_path_validates_non_blocking_behavior(self):
        """
        Verify cleanup path behavior when encountering invalid state.

        The cleanup path uses validate_and_correct_state() which is non-blocking.
        This test documents that invalid states are NOT rejected - they are
        persisted with correction warnings.

        This is intentional: validation provides observability (logs, corrections)
        but does NOT provide enforcement (no exceptions, invalid states persist).
        """
        # State that will fail schema validation (no required fields)
        invalid_state = {"garbage": True}

        # Simulate what cleanup path does
        try:
            result_state, corrections = validate_and_correct_state(
                invalid_state, return_corrections=True
            )
            # Non-blocking: should reach here, not raise
            non_blocking_behavior = True
        except ValueError:
            # This should NOT happen (strict enforcement would raise here)
            non_blocking_behavior = False

        assert non_blocking_behavior, (
            "validate_and_correct_state should NOT raise ValueError - "
            "it should be non-blocking (warnings only)"
        )

    def test_schema_validation_errors_appear_in_corrections(self):
        """
        Verify schema validation errors are captured in corrections list.

        This is the primary mechanism for observability - errors appear
        in corrections rather than raising exceptions.
        """
        # Invalid: completely invalid state (missing required fields like session_id)
        invalid_state = {
            "garbage": True,
            "not_valid": "state"
        }

        result_state, corrections = validate_and_correct_state(
            invalid_state, return_corrections=True
        )

        # Should have schema validation errors in corrections
        schema_errors = [c for c in corrections if "Schema validation" in c]
        assert len(schema_errors) > 0, (
            "Schema validation errors should appear in corrections list "
            f"for visibility without raising exceptions. Got corrections: {corrections}"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

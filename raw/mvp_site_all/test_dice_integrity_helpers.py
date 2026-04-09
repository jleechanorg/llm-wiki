import logging
from unittest.mock import Mock

from mvp_site import constants, dice_integrity
from mvp_site.narrative_response_schema import NarrativeResponse


def test_add_missing_dice_fields_requires_dice_rolls():
    missing: list[str] = []
    dice_integrity.add_missing_dice_fields(
        missing,
        structured_response=None,
        require_dice_rolls=True,
        dice_integrity_violation=False,
    )
    assert "dice_rolls" in missing
    assert "dice_integrity" not in missing


def test_add_missing_dice_fields_integrity_violation():
    missing: list[str] = []
    dice_integrity.add_missing_dice_fields(
        missing,
        structured_response=None,
        require_dice_rolls=False,
        dice_integrity_violation=True,
    )
    assert "dice_integrity" in missing


def test_add_missing_dice_fields_accepts_action_resolution_rolls():
    missing: list[str] = []
    resp = NarrativeResponse(
        narrative="n",
        action_resolution={"mechanics": {"rolls": [{"notation": "1d20", "total": 7}]}},
    )
    dice_integrity.add_missing_dice_fields(
        missing,
        structured_response=resp,
        require_dice_rolls=True,
        dice_integrity_violation=False,
    )
    assert "dice_rolls" not in missing


def test_no_reprompt_function_exists():
    """TDD: Ensure no reprompt logic exists - dice violations only warn, never retry LLM."""
    # The build_dice_integrity_reprompt_lines function was intentionally deleted.
    # Dice integrity violations should only log warnings, NOT trigger reprompts.
    assert not hasattr(dice_integrity, "build_dice_integrity_reprompt_lines"), (
        "Reprompt function should not exist - dice violations only warn, never retry"
    )


def test_has_dice_tool_results_rejects_error_responses():
    """Tool errors should NOT count as valid dice results."""
    # Tool call returned an error (e.g., missing dc_reasoning)
    tool_results = [
        {
            "tool": "roll_skill_check",
            "result": {
                "error": "dc_reasoning is required and must be a non-empty string"
            },
        }
    ]
    assert dice_integrity._has_dice_tool_results(tool_results) is False


def test_has_dice_tool_results_accepts_valid_results():
    """Valid dice results should be accepted."""
    tool_results = [
        {
            "tool": "roll_skill_check",
            "result": {
                "roll": 15,
                "total": 18,
                "formatted": "[DC 15: guard is alert] Perception: 1d20+3 = 18 vs DC 15 (Success)",
                "success": True,
            },
        }
    ]
    assert dice_integrity._has_dice_tool_results(tool_results) is True


def test_apply_tool_results_populates_action_resolution_rolls_skill_check():
    """Tool results should populate action_resolution.mechanics.rolls with totals."""
    resp = NarrativeResponse(
        narrative="n",
        action_resolution={"mechanics": {}},
    )
    tool_results = [
        {
            "tool": "roll_skill_check",
            "args": {
                "skill_name": "stealth",
                "attribute_modifier": 0,
                "proficiency_bonus": 0,
                "dc": 12,
                "dc_reasoning": "Alert guards",
            },
            "result": {
                "skill": "stealth",
                "roll": 5,
                "modifier": 0,
                "total": 5,
                "dc": 12,
                "dc_reasoning": "Alert guards",
                "success": False,
                "notation": "1d20+0",
            },
        }
    ]

    applied = dice_integrity._apply_tool_results_to_structured_response(
        resp,
        tool_results,
        dice_integrity.dice_strategy.DICE_STRATEGY_NATIVE_TWO_PHASE,
    )

    assert applied is True
    mechanics = resp.action_resolution.get("mechanics", {})
    rolls = mechanics.get("rolls", [])
    assert len(rolls) == 1
    roll = rolls[0]
    assert roll.get("total") == 5
    assert roll.get("dc") == 12
    assert roll.get("success") is False


def test_validate_god_mode_action_resolution_non_dict_is_ignored():
    """Non-dict action_resolution should not trigger god mode warnings."""
    resp = NarrativeResponse(
        narrative="",
        session_header="test",
        god_mode_response="HP set to 50",
        state_updates={},
        requires_action_resolution=False,
    )
    resp.action_resolution = "invalid"

    warnings = dice_integrity.validate_god_mode_response(resp, is_god_mode=True)
    assert warnings == []


def test_apply_tool_results_populates_action_resolution_rolls_attack_and_damage():
    """Attack tool results should expand to attack + damage rolls."""
    resp = NarrativeResponse(
        narrative="n",
        action_resolution={"mechanics": {}},
    )
    tool_results = [
        {
            "tool": "roll_attack",
            "args": {
                "attack_modifier": 5,
                "target_ac": 13,
                "damage_notation": "1d8+3",
                "purpose": "Longsword Attack vs Goblin",
            },
            "result": {
                "attack_roll": {
                    "rolls": [17],
                    "total": 22,
                    "modifier": 5,
                    "notation": "1d20+5",
                },
                "target_ac": 13,
                "hit": True,
                "damage": {
                    "notation": "1d8+3",
                    "rolls": [6],
                    "modifier": 3,
                    "total": 9,
                },
            },
        }
    ]

    applied = dice_integrity._apply_tool_results_to_structured_response(
        resp,
        tool_results,
        dice_integrity.dice_strategy.DICE_STRATEGY_NATIVE_TWO_PHASE,
    )

    assert applied is True
    mechanics = resp.action_resolution.get("mechanics", {})
    rolls = mechanics.get("rolls", [])
    assert len(rolls) == 2
    assert rolls[0].get("total") == 22
    assert rolls[0].get("dc") == 13
    assert rolls[0].get("success") is True
    assert rolls[1].get("notation") == "1d8+3"


def test_apply_tool_results_preserves_target_ac_zero():
    """TDD: target_ac=0 must be preserved, not treated as falsy."""
    resp = NarrativeResponse(
        narrative="n",
        action_resolution={"mechanics": {}},
    )
    tool_results = [
        {
            "tool": "roll_attack",
            "args": {
                "attack_modifier": 5,
                "target_ac": 10,  # Fallback value in args
                "damage_notation": "1d8+3",
                "purpose": "Attack vs Ooze",
            },
            "result": {
                "attack_roll": {
                    "rolls": [15],
                    "total": 20,
                    "modifier": 5,
                    "notation": "1d20+5",
                },
                "target_ac": 0,  # Edge case: AC 0 is valid (e.g., helpless target)
                "hit": True,
                "damage": {
                    "notation": "1d8+3",
                    "rolls": [4],
                    "modifier": 3,
                    "total": 7,
                },
            },
        }
    ]

    applied = dice_integrity._apply_tool_results_to_structured_response(
        resp,
        tool_results,
        dice_integrity.dice_strategy.DICE_STRATEGY_NATIVE_TWO_PHASE,
    )

    assert applied is True
    mechanics = resp.action_resolution.get("mechanics", {})
    rolls = mechanics.get("rolls", [])
    assert len(rolls) == 2
    # CRITICAL: target_ac=0 from result must be used, NOT fallback to args.target_ac=10
    assert rolls[0].get("dc") == 0, (
        f"target_ac=0 must be preserved, got {rolls[0].get('dc')}"
    )


def test_has_dice_tool_errors_detects_errors():
    """Should detect and extract tool error messages."""
    tool_results = [
        {"tool": "roll_skill_check", "result": {"error": "dc_reasoning is required"}},
        {"tool": "roll_saving_throw", "result": {"error": "dc_reasoning is required"}},
    ]
    has_errors, errors = dice_integrity._has_dice_tool_errors(tool_results)
    assert has_errors is True
    assert len(errors) == 2
    assert "roll_skill_check: dc_reasoning is required" in errors


def test_has_dice_tool_errors_no_errors():
    """Should return False when no errors."""
    tool_results = [
        {
            "tool": "roll_skill_check",
            "result": {"roll": 15, "total": 18, "success": True},
        }
    ]
    has_errors, errors = dice_integrity._has_dice_tool_errors(tool_results)
    assert has_errors is False
    assert errors == []


def test_detect_narrative_dice_fabrication_with_action_resolution_rolls(caplog):
    structured_response = NarrativeResponse(
        narrative="A quiet moment.",
        action_resolution={"mechanics": {"rolls": [{"notation": "1d20", "total": 12}]}},
    )

    with caplog.at_level(logging.WARNING):
        is_fabricated = dice_integrity._detect_narrative_dice_fabrication(
            narrative_text="",
            structured_response=structured_response,
            api_response=None,
            code_execution_evidence=None,
        )

    assert is_fabricated is True
    assert "SCHEMA_VIOLATION" not in caplog.text


def test_detect_narrative_dice_fabrication_with_action_resolution_audit_events(
    caplog,
):
    """audit_events-only triggers SCHEMA_VIOLATION warning (rolls are required)."""
    structured_response = NarrativeResponse(
        narrative="A quiet moment.",
        action_resolution={
            "mechanics": {
                "audit_events": [
                    {
                        "source": "code_execution",
                        "label": "Stealth check",
                        "notation": "1d20+2",
                        "rolls": [14],
                        "modifier": 2,
                        "total": 16,
                    }
                ]
            }
        },
    )

    with caplog.at_level(logging.WARNING):
        is_fabricated = dice_integrity._detect_narrative_dice_fabrication(
            narrative_text="",
            structured_response=structured_response,
            api_response=None,
            code_execution_evidence=None,
        )

    assert is_fabricated is True
    # audit_events without rolls is a schema violation per prompts
    assert "SCHEMA_VIOLATION" in caplog.text
    assert "audit_events" in caplog.text
    assert "NO rolls" in caplog.text


def test_detect_narrative_dice_fabrication_with_action_resolution_only(caplog):
    """Only action_resolution.mechanics.rolls is checked for dice detection."""
    structured_response = NarrativeResponse(
        narrative="A quiet moment.",
        action_resolution={"mechanics": {"rolls": [{"notation": "1d20", "total": 18}]}},
    )

    with caplog.at_level(logging.WARNING):
        is_fabricated = dice_integrity._detect_narrative_dice_fabrication(
            narrative_text="",
            structured_response=structured_response,
            api_response=None,
            code_execution_evidence=None,
        )

    assert is_fabricated is True


# =============================================================================
# Tests for _validate_dice_integrity_always
# =============================================================================


def test_validate_dice_integrity_always_no_dice():
    """No dice_rolls should always be valid."""
    resp = NarrativeResponse(narrative="You absorb the orb.", dice_rolls=[])
    api_response = Mock()
    api_response._tool_requests_executed = False

    is_valid, reason = dice_integrity._validate_dice_integrity_always(
        structured_response=resp,
        api_response=api_response,
        mode=constants.MODE_CHARACTER,
        is_god_mode=False,
        is_dm_mode=False,
    )
    assert is_valid is True
    assert reason is None


def test_validate_dice_integrity_always_with_tools():
    """Dice_rolls with tool execution should be valid."""
    resp = NarrativeResponse(
        narrative="You roll an Arcana check.",
        dice_rolls=["[DC 15] Arcana: 1d20+5 = 20 (Success)"],
    )
    api_response = Mock()
    api_response._tool_requests_executed = True

    is_valid, reason = dice_integrity._validate_dice_integrity_always(
        structured_response=resp,
        api_response=api_response,
        mode=constants.MODE_CHARACTER,
        is_god_mode=False,
        is_dm_mode=False,
    )
    assert is_valid is True


def test_validate_dice_integrity_always_fabricated():
    """Dice_rolls without tool execution should be INVALID."""
    resp = NarrativeResponse(
        narrative="You roll an Arcana check.",
        action_resolution={
            "mechanics": {
                "rolls": [
                    {"notation": "1d20+5", "total": 20, "dc": 15, "success": True}
                ]
            }
        },
    )
    api_response = Mock()
    api_response._tool_requests_executed = False

    is_valid, reason = dice_integrity._validate_dice_integrity_always(
        structured_response=resp,
        api_response=api_response,
        mode=constants.MODE_CHARACTER,
        is_god_mode=False,
        is_dm_mode=False,
    )
    assert is_valid is False
    assert "DICE INTEGRITY VIOLATION" in reason


def test_validate_dice_integrity_always_god_mode_bypass():
    """God mode should bypass validation."""
    resp = NarrativeResponse(
        narrative="You absorb the orb.",
        dice_rolls=["[DC 15] Arcana: 1d20+5 = 20 (Success)"],  # Fabricated
    )
    api_response = Mock()
    api_response._tool_requests_executed = False

    is_valid, reason = dice_integrity._validate_dice_integrity_always(
        structured_response=resp,
        api_response=api_response,
        mode=constants.MODE_CHARACTER,
        is_god_mode=True,
        is_dm_mode=False,
    )
    assert is_valid is True  # Bypassed


def test_validate_dice_integrity_always_dm_mode_bypass():
    """DM mode should bypass validation."""
    resp = NarrativeResponse(
        narrative="You absorb the orb.",
        dice_rolls=["[DC 15] Arcana: 1d20+5 = 20 (Success)"],  # Fabricated
    )
    api_response = Mock()
    api_response._tool_requests_executed = False

    is_valid, reason = dice_integrity._validate_dice_integrity_always(
        structured_response=resp,
        api_response=api_response,
        mode=constants.MODE_CHARACTER,
        is_god_mode=False,
        is_dm_mode=True,
    )
    assert is_valid is True  # Bypassed


def test_validate_dice_integrity_always_code_execution_strategy_bypass():
    """Code execution strategy should bypass this check (has its own)."""
    resp = NarrativeResponse(
        narrative="You absorb the orb.",
        dice_rolls=[
            "[DC 15] Arcana: 1d20+5 = 20 (Success)"
        ],  # Would fail for two_phase
    )
    api_response = Mock()
    api_response._tool_requests_executed = False

    is_valid, reason = dice_integrity._validate_dice_integrity_always(
        structured_response=resp,
        api_response=api_response,
        mode=constants.MODE_CHARACTER,
        is_god_mode=False,
        is_dm_mode=False,
        dice_roll_strategy=dice_integrity.dice_strategy.DICE_STRATEGY_CODE_EXECUTION,
    )
    assert is_valid is True  # Bypassed for code_execution


def test_validate_dice_integrity_always_native_two_phase_checks():
    """Native two phase strategy should validate tool_requests."""
    resp = NarrativeResponse(
        narrative="You roll an Arcana check.",
        action_resolution={
            "mechanics": {
                "rolls": [
                    {"notation": "1d20+5", "total": 20, "dc": 15, "success": True}
                ]
            }
        },
    )
    api_response = Mock()
    api_response._tool_requests_executed = False

    is_valid, reason = dice_integrity._validate_dice_integrity_always(
        structured_response=resp,
        api_response=api_response,
        mode=constants.MODE_CHARACTER,
        is_god_mode=False,
        is_dm_mode=False,
        dice_roll_strategy=dice_integrity.dice_strategy.DICE_STRATEGY_NATIVE_TWO_PHASE,
    )
    assert is_valid is False  # Should fail for native_two_phase
    assert "DICE INTEGRITY VIOLATION" in reason


# =============================================================================
# Tests for _detect_narrative_dice_fabrication with action_resolution
# =============================================================================


def test_detect_fabrication_action_resolution_only():
    """Dice in action_resolution.mechanics.rolls should be detected."""
    resp = NarrativeResponse(
        narrative="You attack the goblin.",
        action_resolution={
            "mechanics": {
                "rolls": [{"notation": "1d20+5", "total": 18, "purpose": "Attack"}]
            }
        },
    )
    api_response = Mock()
    api_response._tool_requests_executed = False

    # Without code execution evidence, should detect fabrication
    result = dice_integrity._detect_narrative_dice_fabrication(
        narrative_text="",
        structured_response=resp,
        api_response=api_response,
        code_execution_evidence=None,
    )
    assert result is True  # Fabrication detected


def test_detect_fabrication_action_resolution_with_rng():
    """Dice in action_resolution WITH rng_verified should pass."""
    resp = NarrativeResponse(
        narrative="You attack the goblin.",
        action_resolution={
            "mechanics": {
                "rolls": [{"notation": "1d20+5", "total": 18, "purpose": "Attack"}]
            }
        },
    )
    api_response = Mock()
    api_response._tool_requests_executed = False
    code_evidence = {"code_execution_used": True, "rng_verified": True}

    result = dice_integrity._detect_narrative_dice_fabrication(
        narrative_text="",
        structured_response=resp,
        api_response=api_response,
        code_execution_evidence=code_evidence,
    )
    assert result is False  # Valid dice, no fabrication


def test_detect_fabrication_audit_events_only():
    """Dice in action_resolution.mechanics.audit_events should be detected."""
    resp = NarrativeResponse(
        narrative="",
        action_resolution={"mechanics": {"rolls": [], "audit_events": ["1d20+5 = 18"]}},
    )
    api_response = Mock()
    api_response._tool_requests_executed = False

    result = dice_integrity._detect_narrative_dice_fabrication(
        narrative_text="",
        structured_response=resp,
        api_response=api_response,
        code_execution_evidence=None,
    )
    assert result is True  # Fabrication detected


def test_detect_fabrication_legacy_dice_bypass_prevented():
    """Legacy dice_rolls bypass attack is prevented - fabrication detected."""
    # Attack scenario: LLM puts dice ONLY in legacy dice_rolls (not action_resolution)
    # to try bypassing _is_code_execution_fabrication which only checks action_resolution
    resp = NarrativeResponse(
        narrative="You rolled a 15.",
        dice_rolls=["Stealth: 1d20+5 = 15"],  # Legacy field only
        action_resolution={"mechanics": {"rolls": []}},  # Empty action_resolution
    )
    api_response = Mock()
    api_response._tool_requests_executed = False

    # Without code execution evidence, this MUST be detected as fabrication
    result = dice_integrity._detect_narrative_dice_fabrication(
        narrative_text="",
        structured_response=resp,
        api_response=api_response,
        code_execution_evidence=None,
    )
    assert result is True, "Legacy dice bypass attack must be detected as fabrication"


def test_detect_fabrication_no_dice_anywhere():
    """No dice anywhere should return False."""
    resp = NarrativeResponse(
        narrative="You walk down the hall.",
        action_resolution={"mechanics": {"rolls": []}},
    )
    api_response = Mock()
    api_response._tool_requests_executed = False

    result = dice_integrity._detect_narrative_dice_fabrication(
        narrative_text="",
        structured_response=resp,
        api_response=api_response,
        code_execution_evidence=None,
    )
    assert result is False  # No dice, no fabrication


# =============================================================================
# Tests for stdout roll vs rolls schema handling
# =============================================================================


def test_reconcile_handles_roll_singular_in_stdout():
    """Test stdout with 'roll' (singular) should be handled like 'rolls' (array).

    Bug scenario (from campaign mSEMkUw6vRh5jPtfS7p4):
    - stdout has {"roll": 20, "total": 28} (singular)
    - Should be treated same as {"rolls": [20], "total": 28} (array)
    """
    # dice_audit_events with wrong total in rolls
    dice_audit_events = [
        {
            "rolls": [28],  # WRONG - this is the total
            "notation": "1d20+8",
            "source": "code_execution",
            "total": 28,
            "modifier": 0,
            "label": "The All-Seeing Dove",
        }
    ]

    # stdout uses "roll" singular instead of "rolls" array
    debug_info = {
        "code_execution_used": True,
        "stdout": '{"action": "The All-Seeing Dove", "notation": "1d20+8", "roll": 20, "total": 28}',
    }

    corrected = dice_integrity.reconcile_dice_audit_events_with_stdout(
        dice_audit_events, debug_info
    )

    # Should correct rolls using the singular "roll" field
    assert len(corrected) == 1
    assert corrected[0]["rolls"] == [20], (
        f"Expected [20] but got {corrected[0]['rolls']}"
    )


def test_reconcile_handles_roll_singular_with_modifier():
    """Test stdout with 'roll' singular and modifier should extract raw roll."""
    dice_audit_events = [
        {
            "rolls": [24],  # WRONG - total, not raw roll
            "notation": "1d20+9",
            "source": "code_execution",
            "total": 24,
            "modifier": 0,
            "label": "Dove Infiltration",
        }
    ]

    # stdout uses "roll" singular with modifier
    debug_info = {
        "code_execution_used": True,
        "stdout": '{"purpose": "Dove Infiltration", "notation": "1d20+9", "roll": 15, "modifier": 9, "total": 24, "success": true}',
    }

    corrected = dice_integrity.reconcile_dice_audit_events_with_stdout(
        dice_audit_events, debug_info
    )

    assert corrected[0]["rolls"] == [15], (
        f"Expected [15] but got {corrected[0]['rolls']}"
    )
    assert corrected[0]["modifier"] == 9, (
        f"Expected modifier=9 but got {corrected[0]['modifier']}"
    )


def test_reconcile_prefers_rolls_array_over_roll_singular():
    """If both 'roll' and 'rolls' exist, prefer 'rolls' array."""
    dice_audit_events = [
        {
            "rolls": [25],  # WRONG
            "notation": "1d20+5",
            "source": "code_execution",
            "total": 25,
            "modifier": 0,
            "label": "Attack",
        }
    ]

    # stdout has both roll and rolls (edge case)
    debug_info = {
        "code_execution_used": True,
        "stdout": '{"notation": "1d20+5", "roll": 19, "rolls": [20], "modifier": 5, "total": 25}',
    }

    corrected = dice_integrity.reconcile_dice_audit_events_with_stdout(
        dice_audit_events, debug_info
    )

    # Should prefer rolls array
    assert corrected[0]["rolls"] == [20], (
        f"Expected [20] but got {corrected[0]['rolls']}"
    )


def test_reconcile_handles_empty_rolls_with_roll_singular():
    """If dice_audit_events has empty rolls, should populate from roll singular."""
    dice_audit_events = [
        {
            "rolls": [],  # Empty - common when LLM doesn't populate
            "notation": "1d20+6",
            "source": "code_execution",
            "total": 23,
            "modifier": 0,
            "label": "Skill Check",
        }
    ]

    debug_info = {
        "code_execution_used": True,
        "stdout": '{"notation": "1d20+6", "roll": 17, "modifier": 6, "total": 23}',
    }

    corrected = dice_integrity.reconcile_dice_audit_events_with_stdout(
        dice_audit_events, debug_info
    )

    assert corrected[0]["rolls"] == [17], (
        f"Expected [17] but got {corrected[0]['rolls']}"
    )
    assert corrected[0]["modifier"] == 6


# =============================================================================
# Tests for collision handling (multiple events with same key)
# =============================================================================


def test_reconcile_multiple_audit_events_with_same_key_no_double_consumption():
    """Test that multiple audit events with same key don't consume the same stdout event twice.

    Scenario: Two audit events for "Attack" rolls, two stdout events.
    Each audit event should match a different stdout event (one-to-one).
    """
    dice_audit_events = [
        {
            "rolls": [25],  # WRONG
            "notation": "1d20+5",
            "source": "code_execution",
            "total": 25,
            "label": "Attack",
        },
        {
            "rolls": [22],  # WRONG
            "notation": "1d20+5",
            "source": "code_execution",
            "total": 22,
            "label": "Attack",
        },
    ]

    # Two stdout events with same label/notation (as JSON array)
    debug_info = {
        "code_execution_used": True,
        "stdout": '[{"action": "Attack", "notation": "1d20+5", "roll": 18, "modifier": 5, "total": 23}, {"action": "Attack", "notation": "1d20+5", "roll": 12, "modifier": 5, "total": 17}]',
    }

    corrected = dice_integrity.reconcile_dice_audit_events_with_stdout(
        dice_audit_events, debug_info
    )

    assert len(corrected) == 2
    # First audit event gets first stdout event
    assert corrected[0]["rolls"] == [18], (
        f"Expected [18] but got {corrected[0]['rolls']}"
    )
    # Second audit event gets second stdout event (not the same as first)
    assert corrected[1]["rolls"] == [12], (
        f"Expected [12] but got {corrected[1]['rolls']}"
    )


def test_reconcile_prevents_double_consumption_via_fallback():
    """Test that an event matched via primary key isn't consumed again via fallback.

    Bug scenario: Event has both label/notation AND total.
    - First audit event matches via (label, notation) key
    - Second audit event tries to match via fallback (total) key
    - Should NOT return the same already-consumed event
    """
    dice_audit_events = [
        {
            "rolls": [25],
            "notation": "1d20+5",
            "source": "code_execution",
            "total": 23,  # Same total as stdout
            "label": "Attack",
        },
        {
            "rolls": [25],
            "notation": "1d20+2",  # Different notation, no stdout match
            "source": "code_execution",
            "total": 23,  # Same total - would match fallback if not consumed
            "label": "Defense",  # Different label, no stdout match
        },
    ]

    # Single stdout event - matches first audit event via (label, notation)
    debug_info = {
        "code_execution_used": True,
        "stdout": '{"action": "Attack", "notation": "1d20+5", "roll": 18, "modifier": 5, "total": 23}',
    }

    corrected = dice_integrity.reconcile_dice_audit_events_with_stdout(
        dice_audit_events, debug_info
    )

    assert len(corrected) == 2
    # First audit event gets the stdout event via primary key
    assert corrected[0]["rolls"] == [18]
    # Second audit event should NOT get the same event via fallback (already consumed)
    assert corrected[1]["rolls"] == [25], (
        "Second event should keep original rolls (no match)"
    )


def test_reconcile_handles_ndjson_stdout():
    """Test that newline-delimited JSON (NDJSON) is parsed correctly.

    This occurs when stdout_parts are joined with newlines, creating
    valid JSON per-line but invalid as a single JSON string.
    """
    dice_audit_events = [
        {
            "rolls": [25],
            "notation": "1d20+5",
            "source": "code_execution",
            "total": 23,
            "label": "Attack",
        },
        {
            "rolls": [15],
            "notation": "1d6+3",
            "source": "code_execution",
            "total": 9,
            "label": "Damage",
        },
    ]

    # NDJSON: two JSON objects separated by newline (not a valid single JSON)
    debug_info = {
        "code_execution_used": True,
        "stdout": '{"action": "Attack", "notation": "1d20+5", "roll": 18, "modifier": 5, "total": 23}\n{"action": "Damage", "notation": "1d6+3", "roll": 6, "modifier": 3, "total": 9}',
    }

    corrected = dice_integrity.reconcile_dice_audit_events_with_stdout(
        dice_audit_events, debug_info
    )

    assert len(corrected) == 2
    assert corrected[0]["rolls"] == [18], (
        f"Expected [18] but got {corrected[0]['rolls']}"
    )
    assert corrected[1]["rolls"] == [6], f"Expected [6] but got {corrected[1]['rolls']}"


def test_reconcile_total_fallback_requires_unambiguous_match():
    """Test that total fallback only works when exactly one stdout event has that total.

    When multiple stdout events share the same total, fallback matching is
    ambiguous and should not be used (to avoid mis-reconciliation).
    """
    dice_audit_events = [
        {
            "rolls": [25],
            "notation": "1d20+5",
            "source": "code_execution",
            "total": 15,  # Matches both stdout events' totals
            "label": "Unknown Action",  # No label match in stdout
        },
    ]

    # Two stdout events with SAME total but different rolls
    debug_info = {
        "code_execution_used": True,
        "stdout": '[{"action": "Attack", "notation": "1d20+5", "roll": 10, "modifier": 5, "total": 15}, {"action": "Damage", "notation": "2d6+3", "rolls": [5, 4], "modifier": 3, "total": 15}]',
    }

    corrected = dice_integrity.reconcile_dice_audit_events_with_stdout(
        dice_audit_events, debug_info
    )

    # Should NOT match either stdout event (ambiguous total)
    assert corrected[0]["rolls"] == [25], (
        "Ambiguous total should not trigger fallback match"
    )


def test_reconcile_total_fallback_works_when_unambiguous():
    """Test that total fallback works when only one stdout event has that total."""
    dice_audit_events = [
        {
            "rolls": [25],
            "notation": "1d20+5",
            "source": "code_execution",
            "total": 23,  # Only one stdout event has this total
            "label": "Unknown Action",  # No label match in stdout
        },
    ]

    # Two stdout events with DIFFERENT totals
    debug_info = {
        "code_execution_used": True,
        "stdout": '[{"action": "Attack", "notation": "1d20+5", "roll": 18, "modifier": 5, "total": 23}, {"action": "Damage", "notation": "1d6+3", "roll": 6, "modifier": 3, "total": 9}]',
    }

    corrected = dice_integrity.reconcile_dice_audit_events_with_stdout(
        dice_audit_events, debug_info
    )

    # Should match via unambiguous total fallback
    assert corrected[0]["rolls"] == [18], (
        f"Unambiguous total should trigger fallback match, got {corrected[0]['rolls']}"
    )


# =============================================================================
# TDD: Prompt must explicitly instruct LLM to use "rolls" array, not "roll" singular
# =============================================================================


def test_prompt_contains_explicit_rolls_array_instruction():
    """TDD: narrative_system_instruction.md must explicitly instruct LLM to always use 'rolls' array.

    This prevents LLM schema variance where model emits {"roll": 15} instead of {"rolls": [15]}.
    Having a single explicit instruction reduces variance and simplifies downstream parsing.
    """
    import os

    prompt_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "prompts",
        "narrative_system_instruction.md",
    )

    with open(prompt_path) as f:
        content = f.read()

    # Must contain explicit instruction about rolls array format
    assert "ALWAYS use `rolls` (plural, array)" in content, (
        "Prompt must contain explicit instruction: 'ALWAYS use `rolls` (plural, array)'"
    )

    # Must warn against using roll singular
    assert '"roll": 15' in content or "'roll': 15" in content, (
        "Prompt must show forbidden pattern with 'roll' singular"
    )

    # Must show correct pattern with rolls array
    assert '"rolls": [' in content, (
        "Prompt must show correct pattern with 'rolls' array"
    )


def test_prompt_explains_rolls_vs_total_difference():
    """TDD: Prompt must clarify that rolls contains raw die values, not totals.

    Bug scenario: LLM emits {"rolls": [20], "total": 20} when the raw roll was 15
    and modifier was 5. The prompt must explain that rolls = raw die values BEFORE modifiers.
    """
    import os

    prompt_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "prompts",
        "narrative_system_instruction.md",
    )

    with open(prompt_path) as f:
        content = f.read()

    # Must explain rolls contains raw die results before modifiers
    assert "BEFORE adding modifier" in content or "before adding modifier" in content, (
        "Prompt must explain that 'rolls' contains raw die values BEFORE modifiers"
    )

    # Must show the total calculation formula
    assert "total" in content.lower() and "modifier" in content.lower(), (
        "Prompt must explain total = rolls + modifier relationship"
    )


def test_prompt_has_skill_check_phase2_example():
    """TDD: game_state_instruction.md must show Phase 2 example for skill checks.

    Bug scenario: LLM correctly emits tool_requests for skill checks in Phase 1,
    but doesn't populate action_resolution.mechanics.rolls in Phase 2 because
    the prompt only shows combat (roll_attack) examples, not skill check examples.

    The fix: Add explicit skill check Phase 2 example showing how to populate
    action_resolution.mechanics.rolls with skill check results.
    """
    import os

    prompt_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "prompts",
        "game_state_instruction.md",
    )

    with open(prompt_path) as f:
        content = f.read()

    # Must have explicit "Skill Check Example" header in Phase 1/Phase 2 context
    assert "Skill Check Example" in content, (
        "Prompt must contain 'Skill Check Example' header in Phase 1/Phase 2 section"
    )

    # Must explain skill checks follow SAME flow as combat
    assert "Skill checks MUST follow the same Phase 1/Phase 2 flow" in content, (
        "Prompt must explicitly state skill checks follow same Phase 1/Phase 2 flow"
    )

    # Must show skill check Phase 2 with action_resolution.mechanics.rolls populated
    assert '"type": "skill_check"' in content or '"type":"skill_check"' in content, (
        "Prompt must show Phase 2 skill check with type: skill_check in action_resolution"
    )


def test_prompt_documents_canonical_action_resolution_roll_required_fields():
    """REV-m7z: game_state_instruction must document canonical roll required fields.

    action_resolution.mechanics.rolls items are schema-validated. The prompt must
    explicitly state the canonical required fields to keep model outputs aligned:
    notation (string), result (integer), success (boolean).
    """
    import os

    prompt_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "prompts",
        "game_state_instruction.md",
    )

    with open(prompt_path) as f:
        content = f.read()

    assert "Canonical REQUIRED fields per roll item" in content, (
        "Prompt must explicitly call out canonical required fields for action_resolution rolls"
    )
    assert "`notation` (string)" in content, (
        "Prompt must require notation (string) in canonical action_resolution rolls"
    )
    assert "`result` (integer)" in content, (
        "Prompt must require result (integer) in canonical action_resolution rolls"
    )
    assert "`success` (boolean)" in content, (
        "Prompt must require success (boolean) in canonical action_resolution rolls"
    )

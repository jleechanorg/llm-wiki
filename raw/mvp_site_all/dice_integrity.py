from __future__ import annotations

import json
import os
import re
from typing import Any

from mvp_site import constants, dice, dice_strategy, logging_util
from mvp_site.action_resolution_utils import has_action_resolution_dice
from mvp_site.game_state import GameState, format_tool_results_text
from mvp_site.narrative_response_schema import NarrativeResponse
from mvp_site.numeric_converters import coerce_int_safe as _coerce_int

DICE_ROLL_PATTERN = re.compile(
    r"\b\d*d\d+(?:\s*[+\-]\s*\d+)?\b|\brolls?\s+(?:a\s+)?\d+\b",
    re.IGNORECASE,
)
_NARRATIVE_DICE_NOTATION_PATTERN = re.compile(
    r"\b\d*d\d+(?:\s*[+\-]\s*\d+)?\b", re.IGNORECASE
)
_NARRATIVE_DICE_TAG_PATTERN = re.compile(r"\[dice:[^\]]+\]", re.IGNORECASE)
_NARRATIVE_DICE_ROLL_RESULT_PATTERN = re.compile(
    r"\brolls?\s+(?:a\s+)?\d+\b", re.IGNORECASE
)
_NARRATIVE_DICE_CONTEXT_PATTERN = re.compile(
    r"\b(attack|hit|damage|save|saving throw|skill|check|initiative|ac|dc)\b",
    re.IGNORECASE,
)
_NARRATIVE_DICE_SCAN_MAX_CHARS = 5000


def _narrative_contains_dice(text: str) -> bool:
    if not text:
        return False
    if len(text) > _NARRATIVE_DICE_SCAN_MAX_CHARS:
        text = text[:_NARRATIVE_DICE_SCAN_MAX_CHARS]

    if _NARRATIVE_DICE_TAG_PATTERN.search(text):
        return True
    if _NARRATIVE_DICE_NOTATION_PATTERN.search(text):
        return True

    # "rolls a 15" is only treated as dice if nearby context suggests a check/attack
    for match in _NARRATIVE_DICE_ROLL_RESULT_PATTERN.finditer(text):
        start = max(0, match.start() - 80)
        end = min(len(text), match.end() + 80)
        window = text[start:end]
        if _NARRATIVE_DICE_CONTEXT_PATTERN.search(window):
            return True

    return False


def _detect_narrative_dice_fabrication(  # noqa: PLR0911, PLR0912
    *,
    narrative_text: str,
    structured_response: NarrativeResponse | None,
    api_response: Any,
    code_execution_evidence: dict[str, Any] | None,
    dice_roll_strategy: str | None = None,
) -> bool:
    """Detect dice patterns in narrative OR structured response that lack tool/code_execution evidence.

    PRIMARY SOURCE: action_resolution.mechanics.rolls (centralized per PR #4084)

    Args:
        dice_roll_strategy: The dice strategy in use. When NATIVE_TWO_PHASE, certain warnings
            are suppressed because dice come from server-executed tool calls, not code_execution.
    """
    has_dice_in_narrative = narrative_text and _narrative_contains_dice(narrative_text)

    has_dice_in_structured = False
    has_legacy_dice = False

    if structured_response:
        # PRIMARY CHECK: action_resolution.mechanics.rolls/audit_events (ONLY valid source for LLM)
        action_resolution = getattr(structured_response, "action_resolution", None)
        if isinstance(action_resolution, dict):
            mechanics = action_resolution.get("mechanics", {})
            if isinstance(mechanics, dict):
                rolls = mechanics.get("rolls", [])
                audit_events = mechanics.get("audit_events", [])
            else:
                rolls = []
                audit_events = []

            if has_action_resolution_dice(action_resolution):
                has_dice_in_structured = True

                # SCHEMA VIOLATION: audit_events without rolls
                # Per prompts, rolls are REQUIRED for dice; audit_events are supplemental
                rolls_list = rolls if isinstance(rolls, list) else []
                audit_list = audit_events if isinstance(audit_events, list) else []
                if len(audit_list) > 0 and len(rolls_list) == 0:
                    logging_util.warning(
                        logging_util.with_campaign(
                            f"⚠️ SCHEMA_VIOLATION: action_resolution.mechanics has audit_events "
                            f"({len(audit_list)}) but NO rolls. Per prompts, all dice must go in "
                            f"action_resolution.mechanics.rolls - audit_events are supplemental. "
                            f"UI will not display these dice."
                        )
                    )

                # WARN: If dice in action_resolution but no code execution evidence
                # Only warn for CODE_EXECUTION strategy - NATIVE_TWO_PHASE uses server-executed
                # tool calls which don't set code_execution_used flag (that's expected behavior)
                is_code_execution_strategy = (
                    dice_roll_strategy == dice_strategy.DICE_STRATEGY_CODE_EXECUTION
                )
                if is_code_execution_strategy and (
                    code_execution_evidence is None
                    or not code_execution_evidence.get("code_execution_used")
                ):
                    logging_util.warning(
                        logging_util.with_campaign(
                            f"⚠️ ACTION_RESOLUTION_DICE_NO_CODE_EXECUTION: "
                            f"action_resolution.mechanics has dice (rolls={len(rolls_list)}, "
                            f"audit_events={len(audit_list)}) "
                            f"but code_execution_used={code_execution_evidence.get('code_execution_used') if code_execution_evidence else 'None'}. "
                            f"Dice should come from code_execution with random.randint()."
                        )
                    )

        # SCHEMA VIOLATION CHECK: Legacy dice_rolls/dice_audit_events should not be LLM-populated
        # The LLM should ONLY use action_resolution.mechanics - legacy fields are for server backfill
        legacy_dice_rolls = getattr(structured_response, "dice_rolls", None) or []
        legacy_audit_events = (
            getattr(structured_response, "dice_audit_events", None) or []
        )
        if legacy_dice_rolls or legacy_audit_events:
            has_legacy_dice = True
            has_dice_in_structured = True  # Include in integrity validation
            logging_util.warning(
                logging_util.with_campaign(
                    f"⚠️ SCHEMA_VIOLATION: LLM populated legacy dice fields "
                    f"(dice_rolls={len(legacy_dice_rolls)}, dice_audit_events={len(legacy_audit_events)}). "
                    f"LLM should use action_resolution.mechanics.rolls ONLY. "
                    f"Legacy fields are for server backfill, not LLM output."
                )
            )

    dice.log_narrative_dice_detected(bool(has_dice_in_narrative))

    dice.log_dice_fabrication_check(
        has_dice_in_narrative=bool(has_dice_in_narrative),
        has_dice_in_structured=has_dice_in_structured,
        code_execution_used=(
            code_execution_evidence.get("code_execution_used")
            if code_execution_evidence
            else "N/A"
        ),
        tool_requests_executed=getattr(api_response, "_tool_requests_executed", "N/A"),
        debug_enabled=os.getenv("DICE_INTEGRITY_DEBUG", "").lower() == "true",
    )

    # If no dice anywhere, no fabrication possible
    if not has_dice_in_narrative and not has_dice_in_structured:
        return False

    # GREEN FIX (Dec 2024): Use rng_verified instead of code_execution_used
    # This detects fabrication via print('{"rolls": [16]}') without random.randint()
    if code_execution_evidence:
        rng_verified = code_execution_evidence.get("rng_verified", False)
        if rng_verified:
            return False  # Dice came from actual RNG, not fabrication
        # At this point rng_verified=False, check if code was executed without RNG
        code_execution_used = code_execution_evidence.get("code_execution_used", False)
        if code_execution_used:
            dice.log_code_exec_fabrication_violation()
            # This is fabrication - code ran but didn't use RNG
            return True

    # CRITICAL FIX: Don't blindly trust tool_requests_executed flag
    # Verify that tool_results actually contain dice data (non-empty, valid results)
    tool_requests_executed = getattr(api_response, "_tool_requests_executed", None)
    tool_results = getattr(api_response, "_tool_results", None)

    dice.log_tool_results_inspection(
        tool_results=tool_results,
        debug_enabled=os.getenv("DICE_INTEGRITY_DEBUG", "").lower() == "true",
    )

    # ENHANCED: Only accept dice-specific tool results (prevents non-dice tool loophole)
    if tool_requests_executed and tool_results:
        # Verify tool_results contain dice tools specifically
        # This prevents accepting non-dice tools (e.g., search_location) as proof
        if _has_dice_tool_results(tool_results):
            return False  # Dice tool results valid, dice are real

        # Check if dice tools were called but returned errors (e.g., missing dc_reasoning)
        # This is NOT fabrication - the LLM tried to use tools correctly but failed validation
        has_tool_errors, tool_errors = _has_dice_tool_errors(tool_results)
        if has_tool_errors:
            logging_util.warning(
                logging_util.with_campaign(
                    f"🎲 DICE_TOOL_ERROR: Dice tools called but returned errors: {tool_errors}. "
                    "This is a tool validation failure, not fabrication. Flagged for user warning."
                )
            )
            # Return True to flag as integrity violation for user warning
            return True

        # If we get here, tool_requests_executed=True but tool_results lack dice tools
        # This is suspicious - LLM may have called a non-dice tool and fabricated dice
        # Fall through to fabrication check

    # If we found dice but no tool/code_execution evidence, that's FABRICATION
    if has_dice_in_narrative or has_dice_in_structured:
        dice.log_dice_fabrication_detected(
            has_dice_in_narrative=bool(has_dice_in_narrative),
            has_dice_in_structured=has_dice_in_structured,
        )
        return True

    # Backward compatibility: if metadata is missing and no dice detected, be permissive
    if tool_requests_executed is None and code_execution_evidence is None:
        return False

    # If we got here, something unexpected happened
    return False


def add_missing_dice_fields(
    missing: list[str],
    *,
    structured_response: NarrativeResponse | None,
    require_dice_rolls: bool,
    dice_integrity_violation: bool,
) -> None:
    """Append missing dice fields based on current enforcement policy."""
    if require_dice_rolls:
        has_valid_dice = False
        action_resolution = getattr(structured_response, "action_resolution", None)
        if isinstance(action_resolution, dict):
            mechanics = action_resolution.get("mechanics", {})
            if isinstance(mechanics, dict):
                rolls = mechanics.get("rolls", [])
                audit_events = mechanics.get("audit_events", [])
                has_valid_dice = (isinstance(rolls, list) and len(rolls) > 0) or (
                    isinstance(audit_events, list) and len(audit_events) > 0
                )
        if not has_valid_dice:
            missing.append("dice_rolls")

    if dice_integrity_violation:
        missing.append("dice_integrity")


def build_dice_processing_metadata(
    *,
    api_response: Any,
    dice_roll_strategy: str,
    capture_tools: bool = True,
) -> dict[str, Any]:
    """Build dice-specific processing metadata for downstream auditing."""
    metadata: dict[str, Any] = {"dice_strategy": dice_roll_strategy}
    if not capture_tools:
        return metadata

    tool_results = getattr(api_response, "_tool_results", None)
    if tool_results is not None:
        metadata["tool_results"] = tool_results
        metadata["tool_requests_executed"] = bool(
            getattr(api_response, "_tool_requests_executed", False)
        )
    return metadata


def apply_dice_metadata_to_structured_response(
    *,
    structured_response: NarrativeResponse | None,
    dice_metadata: dict[str, Any],
    dice_roll_strategy: str,
) -> None:
    """Attach dice metadata to structured response and align dice rolls."""
    if not structured_response:
        return

    debug_info = structured_response.debug_info or {}
    if "dice_strategy" in dice_metadata:
        debug_info.setdefault("dice_strategy", dice_metadata["dice_strategy"])
    if "tool_results" in dice_metadata:
        debug_info["tool_results"] = dice_metadata["tool_results"]
        debug_info["tool_requests_executed"] = dice_metadata.get(
            "tool_requests_executed", False
        )
    structured_response.debug_info = debug_info

    if "tool_results" in dice_metadata:
        _apply_tool_results_to_structured_response(
            structured_response,
            dice_metadata.get("tool_results"),
            dice_roll_strategy,
        )


def _is_code_execution_fabrication(
    structured_response: Any,
    code_execution_evidence: dict[str, Any] | None,
    tool_requests_executed: bool = False,
    tool_results: Any = None,
) -> bool:
    """Check if dice results appear without verified RNG code_execution evidence.

    GREEN FIX (Dec 2024): Now uses rng_verified instead of code_execution_used.
    This detects fabrication via print('{"rolls": [16]}') without random.randint().

    When tool_requests_executed=True and dice-specific tool results are present,
    the fallback path executed dice server-side with real RNG. This is NOT
    fabrication. Requires dice-specific tool results (not just any tool like
    faction tools).
    """
    if not structured_response:
        return False

    has_dice = False
    action_resolution = getattr(structured_response, "action_resolution", None)
    if isinstance(action_resolution, dict):
        mechanics = action_resolution.get("mechanics", {})
        if isinstance(mechanics, dict):
            rolls = mechanics.get("rolls", [])
            audit_events = mechanics.get("audit_events", [])
            # Check if audit_events contain actual dice events (dicts with rolls/total)
            # If rolls are absent, treat legacy string audit_events as dice evidence
            has_string_audit_events = isinstance(audit_events, list) and any(
                isinstance(e, str) and e.strip() for e in audit_events
            )
            has_dice_audit_events = (
                isinstance(audit_events, list)
                and any(
                    isinstance(e, dict) and ("rolls" in e or "total" in e or "dc" in e)
                    for e in audit_events
                )
            ) or (not rolls and has_string_audit_events)
            has_dice = (
                isinstance(rolls, list) and len(rolls) > 0
            ) or has_dice_audit_events

    if not has_dice:
        return False

    # Check fallback BEFORE evidence-is-None early return.
    # When tool_requests were executed via the fallback path, dice were rolled
    # server-side with real RNG. Verify dice-specific tools were executed
    # (not just any tool like faction tools).
    if tool_requests_executed and _has_dice_tool_results(tool_results):
        logging_util.info(
            "DICE_FALLBACK_OK: code_execution not used but dice tool_requests executed "
            "server-side via fallback - dice are legitimate (not fabrication)"
        )
        return False

    if code_execution_evidence is None:
        logging_util.warning(
            logging_util.with_campaign(
                "⚠️ MISSING_CODE_EXEC_EVIDENCE: action_resolution dice present but no code_execution evidence. "
                "Treating as potential fabrication."
            )
        )
        return True

    # GREEN FIX: Use rng_verified instead of code_execution_used
    # rng_verified = True only if code contained actual random.randint() calls
    rng_verified = code_execution_evidence.get("rng_verified", False)
    if rng_verified:
        return False  # Verified RNG usage - not fabrication

    # If code was executed but no RNG detected, it's fabrication
    code_was_executed = code_execution_evidence.get("code_execution_used", False)
    if code_was_executed:
        logging_util.warning(
            logging_util.with_campaign(
                "🚨 CODE_EXEC_FABRICATION: code_execution_used=True but rng_verified=False. "
                "LLM ran code but did NOT use random.randint() - action_resolution dice are fabricated!"
            )
        )
        return True

    return True  # No code execution AND no fallback - fabrication


def _log_fabricated_dice_if_detected(
    structured_response: Any,
    code_execution_evidence: dict[str, Any],
    tool_requests_executed: bool = False,
    tool_results: Any = None,
) -> None:
    """Log if dice results appear without code_execution evidence."""
    if _is_code_execution_fabrication(
        structured_response,
        code_execution_evidence,
        tool_requests_executed=tool_requests_executed,
        tool_results=tool_results,
    ):
        logging_util.error(
            logging_util.with_campaign(
                "🚨 FABRICATED_DICE_DETECTED: Gemini returned action_resolution dice but did NOT use "
                "code_execution (executable_code_parts=0). Dice values may be hallucinated! "
                f"action_resolution={getattr(structured_response, 'action_resolution', {})}, "
                f"evidence={code_execution_evidence}"
            )
        )


_DICE_TOOL_NAMES = {"roll_dice", "roll_attack", "roll_skill_check", "roll_saving_throw"}


def _has_dice_tool_results(tool_results: Any) -> bool:
    """Check if tool_results contain any SUCCESSFUL dice-related tools.

    Returns False if dice tools were called but returned errors (e.g., missing dc_reasoning).
    This prevents false positive fabrication detection when tools fail validation.
    """
    if not isinstance(tool_results, list):
        return False

    for result in tool_results:
        if not isinstance(result, dict):
            continue

        tool_name = result.get("tool") or result.get("name", "")
        if isinstance(tool_name, str) and tool_name in _DICE_TOOL_NAMES:
            result_data = result.get("result")
            if result_data and isinstance(result_data, dict):
                # CRITICAL: Check for error responses - these are NOT valid dice results
                # This happens when dice tool is called without required params (e.g., dc_reasoning)
                if "error" in result_data:
                    continue  # Tool call failed, not a valid dice result
                # Valid dice result should have roll/total/formatted data
                if any(
                    k in result_data for k in ("roll", "total", "formatted", "rolls")
                ):
                    return True

    return False


def _has_dice_tool_errors(tool_results: Any) -> tuple[bool, list[str]]:
    """Check if dice tools were called but returned errors.

    Returns:
        Tuple of (has_errors, list of error messages)
    """
    if not isinstance(tool_results, list):
        return False, []

    errors: list[str] = []
    for result in tool_results:
        if not isinstance(result, dict):
            continue

        tool_name = result.get("tool") or result.get("name", "")
        if isinstance(tool_name, str) and tool_name in _DICE_TOOL_NAMES:
            result_data = result.get("result")
            if result_data and isinstance(result_data, dict) and "error" in result_data:
                errors.append(f"{tool_name}: {result_data['error']}")

    return bool(errors), errors


def _extract_dice_rolls_from_tool_results(tool_results: Any) -> list[str]:
    """Convert server tool_results into dice_rolls strings (authoritative)."""
    if not isinstance(tool_results, list):
        return []

    dice_tool_results: list[dict[str, Any]] = []
    for item in tool_results:
        if not isinstance(item, dict):
            continue
        tool_name = item.get("tool")
        if isinstance(tool_name, str) and tool_name in _DICE_TOOL_NAMES:
            dice_tool_results.append(item)

    if not dice_tool_results:
        return []

    text = format_tool_results_text(dice_tool_results)
    if not text:
        return []

    rolls: list[str] = []
    for line in text.splitlines():
        cleaned = line.strip()
        if not cleaned:
            continue
        if cleaned.startswith("- "):
            cleaned = cleaned[2:].strip()
        elif cleaned.startswith("-"):
            cleaned = cleaned[1:].strip()
        if cleaned:
            rolls.append(cleaned)

    return rolls


def _extract_dice_audit_events_from_tool_results(  # noqa: PLR0912
    tool_results: Any,
) -> list[dict[str, Any]]:
    """Build dice_audit_events from tool_results (native_two_phase source of truth)."""
    if not isinstance(tool_results, list):
        return []

    def _notation_from_modifier(modifier: Any) -> str | None:
        mod = _coerce_int(modifier, default=None)
        if mod is None:
            return None
        sign = "+" if mod >= 0 else ""
        return f"1d20{sign}{mod}"

    events: list[dict[str, Any]] = []
    for item in tool_results:
        if not isinstance(item, dict):
            continue
        tool_name = item.get("tool")
        if not isinstance(tool_name, str) or tool_name not in _DICE_TOOL_NAMES:
            continue
        result = item.get("result")
        if not isinstance(result, dict):
            continue

        if tool_name == "roll_attack":
            attack = result.get("attack_roll")
            if isinstance(attack, dict):
                events.append(
                    {
                        "source": "server_tool",
                        "label": item.get("args", {}).get("purpose") or "Attack Roll",
                        "notation": attack.get("notation")
                        or _notation_from_modifier(attack.get("modifier")),
                        "rolls": attack.get("rolls") or [],
                        "modifier": attack.get("modifier") or 0,
                        "total": attack.get("total"),
                    }
                )
            damage = result.get("damage")
            if isinstance(damage, dict):
                events.append(
                    {
                        "source": "server_tool",
                        "label": "Damage",
                        "notation": damage.get("notation"),
                        "rolls": damage.get("rolls") or [],
                        "modifier": damage.get("modifier") or 0,
                        "total": damage.get("total"),
                    }
                )
            continue

        if tool_name == "roll_skill_check":
            skill = result.get("skill") or "Skill Check"
            event = {
                "source": "server_tool",
                "label": str(skill).title(),
                "notation": result.get("notation")
                or _notation_from_modifier(result.get("modifier")),
                "rolls": result.get("rolls")
                or ([result.get("roll")] if result.get("roll") is not None else []),
                "modifier": result.get("modifier") or 0,
                "total": result.get("total"),
            }
            # Include DC and reasoning for audit trail - proves DC set before roll
            if result.get("dc") is not None:
                event["dc"] = result.get("dc")
            if result.get("dc_reasoning"):
                event["dc_reasoning"] = result.get("dc_reasoning")
            if result.get("success") is not None:
                event["success"] = result.get("success")
            events.append(event)
            continue

        if tool_name == "roll_saving_throw":
            save_type = result.get("save_type") or "Save"
            event = {
                "source": "server_tool",
                "label": f"{str(save_type).upper()} Save",
                "notation": result.get("notation")
                or _notation_from_modifier(result.get("modifier")),
                "rolls": result.get("rolls")
                or ([result.get("roll")] if result.get("roll") is not None else []),
                "modifier": result.get("modifier") or 0,
                "total": result.get("total"),
            }
            # Include DC and reasoning for audit trail - proves DC set before roll
            if result.get("dc") is not None:
                event["dc"] = result.get("dc")
            if result.get("dc_reasoning"):
                event["dc_reasoning"] = result.get("dc_reasoning")
            if result.get("success") is not None:
                event["success"] = result.get("success")
            events.append(event)
            continue

        if tool_name == "roll_dice":
            events.append(
                {
                    "source": "server_tool",
                    "label": result.get("purpose") or "Dice Roll",
                    "notation": result.get("notation"),
                    "rolls": result.get("rolls") or [],
                    "modifier": result.get("modifier") or 0,
                    "total": result.get("total"),
                }
            )

    return events


def reconcile_dice_audit_events_with_stdout(
    dice_audit_events: list[dict[str, Any]],
    debug_info: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    """Reconcile dice_audit_events with code_execution stdout as source of truth.

    Fixes two bugs:
    1. LLM incorrectly populates dice_audit_events.rolls with the total value
       instead of the raw die roll (PR #4388)
    2. LLM uses inconsistent stdout schema - sometimes "roll" (singular int)
       instead of "rolls" (array) - this function handles both formats

    Args:
        dice_audit_events: List of dice audit event dicts from LLM response
        debug_info: Debug info dict containing stdout from code_execution

    Returns:
        Corrected dice_audit_events with rolls/modifier values from stdout
    """
    if not dice_audit_events:
        return dice_audit_events

    if not debug_info or not isinstance(debug_info, dict):
        return dice_audit_events

    # Only reconcile if code_execution was actually used
    if not debug_info.get("code_execution_used"):
        return dice_audit_events

    stdout = debug_info.get("stdout")
    if not stdout or not isinstance(stdout, str):
        return dice_audit_events

    # Parse stdout JSON - can be single object, array, or newline-delimited JSON (NDJSON)
    # NDJSON occurs when stdout_parts are joined with newlines
    stdout_events: list[dict[str, Any]] = []
    try:
        parsed = json.loads(stdout)
        if isinstance(parsed, dict):
            stdout_events = [parsed]
        elif isinstance(parsed, list):
            stdout_events = [item for item in parsed if isinstance(item, dict)]
    except (json.JSONDecodeError, TypeError):
        # Try parsing as newline-delimited JSON (NDJSON)
        for line in stdout.strip().split("\n"):
            line = line.strip()
            if not line:
                continue
            try:
                parsed_line = json.loads(line)
                if isinstance(parsed_line, dict):
                    stdout_events.append(parsed_line)
                elif isinstance(parsed_line, list):
                    stdout_events.extend(
                        item for item in parsed_line if isinstance(item, dict)
                    )
            except (json.JSONDecodeError, TypeError):
                continue  # Skip unparseable lines

    if not stdout_events:
        return dice_audit_events

    def _extract_rolls_from_stdout_event(event: dict[str, Any]) -> list[int] | None:
        """Extract rolls from stdout event, handling both 'rolls' (array) and 'roll' (singular)."""
        # Prefer 'rolls' array if present
        rolls = event.get("rolls")
        if isinstance(rolls, list) and rolls:
            return rolls

        # Fallback to 'roll' singular
        roll = event.get("roll")
        if roll is not None and isinstance(roll, (int, float)):
            return [int(roll)]

        return None

    # Build lookup by label/purpose and notation for matching
    # Use lists to preserve order when multiple events have same key
    stdout_by_key: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for event in stdout_events:
        label = (
            str(event.get("label") or event.get("purpose") or event.get("action") or "")
            .lower()
            .strip()
        )
        notation = str(event.get("notation") or "").lower().strip()
        total = event.get("total")
        if label or notation:
            # Key by (label, notation) for precise matching
            key = (label, notation)
            if key not in stdout_by_key:
                stdout_by_key[key] = []
            stdout_by_key[key].append(event)
        # Also key by total for fallback matching (outside label/notation check)
        if total is not None:
            fallback_key = ("", str(total))
            if fallback_key not in stdout_by_key:
                stdout_by_key[fallback_key] = []
            stdout_by_key[fallback_key].append(event)

    # Track consumed events by id() to prevent double-consumption
    # (same event object can be in multiple lists due to primary + fallback indexing)
    consumed_event_ids: set[int] = set()

    corrected: list[dict[str, Any]] = []
    for audit_event in dice_audit_events:
        if not isinstance(audit_event, dict):
            corrected.append(audit_event)
            continue

        # Only reconcile code_execution sourced events
        if audit_event.get("source") != "code_execution":
            corrected.append(audit_event)
            continue

        # Find matching stdout event
        label = (
            str(audit_event.get("label") or audit_event.get("purpose") or "")
            .lower()
            .strip()
        )
        notation = str(audit_event.get("notation") or "").lower().strip()
        total = audit_event.get("total")

        # Try exact match first (skip already-consumed events)
        stdout_event = None
        key = (label, notation)
        if key in stdout_by_key:
            while (
                stdout_by_key[key] and id(stdout_by_key[key][0]) in consumed_event_ids
            ):
                stdout_by_key[key].pop(0)  # Remove already-consumed event
            if stdout_by_key[key]:
                stdout_event = stdout_by_key[key].pop(0)
                consumed_event_ids.add(id(stdout_event))

        # Fallback: match by total ONLY if exactly one unconsumed event has that total
        # (avoids mis-reconciliation when multiple events share the same total)
        if not stdout_event and total is not None:
            fallback_key = ("", str(total))
            if fallback_key in stdout_by_key:
                # Filter to unconsumed candidates only
                unconsumed = [
                    e
                    for e in stdout_by_key[fallback_key]
                    if id(e) not in consumed_event_ids
                ]
                # Only use fallback if there's exactly one candidate (unambiguous match)
                if len(unconsumed) == 1:
                    stdout_event = unconsumed[0]
                    consumed_event_ids.add(id(stdout_event))
                    stdout_by_key[fallback_key].remove(stdout_event)

        if stdout_event:
            # Create corrected copy with values from stdout
            corrected_event = audit_event.copy()

            # Extract rolls using helper that handles both singular and array
            extracted_rolls = _extract_rolls_from_stdout_event(stdout_event)
            if extracted_rolls is not None:
                corrected_event["rolls"] = extracted_rolls

            if "modifier" in stdout_event:
                corrected_event["modifier"] = stdout_event["modifier"]
            # Preserve total from stdout if present
            if "total" in stdout_event:
                corrected_event["total"] = stdout_event["total"]
            corrected.append(corrected_event)
        else:
            # No match found, keep original
            corrected.append(audit_event)

    return corrected


def _extract_action_resolution_rolls_from_tool_results(
    tool_results: Any,
) -> list[dict[str, Any]]:
    """Build action_resolution.mechanics.rolls from tool_results (native_two_phase source)."""
    if not isinstance(tool_results, list):
        return []

    def _notation_from_modifier(modifier: Any) -> str | None:
        mod = _coerce_int(modifier, default=None)
        if mod is None:
            return None
        sign = "+" if mod >= 0 else ""
        return f"1d20{sign}{mod}"

    rolls: list[dict[str, Any]] = []
    for item in tool_results:
        if not isinstance(item, dict):
            continue
        tool_name = item.get("tool")
        if not isinstance(tool_name, str) or tool_name not in _DICE_TOOL_NAMES:
            continue
        result = item.get("result")
        if not isinstance(result, dict):
            continue

        if tool_name == "roll_attack":
            args = item.get("args") if isinstance(item.get("args"), dict) else {}
            purpose = args.get("purpose") or "Attack Roll"
            attack = result.get("attack_roll")
            if isinstance(attack, dict):
                attack_rolls = attack.get("rolls") or (
                    [attack.get("roll")] if attack.get("roll") is not None else []
                )
                attack_result = attack_rolls[0] if attack_rolls else attack.get("roll")
                rolls.append(
                    {
                        "purpose": purpose,
                        "notation": attack.get("notation")
                        or _notation_from_modifier(attack.get("modifier")),
                        "rolls": attack_rolls,
                        "result": attack_result,
                        "total": attack.get("total"),
                        "dc": result.get("target_ac")
                        if result.get("target_ac") is not None
                        else args.get("target_ac"),
                        "success": result.get("hit"),
                    }
                )
            damage = result.get("damage")
            if isinstance(damage, dict):
                damage_rolls = damage.get("rolls") or (
                    [damage.get("roll")] if damage.get("roll") is not None else []
                )
                damage_result = damage_rolls[0] if damage_rolls else damage.get("roll")
                rolls.append(
                    {
                        "purpose": f"{purpose} Damage" if purpose else "Damage",
                        "notation": damage.get("notation"),
                        "rolls": damage_rolls,
                        "result": damage_result,
                        "total": damage.get("total"),
                    }
                )
            continue

        if tool_name == "roll_skill_check":
            skill = result.get("skill") or "Skill Check"
            roll_list = result.get("rolls") or (
                [result.get("roll")] if result.get("roll") is not None else []
            )
            roll_result = roll_list[0] if roll_list else result.get("roll")
            roll_entry = {
                "purpose": str(skill).title(),
                "notation": result.get("notation")
                or _notation_from_modifier(result.get("modifier")),
                "rolls": roll_list,
                "result": roll_result,
                "total": result.get("total"),
            }
            if result.get("dc") is not None:
                roll_entry["dc"] = result.get("dc")
            if result.get("dc_reasoning"):
                roll_entry["dc_reasoning"] = result.get("dc_reasoning")
            if result.get("success") is not None:
                roll_entry["success"] = result.get("success")
            rolls.append(roll_entry)
            continue

        if tool_name == "roll_saving_throw":
            save_type = result.get("save_type") or "Save"
            roll_list = result.get("rolls") or (
                [result.get("roll")] if result.get("roll") is not None else []
            )
            roll_result = roll_list[0] if roll_list else result.get("roll")
            roll_entry = {
                "purpose": f"{str(save_type).upper()} Save",
                "notation": result.get("notation")
                or _notation_from_modifier(result.get("modifier")),
                "rolls": roll_list,
                "result": roll_result,
                "total": result.get("total"),
            }
            if result.get("dc") is not None:
                roll_entry["dc"] = result.get("dc")
            if result.get("dc_reasoning"):
                roll_entry["dc_reasoning"] = result.get("dc_reasoning")
            if result.get("success") is not None:
                roll_entry["success"] = result.get("success")
            rolls.append(roll_entry)
            continue

        if tool_name == "roll_dice":
            roll_list = result.get("rolls") or (
                [result.get("roll")] if result.get("roll") is not None else []
            )
            roll_result = roll_list[0] if roll_list else result.get("roll")
            rolls.append(
                {
                    "purpose": result.get("purpose") or "Dice Roll",
                    "notation": result.get("notation"),
                    "rolls": roll_list,
                    "result": roll_result,
                    "total": result.get("total"),
                }
            )

    return rolls


def _has_fallback_dice_results(tool_results: Any) -> bool:
    """Check if tool_results contains any fallback-executed dice results."""
    if not isinstance(tool_results, list):
        return False
    return any(
        isinstance(tr, dict)
        and tr.get("_fallback")
        and tr.get("tool") in _DICE_TOOL_NAMES
        for tr in tool_results
    )


def _apply_tool_results_to_structured_response(
    structured_response: NarrativeResponse | None,
    tool_results: Any,
    dice_roll_strategy: str,
) -> bool:
    """Apply tool_results into action_resolution for native two-phase or fallback strategies."""
    if not structured_response:
        return False
    # Apply for NATIVE_TWO_PHASE strategy, OR when CODE_EXECUTION has fallback dice results
    is_native_two_phase = (
        dice_roll_strategy == dice_strategy.DICE_STRATEGY_NATIVE_TWO_PHASE
    )
    has_fallback = _has_fallback_dice_results(tool_results)
    if not is_native_two_phase and not has_fallback:
        return False

    audit_events = _extract_dice_audit_events_from_tool_results(tool_results)
    action_rolls = _extract_action_resolution_rolls_from_tool_results(tool_results)
    if not action_rolls:
        return False

    action_resolution = getattr(structured_response, "action_resolution", None)
    if not isinstance(action_resolution, dict):
        action_resolution = {}
    mechanics = action_resolution.get("mechanics")
    if not isinstance(mechanics, dict):
        mechanics = {}

    existing_rolls = mechanics.get("rolls")
    if existing_rolls and existing_rolls != action_rolls:
        debug_info = structured_response.debug_info or {}
        debug_info.setdefault("action_resolution_rolls_model", existing_rolls)
        debug_info["action_resolution_rolls_overridden"] = True
        structured_response.debug_info = debug_info
        source = "fallback" if has_fallback else "native_two_phase"
        logging_util.warning(
            logging_util.with_campaign(
                f"ACTION_RESOLUTION_ROLLS_MISMATCH: Replacing model rolls with tool_results "
                f"({source} authoritative)."
            )
        )

    mechanics["rolls"] = action_rolls
    if audit_events:
        mechanics["audit_events"] = audit_events
    action_resolution["mechanics"] = mechanics
    structured_response.action_resolution = action_resolution

    return True


def _should_require_dice_rolls_for_turn(
    *,
    current_game_state: GameState | None,
    user_input: str,
    mode: str,
    is_god_mode: bool,
    is_dm_mode: bool,
) -> bool:
    """Check if dice rolls should be required for this turn."""
    if mode != constants.MODE_CHARACTER or is_god_mode or is_dm_mode:
        return False

    text = (user_input or "").strip().lower()
    if not text or text.startswith("/"):
        return False

    text = _truncate_for_combat_scan(text)
    has_combat_keywords = any(
        pattern.search(text) for pattern in _COMBAT_KEYWORD_PATTERNS_USER_INPUT
    )

    in_combat = bool(
        current_game_state and current_game_state.combat_state.get("in_combat", False)
    )

    return has_combat_keywords or in_combat


COMBAT_ACTION_KEYWORDS = (
    "attack",
    "shoot",
    "strike",
    "stab",
    "slash",
    "swing",
    "hit",
    "cast",
    "spell",
    "fireball",
    "roll",
    "save",
    "saving throw",
    "skill",
    "check",
    "initiative",
    "grapple",
    "shove",
    "dodge",
    "dash",
    "disengage",
    "help",
)

_COMBAT_ACTION_KEYWORDS_USER_INPUT = (
    "attack",
    "shoot",
    "strike",
    "stab",
    "slash",
    "swing",
    "hit",
    "cast",
    "spell",
    "fireball",
    "saving throw",
    "initiative",
    "grapple",
    "shove",
    "dodge",
    "dash",
    "disengage",
)

_COMBAT_KEYWORD_MAX_CHARS = 5000
_COMBAT_KEYWORD_PATTERNS = tuple(
    re.compile(r"\b" + re.escape(keyword) + r"\b") for keyword in COMBAT_ACTION_KEYWORDS
)
_COMBAT_KEYWORD_PATTERNS_USER_INPUT = tuple(
    re.compile(r"\b" + re.escape(keyword) + r"\b")
    for keyword in _COMBAT_ACTION_KEYWORDS_USER_INPUT
)


def _truncate_for_combat_scan(text: str) -> str:
    if len(text) > _COMBAT_KEYWORD_MAX_CHARS:
        return text[:_COMBAT_KEYWORD_MAX_CHARS]
    return text


_PAST_TENSE_MARKERS = (
    "died",
    "killed",
    "defeated",
    "was attacked",
    "were attacked",
    "had attacked",
    "was hit",
    "were hit",
    "had hit",
    "was struck",
    "were struck",
    "had struck",
    "previously",
    "last session",
    "earlier",
    "before",
    "remembered",
    "recalled",
)

_HYPOTHETICAL_MARKERS = (
    "could attack",
    "could strike",
    "could hit",
    "might attack",
    "might strike",
    "might hit",
    "would attack",
    "would strike",
    "would hit",
    "if you attack",
    "if you strike",
    "if you hit",
    "you could",
    "you might",
    "you would",
    "want to attack",
    "plan to attack",
    "decide to attack",
)

_ACTIVE_COMBAT_PATTERNS = (
    "attacks you",
    "strikes at",
    "swings at",
    "shoots at",
    "casts at",
    "hits you",
    "damage to",
    "takes damage",
    "deals damage",
    "dealing damage",
    "roll to hit",
    "rolls to hit",
    "attack roll",
    "makes an attack",
    "roll for initiative",
    "rolls initiative",
    "d20",
    "1d20",
    "2d6",
    "1d8",
    "1d6",
)


def _detect_combat_in_narrative(narrative_text: str) -> bool:
    """Detect ACTIVE combat in LLM-generated narrative text."""
    if not narrative_text:
        return False

    text = _truncate_for_combat_scan(narrative_text.lower())

    has_past_marker = any(marker in text for marker in _PAST_TENSE_MARKERS)
    has_hypothetical_marker = any(marker in text for marker in _HYPOTHETICAL_MARKERS)
    has_active_pattern = any(pattern in text for pattern in _ACTIVE_COMBAT_PATTERNS)

    if has_active_pattern and not has_hypothetical_marker:
        return True

    has_combat_keyword = any(
        pattern.search(text) for pattern in _COMBAT_KEYWORD_PATTERNS
    )

    if has_combat_keyword:
        if has_hypothetical_marker:
            return False
        return not (has_past_marker and not has_active_pattern)

    return False


def _check_dice_integrity(
    *,
    structured_response: NarrativeResponse | None,
    api_response: Any,
) -> tuple[bool, str]:
    """Check if dice in action_resolution came from legitimate tool execution.

    PRIMARY CHECK: action_resolution.mechanics.rolls/audit_events (centralized)
    """
    if not structured_response:
        return True, ""

    # PRIMARY: Check action_resolution.mechanics for dice
    has_real_dice = False
    rolls_count = 0
    audit_events_count = 0
    legacy_dice_rolls: list[str] = []
    action_resolution = getattr(structured_response, "action_resolution", None)
    if isinstance(action_resolution, dict):
        mechanics = action_resolution.get("mechanics", {})
        if isinstance(mechanics, dict):
            rolls = mechanics.get("rolls", [])
            audit_events = mechanics.get("audit_events", [])
            if isinstance(rolls, list):
                rolls_count = len(rolls)
            if isinstance(audit_events, list):
                audit_events_count = len(audit_events)
            has_real_dice = rolls_count > 0 or audit_events_count > 0

    # FALLBACK: Check legacy dice_rolls (for old responses or schema violations)
    if not has_real_dice:
        legacy_dice_rolls = getattr(structured_response, "dice_rolls", None) or []
        has_real_dice = any(str(roll).strip() for roll in legacy_dice_rolls)

    if not has_real_dice:
        return True, ""

    tool_requests_executed = getattr(api_response, "_tool_requests_executed", None)

    if tool_requests_executed is None:
        logging_util.debug(
            logging_util.with_campaign(
                "DICE_INTEGRITY: No _tool_requests_executed metadata on response, "
                "skipping integrity check for backward compatibility"
            )
        )
        return True, ""

    if tool_requests_executed:
        return True, ""

    return False, (
        "Response contains dice outcomes "
        f"(rolls={rolls_count}, audit_events={audit_events_count}, "
        f"legacy_dice_rolls={len(legacy_dice_rolls)}) but no tool_requests were executed. "
        "Dice rolls must come from tool execution, not fabrication."
    )


def _validate_combat_dice_integrity(
    *,
    user_input: str,
    narrative_text: str,
    structured_response: NarrativeResponse | None,
    current_game_state: GameState | None,  # noqa: ARG001
    api_response: Any,
    mode: str,
    is_god_mode: bool,
    is_dm_mode: bool,
    dice_roll_strategy: str | None = None,
) -> tuple[bool, str | None]:
    """Validate dice integrity when combat is detected."""
    if is_god_mode or is_dm_mode:
        return True, None

    if mode != constants.MODE_CHARACTER:
        return True, None

    # Skip for code_execution strategy - that has its own check (_is_code_execution_fabrication)
    if dice_roll_strategy == dice_strategy.DICE_STRATEGY_CODE_EXECUTION:
        return True, None

    user_text = (user_input or "").strip().lower()
    if user_text:
        user_text = _truncate_for_combat_scan(user_text)
    user_has_combat = (
        any(pattern.search(user_text) for pattern in _COMBAT_KEYWORD_PATTERNS)
        if user_text
        else False
    )

    narrative_has_combat = _detect_combat_in_narrative(narrative_text)

    if not user_has_combat and not narrative_has_combat:
        return True, None

    is_valid, reason = _check_dice_integrity(
        structured_response=structured_response,
        api_response=api_response,
    )

    if is_valid:
        return True, None

    combat_source = []
    if user_has_combat:
        combat_source.append("user_input")
    if narrative_has_combat:
        combat_source.append("narrative")

    logging_util.warning(
        logging_util.with_campaign(
            f"DICE_INTEGRITY_VIOLATION: Combat detected in {', '.join(combat_source)} "
            f"but action_resolution dice were not from tool execution. Reason: {reason}"
        )
    )

    return False, (
        "DICE INTEGRITY VIOLATION: Your response includes action_resolution dice but you did not use "
        "tool_requests to roll them. In combat, you MUST use tool_requests (roll_dice, roll_attack, etc.) "
        "to generate dice rolls. Do NOT fabricate dice results. "
        "Regenerate your response using tool_requests for all dice rolls."
    )


def _validate_dice_integrity_always(
    *,
    structured_response: NarrativeResponse | None,
    api_response: Any,
    mode: str,
    is_god_mode: bool,
    is_dm_mode: bool,
    dice_roll_strategy: str | None = None,
) -> tuple[bool, str | None]:
    """Validate dice integrity for ALL responses with action_resolution dice.

    This catches fabricated dice even when combat is not detected - e.g., skill checks
    for absorbing items, Arcana checks, etc. Any response with action_resolution dice must have
    tool_requests_executed.

    NOTE: This function only applies to NATIVE_TWO_PHASE strategy (tool_requests).
    For CODE_EXECUTION strategy (Gemini 3), use _is_code_execution_fabrication instead.
    """
    if is_god_mode or is_dm_mode:
        return True, None

    if mode != constants.MODE_CHARACTER:
        return True, None

    # Skip for code_execution strategy - that has its own check (_is_code_execution_fabrication)
    if dice_roll_strategy == dice_strategy.DICE_STRATEGY_CODE_EXECUTION:
        return True, None

    is_valid, reason = _check_dice_integrity(
        structured_response=structured_response,
        api_response=api_response,
    )

    if is_valid:
        return True, None

    logging_util.warning(
        logging_util.with_campaign(
            f"DICE_INTEGRITY_ALWAYS_VIOLATION: Response has action_resolution dice but no tool execution. "
            f"Reason: {reason}"
        )
    )

    return False, (
        "DICE INTEGRITY VIOLATION: Your response includes action_resolution dice but you did not use "
        "tool_requests to roll them. For ANY dice roll (combat, skill checks, saving throws), "
        "you MUST use tool_requests (roll_skill_check, roll_saving_throw, roll_attack, etc.). "
        "Do NOT fabricate dice results. Regenerate your response using tool_requests."
    )


# =============================================================================
# God Mode Validation Helpers
# =============================================================================


def _check_god_mode_forbidden_list_field(
    structured_response: NarrativeResponse,
    field_name: str,
    log_violation_type: str,
    forbidden_action: str,
) -> str | None:
    """Check for forbidden list field in god mode response.

    Centralized helper for god mode validation of list fields (dice_rolls,
    dice_audit_events, tool_requests). Returns warning message if violation
    detected, None otherwise.

    Args:
        structured_response: The LLM response to validate
        field_name: Attribute name to check (e.g., "dice_rolls")
        log_violation_type: Type for log message (e.g., "DICE")
        forbidden_action: Human description (e.g., "no dice rolling allowed")
    """
    field_value = getattr(structured_response, field_name, None)
    if field_value and isinstance(field_value, list) and len(field_value) > 0:
        # Log with count for list fields, raw value for small lists
        log_detail = (
            f"{len(field_value)} items" if len(field_value) > 3 else str(field_value)
        )
        logging_util.warning(
            logging_util.with_campaign(
                f"🚨 GOD_MODE_{log_violation_type}_VIOLATION: God mode response "
                f"contains {field_name}: {log_detail}"
            )
        )
        return (
            f"GOD_MODE_VIOLATION: {field_name} field populated in god mode response. "
            f"God mode is administrative only - {forbidden_action}."
        )
    return None


def _check_god_mode_dice_rolls(structured_response: NarrativeResponse) -> str | None:
    """Check for forbidden dice_rolls in god mode response."""
    return _check_god_mode_forbidden_list_field(
        structured_response, "dice_rolls", "DICE", "no dice rolling allowed"
    )


def _check_god_mode_dice_audit_events(
    structured_response: NarrativeResponse,
) -> str | None:
    """Check for forbidden dice_audit_events in god mode response."""
    return _check_god_mode_forbidden_list_field(
        structured_response,
        "dice_audit_events",
        "DICE_AUDIT",
        "no dice artifacts allowed",
    )


def _check_god_mode_tool_requests(structured_response: NarrativeResponse) -> str | None:
    """Check for forbidden tool_requests in god mode response."""
    return _check_god_mode_forbidden_list_field(
        structured_response, "tool_requests", "TOOL_REQUESTS", "no tool usage allowed"
    )


def _check_god_mode_action_resolution(
    structured_response: NarrativeResponse,
) -> str | None:
    """Check for forbidden action_resolution dice in god mode response.

    Returns warning message if violation detected, None otherwise.
    """
    action_resolution = getattr(structured_response, "action_resolution", None)
    action_resolution_dict = (
        action_resolution if isinstance(action_resolution, dict) else None
    )
    if action_resolution_dict and has_action_resolution_dice(action_resolution_dict):
        # Extract counts for logging
        mechanics = action_resolution_dict.get("mechanics", {})
        rolls = mechanics.get("rolls", []) if isinstance(mechanics, dict) else []
        audit_events = (
            mechanics.get("audit_events", []) if isinstance(mechanics, dict) else []
        )
        logging_util.warning(
            logging_util.with_campaign(
                f"🚨 GOD_MODE_ACTION_RESOLUTION_VIOLATION: God mode response contains "
                f"action_resolution dice (rolls={len(rolls) if isinstance(rolls, list) else 0}, "
                f"audit_events={len(audit_events) if isinstance(audit_events, list) else 0})"
            )
        )
        return (
            "GOD_MODE_VIOLATION: action_resolution.mechanics contains dice in god mode. "
            "God mode is frozen - no dice rolls or combat mechanics allowed."
        )
    return None


def _check_god_mode_narrative(structured_response: NarrativeResponse) -> str | None:
    """Check for forbidden non-empty narrative in god mode response.

    Ignores placeholder content (session headers, metadata, whitespace) that doesn't
    advance the story. Only warns on actual narrative prose.

    Returns warning message if violation detected, None otherwise.
    """
    narrative = getattr(structured_response, "narrative", None)
    if not narrative or not isinstance(narrative, str):
        return None

    narrative_stripped = narrative.strip()
    if not narrative_stripped:
        return None  # Whitespace only - acceptable

    # Define narrative indicators used across validation checks
    ACTION_VERBS = ("attack", "die", "kill", "fight", "begin", "feel", "scream", "win", "lose", "defeat")
    NARRATIVE_PRONOUNS = ("you", "your", "yours")

    # Ignore common placeholder patterns that don't advance the story
    PLACEHOLDER_PATTERNS = (
        "[SESSION_HEADER]",
        "[Mode:",
        "[HEADER]",
        "[STATUS]",
        "Timestamp:",
        "Location:",
        "Status:",
    )
    # Check if content starts with placeholder pattern
    # Apply action verb/pronoun check to prevent "Location: Die now" bypasses
    is_placeholder_start = any(
        narrative_stripped.startswith(pattern) for pattern in PLACEHOLDER_PATTERNS
    )
    if is_placeholder_start:
        # Strip all placeholder patterns and check if substantive prose remains
        remaining = narrative_stripped
        for pattern in PLACEHOLDER_PATTERNS:
            remaining = remaining.replace(pattern, "")
        remaining = remaining.strip()
        # Only exempt if remaining content is minimal (< 20 chars) AND non-narrative
        # Prevents bypass scenarios like "Location: Die now" or "Status: You win"
        if len(remaining) < 20:
            remaining_lower = remaining.lower()
            has_action_in_remaining = any(verb in remaining_lower for verb in ACTION_VERBS)
            has_pronoun_in_remaining = any(pronoun in remaining_lower for pronoun in NARRATIVE_PRONOUNS)

            # Exempt only if no narrative indicators present
            if not has_action_in_remaining and not has_pronoun_in_remaining:
                return None  # Metadata/headers - acceptable (e.g., "Timestamp: 2024-01-01")
        # Otherwise, it's prose with placeholder prefix - continue to validation

    # Exempt short non-prose content (< 50 chars, no periods, no action verbs, no pronouns).
    # Keep ultra-short generic fragments (e.g. "OK") as violations to avoid narrative bypasses.
    if len(narrative_stripped) < 50:
        if len(narrative_stripped) >= 4:
            has_period = "." in narrative_stripped
            narrative_lower = narrative_stripped.lower()
            has_action_verb = any(verb in narrative_lower for verb in ACTION_VERBS)
            has_pronoun = any(pronoun in narrative_lower for pronoun in NARRATIVE_PRONOUNS)

            if not has_period and not has_action_verb and not has_pronoun:
                return None  # Short metadata without narrative indicators - acceptable

    # Any remaining non-empty narrative content is forbidden in god mode.
    logging_util.warning(
        logging_util.with_campaign(
            f"🚨 GOD_MODE_NARRATIVE_VIOLATION: God mode has narrative prose "
            f"({len(narrative_stripped)} chars). Should use god_mode_response only."
        )
    )
    return (
        "GOD_MODE_VIOLATION: narrative field has content in god mode. "
        "God mode narrative MUST be empty - use god_mode_response field instead."
    )


def validate_god_mode_response(
    structured_response: NarrativeResponse | None,
    *,
    is_god_mode: bool,
) -> list[str]:
    """Validate god mode responses for forbidden dice rolls and narrative content.

    God mode is an administrative "pause menu" - the world is frozen. God mode
    responses should NEVER contain dice rolls, action resolution, or narrative
    content that advances the story.

    Args:
        structured_response: The parsed NarrativeResponse object
        is_god_mode: Whether this is a god mode command

    Returns:
        List of warning messages for violations detected.
        Empty list if no violations.
    """
    if not is_god_mode or not structured_response:
        return []

    warnings: list[str] = []

    # Run all validation checks using helper functions
    checks = [
        _check_god_mode_dice_rolls,
        _check_god_mode_dice_audit_events,
        _check_god_mode_tool_requests,
        _check_god_mode_action_resolution,
        _check_god_mode_narrative,
    ]

    for check in checks:
        warning = check(structured_response)
        if warning:
            warnings.append(warning)

    return warnings

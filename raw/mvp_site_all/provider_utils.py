"""Shared utilities for LLM provider implementations.

Schema reference:
- SOURCE OF TRUTH: mvp_site/prompts/game_state_instruction.md (Section: "JSON Response Format (Required Fields)")
- VALIDATION LAYER: mvp_site/schemas/narrative_response_schema.py
- Hierarchy: prompt → NARRATIVE_RESPONSE_SCHEMA → NarrativeResponse

Provider notes:
- Cerebras/OpenRouter uses NARRATIVE_RESPONSE_SCHEMA via get_openai_json_schema_format(strict=False)
- Gemini avoids response_schema and uses response_mime_type="application/json" + prompt instruction
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from typing import Any, Protocol

from mvp_site import faction_state_util, logging_util
from mvp_site.faction.tools import FACTION_TOOL_NAMES, execute_faction_tool
from mvp_site.game_state import update_game_state_with_tool_results
from mvp_site.llm_providers import gemini_code_execution
from mvp_site.narrative_response_schema import _log_json_parse_error

# Pattern to strip tool_requests dice sections when using code_execution dice strategy.
# These sections are only relevant for native_two_phase strategy (tool_requests flow).
_TOOL_REQUESTS_DICE_PATTERN = re.compile(
    r"<!-- BEGIN_TOOL_REQUESTS_DICE[^>]*-->.*?<!-- END_TOOL_REQUESTS_DICE -->",
    re.DOTALL,
)


def strip_tool_requests_dice_instructions(text: str) -> str:
    """Remove tool_requests dice sections from system instructions.

    Used when code_execution strategy is active - dice are handled via Python
    random.randint() instead of tool_requests.
    """
    if not text or not isinstance(text, str):
        return text if isinstance(text, str) else ""
    return _TOOL_REQUESTS_DICE_PATTERN.sub("", text)


def _attach_tool_execution_metadata(
    response: Any,
    executed: bool,
    tool_results: list[dict] | None = None,
) -> Any:
    """Attach tool execution metadata to a response object.

    This metadata is used by downstream validation to verify dice integrity.

    Args:
        response: The response object to attach metadata to
        executed: Whether tool_requests were executed
        tool_results: The results from tool execution (if any)

    Returns:
        The same response object with metadata attached
    """
    if hasattr(response, "__dict__"):
        response._tool_requests_executed = executed
        response._tool_results = tool_results or []
    return response


# =============================================================================
# NARRATIVE_RESPONSE_SCHEMA - JSON schema for structured LLM outputs
# =============================================================================

# Schema for Cerebras/OpenRouter - supports additionalProperties for dynamic objects
NARRATIVE_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "narrative": {
            "type": "string",
            "description": "The main narrative text describing what happens",
        },
        "planning_block": {
            "type": "object",
            "description": "GM planning with thinking field and dynamic choices (snake_case keys like explore_tavern, attack_goblin, god:option_1, think:analysis)",
            "properties": {
                "thinking": {
                    "type": "string",
                    "description": "GM tactical analysis of the current situation and what the player might want to do",
                },
                "context": {
                    "type": "string",
                    "description": "Current scenario context for choice generation",
                },
                "choices": {
                    "type": "object",
                    "description": "Player choices with snake_case keys (e.g., explore_tavern, attack_goblin)",
                    # NOTE: No minProperties constraint - Phase 1 combat returns empty choices {}
                    # while awaiting dice results (see game_state_instruction.md:41)
                    "additionalProperties": {
                        "type": "object",
                        "description": "A single player choice option",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "Short display text for the choice",
                            },
                            "description": {
                                "type": "string",
                                "description": "Detailed description of what this choice entails",
                            },
                            "risk_level": {
                                "type": "string",
                                "description": "Risk assessment: low, medium, high, or unknown",
                            },
                        },
                        "required": ["text", "description"],
                    },
                },
            },
            "required": ["thinking", "choices"],
            # additionalProperties:true allows extra fields like context
            "additionalProperties": True,
        },
        "entities_mentioned": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of entity names mentioned in the narrative",
        },
        "location_confirmed": {
            "type": "string",
            "description": "Current location name",
        },
        "session_header": {
            "type": "string",
            "description": "Session context header",
        },
        "dice_rolls": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of dice roll results",
        },
        "dice_audit_events": {
            "type": "array",
            "description": (
                "Structured dice audit events with raw rolls and computed totals. "
                "Used for post-hoc RNG auditing and provenance (server_tool vs code_execution)."
            ),
            "items": {
                "type": "object",
                "description": "A single dice audit event",
                "additionalProperties": True,
            },
        },
        "resources": {
            "type": "string",
            "description": "Resource tracking information",
        },
        "rewards_box": {
            "type": "object",
            "description": "Structured rewards summary for user-visible display",
            "properties": {
                "source": {
                    "type": "string",
                    "description": "Reward source: combat, encounter, quest, milestone",
                },
                "xp_gained": {
                    "type": "number",
                    "description": "XP gained from this reward event",
                },
                "current_xp": {
                    "type": "number",
                    "description": "Player's current total XP after rewards",
                },
                "next_level_xp": {
                    "type": "number",
                    "description": "XP threshold for next level",
                },
                "progress_percent": {
                    "type": "number",
                    "description": "Percent progress toward next level",
                },
                "level_up_available": {
                    "type": "boolean",
                    "description": "Whether the player can level up now",
                },
                "loot": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Loot items gained (use 'None' if no loot)",
                },
                "gold": {
                    "type": "number",
                    "description": "Gold gained (0 if none)",
                },
            },
            "required": [
                "source",
                "xp_gained",
                "current_xp",
                "next_level_xp",
                "progress_percent",
                "level_up_available",
                "loot",
            ],
            "additionalProperties": False,
        },
        "turn_summary": {
            "type": "string",
            "description": "Summary of what happened this turn",
        },
        "state_updates": {
            "type": "object",
            "description": "Game state updates (HP, inventory, conditions, etc.)",
            "additionalProperties": True,
        },
        "debug_info": {
            "type": "object",
            "description": "Debug information for development",
            "additionalProperties": True,
        },
        "god_mode_response": {
            "type": "string",
            "description": "Response for god mode commands",
        },
        "tool_requests": {
            "type": "array",
            "description": "MANDATORY for combat and dice rolls. Request dice rolls or skill checks - server will execute and you'll get results for the final narrative. MUST include tool_requests for any attack, skill check, or saving throw.",
            "items": {
                "type": "object",
                "properties": {
                    "tool": {
                        "type": "string",
                        "enum": [
                            # Dice tools
                            "roll_dice",
                            "roll_attack",
                            "roll_skill_check",
                            "roll_saving_throw",
                            "declare_no_roll_needed",
                            # Faction tools
                            "faction_simulate_battle",
                            "faction_intel_operation",
                            "faction_calculate_ranking",
                            "faction_fp_to_next_rank",
                            "faction_calculate_power",
                        ],
                        "description": "The tool to call",
                    },
                    "args": {
                        "type": "object",
                        "description": "Arguments for the tool",
                        "additionalProperties": True,
                    },
                },
                "required": ["tool", "args"],
            },
        },
    },
    "required": ["narrative", "planning_block", "entities_mentioned"],
    # Note: With strict:False, additionalProperties defaults to true (allows extra fields)
}


def get_openai_json_schema_format(
    name: str = "narrative_response", schema: dict[str, Any] | None = None
) -> dict:
    """Get schema in OpenAI/Cerebras json_schema format.

    Returns the schema wrapped for use with response_format.type="json_schema"

    NOTE: Uses strict=False to allow dynamic choice keys in planning_block.
    The game design requires semantic keys like 'explore_tavern', 'attack_goblin',
    'god:option_1' which cannot be pre-defined in a strict schema.

    Structure enforcement still happens via:
    - Top-level fields (narrative, entities_mentioned) are validated
    - planning_block internal structure validated by narrative_response_schema.py
    """
    schema_definition = NARRATIVE_RESPONSE_SCHEMA if schema is None else schema

    return {
        "type": "json_schema",
        "json_schema": {
            "name": name,
            "strict": False,  # Allow dynamic choice keys in planning_block
            "schema": schema_definition,
        },
    }


def stringify_prompt_contents(prompt_contents: list[Any]) -> str:
    """Best-effort stringify prompt content parts for provider message payloads."""
    if not prompt_contents:
        return ""

    parts: list[str] = []
    for item in prompt_contents:
        if isinstance(item, str):
            parts.append(item)
        elif isinstance(item, dict):
            # Handle dict-based content (e.g., {"text": "..."})
            if "text" in item:
                parts.append(str(item["text"]))
            else:
                parts.append(str(item))
        else:
            parts.append(str(item))

    return "\n".join(parts)


def stringify_chat_parts(parts: list[Any]) -> str:
    """Stringify prompt parts for OpenAI-chat compatible providers (Cerebras/OpenRouter).

    Matches the historical formatting used in those providers: JSON-dump non-strings
    and join with a blank line between parts.
    """
    if not parts:
        return ""

    rendered: list[str] = []
    for part in parts:
        if isinstance(part, str):
            rendered.append(part)
        else:
            try:
                rendered.append(json.dumps(part))
            except Exception:  # noqa: BLE001 - defensive stringify
                rendered.append(str(part))
    return "\n\n".join(rendered)


def build_tool_results_prompt(
    tool_results_text: str, extra_instructions: str = ""
) -> str:
    """Build the Phase 2 prompt snippet for injecting tool results."""
    base = (
        "Tool results (use these exact numbers in your narrative):\n"
        f"{tool_results_text}\n\n"
        "The dice rolls have been executed by the server. Copy these EXACT results into your response. "
        "Do NOT recalculate, round, or modify outcomes. "
        "If any dice were rolled, you MUST include them in action_resolution.mechanics.rolls "
        "(or action_resolution.mechanics.audit_events) using the exact results above. "
        "Do NOT invent rolls. Do NOT populate dice_rolls directly. "
        "Now write the final response using these results. Do NOT include tool_requests in your response."
    )
    extra = (extra_instructions or "").strip()
    if not extra:
        return base
    return f"{base}\n\n{extra}"


class _Logger(Protocol):
    def info(self, msg: str) -> None: ...
    def warning(self, msg: str) -> None: ...
    def error(self, msg: str) -> None: ...


def execute_openai_tool_calls(
    tool_calls: list[dict],
    *,
    execute_tool_fn: Callable[[str, dict[str, Any]], dict],
    logger: _Logger | None = None,
) -> list[dict]:
    """Execute OpenAI-compatible tool_calls and return a normalized result list.

    Expected tool_calls format:
      [{"id": str, "type": "function", "function": {"name": str, "arguments": str}}]
    """
    results: list[dict] = []
    for call in tool_calls:
        try:
            call_id = str(call.get("id", ""))
            func = call.get("function", {}) or {}
            tool_name = str(func.get("name", ""))
            args_str = func.get("arguments", "{}")

            # Parse arguments JSON
            try:
                args = json.loads(args_str) if args_str else {}
            except json.JSONDecodeError:
                args = {}

            result = execute_tool_fn(tool_name, args)
            results.append(
                {
                    "tool_call_id": call_id,
                    "tool": tool_name,
                    "args": args,
                    "result": result,
                }
            )
            if logger:
                logger.info(f"NATIVE_TOOL_CALL: {tool_name}({args}) -> {result}")
        except Exception as exc:  # noqa: BLE001 - defensive tool loop
            if logger:
                logger.error(f"Native tool execution error: {exc}")
            results.append(
                {
                    "tool_call_id": str(call.get("id", "")),
                    "tool": str(
                        (call.get("function", {}) or {}).get("name", "unknown")
                    ),
                    "args": {},
                    "result": {"error": str(exc)},
                }
            )
    return results


def _compact_tool_result_for_prompt(result: Any) -> dict[str, Any]:
    """Reduce tool results to the minimal data the model needs to narrate correctly."""
    if not isinstance(result, dict):
        return {"result": result}

    if isinstance(result.get("error"), str) and result["error"]:
        return {"error": result["error"]}

    compact: dict[str, Any] = {}
    if isinstance(result.get("formatted"), str) and result["formatted"]:
        compact["formatted"] = result["formatted"]

    # Common dice payload fields
    for key in ("notation", "rolls", "modifier", "total", "natural_20", "natural_1"):
        if key in result:
            compact[key] = result[key]

    # roll_attack
    for key in (
        "hit",
        "critical",
        "fumble",
        "target_ac",
        "weapon_name",
        "ability_name",
    ):
        if key in result:
            compact[key] = result[key]
    if isinstance(result.get("damage"), dict):
        dmg = result["damage"]
        compact["damage"] = {
            k: dmg.get(k)
            for k in ("notation", "rolls", "modifier", "total", "critical")
        }

    # roll_skill_check / roll_saving_throw
    for key in (
        "skill",
        "dc",
        "success",
        "save_type",
        "proficiency_applied",
        "attribute_name",
        "roll",
    ):
        if key in result:
            compact[key] = result[key]

    return compact


def run_openai_json_first_tool_requests_flow(
    *,
    generate_content_fn: Callable[..., Any],
    prompt_contents: list[Any],
    model_name: str,
    system_instruction_text: str | None,
    temperature: float,
    max_output_tokens: int,
    provider_no_tool_requests_log_prefix: str,
    execute_tool_requests_fn: Callable[[list[dict]], list[dict]],
    format_tool_results_text_fn: Callable[[list[dict]], str],
    logger: _Logger,
    tools: list[dict] | None = None,
    messages: list[dict] | None = None,
    api_key: str | None = None,
    json_mode: bool = True,
    phase1_invalid_json_retries: int = 0,
) -> Any:
    """Run the JSON-first tool_requests orchestration shared by OpenAI-chat providers."""

    def phase1() -> Any:
        logger.info("Phase 1: JSON call (checking for tool_requests)")
        return generate_content_fn(
            prompt_contents=prompt_contents,
            model_name=model_name,
            system_instruction_text=system_instruction_text,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            tools=None if tools is None else tools,
            messages=messages,
            api_key=api_key,
            json_mode=json_mode,
        )

    def extract_text(resp: Any) -> str:
        return getattr(resp, "text", "") or ""

    def build_history(
        *, prompt_contents: list[Any], phase1_text: str, tool_results_prompt: str
    ) -> list[dict[str, Any]]:
        messages: list[dict[str, Any]] = []
        if system_instruction_text:
            messages.append({"role": "system", "content": system_instruction_text})
        messages.append(
            {"role": "user", "content": stringify_chat_parts(prompt_contents)}
        )
        messages.append({"role": "assistant", "content": phase1_text})
        messages.append({"role": "user", "content": tool_results_prompt})
        return messages

    def phase2(messages: list[dict[str, Any]]) -> Any:
        logger.info("Phase 2: JSON call with tool results")
        return generate_content_fn(
            prompt_contents=[],
            model_name=model_name,
            system_instruction_text=None,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            tools=None,
            messages=messages,
            api_key=api_key,
            json_mode=json_mode,
        )

    return run_json_first_tool_requests_flow(
        phase1_generate_fn=phase1,
        extract_text_fn=extract_text,
        prompt_contents=prompt_contents,
        execute_tool_requests_fn=execute_tool_requests_fn,
        format_tool_results_text_fn=format_tool_results_text_fn,
        build_history_fn=build_history,
        phase2_generate_fn=phase2,
        logger=logger,
        no_tool_requests_log_msg=lambda response_data: (
            f"{provider_no_tool_requests_log_prefix}: No tool_requests in LLM response. "
            f"Response keys: {list(response_data.keys())}"
        ),
        phase1_invalid_json_retries=phase1_invalid_json_retries,
    )


def run_json_first_tool_requests_flow(  # noqa: PLR0911, PLR0912, PLR0915
    *,
    phase1_generate_fn: Callable[[], Any],
    extract_text_fn: Callable[[Any], str],
    prompt_contents: list[Any],
    execute_tool_requests_fn: Callable[[list[dict]], list[dict]],
    format_tool_results_text_fn: Callable[[list[dict]], str],
    build_history_fn: Callable[..., Any],
    phase2_generate_fn: Callable[[Any], Any],
    logger: _Logger,
    no_tool_requests_log_msg: str | Callable[[dict[str, Any]], str],
    tool_requests_key: str = "tool_requests",
    phase1_invalid_json_retries: int = 0,
) -> Any:
    """Provider-agnostic JSON-first tool_requests orchestration.

    This is useful for providers that cannot combine tools + JSON mode and
    therefore need to:
    1) Ask for JSON with (optional) tool_requests
    2) Execute tool_requests server-side
    3) Re-ask for JSON with injected tool results
    """
    max_attempts = max(0, int(phase1_invalid_json_retries)) + 1
    response_1: Any | None = None
    response_text = ""
    response_data: Any = None
    phase1_text_for_history = ""

    for attempt in range(1, max_attempts + 1):
        response_1 = phase1_generate_fn()
        response_text = (extract_text_fn(response_1) or "").strip()

        try:
            response_data = json.loads(response_text) if response_text else {}
            phase1_text_for_history = response_text
            if isinstance(response_data, str):
                # Some providers/models double-encode JSON (i.e., return a JSON string whose
                # contents are themselves JSON). Attempt one extra decode so downstream logic
                # can safely treat Phase 1 as dict/list.
                inner_text = response_data.strip()
                try:
                    response_data = json.loads(inner_text) if inner_text else {}
                    phase1_text_for_history = inner_text
                    logger.info(
                        "Phase 1 response was a JSON-encoded string; decoded inner JSON successfully"
                    )
                except json.JSONDecodeError:
                    logger.warning(
                        "Phase 1 response parsed to a string, but inner content was not valid JSON; returning as-is"
                    )
                    return _attach_tool_execution_metadata(response_1, executed=False)
            break
        except json.JSONDecodeError as e:
            if response_text.startswith("[Mode:"):
                stripped_prefix = re.sub(
                    r"^\[Mode:\s*[\w -]+\]\s*\n*",
                    "",
                    response_text,
                    count=1,
                ).strip()
                if stripped_prefix and stripped_prefix != response_text:
                    try:
                        response_data = json.loads(stripped_prefix)
                        phase1_text_for_history = response_text
                        logger.info(
                            "Phase 1 response contained mode prefix; extracted JSON payload"
                        )
                        break
                    except json.JSONDecodeError:
                        pass
            _log_json_parse_error(
                e,
                response_text,
                logger_func=logger.warning,
                base_message_prefix="Phase 1 response not valid JSON",
            )
            if attempt < max_attempts:
                logger.warning(
                    "Retrying Phase 1 after invalid JSON (%s/%s)",
                    attempt,
                    max_attempts,
                )
                continue
            return _attach_tool_execution_metadata(response_1, executed=False)

    if isinstance(response_data, list):
        tool_requests = response_data
    elif isinstance(response_data, dict):
        # Check multiple locations for tool_requests (models may nest them differently).
        # Priority order: top-level, then planning_block, then state_updates.
        tool_requests = response_data.get(tool_requests_key, [])
        if not tool_requests:
            # Check inside planning_block (Qwen sometimes nests tool_requests here)
            planning_block = response_data.get("planning_block", {})
            if isinstance(planning_block, dict):
                tool_requests = planning_block.get(tool_requests_key, [])
        if not tool_requests:
            # Check inside state_updates (another common nesting location)
            state_updates = response_data.get("state_updates", {})
            if isinstance(state_updates, dict):
                tool_requests = state_updates.get(tool_requests_key, [])
    else:
        logger.warning(
            "Phase 1 JSON parsed to unexpected type %s; returning Phase 1 result",
            type(response_data).__name__,
        )
        return _attach_tool_execution_metadata(response_1, executed=False)
    if not tool_requests:
        msg = (
            no_tool_requests_log_msg(response_data)
            if callable(no_tool_requests_log_msg)
            else no_tool_requests_log_msg
        )
        logger.info(msg)
        return _attach_tool_execution_metadata(response_1, executed=False)

    if not isinstance(tool_requests, list):
        logger.warning("tool_requests is not a list, returning Phase 1 result")
        return _attach_tool_execution_metadata(response_1, executed=False)

    logger.info(f"Executing {len(tool_requests)} tool request(s)")
    tool_results = execute_tool_requests_fn(tool_requests)
    if not tool_results:
        logger.warning("No valid tool results, returning Phase 1 result")
        return _attach_tool_execution_metadata(response_1, executed=False)

    # Update game_state with tool results before Phase 2 (bead csz)
    # Extract game_state from prompt_contents (first element is JSON string)
    updated_prompt_contents = list(prompt_contents)  # Copy to avoid mutating original
    if updated_prompt_contents and len(updated_prompt_contents) > 0:
        try:
            first_content = updated_prompt_contents[0]
            logger.debug(
                f"🏰 STATE_UPDATE_DEBUG: prompt_contents[0] type={type(first_content).__name__}, "
                f"is_str={isinstance(first_content, str)}, is_dict={isinstance(first_content, dict)}"
            )
            # Handle both JSON string and dict formats
            if isinstance(first_content, str):
                request_data = json.loads(first_content)
            elif isinstance(first_content, dict):
                request_data = first_content
            else:
                logger.warning(
                    f"🏰 STATE_UPDATE_SKIP: Unexpected prompt_contents[0] type: {type(first_content)}"
                )
                request_data = None

            if request_data:
                game_state = request_data.get("game_state")
                if isinstance(game_state, dict):
                    # Extract turn_number for timestamp tracking
                    faction_minigame = game_state.get("custom_campaign_state", {}).get(
                        "faction_minigame", {}
                    )
                    turn_number = (
                        faction_minigame.get("turn_number")
                        if isinstance(faction_minigame, dict)
                        else None
                    )

                    # Update game_state with tool results
                    updated_game_state = update_game_state_with_tool_results(
                        game_state,
                        tool_results,
                        turn_number=turn_number,
                    )

                    # Re-serialize updated request with new game_state
                    request_data["game_state"] = updated_game_state
                    # Preserve original format (string or dict)
                    if isinstance(first_content, str):
                        updated_prompt_contents[0] = json.dumps(request_data)
                    else:
                        updated_prompt_contents[0] = request_data

                    logger.info(
                        "🏰 STATE_UPDATE: Updated game_state in prompt_contents for Phase 2"
                    )
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            logger.warning(
                f"🏰 STATE_UPDATE_SKIP: Could not extract/update game_state: {e}"
            )

    tool_results_text = format_tool_results_text_fn(tool_results)
    tool_results_prompt = build_tool_results_prompt(tool_results_text)
    history = build_history_fn(
        prompt_contents=updated_prompt_contents,
        phase1_text=phase1_text_for_history,
        tool_results_prompt=tool_results_prompt,
    )

    response_2 = phase2_generate_fn(history)

    # Defensive: Some providers/models occasionally omit action_resolution dice even though tool results were injected.
    # If we executed any dice tools, retry Phase 2 once with an explicit action_resolution requirement to avoid
    # llm_service reprompting later without tool context.
    dice_tool_names = {
        "roll_dice",
        "roll_attack",
        "roll_skill_check",
        "roll_saving_throw",
    }
    executed_dice_tools = any(
        str((tr or {}).get("tool", "")) in dice_tool_names
        for tr in (tool_results or [])
    )

    if executed_dice_tools:
        response2_text = (extract_text_fn(response_2) or "").strip()
        candidate2 = response2_text

        # Check if Phase 2 response is valid JSON
        needs_retry = False
        retry_reason = ""
        try:
            response2_data = json.loads(candidate2) if candidate2 else {}
            # Check for missing action_resolution dice
            has_dice = False
            action_resolution = response2_data.get("action_resolution")
            if isinstance(action_resolution, dict):
                mechanics = action_resolution.get("mechanics", {})
                if isinstance(mechanics, dict):
                    rolls = mechanics.get("rolls", [])
                    audit_events = mechanics.get("audit_events", [])
                    has_dice = (isinstance(rolls, list) and len(rolls) > 0) or (
                        isinstance(audit_events, list) and len(audit_events) > 0
                    )
            if not has_dice:
                needs_retry = True
                retry_reason = "missing_dice_rolls"
        except json.JSONDecodeError:
            needs_retry = True
            retry_reason = "invalid_json"

        if needs_retry:
            # Build retry instructions based on reason
            if retry_reason == "invalid_json":
                retry_instructions = (
                    "CRITICAL: Your previous response was malformed JSON. "
                    "Return ONLY valid JSON with the complete NarrativeResponse schema. "
                    "Include dice in action_resolution.mechanics.rolls (or audit_events) using the exact results above. "
                    "Do NOT invent rolls or populate dice_rolls."
                )
            else:
                retry_instructions = (
                    "IMPORTANT: Your response MUST include dice in action_resolution.mechanics.rolls "
                    "(or action_resolution.mechanics.audit_events) using only the Tool results above. "
                    "Do NOT invent rolls or populate dice_rolls."
                )

            tool_results_prompt_retry = build_tool_results_prompt(
                tool_results_text,
                extra_instructions=retry_instructions,
            )
            history_retry = build_history_fn(
                prompt_contents=prompt_contents,
                phase1_text=phase1_text_for_history,
                tool_results_prompt=tool_results_prompt_retry,
            )
            retry_response = phase2_generate_fn(history_retry)
            return _attach_tool_execution_metadata(
                retry_response, executed=True, tool_results=tool_results
            )

    return _attach_tool_execution_metadata(
        response_2, executed=True, tool_results=tool_results
    )


def run_openai_native_two_phase_flow(
    *,
    generate_content_fn: Callable[..., Any],
    prompt_contents: list[Any],
    model_name: str,
    system_instruction_text: str | None,
    temperature: float,
    max_output_tokens: int,
    dice_roll_tools: list[dict],
    execute_tool_fn: Callable[[str, dict[str, Any]], dict],
    logger: _Logger,
) -> Any:
    """Run native tool calling (Phase 1 tools, Phase 2 JSON) for OpenAI-chat providers."""
    logger.info("NATIVE Phase 1: Calling with tools parameter")

    base_messages: list[dict[str, Any]] = []
    if system_instruction_text:
        base_messages.append({"role": "system", "content": system_instruction_text})
    base_messages.append(
        {"role": "user", "content": stringify_chat_parts(prompt_contents)}
    )

    response1 = generate_content_fn(
        prompt_contents=prompt_contents,
        model_name=model_name,
        system_instruction_text=system_instruction_text,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        tools=dice_roll_tools,
    )

    tool_calls = getattr(response1, "tool_calls", None)
    if not tool_calls:
        logger.info("NATIVE Phase 1: No tool_calls, proceeding to Phase 2 for JSON")

        phase2_messages = list(base_messages)
        if getattr(response1, "text", ""):
            phase2_messages.append({"role": "assistant", "content": response1.text})
            phase2_messages.append(
                {
                    "role": "user",
                    "content": "Now provide your response in the required JSON format.",
                }
            )

        phase2_response = generate_content_fn(
            prompt_contents=[],
            model_name=model_name,
            system_instruction_text=None,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            tools=None,
            messages=phase2_messages
            if getattr(response1, "text", "")
            else base_messages,
        )
        return _attach_tool_execution_metadata(phase2_response, executed=False)

    logger.info(f"NATIVE Phase 1: Executing {len(tool_calls)} tool call(s)")
    tool_results = execute_openai_tool_calls(
        tool_calls,
        execute_tool_fn=execute_tool_fn,
        logger=logger,
    )
    if not tool_results:
        logger.warning("NATIVE: No valid tool results, making JSON-only call")
        no_tools_response = generate_content_fn(
            prompt_contents=prompt_contents,
            model_name=model_name,
            system_instruction_text=system_instruction_text,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            tools=None,
        )
        return _attach_tool_execution_metadata(no_tools_response, executed=False)

    phase2_messages: list[dict[str, Any]] = list(base_messages)
    phase2_messages.append(
        {
            "role": "assistant",
            "content": "",  # Empty string for broader provider compatibility (vs None)
            "tool_calls": tool_calls,
        }
    )
    for result in tool_results:
        phase2_messages.append(
            {
                "role": "tool",
                "tool_call_id": result["tool_call_id"],
                "content": json.dumps(
                    _compact_tool_result_for_prompt(result["result"])
                ),
            }
        )
    phase2_messages.append(
        {
            "role": "user",
            "content": (
                "The dice rolls have been executed. Use these EXACT results in your narrative. "
                "Now provide the complete response in the required JSON format. "
                "Include the dice results in action_resolution.mechanics.rolls "
                "(or action_resolution.mechanics.audit_events). "
                "Do NOT populate dice_rolls."
            ),
        }
    )

    logger.info("NATIVE Phase 2: JSON call with tool results")
    final_response = generate_content_fn(
        prompt_contents=[],
        model_name=model_name,
        system_instruction_text=None,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        tools=None,
        messages=phase2_messages,
    )
    return _attach_tool_execution_metadata(
        final_response, executed=True, tool_results=tool_results
    )


def get_prompt_tool_context(prompt_contents: list[Any]) -> dict[str, Any]:
    """Build domain-tool context from prompt contents."""
    enabled, turn_number = (
        faction_state_util.extract_faction_minigame_state_from_prompt_contents(
            prompt_contents
        )
    )
    is_enabling = faction_state_util.is_faction_enable_action(prompt_contents)
    return {
        "enabled": enabled,
        "turn_number": turn_number,
        "is_enabling": is_enabling,
        "allow_domain_tools": enabled or is_enabling,
    }


def extract_json_payload_and_tool_requests(
    response_text: str,
) -> tuple[dict[str, Any], list[dict]]:
    """Parse top-level JSON payload and tool_requests array from response text."""
    try:
        parsed = json.loads(response_text) if response_text.strip() else {}
    except json.JSONDecodeError:
        return ({}, [])
    if isinstance(parsed, list):
        tool_requests = [item for item in parsed if isinstance(item, dict)]
        return ({}, tool_requests)
    if not isinstance(parsed, dict):
        return ({}, [])
    tool_requests = parsed.get("tool_requests", [])
    if not isinstance(tool_requests, list):
        tool_requests = []
    return (parsed, tool_requests)


def get_enable_turn_retry_instruction() -> str:
    """Instruction for enable-turn retry when tool_requests were omitted."""
    return (
        '\n\nCRITICAL: user_action is "enable_faction_minigame". '
        "You MUST include a tool_requests array that calls "
        "faction_calculate_power and faction_calculate_ranking. "
        "If you omit tool_requests, your response will be rejected.\n"
    )


def inject_tool_requests_if_missing(
    response: Any,
    *,
    expected_tool_requests: list[dict[str, Any]],
) -> None:
    """Ensure tool_requests are present in response JSON when required."""
    if not expected_tool_requests:
        return

    try:
        response_text = getattr(response, "text", "") or ""
    except Exception:
        response_text = ""
    try:
        parsed = json.loads(response_text) if response_text.strip() else {}
    except json.JSONDecodeError:
        return
    if not isinstance(parsed, dict):
        return

    existing = parsed.get("tool_requests")
    if isinstance(existing, list) and existing:
        return

    parsed["tool_requests"] = expected_tool_requests
    injected_text = json.dumps(parsed, ensure_ascii=False)

    try:
        response.text = injected_text
    except Exception as exc:
        logging_util.debug(
            "inject_tool_requests_if_missing: unable to set response.text: %s",
            exc,
        )
    try:
        candidates = getattr(response, "candidates", None) or []
        for candidate in candidates:
            content = getattr(candidate, "content", None)
            if not content:
                continue
            parts = getattr(content, "parts", None) or []
            for part in parts:
                if hasattr(part, "text"):
                    part.text = injected_text
                    break
    except Exception as exc:
        logging_util.debug(
            "inject_tool_requests_if_missing: unable to patch candidate parts: %s",
            exc,
        )


def _extract_minigame_data_from_response(
    response_data: dict[str, Any],
) -> dict[str, Any]:
    if not isinstance(response_data, dict):
        return {}
    state_updates = response_data.get("state_updates", {})
    if not isinstance(state_updates, dict):
        return {}
    custom_campaign_state = state_updates.get("custom_campaign_state", {})
    if not isinstance(custom_campaign_state, dict):
        return {}
    faction_minigame = custom_campaign_state.get("faction_minigame", {})
    if not isinstance(faction_minigame, dict):
        return {}
    return faction_minigame


def _has_required_minigame_init_data(minigame: dict[str, Any]) -> bool:
    if not isinstance(minigame, dict):
        return False
    units = minigame.get("units")
    resources = minigame.get("resources")
    buildings = minigame.get("buildings")
    if (
        not isinstance(units, dict)
        or not isinstance(resources, dict)
        or not isinstance(buildings, dict)
    ):
        return False
    required_units = ("soldiers", "spies", "elites", "elite_avg_level")
    required_resources = ("territory",)
    required_buildings = ("fortifications",)
    return (
        all(key in units for key in required_units)
        and all(key in resources for key in required_resources)
        and all(key in buildings for key in required_buildings)
    )


def _extract_and_execute_domain_tools_from_stdout(stdout: str) -> list[dict]:
    if not stdout:
        return []
    results = []
    for line in stdout.split("\n"):
        stripped = line.strip()
        if not stripped or not stripped.startswith("{"):
            continue
        try:
            parsed = json.loads(stripped)
            if "__faction_tool__" not in parsed:
                continue
            tool_name = parsed["__faction_tool__"]
            if not isinstance(tool_name, str) or tool_name not in FACTION_TOOL_NAMES:
                logging_util.warning(
                    "HYBRID_TOOL: Ignoring non-allowlisted tool from stdout: %r",
                    tool_name,
                )
                continue
            args = parsed.get("args", {})
            result = execute_faction_tool(tool_name, args)
            results.append({"tool": tool_name, "args": args, "result": result})
        except json.JSONDecodeError:
            continue
        except Exception as e:
            logging_util.warning("HYBRID_TOOL: Error processing line: %s", e)
            continue
    return results


def update_prompt_contents_with_tool_results(  # noqa: PLR0911, PLR0912
    prompt_contents: list[Any],
    tool_results: list[dict],
) -> list[Any]:
    """Apply tool results to request game_state in prompt_contents for Phase 2."""
    updated_prompt_contents = list(prompt_contents)
    if not updated_prompt_contents:
        return updated_prompt_contents

    try:
        first_content = updated_prompt_contents[0]
        request_data = None
        is_content_object = False

        if isinstance(first_content, str):
            request_data = json.loads(first_content)
        elif isinstance(first_content, dict):
            request_data = first_content
        elif hasattr(first_content, "parts") and hasattr(first_content, "role"):
            is_content_object = True
            parts = getattr(first_content, "parts", [])
            if parts and len(parts) > 0:
                first_part = parts[0]
                if hasattr(first_part, "text") and first_part.text:
                    try:
                        request_data = json.loads(first_part.text)
                    except json.JSONDecodeError:
                        return updated_prompt_contents
        else:
            return updated_prompt_contents

        if not isinstance(request_data, dict):
            return updated_prompt_contents
        game_state = request_data.get("game_state")
        if not isinstance(game_state, dict):
            return updated_prompt_contents

        faction_minigame = game_state.get("custom_campaign_state", {}).get(
            "faction_minigame", {}
        )
        turn_number = (
            faction_minigame.get("turn_number")
            if isinstance(faction_minigame, dict)
            else None
        )
        updated_game_state = update_game_state_with_tool_results(
            game_state,
            tool_results,
            turn_number=turn_number,
        )
        request_data["game_state"] = updated_game_state

        if is_content_object:
            first_content.parts[0].text = json.dumps(request_data)
            updated_prompt_contents[0] = first_content
        elif isinstance(first_content, str):
            updated_prompt_contents[0] = json.dumps(request_data)
        else:
            updated_prompt_contents[0] = request_data
    except (json.JSONDecodeError, KeyError, TypeError, AttributeError):
        return updated_prompt_contents

    return updated_prompt_contents


def execute_gemini_code_execution_tool_orchestration(  # noqa: PLR0912, PLR0915
    *,
    prompt_contents: list[Any],
    response_1: Any,
    response_data: dict[str, Any],
    json_tool_requests: list[dict],
    context: dict[str, Any],
    execute_tool_requests_fn: Callable[[list[dict]], list[dict]],
) -> list[dict]:
    """Execute domain tools + dice fallback for Gemini code_execution flow."""
    all_tool_results: list[dict] = []
    allow_domain_tools = bool(context.get("allow_domain_tools"))
    turn_number = int(context.get("turn_number", 1) or 1)

    code_exec_evidence = gemini_code_execution.extract_code_execution_evidence(
        response_1
    )
    stdout = code_exec_evidence.get("stdout", "")

    if allow_domain_tools:
        all_tool_results.extend(_extract_and_execute_domain_tools_from_stdout(stdout))
    elif stdout and "__faction_tool__" in stdout:
        logging_util.warning(
            "Gemini code_execution: Domain tool markers found in stdout but disabled"
        )

    dropped_dice_requests: list[dict] = []
    json_tool_results: list[dict] = []
    if json_tool_requests and allow_domain_tools:
        domain_only_requests: list[dict] = []
        for req in json_tool_requests:
            if not isinstance(req, dict):
                continue
            tool_name = req.get("tool")
            args = req.get("args", {}) if isinstance(req.get("args", {}), dict) else {}
            if isinstance(tool_name, str) and tool_name in FACTION_TOOL_NAMES:
                if tool_name == "faction_calculate_ranking":
                    if "player_faction_power" not in args:
                        if "faction_power" in args:
                            args["player_faction_power"] = args.pop("faction_power")
                        else:
                            inferred_fp = (
                                response_data.get("state_updates", {})
                                .get("custom_campaign_state", {})
                                .get("faction_minigame", {})
                                .get("faction_power")
                            )
                            if inferred_fp is not None:
                                args["player_faction_power"] = inferred_fp
                    if "turn_number" not in args:
                        args["turn_number"] = turn_number
                    if "player_faction_power" not in args:
                        continue
                req["args"] = args
                domain_only_requests.append(req)
            elif tool_name in (
                "roll_dice",
                "roll_attack",
                "roll_skill_check",
                "roll_saving_throw",
            ):
                dropped_dice_requests.append(req)

        power_result = None
        for req in domain_only_requests:
            if req.get("tool") == "faction_calculate_power":
                power_args = req.get("args", {})
                try:
                    candidate = execute_faction_tool(
                        "faction_calculate_power", power_args
                    )
                except Exception as e:
                    logging_util.error(
                        "Gemini code_execution: faction_calculate_power failed: %s", e
                    )
                    candidate = {"error": str(e)}
                power_result = candidate
                if not (isinstance(candidate, dict) and "error" in candidate):
                    break

        for req in domain_only_requests:
            tool_name = req.get("tool")
            args = req.get("args", {}) if isinstance(req.get("args", {}), dict) else {}
            if tool_name == "faction_calculate_power":
                result = (
                    power_result
                    if power_result is not None
                    else {"error": "Missing faction_calculate_power result"}
                )
                json_tool_results.append(
                    {"tool": tool_name, "args": args, "result": result}
                )
                continue

            if tool_name == "faction_calculate_ranking":
                power_has_error = (
                    isinstance(power_result, dict) and "error" in power_result
                )
                if power_result is None or power_has_error:
                    continue
                fp_value = power_result.get("faction_power")
                if fp_value is not None:
                    try:
                        fp_value = int(fp_value)
                    except (TypeError, ValueError):
                        logging_util.debug(
                            "Gemini code_execution: unable to coerce faction_power to int: %r",
                            fp_value,
                        )
                    args = dict(args)
                    args["player_faction_power"] = fp_value
            try:
                result = execute_faction_tool(tool_name, args)
            except Exception as e:
                logging_util.error("Gemini code_execution: %s failed: %s", tool_name, e)
                result = {"error": str(e)}
            json_tool_results.append(
                {"tool": tool_name, "args": args, "result": result}
            )
    elif json_tool_requests:
        for req in json_tool_requests:
            if not isinstance(req, dict):
                continue
            tool_name = req.get("tool")
            if isinstance(tool_name, str) and tool_name in (
                "roll_dice",
                "roll_attack",
                "roll_skill_check",
                "roll_saving_throw",
            ):
                dropped_dice_requests.append(req)

    all_tool_results.extend(json_tool_results)

    code_exec_used = code_exec_evidence.get("code_execution_used", False)
    code_has_rng = code_exec_evidence.get("code_contains_rng", False)
    if dropped_dice_requests and not (code_exec_used and code_has_rng):
        dice_fallback_results = execute_tool_requests_fn(dropped_dice_requests)
        for fallback_result in dice_fallback_results:
            fallback_result["_fallback"] = True
            all_tool_results.append(fallback_result)

    auto_power_fp: int | None = None
    if allow_domain_tools:
        has_power = any(
            isinstance(tr, dict) and tr.get("tool") == "faction_calculate_power"
            for tr in all_tool_results
        )
        if not has_power:
            explicit_fp = (
                response_data.get("state_updates", {})
                .get("custom_campaign_state", {})
                .get("faction_minigame", {})
                .get("faction_power")
            )
            try:
                inferred_minigame = _extract_minigame_data_from_response(response_data)
                if inferred_minigame and _has_required_minigame_init_data(
                    inferred_minigame
                ):
                    units = inferred_minigame.get("units", {})
                    resources = inferred_minigame.get("resources", {})
                    buildings = inferred_minigame.get("buildings", {})
                else:
                    first_content = prompt_contents[0] if prompt_contents else None
                    if isinstance(first_content, str):
                        payload = json.loads(first_content)
                    elif isinstance(first_content, dict):
                        payload = first_content
                    else:
                        payload = {}
                    game_state = payload.get("game_state", {})
                    faction_minigame = game_state.get("custom_campaign_state", {}).get(
                        "faction_minigame", {}
                    )
                    if not _has_required_minigame_init_data(faction_minigame):
                        raise ValueError("Missing required minigame init data")
                    units = faction_minigame.get("units", {})
                    resources = faction_minigame.get("resources", {})
                    buildings = faction_minigame.get("buildings", {})

                soldiers = int(units.get("soldiers", 0) or 0)
                spies = int(units.get("spies", 0) or 0)
                elites = int(units.get("elites", 0) or 0)
                elite_level = float(units.get("elite_avg_level", 6.0) or 6.0)
                territory = int(resources.get("territory", 0) or 0)
                forts = int(buildings.get("fortifications", 0) or 0)

                has_unit_data = (
                    soldiers > 0
                    or spies > 0
                    or elites > 0
                    or territory > 0
                    or forts > 0
                )
                if explicit_fp is not None and not has_unit_data:
                    auto_power_fp = int(explicit_fp)
                else:
                    try:
                        power_result = execute_faction_tool(
                            "faction_calculate_power",
                            {
                                "soldiers": soldiers,
                                "spies": spies,
                                "elites": elites,
                                "elite_avg_level": elite_level,
                                "territory": territory,
                                "fortifications": forts,
                            },
                        )
                    except Exception as exc:
                        logging_util.error(
                            "Gemini code_execution: auto-infer faction_calculate_power failed: %s",
                            exc,
                        )
                        power_result = {"error": str(exc)}
                    auto_power_fp = (
                        power_result.get("faction_power")
                        if isinstance(power_result, dict)
                        and "error" not in power_result
                        else None
                    )
                    all_tool_results.insert(
                        0,
                        {
                            "tool": "faction_calculate_power",
                            "args": {
                                "soldiers": soldiers,
                                "spies": spies,
                                "elites": elites,
                                "elite_avg_level": elite_level,
                                "territory": territory,
                                "fortifications": forts,
                            },
                            "result": power_result,
                        },
                    )
            except (
                json.JSONDecodeError,
                KeyError,
                TypeError,
                ValueError,
                AttributeError,
            ) as exc:
                logging_util.debug(
                    "Gemini code_execution: unable to auto-infer faction_calculate_power args: %s",
                    exc,
                )

        authoritative_fp: int | None = None
        for tr in all_tool_results:
            if not isinstance(tr, dict) or tr.get("tool") != "faction_calculate_power":
                continue
            result = tr.get("result", {})
            if isinstance(result, dict):
                if "error" in result:
                    continue
                try:
                    authoritative_fp = int(result.get("faction_power", 0))
                except (TypeError, ValueError):
                    logging_util.debug(
                        "Gemini code_execution: invalid faction_power in tool result: %r",
                        result.get("faction_power"),
                    )
                break

        if authoritative_fp is None and auto_power_fp is not None:
            authoritative_fp = auto_power_fp

        if authoritative_fp is not None:
            existing_ranking_idx: int | None = None
            existing_ranking_fp: int | None = None
            for idx, tr in enumerate(all_tool_results):
                if (
                    isinstance(tr, dict)
                    and tr.get("tool") == "faction_calculate_ranking"
                ):
                    existing_ranking_idx = idx
                    args = tr.get("args", {})
                    if isinstance(args, dict):
                        try:
                            existing_ranking_fp = int(
                                args.get("player_faction_power", 0)
                            )
                        except (TypeError, ValueError):
                            existing_ranking_fp = 0
                    break

            needs_ranking_compute = False
            if existing_ranking_idx is None:
                needs_ranking_compute = True
            elif existing_ranking_fp != authoritative_fp:
                needs_ranking_compute = True
                all_tool_results.pop(existing_ranking_idx)

            if needs_ranking_compute:
                ranking_args = {
                    "player_faction_power": authoritative_fp,
                    "turn_number": turn_number,
                }
                try:
                    ranking_result = execute_faction_tool(
                        "faction_calculate_ranking",
                        ranking_args,
                    )
                except Exception as e:
                    logging_util.error(
                        "Gemini code_execution: faction_calculate_ranking failed: %s",
                        e,
                    )
                    ranking_result = {"error": str(e)}
                all_tool_results.append(
                    {
                        "tool": "faction_calculate_ranking",
                        "args": ranking_args,
                        "result": ranking_result,
                    }
                )

    return all_tool_results


def build_domain_tool_request_enforcement(
    *,
    allow_domain_tools: bool,
    tool_results: list[dict],
    turn_number: int,
) -> tuple[str, list[dict[str, Any]]]:
    """Build enforcement instructions and expected tool_requests for phase 2."""
    if not allow_domain_tools:
        return ("", [])

    expected_tool_requests = faction_state_util.build_expected_faction_tool_requests(
        tool_results, turn_number
    )
    extra_instructions = (
        "OVERRIDE PREVIOUS INSTRUCTION about tool_requests: For faction minigame turns, "
        "you MUST include a tool_requests array in your JSON response that mirrors the "
        "faction tool calls executed above. Use the SAME args shown in Tool results. "
        "Do NOT invent new tool calls.\n"
    )
    if expected_tool_requests:
        extra_instructions += (
            "Use EXACTLY this tool_requests array (copy verbatim):\n"
            f"{json.dumps(expected_tool_requests, ensure_ascii=False)}\n"
        )
    return (extra_instructions, expected_tool_requests)


class ContextTooLargeError(ValueError):
    """Raised when the prompt context is too large for meaningful output.

    This exception indicates that the API returned a response but was unable
    to generate content due to context limitations (e.g., finish_reason='length'
    with minimal completion tokens).
    """

    def __init__(
        self,
        message: str,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        finish_reason: str | None = None,
    ):
        super().__init__(message)
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.finish_reason = finish_reason


def check_context_too_large(
    finish_reason: str | None,
    completion_tokens: int,
    prompt_tokens: int,
    has_content: bool,
) -> None:
    """Check if API response indicates context was too large for meaningful output.

    Raises ContextTooLargeError if the response suggests the prompt consumed
    too much of the context window, leaving insufficient room for output.

    Args:
        finish_reason: The API's finish reason (e.g., 'stop', 'length')
        completion_tokens: Number of tokens generated in the response
        prompt_tokens: Number of tokens in the prompt
        has_content: Whether the response contains actual content

    Raises:
        ContextTooLargeError: If finish_reason='length' and no meaningful content
    """
    if finish_reason == "length" and completion_tokens <= 1 and not has_content:
        raise ContextTooLargeError(
            f"Context too large: prompt used {prompt_tokens:,} tokens, "
            f"model could only generate {completion_tokens} completion token(s). "
            "The prompt must be reduced to allow room for output.",
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            finish_reason=finish_reason,
        )

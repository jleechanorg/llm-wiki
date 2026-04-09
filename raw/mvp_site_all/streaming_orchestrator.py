"""Streaming orchestrator for real-time LLM response streaming.

This module provides SSE (Server-Sent Events) streaming for LLM responses,
enabling users to see response chunks as they are generated.

Architecture:
- StreamEvent: Data class for SSE events
- stream_narrative_simple: Basic streaming without game state
- stream_story_with_game_state: Full streaming with real game logic integration
- Handles two-phase generation (tools + narrative) with streaming Phase 2
"""

from __future__ import annotations

import copy
import importlib
import importlib.util
import sys
import time
from collections.abc import Generator
from typing import Any

from mvp_site import constants, logging_util
from mvp_site.game_state import GameState
from mvp_site.narrative_response_schema import (
    JSON_PARSE_FALLBACK_MARKER,
    parse_structured_response,
)
from mvp_site.session_header_utils import generate_session_header_fallback
from mvp_site.stream_events import StreamEvent


def _lazy_module(name: str):
    """Return a lazy module proxy; body executes on first attribute access.

    Cloud Run cold-start optimization: google.genai (via gemini_provider, ~840ms)
    and google.cloud.firestore (via firestore_service, ~500ms) add ~1.5s to cold
    start. LazyLoader keeps module references at module level per CLAUDE.md
    conventions while deferring the body to first use. If the module is already
    loaded (e.g., in test environments), the cached module is returned unchanged.
    """
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.find_spec(name)
    loader = importlib.util.LazyLoader(spec.loader)
    spec.loader = loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    loader.exec_module(module)
    return module


# Cold-start: defer google.genai and google.cloud.firestore loading.
# These loads happen on the first streaming request, not at server startup.
firestore_service = _lazy_module("mvp_site.firestore_service")
gemini_provider = _lazy_module("mvp_site.llm_providers.gemini_provider")
llm_service = _lazy_module("mvp_site.llm_service")
world_logic = _lazy_module("mvp_site.world_logic")


def warm_lazy_dependencies() -> dict[str, bool]:
    """Force-load streaming lazy modules during app startup warmup."""
    warmup_targets = (
        ("firestore_service", firestore_service, "get_campaign_by_id"),
        ("gemini_provider", gemini_provider, "generate_content_stream_sync"),
        ("llm_service", llm_service, "continue_story_streaming"),
    )
    warmup_status: dict[str, bool] = {}

    for module_name, module_obj, attr_name in warmup_targets:
        try:
            getattr(module_obj, attr_name)
            warmup_status[module_name] = True
        except Exception:
            warmup_status[module_name] = False
            logging_util.exception(
                "Streaming lazy-module warmup failed: %s.%s",
                module_name,
                attr_name,
            )

    return warmup_status


def continue_story_streaming(**kwargs):
    """Passthrough wrapper for patchable streaming call sites in tests."""
    return llm_service.continue_story_streaming(**kwargs)


def _enrich_streaming_structured_fields(
    structured_fields: dict[str, Any],
    *,
    updated_state_dict: dict[str, Any],
    story_context: list[dict[str, Any]] | None,
) -> None:
    """Extract living world data and add sequence metadata to streaming structured_fields.

    Mirrors the non-streaming path in world_logic.process_action_unified:
    1. Extracts world_events from state_updates (including custom_campaign_state nesting)
    2. Normalizes append-syntax world_events for UI consumers
    3. Annotates with turn/scene numbers
    4. Backfills from game state when LLM omits world_events
    5. Adds sequence_id and user_scene_number
    """
    # Compute sequence_id and user_scene_number (same as non-streaming)
    ctx = story_context or []
    sequence_id = len(ctx) + 2
    user_scene_number = (
        sum(
            1
            for entry in ctx
            if isinstance(entry, dict)
            and str(entry.get("actor", "")).lower() == constants.ACTOR_GEMINI.lower()
        )
        + 1
    )
    structured_fields["sequence_id"] = sequence_id
    structured_fields["user_scene_number"] = user_scene_number

    # Extract world_events — prefer top-level, fall back to state_updates
    # (mirrors non-streaming path in world_logic.process_action_unified)
    state_updates = structured_fields.get("state_updates")
    if "world_events" not in structured_fields:  # noqa: SIM102
        if isinstance(state_updates, dict):
            world_events = state_updates.get("world_events")
            if "world_events" not in state_updates or not isinstance(
                world_events, dict
            ):
                custom_state = state_updates.get("custom_campaign_state", {})
                if isinstance(custom_state, dict):
                    world_events = custom_state.get("world_events")
            if isinstance(world_events, dict):
                structured_fields["world_events"] = world_events

    # Normalize and annotate world_events
    player_turn = updated_state_dict.get("turn_number") or updated_state_dict.get(
        "player_turn"
    )
    llm_world_events = structured_fields.get("world_events")
    if llm_world_events and isinstance(llm_world_events, dict):
        llm_world_events = world_logic.normalize_world_events_for_story_payload(
            llm_world_events
        )
        world_logic.annotate_world_events_with_turn_scene(
            {"world_events": llm_world_events},
            player_turn or 0,
            scene_number=user_scene_number,
        )
        structured_fields["world_events"] = llm_world_events
        if not isinstance(state_updates, dict):
            state_updates = {}
            structured_fields["state_updates"] = state_updates
        state_updates["world_events"] = copy.deepcopy(llm_world_events)

    # Backfill from game state when LLM omits world_events
    if isinstance(user_scene_number, int):
        world_logic._try_backfill_story_entry_world_events(
            structured_fields,
            updated_game_state_dict=updated_state_dict,
            player_turn=player_turn,
            user_scene_number=user_scene_number,
        )

    # Filter to current scene only (prevent cumulative history bleed)
    world_events_for_entry = structured_fields.get("world_events")
    if isinstance(world_events_for_entry, dict) and isinstance(user_scene_number, int):
        filtered = world_logic._filter_story_entry_world_events_to_scene(
            world_events_for_entry,
            user_scene_number,
            current_turn=player_turn,
        )
        if isinstance(filtered, dict):
            # filtered is already a deep copy from _filter_story_entry_world_events_to_scene (line 391 in world_logic.py)
            # Assign directly to structured_fields, then deep copy for state_updates
            structured_fields["world_events"] = filtered
            # Also update state_updates to prevent cumulative history bleed (matches non-streaming path)
            state_updates = structured_fields.get("state_updates")
            if not isinstance(state_updates, dict):
                state_updates = {}
                structured_fields["state_updates"] = state_updates
            state_updates["world_events"] = copy.deepcopy(filtered)


_LW_REQUIRED_FIELDS = frozenset(
    {
        "actor",
        "action",
        "location",
        "outcome",
        "event_type",
        "status",
        "discovery_condition",
    }
)


def _count_compliant_lw_events(background_events: list) -> int:
    """Count background_events that contain all required LW fields.

    An event is compliant when it is a dict with all fields in _LW_REQUIRED_FIELDS
    present (value may be empty string — presence of the key is what matters).
    """
    count = 0
    for event in background_events:
        if not isinstance(event, dict):
            continue
        if all(field in event for field in _LW_REQUIRED_FIELDS):
            count += 1
    return count


def _warn_if_living_world_missing(
    *,
    updated_state_dict: dict[str, Any],
    structured_fields: dict[str, Any] | None,
    state_updates: dict[str, Any] | None,
    is_god_mode: bool,
    agent_mode: str | None,
    mode: str,
    should_freeze_time: bool = False,
) -> str | None:
    """Warn when living world events are missing on turns where they should fire.

    Living world instruction fires every turn (build_living_world_instruction always
    returns content for turn >= 1). This function checks whether the LLM actually
    produced world_events and emits a warning if not, to aid debugging.

    Returns a warning message string when a warning is emitted, or None otherwise.
    The caller may include the returned string in the SSE done event's warnings field.
    """
    effective_mode = agent_mode or mode
    turn_number = (
        updated_state_dict.get("turn_number")
        or updated_state_dict.get("player_turn")
        or 0
    )
    skip = (
        should_freeze_time
        or is_god_mode
        or agent_mode == constants.MODE_THINK
        or not world_logic.mode_advances_time(effective_mode)
        or not isinstance(turn_number, int)
        or turn_number < 1
    )
    if skip:
        return None

    # Check for world_events in structured_fields, state_updates, or game state
    sf_we = (
        structured_fields.get("world_events")
        if isinstance(structured_fields, dict)
        else None
    )
    su_we = (
        state_updates.get("world_events") if isinstance(state_updates, dict) else None
    )

    has_world_events = (
        isinstance(sf_we, dict) and sf_we or isinstance(su_we, dict) and su_we
    )

    if not has_world_events:
        msg = (
            f"LIVING_WORLD_MISSING: world_events absent on turn {turn_number} "
            f"(mode={mode} agent_mode={agent_mode}). Living world instruction fires every turn"
            " — LLM did not include state_updates.world_events. "
            "Check narrative_response_schema and living_world_instruction.md."
        )
        logging_util.warning("🌍 %s", msg)
        return msg
    # Check for non-standard schema (no background_events key)
    we = sf_we or su_we
    if isinstance(we, dict) and "background_events" not in we:
        msg = (
            f"LIVING_WORLD_SCHEMA: world_events present on turn {turn_number} but missing "
            f"'background_events' key. Got keys: {list(we.keys())}. "
            "LLM may be using a non-standard schema."
        )
        logging_util.warning("🌍 %s", msg)
        return msg
    if isinstance(we, dict) and "background_events" in we:
        background_events = we["background_events"]
        if not isinstance(background_events, list):
            msg = (
                f"LIVING_WORLD_SCHEMA: background_events on turn {turn_number} is not a list "
                f"(got {type(background_events).__name__}). "
                "Append-style or object payloads bypass compliance scoring."
            )
            logging_util.warning("🌍 %s", msg)
            return msg
        compliant_count = _count_compliant_lw_events(background_events)
        if compliant_count < 2:
            msg = (
                f"LIVING_WORLD_COMPLIANCE: world_events on turn {turn_number} has only "
                f"{compliant_count} compliant background_events (need >= 2). "
                f"Each event must include all required fields: {_LW_REQUIRED_FIELDS}. "
                "Check living_world_instruction.md and narrative_response_schema."
            )
            logging_util.warning("🌍 %s", msg)
            return msg
    return None


def _extract_header_value(session_header: str, key: str) -> str | None:
    """Extract `Key: value` from normalized session header text."""
    prefix = f"{key}:"
    for raw_line in session_header.splitlines():
        line = raw_line.strip()
        if not line.startswith(prefix):
            continue
        value = line[len(prefix) :].strip()
        return value or None
    return None


def _build_early_metadata_payload(current_game_state: GameState) -> dict[str, Any]:
    """Build best-effort early metadata so frontend can render pre-sections early."""
    session_header = generate_session_header_fallback(current_game_state)
    payload: dict[str, Any] = {}
    if session_header:
        payload["session_header"] = session_header
    location = (
        _extract_header_value(session_header, "Location") if session_header else None
    )
    if location and location != "Unknown":
        payload["location_confirmed"] = location
    resources = (
        _extract_header_value(session_header, "Resources") if session_header else None
    )
    if resources:
        payload["resources"] = resources
    return payload


def _extract_god_mode_response_text(structured: Any) -> str | None:
    """Extract non-empty god_mode_response from dict or object payloads."""
    god_mode_text: str | None = None
    if isinstance(structured, dict):
        raw = structured.get("god_mode_response")
        if isinstance(raw, str):
            god_mode_text = raw
    elif structured is not None and hasattr(structured, "god_mode_response"):
        raw = getattr(structured, "god_mode_response", None)
        if isinstance(raw, str):
            god_mode_text = raw
    if isinstance(god_mode_text, str) and god_mode_text.strip():
        return god_mode_text
    return None


def stream_narrative_simple(
    prompt_text: str,
    model_name: str = "gemini-2.5-flash",
    system_instruction: str | None = None,
    temperature: float = 0.7,
    max_output_tokens: int = 4096,
) -> Generator[StreamEvent, None, None]:
    """Simple streaming for narrative text without structured output.

    This is a simplified streaming flow for cases where you just need
    raw text streaming without JSON parsing or tool execution.

    Args:
        prompt_text: The prompt to send to the LLM
        model_name: Model to use for generation
        system_instruction: Optional system instruction
        temperature: Sampling temperature
        max_output_tokens: Maximum output tokens

    Yields:
        StreamEvent objects for each chunk and completion
    """
    full_text_parts: list[str] = []
    sequence = 0

    try:
        logging_util.info(f"Starting simple streaming with model {model_name}")

        for chunk in gemini_provider.generate_content_stream_sync(
            prompt_contents=[prompt_text],
            model_name=model_name,
            system_instruction_text=system_instruction,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        ):
            full_text_parts.append(chunk)
            yield StreamEvent(
                type="chunk",
                payload={"text": chunk, "sequence": sequence},
            )
            sequence += 1

        # Emit done event with complete text
        full_text = "".join(full_text_parts)
        yield StreamEvent(
            type="done",
            payload={
                "full_narrative": full_text,
                "chunk_count": sequence,
            },
        )

    except Exception:
        logging_util.exception("Streaming error during simple narrative generation")
        yield StreamEvent(
            type="error",
            payload={
                "message": "An unexpected error occurred while streaming the response.",
                "partial_text": "".join(full_text_parts),
            },
        )


def stream_with_context(
    user_input: str,
    story_context: list[dict[str, Any]],
    model_name: str = "gemini-2.5-flash",
    system_instruction: str | None = None,
    temperature: float = 0.7,
    max_output_tokens: int = 4096,
) -> Generator[StreamEvent, None, None]:
    """Stream narrative with story context history.

    Builds a prompt from the story context and user input, then streams
    the response. This is suitable for interactive story continuation.

    Args:
        user_input: Current user action/input
        story_context: List of previous story entries with actor/text
        model_name: Model to use
        system_instruction: Optional system instruction
        temperature: Sampling temperature
        max_output_tokens: Maximum output tokens

    Yields:
        StreamEvent objects
    """
    # Build conversation history for the prompt
    prompt_parts = []

    # Add context from story history (last N entries for token management)
    max_context_entries = 10
    recent_context = story_context[-max_context_entries:] if story_context else []

    for entry in recent_context:
        if not isinstance(entry, dict):
            continue
        actor = entry.get("actor", "unknown")
        text = entry.get("text", "")
        if actor == "user":
            prompt_parts.append(f"Player: {text}")
        elif actor == "gemini":
            prompt_parts.append(f"Story: {text}")

    # Add current user input
    prompt_parts.append(f"Player: {user_input}")
    prompt_parts.append("Story:")

    prompt_text = "\n\n".join(prompt_parts)

    # Stream the response
    yield from stream_narrative_simple(
        prompt_text=prompt_text,
        model_name=model_name,
        system_instruction=system_instruction,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
    )


def create_sse_response_headers() -> dict[str, str]:
    """Create headers for SSE response.

    Returns:
        Dictionary of headers for Server-Sent Events
    """
    return {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "X-Accel-Buffering": "no",  # Disable nginx buffering
    }


def stream_events_generator(
    events: Generator[StreamEvent, None, None],
) -> Generator[str, None, None]:
    """Convert StreamEvent generator to SSE string generator.

    This is a utility for Flask's Response stream_with_context.

    Args:
        events: Generator of StreamEvent objects

    Yields:
        SSE-formatted strings
    """
    for event in events:
        yield event.to_sse()


def stream_story_with_game_state(  # noqa: PLR0912, PLR0915
    user_id: str,
    campaign_id: str,
    user_input: str,
    mode: str = "character",
) -> Generator[StreamEvent, None, None]:
    """Stream story continuation with full game state integration.

    This is the production streaming flow that uses the SAME logic as
    llm_service.continue_story, including:
    1. Same provider/model selection
    2. Same agent selection and system instructions
    3. Same LLMRequest building with budget allocation
    4. Same story context truncation

    The only difference is that responses are streamed instead of returned
    as a complete response.

    Args:
        user_id: User ID for authentication
        campaign_id: Campaign ID to continue
        user_input: User's action/input
        mode: Interaction mode (character, story, god, etc.)

    Yields:
        StreamEvent objects for chunks, tools, state, and completion
    """
    full_narrative: str | None = None
    raw_response_text: str | None = None
    structured_fields: dict[str, Any] | None = None
    state_updates: dict[str, Any] | None = None

    try:
        t0 = time.perf_counter()
        logging_util.info(
            f"Stream story starting: user_id={user_id}, campaign_id={campaign_id}"
        )

        # Load campaign data and story context
        campaign_data, story_context = firestore_service.get_campaign_by_id(
            user_id, campaign_id
        )
        t1 = time.perf_counter()
        logging_util.info("⏱️ STREAM_TIMING | get_campaign_by_id: %.3fs", t1 - t0)

        if not campaign_data:
            yield StreamEvent(
                type="error",
                payload={"message": "Campaign not found"},
            )
            return

        story_context = story_context or []

        # Load game state
        game_state_obj = firestore_service.get_campaign_game_state(user_id, campaign_id)
        t2 = time.perf_counter()
        logging_util.info("⏱️ STREAM_TIMING | get_campaign_game_state: %.3fs", t2 - t1)
        if isinstance(game_state_obj, GameState):
            current_game_state = game_state_obj
        elif isinstance(game_state_obj, dict):
            current_game_state = GameState.from_dict(game_state_obj)
        else:
            current_game_state = GameState.from_dict({})

        # Get user settings
        user_settings = firestore_service.get_user_settings(user_id)
        t3 = time.perf_counter()
        logging_util.info("⏱️ STREAM_TIMING | get_user_settings: %.3fs", t3 - t2)
        if user_settings and "debug_mode" in user_settings:
            current_game_state.debug_mode = user_settings["debug_mode"]

        # Get campaign configuration
        selected_prompts = campaign_data.get("selected_prompts", [])
        use_default_world = campaign_data.get("use_default_world", False)

        logging_util.info(
            "⏱️ STREAM_TIMING | total_firestore_reads: %.3fs | story_entries=%d",
            t3 - t0,
            len(story_context),
        )

        early_metadata = _build_early_metadata_payload(current_game_state)
        if early_metadata:
            yield StreamEvent(type="metadata", payload=early_metadata)

        # Use the REAL continue_story_streaming from llm_service
        # This uses the SAME logic as continue_story
        for event in continue_story_streaming(
            user_input=user_input,
            mode=mode,
            story_context=story_context,
            current_game_state=current_game_state,
            selected_prompts=selected_prompts,
            use_default_world=use_default_world,
            user_id=user_id,
            campaign_id=campaign_id,
        ):
            if event.type != "done":
                yield event
                continue

            # === DONE EVENT: PERSIST BEFORE YIELDING ===
            # All Firestore writes MUST complete before yielding done.
            # Once the client receives done it may close the connection,
            # and GeneratorExit would kill any code after yield.
            full_narrative = event.payload.get("full_narrative")
            raw_response_text = event.payload.get("raw_response_text")
            done_state_updates = event.payload.get("state_updates")
            state_updates = (
                done_state_updates if isinstance(done_state_updates, dict) else None
            )
            done_structured_response = event.payload.get("structured_response")
            if isinstance(done_structured_response, dict):
                structured_fields = done_structured_response

            # Collect warnings from persistence to yield after done
            persistence_warnings: list[StreamEvent] = []
            # Living world warnings to include in the done event's warnings field
            living_world_warnings: list[str] = []
            updated_state_dict: dict[str, Any] = {}

            # Persist game state updates (planning_block, HP changes, etc.)
            try:
                state_dirty = False
                updated_state_dict = (
                    current_game_state.to_dict()
                    if isinstance(current_game_state, GameState)
                    else {}
                )
                if state_updates:
                    updated_state_dict = firestore_service.update_state_with_changes(
                        updated_state_dict, state_updates
                    )
                    state_dirty = True

                if structured_fields and structured_fields.get("planning_block"):
                    updated_state_dict["planning_block"] = structured_fields[
                        "planning_block"
                    ]
                    state_dirty = True

                # Determine agent mode for living world tracking
                agent_mode_used = event.payload.get("agent_mode")
                is_god_mode_turn = constants.MODE_GOD in (mode, agent_mode_used)

                # Compute should_freeze_time to mirror non-streaming path logic
                is_think_mode = agent_mode_used == constants.MODE_THINK
                is_character_creation_mode = (
                    agent_mode_used == constants.MODE_CHARACTER_CREATION
                )
                is_level_up_mode = agent_mode_used == constants.MODE_LEVEL_UP
                is_freeze_time_choice = (
                    world_logic._should_freeze_time_for_selected_choice(
                        user_input, story_context
                    )
                )
                should_freeze_time = (
                    is_think_mode
                    or is_freeze_time_choice
                    or is_character_creation_mode
                    or is_level_up_mode
                )

                # Increment turn counter — mirrors the non-streaming path in world_logic.py.
                # This ensures player_turn advances and last_living_world_turn tracks correctly.
                _turn_before = updated_state_dict.get("turn_number")
                updated_state_dict = world_logic._increment_turn_counter(
                    updated_state_dict,
                    is_god_mode=is_god_mode_turn,
                    should_freeze_time=should_freeze_time,
                )
                # Mark dirty only when the turn counter actually changed.
                # On god/freeze turns _increment_turn_counter normalizes (str→int) without
                # incrementing, so avoid a spurious Firestore write in those cases.
                if updated_state_dict.get("turn_number") != _turn_before:
                    state_dirty = True

                # Update living world tracking (last_living_world_turn) when trigger fires.
                # Mirrors _maybe_update_living_world_tracking in non-streaming path.
                updated_state_dict = world_logic._maybe_update_living_world_tracking(
                    updated_state_dict,
                    current_game_state=current_game_state,
                    turn_number=updated_state_dict.get("turn_number", 0),
                    mode=mode,
                    agent_mode=agent_mode_used,
                    is_god_mode=is_god_mode_turn,
                    is_think_mode=agent_mode_used == constants.MODE_THINK,
                    should_freeze_time=should_freeze_time,
                )

                # Debug warning: living world instruction fires every turn —
                # warn if world_events are missing from the LLM response.
                _lw_warning = _warn_if_living_world_missing(
                    updated_state_dict=updated_state_dict,
                    structured_fields=structured_fields,
                    state_updates=state_updates,
                    is_god_mode=is_god_mode_turn,
                    agent_mode=agent_mode_used,
                    mode=mode,
                    should_freeze_time=should_freeze_time,
                )
                if _lw_warning is not None:
                    living_world_warnings.append(_lw_warning)

                if state_dirty:
                    firestore_service.update_campaign_game_state(
                        user_id, campaign_id, updated_state_dict
                    )
                    logging_util.info(
                        "Persisted streaming game state updates for campaign %s.",
                        campaign_id,
                    )
            except Exception:
                logging_util.exception("Failed to persist streaming game state updates")
                persistence_warnings.append(
                    StreamEvent(
                        type="warning",
                        payload={
                            "message": "Story saved but game state may not have persisted."
                        },
                    )
                )

            # Validate and persist story entries
            if full_narrative is not None:
                validated_narrative: str | None = None
                validation_failed = False
                try:
                    # If raw_response_text is present, validate against it exactly.
                    # This catches empty/invalid raw payloads even when a fallback narrative exists.
                    if raw_response_text is not None:
                        if (
                            not isinstance(raw_response_text, str)
                            or not raw_response_text.strip()
                        ):
                            raise ValueError("Empty raw_response_text")
                        validation_source = raw_response_text
                    else:
                        validation_source = full_narrative
                    parsed_narrative, parsed_structured_response = (
                        parse_structured_response(
                            validation_source, requires_action_resolution=False
                        )
                    )
                    if not parsed_narrative or not parsed_narrative.strip():
                        god_mode_text = _extract_god_mode_response_text(
                            parsed_structured_response
                        )
                        # Fallback for streamed God Mode responses where parser output
                        # may omit narrative but done payload already has god_mode_response.
                        if not god_mode_text and mode == "god":
                            god_mode_text = _extract_god_mode_response_text(
                                structured_fields
                            )

                        if god_mode_text:
                            validated_narrative = god_mode_text
                        else:
                            raise ValueError(
                                "Structured response missing narrative text"
                            )
                    elif parsed_narrative == JSON_PARSE_FALLBACK_MARKER:
                        # parse_structured_response returned the error marker because the
                        # validation source was plain text (e.g. OpenRouter non-JSON stream).
                        # The done payload's full_narrative already holds the corrected
                        # narrative produced by the streaming fallback in llm_service.py;
                        # use it rather than storing the error string in Firestore.
                        _candidate = (full_narrative or "").strip()
                        if _candidate and _candidate != JSON_PARSE_FALLBACK_MARKER:
                            validated_narrative = _candidate
                        else:
                            raise ValueError(
                                "Narrative resolved to JSON-parse-failure marker with no usable fallback"
                            )
                    else:
                        validated_narrative = parsed_narrative
                    if (
                        structured_fields is None
                        and parsed_structured_response is not None
                    ):
                        if isinstance(parsed_structured_response, dict):
                            structured_fields = parsed_structured_response
                        elif hasattr(parsed_structured_response, "model_dump"):
                            structured_fields = parsed_structured_response.model_dump()
                        elif hasattr(parsed_structured_response, "to_dict"):
                            structured_fields = parsed_structured_response.to_dict()
                except Exception:
                    fallback_god_mode_text = _extract_god_mode_response_text(
                        structured_fields
                    )
                    if fallback_god_mode_text:
                        validated_narrative = fallback_god_mode_text
                    else:
                        validation_failed = True
                        logging_util.exception(
                            "Streaming response validation failed before persistence"
                        )
                        persistence_warnings.append(
                            StreamEvent(
                                type="warning",
                                payload={
                                    "message": (
                                        "Response validation failed; only user input was persisted."
                                    )
                                },
                            )
                        )

                try:
                    # Persistence contract:
                    # - SSE streaming endpoint persists story entries here.
                    # - llm_service.continue_story_streaming does NOT persist.
                    # - Non-streaming API uses world_logic.process_action_unified.
                    firestore_service.add_story_entry(
                        user_id,
                        campaign_id,
                        "user",
                        user_input,
                        mode=mode,
                    )
                    if not validation_failed and validated_narrative:
                        # Align with non-streaming: extract living world data
                        # from state_updates and backfill when LLM omits events.
                        gemini_structured = (
                            copy.deepcopy(structured_fields)
                            if structured_fields
                            else {}
                        )
                        _enrich_streaming_structured_fields(
                            gemini_structured,
                            updated_state_dict=updated_state_dict,
                            story_context=story_context,
                        )
                        firestore_service.add_story_entry(
                            user_id,
                            campaign_id,
                            "gemini",
                            validated_narrative,
                            mode=mode,
                            structured_fields=gemini_structured,
                        )
                    logging_util.info(
                        f"Persisted streaming story entries for campaign {campaign_id}"
                    )
                except Exception:
                    logging_util.exception("Failed to persist streaming story entries")
                    persistence_warnings.append(
                        StreamEvent(
                            type="warning",
                            payload={
                                "message": "Story saved but some data may not have persisted."
                            },
                        )
                    )

            # Attach living world warnings to the done event payload so the client
            # can surface them via the done.warnings field.
            if living_world_warnings:
                event.payload["warnings"] = living_world_warnings

            # Now yield done event (persistence already complete)
            yield event

            # Yield any persistence warnings (best-effort, non-critical)
            yield from persistence_warnings

    except Exception:
        logging_util.exception("Streaming error in stream_story_with_game_state")
        yield StreamEvent(
            type="error",
            payload={
                "message": "An unexpected error occurred while streaming the response.",
            },
        )

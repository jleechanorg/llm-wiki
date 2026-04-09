"""
LLM Service - AI Integration and Response Processing

This module provides comprehensive AI service integration for WorldArchitect.AI,
handling all aspects of story generation, prompt construction, and response processing.

Key Responsibilities:
- Gemini AI client management and model selection
- System instruction building and prompt construction
- Entity tracking and narrative validation
- JSON response parsing and structured data handling
- Model fallback and error handling
- Planning block enforcement and debug content management
- Token counting and context management
- Agent-based mode handling (story mode vs god mode)
- **FIXED: Token limit management to prevent backstory cutoffs**

Architecture:
- Uses Google Generative AI (Gemini) for story generation
- Implements agent architecture for different interaction modes
- Uses PromptBuilder (agent_prompts) for system instruction construction
- Provides entity tracking with multiple mitigation strategies
- Includes comprehensive error handling
- Supports both initial story generation and continuation
- Manages complex state interactions and validation

Key Classes:
- BaseAgent: Abstract base class for all agents
- StoryModeAgent: Agent for narrative storytelling (character mode)
- GodModeAgent: Agent for administrative commands (god mode)
- CombatAgent: Agent for active combat encounters (combat mode)
- PromptBuilder: Constructs system instructions and prompts (agent_prompts)
- LLMResponse: Custom response object with parsed data
- EntityPreloader: Pre-loads entity context for tracking
- EntityInstructionGenerator: Creates entity-specific instructions

Agent Architecture:
Each agent has a focused subset of system prompts (in load order):
- StoryModeAgent: master_directive → game_state → debug → narrative/mechanics (selected) → dnd_srd → continuation reminder → optional world
- GodModeAgent: master_directive → god_mode → game_state → mechanics → dnd_srd → debug
- CombatAgent: master_directive → game_state → combat → narrative → dnd_srd → mechanics → debug (auto-selected when in_combat=true)
Use get_agent_for_input() factory function to select the appropriate agent.

Dependencies:
- Google Generative AI SDK for Gemini API calls
- Custom entity tracking and validation modules
- Game state management for context
- Token utilities for cost management

Turn/Scene Terminology (IMPORTANT):
The codebase uses distinct counting systems for story progression:

- **story_entry_count / turn_number**: Internal counter of ALL story entries
  (both user inputs and AI responses). Calculated as len(story_context) + 1.
  Used for: caching, entity manifest tracking, internal sequencing.

- **sequence_id**: Absolute position in story array. Every entry (user + AI)
  gets an incrementing sequence_id. Technical identifier for ordering.

- **user_scene_number**: User-facing "Scene #X" counter. ONLY increments for
  AI (Gemini) responses. User inputs get user_scene_number=None.
  This is what players see as the scene progression.

Relationship (approximate, assumes perfect alternation):
  user_scene_number ≈ story_entry_count / 2

Example with 6 entries (alternating user/AI):
  Entry 1: user   → sequence_id=1, user_scene_number=None
  Entry 2: gemini → sequence_id=2, user_scene_number=1 (Scene #1)
  Entry 3: user   → sequence_id=3, user_scene_number=None
  Entry 4: gemini → sequence_id=4, user_scene_number=2 (Scene #2)
  Entry 5: user   → sequence_id=5, user_scene_number=None
  Entry 6: gemini → sequence_id=6, user_scene_number=3 (Scene #3)
"""

import hashlib
import hmac
import json
import os
import re
import sys
import threading
import time
from collections.abc import Generator
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from urllib.parse import urlsplit

from google.genai import types

from mvp_site import (
    constants,
    dice,
    dice_integrity,
    dice_provably_fair,
    dice_strategy,
    faction_state_util,
    logging_util,
)
from mvp_site.action_resolution_utils import has_action_resolution_dice
from mvp_site.agent_prompts import (
    clear_loaded_files_tracking,
    get_current_turn_prompt,
    get_loaded_instruction_files,
    get_static_prompt_parts,
)
from mvp_site.agents import (
    BaseAgent as _BaseAgent,
)
from mvp_site.agents import (
    CharacterCreationAgent,
    FactionManagementAgent,
    GodModeAgent,
    PlanningAgent,
    RewardsAgent,
    StoryModeAgent,
    get_agent_for_input,
)
from mvp_site.streaming_chunk_logger import (
    finalize_chunk_logger,
    get_or_create_chunk_logger,
)

# Backward-compatible re-export for imports like:
# from mvp_site.llm_service import BaseAgent
BaseAgent = _BaseAgent

# Context compaction and budget allocation
# FIX Issue 4: Remove unused imports (only 3 of 24 imports were actually used)
from mvp_site.context_compaction import (
    BUDGET_STORY_CONTEXT_ABSOLUTE_MIN,
    _allocate_request_budget,
    _compact_core_memories,
    _filter_persisted_warnings,
    _save_warning_persist_keys,
)
from mvp_site.custom_types import UserId
from mvp_site.decorators import log_exceptions
from mvp_site.entity_instructions import EntityInstructionGenerator

# Import entity tracking mitigation modules
from mvp_site.entity_preloader import EntityPreloader
from mvp_site.entity_tracking import create_from_game_state
from mvp_site.entity_validator import EntityValidator
from mvp_site.equipment_display import (
    ensure_equipment_summary_in_narrative,
    extract_equipment_display,
    is_equipment_query,
)
from mvp_site.file_cache import read_file_cached
from mvp_site.firestore_service import get_user_settings
from mvp_site.game_state import (
    GameState,
    execute_tool_requests,
    format_tool_results_text,
)
from mvp_site.gemini_cache_manager import get_cache_manager
from mvp_site.llm_providers import (
    ContextTooLargeError,
    cerebras_provider,
    gemini_provider,
    openclaw_provider,
    openrouter_provider,
)
from mvp_site.llm_providers.gemini_provider import (
    apply_code_execution_system_instruction,
    uses_code_execution_strategy,
)

# Centralized in provider_utils to avoid duplication
from mvp_site.llm_providers.provider_utils import (
    build_domain_tool_request_enforcement,
    build_tool_results_prompt,
    execute_gemini_code_execution_tool_orchestration,
    extract_json_payload_and_tool_requests,
    get_enable_turn_retry_instruction,
    get_prompt_tool_context,
    inject_tool_requests_if_missing,
    stringify_chat_parts,
    update_prompt_contents_with_tool_results,
)
from mvp_site.llm_providers.provider_utils import (
    strip_tool_requests_dice_instructions as _strip_tool_requests_dice_instructions,
)
from mvp_site.llm_request import (
    MAX_PAYLOAD_SIZE,
    LLMRequest,
    LLMRequestError,
    PayloadTooLargeError,
)
from mvp_site.llm_response import LLMResponse

# Memory utilities now imported via agent_prompts (centralized prompt manipulation)
# Removed old json_input_schema import - now using LLMRequest for structured JSON
from mvp_site.narrative_response_schema import (
    JSON_PARSE_FALLBACK_MARKER,
    NarrativeResponse,
    create_structured_prompt_injection,
    parse_structured_response,
    validate_entity_coverage,
)
from mvp_site.narrative_sync_validator import NarrativeSyncValidator
from mvp_site.schemas.entities_pydantic import sanitize_entity_name_for_id
from mvp_site.serialization import json_default_serializer
from mvp_site.settings_validation import validate_openclaw_gateway_url
from mvp_site.stream_events import StreamEvent
from mvp_site.token_utils import estimate_tokens, log_with_tokens

# Import for streaming support (late import to avoid circular dependency)
# StreamEvent is imported at runtime in continue_story_streaming


def build_full_content_for_retry(gemini_request: "LLMRequest") -> str:
    """Build full content string for cache retry scenarios.

    When explicit caching fails (403 PERMISSION_DENIED or cache miss), we need
    to retry with the FULL content, not just the uncacheable portion.

    This centralized function ensures consistent serialization across all
    cache retry paths.

    Args:
        gemini_request: The LLMRequest containing full context

    Returns:
        JSON string of the full request content (indent=2 for readability)
    """
    return json.dumps(
        gemini_request.to_json(), indent=2, default=json_default_serializer
    )


# Raw LLM capture limit configuration
RAW_LIMIT_DEFAULT = 20000


def _get_raw_limit() -> int:
    """Get raw LLM capture limit from environment variable with robust error handling.

    Returns:
        Integer limit, defaults to RAW_LIMIT_DEFAULT if env var is invalid or missing.
    """
    try:
        return int(os.getenv("CAPTURE_RAW_LLM_MAX_CHARS", str(RAW_LIMIT_DEFAULT)))
    except (TypeError, ValueError):
        return RAW_LIMIT_DEFAULT


def _is_mcp_real_mode() -> bool:
    """Return True when MCP tests explicitly request real mode."""
    return os.getenv("MCP_TEST_MODE", "").strip().lower() == "real"


def _is_mock_services_mode() -> bool:
    """Return True when mock services are enabled (env var or per-request SMOKE_TOKEN flag)."""
    if os.getenv("MOCK_SERVICES_MODE", "").strip().lower() == "true":
        return True
    try:
        from flask import g as flask_g

        return bool(getattr(flask_g, "mock_services_mode", False))
    except RuntimeError:
        return False


logging_util.basicConfig(
    level=logging_util.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Dice integrity helpers centralized in mvp_site/dice_integrity.py
DICE_ROLL_PATTERN = dice_integrity.DICE_ROLL_PATTERN
_detect_narrative_dice_fabrication = dice_integrity._detect_narrative_dice_fabrication
_is_code_execution_fabrication = dice_integrity._is_code_execution_fabrication
_log_fabricated_dice_if_detected = dice_integrity._log_fabricated_dice_if_detected
_should_require_dice_rolls_for_turn = dice_integrity._should_require_dice_rolls_for_turn
_validate_combat_dice_integrity = dice_integrity._validate_combat_dice_integrity
_validate_dice_integrity_always = dice_integrity._validate_dice_integrity_always

# Initialize entity tracking mitigation modules
entity_preloader = EntityPreloader()
instruction_generator = EntityInstructionGenerator()
entity_validator = EntityValidator()

# Expected companion count for validation
EXPECTED_COMPANION_COUNT = 3

# Equipment display functions moved to mvp_site/equipment_display.py
# Import: is_equipment_query, classify_equipment_query, extract_equipment_display,
#         ensure_equipment_summary_in_narrative, EQUIPMENT_QUERY_KEYWORDS

# Remove redundant json_datetime_serializer - use json_default_serializer instead
# which properly handles Firestore Sentinels, datetime objects, and other special types


def _merge_cache_payloads(
    cacheable: dict[str, Any],
    uncacheable: dict[str, Any],
) -> dict[str, Any]:
    """Merge cacheable + uncacheable payloads, concatenating story_history."""
    merged = {**cacheable, **uncacheable}
    merged["story_history"] = cacheable.get("story_history", []) + uncacheable.get(
        "story_history", []
    )
    return merged


# --- CONSTANTS ---
# Default model selection based on the configured DEFAULT_LLM_PROVIDER
# This ensures provider-model consistency across all code paths
if constants.DEFAULT_LLM_PROVIDER == constants.LLM_PROVIDER_CEREBRAS:
    DEFAULT_MODEL: str = constants.DEFAULT_CEREBRAS_MODEL
    TEST_MODEL: str = constants.DEFAULT_CEREBRAS_MODEL
elif constants.DEFAULT_LLM_PROVIDER == constants.LLM_PROVIDER_OPENROUTER:
    DEFAULT_MODEL = constants.DEFAULT_OPENROUTER_MODEL
    TEST_MODEL = constants.DEFAULT_OPENROUTER_MODEL
else:  # Gemini (default fallback)
    DEFAULT_MODEL = constants.DEFAULT_GEMINI_MODEL
    TEST_MODEL = constants.DEFAULT_GEMINI_MODEL


@dataclass(frozen=True)
class ProviderSelection:
    provider: str
    model: str


def _select_provider_with_fallback() -> tuple[str, str]:
    """Select the best available provider based on API key availability.

    Returns the default provider if its API key is available, otherwise falls
    back to an alternative provider with an available key.

    This prevents hard failures when the default provider's API key is missing
    but other provider keys are available.

    Returns:
        tuple[str, str]: (provider_name, model_name)
    """
    default_provider = constants.DEFAULT_LLM_PROVIDER

    # Check if default provider's API key is available
    api_key_map = {
        constants.LLM_PROVIDER_GEMINI: os.environ.get("GEMINI_API_KEY", ""),
        constants.LLM_PROVIDER_CEREBRAS: os.environ.get("CEREBRAS_API_KEY", ""),
        constants.LLM_PROVIDER_OPENROUTER: os.environ.get("OPENROUTER_API_KEY", ""),
    }

    model_map = {
        constants.LLM_PROVIDER_GEMINI: constants.DEFAULT_GEMINI_MODEL,
        constants.LLM_PROVIDER_CEREBRAS: constants.DEFAULT_CEREBRAS_MODEL,
        constants.LLM_PROVIDER_OPENROUTER: constants.DEFAULT_OPENROUTER_MODEL,
    }

    # Try default provider first
    if api_key_map.get(default_provider):
        return default_provider, model_map[default_provider]

    # Fall back to first available provider
    fallback_order = [
        constants.LLM_PROVIDER_CEREBRAS,
        constants.LLM_PROVIDER_GEMINI,
        constants.LLM_PROVIDER_OPENROUTER,
    ]

    for provider in fallback_order:
        if api_key_map.get(provider):
            logging_util.warning(
                f"Default provider {default_provider} API key missing, "
                f"falling back to {provider}"
            )
            return provider, model_map[provider]

    # No API keys available - return default and let it fail with clear error
    return default_provider, model_map[default_provider]


# No longer using pro model for any inputs

# Gemini 2.5 Flash OUTPUT token limits (corrected based on updated specs)
# Gemini 2.5 Flash = 65,535 output tokens (not 8,192 as initially thought)
# Using conservative 50,000 output token limit to stay well below maximum
MAX_OUTPUT_TOKENS: int = (
    50000  # Conservative output token limit below Gemini 2.5 Flash max (65,535)
)
TEMPERATURE: float = 0.9
# TARGET_WORD_COUNT moved to agent_prompts.py for centralized prompt manipulation
# Add a safety margin for JSON responses to prevent mid-response cutoffs

# Default planning block generation has been REMOVED.
# If the LLM doesn't generate a planning block, we return the response as-is and let any
# downstream validation/UI handling surface it (no server-side retries).
# For JSON mode, use same output token limit as regular mode
# This ensures complete character backstories and complex JSON responses
JSON_MODE_MAX_OUTPUT_TOKENS: int = MAX_OUTPUT_TOKENS  # Same limit for consistency
MAX_INPUT_TOKENS: int = 300000
SAFE_CHAR_LIMIT: int = MAX_INPUT_TOKENS * 4
GEMINI_COMPACTION_TOKEN_LIMIT: int = 300_000  # Cap compaction well below 1M max
# Dynamic output reserve: 12k default for normal gameplay, scales up for combat/complex
OUTPUT_TOKEN_RESERVE_DEFAULT: int = 12_000  # Typical responses are 1-3k tokens
OUTPUT_TOKEN_RESERVE_COMBAT: int = 24_000  # Combat/complex scenes need more
OUTPUT_TOKEN_RESERVE_MIN: int = 1024
OUTPUT_TOKEN_RESERVE_RATIO: float = 0.20  # Reserve 20% of context for output tokens
_BYOK_PROVIDER_API_KEY_FIELDS: dict[str, str] = {
    constants.LLM_PROVIDER_GEMINI: "gemini_api_key",
    constants.LLM_PROVIDER_OPENROUTER: "openrouter_api_key",
    constants.LLM_PROVIDER_CEREBRAS: "cerebras_api_key",
}

# Entity tracking token reserves - these are added AFTER truncation so must be pre-budgeted
# Sizes based on production data with 10+ NPCs:
# - entity_preload_text: ~2000-3000 tokens (NPC summaries)
# - entity_specific_instructions: ~1500-2000 tokens (per-turn instructions)
# - entity_tracking_instruction: ~1000-1500 tokens (tracking rules)
# NOTE: timeline_log text is constructed for diagnostics/entity instructions but is NOT
# serialized into the structured LLMRequest payload.
ENTITY_TRACKING_TOKEN_RESERVE: int = 10_500  # Conservative reserve for entity tracking

# Minimum story budget to ensure at least some conversation history is included
# Even with large scaffolds, we want to preserve recent turns for continuity
# This reserves space for approximately 5-10 turns minimum
MIN_STORY_TOKEN_BUDGET: int = 10_000  # ~10k tokens ≈ 5-10 story entries

# Entity tiering configuration for LRU-style token reduction
# Caps entity_tracking growth for campaigns with many NPCs by:
# 1. Only including recently-active entities (mentioned in last N turns)
# 2. Trimming fields to essential info only (name, role, status, hp)
# Note: Typical campaigns have ~50-200 tokens; this guards against edge cases.
ENTITY_TIER_ACTIVE_MAX: int = 5  # Max entities with essential field tracking
ENTITY_TIER_PRESENT_MAX: int = 10  # Max entities with minimal (name+role) tracking
ENTITY_TIER_DORMANT_MAX: int = (
    20  # Max dormant entities with minimal (name+role) tracking
)
ENTITY_LOOKBACK_TURNS: int = 5  # Turns to scan for recent entity mentions


def _extract_recently_mentioned_entities(
    story_context: list[dict[str, Any]],
    npc_names: list[str],
    lookback_turns: int = ENTITY_LOOKBACK_TURNS,
) -> dict[str, int]:
    """
    Scan recent story turns to find which NPCs were mentioned.

    Uses LRU-style recency scoring: entities mentioned more recently get higher scores.
    This allows us to prioritize active entities over dormant ones.

    Args:
        story_context: List of story turn entries with 'text' field
        npc_names: List of known NPC names to search for
        lookback_turns: Number of recent turns to scan

    Returns:
        Dict of {npc_name: recency_score} where higher = more recent
    """
    recent_turns = story_context[-lookback_turns:] if story_context else []
    mentioned: dict[str, int] = {}

    for turn_idx, turn in enumerate(recent_turns):
        text = turn.get("text", "").lower()
        for npc_name in npc_names:
            # Use word boundary regex to avoid "King" matching "Kingsley"
            pattern = rf"\b{re.escape(npc_name.lower())}\b"
            if re.search(pattern, text):
                # Higher index = more recent = higher score
                mentioned[npc_name] = turn_idx

    return mentioned


def _coerce_npc_entry_to_dict(npc_name: str, npc_info: Any) -> dict[str, Any]:
    """Normalize malformed NPC entries into a dict for downstream code safety."""
    if isinstance(npc_info, dict):
        return dict(npc_info)

    if npc_info is None:
        logging_util.warning(
            f"⚠️ NPC '{npc_name}' data is None; using empty fallback dict"
        )
        return {"name": npc_name}

    if isinstance(npc_info, list):
        normalized: dict[str, Any] = {"name": npc_name}
        status_fragments: list[str] = []

        for item in npc_info:
            if isinstance(item, dict):
                normalized.update(item)
                continue

            if not isinstance(item, str):
                status_fragments.append(str(item))
                continue

            item_value = item.strip()
            if not item_value:
                continue

            if ":" in item_value:
                key, value = item_value.split(":", 1)
                normalized[key.strip()] = value.strip()
            else:
                status_fragments.append(item_value)

        if status_fragments and "status" not in normalized:
            normalized["status"] = ", ".join(status_fragments)

        if len(normalized) == 1:
            logging_util.warning(
                f"⚠️ NPC '{npc_name}' entry is list-based and could not be parsed into fields: {npc_info}"
            )
        else:
            logging_util.info(
                f"⚠️ NPC '{npc_name}' entry normalized from list format into dict"
            )
        return normalized

    if isinstance(npc_info, str):
        if npc_info.strip():
            logging_util.warning(
                f"⚠️ NPC '{npc_name}' entry is string; converting to status field"
            )
            return {"name": npc_name, "status": npc_info.strip()}
        return {"name": npc_name}

    logging_util.warning(
        f"⚠️ NPC '{npc_name}' entry has unexpected type={type(npc_info).__name__}; coercing to status string"
    )
    return {"name": npc_name, "status": str(npc_info)}


def _tier_entities(
    npc_data: dict[str, Any],
    recently_mentioned: dict[str, int],
    current_location: str,
) -> tuple[list[str], list[str], list[str]]:
    """
    Categorize NPCs into ACTIVE, PRESENT, DORMANT tiers for token optimization.

    ACTIVE: Recently mentioned, get essential field tracking (~50 tokens each)
    PRESENT: In current location, get minimal tracking (~10 tokens each)
    DORMANT: Not active, included with minimal tracking when budget allows

    Args:
        npc_data: Dict of NPC name -> NPC data from game_state
        recently_mentioned: Dict of NPC name -> recency score from story scan
        current_location: Current location name for presence check

    Returns:
        Tuple of (active_names, present_names, dormant_names)
    """
    active_candidates: list[tuple[str, int]] = []
    present: list[str] = []

    # Coerce current_location to string once before the loop (belt-and-suspenders against dict/non-str)
    if isinstance(current_location, dict):
        _loc_name = current_location.get("name")
        current_location = (
            _loc_name if _loc_name is not None else (current_location.get("id") or "")
        )
        current_location = str(current_location)
    elif current_location is not None and not isinstance(current_location, str):
        current_location = str(current_location)

    for name, raw_data in npc_data.items():
        data = _coerce_npc_entry_to_dict(name, raw_data)
        npc_location = data.get("current_location", data.get("location", ""))
        if isinstance(npc_location, dict):
            logging_util.warning(
                f"⚠️ NPC '{name}' location is dict: {list(npc_location.keys())}"
            )
            _loc_name = npc_location.get("name")
            npc_location = (
                _loc_name if _loc_name is not None else (npc_location.get("id") or "")
            )
            npc_location = str(npc_location)
        elif npc_location is not None and not isinstance(npc_location, str):
            npc_location = str(npc_location)
        # Normalize locations for comparison (strip whitespace, lowercase)
        npc_location_normalized = npc_location.strip().lower() if npc_location else ""
        current_location_normalized = (
            current_location.strip().lower() if current_location else ""
        )

        if name in recently_mentioned:
            # Recently mentioned - candidate for ACTIVE tier
            active_candidates.append((name, recently_mentioned[name]))
        elif (
            npc_location_normalized
            and current_location_normalized
            and (npc_location_normalized == current_location_normalized)
        ):
            # In same location but not recently mentioned - PRESENT tier
            present.append(name)

    # Sort active by recency (higher score = more recent), take top N
    active_candidates.sort(key=lambda x: x[1], reverse=True)
    active = [name for name, _ in active_candidates[:ENTITY_TIER_ACTIVE_MAX]]

    # Limit present entities
    present = present[:ENTITY_TIER_PRESENT_MAX]

    # Everything not ACTIVE or PRESENT is DORMANT (included with minimal tracking when budget allows)
    dormant = [name for name in npc_data if name not in active and name not in present]
    dormant = dormant[:ENTITY_TIER_DORMANT_MAX]

    return active, present, dormant


def _trim_entity_fields(npc_data: dict[str, Any], tier: str) -> dict[str, Any]:
    """
    Extract only essential fields based on entity tier.

    ACTIVE tier (~50 tokens): name, role, attitude, status, hp, location
    PRESENT tier (~10 tokens): name, role only
    DORMANT tier (~10 tokens): name, role only

    This reduces per-entity tokens from ~500 to ~50 or ~10.

    Args:
        npc_data: Full NPC data dict from game_state
        tier: Either "ACTIVE", "PRESENT", or "DORMANT"

    Returns:
        Trimmed dict with only essential fields
    """
    npc_name = (
        npc_data.get("name", "unknown") if isinstance(npc_data, dict) else "unknown"
    )
    data = _coerce_npc_entry_to_dict(npc_name, npc_data)

    if tier == "ACTIVE":
        # Extract health info safely
        health = data.get("health", {})
        if isinstance(health, dict):
            hp_current = health.get("hp", "?")
            hp_max = health.get("hp_max", "?")
        else:
            hp_current = data.get("hp_current", data.get("hp", "?"))
            hp_max = data.get("hp_max", "?")

        # Extract status safely
        status_list = data.get("status", ["conscious"])
        if isinstance(status_list, list) and status_list:
            status = status_list[0] if isinstance(status_list[0], str) else "conscious"
        elif isinstance(status_list, str):
            status = status_list
        else:
            status = "conscious"

        return {
            "name": data.get("display_name", data.get("name", "Unknown")),
            "role": data.get("role", "NPC"),
            "attitude": data.get("attitude_to_party", "neutral"),
            "status": status,
            "hp": f"{hp_current}/{hp_max}",
            "location": data.get("current_location", data.get("location", "unknown")),
        }

    if tier == "PRESENT":
        return {
            "name": data.get("display_name", data.get("name", "Unknown")),
            "role": data.get("role", "NPC"),
        }

    if tier == "DORMANT":
        return {
            "name": data.get("display_name", data.get("name", "Unknown")),
            "role": data.get("role", "NPC"),
        }

    return {}


def _build_trimmed_entity_tracking(
    npc_data: dict[str, Any],
    story_context: list[dict[str, Any]],
    current_location: str,
    max_tokens: int | None = None,
) -> tuple[dict[str, Any], str]:
    """
    Build entity_tracking_data with tiered, trimmed entities.

    Reduces token usage by limiting entity count and field depth:
    1. Include all tiers (active, present, dormant) with trimmed fields
    2. Trimming fields to essentials only
    3. Further reducing entities if max_tokens budget is specified

    Args:
        npc_data: Dict of NPC name -> NPC data from game_state.npc_data
        story_context: List of story turn entries
        current_location: Current location name
        max_tokens: Optional token budget for entity tracking (from budget allocator)

    Returns:
        Tuple of (entity_tracking_data, log_summary)
    """
    if not npc_data or not isinstance(npc_data, dict):
        if npc_data and not isinstance(npc_data, dict):
            logging_util.warning(
                "⚠️ _build_trimmed_entity_tracking received non-dict npc_data; coercing to empty"
            )
        return (
            {"active_entities": [], "present_entities": [], "dormant_entities": []},
            "ENTITY_TIERS: no NPCs",
        )

    # Get NPC names for scanning
    npc_names = list(npc_data.keys())

    # Find recently mentioned entities via LRU scan
    recently_mentioned = _extract_recently_mentioned_entities(story_context, npc_names)

    # Tier the entities
    active, present, dormant = _tier_entities(
        npc_data, recently_mentioned, current_location
    )

    # Build trimmed entity lists
    active_entities = [
        _trim_entity_fields(npc_data[name], "ACTIVE")
        for name in active
        if name in npc_data
    ]
    present_entities = [
        _trim_entity_fields(npc_data[name], "PRESENT")
        for name in present
        if name in npc_data
    ]
    dormant_entities = [
        _trim_entity_fields(npc_data[name], "DORMANT")
        for name in dormant
        if name in npc_data
    ]

    # Build tracking data - much smaller than before
    entity_tracking_data = {
        "active_entities": active_entities,
        "present_entities": present_entities,
        "dormant_entities": dormant_entities,
    }

    # If max_tokens budget specified, enforce it by progressively dropping entities
    if max_tokens is not None:
        dropped_counts = {"dormant": 0, "present": 0, "active": 0}
        current_json = json.dumps(entity_tracking_data, separators=(",", ":"))
        current_tokens = estimate_tokens(current_json)

        # Drop dormant entities first, then present, then active
        while current_tokens > max_tokens and dormant_entities:
            dormant_entities.pop()
            dropped_counts["dormant"] += 1
            entity_tracking_data["dormant_entities"] = dormant_entities
            current_json = json.dumps(entity_tracking_data, separators=(",", ":"))
            current_tokens = estimate_tokens(current_json)

        while current_tokens > max_tokens and present_entities:
            present_entities.pop()
            dropped_counts["present"] += 1
            entity_tracking_data["present_entities"] = present_entities
            current_json = json.dumps(entity_tracking_data, separators=(",", ":"))
            current_tokens = estimate_tokens(current_json)

        while current_tokens > max_tokens and active_entities:
            active_entities.pop()
            dropped_counts["active"] += 1
            entity_tracking_data["active_entities"] = active_entities
            current_json = json.dumps(entity_tracking_data, separators=(",", ":"))
            current_tokens = estimate_tokens(current_json)

        if current_tokens > max_tokens:
            logging_util.warning(
                f"⚠️ ENTITY_TRACKING_BUDGET_EXCEEDED: {current_tokens}tk > {max_tokens}tk "
                f"even after dropping all entities"
            )

    log_summary = (
        f"ENTITY_TIERS: active={len(active_entities)}/{ENTITY_TIER_ACTIVE_MAX}, "
        f"present={len(present_entities)}/{ENTITY_TIER_PRESENT_MAX}, "
        f"dormant={len(dormant_entities)}/{len(dormant)}"
    )

    if max_tokens is not None:
        final_tokens = estimate_tokens(
            json.dumps(entity_tracking_data, separators=(",", ":"))
        )
        log_summary += f", budget={final_tokens}/{max_tokens}tk"
        if dropped_counts != {"dormant": 0, "present": 0, "active": 0}:
            log_summary += (
                f", dropped=dormant:{dropped_counts['dormant']}"
                f", present:{dropped_counts['present']}"
                f", active:{dropped_counts['active']}"
            )

    return entity_tracking_data, log_summary


def _get_context_window_tokens(model_name: str) -> int:
    """Return the configured context window size for a model in tokens."""
    lookup_name = model_name.removeprefix("openclaw/")
    return constants.MODEL_CONTEXT_WINDOW_TOKENS.get(
        lookup_name, constants.DEFAULT_CONTEXT_WINDOW_TOKENS
    )


def _get_safe_context_token_budget(provider: str, model_name: str) -> int:
    """Apply a 90% safety margin to the model's context window before truncation."""

    context_tokens = _get_context_window_tokens(model_name)
    safe_tokens = int(context_tokens * constants.CONTEXT_WINDOW_SAFETY_RATIO)

    # Gemini supports 1M tokens; compact earlier for latency/stability.
    if provider == constants.LLM_PROVIDER_GEMINI:
        return min(safe_tokens, GEMINI_COMPACTION_TOKEN_LIMIT)

    return safe_tokens


def _calculate_context_budget(
    provider: str,
    model_name: str,
    is_combat_or_complex: bool = False,
) -> tuple[int, int, int]:
    """
    CENTRALIZED context budget calculation for both truncation and validation.

    This single function ensures truncation and validation use identical logic,
    preventing bugs where content passes truncation but fails validation.

    Args:
        provider: LLM provider name (e.g., 'gemini', 'cerebras')
        model_name: Model identifier
        is_combat_or_complex: Whether combat/complex scenes need extra output reserve

    Returns:
        tuple of (safe_token_budget, output_reserve, max_input_allowed)
        - safe_token_budget: Total safe tokens for this model (90% of context)
        - output_reserve: Tokens reserved for output (20% of safe budget, or combat minimum)
        - max_input_allowed: Maximum tokens allowed for input (80% of safe budget)
    """
    safe_token_budget = _get_safe_context_token_budget(provider, model_name)

    # Use consistent 20% ratio for output reserve
    output_reserve = int(safe_token_budget * OUTPUT_TOKEN_RESERVE_RATIO)

    # For combat/complex scenes, use the larger of ratio-based or fixed reserve
    if is_combat_or_complex:
        output_reserve = max(output_reserve, OUTPUT_TOKEN_RESERVE_COMBAT)

    max_input_allowed = safe_token_budget - output_reserve

    return safe_token_budget, output_reserve, max_input_allowed


def _get_safe_output_token_limit(
    model_name: str,
    prompt_tokens: int,
    system_tokens: int,
) -> int:
    """
    Compute a conservative max_output_tokens based on remaining context.

    - Uses actual model context window (not compaction limit) for output calculation.
    - Compaction limit is only for INPUT compaction decisions, not output budgeting.
    - Reserves 20% of context for output tokens to ensure quality responses.
    - Caps by JSON_MODE_MAX_OUTPUT_TOKENS so we don't exceed API limits.
    """
    # Use actual model context window for output calculation
    # The compaction limit is only for INPUT compaction, not output budgeting
    model_context = _get_context_window_tokens(model_name)
    safe_context = int(model_context * constants.CONTEXT_WINDOW_SAFETY_RATIO)

    # Reserve 20% of context for output tokens
    output_reserve = int(safe_context * OUTPUT_TOKEN_RESERVE_RATIO)
    max_input_allowed = safe_context - output_reserve

    total_input = prompt_tokens + system_tokens
    if total_input > max_input_allowed:
        # Input exceeds 80% of context - not enough room for output
        # Fail fast with a clear error instead of sending a doomed request
        # Use ContextTooLargeError for consistent upstream handling
        raise ContextTooLargeError(
            f"Context too large for model {model_name}: "
            f"input uses {total_input:,} tokens, "
            f"max allowed is {max_input_allowed:,} tokens (80% of {safe_context:,}), "
            f"reserving {output_reserve:,} tokens (20%) for output. "
            "Reduce prompt size or use a model with larger context window.",
            prompt_tokens=total_input,
            completion_tokens=0,
            finish_reason="context_exceeded",
        )

    # Calculate remaining space for output
    raw_remaining = safe_context - total_input
    # Ensure at least the minimum reserve or the remaining context, whichever is larger
    remaining = max(OUTPUT_TOKEN_RESERVE_MIN, raw_remaining)

    model_cap = constants.MODEL_MAX_OUTPUT_TOKENS.get(
        model_name.removeprefix("openclaw/"), JSON_MODE_MAX_OUTPUT_TOKENS
    )
    return min(JSON_MODE_MAX_OUTPUT_TOKENS, model_cap, remaining)


def _calculate_prompt_and_system_tokens(
    user_prompt_contents: list[Any],
    system_instruction_text: str | None,
    provider_name: str,
    model_name: str,
) -> tuple[int, int]:
    """Provider-aware token estimation for prompt + system parts."""

    if provider_name != constants.LLM_PROVIDER_GEMINI:
        # Join string contents from list of messages or raw strings
        parts: list[str] = []
        for item in user_prompt_contents:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict) and "content" in item:
                parts.append(str(item["content"]))
            else:
                parts.append(str(item))
        combined_prompt = " ".join(parts)
        prompt_tokens = estimate_tokens(combined_prompt)
        system_tokens = estimate_tokens(system_instruction_text or "")
        return prompt_tokens, system_tokens

    # Gemini provider uses API for token counting with fallback to estimation
    try:
        raw_prompt_tokens = gemini_provider.count_tokens(
            model_name, user_prompt_contents
        )
        # Guard against non-numeric returns (e.g., Mock objects in tests)
        user_prompt_tokens = (
            raw_prompt_tokens if isinstance(raw_prompt_tokens, int) else 0
        )
    except Exception:
        # Fallback to estimation if API call fails
        combined_prompt = " ".join(str(item) for item in user_prompt_contents)
        user_prompt_tokens = estimate_tokens(combined_prompt)

    system_tokens = 0
    if system_instruction_text is not None:
        try:
            raw_system_tokens = gemini_provider.count_tokens(
                model_name, [system_instruction_text]
            )
            # Guard against non-numeric returns (e.g., Mock objects in tests)
            system_tokens = (
                raw_system_tokens if isinstance(raw_system_tokens, int) else 0
            )
        except Exception:
            # Fallback to estimation if API call fails
            system_tokens = estimate_tokens(system_instruction_text)

    return user_prompt_tokens, system_tokens


# Turn count caps - increased from legacy 20/20 to allow percentage-based allocation
# to fully utilize available budget. With 20/20 caps, only ~46% of budget was used.
# Set high enough (500) to not interfere with percentage calculations while
# maintaining a safety net for edge cases.
TURNS_TO_KEEP_AT_START: int = 500
TURNS_TO_KEEP_AT_END: int = 500

# =============================================================================
# CONTEXT BUDGET ALLOCATION SYSTEM
# =============================================================================
#
# This system ensures LLM prompts fit within model-specific token limits.
# See docs/context_budget_design.md for full design documentation.
#
# ARCHITECTURE DECISION: NO AUTO-FALLBACK TO LARGER MODELS
# ---------------------------------------------------------
# DO NOT add automatic fallback to larger context models (e.g., Gemini 1M).
# This was explicitly removed in PR #2311. Reasons:
# 1. Cost unpredictability - larger models cost more per token
# 2. Voice inconsistency - different models have different personalities
# 3. Latency variance - larger contexts increase response time
# 4. Proper solution is adaptive truncation, not model switching
#
# If ContextTooLargeError occurs, the solution is to improve truncation,
# not to silently switch models. See bead WA-1 for tracking.
#
# CONTEXT BUDGET HIERARCHY (% of model context window)
# ----------------------------------------------------
# Model Context Window (100%)
# └── Safe Budget (90% - CONTEXT_WINDOW_SAFETY_RATIO)
#     ├── Output Reserve (20% - OUTPUT_TOKEN_RESERVE_RATIO)
#     │   └── Reserved for LLM response generation
#     └── Max Input Allowed (80%)
#         ├── Scaffold (~15-20% of input)
#         │   ├── System instruction (~5-8K tokens)
#         │   ├── Game state JSON (~2-4K tokens)
#         │   ├── Checkpoint block (~1-2K tokens)
#         │   └── Core memories/companions (~2-3K tokens)
#         ├── Entity Tracking Reserve (10.5K tokens fixed)
#         │   ├── entity_preload_text (~2-3K)
#         │   ├── entity_specific_instructions (~1.5-2K)
#         │   └── entity_tracking_instruction (~1-1.5K)
#         └── Story Budget (remaining ~50-60%)
#             ├── Start Turns (25% - STORY_BUDGET_START_RATIO)
#             ├── Middle Compaction (10% - STORY_BUDGET_MIDDLE_RATIO)
#             ├── End Turns (60% - STORY_BUDGET_END_RATIO)
#             └── Truncation marker (5% safety margin)
#
# Middle compaction is implemented via _compact_middle_turns() which extracts
# key events (deaths, level-ups, discoveries) from dropped middle turns.
# =============================================================================

# Percentage-based story budget allocation
# Story budget = available tokens after scaffold and output reserve
# These ratios ensure turns scale with model context size
STORY_BUDGET_START_RATIO: float = (
    0.25  # 25% of story budget for first turns (context setup)
)
STORY_BUDGET_MIDDLE_RATIO: float = 0.10  # 10% for compacted middle (key events summary)
STORY_BUDGET_END_RATIO: float = (
    0.60  # 60% of story budget for recent turns (most important)
)
# Remaining 5% reserved for truncation marker and safety margin

# Keywords that indicate important events worth preserving in middle compaction
# Organized by category for maintainability
MIDDLE_COMPACTION_KEYWORDS: set[str] = {
    "attack",
    "hit",
    "damage",
    "kill",
    "defeat",
    "victory",
    "died",
    "death",
    "combat",
    "fight",
    "battle",
    "wound",
    "heal",
    "critical",
    "strike",
    "slash",
    "stab",
    "shoot",
    "cast",
    "spell",
    "miss",
    "dodge",
    "block",
    "parry",
    "discover",
    "find",
    "found",
    "acquire",
    "obtain",
    "receive",
    "gain",
    "loot",
    "treasure",
    "gold",
    "item",
    "weapon",
    "armor",
    "artifact",
    "key",
    "unlock",
    "open",
    "chest",
    "reward",
    "coins",
    "gems",
    "potion",
    "scroll",
    "map",
    "quest",
    "mission",
    "objective",
    "complete",
    "accomplish",
    "learn",
    "warn",
    "reveal",
    "secret",
    "clue",
    "mystery",
    "truth",
    "prophecy",
    "legend",
    "oath",
    "promise",
    "vow",
    "betray",
    "deceive",
    "lie",
    "confess",
    "admit",
    "arrive",
    "enter",
    "leave",
    "travel",
    "reach",
    "escape",
    "flee",
    "run",
    "climb",
    "descend",
    "cross",
    "portal",
    "gate",
    "door",
    "passage",
    "hidden",
    "meet",
    "ally",
    "join",
    "hire",
    "recruit",
    "dismiss",
    "farewell",
    "greet",
    "negotiate",
    "bargain",
    "trade",
    "buy",
    "sell",
    "steal",
    "pickpocket",
    "level",
    "experience",
    "rest",
    "camp",
    "merchant",
    "shop",
    "inn",
    "tavern",
    "save",
    "rescue",
    "capture",
    "imprison",
    "free",
    "liberate",
    "transform",
    "suddenly",
    "finally",
    "unfortunately",
    "fortunately",
    "surprisingly",
    "importantly",
    "critically",
    "desperately",
    "triumphantly",
}

# Regex patterns for importance detection (language-agnostic)
# DICE_ROLL_PATTERN is provided by mvp_site.dice_integrity

# Pattern for numeric results (damage, HP, gold amounts - "15 damage", "50 gold", "-10 HP")
NUMERIC_RESULT_PATTERN = re.compile(
    r"\b[+\-]?\d+\s*(?:damage|hp|gold|coins|xp|exp|points?|gp|sp|cp)\b", re.IGNORECASE
)

# Pattern for quoted dialogue (may contain important information)
DIALOGUE_PATTERN = re.compile(r'"[^"]{20,}"')

# Common abbreviations to avoid splitting on (case-insensitive)
ABBREVIATIONS = {
    "mr",
    "mrs",
    "ms",
    "dr",
    "prof",
    "sr",
    "jr",
    "vs",
    "etc",
    "inc",
    "ltd",
    "st",
    "ave",
    "blvd",
    "no",
    "vol",
    "pg",
    "pp",
    "fig",
    "approx",
    "dept",
}


def _split_into_sentences(text: str) -> list[str]:
    """
    Split text into sentences, handling abbreviations and decimal numbers.

    This is more robust than simple split on '.!?' because it:
    - Preserves abbreviations like "Dr.", "Mr.", "etc."
    - Preserves decimal numbers like "3.14"
    - Handles multiple punctuation like "..." and "!?"

    Args:
        text: The text to split into sentences

    Returns:
        List of sentence strings
    """
    if not text:
        return []

    sentences = []
    current = []
    words = text.split()

    for _i, word in enumerate(words):
        current.append(word)

        # Check if this word ends a sentence
        if word and word[-1] in ".!?":
            # Check if it's an abbreviation (word without punctuation, lowercase)
            word_base = word.rstrip(".!?").lower()

            # Don't split on abbreviations
            if word_base in ABBREVIATIONS:
                continue

            # Don't split on single letters followed by period (initials like "J.")
            if len(word_base) == 1 and word.endswith("."):
                continue

            # Don't split on numbers (decimal numbers like "3.14")
            if word_base.replace(".", "").replace(",", "").isdigit():
                continue

            # This looks like a real sentence ending
            sentence = " ".join(current).strip()
            if len(sentence) > 10:  # Minimum sentence length
                sentences.append(sentence)
            current = []

    # Add any remaining text as final sentence
    if current:
        sentence = " ".join(current).strip()
        if len(sentence) > 10:
            sentences.append(sentence)

    return sentences


def _is_important_sentence(sentence: str) -> bool:
    """
    Determine if a sentence is important using keywords AND patterns.

    This is more robust than keyword-only matching because it also detects:
    - Dice rolls (language-agnostic game mechanics)
    - Numeric results (damage, gold, HP changes)
    - Long quoted dialogue (often contains important information)
    - Exclamatory sentences (often dramatic moments)

    Args:
        sentence: The sentence to evaluate

    Returns:
        True if the sentence appears important
    """
    sentence_lower = sentence.lower()

    # Check for keywords (fast path)
    if any(kw in sentence_lower for kw in MIDDLE_COMPACTION_KEYWORDS):
        return True

    # Check for dice roll patterns (language-agnostic)
    if DICE_ROLL_PATTERN.search(sentence):
        return True

    # Check for numeric results (damage, gold, etc.)
    if NUMERIC_RESULT_PATTERN.search(sentence):
        return True

    # Check for significant dialogue (long quoted text)
    if DIALOGUE_PATTERN.search(sentence):
        return True

    # Exclamatory sentences are often important dramatic moments
    return sentence.rstrip().endswith("!") and len(sentence) > 30


SAFETY_SETTINGS: list[types.SafetySetting] = [
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=types.HarmBlockThreshold.BLOCK_NONE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=types.HarmBlockThreshold.BLOCK_NONE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=types.HarmBlockThreshold.BLOCK_NONE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=types.HarmBlockThreshold.BLOCK_NONE,
    ),
]


def _clear_client() -> None:
    """FOR TESTING ONLY: Clears the cached Gemini client."""
    gemini_provider.clear_cached_client()


def get_client():
    """Initializes and returns a singleton Gemini client."""
    return gemini_provider.get_client()


def compute_player_turn_number(story_context: list[dict[str, Any]]) -> int:
    """Compute 1-indexed player turn number, excluding GOD-mode prompts.

    This counts only player (user) turns, excluding GOD-mode commands.
    Used for living world cadence (fires every 3 player turns) and
    turn/scene annotation in world_events.
    """
    if not story_context:
        return 1
    user_turns = 0
    for entry in story_context:
        if entry.get(constants.KEY_ACTOR) != constants.ACTOR_USER:
            continue
        mode = entry.get(constants.KEY_MODE)
        text = entry.get(constants.KEY_TEXT, "")
        if mode == constants.MODE_GOD:
            continue
        if isinstance(text, str) and text.strip().upper().startswith("GOD MODE:"):
            continue
        user_turns += 1
    return max(1, user_turns + 1)


def _prepare_entity_tracking(
    game_state: GameState, story_context: list[dict[str, Any]], session_number: int
) -> tuple[str, list[str], str]:
    """
    Prepare entity tracking manifest and expected entities.

    Args:
        game_state: Current GameState object
        story_context: List of story context entries
        session_number: Current session number

    Returns:
        tuple: (entity_manifest_text, expected_entities, entity_tracking_instruction)
    """
    # story_entry_count (aka turn_number): Total entries in story (user + AI)
    # NOTE: This is NOT the user-facing "Scene #X" - see module docstring for terminology
    turn_number: int = len(story_context) + 1

    # Create entity manifest from current game state (with basic caching)
    game_state_dict: dict[str, Any] = game_state.to_dict()
    manifest_cache_key = f"manifest_{session_number}_{turn_number}_{hash(str(sorted(game_state_dict.get('npc_data', {}).items())))}"

    # Simple in-memory cache for the request duration
    if not hasattr(game_state, "_manifest_cache"):
        game_state._manifest_cache = {}  # type: ignore[attr-defined]

    if manifest_cache_key in game_state._manifest_cache:  # type: ignore[attr-defined]
        entity_manifest = game_state._manifest_cache[manifest_cache_key]  # type: ignore[attr-defined]
        logging_util.debug("Using cached entity manifest")
    else:
        try:
            entity_manifest = create_from_game_state(
                game_state_dict, session_number, turn_number
            )
            game_state._manifest_cache[manifest_cache_key] = entity_manifest  # type: ignore[attr-defined]
            logging_util.debug("Created new entity manifest")
        except Exception as e:
            # Graceful degradation: If entity validation fails, warn but continue
            # This prevents crashes from malformed data (e.g., location as dict instead of string)
            logging_util.warning(
                f"Entity manifest creation failed (validation error), continuing without entity tracking: {e}"
            )
            entity_manifest = None
            # Don't cache failures - retry next time in case data is fixed

    if entity_manifest is None:
        # CI safety: some test fixtures can yield a None manifest; skip entity tracking in that case
        logging_util.warning(
            "Entity manifest generation returned None; skipping entity tracking for this turn"
        )
        entity_manifest_text = ""
        expected_entities: list[str] = []
    else:
        try:
            entity_manifest_text = entity_manifest.to_prompt_format()
        except Exception as e:
            logging_util.error(f"Entity manifest to_prompt_format() failed: {e}")
            entity_manifest_text = ""

        try:
            expected_entities = entity_manifest.get_expected_entities() or []
        except Exception as e:
            logging_util.error(f"Entity manifest get_expected_entities() failed: {e}")
            expected_entities = []

    # Always add structured response format instruction (for both entity tracking and general JSON response)
    entity_tracking_instruction = create_structured_prompt_injection(
        entity_manifest_text, expected_entities
    )

    return entity_manifest_text, expected_entities, entity_tracking_instruction


def _build_timeline_log(story_context: list[dict[str, Any]]) -> str:
    """
    Build the timeline log string from story context.

    Args:
        story_context: List of story context entries

    Returns:
        str: Formatted timeline log
    """
    timeline_log_parts = []
    for entry in story_context:
        actor_label = (
            "Story"
            if entry.get(constants.KEY_ACTOR) == constants.ACTOR_GEMINI
            else "You"
        )
        seq_id = entry.get("sequence_id", "N/A")
        timeline_log_parts.append(
            f"[SEQ_ID: {seq_id}] {actor_label}: {entry.get(constants.KEY_TEXT)}"
        )

    return "\n\n".join(timeline_log_parts)


def _select_model_for_continuation(_user_input_count: int) -> str:
    """
    Select the appropriate model based on testing mode and input count.

    Args:
        user_input_count: Number of user inputs so far

    Returns:
        str: Model name to use
    """
    # Use test model in mock services mode for faster/cheaper testing
    mock_mode = _is_mock_services_mode()
    if mock_mode:
        return TEST_MODEL
    return DEFAULT_MODEL


def _parse_gemini_response(
    raw_response_text: str,
    context: str = "general",
    requires_action_resolution: bool = True,
) -> tuple[str, NarrativeResponse | None]:
    """
    Centralized JSON parsing logic for all Gemini responses.
    Handles JSON extraction, parsing, and fallback logic.

    Args:
        raw_response_text: Raw text from Gemini API.
        context: Context of the parse (e.g., "general", "planning_block").
        requires_action_resolution: Whether actions in the structured response
            must be fully resolved by this parse step. This is set by the caller,
            not by the agent.
    Returns:
        tuple: (narrative_text, structured_data) where:
               - narrative_text is clean text for display
               - structured_data is parsed data (NarrativeResponse or None)
    """
    # Log raw response text for debugging (first 500 chars of extracted text)
    text_preview = raw_response_text[:500]
    preview_suffix = "..." if len(raw_response_text) > 500 else ""
    logging_util.debug(
        f"[{context}] Raw response text ({len(raw_response_text)} chars): "
        f"{text_preview}{preview_suffix}"
    )

    # Use the existing robust parsing logic
    response_text, structured_response = parse_structured_response(
        raw_response_text,
        requires_action_resolution=requires_action_resolution,
    )

    return response_text, structured_response


def _process_structured_response(
    raw_response_text: str,
    expected_entities: list[str],
    requires_action_resolution: bool = True,
) -> tuple[str, NarrativeResponse | None]:
    """
    Process structured JSON response and validate entity coverage.
    Args:
        raw_response_text: Raw response from API
        expected_entities: List of expected entity names
        requires_action_resolution: Whether action_resolution is required.
    Returns:
        tuple: (response_text, structured_response) where structured_response is NarrativeResponse or None
    """
    # Use centralized parsing logic
    response_text, structured_response = _parse_gemini_response(
        raw_response_text,
        context="structured_response",
        requires_action_resolution=requires_action_resolution,
    )

    # Validate structured response coverage
    if isinstance(structured_response, NarrativeResponse):
        coverage_validation = validate_entity_coverage(
            structured_response, expected_entities
        )
        logging_util.info(
            f"STRUCTURED_GENERATION: Coverage rate {coverage_validation['coverage_rate']:.2f}, "
            f"Schema valid: {coverage_validation['schema_valid']}"
        )

        if not coverage_validation["schema_valid"]:
            logging_util.warning(
                f"STRUCTURED_GENERATION: Missing from schema: {coverage_validation['missing_from_schema']}"
            )

        # State updates are now handled via structured_response object only
        # Legacy STATE_UPDATES_PROPOSED text blocks are no longer used in JSON mode
    else:
        logging_util.warning(
            "STRUCTURED_GENERATION: Failed to parse JSON response, falling back to plain text"
        )

    return response_text, structured_response


# Global lock for per-run escalation counters
_ESCALATION_LOCK = threading.Lock()


def _validate_entity_tracking(
    response_text: str, expected_entities: list[str], game_state: GameState
) -> str:
    """
    Validate that the narrative includes all expected entities.

    Args:
        response_text: Generated narrative text
        expected_entities: List of expected entity names
        game_state: Current GameState object

    Returns:
        str: Response text with debug validation if in debug mode
    """
    validator = NarrativeSyncValidator()
    validation_result = validator.validate(
        narrative_text=response_text,
        expected_entities=expected_entities,
        location=game_state.world_data.get("current_location_name", "Unknown"),
    )

    if not validation_result.all_entities_present:
        # Per-run escalation: keep logs INFO by default; escalate when spammy.
        # Each evidence run starts a fresh server process, so module-level counts are per-run.
        with _ESCALATION_LOCK:
            if not hasattr(_validate_entity_tracking, "_counts"):
                _validate_entity_tracking._counts = {}  # type: ignore[attr-defined]
            counts: dict[str, int] = _validate_entity_tracking._counts  # type: ignore[attr-defined]
            counts["ENTITY_TRACKING_VALIDATION"] = (
                counts.get("ENTITY_TRACKING_VALIDATION", 0) + 1
            )
            n = counts["ENTITY_TRACKING_VALIDATION"]

        if n >= 10:
            log_fn = logging_util.error
        elif n >= 3:
            log_fn = logging_util.warning
        else:
            log_fn = logging_util.info

        log_fn(
            "ENTITY_TRACKING_VALIDATION: Narrative failed entity validation (count=%d)",
            n,
        )
        log_fn("Missing entities: %s", validation_result.entities_missing)
        if validation_result.warnings:
            for warning in validation_result.warnings:
                log_fn("Validation warning: %s", warning)

    # Debug validation is now handled via structured_response.debug_info
    # No longer append debug content to narrative text in JSON mode

    return response_text


def _log_token_count(
    model_name: str,
    user_prompt_contents: list[Any],
    system_instruction_text: str | None = None,
    provider_name: str = constants.DEFAULT_LLM_PROVIDER,
) -> None:
    """Helper function to count and log the number of tokens being sent, with a breakdown.

    Also warns when approaching output token limits to prevent truncation issues.
    """
    try:
        prompt_tokens, system_tokens = _calculate_prompt_and_system_tokens(
            user_prompt_contents, system_instruction_text, provider_name, model_name
        )
        total_tokens = prompt_tokens + system_tokens

        current_output_limit = _get_safe_output_token_limit(
            model_name, prompt_tokens, system_tokens
        )
        logging_util.debug(
            f"🔍 TOKEN_ANALYSIS: Sending {total_tokens} input tokens to API (Prompt: {prompt_tokens or 0}, System: {system_tokens or 0})"
        )
        logging_util.debug(
            f"🔍 TOKEN_LIMITS: Output limit set to {current_output_limit} tokens (conservative limit, API max: 65535)"
        )

        model_info_msg = (
            f"🔍 MODEL_INFO: Using provider '{provider_name}', model '{model_name}'"
        )
        logging_util.info(model_info_msg)

    except Exception as e:
        logging_util.warning(f"Could not count tokens before API call: {e}")


def _check_explicit_cache_hit(
    response: Any, cache_name: str | None, campaign_id: str
) -> bool | None:
    """
    Check if explicit cache was hit and log warning if cache miss detected.

    Args:
        response: LLM response object with usage_metadata
        cache_name: The cache name that was used
        campaign_id: Campaign identifier for logging
    """
    if not cache_name:
        return None

    # Extract usage metadata from response
    if not hasattr(response, "usage_metadata"):
        return None

    usage = response.usage_metadata

    # Safely extract cached token count
    cached_tokens = 0
    try:
        cached_tokens = int(getattr(usage, "cached_content_token_count", 0) or 0)
    except (TypeError, ValueError):
        cached_tokens = 0

    prompt_tokens = 0
    try:
        prompt_tokens = int(getattr(usage, "prompt_token_count", 0) or 0)
    except (TypeError, ValueError):
        prompt_tokens = 0

    # Test hook: force a cache miss for validation scenarios
    if os.environ.get("FORCE_EXPLICIT_CACHE_MISS", "").lower() == "true":
        logging_util.warning(
            f"🚨 EXPLICIT_CACHE_FORCED_MISS: campaign={campaign_id}, cache_name={cache_name} "
            f"(test hook enabled)"
        )
        return False

    # Log warning if cached_tokens==0, but do NOT treat as a hard miss requiring retry.
    # Gemini sporadically returns cached_content_token_count=0 even when cache is active
    # (e.g., propagation delay immediately after a rebuild). Retrying on this soft signal
    # triggers an unnecessary 80k-token full-context call and nukes the cache via reset_cache().
    # Hard misses (CachedContent not found / PERMISSION_DENIED) are handled in the except block.
    if cached_tokens == 0:
        logging_util.warning(
            f"🚨 EXPLICIT_CACHE_NOT_HIT: campaign={campaign_id}, cache_name={cache_name}, "
            f"cached_tokens=0, prompt_tokens={prompt_tokens}, cache_hit_rate=0%. "
            f"Soft miss — returning response without retry (REV-wz2)."
        )

    return True


def _call_llm_api_with_explicit_cache(
    gemini_request: LLMRequest,
    campaign_id: str,
    model_name: str,
    system_instruction_text: str | None = None,
    provider_name: str = constants.DEFAULT_LLM_PROVIDER,
    temperature: float | None = None,
    force_tool_mode: str | None = None,
    user_api_key: str | None = None,
    user_id: UserId | None = None,
    is_think_mode: bool = False,
) -> Any:
    """
    Call LLM API with explicit caching for unchanging story entries.

    Args:
        gemini_request: LLMRequest with all data
        campaign_id: Campaign identifier for cache management
        model_name: Model to use
        system_instruction_text: System instructions
        provider_name: LLM provider name
        temperature: Sampling temperature
        force_tool_mode: Tool calling mode override
        user_api_key: Optional API key for BYOK override
        user_id: User ID for OpenClaw gateway lookup

    Returns:
        Provider response object
    """
    # Get user_id from gemini_request if not provided
    if user_id is None:
        user_id = getattr(gemini_request, "user_id", None)

    cache_mgr = get_cache_manager(campaign_id)
    story_count = len(gemini_request.story_history)

    # N-1 promotion: if a previous rebuild created a pending cache,
    # promote it now (the new cache has had at least one request cycle
    # to propagate on Gemini's side).
    if cache_mgr.has_pending_cache():
        client = gemini_provider.get_client(api_key=user_api_key)
        cache_mgr.promote_pending_cache(client)

    _merge_explicit_cache_payload = _merge_cache_payloads

    # Check if cache needs rebuild
    if cache_mgr.should_rebuild(
        story_count,
        requires_code_execution=(model_name in constants.MODELS_WITH_CODE_EXECUTION),
        model_name=model_name,
    ):
        # Split content into cacheable and uncacheable parts
        # Cache all existing story entries; the current user action stays uncacheable.
        entries_to_cache = story_count

        logging_util.info(
            f"📦 CACHE_BUILD: campaign={campaign_id}, total_entries={story_count}, "
            f"caching={entries_to_cache}, previously_cached={cache_mgr.cached_entry_count}, "
            f"threshold={cache_mgr.REBUILD_THRESHOLD}"
        )
        cacheable_json, uncacheable_json = gemini_request.to_explicit_cache_parts(
            cached_entry_count=entries_to_cache
        )

        # Create cache with system_instruction in CachedContentConfig (required by Gemini API)
        # Story entries go in contents, system_instruction goes in config.system_instruction
        client = gemini_provider.get_client(api_key=user_api_key)

        # FIX BUG #2 (BEAD-5bw): Cache sends two separate JSON objects instead of one merged
        # Old approach: Cache cacheable_json, send uncacheable_json separately = 2 JSON objects
        # New approach: Cache only story entries, send MERGED JSON as live content = 1 JSON object
        #
        # Extract old story entries to cache (not as JSON, just the entries themselves)
        old_story_entries = cacheable_json.get("story_history", [])

        # Serialize old entries as individual text chunks for caching
        cached_story_parts = [
            json.dumps(entry, indent=2, default=json_default_serializer)
            for entry in old_story_entries
        ]

        # Apply code_execution override to system instruction BEFORE caching
        # This ensures the cached system instruction has the correct dice guidance
        cache_system_instruction = apply_code_execution_system_instruction(
            system_instruction_text, model_name
        )

        # CRITICAL FIX (DICE-s8u): Include code_execution tool in cache for models that support it
        # When using cached_content, Gemini API rejects tools in GenerateContent config.
        # Tools MUST be in the cache itself for code_execution to work.
        cache_tools = None
        if model_name in constants.MODELS_WITH_CODE_EXECUTION:
            cache_tools = [types.Tool(code_execution={})]
            logging_util.info(
                f"📦 CACHE_CODE_EXECUTION: Adding code_execution tool to cache "
                f"for model={model_name}"
            )

        # Build full content for retry (centralized function for cache failure scenarios)
        full_content_for_retry = build_full_content_for_retry(gemini_request)

        # BYOK CACHE FIX: Wrap cache creation to fall back to non-cached generation on failure
        try:
            cache_result = cache_mgr.create_cache(
                client=client,
                system_instruction=cache_system_instruction or "",
                story_entries=cached_story_parts,  # Cache individual story entries, NOT full JSON
                model_name=model_name,
                actual_story_count=entries_to_cache,  # Track actual story entries cached
                tools=cache_tools,  # Include code_execution tool if model supports it
            )
            # N-1 deferral: cache_result.cache_name is None for first-ever (no old cache),
            # or the old cache name for rebuilds (still valid this request).
            # Use it directly — no conditional needed.
            cache_name = cache_result.cache_name
            use_system_instruction = (
                cache_name is None
            )  # True only when no cache available
        except Exception as e:
            error_msg = str(e)
            logging_util.warning(
                f"🚨 CACHE_CREATE_FAILED: campaign={campaign_id}, error='{error_msg}'. "
                "Falling back to non-cached generation."
            )
            cache_mgr.reset_cache(client)
            # Fall back to non-cached generation
            return _call_llm_api(
                prompt_contents=[full_content_for_retry],
                model_name=model_name,
                current_prompt_text_for_logging=f"CacheCreateFallback: {campaign_id}",
                system_instruction_text=system_instruction_text,
                provider_name=provider_name,
                temperature=temperature,
                force_tool_mode=force_tool_mode,
                cache_name=None,
                is_think_mode=is_think_mode,
                user_api_key=user_api_key,
                user_id=user_id,
            )

        # Merge cacheable + uncacheable into ONE complete JSON object
        # This is what the model expects - a single JSON document with all context
        merged_json = _merge_explicit_cache_payload(cacheable_json, uncacheable_json)

        # Build the single merged content string
        merged_content_string = json.dumps(
            merged_json, indent=2, default=json_default_serializer
        )

        # Call API with cache reference
        # NOTE: When using cache, do NOT pass system_instruction or tools (Gemini API constraint)
        try:
            response = _call_llm_api(
                prompt_contents=[
                    merged_content_string
                ],  # Single merged JSON (Bug #2 fix)
                model_name=model_name,
                current_prompt_text_for_logging=f"ExplicitCache: {campaign_id}",
                system_instruction_text=system_instruction_text
                if use_system_instruction
                else None,
                provider_name=provider_name,
                temperature=temperature,
                force_tool_mode=None
                if cache_name is not None
                else force_tool_mode,  # Tools baked in cache; restore when uncached (N-1 deferred)
                cache_name=cache_name,
                is_think_mode=is_think_mode,
                user_api_key=user_api_key,
                user_id=user_id,
            )
        except Exception as e:
            error_msg = str(e)
            if (
                "CachedContent not found" in error_msg
                or "PERMISSION_DENIED" in error_msg
            ):
                logging_util.warning(
                    f"🚨 EXPLICIT_CACHE_NOT_HIT: campaign={campaign_id}, cache_name={cache_name} "
                    f"error='{error_msg}'. Retrying without cache for full context."
                )
                logging_util.warning(
                    f"🚨 EXPLICIT_CACHE_RETRY: campaign={campaign_id}, cache_name={cache_name} "
                    "missed. Retrying without cache for full context."
                )
                # Invalidate stale cache to prevent repeated failures on subsequent requests
                client = gemini_provider.get_client(api_key=user_api_key)
                cache_mgr.reset_cache(client)
                # CRITICAL FIX: Use full_content_for_retry, NOT uncacheable_string
                # When cache fails, we need ALL content (cacheable + uncacheable) not just recent entries
                return _call_llm_api(
                    prompt_contents=[full_content_for_retry],
                    model_name=model_name,
                    current_prompt_text_for_logging=f"ExplicitCacheRetry: {campaign_id}",
                    system_instruction_text=system_instruction_text,
                    provider_name=provider_name,
                    temperature=temperature,
                    force_tool_mode=force_tool_mode,
                    cache_name=None,
                    is_think_mode=is_think_mode,
                    user_api_key=user_api_key,
                    user_id=user_id,
                )
            raise

        # Log cache hit status. Retry only happens above on hard API errors (except block).
        # cached_tokens==0 is a soft metric — do not retry (REV-wz2).
        cache_check = _check_explicit_cache_hit(response, cache_name, campaign_id)
        if cache_check is False:
            logging_util.warning(
                f"🚨 EXPLICIT_CACHE_RETRY_FORCED_MISS: campaign={campaign_id}, "
                f"cache_name={cache_name}. Retrying without cache for test validation."
            )
            return _call_llm_api(
                prompt_contents=[full_content_for_retry],
                model_name=model_name,
                current_prompt_text_for_logging=f"ExplicitCacheRetryForcedMiss: {campaign_id}",
                system_instruction_text=system_instruction_text,
                provider_name=provider_name,
                temperature=temperature,
                force_tool_mode=force_tool_mode,
                cache_name=None,
                is_think_mode=is_think_mode,
                user_api_key=user_api_key,
                user_id=user_id,
            )
        return response

    # Reuse existing cache
    cache_name = cache_mgr.get_cache_name()
    cached_entry_count = cache_mgr.cached_entry_count

    logging_util.info(
        f"📦 CACHE_REUSE: campaign={campaign_id}, cache={cache_name}, "
        f"entries={story_count}, cached={cached_entry_count}"
    )

    # Split content based on cached entry count
    cacheable_json, uncacheable_json = gemini_request.to_explicit_cache_parts(
        cached_entry_count=cached_entry_count
    )

    # FIX BUG #2 (BEAD-5bw): Merge cacheable + uncacheable into one JSON object
    # Merge cacheable + uncacheable into ONE complete JSON object
    merged_json = _merge_explicit_cache_payload(cacheable_json, uncacheable_json)

    # Build the single merged content string
    merged_content_string = json.dumps(
        merged_json, indent=2, default=json_default_serializer
    )

    # Build full content for retry (centralized function for cache failure scenarios)
    full_content_for_retry = build_full_content_for_retry(gemini_request)

    # Call API with cache reference
    # NOTE: When using cache, do NOT pass system_instruction or tools (Gemini API constraint)
    try:
        response = _call_llm_api(
            prompt_contents=[merged_content_string],  # Single merged JSON (Bug #2 fix)
            model_name=model_name,
            current_prompt_text_for_logging=f"ExplicitCache: {campaign_id}",
            system_instruction_text=None,  # In cache
            provider_name=provider_name,
            temperature=temperature,
            force_tool_mode=None,  # Tools baked in cache
            cache_name=cache_name,
            is_think_mode=is_think_mode,
            user_api_key=user_api_key,
            user_id=user_id,
        )
    except Exception as e:
        error_msg = str(e)
        if "CachedContent not found" in error_msg or "PERMISSION_DENIED" in error_msg:
            logging_util.warning(
                f"🚨 EXPLICIT_CACHE_NOT_HIT: campaign={campaign_id}, cache_name={cache_name} "
                f"error='{error_msg}'. Retrying without cache for full context."
            )
            logging_util.warning(
                f"🚨 EXPLICIT_CACHE_RETRY: campaign={campaign_id}, cache_name={cache_name} "
                "missed. Retrying without cache for full context."
            )
            # Invalidate stale cache to prevent repeated failures on subsequent requests
            client = gemini_provider.get_client(api_key=user_api_key)
            cache_mgr.reset_cache(client)
            # CRITICAL FIX: Use full_content_for_retry, NOT uncacheable_string
            # When cache fails, we need ALL content (cacheable + uncacheable) not just recent entries
            return _call_llm_api(
                prompt_contents=[full_content_for_retry],
                model_name=model_name,
                current_prompt_text_for_logging=f"ExplicitCacheRetry: {campaign_id}",
                system_instruction_text=system_instruction_text,
                provider_name=provider_name,
                temperature=temperature,
                force_tool_mode=force_tool_mode,
                cache_name=None,
                is_think_mode=is_think_mode,
                user_api_key=user_api_key,
                user_id=user_id,
            )
        raise

    # Log cache hit status. Retry only happens above on hard API errors (except block).
    # cached_tokens==0 is a soft metric — do not retry (REV-wz2).
    cache_check = _check_explicit_cache_hit(response, cache_name, campaign_id)
    if cache_check is False:
        logging_util.warning(
            f"🚨 EXPLICIT_CACHE_RETRY_FORCED_MISS: campaign={campaign_id}, "
            f"cache_name={cache_name}. Retrying without cache for test validation."
        )
        return _call_llm_api(
            prompt_contents=[full_content_for_retry],
            model_name=model_name,
            current_prompt_text_for_logging=f"ExplicitCacheRetryForcedMiss: {campaign_id}",
            system_instruction_text=system_instruction_text,
            provider_name=provider_name,
            temperature=temperature,
            force_tool_mode=force_tool_mode,
            cache_name=None,
            is_think_mode=is_think_mode,
            user_api_key=user_api_key,
            user_id=user_id,
        )
    return response


def _call_llm_api_with_llm_request(
    gemini_request: LLMRequest,
    model_name: str,
    system_instruction_text: str | None = None,
    provider_name: str = constants.DEFAULT_LLM_PROVIDER,
    temperature: float | None = None,
    force_tool_mode: str | None = None,
    is_think_mode: bool = False,
    user_id: UserId | None = None,
) -> Any:
    """
    Calls LLM API with structured JSON from LLMRequest.

    This function sends the JSON structure to Gemini API as a formatted string.
    The Gemini API expects string content, so we convert the structured data
    to a JSON string for proper communication.

    Explicit Caching (always enabled for Gemini):
    - Routes to _call_llm_api_with_explicit_cache() for cache-optimized flow
    - Splits content into cacheable (static + old entries) and uncacheable parts
    - Achieves 100% cache hit frequency vs 30% with implicit caching
    - Provides 78% cost reduction vs 26% with implicit caching (3x improvement)

    Args:
        gemini_request: LLMRequest object with structured data
        model_name: Model to use for API call
        system_instruction_text: System instructions (optional)
        provider_name: LLM provider name
        temperature: Sampling temperature
        force_tool_mode: Tool calling mode override

    Returns:
        Gemini API response object

    Raises:
        TypeError: If parameters are of incorrect type
        ValueError: If parameters are invalid
        LLMRequestError: If LLMRequest validation fails
    """
    # Input validation - critical for API stability
    if gemini_request is None:
        raise TypeError("gemini_request cannot be None")

    if not isinstance(gemini_request, LLMRequest):
        raise TypeError(
            f"gemini_request must be LLMRequest instance, got {type(gemini_request)}"
        )

    if not model_name or not isinstance(model_name, str):
        raise ValueError(
            f"model_name must be non-empty string, got {type(model_name)}: {model_name}"
        )

    if system_instruction_text is not None and not isinstance(
        system_instruction_text, str
    ):
        raise TypeError(
            f"system_instruction_text must be string or None, got {type(system_instruction_text)}"
        )

    if (
        constants.EXPLICIT_CACHE_ENABLED
        and provider_name == constants.LLM_PROVIDER_GEMINI
        and gemini_request.game_state
        and isinstance(gemini_request.game_state, dict)
    ):
        campaign_id = gemini_request.game_state.get("campaign_id")
        if campaign_id and gemini_request.story_history:
            logging_util.info(
                f"📦 EXPLICIT_CACHE: campaign={campaign_id}, "
                f"entries={len(gemini_request.story_history)}"
            )
            resolved_user_id = (
                user_id if user_id is not None else gemini_request.user_id
            )
            user_api_key = _get_user_api_key_for_provider(
                user_id=resolved_user_id,
                provider_name=provider_name,
            )
            return _call_llm_api_with_explicit_cache(
                gemini_request=gemini_request,
                campaign_id=campaign_id,
                model_name=model_name,
                system_instruction_text=system_instruction_text,
                provider_name=provider_name,
                temperature=temperature,
                force_tool_mode=force_tool_mode,
                user_api_key=user_api_key,
                user_id=resolved_user_id,
                is_think_mode=is_think_mode,
            )

    resolved_user_id = user_id if user_id is not None else gemini_request.user_id
    user_api_key = _get_user_api_key_for_provider(
        user_id=resolved_user_id,
        provider_name=provider_name,
    )

    # Log validation success for debugging
    logging_util.debug(
        f"Input validation passed for LLMRequest with user_id: {gemini_request.user_id}, "
        f"model: {model_name}"
    )

    # Convert LLMRequest to JSON for API call
    try:
        json_data = gemini_request.to_json()
    except Exception as e:
        logging_util.error(f"Failed to convert LLMRequest to JSON: {e}")
        raise ValueError(f"LLMRequest serialization failed: {e}") from e

    # Validate JSON data structure before API call
    if not isinstance(json_data, dict):
        raise ValueError(
            f"Expected dict from LLMRequest.to_json(), got {type(json_data)}"
        )

    # Ensure critical fields are present
    required_fields = ["user_action", "game_mode", "user_id"]
    missing_fields = [field for field in required_fields if field not in json_data]
    if missing_fields:
        raise ValueError(f"Missing required fields in JSON data: {missing_fields}")

    logging_util.debug(f"JSON validation passed with {len(json_data)} fields")

    # Add priority instruction as JSON field when user_action exists
    # This guides the LLM to focus on current user action over story_history AND game_state
    # while preserving the JSON contract (per CLAUDE.md "JSON Schema Over Text Instructions")
    user_action = json_data.get("user_action")
    if user_action and str(user_action).strip():
        # Add priority instruction directly to JSON structure (not text wrapping)
        # This preserves the JSON contract while guiding LLM behavior
        json_data["priority_instruction"] = (
            "CRITICAL: Respond to user_action field, NOT story_history or game_state entries. "
            "story_history and game_state are context only. Focus exclusively on current user_action."
        )
        json_data["message_type"] = "story_continuation"

        # Log user_action for debugging (DEBUG level to avoid PII leaks)
        logging_util.debug(
            "USER_ACTION preview: %s...",
            str(user_action)[:200],
        )

    # Convert JSON dict to formatted string for Gemini API
    # The API expects string content, not raw dicts
    # Uses indent=2 for readability (matches origin/main format)
    # Uses centralized json_default_serializer from mvp_site.serialization
    json_string = json.dumps(json_data, indent=2, default=json_default_serializer)

    prompt_size_bytes = len(json_string.encode("utf-8"))
    if prompt_size_bytes > MAX_PAYLOAD_SIZE:
        raise PayloadTooLargeError(
            f"Prompt payload too large: {prompt_size_bytes} bytes exceeds limit of {MAX_PAYLOAD_SIZE} bytes"
        )

    # Safe user_action access for logging (handles None/empty string for initial story)
    user_action_preview = (
        (gemini_request.user_action or "")[:100]
        if gemini_request.user_action
        else "initial_story"
    )

    # Send the structured JSON as string to the API
    return _call_llm_api(
        [json_string],  # Send JSON as formatted string
        model_name,
        f"LLMRequest: {user_action_preview}...",  # Logging
        system_instruction_text,
        provider_name,
        temperature=temperature,
        force_tool_mode=force_tool_mode,
        is_think_mode=is_think_mode,
        user_api_key=user_api_key,
        user_id=user_id,
    )


def _get_user_api_key_for_provider(
    user_id: UserId | None, provider_name: str
) -> str | None:
    """Extract a BYOK API key for the selected provider from user settings."""
    key_field = _BYOK_PROVIDER_API_KEY_FIELDS.get(provider_name)
    if user_id is None or key_field is None:
        return None

    user_settings = get_user_settings(user_id)
    if not isinstance(user_settings, dict):
        return None

    raw_key = user_settings.get(key_field)
    if raw_key is None or not isinstance(raw_key, str):
        return None

    key = raw_key.strip()
    if key == "":
        return None

    logging_util.debug(
        "BYOK key loaded for provider=%s user=%s", provider_name, user_id
    )
    return key


def _safe_openclaw_gateway_url_for_log(raw_url: str) -> str:
    try:
        parts = urlsplit(raw_url)
        if parts.scheme and parts.hostname:
            # Use hostname (not netloc) to exclude any embedded userinfo credentials.
            host = parts.hostname
            if parts.port:
                host = f"{host}:{parts.port}"
            return f"{parts.scheme}://{host}"
    except Exception:
        pass

    digest = hashlib.sha256(raw_url.encode("utf-8", errors="replace")).hexdigest()[:8]
    return f"<redacted:{digest}>"


def _get_openclaw_gateway_url(user_id: UserId | None, provider_name: str) -> str | None:
    """Read user-configured OpenClaw gateway URL (e.g. Tailscale Funnel / Cloudflare Tunnel)."""
    if user_id is None or provider_name != constants.LLM_PROVIDER_OPENCLAW:
        return None
    user_settings = get_user_settings(user_id)
    if not isinstance(user_settings, dict):
        return None
    raw_url = user_settings.get("openclaw_gateway_url")
    if not isinstance(raw_url, str) or not raw_url.strip():
        return None

    url, error = validate_openclaw_gateway_url(raw_url)
    if error is None:
        return url

    logging_util.warning(
        "Ignoring invalid OpenClaw gateway URL %s for user=%s provider=%s: %s",
        _safe_openclaw_gateway_url_for_log(raw_url),
        user_id,
        provider_name,
        error,
    )
    return None


def _get_openclaw_gateway_token(
    user_id: UserId | None, provider_name: str
) -> str | None:
    """Read user-configured OpenClaw gateway token."""
    if user_id is None or provider_name != constants.LLM_PROVIDER_OPENCLAW:
        return None

    user_settings = get_user_settings(user_id)
    if not isinstance(user_settings, dict):
        return None

    raw_token = user_settings.get("openclaw_gateway_token")
    if not isinstance(raw_token, str) or not raw_token.strip():
        return None

    token = raw_token.strip()
    if not token:
        return None

    return token


def _get_openclaw_gateway_port(
    user_id: UserId | None, provider_name: str
) -> int | None:
    """Read user-configured OpenClaw localhost gateway port."""
    if user_id is None or provider_name != constants.LLM_PROVIDER_OPENCLAW:
        return None

    user_settings = get_user_settings(user_id)
    if not isinstance(user_settings, dict):
        return None

    raw_port = user_settings.get("openclaw_gateway_port")
    port: int | None = None
    if isinstance(raw_port, bool):
        port = None
    elif isinstance(raw_port, int):
        port = raw_port
    elif isinstance(raw_port, str) and raw_port.strip().isdigit():
        port = int(raw_port.strip())

    if port is None:
        return None
    if 1 <= port <= 65535:
        return port

    logging_util.warning(
        "Ignoring invalid OpenClaw gateway port %r for user=%s provider=%s",
        raw_port,
        user_id,
        provider_name,
    )
    return None


# --- Retry Configuration for Transient API Errors ---
# FAILED_PRECONDITION errors from Gemini are sometimes transient and succeed on retry.
# We retry these errors with exponential backoff and warn the user when retries occur.
GEMINI_RETRY_MAX_ATTEMPTS = 3
GEMINI_RETRY_TOOLFLOW_MAX_ATTEMPTS = 2
GEMINI_RETRY_BASE_DELAY_SECONDS = 2.0  # Base delay, doubles each attempt
GEMINI_RETRIABLE_STATUSES = {
    "FAILED_PRECONDITION"
}  # Status strings that should be retried


def _is_retriable_gemini_error(exception: Exception) -> bool:
    """Check if a Gemini API error is retriable (transient).

    Returns True for FAILED_PRECONDITION errors which are known to be
    intermittent on gemini-3-flash-preview model.
    """
    # Check for google.genai.errors.ClientError with retriable status
    if hasattr(exception, "status"):
        status = str(exception.status)
        if status in GEMINI_RETRIABLE_STATUSES:
            return True
    # Also check error message as fallback
    error_str = str(exception)
    if "FAILED_PRECONDITION" in error_str:
        return True
    return False


def _log_retry_attempt(
    attempt: int,
    max_attempts: int,
    exception: Exception,
    delay_seconds: float,
    model_name: str,
) -> None:
    """Log retry attempt with detailed error info."""
    error_status = getattr(exception, "status", "UNKNOWN")
    error_message = getattr(exception, "message", str(exception))
    logging_util.warning(
        f"🔄 GEMINI_RETRY: Attempt {attempt}/{max_attempts} failed | "
        f"model={model_name} | status={error_status} | message={error_message} | "
        f"retrying in {delay_seconds:.1f}s..."
    )


def _append_server_warning(structured_response: Any, warning_message: str) -> bool:
    """Append a server-generated system warning to debug_info.

    Returns True if the warning was added (not already present).
    """
    if not structured_response or not warning_message:
        return False

    if not isinstance(structured_response.debug_info, dict):
        structured_response.debug_info = {}

    server_warnings = structured_response.debug_info.get("_server_system_warnings", [])
    if not isinstance(server_warnings, list):
        server_warnings = []

    if warning_message in server_warnings:
        return False

    server_warnings.append(warning_message)
    structured_response.debug_info["_server_system_warnings"] = server_warnings
    return True


def _append_warning_to_debug_info(
    debug_info: dict,
    warning_message: str,
    log_message: str | None = None,
) -> bool:
    """
    Append a server-generated warning to debug_info._server_system_warnings.

    This helper works with raw debug_info dict (not structured_response).
    Use this when you have direct access to debug_info and need to add warnings.

    Args:
        debug_info: Raw debug_info dict (not structured_response)
        warning_message: Warning text to append (will be deduplicated)
        log_message: Optional log message for enforcement tracking

    Returns:
        True if warning was added, False if already present

    Example:
        >>> debug_info = {}
        >>> _append_warning_to_debug_info(
        ...     debug_info,
        ...     "⚠️ Dice Integrity Warning: No RNG usage detected",
        ...     "🚨 DICE-s8u ENFORCEMENT: Added fabrication warning"
        ... )
        True
    """
    if not isinstance(debug_info, dict) or not warning_message:
        return False

    server_warnings = debug_info.get("_server_system_warnings", [])
    if not isinstance(server_warnings, list):
        server_warnings = []

    if warning_message in server_warnings:
        return False

    server_warnings.append(warning_message)
    debug_info["_server_system_warnings"] = server_warnings

    if log_message:
        logging_util.warning(log_message)

    return True


def _add_api_retry_warning_to_response(
    api_response: Any,
    structured_response: Any,
) -> None:
    """Add user-visible warning if API request required retries.

    Checks for _retry_metadata on the API response and adds a warning
    to _server_system_warnings in the structured response's debug_info.
    This warns users about transient API issues similar to dice integrity warnings.
    """
    if not structured_response:
        return
    if not hasattr(api_response, "_retry_metadata"):
        return

    retry_metadata = api_response._retry_metadata
    if not retry_metadata:
        return

    # Add retry warning (similar format to dice integrity warnings)
    attempts = retry_metadata.get("attempts_made", 2)
    max_attempts = retry_metadata.get("max_attempts", GEMINI_RETRY_MAX_ATTEMPTS)
    warning_message = f"API retry required (attempt {attempts}/{max_attempts}) - transient error recovered"

    if _append_server_warning(structured_response, warning_message):
        logging_util.info(
            f"📢 Added API retry warning to user response: {warning_message}"
        )


def _call_llm_api(  # noqa: PLR0912, PLR0915
    prompt_contents: list[Any],
    model_name: str,
    current_prompt_text_for_logging: str | None = None,
    system_instruction_text: str | None = None,
    provider_name: str = constants.DEFAULT_LLM_PROVIDER,
    temperature: float | None = None,
    force_tool_mode: str | None = None,
    cache_name: str | None = None,
    is_think_mode: bool = False,
    user_api_key: str | None = None,
    user_id: UserId | None = None,
) -> Any:
    """
    Calls the configured LLM provider.

    Args:
        prompt_contents: The content to send to the API
        model_name: Primary model to use
        current_prompt_text_for_logging: Text for logging purposes (optional)
        system_instruction_text: System instructions (optional)
        provider_name: LLM provider name (gemini, openrouter, cerebras)
        temperature: Sampling temperature override
        force_tool_mode: Tool calling mode override
        cache_name: Explicit cache name for Gemini (optional)

    Returns:
        Provider-specific response object (Gemini, OpenRouter, or Cerebras)
    """
    if _is_mock_services_mode():
        logging_util.info("MOCK_SERVICES_MODE enabled - returning mock LLM response")

        mock_world_events = {
            "background_events": [
                {
                    "actor": "Harbor Master Alden",
                    "action": "issued an emergency curfew at the North Dock",
                    "location": "North Dock",
                    "event_type": "immediate",
                    "status": "pending",
                    "title": "Harbor master emergency curfew",
                    "discovery_condition": "player approaches the docks",
                    "estimated_discovery_turn": 4,
                    "player_impact": "Trade and movement are more tightly controlled tonight.",
                },
                {
                    "actor": "Captain Rhea",
                    "action": "redirected two courier routes away from the western gate",
                    "location": "Guild Ledger Office",
                    "event_type": "immediate",
                    "status": "pending",
                    "title": "Courier routes adjusted",
                    "discovery_condition": "hear travel rumors nearby",
                    "estimated_discovery_turn": 5,
                    "player_impact": "Some contacts may be harder to reach quickly.",
                },
                {
                    "actor": "Weather Ward",
                    "action": "reported unusual storms moving in from the east",
                    "location": "Weather Tower",
                    "event_type": "immediate",
                    "status": "discovered",
                    "title": "Weather warnings posted",
                    "discovery_condition": "conversation with local merchants",
                    "estimated_discovery_turn": 3,
                    "player_impact": "Road conditions and river crossings may worsen.",
                },
                {
                    "actor": "Syndicate Spokesman",
                    "action": "began covert talks with a faction envoy",
                    "location": "Old Quarter",
                    "event_type": "long_term",
                    "status": "pending",
                    "title": "Covert faction alignment shift",
                    "discovery_condition": "long-term rumors surface",
                    "estimated_discovery_turn": 12,
                    "player_impact": "Political pressure in district negotiations increases.",
                },
            ],
            "scene_event": {
                "type": "messenger_arrival",
                "actor": "Guild Messenger",
                "description": "A messenger arrives at the guild hall with a sealed dispatch for nearby caravans.",
                "action": "arrives with urgent trade dispatches",
                "location": "Guild Hall",
                "importance": "medium",
            },
        }
        mock_action_resolution = {
            "trigger": "mock_action",
            "player_intent": "deterministic follow-through",
            "original_input": "mock input",
            "resolution_type": "narrative",
            "mechanics": {
                "outcome": "story_continued",
                "rolls": [
                    {
                        "notation": "1d20+3",
                        "result": 15,
                        "total": 18,
                        "rolls": [15],
                        "raw_rolls": [15],
                        "purpose": "mock_check",
                        "dc": 12,
                        "dc_reasoning": "deterministic mock path",
                        "success": True,
                    }
                ],
            },
            "audit_flags": ["mock_response", "deterministic"],
            "reinterpreted": False,
        }

        # Ensure planning_block always has choices for thinking mode tests
        mock_choices = {
            "continue_forward": {
                "text": "Continue Forward",
                "description": "Continue with deterministic mock path continuation",
                "risk_level": "low",
                "notes": "Mock mode stable response for smoke test coverage",
            },
            "assess_situation": {
                "text": "Assess Situation",
                "description": "Strategic review of current tactical position",
                "risk_level": "none",
                "notes": "Thinking mode analysis option",
            },
            "prepare_action": {
                "text": "Prepare Next Action",
                "description": "Plan next tactical move",
                "risk_level": "low",
                "notes": "Forward planning option",
            },
        }

        mock_response_payload = {
            "narrative": (
                "Mock mode response: the turn advances on a deterministic path "
                "with a valid state progression and transparent planning block."
            ),
            "session_header": "Scene #Mock",
            "planning_block": {
                "thinking": "Mock mode active. Deterministic server path selected.",
                "choices": mock_choices,
            },
            "state_updates": {
                "game_state": {
                    "player_character_data": {
                        "name": "Mock Player",
                        "level": 1,
                        "experience": {"current": 42, "next_level": 100},
                    },
                    "combat_state": {"in_combat": False},
                    "world_events": mock_world_events,
                },
                "world_data": {"world_time": "0000-01-01T00:00:00Z"},
                "custom_campaign_state": {"mock_campaign_mode": True},
                "world_events": mock_world_events,
            },
            "action_resolution": mock_action_resolution,
            "debug_info": {
                "agent_mode": "mock",
                "mock_seed": "mock_service_deterministic",
            },
        }

        class MockResponse:
            def __init__(self):
                self.text = json.dumps(mock_response_payload)
                self.parts = []
                self.candidates = []
                self._tool_results = []
                self._tool_requests_executed = False

        # Confirm mock response has choices in planning_block
        pb = mock_response_payload.get("planning_block", {})
        choices_count = len(pb.get("choices", {}))
        logging_util.info(
            f"🧪 MOCK_MODE: Returning mock response with planning_block.choices ({choices_count} choices)"
        )

        return MockResponse()

    if current_prompt_text_for_logging:
        logging_util.debug(
            f"Calling LLM API with prompt ({len(current_prompt_text_for_logging)} chars): {str(current_prompt_text_for_logging)[:100]}..."
        )

    # Log token estimate for prompt
    all_prompt_text = []
    for p in prompt_contents:
        if isinstance(p, str):
            all_prompt_text.append(p)
        elif isinstance(p, dict):
            # Handle JSON data for logging purposes
            all_prompt_text.append(f"JSON({len(str(p))} chars)")

    if system_instruction_text is not None:
        all_prompt_text.append(system_instruction_text)

    combined_text = " ".join(all_prompt_text)
    log_with_tokens("Calling LLM API", combined_text, logging_util)

    current_selection = ProviderSelection(provider_name, model_name)
    try:
        prompt_tokens, system_tokens = _calculate_prompt_and_system_tokens(
            prompt_contents, system_instruction_text, provider_name, model_name
        )
        _log_token_count(
            model_name,
            prompt_contents,
            system_instruction_text,
            provider_name,
        )

        logging_util.info(f"Calling LLM provider/model: {provider_name}/{model_name}")

        safe_output_limit = _get_safe_output_token_limit(
            model_name,
            prompt_tokens,
            system_tokens,
        )

        # Use provided temperature or default to TEMPERATURE constant
        # Lower temperature (0.2) for deterministic tool calling in faction minigame
        effective_temperature = temperature if temperature is not None else TEMPERATURE

        # DIAGNOSTIC: Log which provider branch we're about to execute
        logging_util.info(
            f"🔍 CALL_LLM_API_DISPATCH: provider_name={provider_name}, "
            f"model_name={model_name}, "
            f"temperature={effective_temperature}, "
            f"is_gemini={provider_name == constants.LLM_PROVIDER_GEMINI}, "
            f"is_cerebras={provider_name == constants.LLM_PROVIDER_CEREBRAS}, "
            f"is_openrouter={provider_name == constants.LLM_PROVIDER_OPENROUTER}"
        )

        if provider_name == constants.LLM_PROVIDER_GEMINI:
            # Use get_dice_roll_strategy to determine the approach
            strategy = dice_strategy.get_dice_roll_strategy(model_name, provider_name)

            # CRITICAL FIX: Disable code_execution for thinking mode
            # Thinking mode is pure strategic planning with no dice rolls.
            # Code execution + thinking mode triggers FAILED_PRECONDITION in Gemini API.
            is_think_mode_detected = is_think_mode
            if is_think_mode_detected:
                logging_util.info(
                    "🧠 THINK_MODE_OVERRIDE: Disabling code_execution for pure strategic planning"
                )
                strategy = dice_strategy.DICE_STRATEGY_NATIVE_TWO_PHASE

            # Retry loop for transient errors (e.g., FAILED_PRECONDITION)
            # gemini-3 models must be single-pass (no retries) due to request shape constraints.
            response = None
            last_error = None
            retry_attempts_made = 0
            attempted_strategies = [strategy]
            effective_strategy = strategy
            max_attempts = (
                1
                if model_name.startswith("gemini-3")
                else GEMINI_RETRY_TOOLFLOW_MAX_ATTEMPTS
            )

            for attempt in range(1, max_attempts + 1):
                try:
                    if effective_strategy == dice_strategy.DICE_STRATEGY_CODE_EXECUTION:
                        # Gemini 3.x: code_execution + JSON together (single inference)
                        if attempt == 1:
                            logging_util.info(
                                f"🔍 CALL_LLM_API_GEMINI: code_execution strategy for {model_name}"
                            )
                        response = gemini_provider.generate_content_with_code_execution(
                            prompt_contents=prompt_contents,
                            model_name=model_name,
                            system_instruction_text=system_instruction_text,
                            temperature=effective_temperature,
                            safety_settings=SAFETY_SETTINGS,
                            json_mode_max_output_tokens=safe_output_limit,
                            cache_name=cache_name,
                            api_key=user_api_key,
                        )
                    else:
                        # native_two_phase: Gemini 2.x cannot combine tools + JSON mode.
                        # Use JSON-first tool_requests flow to match prompt documentation.
                        if attempt == 1:
                            logging_util.info(
                                f"🔍 CALL_LLM_API_GEMINI: json_first_tool_requests strategy for {model_name}"
                            )
                        response = gemini_provider.generate_content_with_native_tools(
                            prompt_contents=prompt_contents,
                            model_name=model_name,
                            system_instruction_text=system_instruction_text,
                            temperature=effective_temperature,
                            safety_settings=SAFETY_SETTINGS,
                            json_mode_max_output_tokens=safe_output_limit,
                            force_tool_mode=force_tool_mode,
                            cache_name=cache_name,
                            api_key=user_api_key,
                            native_tools=faction_state_util.build_native_tools_for_prompt_contents(
                                prompt_contents
                            ),
                        )
                    # Success! Break out of retry loop
                    break

                except Exception as api_error:
                    last_error = api_error
                    if _is_retriable_gemini_error(api_error) and attempt < max_attempts:
                        # Calculate exponential backoff delay
                        delay = GEMINI_RETRY_BASE_DELAY_SECONDS * (2 ** (attempt - 1))
                        _log_retry_attempt(
                            attempt,
                            max_attempts,
                            api_error,
                            delay,
                            model_name,
                        )
                        retry_attempts_made = attempt
                        time.sleep(delay)
                        # Continue to next attempt
                    else:
                        # Not retriable or max attempts reached - re-raise
                        raise

            # If we get here, response should be set (either first attempt or retry succeeded)
            if response is None:
                # This shouldn't happen, but handle it gracefully
                raise last_error or RuntimeError(
                    "No response from Gemini API after retries"
                )

            if effective_strategy == dice_strategy.DICE_STRATEGY_CODE_EXECUTION:
                response = _orchestrate_gemini_code_execution_tool_requests(
                    prompt_contents=prompt_contents,
                    response_1=response,
                    model_name=model_name,
                    system_instruction_text=system_instruction_text,
                    temperature=effective_temperature,
                    safety_settings=SAFETY_SETTINGS,
                    json_mode_max_output_tokens=safe_output_limit,
                    cache_name=cache_name,
                    user_api_key=user_api_key,
                )

            # Attach retry metadata to response for user warning
            # This will be picked up later to add a user-visible warning
            if retry_attempts_made > 0:
                logging_util.warning(
                    f"✅ GEMINI_RETRY_SUCCESS: Request succeeded on attempt {retry_attempts_made + 1}/{max_attempts} | "
                    f"model={model_name}"
                )
                # Attach metadata to response object for later warning generation
                response._retry_metadata = {
                    "attempts_made": retry_attempts_made + 1,
                    "max_attempts": max_attempts,
                    "model": model_name,
                    "initial_strategy": strategy,
                    "effective_strategy": effective_strategy,
                    "attempted_strategies": attempted_strategies,
                }

            # Log finish_reason for debugging truncated responses
            _log_gemini_response_metadata(response, model_name)

            # Log usage metadata (Gemini only).
            # NOTE: This non-streaming path is only hit by get_initial_story (campaign
            # creation). Gameplay uses continue_story_streaming which doesn't log here.
            # cached_tokens=0 is expected here because new campaigns have no cached story.
            if hasattr(response, "usage_metadata"):
                usage = response.usage_metadata

                # Coalesce None to 0 and ensure int type (handles MagicMock in tests)
                def safe_int(value, default=0):
                    """Convert to int, handling None and MagicMock objects."""
                    if value is None:
                        return default
                    try:
                        return int(value)
                    except (TypeError, ValueError):
                        return default

                usage_prompt_tokens = safe_int(getattr(usage, "prompt_token_count", 0))
                usage_cached_tokens = safe_int(
                    getattr(usage, "cached_content_token_count", 0)
                )
                usage_response_tokens = safe_int(
                    getattr(usage, "candidates_token_count", 0)
                )

                # Calculate cache hit rate (guard against division by zero)
                cache_hit_rate = (
                    (100 * usage_cached_tokens / usage_prompt_tokens)
                    if usage_prompt_tokens > 0
                    else 0
                )

                logging_util.info(
                    f"🔍 GEMINI_USAGE: "
                    f"prompt_tokens={usage_prompt_tokens}, "
                    f"cached_tokens={usage_cached_tokens}, "
                    f"response_tokens={usage_response_tokens}, "
                    f"cache_hit_rate={cache_hit_rate:.1f}%, "
                    f"model={model_name}"
                )

                # Cache miss warning is emitted by _check_explicit_cache_hit()

            # Log full response structure for debugging (Gemini only)
            if hasattr(response, "candidates") and response.candidates:
                try:
                    first_candidate = response.candidates[0]
                    finish_reason = getattr(first_candidate, "finish_reason", None)
                    safety_ratings = getattr(first_candidate, "safety_ratings", [])

                    # Extract safety rating summary
                    safety_summary = []
                    for rating in safety_ratings:
                        try:
                            category = str(getattr(rating, "category", "UNKNOWN"))
                            probability = str(getattr(rating, "probability", "UNKNOWN"))
                            safety_summary.append(f"{category}:{probability}")
                        except Exception as exc:
                            logging_util.debug("🔍 GEMINI_SAFETY_RATING_PARSE: %s", exc)
                            continue

                    # Count parts in response
                    parts_count = 0
                    if hasattr(first_candidate, "content") and hasattr(
                        first_candidate.content, "parts"
                    ):
                        parts_count = len(first_candidate.content.parts)

                    # Get text length
                    text_length = len(response.text) if hasattr(response, "text") else 0

                    logging_util.info(
                        f"🔍 GEMINI_RESPONSE_STRUCTURE: "
                        f"candidates={len(response.candidates)}, "
                        f"finish_reason={finish_reason}, "
                        f"parts={parts_count}, "
                        f"text_len={text_length}, "
                        f"safety={','.join(safety_summary) if safety_summary else 'none'}"
                    )
                except Exception as e:
                    # Don't let response structure logging break the flow
                    logging_util.debug(f"Could not log response structure: {e}")

            return response
        if provider_name == constants.LLM_PROVIDER_OPENROUTER:
            # JSON-first tool_requests flow (matches prompt documentation)
            # Phase 1: JSON with optional tool_requests, Phase 2: JSON with results
            # Avoids forced tool calls - LLM decides when dice are needed
            logging_util.info(
                f"🔍 CALL_LLM_API_OPENROUTER: json_first_tool_requests strategy for {model_name}"
            )
            return openrouter_provider.generate_content_with_tool_requests(
                prompt_contents=prompt_contents,
                model_name=model_name,
                system_instruction_text=system_instruction_text,
                temperature=effective_temperature,
                max_output_tokens=safe_output_limit,
                api_key=user_api_key,
            )
        if provider_name == constants.LLM_PROVIDER_CEREBRAS:
            # JSON-first tool_requests flow (matches prompt documentation)
            # Phase 1: JSON with optional tool_requests, Phase 2: JSON with results
            # Avoids forced tool calls - LLM decides when dice are needed
            logging_util.info(
                f"🔍 CALL_LLM_API_CEREBRAS: json_first_tool_requests strategy for {model_name}"
            )
            return cerebras_provider.generate_content_with_tool_requests(
                prompt_contents=prompt_contents,
                model_name=model_name,
                system_instruction_text=system_instruction_text,
                temperature=effective_temperature,
                max_output_tokens=safe_output_limit,
                api_key=user_api_key,
            )
        if provider_name == constants.LLM_PROVIDER_OPENCLAW:
            logging_util.info(
                f"🔍 CALL_LLM_API_OPENCLAW: json_first_tool_requests strategy for {model_name}"
            )
            gateway_port = _get_openclaw_gateway_port(user_id, provider_name)
            gateway_url = _get_openclaw_gateway_url(user_id, provider_name)
            gateway_token = _get_openclaw_gateway_token(user_id, provider_name)
            return openclaw_provider.generate_content_with_tool_requests(
                prompt_contents=prompt_contents,
                model_name=model_name,
                system_instruction_text=system_instruction_text,
                temperature=effective_temperature,
                max_output_tokens=safe_output_limit,
                api_key=user_api_key,
                gateway_port=gateway_port,
                gateway_url=gateway_url,
                gateway_token=gateway_token,
            )
        logging_util.error(
            f"🔍 CALL_LLM_API_UNSUPPORTED: provider_name={provider_name} is not supported!"
        )
        raise ValueError(f"Unsupported provider: {provider_name}")
    except ContextTooLargeError as e:
        logging_util.error(
            "Context too large for selected model. "
            "Reduce prompt size or choose a model with a larger context window."
        )
        raise LLMRequestError(str(e), status_code=422) from e
    except ValueError as e:
        message = str(e)
        if "context" in message.lower() or "too large" in message.lower():
            raise LLMRequestError(message, status_code=422) from e
        raise
    except Exception as e:
        error_message = str(e)
        status_code = None

        # Enhanced logging for ClientError (Gemini API) to capture detailed error information
        if hasattr(e, "__class__") and "ClientError" in e.__class__.__name__:
            try:
                # Extract full error details from ClientError
                details = getattr(e, "details", None)
                code = getattr(e, "code", None)
                status = getattr(e, "status", None)
                message = getattr(e, "message", None)

                logging_util.error(
                    f"🔍 GEMINI_CLIENT_ERROR_DETAILS: "
                    f"code={code}, "
                    f"status={status}, "
                    f"message={message}"
                )

                # Log full error dict in pretty format for easier debugging
                if details and isinstance(details, dict):
                    logging_util.error(
                        f"🔍 GEMINI_ERROR_FULL_JSON:\n{json.dumps(details, indent=2)}"
                    )

                    # Check for specific precondition failures in nested details
                    error_dict = details.get("error", {})
                    error_details = error_dict.get("details", [])

                    if error_details:
                        logging_util.error(
                            f"🔍 GEMINI_ERROR_NESTED_DETAILS: {len(error_details)} detail(s) found"
                        )

                        # Log any field violations or specific constraints
                        for i, detail in enumerate(error_details):
                            if isinstance(detail, dict):
                                detail_type = detail.get("@type", "unknown")
                                reason = detail.get("reason", "not specified")
                                domain = detail.get("domain", "not specified")
                                logging_util.error(
                                    f"🔍 GEMINI_ERROR_DETAIL[{i}]: "
                                    f"type={detail_type}, "
                                    f"reason={reason}, "
                                    f"domain={domain}"
                                )
            except Exception as detail_err:
                logging_util.error(
                    f"Failed to extract ClientError details: {detail_err}"
                )

        if hasattr(e, "status_code"):
            status_code = e.status_code
        elif hasattr(e, "code"):
            # Ensure code is an integer (API may return unexpected types)
            try:
                status_code = int(e.code)
            except (TypeError, ValueError):
                status_code = None
        elif hasattr(e, "response") and hasattr(e.response, "status_code"):
            status_code = e.response.status_code
        elif "503" in error_message:
            status_code = 503
        elif "429" in error_message:
            status_code = 429

        if status_code in (503, 429):
            human_reason = (
                "service unavailable" if status_code == 503 else "rate limited"
            )
            logging_util.error(
                f"Provider {current_selection.provider}/{current_selection.model} {human_reason}: {error_message}"
            )
            raise LLMRequestError(
                f"LLM provider error ({status_code}): {human_reason}. Please try again shortly.",
                status_code=status_code,
            ) from e

        # Enhanced error logging for Gemini API errors (google.genai.errors.APIError)
        # Extract detailed information to help diagnose issues like FAILED_PRECONDITION
        error_details = []
        if hasattr(e, "details"):
            error_details.append(f"details={e.details}")
            # Extract nested debug info from details (Google RPC error details)
            # Format: {"error": {"details": [{"@type": "...DebugInfo", "detail": "..."}]}}
            try:
                details_obj = e.details
                if isinstance(details_obj, dict):
                    nested_details = details_obj.get("error", {}).get("details", [])
                    if not nested_details and "details" in details_obj:
                        nested_details = details_obj.get("details", [])
                    for detail_item in nested_details:
                        if isinstance(detail_item, dict):
                            detail_type = detail_item.get("@type", "unknown")
                            detail_msg = detail_item.get(
                                "detail", detail_item.get("message", "")
                            )
                            if detail_msg:
                                error_details.append(
                                    f"rpc_detail[{detail_type}]={detail_msg}"
                                )
            except Exception as exc:
                logging_util.warning(
                    f"Failed to parse nested Gemini error details: {exc}"
                )
        if hasattr(e, "status"):
            error_details.append(f"status={e.status}")
        if hasattr(e, "message"):
            error_details.append(f"message={e.message}")
        if hasattr(e, "response"):
            resp = e.response
            # Check both that headers attr exists AND is not None to avoid TypeError
            if hasattr(resp, "headers") and resp.headers is not None:
                # Log request ID and other useful headers
                headers_to_log = ["x-request-id", "x-goog-request-id", "x-debug-info"]
                for h in headers_to_log:
                    if h in resp.headers:
                        error_details.append(f"{h}={resp.headers[h]}")
            # Also try to log raw response text for additional context
            # Wrapped in try/except to prevent masking original exception on encoding issues
            try:
                if hasattr(resp, "text") and resp.text:
                    # Only log if different from details (avoid duplication)
                    resp_text = resp.text[:500]  # Limit to first 500 chars
                    if "Precondition check failed" not in str(error_details):
                        error_details.append(f"raw_response={resp_text}")
            except Exception as exc:
                logging_util.warning(
                    f"Failed to read Gemini response text for diagnostics: {exc}"
                )

        detail_str = (
            " | ".join(error_details) if error_details else "no additional details"
        )
        logging_util.error(
            f"🔥🔴 Non-recoverable error with model {current_selection.model}: {e}"
        )
        logging_util.error(f"🔥🔴 Error diagnostics: code={status_code} | {detail_str}")
        raise


def _log_gemini_response_metadata(response: Any, model_name: str) -> None:
    """Log finish_reason and prompt_feedback for debugging truncated responses.

    This helps diagnose issues where Gemini returns truncated or invalid JSON,
    such as safety filters, length limits, or other generation stops.
    """
    try:
        candidates = getattr(response, "candidates", None) or []
        prompt_feedback = getattr(response, "prompt_feedback", None)

        if not candidates:
            logging_util.warning(
                f"🔍 GEMINI_RESPONSE_META: model={model_name} | NO_CANDIDATES | "
                f"prompt_feedback={prompt_feedback}"
            )
            return

        for i, cand in enumerate(candidates):
            # Normalize finish_reason: None -> "UNKNOWN" to ensure warnings are emitted
            # for incomplete/blocked responses (per Gemini SDK, None means not stopped)
            finish_reason_raw = getattr(cand, "finish_reason", None)
            finish_reason_str = (
                "UNKNOWN" if finish_reason_raw is None else str(finish_reason_raw)
            )
            safety_ratings = getattr(cand, "safety_ratings", None)

            # Extract text length from content.parts
            text_length = 0
            try:
                content = getattr(cand, "content", None)
                parts = getattr(content, "parts", None) if content else None
                if parts:
                    for part in parts:
                        if hasattr(part, "text") and part.text:
                            text_length += len(part.text)
            except Exception as e:
                # Best-effort: failures while computing text_length should not break logging
                logging_util.debug(
                    f"🔍 GEMINI_RESPONSE_META: Failed to compute text_length for candidate {i}: {e}"
                )

            # Log warning for non-STOP finish reasons (indicates potential truncation)
            if finish_reason_str not in ("STOP", "FinishReason.STOP"):
                logging_util.warning(
                    f"⚠️ GEMINI_RESPONSE_META: model={model_name} | candidate_index={i} | "
                    f"finish_reason={finish_reason_str} | text_length={text_length} | "
                    f"safety_ratings={safety_ratings} | prompt_feedback={prompt_feedback}"
                )
            else:
                logging_util.info(
                    f"🔍 GEMINI_RESPONSE_META: model={model_name} | candidate_index={i} | "
                    f"finish_reason={finish_reason_str} | text_length={text_length}"
                )
    except Exception as e:
        logging_util.warning(
            f"🔍 GEMINI_RESPONSE_META: Failed to extract metadata: {e}"
        )


def _get_text_from_response(response: Any) -> str:
    """Safely extracts text from a Gemini response object.

    IMPORTANT: Avoid accessing `response.text` directly. The Google GenAI SDK emits
    warnings when responses contain non-text parts and `text` concatenation drops
    those parts. We instead extract from candidates.content.parts.
    """
    try:
        candidates = getattr(response, "candidates", None) or []
        for cand in candidates:
            content = getattr(cand, "content", None)
            parts = getattr(content, "parts", None) if content is not None else None
            if parts is None:
                continue
            text_parts: list[str] = []
            for part in parts:
                text_value = getattr(part, "text", None)
                if isinstance(text_value, str):
                    text_parts.append(text_value)
            if text_parts:
                return "".join(text_parts)
    except Exception as e:
        logging_util.error(f"Unexpected error in _get_text_from_response: {e}")

    # Compatibility fallback: many unit/integration tests use FakeLLMResponse objects
    # that provide a plain `.text` string but no candidates/content/parts structure.
    # Only use this fallback when the structured extraction above produced nothing.
    try:
        text_attr = getattr(response, "text", None)
        if isinstance(text_attr, str):
            return text_attr
    except Exception as e:
        logging_util.error(
            f"Unexpected error reading response.text in _get_text_from_response: {e}"
        )

    # Enhanced logging for blocked responses
    feedback_info = ""
    try:
        if hasattr(response, "prompt_feedback"):
            feedback_info += f" PromptFeedback: {response.prompt_feedback}"

        candidates = getattr(response, "candidates", [])
        if candidates:
            for i, cand in enumerate(candidates):
                finish_reason = getattr(cand, "finish_reason", "UNKNOWN")
                safety_ratings = getattr(cand, "safety_ratings", "UNKNOWN")
                feedback_info += f" Candidate[{i}]: finish_reason={finish_reason}, safety_ratings={safety_ratings}"
        else:
            feedback_info += " No candidates returned."

    except Exception as log_err:
        feedback_info += f" (Failed to extract details: {log_err})"

    logging_util.warning(
        f"Response did not contain valid text.{feedback_info} Full response object: {response}"
    )
    return "[System Message: The model returned a non-text response. Please check the logs for details.]"


def _serialize_gemini_response_parts(api_response: Any) -> list[dict[str, Any]]:
    """Best-effort serialization of Gemini candidates.content.parts for evidence bundles."""
    serialized: list[dict[str, Any]] = []
    try:
        candidates = getattr(api_response, "candidates", None) or []
        for cand in candidates:
            cand_dict: dict[str, Any] = {
                "finish_reason": str(getattr(cand, "finish_reason", "")),
            }
            content = getattr(cand, "content", None)
            parts = getattr(content, "parts", None) if content is not None else None
            out_parts: list[dict[str, Any]] = []
            if parts is not None:
                for part in parts:
                    part_dict: dict[str, Any] = {}
                    text_value = getattr(part, "text", None)
                    if isinstance(text_value, str):
                        part_dict["text"] = text_value

                    thought_sig = getattr(part, "thought_signature", None)
                    if thought_sig is not None:
                        part_dict["thought_signature"] = thought_sig

                    executable = getattr(part, "executable_code", None)
                    if executable is not None:
                        part_dict["executable_code"] = {
                            "language": getattr(executable, "language", None),
                            "code": getattr(executable, "code", None),
                        }

                    exec_result = getattr(part, "code_execution_result", None)
                    if exec_result is not None:
                        part_dict["code_execution_result"] = {
                            "outcome": getattr(exec_result, "outcome", None),
                            "output": getattr(exec_result, "output", None),
                        }

                    fn_call = getattr(part, "function_call", None)
                    if fn_call is not None:
                        part_dict["function_call"] = {
                            "name": getattr(fn_call, "name", None),
                            "args": getattr(fn_call, "args", None),
                        }

                    fn_resp = getattr(part, "function_response", None)
                    if fn_resp is not None:
                        part_dict["function_response"] = {
                            "name": getattr(fn_resp, "name", None),
                            "response": getattr(fn_resp, "response", None),
                        }

                    if part_dict:
                        out_parts.append(part_dict)
            cand_dict["parts"] = out_parts
            serialized.append(cand_dict)
    except Exception as e:
        logging_util.warning("Gemini parts serialization failed: %s", e)
    return serialized


def _build_gemini_two_phase_history(
    *,
    prompt_contents: list[Any],
    phase1_text: str,
    tool_results_prompt: str,
) -> list[Any]:
    """Build Gemini-native history used for second-pass JSON generation."""
    history: list[Any] = []

    for content in prompt_contents:
        if isinstance(content, dict):
            history.append(
                types.Content(
                    role="user",
                    parts=[
                        types.Part(
                            text=json.dumps(
                                content,
                                ensure_ascii=False,
                                default=json_default_serializer,
                            )
                        )
                    ],
                )
            )
        elif isinstance(content, str):
            history.append(types.Content(role="user", parts=[types.Part(text=content)]))
        else:
            history.append(content)

    if phase1_text is not None:
        history.append(
            types.Content(role="model", parts=[types.Part(text=phase1_text)])
        )

    if tool_results_prompt is not None:
        history.append(
            types.Content(role="user", parts=[types.Part(text=tool_results_prompt)])
        )

    return history


def _orchestrate_gemini_code_execution_tool_requests(
    *,
    prompt_contents: list[Any],
    response_1: Any,
    model_name: str,
    system_instruction_text: str | None,
    temperature: float,
    safety_settings: list[Any],
    json_mode_max_output_tokens: int,
    cache_name: str | None = None,
    user_api_key: str | None = None,
) -> Any:
    """Provider-agnostic orchestration for code_execution tool requests.

    llm_service owns this orchestration so provider modules remain execution adapters.
    """
    context = get_prompt_tool_context(prompt_contents)

    raw_response_text = _get_text_from_response(response_1)
    response_text = raw_response_text or ""
    response_data, json_tool_requests = extract_json_payload_and_tool_requests(
        response_text
    )

    if (
        context["is_enabling"]
        and context["allow_domain_tools"]
        and not json_tool_requests
    ):
        logging_util.warning(
            "Gemini code_execution: Missing tool_requests on enable_faction_minigame; retrying with explicit instruction"
        )
        retry_system_instruction = (
            gemini_provider.apply_code_execution_system_instruction(
                system_instruction_text, model_name
            )
        )
        if cache_name:
            retry_instruction = None
            retry_prompt = [get_enable_turn_retry_instruction()] + list(prompt_contents)
        else:
            retry_instruction = (
                retry_system_instruction or ""
            ) + get_enable_turn_retry_instruction()
            retry_prompt = prompt_contents
        response_1 = gemini_provider.generate_json_mode_content(
            prompt_contents=retry_prompt,
            model_name=model_name,
            system_instruction_text=retry_instruction,
            temperature=temperature,
            safety_settings=safety_settings,
            json_mode_max_output_tokens=json_mode_max_output_tokens,
            enable_code_execution=True,
            api_key=user_api_key,
            cache_name=cache_name,
        )
        raw_response_text = _get_text_from_response(response_1)
        response_text = raw_response_text or ""
        response_data, json_tool_requests = extract_json_payload_and_tool_requests(
            response_text
        )

    all_tool_results = execute_gemini_code_execution_tool_orchestration(
        prompt_contents=prompt_contents,
        response_1=response_1,
        response_data=response_data,
        json_tool_requests=json_tool_requests,
        context=context,
        execute_tool_requests_fn=execute_tool_requests,
    )

    if not all_tool_results:
        logging_util.info("No tool_requests or hybrid tools in code_execution response")
        return response_1

    updated_prompt_contents = update_prompt_contents_with_tool_results(
        prompt_contents, all_tool_results
    )
    combined_results_text = format_tool_results_text(all_tool_results)
    turn_number = int(context.get("turn_number") or 1)
    extra_instructions, expected_tool_requests = build_domain_tool_request_enforcement(
        allow_domain_tools=bool(context["allow_domain_tools"]),
        tool_results=all_tool_results,
        turn_number=turn_number,
    )
    tool_results_prompt = build_tool_results_prompt(
        combined_results_text, extra_instructions=extra_instructions
    )
    history = _build_gemini_two_phase_history(
        prompt_contents=updated_prompt_contents,
        phase1_text=raw_response_text if raw_response_text else None,
        tool_results_prompt=tool_results_prompt,
    )

    phase2_system_instruction = gemini_provider.apply_code_execution_system_instruction(
        system_instruction_text,
        model_name,
    )
    response_2 = None
    max_attempts = (
        1 if model_name.startswith("gemini-3") else GEMINI_RETRY_TOOLFLOW_MAX_ATTEMPTS
    )

    for attempt in range(1, max_attempts + 1):
        try:
            response_2 = gemini_provider.generate_json_mode_content(
                prompt_contents=history,
                model_name=model_name,
                system_instruction_text=phase2_system_instruction,
                temperature=temperature,
                safety_settings=safety_settings,
                json_mode_max_output_tokens=json_mode_max_output_tokens,
                enable_code_execution=True,
                cache_name=None,  # Phase 2 has full history; dynamic system_instruction incompatible with cache
                api_key=user_api_key,
            )
            break
        except Exception as api_error:
            if _is_retriable_gemini_error(api_error) and attempt < max_attempts:
                delay = GEMINI_RETRY_BASE_DELAY_SECONDS * (2 ** (attempt - 1))
                _log_retry_attempt(
                    attempt,
                    max_attempts,
                    api_error,
                    delay,
                    model_name,
                )
                time.sleep(delay)
                continue
            raise

    if response_2 is None:
        raise RuntimeError("No response from Gemini API after retries in Phase 2")

    if context["is_enabling"] and context["allow_domain_tools"]:
        inject_tool_requests_if_missing(
            response_2,
            expected_tool_requests=expected_tool_requests,
        )

    response_2._tool_results = all_tool_results
    response_2._tool_requests_executed = True
    return response_2


def _maybe_get_gemini_code_execution_evidence(
    *,
    provider_name: str,
    model_name: str,
    api_response: Any,
    context: str,
) -> dict[str, Any] | None:
    """Return server-verified Gemini code_execution evidence when applicable."""
    if provider_name != constants.LLM_PROVIDER_GEMINI:
        return None
    if (
        dice_strategy.get_dice_roll_strategy(model_name, provider_name)
        != dice_strategy.DICE_STRATEGY_CODE_EXECUTION
    ):
        return None
    gemini_provider.maybe_log_code_execution_parts(
        api_response,
        model_name=model_name,
        context=context,
    )
    return gemini_provider.extract_code_execution_evidence(api_response)


def _get_context_stats(
    context: list[dict[str, Any]],
    model_name: str,
    current_game_state: GameState,
    provider_name: str = constants.DEFAULT_LLM_PROVIDER,
) -> str:
    """Helper to calculate and format statistics for a given story context."""
    if not context:
        return "Turns: 0, Tokens: 0"

    combined_text = "".join(entry.get(constants.KEY_TEXT, "") for entry in context)
    estimated_tokens = estimate_tokens(combined_text)

    # Try to get exact token count via API, fall back to estimate
    actual_tokens: str | int | None = "N/A"
    try:
        if provider_name == constants.LLM_PROVIDER_GEMINI:
            text_contents = [entry.get(constants.KEY_TEXT, "") for entry in context]
            actual_tokens = gemini_provider.count_tokens(model_name, text_contents)
        else:
            actual_tokens = estimated_tokens
    except Exception as e:
        logging_util.warning(f"Could not count tokens for context stats: {e}")
        actual_tokens = estimated_tokens  # Fall back to estimate

    all_core_memories = current_game_state.custom_campaign_state.get(
        "core_memories", []
    )
    stats_string = f"Turns: {len(context)}, Tokens: {actual_tokens} (est: {estimated_tokens}), Core Memories: {len(all_core_memories)}"

    if all_core_memories:
        last_three = all_core_memories[-3:]
        stats_string += "\\n--- Last 3 Core Memories ---\\n"
        for i, memory in enumerate(last_three, 1):
            stats_string += (
                f"  {len(all_core_memories) - len(last_three) + i}: {memory}\\n"
            )
        stats_string += "--------------------------"

    return stats_string


def _calculate_percentage_based_turns(
    story_context: list[dict[str, Any]],
    max_tokens: int,
) -> tuple[int, int]:
    """
    Calculate how many turns to keep based on percentage of story budget.

    Uses STORY_BUDGET_START_RATIO (25%), STORY_BUDGET_MIDDLE_RATIO (10%),
    and STORY_BUDGET_END_RATIO (60%) to allocate tokens proportionally,
    then converts to turn counts. Middle turns are compacted separately.

    Args:
        story_context: Full story context to analyze
        max_tokens: Maximum tokens available for story

    Returns:
        (start_turns, end_turns) tuple based on percentage allocation
    """
    total_turns = len(story_context)
    if total_turns == 0:
        return (0, 0)

    # Calculate average tokens per turn
    combined_text = "".join(
        entry.get(constants.KEY_TEXT, "") for entry in story_context
    )
    total_story_tokens = estimate_tokens(combined_text)
    if total_story_tokens <= 0 or total_turns <= 0:
        # Fallback average when text is empty or invalid; keeps math safe.
        avg_tokens_per_turn = 500
    else:
        avg_tokens_per_turn = total_story_tokens / total_turns

    # Calculate token budgets for start and end
    start_token_budget = int(max_tokens * STORY_BUDGET_START_RATIO)
    end_token_budget = int(max_tokens * STORY_BUDGET_END_RATIO)

    # Convert to turn counts (cap at legacy maximums for safety)
    raw_start_turns = min(
        int(start_token_budget / avg_tokens_per_turn),
        TURNS_TO_KEEP_AT_START,
        total_turns // 2,  # Never take more than half for start
    )

    # Apply start minimum but never exceed total turns
    start_turns = min(max(3, raw_start_turns), total_turns)

    raw_end_turns = min(
        int(end_token_budget / avg_tokens_per_turn),
        TURNS_TO_KEEP_AT_END,
    )
    desired_end_turns = (
        max(5, raw_end_turns) if total_turns >= 5 else min(total_turns, raw_end_turns)
    )

    # Enforce non-overlap using the post-minimum start_turns value
    remaining_turns = max(0, total_turns - start_turns)
    end_turns = min(desired_end_turns, remaining_turns)

    # Final safety: if minimums still force overlap, trim the start portion first
    if start_turns + end_turns > total_turns:
        end_turns = max(0, total_turns - start_turns)

    logging_util.info(
        f"📊 PERCENTAGE-BASED TURNS: avg_tokens/turn={avg_tokens_per_turn:.0f}, "
        f"start_budget={start_token_budget}tk→{start_turns} turns (25%), "
        f"end_budget={end_token_budget}tk→{end_turns} turns (60%), "
        f"middle_budget={int(max_tokens * STORY_BUDGET_MIDDLE_RATIO)}tk (10% for compaction)"
    )

    return (start_turns, end_turns)


def _compact_middle_turns(  # noqa: PLR0912, PLR0915
    middle_turns: list[dict[str, Any]],
    max_tokens: int,
) -> dict[str, Any]:
    """
    Compact middle turns into a summary preserving key events.

    Instead of completely dropping middle turns, extract important sentences
    using multiple detection methods:
    1. Keyword matching (expanded set with action verbs, story markers)
    2. Pattern matching (dice rolls, damage numbers - language-agnostic)
    3. Structural markers (dialogue, exclamations)
    4. Fallback sampling (when no important sentences found)

    The sentence splitting is robust against abbreviations (Dr., Mr.) and
    decimal numbers (3.14, 2.5).

    Args:
        middle_turns: The turns being dropped from the middle section
        max_tokens: Maximum tokens allowed for the compacted summary

    Returns:
        A system message containing the compacted middle summary
    """
    if not middle_turns:
        return {
            "actor": "system",
            "text": "[...time passes...]",
        }

    # Extract important sentences from middle turns
    important_events: list[str] = []
    all_sentences: list[str] = []  # For fallback sampling
    total_tokens = 0

    # Reserve tokens for formatting overhead (header + footer + bullets buffer)
    formatting_overhead = 30
    effective_max_tokens = max(10, max_tokens - formatting_overhead)

    for turn in middle_turns:
        text = turn.get(constants.KEY_TEXT, "")
        if not text:
            continue

        # Use robust sentence splitting (handles abbreviations, decimals)
        sentences = _split_into_sentences(text)
        all_sentences.extend(sentences)

        # Check each sentence for importance using keywords AND patterns
        for sentence in sentences:
            if _is_important_sentence(sentence):
                sentence_tokens = estimate_tokens(sentence)
                if total_tokens + sentence_tokens <= effective_max_tokens:
                    important_events.append(sentence)
                    total_tokens += sentence_tokens
                else:
                    # Reached token limit
                    break

        if total_tokens >= effective_max_tokens:
            break

    # Fallback: If no important events found, sample evenly from all sentences
    if not important_events and all_sentences:
        # Sample every Nth sentence to get representative coverage
        sample_count = min(5, len(all_sentences))
        if sample_count > 0:
            step = max(1, len(all_sentences) // sample_count)
            sampled = all_sentences[::step][:sample_count]

            for sentence in sampled:
                sentence_tokens = estimate_tokens(sentence)
                if total_tokens + sentence_tokens <= effective_max_tokens:
                    important_events.append(sentence)
                    total_tokens += sentence_tokens

    # Format the compacted summary
    unique_events: list[str] = []  # Initialize for post-format budget check
    if important_events:
        # Deduplicate while preserving order
        seen: set[str] = set()
        for event in important_events:
            # Normalize for dedup (lowercase, strip)
            normalized = event.lower().strip()
            if normalized not in seen:
                seen.add(normalized)
                unique_events.append(event)

        # Limit to reasonable number of events
        max_events = 15
        if len(unique_events) > max_events:
            unique_events = unique_events[:max_events]

        summary_text = (
            "[...time passes, and these key events occurred...]\n\n"
            + "\n".join(f"- {event}" for event in unique_events)
            + "\n\n[...the story continues from the most recent events...]"
        )
    else:
        # No sentences at all - use minimal marker
        summary_text = (
            f"[...{len(middle_turns)} turns of exploration and conversation passed...]\n"
            "[...the story continues from the most recent events...]"
        )

    # FIX Bug 3: Post-format budget verification
    # Ensure the formatted output actually fits in the budget
    actual_tokens = estimate_tokens(summary_text)
    if actual_tokens > max_tokens:
        logging_util.warning(
            f"Middle compaction exceeded budget: {actual_tokens} > {max_tokens} tokens. Trimming events."
        )
        # Progressively remove events until we fit
        while unique_events and actual_tokens > max_tokens:
            unique_events.pop()  # Remove last event
            if unique_events:
                summary_text = (
                    "[...time passes, and these key events occurred...]\n\n"
                    + "\n".join(f"- {event}" for event in unique_events)
                    + "\n\n[...the story continues from the most recent events...]"
                )
            else:
                # All events removed - use minimal marker
                summary_text = (
                    f"[...{len(middle_turns)} turns passed...]\n"
                    "[...the story continues...]"
                )
            actual_tokens = estimate_tokens(summary_text)

    logging_util.info(
        f"📊 MIDDLE COMPACTION: {len(middle_turns)} turns → "
        f"{len(important_events)} key events, {actual_tokens} tokens (budget: {max_tokens})"
    )

    return {
        "actor": "system",
        "text": summary_text,
    }


def _truncate_context(  # noqa: PLR0911, PLR0912, PLR0915
    story_context: list[dict[str, Any]],
    max_chars: int,
    model_name: str,
    current_game_state: GameState,
    provider_name: str = constants.DEFAULT_LLM_PROVIDER,
    turns_to_keep_at_start: int = TURNS_TO_KEEP_AT_START,
    turns_to_keep_at_end: int = TURNS_TO_KEEP_AT_END,
) -> list[dict[str, Any]]:
    """
    Intelligently truncates the story context to fit within a given character budget.

    PERCENTAGE-BASED TRUNCATION: Uses 25%/10%/60% ratio for start/middle/end allocation.
    ADAPTIVE FALLBACK: If initial allocation still exceeds budget, iteratively
    reduces turn count until it fits.
    HARD-TRIM GUARANTEE: If even minimum turns exceed budget, text is hard-trimmed
    to guarantee the result fits within budget.
    """
    initial_stats = _get_context_stats(
        story_context, model_name, current_game_state, provider_name
    )
    logging_util.info(f"Initial context stats: {initial_stats}")

    combined_text = "".join(
        entry.get(constants.KEY_TEXT, "") for entry in story_context
    )
    current_tokens = estimate_tokens(combined_text)
    max_tokens = estimate_tokens(
        " " * max_chars
    )  # Convert char budget to token budget using estimate_tokens

    if current_tokens <= max_tokens:
        logging_util.info("Context is within token budget. No truncation needed.")
        return story_context

    logging_util.warning(
        f"Context ({current_tokens} tokens) exceeds budget of {max_tokens} tokens. Truncating..."
    )

    total_turns = len(story_context)

    # Calculate percentage-based turn limits instead of using fixed counts
    pct_start, pct_end = _calculate_percentage_based_turns(story_context, max_tokens)
    turns_to_keep_at_start = min(turns_to_keep_at_start, pct_start)
    turns_to_keep_at_end = min(turns_to_keep_at_end, pct_end)

    if total_turns <= turns_to_keep_at_start + turns_to_keep_at_end:
        # Few turns - but still need to check if they fit in budget
        # If over budget with few turns, we must hard-trim the text content
        total_keep = turns_to_keep_at_start + turns_to_keep_at_end
        # FIX: Handle [-0:] which returns full list in Python
        candidate = story_context[-total_keep:] if total_keep > 0 else []

        if not candidate:
            # No turns to keep - return empty
            return []

        candidate_text = "".join(e.get(constants.KEY_TEXT, "") for e in candidate)
        candidate_tokens = estimate_tokens(candidate_text)

        if candidate_tokens <= max_tokens:
            return candidate

        # Still over budget - iteratively hard-trim until we fit
        # Start with proportional trim based on current vs target
        trim_ratio = max_tokens / max(1, candidate_tokens)
        # FIX: Loop until we actually fit, not just 10 iterations
        max_iterations = 50  # Increased from 10
        for _iteration in range(max_iterations):
            trimmed_entries = []
            # FIX: Always trim from the ORIGINAL candidate list to avoid recursive over-truncation
            # The trim_ratio is relative to the original size.
            for entry in candidate:
                text = entry.get(constants.KEY_TEXT, "")
                # FIX: Remove 50-char floor - allow trimming to any size
                entry_max_chars = int(len(text) * trim_ratio)

                # FIX: If entry would be empty or near-empty, drop it entirely
                if entry_max_chars <= 10:
                    # Skip this entry (drop it)
                    continue

                # FIX: Check for JSON/structured content - don't corrupt it
                if text.strip().startswith("{") or text.strip().startswith("["):
                    # This looks like JSON - either keep fully or drop
                    if len(text) > entry_max_chars:
                        continue  # Drop JSON entry rather than corrupt it
                    trimmed_entries.append(entry)
                    continue

                if len(text) > entry_max_chars:
                    trimmed_text = text[:entry_max_chars] + "... [truncated]"
                    trimmed_entries.append({**entry, constants.KEY_TEXT: trimmed_text})
                else:
                    trimmed_entries.append(entry)

            # If we've dropped all entries, keep at least one minimal marker
            if not trimmed_entries:
                trimmed_entries = [
                    {
                        "actor": "system",
                        "text": "[...context truncated to fit budget...]",
                    }
                ]

            trimmed_text = "".join(
                e.get(constants.KEY_TEXT, "") for e in trimmed_entries
            )
            trimmed_tokens = estimate_tokens(trimmed_text)

            if trimmed_tokens <= max_tokens:
                logging_util.warning(
                    f"Hard-trimmed {len(candidate)} turns to fit budget: "
                    f"{candidate_tokens} tokens -> {trimmed_tokens} tokens"
                )
                return trimmed_entries

            # Still over - reduce ratio further and try again
            trim_ratio *= 0.7

        # Final fallback - return minimal marker if still over budget
        logging_util.warning(
            f"Hard-trim exhausted iterations, returning minimal marker: "
            f"{candidate_tokens} tokens -> budget: {max_tokens}"
        )
        return [{"actor": "system", "text": "[...context truncated to fit budget...]"}]

    # Calculate middle token budget (10% of story budget)
    middle_token_budget = int(max_tokens * STORY_BUDGET_MIDDLE_RATIO)

    # ADAPTIVE LOOP: Reduce turns until content fits within token budget
    # Use absolute minimums but respect passed-in values if they're smaller
    abs_min_start = 3
    abs_min_end = 5
    min_start = (
        min(abs_min_start, turns_to_keep_at_start) if turns_to_keep_at_start > 0 else 0
    )
    min_end = min(abs_min_end, turns_to_keep_at_end)

    current_start = turns_to_keep_at_start
    current_end = turns_to_keep_at_end

    while current_start >= min_start and current_end >= min_end:
        start_context = story_context[:current_start] if current_start > 0 else []
        end_context = story_context[-current_end:] if current_end > 0 else []

        # Extract and compact middle turns instead of dropping them
        middle_start_idx = current_start
        middle_end_idx = total_turns - current_end
        middle_turns = (
            story_context[middle_start_idx:middle_end_idx]
            if middle_end_idx > middle_start_idx
            else []
        )

        # Compact middle turns to preserve key events
        middle_summary = _compact_middle_turns(middle_turns, middle_token_budget)

        truncated_context = start_context + [middle_summary] + end_context

        truncated_text = "".join(
            entry.get(constants.KEY_TEXT, "") for entry in truncated_context
        )
        truncated_tokens = estimate_tokens(truncated_text)

        if truncated_tokens <= max_tokens:
            # Found a fit
            final_stats = _get_context_stats(
                truncated_context, model_name, current_game_state, provider_name
            )
            if (
                current_start < turns_to_keep_at_start
                or current_end < turns_to_keep_at_end
            ):
                logging_util.warning(
                    f"Adaptive truncation reduced to {current_start}+{current_end} turns "
                    f"(from {turns_to_keep_at_start}+{turns_to_keep_at_end}) to fit budget. "
                    f"Middle: {len(middle_turns)} turns compacted. "
                    f"Final: {truncated_tokens} tokens <= {max_tokens} budget"
                )
            else:
                logging_util.info(
                    f"Truncation: {current_start} start + {len(middle_turns)} middle (compacted) + "
                    f"{current_end} end = {truncated_tokens} tokens"
                )
            # Log comprehensive budget breakdown
            utilization_pct = (
                (truncated_tokens / max_tokens * 100) if max_tokens > 0 else 0
            )
            start_tokens = estimate_tokens(
                "".join(e.get(constants.KEY_TEXT, "") for e in start_context)
            )
            end_tokens = estimate_tokens(
                "".join(e.get(constants.KEY_TEXT, "") for e in end_context)
            )
            middle_tokens = estimate_tokens(middle_summary.get(constants.KEY_TEXT, ""))
            logging_util.info(
                f"📊 BUDGET UTILIZATION: {truncated_tokens:,}/{max_tokens:,} tokens ({utilization_pct:.1f}%) | "
                f"Components: start={start_tokens:,}tk ({current_start} turns), "
                f"middle={middle_tokens:,}tk (compacted from {len(middle_turns)} turns), "
                f"end={end_tokens:,}tk ({current_end} turns) | "
                f"Original: {current_tokens:,}tk ({total_turns} turns)"
            )
            logging_util.info(f"Final context stats after truncation: {final_stats}")
            return truncated_context

        # Still over budget - reduce turns (alternate between start and end)
        # Prioritize keeping recent context, reduce start turns faster
        if current_start > min_start and current_start >= current_end:
            step = 2 if current_start - 2 >= min_start else 1
            current_start -= step
        elif current_end > min_end:
            step = 2 if current_end - 2 >= min_end else 1
            current_end -= step
        elif current_start > min_start:
            current_start -= 1
        else:
            # Can't reduce further - exit loop and use last resort
            break

    # Last resort: minimum turns with compacted middle
    start_context = story_context[:min_start] if min_start > 0 else []
    end_context = story_context[-min_end:] if min_end > 0 else []

    # Extract and compact middle turns for last resort
    middle_start_idx = min_start
    middle_end_idx = total_turns - min_end
    middle_turns = (
        story_context[middle_start_idx:middle_end_idx]
        if middle_end_idx > middle_start_idx
        else []
    )
    middle_summary = _compact_middle_turns(middle_turns, middle_token_budget)

    truncated_context = start_context + [middle_summary] + end_context

    truncated_text = "".join(
        entry.get(constants.KEY_TEXT, "") for entry in truncated_context
    )
    truncated_tokens = estimate_tokens(truncated_text)

    logging_util.warning(
        f"Aggressive truncation to {min_start}+{min_end} turns. "
        f"Tokens: {truncated_tokens} (budget: {max_tokens})"
    )

    # If STILL over budget after minimum turns, iteratively hard-trim the text content
    if truncated_tokens > max_tokens:
        trim_ratio = max_tokens / max(1, truncated_tokens)
        original_context = truncated_context

        for iteration in range(50):  # Increased iterations for convergence
            hard_trimmed = []
            for entry in original_context:
                text = entry.get(constants.KEY_TEXT, "")
                # FIX: Remove 50-char floor - allow trimming to any size
                entry_max_chars = int(len(text) * trim_ratio)

                # FIX: If entry would be too small, drop it entirely
                if entry_max_chars <= 10:
                    # Drop this entry - not enough content to be useful
                    continue

                # FIX: Detect JSON content and drop instead of corrupting
                text_stripped = text.strip()
                if text_stripped.startswith(("{", "[")) and len(text) > entry_max_chars:
                    # JSON content would be corrupted by truncation - drop it
                    continue

                if len(text) > entry_max_chars:
                    trimmed_text = text[:entry_max_chars] + "... [truncated]"
                    hard_trimmed.append({**entry, constants.KEY_TEXT: trimmed_text})
                else:
                    hard_trimmed.append(entry)

            # If we dropped all entries, return minimal marker
            if not hard_trimmed:
                hard_trimmed = [
                    {
                        "actor": "system",
                        "text": "[...previous context truncated to fit model limits...]",
                    }
                ]

            trimmed_text = "".join(e.get(constants.KEY_TEXT, "") for e in hard_trimmed)
            new_tokens = estimate_tokens(trimmed_text)

            if new_tokens <= max_tokens:
                logging_util.warning(
                    f"Hard-trimmed last resort to fit budget: "
                    f"{truncated_tokens} tokens -> {new_tokens} tokens (iteration {iteration + 1})"
                )
                truncated_context = hard_trimmed
                break

            # Still over - reduce ratio further
            trim_ratio *= 0.7
            truncated_context = hard_trimmed

    final_stats = _get_context_stats(
        truncated_context, model_name, current_game_state, provider_name
    )
    # Log comprehensive budget breakdown for last-resort path
    final_text = "".join(e.get(constants.KEY_TEXT, "") for e in truncated_context)
    final_tokens = estimate_tokens(final_text)
    utilization_pct = (final_tokens / max_tokens * 100) if max_tokens > 0 else 0
    logging_util.info(
        f"📊 BUDGET UTILIZATION (last-resort): {final_tokens:,}/{max_tokens:,} tokens ({utilization_pct:.1f}%) | "
        f"Original: {current_tokens:,}tk ({total_turns} turns) | "
        f"Final: {len(truncated_context)} entries"
    )
    logging_util.info(f"Final context stats after truncation: {final_stats}")

    return truncated_context


def _get_sequence_id_context_for_budget(
    story_context: list[dict[str, Any]],
    max_input_allowed: int,
    model_name: str,
    current_game_state: GameState,
    provider_name: str = constants.DEFAULT_LLM_PROVIDER,
) -> list[dict[str, Any]]:
    """Return a bounded story context for sequence_id budget measurement."""
    if not story_context:
        return []

    min_story_budget_tokens = int(max_input_allowed * BUDGET_STORY_CONTEXT_ABSOLUTE_MIN)
    min_story_budget_chars = min_story_budget_tokens * 4
    return _truncate_context(
        story_context,
        min_story_budget_chars,
        model_name,
        current_game_state,
        provider_name,
    )


def _apply_compacted_game_state(
    game_state_for_llm: dict[str, Any],
    compacted_game_state: str,
    campaign_id: str | None,
    user_settings: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Apply compacted game_state JSON and re-inject campaign_id if provided."""
    # Log before state for comparison
    original_size = len(json.dumps(game_state_for_llm, default=json_default_serializer))
    original_keys = (
        list(game_state_for_llm.keys()) if isinstance(game_state_for_llm, dict) else []
    )

    try:
        compacted_state = json.loads(compacted_game_state)
    except json.JSONDecodeError as e:
        logging_util.warning(
            f"Failed to parse compacted_game_state, using original: {e}"
        )
        return game_state_for_llm

    if not isinstance(compacted_state, dict):
        logging_util.warning(
            "Failed to parse compacted_game_state as dict, using original."
        )
        return game_state_for_llm

    # Track injected fields
    injected_fields = []
    if campaign_id is not None:
        compacted_state["campaign_id"] = campaign_id
        injected_fields.append("campaign_id")
    if isinstance(user_settings, dict):
        compacted_state["user_settings"] = user_settings
        injected_fields.append(f"user_settings({len(user_settings)} keys)")

    # Log after state with comparison
    compacted_size = len(json.dumps(compacted_state, default=json_default_serializer))
    compacted_keys = list(compacted_state.keys())
    reduction_pct = (
        ((original_size - compacted_size) / original_size * 100)
        if original_size > 0
        else 0
    )

    logging_util.info(
        f"📊 COMPACTION_APPLIED: {original_size:,} -> {compacted_size:,} chars "
        f"({reduction_pct:.1f}% reduction) | "
        f"keys: {len(original_keys)} -> {len(compacted_keys)} | "
        f"injected: {injected_fields if injected_fields else 'none'}"
    )

    return compacted_state


# Mock response constants for better maintainability
MOCK_INITIAL_STORY_WITH_COMPANIONS = """{
"narrative": "Welcome to your adventure! You find yourself at the entrance of a mysterious dungeon, with stone walls covered in ancient runes. The air is thick with magic and possibility. As you approach, three skilled adventurers emerge from the shadows to join your quest.",
"entities_mentioned": ["dungeon", "runes"],
"location_confirmed": "Dungeon Entrance",
"characters": [{"name": "Aria Moonwhisper", "class": "Elf Ranger", "background": "A skilled archer from the Silverleaf Forest"}],
"setting": {"location": "Dungeon Entrance", "atmosphere": "mysterious"},
"mechanics": {"initiative_rolled": false, "characters_need_setup": true},
"action_resolution": {
  "trigger": "system",
  "player_intent": "start adventure",
  "original_input": "Start a fantasy adventure",
  "resolution_type": "narrative",
  "mechanics": {"outcome": "story_start"},
  "audit_flags": ["mock_response"],
  "reinterpreted": false
},
"npc_data": {
  "Thorin Ironshield": {
    "mbti": "ISTJ",
    "role": "warrior",
    "background": "A steadfast dwarf fighter with decades of battle experience",
    "relationship": "companion",
    "skills": ["combat", "defense", "weapon mastery"],
    "personality_traits": ["loyal", "protective", "methodical"],
    "equipment": ["enchanted shield", "battle axe", "chainmail"]
  },
  "Luna Starweaver": {
    "mbti": "INFP",
    "role": "healer",
    "background": "A gentle elf cleric devoted to the healing arts",
    "relationship": "companion",
    "skills": ["healing magic", "divine spells", "herbalism"],
    "personality_traits": ["compassionate", "wise", "intuitive"],
    "equipment": ["holy symbol", "healing potions", "staff of light"]
  },
  "Zara Swiftblade": {
    "mbti": "ESTP",
    "role": "scout",
    "background": "A quick-witted halfling rogue skilled in stealth and traps",
    "relationship": "companion",
    "skills": ["stealth", "lockpicking", "trap detection"],
    "personality_traits": ["agile", "clever", "bold"],
    "equipment": ["thieves' tools", "daggers", "studded leather armor"]
  }
}
}"""

MOCK_INITIAL_STORY_NO_COMPANIONS = """{
"narrative": "Welcome to your adventure! You find yourself at the entrance of a mysterious dungeon, with stone walls covered in ancient runes. The air is thick with magic and possibility.",
"entities_mentioned": ["dungeon", "runes"],
"location_confirmed": "Dungeon Entrance",
"characters": [{"name": "Aria Moonwhisper", "class": "Elf Ranger", "background": "A skilled archer from the Silverleaf Forest"}],
"setting": {"location": "Dungeon Entrance", "atmosphere": "mysterious"},
"mechanics": {"initiative_rolled": false, "characters_need_setup": true},
"action_resolution": {
  "trigger": "system",
  "player_intent": "start adventure",
  "original_input": "Start a fantasy adventure",
  "resolution_type": "narrative",
  "mechanics": {"outcome": "story_start"},
  "audit_flags": ["mock_response"],
  "reinterpreted": false
}
}"""


def _get_default_model_for_provider(provider: str) -> str:
    """Get the default model for a given provider."""
    model_map = {
        constants.LLM_PROVIDER_GEMINI: constants.DEFAULT_GEMINI_MODEL,
        constants.LLM_PROVIDER_CEREBRAS: constants.DEFAULT_CEREBRAS_MODEL,
        constants.LLM_PROVIDER_OPENROUTER: constants.DEFAULT_OPENROUTER_MODEL,
        constants.LLM_PROVIDER_OPENCLAW: constants.DEFAULT_OPENCLAW_MODEL,
    }
    return model_map.get(provider, constants.DEFAULT_GEMINI_MODEL)


def _select_provider_and_model(user_id: UserId | None) -> ProviderSelection:
    """Select the configured LLM provider and model for a user.

    Provider selection priority:
    1. FORCE_PROVIDER env var - explicit override (for CI cost control)
    2. User settings from database
    3. Default provider (Gemini)

    Note: TESTING_AUTH_BYPASS only bypasses authentication, not provider.
    """
    # DIAGNOSTIC: Log entry with all relevant env vars
    logging_util.info(
        f"🔍 PROVIDER_SELECTION_START: user_id={user_id}, "
        f"FORCE_PROVIDER={os.environ.get('FORCE_PROVIDER')}, "
        f"MOCK_SERVICES_MODE={os.environ.get('MOCK_SERVICES_MODE')}, "
        f"FORCE_TEST_MODEL={os.environ.get('FORCE_TEST_MODEL')}, "
        f"TESTING_AUTH_BYPASS={os.environ.get('TESTING_AUTH_BYPASS')}"
    )

    # Explicit provider override - for CI cost control
    # Set FORCE_PROVIDER=gemini to prevent hitting real external APIs
    forced_provider = os.environ.get("FORCE_PROVIDER", "").lower()
    if forced_provider:
        if forced_provider not in constants.ALLOWED_LLM_PROVIDERS:
            logging_util.warning(
                f"⚠️ FORCE_PROVIDER={forced_provider} not allowed, using default"
            )
            return ProviderSelection(constants.DEFAULT_LLM_PROVIDER, DEFAULT_MODEL)
        model = _get_default_model_for_provider(forced_provider)
        logging_util.info(
            f"🔍 PROVIDER_SELECTION_FORCED: Using FORCE_PROVIDER={forced_provider}"
        )
        return ProviderSelection(forced_provider, model)

    provider = constants.DEFAULT_LLM_PROVIDER
    model = DEFAULT_MODEL

    if not user_id:
        logging_util.info(
            "🔍 PROVIDER_SELECTION_NO_USER: No user_id provided, returning default Gemini"
        )
        return ProviderSelection(provider, model)

    try:
        user_settings = get_user_settings(user_id)
        logging_util.debug(
            f"🔍 PROVIDER_SELECTION_SETTINGS: user_id={user_id}, "
            f"settings_keys={list(user_settings.keys()) if user_settings else None}"
        )
        if user_settings is None:
            logging_util.warning(
                "⚠️ PROVIDER_SELECTION_SETTINGS_MISSING: "
                f"No user settings document for user_id={user_id}; using default provider/model."
            )
            return ProviderSelection(provider, model)

        requested_provider = user_settings.get("llm_provider")
        if requested_provider is not None:
            if requested_provider not in constants.ALLOWED_LLM_PROVIDERS:
                message = (
                    "PROVIDER_SELECTION_INVALID_PROVIDER: "
                    f"Invalid provider '{requested_provider}' configured for user_id={user_id}."
                )
                logging_util.error(f"❌ {message}")
                raise LLMRequestError(message, status_code=422)
            provider = requested_provider

        if provider == constants.LLM_PROVIDER_OPENROUTER:
            preferred_openrouter = user_settings.get("openrouter_model")
            if preferred_openrouter in constants.ALLOWED_OPENROUTER_MODELS:
                model = preferred_openrouter
            else:
                model = constants.DEFAULT_OPENROUTER_MODEL
        elif provider == constants.LLM_PROVIDER_CEREBRAS:
            preferred_cerebras = user_settings.get("cerebras_model")
            if preferred_cerebras in constants.ALLOWED_CEREBRAS_MODELS:
                model = preferred_cerebras
            else:
                model = constants.DEFAULT_CEREBRAS_MODEL
        elif provider == constants.LLM_PROVIDER_OPENCLAW:
            model = (
                user_settings.get("openclaw_model") or constants.DEFAULT_OPENCLAW_MODEL
            )
        else:
            # GEMINI logic
            user_preferred_model = user_settings.get("gemini_model")

            # Check for legacy mapping
            if user_preferred_model in constants.GEMINI_MODEL_MAPPING:
                user_preferred_model = constants.GEMINI_MODEL_MAPPING[
                    user_preferred_model
                ]

            if (
                not user_preferred_model
                or user_preferred_model not in constants.ALLOWED_GEMINI_MODELS
            ):
                user_preferred_model = constants.DEFAULT_GEMINI_MODEL

            return ProviderSelection(
                provider=constants.LLM_PROVIDER_GEMINI,
                model=user_preferred_model,
            )

        logging_util.info(
            f"🔍 PROVIDER_SELECTION_FINAL: provider={provider}, model={model}"
        )
        return ProviderSelection(provider, model)
    except (KeyError, AttributeError, ValueError) as e:
        message = (
            "PROVIDER_SELECTION_SETTINGS_EXCEPTION: "
            f"Failed retrieving user settings for user_id={user_id}: {e}"
        )
        logging_util.error(f"❌ {message}")
        raise LLMRequestError(message, status_code=422) from e


def select_provider_and_model(user_id: UserId | None) -> ProviderSelection:
    """Public wrapper for provider/model selection.

    world_logic (and other call sites outside llm_service) should use this instead of
    importing a private helper.
    """
    return _select_provider_and_model(user_id)


def _select_model_for_user(user_id: UserId | None) -> str:
    return _select_provider_and_model(user_id).model


@log_exceptions
def get_initial_story(  # noqa: PLR0912, PLR0915
    prompt: str,
    user_id: UserId | None = None,
    selected_prompts: list[str] | None = None,
    generate_companions: bool = False,
    use_default_world: bool = False,
    use_character_creation_agent: bool = False,
    initial_npc_data: dict[str, Any] | None = None,  # Companions from god_mode
) -> LLMResponse:
    """
    Generates the initial story part, including character, narrative, and mechanics instructions.

    Returns:
        LLMResponse: Custom response object containing:
            - narrative_text: Clean text for display (guaranteed to be clean narrative)
            - structured_response: Parsed JSON with state updates, entities, etc.
    """
    # Clear file tracking for this request (for lightweight evidence capture)
    clear_loaded_files_tracking()

    # Check for mock mode and return mock response immediately
    mock_mode = _is_mock_services_mode()
    if mock_mode:
        logging_util.info("Using mock mode - returning mock initial story response")

        # If CharacterCreationAgent should be used, return character creation narrative
        if use_character_creation_agent:
            logging_util.info(
                "Mock mode: Using CharacterCreationAgent for character review"
            )
            # Return character creation narrative for God Mode campaigns with character data
            character_creation_narrative = """[CHARACTER CREATION]

Welcome! I see you have a pre-defined character template. Let's review and finalize your character before we begin the adventure.

**Your Character So Far:**
- **Name:** (From template)
- **Class:** (From template)
- **Level:** (From template)

**Questions to Complete Your Character:**

1. **Race:** What race is your character? (Human, Elf, Dwarf, Halfling, Dragonborn, etc.)
2. **Background:** What was your character's life before this adventure? (Noble, Soldier, Acolyte, Folk Hero, etc.)
3. **Alignment:** What alignment best fits your character?
4. **Personality:** What drives your character? What are their ideals, bonds, and flaws?

Take your time! Once we finalize these details, we'll begin your epic adventure."""

            # Parse as structured response
            # CharacterCreationAgent does not require action_resolution
            narrative_text, structured_response = parse_structured_response(
                json.dumps(
                    {
                        "narrative": character_creation_narrative,
                        "entities_mentioned": [],
                        "location_confirmed": "",
                        "state_updates": {
                            "custom_campaign_state": {
                                "character_creation_in_progress": True
                            }
                        },
                    }
                ),
                requires_action_resolution=False,  # CharacterCreationAgent exempt
            )

            if structured_response:
                if structured_response.debug_info is None:
                    structured_response.debug_info = {}
                structured_response.debug_info["agent_name"] = "CharacterCreationAgent"
                return LLMResponse.create_from_structured_response(
                    structured_response, "mock-model"
                )
            return LLMResponse.create_legacy(
                character_creation_narrative,
                "mock-model",
            )

        # Regular story mode
        if generate_companions:
            logging_util.info("Mock mode: Generating companions as requested")
            mock_response_text = MOCK_INITIAL_STORY_WITH_COMPANIONS
        else:
            logging_util.info("Mock mode: No companions requested")
            mock_response_text = MOCK_INITIAL_STORY_NO_COMPANIONS

        # Parse the mock response to get structured data
        # StoryModeAgent requires action_resolution
        narrative_text, structured_response = parse_structured_response(
            mock_response_text,
            requires_action_resolution=True,  # StoryModeAgent requires it
        )

        if structured_response:
            # Add agent_name to debug_info for mock responses too
            # Initial story always uses StoryModeAgent (same as non-mock path)
            if structured_response.debug_info is None:
                structured_response.debug_info = {}
            structured_response.debug_info["agent_name"] = "StoryModeAgent"
            return LLMResponse.create_from_structured_response(
                structured_response, "mock-model"
            )
        return LLMResponse.create_legacy(
            "Welcome to your adventure! You find yourself at the entrance of a mysterious dungeon, with stone walls covered in ancient runes. The air is thick with magic and possibility.",
            "mock-model",
        )

    if selected_prompts is None:
        selected_prompts = []
        logging_util.warning(
            "No specific system prompts selected for initial story. Using none."
        )

    # Create game_state with companions if provided (from god_mode)
    initial_game_state_for_agent = None
    if initial_npc_data:
        initial_game_state_for_agent = GameState(npc_data=initial_npc_data)
        logging_util.info(
            f"🎭 Passing {len(initial_npc_data)} companions to agent for instruction building: {list(initial_npc_data.keys())}"
        )

    # Select agent based on use_character_creation_agent flag
    # For God Mode campaigns with character data, use CharacterCreationAgent
    # For regular campaigns, use StoryModeAgent
    if use_character_creation_agent:
        agent = CharacterCreationAgent(game_state=initial_game_state_for_agent)
        logging_util.info(
            "Using CharacterCreationAgent for initial story (God Mode with character)"
        )
    else:
        agent = StoryModeAgent(game_state=initial_game_state_for_agent)
        logging_util.info("Using StoryModeAgent for initial story (regular campaign)")

    # --- MODEL SELECTION ---
    # Use centralized helper for consistent model selection across all story generation
    provider_selection = _select_provider_and_model(user_id)
    model_to_use: str = provider_selection.model
    logging_util.info(
        f"Using provider/model: {provider_selection.provider}/{model_to_use} for initial story generation."
    )
    dice_roll_strategy = dice_strategy.get_dice_roll_strategy(
        model_to_use, provider_selection.provider
    )

    # Build system instructions based on agent type
    if use_character_creation_agent:
        # CharacterCreationAgent builds instructions directly (no build_system_instruction_parts)
        # It will include companion instructions if companions are in game_state
        system_instruction_final = agent.build_system_instructions(
            selected_prompts=selected_prompts,
            use_default_world=use_default_world,
            include_continuation_reminder=False,
            dice_roll_strategy=dice_roll_strategy,
        )
    else:
        builder = agent.prompt_builder

        # Start from agent's standard story-mode stack (without continuation reminders)
        system_instruction_parts = agent.build_system_instruction_parts(
            selected_prompts=selected_prompts,
            include_continuation_reminder=False,
            turn_number=0,
            dice_roll_strategy=dice_roll_strategy,
        )
        # Initial story specific: Add companion generation instruction if requested
        if generate_companions:
            system_instruction_parts.append(builder.build_companion_instruction())

        # Initial story specific: Add background summary instruction
        system_instruction_parts.append(builder.build_background_summary_instruction())

        # Finalize with world content (world lore must remain last in the hierarchy)
        system_instruction_final = builder.finalize_instructions(
            system_instruction_parts, use_default_world
        )

    if dice_roll_strategy == dice_strategy.DICE_STRATEGY_CODE_EXECUTION:
        system_instruction_final = _strip_tool_requests_dice_instructions(
            system_instruction_final
        )

    # Add clear indication when using default world setting
    if use_default_world:
        prompt = f"Use default setting Assiah. {prompt}"

    # --- ENTITY TRACKING FOR INITIAL STORY ---
    # Extract expected entities from the prompt for initial tracking
    expected_entities: list[str] = []
    entity_preload_text: str = ""
    entity_specific_instructions: str = ""
    entity_tracking_instruction: str = ""

    # Let the LLM determine and provide character names in the response
    # rather than extracting them via regex patterns from the prompt
    # Character names will be handled by structured generation and entity tracking

    # Player character name should come from LLM structured response (player_character_data.name)
    # NOT from fragile regex parsing of user prompts

    # Create a minimal initial game state for entity tracking
    # Use default player character - actual name will come from LLM response
    pc_name = "Player Character"

    if expected_entities:
        initial_game_state = {
            "player_character_data": {
                "name": pc_name,
                "hp": 10,
                "max_hp": 10,
                "level": 1,
                "string_id": f"pc_{sanitize_entity_name_for_id(pc_name)}_001",
            },
            "npc_data": {},
            "world_data": {"current_location_name": "The throne room"},
            "combat_state": {"in_combat": False},
        }

        # 1. Entity Pre-Loading (Option 3)
        entity_preload_text = entity_preloader.create_entity_preload_text(
            initial_game_state, 1, 1, "Starting Location"
        )

        # 2. Entity-Specific Instructions (Option 5)
        entity_instructions = instruction_generator.generate_entity_instructions(
            entities=expected_entities,
            player_references=[prompt],
            location="Starting Location",
            story_context="",
        )
        entity_specific_instructions = entity_instructions

        # 3. Create entity manifest for tracking using create_from_game_state
        # For initial story, we use session 1, turn 1
        try:
            entity_manifest = create_from_game_state(initial_game_state, 1, 1)
            entity_manifest_text = entity_manifest.to_prompt_format()
        except Exception as e:
            # Graceful degradation: If entity validation fails, warn but continue campaign creation
            # This prevents crashes from malformed data during campaign setup
            logging_util.warning(
                f"Entity manifest creation failed during initial story (validation error), "
                f"continuing without entity tracking: {e}"
            )
            entity_manifest_text = ""

        entity_tracking_instruction = create_structured_prompt_injection(
            entity_manifest_text, expected_entities
        )

    # Build enhanced prompt with entity tracking (only for regular story mode)
    # For character creation mode, enhanced_prompt is already set above
    if not use_character_creation_agent:
        enhanced_prompt: str = prompt
        if (
            entity_preload_text
            or entity_specific_instructions
            or entity_tracking_instruction
        ):
            enhanced_prompt = (
                f"{entity_preload_text}"
                f"{entity_specific_instructions}"
                f"{entity_tracking_instruction}"
                f"\nUSER REQUEST:\n{prompt}"
            )
            logging_util.info(
                f"Added entity tracking to initial story. Expected entities: {expected_entities}"
            )

        # Add character creation reminder if mechanics is enabled (only for regular story mode)
        if selected_prompts and constants.PROMPT_TYPE_MECHANICS in selected_prompts:
            enhanced_prompt = (
                constants.CHARACTER_DESIGN_REMINDER + "\n\n" + enhanced_prompt
            )
            logging_util.info(
                "Added character creation reminder to initial story prompt"
            )

    # ONLY use LLMRequest structured JSON architecture (NO legacy fallbacks)
    if not user_id:
        raise ValueError("user_id is required for initial story generation")

    # NEW ARCHITECTURE: Use LLMRequest for structured JSON (NO string concatenation)
    world_data = {}  # Could be extracted from builder if needed

    # Build LLMRequest with structured data
    # Use enhanced_prompt if set (for character creation mode), otherwise use prompt
    prompt_to_use = (
        enhanced_prompt if "enhanced_prompt" in locals() and enhanced_prompt else prompt
    )
    gemini_request = LLMRequest.build_initial_story(
        character_prompt=prompt_to_use,
        user_id=str(user_id),
        selected_prompts=selected_prompts or [],
        generate_companions=generate_companions,
        use_default_world=use_default_world,
        world_data=world_data,
    )

    # Send structured JSON directly to Gemini API (NO string conversion)
    api_response = _call_llm_api_with_llm_request(
        gemini_request=gemini_request,
        model_name=model_to_use,
        system_instruction_text=system_instruction_final,
        provider_name=provider_selection.provider,
        user_id=user_id,
    )
    logging_util.info("Successfully used LLMRequest for initial story generation")
    final_api_response = api_response

    code_execution_evidence = _maybe_get_gemini_code_execution_evidence(
        provider_name=provider_selection.provider,
        model_name=model_to_use,
        api_response=api_response,
        context="initial_story",
    )
    # Extract text from raw API response object
    raw_response_text: str = _get_text_from_response(api_response)

    # Create LLMResponse from raw response, which handles all parsing internally
    # Parse the structured response to extract clean narrative and debug data
    narrative_text, structured_response = parse_structured_response(
        raw_response_text,
        requires_action_resolution=agent.requires_action_resolution,
    )
    capture_raw = os.getenv("CAPTURE_RAW_LLM", "true").lower() == "true"
    capture_tools = True
    raw_limit = _get_raw_limit()
    processing_metadata: dict[str, Any] = {
        "llm_provider": provider_selection.provider,
        "llm_model": model_to_use,
        "execution_path": "non_streaming",
    }
    if capture_raw:
        processing_metadata["raw_response_text"] = raw_response_text
    processing_metadata.update(
        dice_integrity.build_dice_processing_metadata(
            api_response=final_api_response,
            dice_roll_strategy=dice_roll_strategy,
            capture_tools=capture_tools,
        )
    )

    if structured_response:
        debug_info = structured_response.debug_info or {}
        debug_info.setdefault("llm_provider", provider_selection.provider)
        debug_info.setdefault("llm_model", model_to_use)
        debug_info.setdefault("execution_path", "non_streaming")
        # Capture which agent served this request
        debug_info["agent_name"] = agent.__class__.__name__
        # Capture which instruction files were loaded (lightweight evidence)
        # NOTE: We only store filenames and char count, NOT full text (saves ~36KB/entry)
        debug_info["system_instruction_files"] = get_loaded_instruction_files()
        debug_info["system_instruction_char_count"] = len(system_instruction_final)
        # Log raw data instead of storing (avoids 30MB+ bloat in large campaigns)
        if capture_raw:
            _log_raw_llm_data(
                system_instruction_final=system_instruction_final,
                gemini_request=gemini_request,
                raw_response_text=raw_response_text,
                raw_limit=raw_limit,
                provider_name=provider_selection.provider,
                model_name=model_to_use,
                api_response=api_response,
            )
        if code_execution_evidence:
            # Persist server-verified evidence (do not rely on model self-reporting).
            debug_info.update(code_execution_evidence)
            _log_fabricated_dice_if_detected(
                structured_response,
                code_execution_evidence,
                tool_requests_executed=bool(
                    getattr(api_response, "_tool_requests_executed", False)
                ),
                tool_results=getattr(api_response, "_tool_results", None),
            )
        structured_response.debug_info = debug_info
        dice_integrity.apply_dice_metadata_to_structured_response(
            structured_response=structured_response,
            dice_metadata=processing_metadata,
            dice_roll_strategy=dice_roll_strategy,
        )
        # Add user warning if API required retries (transient error recovery)
        _add_api_retry_warning_to_response(api_response, structured_response)

    # DIAGNOSTIC LOGGING: Log parsed response details for debugging empty narrative issues
    logging_util.info(
        f"📊 PARSED_RESPONSE (initial_story): narrative_length={len(narrative_text)}, "
        f"structured_response={'present' if structured_response else 'None'}, "
        f"raw_response_length={len(raw_response_text)}"
    )
    if len(narrative_text) == 0:
        # Include preview suffix only if response was truncated
        raw_preview = raw_response_text[:500]
        preview_suffix = "..." if len(raw_response_text) > 500 else ""
        logging_util.warning(
            f"⚠️ EMPTY_NARRATIVE (initial_story): LLM returned empty narrative. "
            f"Raw response preview: {raw_preview}{preview_suffix}"
        )
        # Log structured response fields if available (consistent with continue_story)
        if structured_response:
            has_planning = bool(
                structured_response.planning_block
                if hasattr(structured_response, "planning_block")
                else False
            )
            has_session = bool(
                structured_response.session_header
                if hasattr(structured_response, "session_header")
                else False
            )
            logging_util.warning(
                f"⚠️ EMPTY_NARRATIVE (initial_story): structured_response has "
                f"planning_block={has_planning}, session_header={has_session}"
            )

    # Provider hardening: non-god responses must never emit empty narrative.
    # Keep a deterministic fallback so Firestore writes/evidence remain stable.
    if len(narrative_text.strip()) == 0:
        has_god_mode_response = bool(
            structured_response
            and getattr(structured_response, constants.FIELD_GOD_MODE_RESPONSE, "")
        )
        if not has_god_mode_response:
            narrative_text = JSON_PARSE_FALLBACK_MARKER
            if structured_response:
                structured_response.narrative = narrative_text

    # Create LLMResponse with proper debug content separation
    if structured_response:
        # Use structured response (preferred) - ensures clean separation
        gemini_response = LLMResponse.create_from_structured_response(
            structured_response,
            model_to_use,
            combined_narrative_text=narrative_text,
            provider=provider_selection.provider,
            processing_metadata=processing_metadata,
            raw_response_text=raw_response_text,
        )
    else:
        # Fallback to legacy mode for non-JSON responses
        gemini_response = LLMResponse.create_legacy(
            narrative_text,
            model_to_use,
            provider=provider_selection.provider,
            processing_metadata=processing_metadata,
            raw_response_text=raw_response_text,
        )

    # --- ENTITY VALIDATION FOR INITIAL STORY ---
    if expected_entities:
        validator = NarrativeSyncValidator()
        validation_result = validator.validate(
            narrative_text=gemini_response.narrative_text,
            expected_entities=expected_entities,
            location="Starting Location",
        )

        if not validation_result.all_entities_present:
            logging_util.warning(
                f"Initial story failed entity validation. Missing: {validation_result.entities_missing}"
            )
            # For initial story, we'll log but not retry to avoid complexity
            # The continue_story function will handle retry logic for subsequent interactions

    # Log LLMResponse creation - INFO level for production visibility
    logging_util.info(
        f"📝 FINAL_RESPONSE (initial_story): narrative_length={len(gemini_response.narrative_text)}, "
        f"has_structured_response={gemini_response.structured_response is not None}"
    )

    # Companion validation (moved from world_logic.py for proper SRP)
    if generate_companions:
        _validate_companion_generation(gemini_response)

    # Return our custom LLMResponse object (not raw API response)
    # This object contains:
    # - narrative_text: Clean text for display (guaranteed to be clean narrative)
    # - structured_response: Parsed JSON structure with state updates, entities, etc.
    return gemini_response


# Note: _is_in_character_creation function removed as we now include planning blocks
# during character creation for better interactivity


def _log_debug_response(
    response_text: str | None, context: str = "", max_length: int = 400
) -> None:
    """Helper to log truncated response text for debugging."""
    if not response_text:
        logging_util.warning(
            f"🔍 API_RESPONSE_DEBUG ({context}): Response is empty or None"
        )
        return

    # Convert to string safely
    response_str = str(response_text)

    # Log basic info
    logging_util.info(
        f"🔍 API_RESPONSE_DEBUG ({context}): Length: {len(response_str)} chars"
    )

    # Log truncated content for debugging
    if len(response_str) <= max_length:
        logging_util.info(f"🔍 API_RESPONSE_DEBUG ({context}): Content: {response_str}")
    else:
        half_length = max_length // 2
        start_content = response_str[:half_length]
        end_content = response_str[-half_length:]
        logging_util.info(
            f"🔍 API_RESPONSE_DEBUG ({context}): Content: {start_content}...[{len(response_str) - max_length} chars omitted]...{end_content}"
        )


def _log_raw_llm_data(
    system_instruction_final: str,
    gemini_request: LLMRequest,
    raw_response_text: str,
    raw_limit: int,
    *,
    provider_name: str,
    model_name: str,
    api_response: Any | None = None,
) -> None:
    """Log raw LLM inputs/outputs with previews and length caps."""

    instruction_preview = system_instruction_final[:2000]
    instruction_suffix = (
        "..." if len(system_instruction_final) > len(instruction_preview) else ""
    )
    logging_util.info(
        f"📝 SYSTEM_INSTRUCTION ({len(system_instruction_final)} chars): "
        f"{instruction_preview}{instruction_suffix}"
    )

    try:
        request_payload = (
            gemini_request.to_json()
            if hasattr(gemini_request, "to_json")
            else str(gemini_request)
        )
        request_str_full = (
            json.dumps(request_payload, default=str)
            if isinstance(request_payload, dict)
            else str(request_payload)
        )
        request_length = len(request_str_full)
        request_preview = request_str_full[:raw_limit]
        request_suffix = "..." if len(request_str_full) > len(request_preview) else ""
        logging_util.info(
            f"📤 RAW_REQUEST ({request_length} chars; logged up to {raw_limit}): "
            f"{request_preview}{request_suffix}"
        )
    except Exception as e:
        logging_util.info(f"📤 RAW_REQUEST capture failed: {e}")

    response_preview = raw_response_text[:raw_limit]
    response_suffix = "..." if len(raw_response_text) > len(response_preview) else ""
    logging_util.info(
        f"📥 RAW_RESPONSE ({len(raw_response_text)} chars; logged up to {raw_limit}): "
        f"{response_preview}{response_suffix}"
    )

    # REV-65v: For Gemini 3.x code_execution models, capture the STRIPPED system
    # instruction (after dice tool sections are removed). This reflects what the
    # LLM actually receives, not the raw input.
    system_instruction_for_capture = system_instruction_final
    if (
        provider_name == "gemini"
        and uses_code_execution_strategy(model_name)
        and isinstance(system_instruction_final, str)
    ):
        system_instruction_for_capture = apply_code_execution_system_instruction(
            system_instruction_final, model_name
        )

    _append_llm_request_response_capture(
        {
            "type": "request",
            "timestamp": datetime.now(UTC).isoformat(),
            "provider": provider_name,
            "model": model_name,
            "system_instruction_text": system_instruction_for_capture,
            "request_payload": request_str_full,
        }
    )
    _append_llm_request_response_capture(
        {
            "type": "response",
            "timestamp": datetime.now(UTC).isoformat(),
            "provider": provider_name,
            "model": model_name,
            "response_text": raw_response_text,
            # For Gemini, persist the full structured parts (non-text included) for evidence/debugging.
            "response_parts": (
                _serialize_gemini_response_parts(api_response)
                if provider_name == "gemini" and api_response is not None
                else None
            ),
        }
    )


def _get_llm_capture_path() -> str:
    """Return LLM request/response capture path when enabled."""
    return os.getenv("LLM_REQUEST_RESPONSE_CAPTURE_PATH", "").strip()


def _get_llm_capture_max_chars() -> int:
    """Deprecated no-op retained for backward compatibility."""
    try:
        return int(os.getenv("LLM_CAPTURE_MAX_CHARS", "200000"))
    except ValueError:
        return 200000


def _truncate_llm_capture_text(text: str, _limit: int) -> str:
    """Deprecated no-op retained for backward compatibility."""
    return text


def _append_llm_request_response_capture(payload: dict[str, Any]) -> None:
    """Append a single request/response capture entry as JSONL."""
    capture_path = _get_llm_capture_path()
    if not capture_path:
        return
    try:
        with open(capture_path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, default=str))
            handle.write("\n")
    except OSError as e:
        logging_util.warning("LLM capture write failed: %s", e)


def _check_missing_required_fields(
    structured_response: NarrativeResponse | None,
    mode: str,
    is_god_mode: bool = False,
    is_dm_mode: bool = False,
    require_dice_rolls: bool = False,
    dice_integrity_violation: bool = False,
    require_social_hp_challenge: bool = False,
    debug_mode: bool = False,  # noqa: ARG001
) -> list[str]:
    """Check if required fields are missing from the structured response.

    NOTE: There are no server-side retries for missing fields.
    Missing fields are still DETECTED and LOGGED for observability.
    Warnings are added to system_warnings in debug_info for user visibility.

    Detected fields (logged for observability):
    - planning_block: Must have 'thinking' or 'choices' content
    - dice_rolls: Required when require_dice_rolls=True
    - dice_integrity: Flagged when dice_integrity_violation=True
    - session_header: Cosmetic, logged but not critical


    Args:
        structured_response: The parsed NarrativeResponse object
        mode: Current game mode
        is_god_mode: Whether this is a god mode command
        is_dm_mode: Whether the response is in DM mode
        require_dice_rolls: Whether dice_rolls is required for this turn
        dice_integrity_violation: Whether dice integrity check failed
        require_social_hp_challenge: Whether social HP challenge is required
        debug_mode: Whether user has debug mode enabled (deprecated, warnings always added)

    Returns:
        List of missing field names for observability (no retries).

    Side Effects:
        When critical fields are missing, modifies structured_response.debug_info
        in place to add warning messages to system_warnings list.
    """
    # Note: debug_mode parameter is deprecated (warnings always added)
    # Only check for story mode (character mode, not god/dm mode)
    if mode != constants.MODE_CHARACTER or is_god_mode or is_dm_mode:
        return []

    if not structured_response:
        logging_util.warning(
            "⚠️ LLM_MISSING_FIELDS: No structured response - would need planning_block, session_header"
        )
        return ["planning_block", "session_header"]

    detected_missing = []

    # Check planning_block
    planning_block = getattr(structured_response, "planning_block", None)
    if not planning_block or not isinstance(planning_block, dict):
        detected_missing.append("planning_block")
    else:
        # Check if planning_block has content
        thinking_value = planning_block.get("thinking", "")
        has_thinking = isinstance(thinking_value, str) and thinking_value.strip()

        choices_value = planning_block.get("choices")
        # Accept both dict-format and list-format choices
        has_choices = (isinstance(choices_value, dict) and len(choices_value) > 0) or (
            isinstance(choices_value, list) and len(choices_value) > 0
        )

        has_content = has_thinking or has_choices
        if not has_content:
            detected_missing.append("planning_block")

    # Check session_header (cosmetic but tracked)
    session_header = getattr(structured_response, "session_header", None)
    if not session_header or not str(session_header).strip():
        detected_missing.append("session_header")

    # Check dice if required - action_resolution.mechanics.rolls/audit_events only
    if require_dice_rolls:
        action_resolution = getattr(structured_response, "action_resolution", None)
        has_valid_dice = has_action_resolution_dice(
            action_resolution if isinstance(action_resolution, dict) else None
        )

        if not has_valid_dice:
            detected_missing.append("dice_rolls")

    # Check dice integrity
    if dice_integrity_violation:
        detected_missing.append("dice_integrity")

    # Check social HP challenge if required - validate all required subfields
    if require_social_hp_challenge:
        social_hp_challenge = getattr(structured_response, "social_hp_challenge", None)
        is_missing = True
        if isinstance(social_hp_challenge, dict) and social_hp_challenge:
            # Validate all required subfields have meaningful content
            # Use `or ""` to handle explicit None values (LLM may output null)
            npc_name = str(social_hp_challenge.get("npc_name") or "").strip()
            objective = str(social_hp_challenge.get("objective") or "").strip()
            resistance = str(social_hp_challenge.get("resistance_shown") or "").strip()
            social_hp_val = social_hp_challenge.get("social_hp")
            social_hp_max = social_hp_challenge.get("social_hp_max")
            is_missing = not (
                npc_name
                and objective
                and resistance
                and social_hp_val is not None
                and isinstance(social_hp_max, (int, float))
                and social_hp_max > 0
            )
        if is_missing:
            detected_missing.append("social_hp_challenge")

    # Log warnings for observability (always)
    if detected_missing:
        # Filter out session_header from warning since it's cosmetic
        critical_missing = [f for f in detected_missing if f != "session_header"]
        if critical_missing:
            logging_util.warning(
                f"⚠️ LLM_MISSING_FIELDS: Response missing {critical_missing} "
                "(no server-side retries; accepting response as-is)"
            )

        # Add server-generated system warning for missing fields
        # SECURITY: Use _server_system_warnings key (not system_warnings) to prevent LLM spoofing.
        # Only server code can write to _server_system_warnings; LLM-provided system_warnings in
        # debug_info are ignored. This prevents the model from injecting misleading "system" warnings.
        if critical_missing and structured_response:
            # Add warning for missing fields (exclude planning_block to avoid double-warning)
            # planning_block gets its own warning from _validate_and_enforce_planning_block
            fields_to_warn = [f for f in critical_missing if f != "planning_block"]
            if fields_to_warn:
                warning_message = (
                    f"Missing required fields: {', '.join(fields_to_warn)}"
                )
                _append_server_warning(structured_response, warning_message)

    return detected_missing


def _validate_and_enforce_planning_block(
    response_text: str | None,
    structured_response: NarrativeResponse | None = None,
) -> str:
    """
    Validates that structured_response.planning_block exists and is valid JSON.
    The structured_response.planning_block field is the PRIMARY and AUTHORITATIVE source.

    IMPORTANT: This function NO LONGER generates default/fallback planning blocks.
    If the LLM doesn't generate a planning block, we return the response as-is
    and let the error propagate to the UI.

    Args:
        response_text: The AI's response text (for context only)
        structured_response: NarrativeResponse object to check (REQUIRED)

    Returns:
        str: Response text unchanged - no modifications are made
    """
    # Handle None response_text gracefully
    if response_text is None:
        logging_util.warning(
            "🔍 VALIDATION_INPUT: Response text is None, returning empty string"
        )
        return ""

    # Skip planning block validation if AI response indicates mode switch
    if response_text and (
        "[Mode: DM MODE]" in response_text or "[Mode: GOD MODE]" in response_text
    ):
        logging_util.info(
            "Response indicates mode switch - skipping planning block validation"
        )
        return response_text

    # Check if response already contains a valid planning block
    if (
        structured_response
        and hasattr(structured_response, "planning_block")
        and structured_response.planning_block
    ):
        planning_block = structured_response.planning_block

        # Only accept JSON format
        if isinstance(planning_block, dict):
            # JSON format - check if it has choices or thinking content
            has_content = planning_block.get("thinking", "").strip() or (
                planning_block.get("choices")
                and len(planning_block.get("choices", {})) > 0
            )

            if has_content:
                logging_util.info("✅ Planning block found in JSON structured response")
                return response_text
            logging_util.warning(
                "⚠️ PLANNING_BLOCK_EMPTY: Planning block exists but has no content"
            )
            return response_text
        # String format no longer supported
        logging_util.error(
            f"❌ STRING PLANNING BLOCKS NO LONGER SUPPORTED: Found {type(planning_block).__name__} planning block, only JSON format is allowed"
        )
        return response_text

    # Planning block is missing - log warning but DO NOT generate defaults
    # The LLM is responsible for generating planning blocks, not this function
    logging_util.warning(
        "⚠️ PLANNING_BLOCK_MISSING: Story mode response missing required planning block. "
        "The LLM should have generated this - no fallback will be used."
    )

    # Add server-generated system warning if structured_response is available
    # SECURITY: Use _server_system_warnings key (not system_warnings) to prevent LLM spoofing.
    # Only server code can write to _server_system_warnings; LLM-provided system_warnings in
    # debug_info are ignored. This prevents the model from injecting misleading "system" warnings.
    if structured_response:
        # Add planning block missing warning
        warning_message = "Missing required planning block"
        _append_server_warning(structured_response, warning_message)

    # Return response text unchanged - no fallback content is added
    return response_text


@dataclass
class PreparedContinuation:
    """Holds all prepared data for story continuation.

    This consolidates preparation logic shared between continue_story()
    and continue_story_streaming() to eliminate duplication.
    """

    agent: Any  # Agent instance (DialogAgent, GodModeAgent, etc.)
    system_instruction_final: str
    gemini_request: Any  # LLMRequest
    model_to_use: str
    provider_selection: Any  # ProviderSelection
    dice_roll_strategy: str | None
    is_god_mode_command: bool
    is_think_mode: bool
    checkpoint_block: str
    core_memories: str
    sequence_ids: str
    raw_user_input: str
    processed_user_input: str  # After validation mutations
    temperature_override: float | None
    force_tool_mode: str | None
    entity_tracking_data: dict
    expected_entities: list
    truncated_story_context: list
    final_user_input: str  # After agent preprocessing + dice enforcement
    classifier_metadata: dict | None  # From get_agent_for_input
    budget_warnings_to_show: list  # Filtered budget warnings for UI display
    new_persist_keys: list  # New warning keys to persist
    user_id: UserId


def _prepare_story_continuation(  # noqa: PLR0912, PLR0915
    user_input: str,
    mode: str,
    story_context: list[dict[str, Any]],
    current_game_state: GameState,
    selected_prompts: list[str] | None = None,
    use_default_world: bool = False,
    user_id: UserId | None = None,
    campaign_id: str | None = None,
) -> PreparedContinuation:
    """Prepare all data needed for story continuation.

    This function consolidates the preparation logic that is shared between
    continue_story() and continue_story_streaming() to eliminate duplication.

    Returns:
        PreparedContinuation: All prepared data needed to make the API call
            and process the response.
    """
    # Clear file tracking for this request (for lightweight evidence capture)
    clear_loaded_files_tracking()

    # Determine which model to use based on user preferences
    # Use centralized helper for consistent model selection across all story generation
    provider_selection = _select_provider_and_model(user_id)
    model_to_use = provider_selection.model
    logging_util.info(
        f"Using provider/model: {provider_selection.provider}/{model_to_use} for story continuation."
    )
    dice_roll_strategy = dice_strategy.get_dice_roll_strategy(
        model_to_use, provider_selection.provider
    )

    # Preserve the raw user input before any validation mutations
    raw_user_input = user_input

    # Check for multiple think commands in input using regex
    think_pattern: str = r"Main Character:\s*think[^\n]*"
    think_matches: list[str] = re.findall(think_pattern, user_input, re.IGNORECASE)
    if len(think_matches) > 1:
        logging_util.warning(
            f"Multiple think commands detected: {len(think_matches)}. Processing as single response."
        )

    # --- NEW: Validate checkpoint consistency before generating response ---
    if story_context:
        # Get the most recent AI response to validate against current state
        recent_ai_responses = [
            entry.get(constants.KEY_TEXT, "")
            for entry in story_context[-3:]
            if entry.get(constants.KEY_ACTOR) == constants.ACTOR_GEMINI
        ]
        if recent_ai_responses:
            latest_narrative = recent_ai_responses[-1]
            discrepancies = current_game_state.validate_checkpoint_consistency(
                latest_narrative
            )

            if discrepancies:
                logging_util.warning(
                    f"CHECKPOINT_VALIDATION: Found {len(discrepancies)} potential discrepancies:"
                )
                for i, discrepancy in enumerate(discrepancies, 1):
                    logging_util.warning(f"  {i}. {discrepancy}")

                # Add validation prompt to ensure AI addresses inconsistencies
                validation_instruction = (
                    "IMPORTANT: State validation detected potential inconsistencies between the game state "
                    "and recent narrative. Please ensure your response maintains strict consistency with the "
                    "CURRENT GAME STATE data, especially regarding character health, location, and mission status."
                )
                user_input = f"{validation_instruction}\n\n{user_input}"

    if selected_prompts is None:
        selected_prompts = []
        logging_util.warning(
            "No specific system prompts selected for continue_story. Using none."
        )

    # Use agent architecture to construct system instructions
    # Rewards mode is explicit and must always use RewardsAgent for focused prompts.
    if mode == constants.MODE_REWARDS:
        agent = RewardsAgent(current_game_state)
        classifier_metadata = None
    else:
        # Extract the last AI response from story_context to provide context for agent selection
        # This helps the semantic classifier distinguish between generic actions and dialog responses.
        last_ai_response = None
        if story_context:
            for entry in reversed(story_context):
                if entry.get(constants.KEY_ACTOR) == constants.ACTOR_GEMINI:
                    last_ai_response = entry.get(constants.KEY_TEXT)
                    break

        # The agent is selected based on the raw user input and mode
        # Mode parameter enables API clients to use mode="think" without THINK: prefix
        # Pass last_ai_response as context to improve classification accuracy
        agent, classifier_metadata = get_agent_for_input(
            raw_user_input, current_game_state, mode, last_ai_response=last_ai_response
        )

    # Use default temperature (0.9) for FactionManagementAgent to match iteration_011 behavior
    # iteration_011 achieved 56% tool invocation with default temperature, not a lower override
    temperature_override = None
    force_tool_mode: str | None = None
    if isinstance(agent, FactionManagementAgent):
        if agent.minigame_enabled:
            # Don't override - use default TEMPERATURE = 0.9 (matches iteration_011)
            logging_util.info(
                f"🏰 FACTION_MINIGAME: Agent selected, minigame enabled, using default temperature {TEMPERATURE} (matches iteration_011)"
            )
            # Force tool mode ANY to ensure faction tools are called (bead worktree_world_faction-0kr)
            force_tool_mode = "ANY"
            logging_util.info(
                "🏰 FACTION_TOOL_MODE: Forcing mode=ANY to ensure faction tools are invoked"
            )
        else:
            logging_util.info(
                f"🏰 FACTION_MINIGAME: Agent selected but minigame NOT enabled (minigame_enabled={agent.minigame_enabled})"
            )
    is_god_mode_command: bool = isinstance(agent, GodModeAgent)
    is_think_mode: bool = isinstance(agent, PlanningAgent)

    # Get turn number for living world advancement from game state
    # Falls back to computing from context for backward compatibility with old campaigns
    # IMPORTANT: stored_turn is the value AFTER the last completed action.
    # For the current request, we need stored_turn + 1 (for non-GOD mode).
    # GOD mode doesn't increment player_turn, so we use stored_turn as-is.
    stored_turn = getattr(current_game_state, "player_turn", 0)
    if stored_turn > 0:
        # Use stored value + 1 for current turn (non-GOD mode will increment after)
        # For GOD mode, this gives the correct "current" turn since it won't increment
        turn_number = stored_turn + 1 if not is_god_mode_command else stored_turn
    else:
        # Fallback for old campaigns without player_turn
        turn_number = compute_player_turn_number(story_context)

    # Read LLM-requested instruction hints from previous turn
    # These are sections the LLM requested via debug_info.meta.needs_detailed_instructions
    pending_hints: list[str] = (
        getattr(current_game_state, "pending_instruction_hints", []) or []
    )
    if pending_hints:
        logging_util.info(
            f"📋 DYNAMIC_PROMPTS: Loading LLM-requested sections from previous turn: {pending_hints}"
        )

    # 🚨 AUTO-INJECT SOCIAL HP REMINDER for high-tier NPCs
    # If game state contains god_primordial, king_ancient, or level >= 15 NPCs,
    # automatically add "social_hp" to pending_hints to reinforce the system
    raw_npc_data = getattr(current_game_state, "npc_data", None) or {}
    npc_data = raw_npc_data if isinstance(raw_npc_data, dict) else {}

    def _safe_int(value: Any, default: int = 0) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    high_tier_npcs = []
    if raw_npc_data and not isinstance(raw_npc_data, dict):
        logging_util.warning(
            f"SOCIAL_HP: npc_data is not a dict (type={type(raw_npc_data).__name__}), skipping high-tier NPC scan"
        )

    for npc_id, npc_info in npc_data.items():
        if not isinstance(npc_info, dict):
            continue
        tier = (npc_info.get("tier") or "").lower()
        level = _safe_int(npc_info.get("level"))
        name = npc_info.get("name", npc_id)
        # Detect high-tier NPCs that require Social HP enforcement
        if tier in ("god_primordial", "king_ancient", "lord_general") or level >= 15:
            high_tier_npcs.append(f"{name} (tier={tier}, level={level})")

    if high_tier_npcs and "social_hp" not in pending_hints:
        pending_hints = list(pending_hints) + ["social_hp"]
        logging_util.info(
            f"🚨 SOCIAL_HP: Auto-injected Social HP reminder due to high-tier NPCs: {high_tier_npcs}"
        )

    if is_god_mode_command:
        # GOD MODE: Use GodModeAgent with focused administrative prompts
        # God mode is for correcting mistakes/changing campaign, NOT playing
        # CRITICAL: Set dice_roll_strategy to None for the ENTIRE god mode flow.
        # Previous fix (PR #4334) only passed None to build_system_instructions,
        # but the local variable was still used for:
        # 1. Adding "[SYSTEM ENFORCEMENT:...]" to user input
        # 2. Code execution fabrication checks
        # 3. Dice metadata in structured response
        # Bug discovered in bead REV-e0o: god mode still allowed code execution.
        dice_roll_strategy = None  # Disable dice for entire god mode flow
        system_instruction_final = agent.build_system_instructions(
            dice_roll_strategy=None  # Explicit None - god mode = no dice
        )
    else:
        # STORY MODE: Use StoryModeAgent with full gameplay prompts
        # Include continuation reminders only in character mode
        include_continuation = mode == constants.MODE_CHARACTER
        # Pass turn_number for living world advancement (every 3 turns)
        # Pass pending_hints to load LLM-requested detailed sections
        system_instruction_final = agent.build_system_instructions(
            selected_prompts=selected_prompts,
            use_default_world=use_default_world,
            include_continuation_reminder=include_continuation,
            turn_number=turn_number,
            llm_requested_sections=pending_hints if pending_hints else None,
            dice_roll_strategy=dice_roll_strategy,
        )

    if dice_roll_strategy == dice_strategy.DICE_STRATEGY_CODE_EXECUTION:
        system_instruction_final = _strip_tool_requests_dice_instructions(
            system_instruction_final
        )

    # --- NEW: Component-Level Budget Allocation ---
    # Uses min/max percentage constraints to guarantee story context quality.
    # See BUDGET_* constants for percentage allocations.

    # 1. Serialize game state for budget measurement
    # IMPORTANT: Exclude npc_data here to match the shape actually sent to the LLM.
    game_state_for_budget = current_game_state.to_dict()
    if isinstance(game_state_for_budget, dict):
        # Use a shallow copy so we don't accidentally mutate the original game state
        game_state_for_budget = dict(game_state_for_budget)
        game_state_for_budget.pop("npc_data", None)
    serialized_game_state = json.dumps(
        game_state_for_budget, indent=2, default=json_default_serializer
    )

    # 2. Calculate total input budget
    is_combat_or_complex = (
        current_game_state.is_in_combat() if current_game_state else False
    )
    safe_token_budget, output_token_reserve, max_input_allowed = (
        _calculate_context_budget(
            provider_selection.provider, model_to_use, is_combat_or_complex
        )
    )

    # 3. Get temp prompt parts for budget measurement
    # Use a bounded story context so sequence_id measurement doesn't explode
    sequence_id_context = _get_sequence_id_context_for_budget(
        story_context=story_context,
        max_input_allowed=max_input_allowed,
        model_name=model_to_use,
        current_game_state=current_game_state,
        provider_name=provider_selection.provider,
    )
    temp_checkpoint_block, temp_core_memories, temp_seq_ids = get_static_prompt_parts(
        current_game_state, sequence_id_context
    )

    # 4. Allocate budget across components using min/max percentages
    # This ensures story context gets at least 30% (or 15% in emergency)
    # Include checkpoint_block and sequence_id to prevent overflow
    budget_result = _allocate_request_budget(
        max_input_allowed=max_input_allowed,
        system_instruction=system_instruction_final,
        game_state_json=serialized_game_state,
        core_memories=temp_core_memories,
        entity_tracking_estimate=ENTITY_TRACKING_TOKEN_RESERVE,
        story_context=story_context,
        checkpoint_block=temp_checkpoint_block,
        sequence_id_list=temp_seq_ids,
    )

    # 5. Extract allocated budgets and compacted content
    story_budget_tokens = budget_result.get_story_budget()
    char_budget_for_story = story_budget_tokens * 4

    # Get compacted content (or original if no compaction needed)
    compacted_system_instruction = budget_result.compacted_content.get(
        "system_instruction", system_instruction_final
    )
    compacted_game_state = budget_result.compacted_content.get(
        "game_state", serialized_game_state
    )
    # NOTE: core_memories compaction now happens AFTER truncating story context,
    # using core_memories_summary from the final truncated context (bead worktree_logs6-d2r).
    # The temp_core_memories compaction from budget_result is intentionally unused.
    entity_tracking_alloc = budget_result.get_allocation("entity_tracking")
    entity_tracking_budget = (
        entity_tracking_alloc.allocated_tokens
        if entity_tracking_alloc
        else budget_result.compacted_content.get(
            "entity_tracking", ENTITY_TRACKING_TOKEN_RESERVE
        )
    )

    # Update system instruction if compacted
    if compacted_system_instruction != system_instruction_final:
        system_instruction_final = compacted_system_instruction
        logging_util.info(
            "🔨 SYSTEM_INSTRUCTION: Using compacted version from budget allocator"
        )

    # 6. Filter budget warnings for UI display (suppress already-shown warnings)
    budget_warnings_to_show, new_persist_keys = _filter_persisted_warnings(
        budget_result.warnings, current_game_state
    )

    # Log budget summary
    reserve_mode = "combat" if is_combat_or_complex else "normal"
    story_pct = (
        (story_budget_tokens / max_input_allowed * 100)
        if max_input_allowed > 0
        else 0.0
    )
    logging_util.info(
        f"📊 BUDGET: model_limit={_get_context_window_tokens(model_to_use)}tk, "
        f"safe_budget={safe_token_budget}tk, max_input={max_input_allowed}tk, "
        f"output_reserve={output_token_reserve}tk ({reserve_mode}), "
        f"story_budget={story_budget_tokens}tk ({story_pct:.1f}%)"
    )

    # 7. Truncate story context using allocated budget
    truncated_story_context = _truncate_context(
        story_context,
        char_budget_for_story,
        model_to_use,
        current_game_state,
        provider_selection.provider,
    )

    # Now that we have the final, truncated context, we can generate the real prompt parts.
    checkpoint_block, core_memories_summary, sequence_id_list_string = (
        get_static_prompt_parts(current_game_state, truncated_story_context)
    )

    # FIX bead worktree_logs6-d2r: Use core memories from final truncated context,
    # not the bounded sequence_id_context used for budget measurement.
    # Apply budget compaction to the final core_memories_summary.
    core_memories_alloc = budget_result.get_allocation("core_memories")
    if core_memories_alloc:
        core_memories_budget_tokens = core_memories_alloc.allocated_tokens
        final_core_memories = _compact_core_memories(
            core_memories_summary, core_memories_budget_tokens
        )
        if final_core_memories != core_memories_summary:
            logging_util.info(
                f"🔨 CORE_MEMORIES: Compacted final memories from "
                f"{estimate_tokens(core_memories_summary):,}tk to "
                f"{estimate_tokens(final_core_memories):,}tk "
                f"(budget={core_memories_budget_tokens:,}tk)"
            )
    else:
        # Fallback if no allocation found (shouldn't happen)
        final_core_memories = core_memories_summary

    # FIX bead worktree_logs6-cc4: Cap sequence_id_list_string to allocated budget.
    # The budget was measured on sequence_id_context (bounded 20%) but the list is
    # built from truncated_story_context (full allocated). Apply cap to prevent overflow.
    sequence_id_alloc = budget_result.get_allocation("sequence_id")
    if sequence_id_alloc and sequence_id_list_string:
        sequence_id_budget_tokens = sequence_id_alloc.allocated_tokens
        current_seq_tokens = estimate_tokens(sequence_id_list_string)
        if current_seq_tokens > sequence_id_budget_tokens > 0:
            # Truncate sequence IDs to fit budget
            max_chars = sequence_id_budget_tokens * 4
            # Split, keep from end (most recent), rejoin
            seq_ids = sequence_id_list_string.split(", ")
            truncated_ids = []
            current_len = 0
            for seq_id in reversed(seq_ids):
                # Account for ", " separator
                addition_len = len(seq_id) + (2 if truncated_ids else 0)
                if current_len + addition_len <= max_chars:
                    truncated_ids.insert(0, seq_id)
                    current_len += addition_len
                else:
                    break
            final_sequence_ids = ", ".join(truncated_ids)
            logging_util.info(
                f"🔨 SEQUENCE_IDS: Capped from {current_seq_tokens:,}tk to "
                f"{estimate_tokens(final_sequence_ids):,}tk "
                f"(budget={sequence_id_budget_tokens:,}tk, "
                f"kept {len(truncated_ids)}/{len(seq_ids)} IDs)"
            )
        else:
            final_sequence_ids = sequence_id_list_string
    else:
        final_sequence_ids = sequence_id_list_string or ""

    # --- ENTITY TRACKING: Create scene manifest for entity tracking ---
    # Always prepare entity tracking to ensure JSON response format
    session_number: int = current_game_state.custom_campaign_state.get(
        "session_number", 1
    )
    _, expected_entities, entity_tracking_instruction = _prepare_entity_tracking(
        current_game_state, truncated_story_context, session_number
    )

    # Build timeline log (used for entity prompts and diagnostics, not serialized in LLMRequest)
    timeline_log_string: str = _build_timeline_log(truncated_story_context)

    # Enhanced entity tracking with mitigation strategies
    entity_preload_text: str = ""
    entity_specific_instructions: str = ""

    if expected_entities:
        # 1. Entity Pre-Loading (Option 3)
        game_state_dict = current_game_state.to_dict()
        # Use player turns (user/AI pairs) based on the truncated context to keep
        # entity tracking cadence aligned with the visible story log.
        turn_number = (len(truncated_story_context) // 2) + 1
        current_location = current_game_state.world_data.get(
            "current_location_name", "Unknown"
        )
        entity_preload_text = entity_preloader.create_entity_preload_text(
            game_state_dict, session_number, turn_number, current_location
        )

        # 2. Entity-Specific Instructions (Option 5)
        player_references = [user_input] if user_input else []
        entity_instructions = instruction_generator.generate_entity_instructions(
            entities=expected_entities,
            player_references=player_references,
            location=current_location,
            story_context=timeline_log_string,
        )
        entity_specific_instructions = entity_instructions
        logging_util.info(
            "ENTITY_TRACKING_PROMPT: preload_chars=%s, specific_chars=%s",
            len(entity_preload_text),
            len(entity_specific_instructions),
        )

    # Create the final prompt for the current user turn (User's preferred method)
    current_prompt_text: str = get_current_turn_prompt(user_input, mode)

    # EQUIPMENT CONTEXT INJECTION: When user asks about equipment/items,
    # inject explicit equipment list so LLM has clear context (not buried in JSON)
    if is_equipment_query(user_input):
        equipment_display = extract_equipment_display(current_game_state)
        if equipment_display:
            # Build human-readable equipment summary
            equipment_lines = []
            for item in equipment_display:
                name = item.get("name", "Unknown")
                slot = item.get("slot", "")
                stats = item.get("stats", "")
                if stats:
                    equipment_lines.append(f"  - {slot}: {name} ({stats})")
                else:
                    equipment_lines.append(f"  - {slot}: {name}")
            equipment_context = (
                "\n\n[PLAYER EQUIPMENT - YOU MUST MENTION THESE BY NAME]\n"
                + "\n".join(equipment_lines)
                + "\n\nCRITICAL INSTRUCTION: In your narrative response, you MUST explicitly name "
                + "at least 3-4 of the items listed above. Do NOT use vague terms like "
                + "'your gear' or 'your equipment'. Instead, write things like "
                + "'Your Helm of Telepathy gleams...' or 'You grip the Flame Tongue...'.\n\n"
            )
            current_prompt_text = equipment_context + current_prompt_text
            logging_util.info(
                f"📦 EQUIPMENT_CONTEXT_INJECTED: {len(equipment_display)} items added to prompt"
            )

    # Select appropriate model (use user preference if available, otherwise default selection)
    chosen_model: str = model_to_use

    # ONLY use LLMRequest structured JSON architecture (NO legacy fallbacks)
    user_id_from_state = getattr(current_game_state, "user_id", None) or user_id
    if not user_id_from_state:
        raise ValueError(
            "user_id is required for story continuation (provide in GameState or argument)"
        )

    # Build trimmed entity tracking data using LRU-style tiering
    # This caps entity_tracking growth for campaigns with many NPCs
    current_location = current_game_state.world_data.get(
        "current_location_name", current_game_state.world_data.get("location", "")
    )
    if isinstance(current_location, dict):
        logging_util.warning(
            f"⚠️ world_data current_location_name is dict, extracting string: {list(current_location.keys())}"
        )
        _loc_name = current_location.get("name")
        current_location = (
            _loc_name if _loc_name is not None else (current_location.get("id") or "")
        )
    entity_tracking_data, entity_tier_log = _build_trimmed_entity_tracking(
        npc_data=current_game_state.npc_data,
        story_context=truncated_story_context,
        current_location=current_location,
        max_tokens=entity_tracking_budget
        if isinstance(entity_tracking_budget, int)
        else None,
    )
    logging_util.info(entity_tier_log)

    # Measure and log actual entity tracking token usage
    entity_tracking_tokens = estimate_tokens(json.dumps(entity_tracking_data))
    logging_util.info(
        f"ENTITY_TRACKING_SIZE: {entity_tracking_tokens}tk "
        f"(reserve was {ENTITY_TRACKING_TOKEN_RESERVE}tk)"
    )

    # Build LLMRequest with structured data (NO string concatenation)
    # CRITICAL: Exclude npc_data from game_state - it's ~500 tokens per NPC
    # Entity data is now provided via trimmed entity_tracking_data instead
    full_game_state = current_game_state.to_dict()
    # Serialize and deserialize to convert Firestore timestamps to JSON-compatible types
    full_game_state = json.loads(
        json.dumps(full_game_state, default=json_default_serializer)
    )
    game_state_for_llm = {k: v for k, v in full_game_state.items() if k != "npc_data"}
    # Keep debug_info persisted in game state, but do not send it to the LLM.
    # This avoids prompt noise and prevents non-canonical debug fields from
    # influencing generation contracts.
    game_state_for_llm.pop("debug_info", None)
    # Include user_settings for LLM visibility (e.g., spicy_mode toggle handling).
    user_settings = getattr(current_game_state, "user_settings", None)
    if isinstance(user_settings, dict):
        game_state_for_llm["user_settings"] = user_settings

    # Inject campaign_id for explicit caching (BEAD-3qy fix)
    # This enables _call_llm_api_with_explicit_cache() to be triggered
    if campaign_id is not None:
        game_state_for_llm["campaign_id"] = campaign_id
        logging_util.debug(
            f"📦 CACHE_SETUP: Injected campaign_id={campaign_id} into game_state"
        )

    # Pop pending_system_corrections BEFORE compaction to prevent loss.
    # _compact_game_state only preserves fields in priority tiers (CRITICAL/HIGH/MEDIUM/LOW).
    # pending_system_corrections is not in any tier, so compaction would drop it.
    pending_system_corrections = game_state_for_llm.pop(
        "pending_system_corrections", []
    )
    if not isinstance(pending_system_corrections, list):
        logging_util.warning(
            "pending_system_corrections is not a list; dropping invalid value: %s",
            type(pending_system_corrections).__name__,
        )
        pending_system_corrections = []

    # BLOCKING FIX: Use compacted game_state if budget allocator produced one
    if compacted_game_state != serialized_game_state:
        game_state_for_llm = _apply_compacted_game_state(
            game_state_for_llm=game_state_for_llm,
            compacted_game_state=compacted_game_state,
            campaign_id=campaign_id,
            user_settings=user_settings if isinstance(user_settings, dict) else None,
        )
        logging_util.info(
            "🔨 GAME_STATE: Using compacted version from budget allocator"
        )

    # NOTE: LLM gets full context per CLAUDE.md principle - never mask information
    # The LLM sees actual faction_power and ranking values. Tool calls are enforced
    # via prompt instructions (TOP 5 CRITICAL RULES) and server-side auto-invocation,
    # not by hiding information from the LLM.

    # DEBUG: Log game_state component sizes to identify bloat sources
    try:
        npc_data_tokens = estimate_tokens(
            json.dumps(
                full_game_state.get("npc_data", {}), default=json_default_serializer
            )
        )
        world_data_tokens = estimate_tokens(
            json.dumps(
                full_game_state.get("world_data", {}), default=json_default_serializer
            )
        )
        player_data_tokens = estimate_tokens(
            json.dumps(
                full_game_state.get("player_character_data", {}),
                default=json_default_serializer,
            )
        )
        remaining_state_tokens = estimate_tokens(
            json.dumps(game_state_for_llm, default=json_default_serializer)
        )
        logging_util.info(
            f"GAME_STATE_BREAKDOWN: npc_data={npc_data_tokens}tk (EXCLUDED), "
            f"world_data={world_data_tokens}tk, player_data={player_data_tokens}tk, "
            f"remaining_state={remaining_state_tokens}tk"
        )
    except Exception as e:
        logging_util.warning(f"Could not measure game_state breakdown: {e}")

    # Strip story entries to essential fields only to reduce token bloat.
    # Keep `world_events` only when available; this is enough to preserve living
    # world continuity without reintroducing full state_updates metadata.
    essential_story_fields = {"text", "actor", "mode", "sequence_id", "world_events"}
    stripped_story_context = []
    for entry in truncated_story_context:
        if not isinstance(entry, dict):
            continue

        stripped_entry = {k: v for k, v in entry.items() if k in essential_story_fields}
        # Lift LW deltas into lightweight `world_events` for continuity checks.
        if "world_events" not in stripped_entry or not isinstance(
            stripped_entry.get("world_events"), dict
        ):
            state_updates = entry.get("state_updates", {})
            if isinstance(state_updates, dict):
                state_world_events = state_updates.get("world_events")
                if isinstance(state_world_events, dict):
                    stripped_entry["world_events"] = state_world_events
        if stripped_entry:
            stripped_story_context.append(stripped_entry)

    # Log pending system_corrections (already extracted before compaction above)
    if pending_system_corrections:
        logging_util.warning(
            f"🔧 Injecting {len(pending_system_corrections)} system_corrections into LLM request: "
            f"{pending_system_corrections}"
        )

    # Diagnostic log for god mode investigation (INFO level to ensure visibility in GCP)
    logging_util.info(
        f"🐛 DEBUG_MODE_VALUE: mode={mode!r}, agent={agent.__class__.__name__}, agent.MODE={agent.MODE}"
    )

    # Apply agent-specific input preprocessing (e.g., GodModeAgent adds warning reminder)
    # This MUST happen before LLMRequest.build_story_continuation() to ensure the
    # preprocessed input reaches the LLM.
    user_input = agent.preprocess_input(user_input)
    logging_util.debug(f"📝 After preprocess_input: user_action={user_input[:200]}...")

    logging_util.debug(
        f"📝 Building LLMRequest: user_action={user_input[:200]}..., "
        f"story_history_length={len(stripped_story_context)}"
    )
    if stripped_story_context:
        last_story_entry = stripped_story_context[-1]
        # Guard against non-dict entries from malformed Firestore data
        if isinstance(last_story_entry, dict):
            logging_util.debug(
                f"📝 Last story_history entry: actor={last_story_entry.get('actor')}, "
                f"text={str(last_story_entry.get('text', ''))[:100]}..."
            )

    # CRITICAL FIX (DICE-s8u): Append dice enforcement reminder to user_input for
    # code_execution strategy. Gemini uses code_execution for initial_story but ignores
    # it for continue_story. By adding the reminder at the END of user_input, it's the
    # LAST thing Gemini sees before generating its response, maximizing attention.
    enforced_user_input = user_input
    if dice_roll_strategy == dice_strategy.DICE_STRATEGY_CODE_EXECUTION:
        enforced_user_input = (
            f"{user_input}\n\n"
            "[SYSTEM ENFORCEMENT: For ANY dice roll, you MUST use the code_execution tool "
            "with random.randint(). Your code will be inspected. Fabricated dice = rejection.]"
        )

    gemini_request = LLMRequest.build_story_continuation(
        user_action=enforced_user_input,
        user_id=str(user_id_from_state),
        game_mode=mode,
        game_state=game_state_for_llm,
        story_history=stripped_story_context,
        checkpoint_block=checkpoint_block,
        core_memories=final_core_memories.split("\n") if final_core_memories else [],
        sequence_ids=final_sequence_ids.split(", ") if final_sequence_ids else [],
        entity_tracking=entity_tracking_data,
        selected_prompts=selected_prompts or [],
        use_default_world=use_default_world,
        system_corrections=pending_system_corrections,
    )

    # Log what was actually set in the request (DEBUG level to avoid log noise)
    logging_util.debug(
        f"📝 LLMRequest created: user_action={gemini_request.user_action[:200] if gemini_request.user_action else 'None'}..., "
        f"story_history_length={len(gemini_request.story_history) if gemini_request.story_history else 0}"
    )

    # DEBUG: Log full LLMRequest payload size breakdown
    try:
        payload_json = gemini_request.to_json()
        story_history_tokens = estimate_tokens(
            json.dumps(
                payload_json.get("story_history", []), default=json_default_serializer
            )
        )
        total_payload_tokens = estimate_tokens(
            json.dumps(payload_json, default=json_default_serializer)
        )
        logging_util.info(
            f"LLMREQUEST_PAYLOAD: story_history={story_history_tokens}tk, "
            f"total_payload={total_payload_tokens}tk"
        )
    except Exception as e:
        logging_util.warning(f"Could not measure LLMRequest payload: {e}")

    # Return all prepared data
    return PreparedContinuation(
        agent=agent,
        system_instruction_final=system_instruction_final,
        gemini_request=gemini_request,
        model_to_use=model_to_use,
        provider_selection=provider_selection,
        dice_roll_strategy=dice_roll_strategy,
        is_god_mode_command=is_god_mode_command,
        is_think_mode=is_think_mode,
        checkpoint_block=checkpoint_block,
        core_memories=final_core_memories,
        sequence_ids=final_sequence_ids,
        raw_user_input=raw_user_input,
        processed_user_input=user_input,  # After validation mutations
        temperature_override=temperature_override,
        force_tool_mode=force_tool_mode,
        entity_tracking_data=entity_tracking_data,
        expected_entities=expected_entities,
        truncated_story_context=truncated_story_context,
        final_user_input=enforced_user_input,  # After agent preprocessing + dice enforcement
        classifier_metadata=classifier_metadata,
        budget_warnings_to_show=budget_warnings_to_show,
        new_persist_keys=new_persist_keys,
        user_id=user_id_from_state,
    )


@log_exceptions
def continue_story(  # noqa: PLR0912, PLR0915
    user_input: str,
    mode: str,
    story_context: list[dict[str, Any]],
    current_game_state: GameState,
    selected_prompts: list[str] | None = None,
    use_default_world: bool = False,
    user_id: UserId | None = None,
    include_raw_llm_payloads: bool = False,
    campaign_id: str | None = None,
) -> LLMResponse:
    """
    Continues the story by calling the Gemini API with the current context and game state.

    Args:
        user_input: The user's input text
        mode: The interaction mode (e.g., 'character', 'story')
        story_context: List of previous story entries
        current_game_state: Current GameState object
        selected_prompts: List of selected prompt types
        use_default_world: Whether to include world content in system instructions
        user_id: Optional user ID to retrieve user-specific settings (e.g., preferred model)
        campaign_id: Optional campaign ID for explicit caching (enables Gemini cache reuse)

    Returns:
        LLMResponse: Custom response object containing:
            - narrative_text: Clean text for display (guaranteed to be clean narrative)
            - structured_response: Parsed JSON with state updates, entities, etc.
    """
    # NOTE: Mock mode short-circuit is NOT added here (unlike get_initial_story)
    # because tests use patches on _call_llm_api_with_llm_request to control responses.
    # The _select_provider_and_model() guard already prevents hitting real providers
    # in test mode by returning default Gemini provider which is then mocked.

    # Prepare all data for story continuation using shared preparation logic
    # The _prepare_story_continuation() function handles:
    # - get_static_prompt_parts(current_game_state, truncated_story_context) for
    #   checkpoint_block, core_memories_summary, sequence_id_list_string
    # - _compact_core_memories(core_memories_summary, budget) to get final_core_memories
    # - Capping sequence_id_list_string to allocated budget to get final_sequence_ids
    # Sequence ID budget enforcement is applied in _prepare_story_continuation() to prevent
    # prompt overflows from unbounded sequence-id context.
    #
    # Core memories compaction (_compact_core_memories) is also applied in
    # _prepare_story_continuation() to fit within allocated budget, ensuring we build
    # the prompt from the final compacted core memories rather than any intermediate value.
    prepared = _prepare_story_continuation(
        user_input=user_input,
        mode=mode,
        story_context=story_context,
        current_game_state=current_game_state,
        selected_prompts=selected_prompts,
        use_default_world=use_default_world,
        user_id=user_id,
        campaign_id=campaign_id,
    )

    # Send structured JSON directly to Gemini API (NO string conversion)
    api_response = _call_llm_api_with_llm_request(
        gemini_request=prepared.gemini_request,
        model_name=prepared.model_to_use,
        system_instruction_text=prepared.system_instruction_final,
        provider_name=prepared.provider_selection.provider,
        temperature=prepared.temperature_override,
        force_tool_mode=prepared.force_tool_mode,
        is_think_mode=prepared.is_think_mode,
        user_id=prepared.user_id,
    )
    logging_util.info("Successfully used LLMRequest for structured JSON communication")
    final_api_response = api_response

    code_execution_evidence = _maybe_get_gemini_code_execution_evidence(
        provider_name=prepared.provider_selection.provider,
        model_name=prepared.model_to_use,
        api_response=api_response,
        context="continue_story",
    )
    # Extract text from raw API response object
    raw_response_text: str = _get_text_from_response(api_response)

    # Create initial LLMResponse from raw response
    # Parse the structured response to extract clean narrative and debug data
    narrative_text: str
    structured_response: NarrativeResponse | None
    narrative_text, structured_response = parse_structured_response(
        raw_response_text,
        requires_action_resolution=prepared.agent.requires_action_resolution,
    )
    tool_results_for_dice = getattr(api_response, "_tool_results", None)
    if structured_response:
        dice_integrity.apply_dice_metadata_to_structured_response(
            structured_response=structured_response,
            dice_metadata={
                "tool_results": tool_results_for_dice,
                "tool_requests_executed": bool(
                    getattr(api_response, "_tool_requests_executed", False)
                ),
                "dice_strategy": prepared.dice_roll_strategy,
            },
            dice_roll_strategy=prepared.dice_roll_strategy,
        )

    # Detect missing fields for observability only (no server-side retries).
    is_dm_mode_initial = (
        "[Mode: DM MODE]" in narrative_text or "[Mode: GOD MODE]" in narrative_text
    )
    require_dice_rolls = _should_require_dice_rolls_for_turn(
        current_game_state=current_game_state,
        user_input=user_input,
        mode=mode,
        is_god_mode=prepared.is_god_mode_command,
        is_dm_mode=is_dm_mode_initial,
    )

    # COMBAT DICE INTEGRITY VALIDATION (strictest mode)
    # Detect combat in BOTH user input AND narrative, validate tool execution
    dice_integrity_valid, dice_integrity_reason = _validate_combat_dice_integrity(
        user_input=user_input,
        narrative_text=narrative_text,
        structured_response=structured_response,
        current_game_state=current_game_state,
        api_response=api_response,
        mode=mode,
        is_god_mode=prepared.is_god_mode_command,
        is_dm_mode=is_dm_mode_initial,
        dice_roll_strategy=prepared.dice_roll_strategy,
    )

    # ALWAYS-ON DICE INTEGRITY VALIDATION (native_two_phase only)
    # Catches fabricated dice even when combat is NOT detected (e.g., Arcana checks,
    # absorbing artifacts, skill checks outside combat). Any dice_rolls must have tools.
    # NOTE: Skipped for code_execution strategy - that has its own check.
    always_dice_valid, always_dice_reason = _validate_dice_integrity_always(
        structured_response=structured_response,
        api_response=api_response,
        mode=mode,
        is_god_mode=prepared.is_god_mode_command,
        is_dm_mode=is_dm_mode_initial,
        dice_roll_strategy=prepared.dice_roll_strategy,
    )
    # Combine with combat check - fail if EITHER fails
    if not always_dice_valid and dice_integrity_valid:
        dice_integrity_valid = False
        dice_integrity_reason = always_dice_reason

    # CODE_EXECUTION FABRICATION CHECK (Gemini 3 Flash code_execution mode)
    # If model claims dice_rolls but didn't use code_execution, record an integrity violation.
    code_exec_fabrication = False
    if prepared.dice_roll_strategy == dice_strategy.DICE_STRATEGY_CODE_EXECUTION:
        code_exec_fabrication = _is_code_execution_fabrication(
            structured_response,
            code_execution_evidence,
            tool_requests_executed=bool(
                getattr(api_response, "_tool_requests_executed", False)
            ),
            tool_results=getattr(api_response, "_tool_results", None),
        )
    if code_exec_fabrication:
        dice.log_code_exec_fabrication_violation()

    narrative_dice_fabrication = _detect_narrative_dice_fabrication(
        narrative_text=narrative_text,
        structured_response=structured_response,
        api_response=api_response,
        code_execution_evidence=code_execution_evidence,
        dice_roll_strategy=prepared.dice_roll_strategy,
    )
    debug_enabled = os.getenv("DICE_INTEGRITY_DEBUG", "").lower() == "true"
    dice.log_pre_post_detection_context(
        dice_strategy=prepared.dice_roll_strategy,
        tool_requests_executed=getattr(api_response, "_tool_requests_executed", "N/A"),
        tool_results_count=len(getattr(api_response, "_tool_results", []) or []),
        code_execution_used=(
            code_execution_evidence.get("code_execution_used")
            if code_execution_evidence
            else "N/A"
        ),
        debug_enabled=debug_enabled,
    )
    # Extract dice for logging - PRIMARY: action_resolution, FALLBACK: dice_rolls
    dice_for_logging = None
    action_resolution = getattr(structured_response, "action_resolution", None)
    if isinstance(action_resolution, dict):
        mechanics = action_resolution.get("mechanics", {})
        if isinstance(mechanics, dict):
            dice_for_logging = mechanics.get("rolls") or mechanics.get("audit_events")
    if not dice_for_logging:
        dice_for_logging = getattr(structured_response, "dice_rolls", None)

    dice.log_post_detection_result(
        narrative_dice_fabrication=narrative_dice_fabrication,
        dice_rolls=dice_for_logging,
        debug_enabled=debug_enabled,
    )
    if narrative_dice_fabrication:
        dice.log_narrative_dice_fabrication_violation()

    dice_integrity_violation = (
        not dice_integrity_valid or code_exec_fabrication or narrative_dice_fabrication
    )

    # Social HP enforcement is handled by prepared.agent prompts (narrative_system_instruction.md)
    # NOT by detecting challenge boxes in narrative output.
    #
    # We still detect missing fields for observability (no server-side retries).
    detected_missing_fields = _check_missing_required_fields(
        structured_response,
        mode,
        is_god_mode=prepared.is_god_mode_command,
        is_dm_mode=is_dm_mode_initial,
        require_dice_rolls=require_dice_rolls,
        dice_integrity_violation=dice_integrity_violation,
        require_social_hp_challenge=False,
        debug_mode=getattr(current_game_state, "debug_mode", False),
    )

    # Validate god mode responses for forbidden dice/narrative content
    god_mode_violations = dice_integrity.validate_god_mode_response(
        structured_response,
        is_god_mode=prepared.is_god_mode_command,
    )
    if god_mode_violations and structured_response:
        # Add warnings to debug_info for user visibility
        for warning in god_mode_violations:
            _append_server_warning(structured_response, warning)

    # Note: dice_roll_strategy is already set in prepared (either from model default or None for god mode)
    # No need to re-derive it here
    capture_raw = os.getenv("CAPTURE_RAW_LLM", "true").lower() == "true"
    capture_tools = True
    raw_limit = _get_raw_limit()
    processing_metadata: dict[str, Any] = {
        "llm_provider": prepared.provider_selection.provider,
        "llm_model": prepared.model_to_use,
        "execution_path": "non_streaming",
        "llm_missing_fields": detected_missing_fields,
    }
    if capture_raw:
        processing_metadata["raw_response_text"] = raw_response_text
    if include_raw_llm_payloads:
        # Return raw payloads to callers without persisting them to Firestore.
        # Store full request and full response for forensic/debug evidence.
        raw_request_payload = None
        raw_request_capture_errors: list[str] = []
        payload_builders = (
            ("to_json", lambda: prepared.gemini_request.to_json()),
            ("dict", lambda: dict(prepared.gemini_request.__dict__)),
        )
        for payload_mode, payload_builder in payload_builders:
            try:
                raw_request_payload = json.loads(
                    json.dumps(payload_builder(), default=json_default_serializer)
                )
                break
            except Exception as e:
                raw_request_capture_errors.append(
                    f"{payload_mode}: {type(e).__name__}: {e}"
                )
                logging_util.debug(
                    "RAW_REQUEST capture attempt failed (%s): %s", payload_mode, e
                )
        if raw_request_payload is None:
            logging_util.warning(
                "RAW_REQUEST capture failed (include_raw_llm_payloads): "
                f"{'; '.join(raw_request_capture_errors) or 'all retries failed'}"
            )
            raw_request_payload = {
                "_capture_error": "; ".join(raw_request_capture_errors),
            }
        processing_metadata["raw_request_payload"] = raw_request_payload
        if "raw_response_text" not in processing_metadata:
            processing_metadata["raw_response_text"] = raw_response_text
    processing_metadata.update(
        dice_integrity.build_dice_processing_metadata(
            api_response=final_api_response,
            dice_roll_strategy=prepared.dice_roll_strategy,
            capture_tools=capture_tools,
        )
    )

    if capture_raw:
        _log_raw_llm_data(
            system_instruction_final=prepared.system_instruction_final,
            gemini_request=prepared.gemini_request,
            raw_response_text=raw_response_text,
            raw_limit=raw_limit,
            provider_name=prepared.provider_selection.provider,
            model_name=prepared.model_to_use,
            api_response=api_response,
        )

    if structured_response:
        debug_info = structured_response.debug_info or {}
        debug_info.setdefault("llm_provider", prepared.provider_selection.provider)
        debug_info.setdefault("llm_model", prepared.model_to_use)
        debug_info.setdefault("execution_path", "non_streaming")
        # Capture which prepared.agent served this request
        debug_info["agent_name"] = prepared.agent.__class__.__name__
        # Capture intent classifier metadata for test validation
        debug_info["intent_classifier"] = prepared.classifier_metadata
        # Capture which instruction files were loaded (lightweight evidence)
        # NOTE: We only store filenames and char count, NOT full text (saves ~36KB/entry)
        debug_info["system_instruction_files"] = get_loaded_instruction_files()
        debug_info["system_instruction_char_count"] = len(
            prepared.system_instruction_final
        )
        # Capture identity block and directives block for explicit evidence (small, keep these)
        if hasattr(prepared.agent, "prompt_builder"):
            pb = prepared.agent.prompt_builder
            if pb.last_identity_block:
                debug_info["character_identity_block"] = pb.last_identity_block
            if pb.last_directives_block:
                debug_info["god_mode_directives_block"] = pb.last_directives_block
        if code_execution_evidence:
            debug_info.update(code_execution_evidence)
            _log_fabricated_dice_if_detected(
                structured_response,
                code_execution_evidence,
                tool_requests_executed=bool(
                    getattr(api_response, "_tool_requests_executed", False)
                ),
                tool_results=getattr(api_response, "_tool_results", None),
            )
        structured_response.debug_info = debug_info
        dice_integrity.apply_dice_metadata_to_structured_response(
            structured_response=structured_response,
            dice_metadata=processing_metadata,
            dice_roll_strategy=prepared.dice_roll_strategy,
        )
        # Add user warning if API required retries (transient error recovery)
        _add_api_retry_warning_to_response(final_api_response, structured_response)

        # Add enforcement warning when code_execution fabrication is detected.
        # Distinguishes "code ran without RNG" vs "no code execution at all".
        if code_exec_fabrication:
            raw_code_execution_used = (
                code_execution_evidence.get("code_execution_used")
                if isinstance(code_execution_evidence, dict)
                else None
            )
            code_was_executed = raw_code_execution_used is True
            if code_was_executed:
                fabrication_warning = (
                    "⚠️ Dice Integrity Warning: Code execution detected but no verified RNG usage. "
                    "Dice values may not be authentic random results."
                )
            else:
                fabrication_warning = (
                    "⚠️ Dice Integrity Warning: No code execution used for dice rolls. "
                    "Dice values were not generated by RNG and may not be authentic."
                )
            _append_warning_to_debug_info(
                debug_info,
                fabrication_warning,
                "🚨 DICE-s8u ENFORCEMENT: Added fabrication warning to user response",
            )
            # Flag fabrication so persistence layer can inject a correction entry
            # into story context for the next turn (zero-latency self-correction).
            # ARCHITECTURAL FIX: Store in processing_metadata instead of model-supplied debug_info
            # to maintain proper trust boundary (server-authored data should not live in model output).
            action_res_for_correction = getattr(
                structured_response, "action_resolution", {}
            )
            fabricated_rolls = []
            if isinstance(action_res_for_correction, dict):
                mechanics = action_res_for_correction.get("mechanics", {})
                if isinstance(mechanics, dict):
                    rolls_value = None
                    for key in ("rolls", "Rolls", "ROLLS"):
                        if key in mechanics:
                            rolls_value = mechanics[key]
                            break
                    if isinstance(rolls_value, list):
                        fabricated_rolls = rolls_value
            processing_metadata["dice_fabrication_correction"] = {
                "code_execution_used": bool(code_was_executed),
                "fabricated_rolls": fabricated_rolls,
            }
        # SECURITY: Always clear LLM-provided _server_dice_fabrication_correction to prevent spoofing
        # (LLM should never be able to set server-prefixed fields)
        if "_server_dice_fabrication_correction" in debug_info:
            del debug_info["_server_dice_fabrication_correction"]
            logging_util.info(
                "🛡️ DICE SECURITY: Cleared LLM-provided _server_dice_fabrication_correction field"
            )
        # DICE-s8u: Add warning when DC is set after RNG in code_execution
        if code_execution_evidence:
            dc_before_rng = code_execution_evidence.get("dc_set_before_rng")
            dc_before_next_rng = code_execution_evidence.get("dc_set_before_next_rng")
            if dc_before_rng is False:
                if dc_before_next_rng is True:
                    dc_order_warning = (
                        "⚠️ Dice Integrity Warning: DC was set after earlier RNG in code "
                        "execution. DC should be decided before any RNG to avoid post-hoc bias."
                    )
                else:
                    dc_order_warning = (
                        "⚠️ Dice Integrity Warning: DC was set after RNG in code execution. "
                        "DC must be decided before rolling."
                    )
                _append_warning_to_debug_info(
                    debug_info,
                    dc_order_warning,
                    "🚨 DICE-s8u ENFORCEMENT: Added DC-before-RNG warning to user response",
                )
            elif dc_before_rng is True and dc_before_next_rng is False:
                dc_order_warning = (
                    "⚠️ Dice Integrity Warning: A DC assignment appears after the last RNG call. "
                    "Each DC must be followed by its corresponding roll, not defined afterward."
                )
                _append_warning_to_debug_info(
                    debug_info,
                    dc_order_warning,
                    "🚨 DICE-s8u ENFORCEMENT: Added DC-before-next-RNG warning to user response",
                )
            # Schema-based validation: warn when DC is present but dc_reasoning is missing
            dc_reasoning_missing = code_execution_evidence.get("dc_reasoning_missing")
            if dc_reasoning_missing:
                reasoning_warning = (
                    "⚠️ Dice Integrity Warning: Skill check DC was set without explanation. "
                    "DCs should include dc_reasoning to show fair difficulty assessment."
                )
                _append_warning_to_debug_info(
                    debug_info,
                    reasoning_warning,
                    "🚨 DICE ENFORCEMENT: Added dc_reasoning_missing warning to user response",
                )

    # DIAGNOSTIC LOGGING: Log parsed response details for debugging empty narrative issues
    logging_util.info(
        f"📊 PARSED_RESPONSE: narrative_length={len(narrative_text)}, "
        f"structured_response={'present' if structured_response else 'None'}, "
        f"raw_response_length={len(raw_response_text)}"
    )
    if len(narrative_text) == 0:
        # Include preview suffix only if response was truncated
        raw_preview = raw_response_text[:500]
        preview_suffix = "..." if len(raw_response_text) > 500 else ""
        logging_util.warning(
            f"⚠️ EMPTY_NARRATIVE: LLM returned empty narrative. "
            f"Raw response preview: {raw_preview}{preview_suffix}"
        )
        # Log structured response fields if available
        if structured_response:
            has_planning = bool(
                structured_response.planning_block
                if hasattr(structured_response, "planning_block")
                else False
            )
            has_session = bool(
                structured_response.session_header
                if hasattr(structured_response, "session_header")
                else False
            )
            logging_util.warning(
                f"⚠️ EMPTY_NARRATIVE: structured_response has planning_block={has_planning}, "
                f"session_header={has_session}"
            )

    # Provider hardening: non-god responses must never emit empty narrative.
    # Keep a deterministic fallback so Firestore writes/evidence remain stable.
    if len(narrative_text.strip()) == 0:
        has_god_mode_response = bool(
            structured_response
            and getattr(structured_response, constants.FIELD_GOD_MODE_RESPONSE, "")
        )
        if not has_god_mode_response:
            narrative_text = JSON_PARSE_FALLBACK_MARKER
            if structured_response:
                structured_response.narrative = narrative_text

    # Create LLMResponse with proper debug content separation
    # Include agent_mode as single source of truth for mode detection in world_logic.py
    # Include budget_warnings for UI display (already filtered by persistence logic)
    if structured_response:
        # Use structured response (preferred) - ensures clean separation
        gemini_response = LLMResponse.create_from_structured_response(
            structured_response,
            prepared.model_to_use,
            combined_narrative_text=narrative_text,
            provider=prepared.provider_selection.provider,
            processing_metadata=processing_metadata,
            agent_mode=prepared.agent.MODE,
            raw_response_text=raw_response_text,
            budget_warnings=prepared.budget_warnings_to_show,
        )
    else:
        # Fallback to legacy mode for non-JSON responses
        gemini_response = LLMResponse.create_legacy(
            narrative_text,
            prepared.model_to_use,
            provider=prepared.provider_selection.provider,
            processing_metadata=processing_metadata,
            agent_mode=prepared.agent.MODE,
            raw_response_text=raw_response_text,
            budget_warnings=prepared.budget_warnings_to_show,
        )

    # Persist budget warning keys to suppress future duplicate warnings
    if prepared.new_persist_keys:
        _save_warning_persist_keys(current_game_state, prepared.new_persist_keys)

    response_text: str = gemini_response.narrative_text

    # Validate entity tracking if enabled
    if prepared.expected_entities:
        # Use the common validation function for entity tracking validation
        # (No longer modifies response_text - validation goes to logs only)
        _validate_entity_tracking(
            response_text, prepared.expected_entities, current_game_state
        )

    # Validate and enforce planning block for story mode
    # Check if user is switching to god mode with their input
    user_input_lower: str = prepared.raw_user_input.lower().strip()
    is_switching_to_god_mode: bool = user_input_lower in constants.MODE_SWITCH_SIMPLE

    # Check if user sent a "GOD MODE:" prefixed command (administrative mode)
    # God mode = DM mode behavior: no narrative advancement, no planning blocks
    # Also check if the AI response indicates DM MODE
    is_dm_mode_response: bool = (
        "[Mode: DM MODE]" in response_text or "[Mode: GOD MODE]" in response_text
    )

    # Only add planning blocks if:
    # 1. Currently in character or think mode
    # 2. User isn't switching to god mode
    # 3. AI response isn't in DM mode
    # 4. User didn't send a GOD MODE: command (administrative, not gameplay)
    if (
        mode in (constants.MODE_CHARACTER, constants.MODE_THINK)
        and not is_switching_to_god_mode
        and not is_dm_mode_response
        and not prepared.is_god_mode_command
    ):
        response_text = _validate_and_enforce_planning_block(
            response_text,
            structured_response=gemini_response.structured_response,
        )

    # MODERNIZED: No longer recreate LLMResponse based on response_text modifications
    # The structured_response is now the authoritative source, response_text is for backward compatibility only
    # The frontend uses gemini_response.structured_response directly, not narrative_text

    # POST-PROCESSING: Add equipment_display if this was an equipment query
    # This guarantees 100% accuracy by reading directly from game_state
    logging_util.debug(f"🔍 EQUIPMENT_QUERY_CHECK: user_input={user_input[:80]}...")
    if is_equipment_query(user_input):
        logging_util.info(
            "📦 EQUIPMENT_QUERY_DETECTED: Extracting equipment from game_state"
        )
        equipment_display = extract_equipment_display(current_game_state)
        logging_util.info(f"📦 EQUIPMENT_EXTRACTED: {len(equipment_display)} items")
        if equipment_display:
            gemini_response.processing_metadata["equipment_display"] = equipment_display
            logging_util.info(
                f"📦 EQUIPMENT_DISPLAY: Added {len(equipment_display)} items from game_state"
            )
            # Ensure narrative includes item names so users know equipment isn't ignored
            gemini_response.narrative_text = ensure_equipment_summary_in_narrative(
                gemini_response.narrative_text,
                equipment_display,
                user_input=prepared.raw_user_input,
                min_item_mentions=2,
            )
    else:
        logging_util.debug("🔍 EQUIPMENT_QUERY_SKIP: Not an equipment query")

    # Log LLMResponse creation - INFO level for production visibility
    logging_util.info(
        f"📝 FINAL_RESPONSE: narrative_length={len(gemini_response.narrative_text)}, "
        f"has_structured_response={gemini_response.structured_response is not None}"
    )

    # Return our custom LLMResponse object (not raw API response)
    # This object contains:
    # - narrative_text: Clean text for display (guaranteed to be clean narrative)
    # - structured_response: Parsed JSON structure with state updates, entities, etc.
    # - processing_metadata: Additional metadata including equipment_display when relevant
    if gemini_response.structured_response and hasattr(
        gemini_response.structured_response, "narrative"
    ):
        gemini_response.structured_response.narrative = gemini_response.narrative_text
    return gemini_response


def _build_mock_streaming_text(*, is_god_mode_command: bool) -> str:
    """Build deterministic mock LLM response text for MOCK_SERVICES_MODE streaming tests.

    Returns a JSON string that satisfies all streaming contract validators:
    - god mode: includes non-empty god_mode_response
    - other modes: includes non-empty narrative and planning_block with choices
    """
    if is_god_mode_command:
        return json.dumps(
            {
                "narrative": "",
                "god_mode_response": (
                    "=== GOD MODE INFORMATION (mock) ===\n\n"
                    "Current state: Mock testing environment.\n"
                    "All systems nominal for smoke test coverage.\n"
                    "No real game state changes were made."
                ),
                "session_header": "",
                "planning_block": {},
                "state_updates": {},
                "debug_info": {
                    "agent_mode": "god",
                    "mock_seed": "mock_streaming_god_mode",
                },
            },
            indent=2,
        )
    return json.dumps(
        {
            "narrative": (
                "Mock mode streaming response: the turn advances on a deterministic path "
                "with a valid state progression and transparent planning block."
            ),
            "session_header": "Scene #Mock",
            "planning_block": {
                "thinking": "Mock mode active. Deterministic server path selected.",
                "choices": {
                    "continue_forward": {
                        "text": "Continue Forward",
                        "description": "Continue with deterministic mock path continuation",
                        "risk_level": "low",
                    },
                    "assess_situation": {
                        "text": "Assess Situation",
                        "description": "Strategic review of current tactical position",
                        "risk_level": "none",
                    },
                },
            },
            "state_updates": {},
            "debug_info": {
                "agent_mode": "mock",
                "mock_seed": "mock_streaming_deterministic",
            },
        },
        indent=2,
    )


def _is_mocked_callable(target: object) -> bool:
    """Best-effort detection for unittest.mock-based callables without importing it."""
    return callable(target) and any(
        hasattr(target, attr)
        for attr in (
            "assert_called",
            "assert_called_once",
            "mock_calls",
            "return_value",
        )
    )


def _build_streaming_response_signature(
    *,
    request_id: str,
    response_text: str,
    execution_trace: dict[str, Any],
    signing_secret: str | None,
) -> dict[str, Any]:
    """Build a deterministic response fingerprint for streaming done-event proof.

    The signature is content-addressed for every response + trace pair.
    When a secret is provided, it becomes an HMAC for integrity verification.
    """
    signature_payload = json.dumps(
        {
            "request_id": request_id,
            "response_text": response_text,
            "execution_trace": execution_trace,
        },
        sort_keys=True,
        separators=(",", ":"),
        default=json_default_serializer,
    )

    if signing_secret:
        digest = hmac.new(
            signing_secret.encode("utf-8"),
            signature_payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        algorithm = "hmac-sha256"
        signed = True
    else:
        digest = hashlib.sha256(signature_payload.encode("utf-8")).hexdigest()
        algorithm = "sha256"
        signed = False

    return {
        "schema_version": "streaming-response-v1",
        "algorithm": algorithm,
        "digest": digest,
        "signed": signed,
        "response_length": len(response_text),
        "request_id": request_id,
    }


def _classify_raw_narrative(text: str) -> bool:
    """Return True when *text* is a genuine string narrative suitable for streaming fallback.

    A genuine narrative is non-empty, not the JSON-parse sentinel, contains at least
    one alphabetic character, and does not parse to a non-string JSON value (dict,
    list, null, bool, number).  JSON-quoted strings such as '"You wait."' *do*
    parse to ``str`` and are therefore treated as narrative (True).

    Malformed JSON (e.g. truncated or syntax-error) that fails to parse must NOT
    be classified as narrative — otherwise raw JSON gets stored as story text.
    Reject text that looks like JSON (starts with ``{`` or ``[``) even when parse fails.
    """
    if not text or not text.strip():
        return False
    if text == JSON_PARSE_FALLBACK_MARKER:
        return False
    stripped = text.strip()
    if stripped.startswith("{") or stripped.startswith("["):
        return False
    try:
        _parsed = json.loads(text)
        if not isinstance(_parsed, str):
            return False
    except json.JSONDecodeError:
        pass
    return any(c.isalpha() for c in text)


def continue_story_streaming(
    user_input: str,
    mode: str,
    story_context: list[dict[str, Any]],
    current_game_state: GameState,
    selected_prompts: list[str] | None = None,
    use_default_world: bool = False,
    user_id: UserId | None = None,
    include_raw_llm_payloads: bool = False,
    campaign_id: str | None = None,
) -> Generator[Any, None, None]:
    """Stream story continuation with the same logic as continue_story.

    This function mirrors continue_story but yields StreamEvent objects
    instead of returning an LLMResponse. It uses the SAME:
    - Provider/model selection
    - Agent selection and system instructions
    - LLMRequest building
    - Budget allocation

    The key difference is that it streams the LLM response chunks instead
    of waiting for completion.

    Args:
        user_input: The user's input text
        mode: The interaction mode (e.g., 'character', 'story')
        story_context: List of previous story entries
        current_game_state: Current GameState object
        selected_prompts: List of selected prompt types
        use_default_world: Whether to include world content in system instructions
        user_id: Optional user ID to retrieve user-specific settings
        campaign_id: Optional campaign ID

    Yields:
        StreamEvent objects: status, chunk, tool_result, warning, error, done
    """
    full_text_parts: list[str] = []
    sequence = 0
    request_id: str | None = None

    try:
        t_prep_start = time.perf_counter()
        prepared = _prepare_story_continuation(
            user_input=user_input,
            mode=mode,
            story_context=story_context,
            current_game_state=current_game_state,
            selected_prompts=selected_prompts,
            use_default_world=use_default_world,
            user_id=user_id,
            campaign_id=campaign_id,
        )
        is_god_mode_command = bool(getattr(prepared, "is_god_mode_command", False))
        t_prep_end = time.perf_counter()
        logging_util.info(
            "⏱️ STREAM_TIMING | _prepare_story_continuation: %.3fs",
            t_prep_end - t_prep_start,
        )

        # Convert LLMRequest to JSON string for streaming
        json_data = prepared.gemini_request.to_json()
        json_data["priority_instruction"] = (
            "CRITICAL: Respond to user_action field, NOT story_history or game_state entries."
        )
        json_data["message_type"] = "story_continuation"
        json_string = json.dumps(json_data, indent=2, default=json_default_serializer)
        effective_json_string = json_string
        effective_system_instruction = prepared.system_instruction_final
        stream_cache_name: str | None = None
        stream_cache_source = "not_used"
        stream_cache_requested = False
        t_json_end = time.perf_counter()
        logging_util.info(
            "⏱️ STREAM_TIMING | json_serialization: %.3fs | payload_bytes=%d",
            t_json_end - t_prep_end,
            len(json_string.encode("utf-8")),
        )
        prompt_size_bytes = len(json_string.encode("utf-8"))
        if prompt_size_bytes > MAX_PAYLOAD_SIZE:
            raise PayloadTooLargeError(
                f"Prompt payload too large: {prompt_size_bytes} bytes exceeds limit of {MAX_PAYLOAD_SIZE} bytes"
            )

        if prepared.provider_selection.provider not in {
            constants.LLM_PROVIDER_GEMINI,
            constants.LLM_PROVIDER_OPENCLAW,
            constants.LLM_PROVIDER_OPENROUTER,
        }:
            yield StreamEvent(
                type="error",
                payload={
                    "message": (
                        "Streaming is currently supported only for Gemini, OpenClaw, and OpenRouter providers. "
                        f"Selected provider was: {prepared.provider_selection.provider}."
                    ),
                    "error_type": "streaming_unsupported_provider",
                    "provider_used": prepared.provider_selection.provider,
                },
            )
            return

        effective_temperature = (
            prepared.temperature_override
            if prepared.temperature_override is not None
            else TEMPERATURE
        )

        user_api_key = _get_user_api_key_for_provider(
            user_id=prepared.user_id,
            provider_name=prepared.provider_selection.provider,
        )
        logging_util.info(
            "BYOK_RESOLUTION: user_id=%s, provider=%s, has_byok=%s",
            prepared.user_id,
            prepared.provider_selection.provider,
            user_api_key is not None,
        )

        # Capture mock-mode once here so all downstream code (cache gating,
        # MCP guard, done payload, etc.) use a consistent per-request value
        # rather than re-evaluating _is_mock_services_mode() after the Flask
        # request context may have been torn down.
        is_mock_mode = _is_mock_services_mode()

        # Streaming explicit cache path (production default endpoint).
        # Keep non-streaming cache support intact; this augments streaming only.
        if (
            constants.EXPLICIT_CACHE_ENABLED
            and not is_mock_mode
            and prepared.provider_selection.provider == constants.LLM_PROVIDER_GEMINI
            and isinstance(getattr(prepared.gemini_request, "game_state", None), dict)
        ):
            stream_cache_requested = True
            cache_campaign_id = prepared.gemini_request.game_state.get("campaign_id")
            story_history = getattr(prepared.gemini_request, "story_history", None)
            if cache_campaign_id and story_history:
                cache_mgr = get_cache_manager(cache_campaign_id)
                cache_client = gemini_provider.get_client(api_key=user_api_key)
                if cache_mgr.has_pending_cache():
                    cache_mgr.promote_pending_cache(client=cache_client)

                story_count = len(story_history)
                requires_code_execution = (
                    prepared.model_to_use in constants.MODELS_WITH_CODE_EXECUTION
                )

                def _build_streaming_merged_payload(
                    cached_entry_count: int,
                ) -> str:
                    cacheable_payload, uncacheable_payload = (
                        prepared.gemini_request.to_explicit_cache_parts(
                            cached_entry_count=cached_entry_count
                        )
                    )
                    merged = _merge_cache_payloads(
                        cacheable_payload, uncacheable_payload
                    )
                    merged["priority_instruction"] = (
                        "CRITICAL: Respond to user_action field, NOT story_history or game_state entries."
                    )
                    merged["message_type"] = "story_continuation"
                    return json.dumps(
                        merged,
                        indent=2,
                        default=json_default_serializer,
                    )

                if cache_mgr.should_rebuild(
                    story_count,
                    requires_code_execution=requires_code_execution,
                    model_name=prepared.model_to_use,
                ):
                    logging_util.info(
                        f"📦 CACHE_BUILD: campaign={cache_campaign_id}, "
                        f"total_entries={story_count}, caching={story_count}, "
                        f"previously_cached={cache_mgr.cached_entry_count}, "
                        f"threshold={cache_mgr.REBUILD_THRESHOLD}"
                    )
                    cacheable_payload, _ = (
                        prepared.gemini_request.to_explicit_cache_parts(
                            cached_entry_count=story_count
                        )
                    )
                    old_story_entries = cacheable_payload.get("story_history", [])
                    cached_story_parts = [
                        json.dumps(entry, indent=2, default=json_default_serializer)
                        for entry in old_story_entries
                    ]
                    cache_system_instruction = apply_code_execution_system_instruction(
                        prepared.system_instruction_final, prepared.model_to_use
                    )
                    cache_tools = None
                    if requires_code_execution:
                        cache_tools = [types.Tool(code_execution={})]
                    try:
                        cache_result = cache_mgr.create_cache(
                            client=cache_client,
                            system_instruction=cache_system_instruction or "",
                            story_entries=cached_story_parts,
                            model_name=prepared.model_to_use,
                            actual_story_count=story_count,
                            tools=cache_tools,
                        )
                        stream_cache_source = "created"
                        effective_json_string = _build_streaming_merged_payload(
                            cached_entry_count=cache_mgr.cached_entry_count
                        )
                        # N-1 deferral: cache_result.cache_name is None for first-ever
                        # (no old cache), or the old cache name for rebuilds (still valid).
                        stream_cache_name = cache_result.cache_name
                        effective_system_instruction = (
                            prepared.system_instruction_final
                            if stream_cache_name is None
                            else None
                        )
                    except Exception as e:
                        logging_util.warning(
                            f"🚨 CACHE_CREATE_FAILED: campaign={cache_campaign_id}, "
                            f"error='{e}'. Falling back to uncached streaming."
                        )
                        cache_mgr.reset_cache(cache_client)
                        stream_cache_source = "create_failed"
                        stream_cache_name = None
                else:
                    stream_cache_name = cache_mgr.get_cache_name()
                    cached_entry_count = cache_mgr.cached_entry_count
                    logging_util.info(
                        f"📦 CACHE_REUSE: campaign={cache_campaign_id}, "
                        f"cache={stream_cache_name}, entries={story_count}, "
                        f"cached={cached_entry_count}"
                    )
                    if stream_cache_name:
                        stream_cache_source = "reused"
                        effective_json_string = _build_streaming_merged_payload(
                            cached_entry_count=cached_entry_count
                        )
                        effective_system_instruction = None
                    else:
                        stream_cache_source = "reused_missing_name"

        t_token_start = time.perf_counter()
        prompt_tokens, system_tokens = _calculate_prompt_and_system_tokens(
            user_prompt_contents=[effective_json_string],
            system_instruction_text=effective_system_instruction,
            provider_name=prepared.provider_selection.provider,
            model_name=prepared.model_to_use,
        )
        max_output_tokens = _get_safe_output_token_limit(
            model_name=prepared.model_to_use,
            prompt_tokens=prompt_tokens,
            system_tokens=system_tokens,
        )
        t_token_end = time.perf_counter()
        logging_util.info(
            "⏱️ STREAM_TIMING | token_calculation: %.3fs | prompt_tokens=%d system_tokens=%d max_output=%d",
            t_token_end - t_token_start,
            prompt_tokens,
            system_tokens,
            max_output_tokens,
        )

        # === STREAMING API CALL ===
        # Initialize chunk logger for BD-iwr evidence standard
        if _is_mcp_real_mode() and is_mock_mode:
            logging_util.error(
                "MODE_GUARD: MCP_TEST_MODE=real with MOCK_SERVICES_MODE=true is "
                "invalid for streaming"
            )
            yield StreamEvent(
                type="error",
                payload={
                    "message": (
                        "Invalid mode configuration: MCP_TEST_MODE=real cannot be "
                        "used with MOCK_SERVICES_MODE=true."
                    ),
                    "error_type": "mode_configuration_conflict",
                    "mock_services_mode": True,
                    "test_mode": "real",
                },
            )
            return

        request_id = (
            f"{campaign_id}_{int(datetime.now(UTC).timestamp())}"
            if campaign_id
            else "unknown"
        )
        chunk_logger = get_or_create_chunk_logger(
            request_id=request_id,
            campaign_id=campaign_id,
        )

        t_llm_start = time.perf_counter()
        stream_start_time = datetime.now(UTC).isoformat()
        first_chunk_logged = False
        gateway_port = _get_openclaw_gateway_port(
            user_id=prepared.user_id,
            provider_name=prepared.provider_selection.provider,
        )
        gateway_url = _get_openclaw_gateway_url(
            user_id=prepared.user_id,
            provider_name=prepared.provider_selection.provider,
        )
        gateway_token = _get_openclaw_gateway_token(
            user_id=prepared.user_id,
            provider_name=prepared.provider_selection.provider,
        )
        phase1_source = "provider"
        phase2_source = "not_executed"
        phase2_executed = False
        phase1_chunk_count = 0
        phase2_chunk_count = 0
        is_gemini_stream_callable_mock = is_mock_mode and _is_mocked_callable(
            gemini_provider.generate_content_stream_sync
        )
        is_openclaw_stream_callable_mock = is_mock_mode and _is_mocked_callable(
            openclaw_provider.generate_content_stream_sync
        )
        is_openrouter_stream_callable_mock = is_mock_mode and _is_mocked_callable(
            openrouter_provider.generate_content_stream_sync
        )
        if is_mock_mode:
            # Mock mode normally skips direct provider calls and returns deterministic text.
            # When the provider function is mocked in tests, still call it so call counts
            # and kwargs assertions remain valid.
            if (
                prepared.provider_selection.provider == constants.LLM_PROVIDER_GEMINI
                and is_gemini_stream_callable_mock
            ):
                logging_util.info(
                    "MOCK_SERVICES_MODE: streaming path using mocked Gemini provider "
                    "(is_god_mode_command=%s)",
                    is_god_mode_command,
                )
                phase1_source = "mock_callable"
                stream_iter = gemini_provider.generate_content_stream_sync(
                    prompt_contents=[effective_json_string],
                    model_name=prepared.model_to_use,
                    system_instruction_text=effective_system_instruction,
                    temperature=effective_temperature,
                    max_output_tokens=max_output_tokens,
                    json_mode=True,
                    api_key=user_api_key,
                    cache_name=stream_cache_name,
                )
            elif (
                prepared.provider_selection.provider == constants.LLM_PROVIDER_OPENCLAW
                and is_openclaw_stream_callable_mock
            ):
                logging_util.info(
                    "MOCK_SERVICES_MODE: streaming path using mocked OpenClaw provider "
                    "(is_god_mode_command=%s)",
                    is_god_mode_command,
                )
                phase1_source = "mock_callable"
                stream_iter = openclaw_provider.generate_content_stream_sync(
                    prompt_contents=[effective_json_string],
                    model_name=prepared.model_to_use,
                    system_instruction_text=effective_system_instruction,
                    temperature=effective_temperature,
                    max_output_tokens=max_output_tokens,
                    json_mode=True,
                    api_key=user_api_key,
                    gateway_port=gateway_port,
                    gateway_url=gateway_url,
                    gateway_token=gateway_token,
                )
            elif (
                prepared.provider_selection.provider
                == constants.LLM_PROVIDER_OPENROUTER
                and is_openrouter_stream_callable_mock
            ):
                logging_util.info(
                    "MOCK_SERVICES_MODE: streaming path using mocked OpenRouter provider "
                    "(is_god_mode_command=%s)",
                    is_god_mode_command,
                )
                phase1_source = "mock_callable"
                stream_iter = openrouter_provider.generate_content_stream_sync(
                    prompt_contents=[json_string],
                    model_name=prepared.model_to_use,
                    system_instruction_text=prepared.system_instruction_final,
                    temperature=effective_temperature,
                    max_output_tokens=max_output_tokens,
                    json_mode=True,
                    api_key=user_api_key,
                )
            else:
                logging_util.info(
                    "MOCK_SERVICES_MODE: streaming path using local mock response "
                    "(is_god_mode_command=%s)",
                    is_god_mode_command,
                )
                phase1_source = "mock_local_fallback"
                stream_iter = iter(
                    [
                        _build_mock_streaming_text(
                            is_god_mode_command=is_god_mode_command
                        )
                    ]
                )
        elif prepared.provider_selection.provider == constants.LLM_PROVIDER_GEMINI:
            phase1_source = "provider"

            def _gemini_stream_with_cache_fallback():
                nonlocal stream_cache_source, stream_cache_name
                # Inject provably-fair seed for code execution models when using cache
                # (same pattern as non-streaming path - seed goes in prompt, not system_instruction)
                _effective_prompt_contents = [effective_json_string]
                _effective_system_instruction = effective_system_instruction
                if prepared.model_to_use in constants.MODELS_WITH_CODE_EXECUTION:
                    _pf_seed = dice_provably_fair.generate_server_seed()
                    logging_util.info(
                        f"PROVABLY_FAIR: commitment={dice_provably_fair.compute_commitment(_pf_seed)}"
                    )
                    _seed_override_text = (
                        f"SERVER_SEED={_pf_seed}. Use random.seed('{_pf_seed}') "
                        "instead of time.time_ns()."
                    )
                    _seed_content = types.Content(
                        role="user",
                        parts=[types.Part(text=_seed_override_text)],
                    )
                    _effective_prompt_contents = [
                        _seed_content
                    ] + _effective_prompt_contents
                    # When using cache, system instruction is baked in - set to None
                    # For N-1 first-ever deferred (no cache), keep system_instruction active
                    if stream_cache_name:
                        _effective_system_instruction = None
                _initial_iter = gemini_provider.generate_content_stream_sync(
                    prompt_contents=_effective_prompt_contents,
                    model_name=prepared.model_to_use,
                    system_instruction_text=_effective_system_instruction,
                    temperature=effective_temperature,
                    max_output_tokens=max_output_tokens,
                    json_mode=True,
                    api_key=user_api_key,
                    cache_name=stream_cache_name,
                )
                try:
                    yield from _initial_iter
                except Exception as _e:
                    _err = str(_e)
                    if stream_cache_name:
                        # Any error while a cache is active: give up on the cache
                        # and retry without it. Cache errors (stale, model mismatch,
                        # FAILED_PRECONDITION, PERMISSION_DENIED) are the common cause,
                        # but even unrelated errors are better retried uncached than
                        # surfaced to the user as a broken action.
                        _is_key_mismatch = (
                            "API_KEY_INVALID" in _err or "API key expired" in _err
                        )
                        _is_precondition = (
                            "FAILED_PRECONDITION" in _err
                            or "Precondition check failed" in _err
                        )
                        _is_stale = (
                            "CachedContent not found" in _err
                            or "NOT_FOUND" in _err
                            or "PERMISSION_DENIED" in _err
                        )
                        # Only reset for actual cache errors - don't nuke valid caches for
                        # quota/safety/rate-limit errors
                        if _is_key_mismatch or _is_precondition or _is_stale:
                            _reason = (
                                "key_mismatch"
                                if _is_key_mismatch
                                else ("precondition" if _is_precondition else "stale")
                            )
                            logging_util.warning(
                                f"🚨 STREAM_CACHE_STALE: cache={stream_cache_name}, "
                                f"reason={_reason}, error='{_err}'. Resetting cache and retrying uncached."
                            )
                            cache_mgr.reset_cache(cache_client)
                            stream_cache_source = "stale_fallback"
                            stream_cache_name = None
                            yield from gemini_provider.generate_content_stream_sync(
                                prompt_contents=(
                                    [_seed_content, json_string]
                                    if prepared.model_to_use
                                    in constants.MODELS_WITH_CODE_EXECUTION
                                    else [json_string]
                                ),
                                model_name=prepared.model_to_use,
                                system_instruction_text=prepared.system_instruction_final,
                                temperature=effective_temperature,
                                max_output_tokens=max_output_tokens,
                                json_mode=True,
                                api_key=user_api_key,
                                cache_name=None,
                            )
                        else:
                            # Unknown error - don't reset cache, let it propagate
                            logging_util.warning(
                                f"🚨 STREAM_API_ERROR (cache preserved): cache={stream_cache_name}, "
                                f"error='{_err}'. Not resetting cache - will surface error to user."
                            )
                            raise
                    else:
                        raise

            stream_iter = _gemini_stream_with_cache_fallback()
        elif prepared.provider_selection.provider == constants.LLM_PROVIDER_OPENROUTER:
            phase1_source = "provider"
            stream_iter = openrouter_provider.generate_content_stream_sync(
                prompt_contents=[json_string],
                model_name=prepared.model_to_use,
                system_instruction_text=prepared.system_instruction_final,
                temperature=effective_temperature,
                max_output_tokens=max_output_tokens,
                json_mode=True,
                api_key=user_api_key,
            )
        else:
            stream_iter = openclaw_provider.generate_content_stream_sync(
                prompt_contents=[effective_json_string],
                model_name=prepared.model_to_use,
                system_instruction_text=effective_system_instruction,
                temperature=effective_temperature,
                max_output_tokens=max_output_tokens,
                json_mode=True,
                api_key=user_api_key,
                gateway_port=gateway_port,
                gateway_url=gateway_url,
                gateway_token=gateway_token,
            )
        for chunk in stream_iter:
            if not first_chunk_logged:
                t_first_chunk = time.perf_counter()
                logging_util.info(
                    "⏱️ STREAM_TIMING | llm_time_to_first_chunk: %.3fs | total_pre_stream: %.3fs",
                    t_first_chunk - t_llm_start,
                    t_first_chunk - t_prep_start,
                )
                first_chunk_logged = True

            # Log chunk with timestamp for evidence collection (BD-iwr)
            chunk_timestamp = datetime.now(UTC)
            chunk_logger.log_chunk(
                sequence=sequence,
                text=chunk,
                timestamp=chunk_timestamp,
            )

            full_text_parts.append(chunk)
            yield StreamEvent(
                type="chunk",
                payload={
                    "text": chunk,
                    "sequence": sequence,
                    "request_id": request_id,  # Include for correlation
                },
            )
            sequence += 1
            phase1_chunk_count += 1

        # === COMPLETION ===
        full_narrative = "".join(full_text_parts)

        # Try to parse the response as JSON for structured data
        structured_response = None
        narrative_text = full_narrative
        parse_strict_narrative = not is_god_mode_command

        def _parse_streamed_response(raw_response_text: str):
            return parse_structured_response(
                raw_response_text,
                requires_action_resolution=prepared.agent.requires_action_resolution,
                allow_legacy_planning_block=True,
                strict_narrative=parse_strict_narrative,
            )

        try:
            narrative_text, structured_response = _parse_streamed_response(
                full_narrative
            )
        except Exception:
            logging_util.warning(
                "Failed to parse streaming response as structured JSON, using raw text"
            )

        # Some streaming providers (e.g. OpenRouter with non-schema-support models) return
        # plain-text narrative or JSON missing the narrative field. In both cases
        # parse_structured_response yields the error-fallback marker or empty string.
        # When the raw accumulated text is a non-trivial story response, use it directly
        # as the narrative so users see story content instead of an error message.
        # Note: the [4214.03]-style numeric array artifacts only occur with
        # response_format=json_object in streaming, which is no longer sent for these models.
        _has_structured_god_mode_response = bool(
            structured_response
            and hasattr(structured_response, "god_mode_response")
            and isinstance(structured_response.god_mode_response, str)
            and structured_response.god_mode_response.strip()
        )
        _parse_returned_error = narrative_text == JSON_PARSE_FALLBACK_MARKER or (
            (not narrative_text or not narrative_text.strip())
            and not _has_structured_god_mode_response
        )
        _raw_narrative = (full_narrative or "").strip()
        _raw_looks_like_story = _classify_raw_narrative(_raw_narrative)
        _structured_has_tool_requests = bool(
            structured_response
            and hasattr(structured_response, "tool_requests")
            and structured_response.tool_requests
        )
        if (
            _parse_returned_error
            and _raw_looks_like_story
            and not _structured_has_tool_requests
        ):
            logging_util.warning(
                "Streaming JSON parse failed but raw text looks like narrative — "
                "using raw accumulated text as narrative fallback (provider=%s, model=%s, chars=%d)",
                prepared.provider_selection.provider,
                prepared.model_to_use,
                len(full_narrative),
            )
            narrative_text = full_narrative.strip()
            # Build minimal structured response so downstream fields (e.g. done payload
            # structured_response.narrative) are populated for client consumption.
            structured_response = NarrativeResponse(
                narrative=narrative_text,
                requires_action_resolution=prepared.agent.requires_action_resolution,
            )

        # Two-phase flow for tool_requests: execute tools server-side and stream final response.
        tool_requests = []
        if structured_response and hasattr(structured_response, "tool_requests"):
            tool_requests = structured_response.tool_requests or []
        tool_requests_executed = bool(tool_requests)

        if tool_requests:
            tool_results: list[dict[str, Any]] = []
            for req in tool_requests:
                tool_name = (
                    req.get("tool", "unknown") if isinstance(req, dict) else "unknown"
                )
                args = req.get("args", {}) if isinstance(req, dict) else {}
                yield StreamEvent(
                    type="tool_start",
                    payload={"tool_name": tool_name, "args": args},
                )

                single_results = (
                    execute_tool_requests([req]) if isinstance(req, dict) else []
                )
                for result in single_results:
                    tool_results.append(result)
                    yield StreamEvent(
                        type="tool_result",
                        payload={
                            "tool_name": result.get("tool", tool_name),
                            "result": result.get("result", {}),
                        },
                    )

            tool_results_text = format_tool_results_text(tool_results)
            tool_results_prompt = build_tool_results_prompt(tool_results_text)
            updated_prompt_contents = update_prompt_contents_with_tool_results(
                [effective_json_string],
                tool_results,
            )
            if prepared.provider_selection.provider == constants.LLM_PROVIDER_GEMINI:
                phase2_history = _build_gemini_two_phase_history(
                    prompt_contents=updated_prompt_contents,
                    phase1_text=full_narrative,
                    tool_results_prompt=tool_results_prompt,
                )
            else:
                phase2_history = [
                    {
                        "role": "user",
                        "content": stringify_chat_parts(updated_prompt_contents),
                    },
                    {"role": "assistant", "content": full_narrative},
                    {"role": "user", "content": tool_results_prompt},
                ]

            phase2_parts: list[str] = []
            yield StreamEvent(
                type="phase_transition",
                payload={
                    "phase": "post_tools",
                    "reset_text": True,
                },
            )
            phase2_system_instruction = prepared.system_instruction_final
            phase2_prompt_tokens, phase2_system_tokens = (
                _calculate_prompt_and_system_tokens(
                    user_prompt_contents=phase2_history,
                    system_instruction_text=phase2_system_instruction,
                    provider_name=prepared.provider_selection.provider,
                    model_name=prepared.model_to_use,
                )
            )
            phase2_max_output_tokens = _get_safe_output_token_limit(
                model_name=prepared.model_to_use,
                prompt_tokens=phase2_prompt_tokens,
                system_tokens=phase2_system_tokens,
            )
            if prepared.provider_selection.provider == constants.LLM_PROVIDER_GEMINI:
                if is_mock_mode and is_gemini_stream_callable_mock:
                    logging_util.info(
                        "MOCK_SERVICES_MODE: phase2 streaming path using mocked Gemini provider"
                    )
                    phase2_source = "mock_callable"
                    phase2_executed = True
                    phase2_stream_iter = gemini_provider.generate_content_stream_sync(
                        prompt_contents=phase2_history,
                        model_name=prepared.model_to_use,
                        system_instruction_text=phase2_system_instruction,
                        temperature=effective_temperature,
                        max_output_tokens=phase2_max_output_tokens,
                        json_mode=True,
                        api_key=user_api_key,
                        cache_name=None,  # Phase 2 has full history; dynamic system_instruction incompatible with cache
                    )
                elif is_mock_mode:
                    logging_util.info(
                        "MOCK_SERVICES_MODE: phase2 streaming path using local mock response "
                        "(is_god_mode_command=%s)",
                        is_god_mode_command,
                    )
                    phase2_source = "mock_local_fallback"
                    phase2_executed = True
                    phase2_stream_iter = iter(
                        [
                            _build_mock_streaming_text(
                                is_god_mode_command=is_god_mode_command
                            )
                        ]
                    )
                else:
                    phase2_source = "provider"
                    phase2_executed = True
                    phase2_stream_iter = gemini_provider.generate_content_stream_sync(
                        prompt_contents=phase2_history,
                        model_name=prepared.model_to_use,
                        system_instruction_text=phase2_system_instruction,
                        temperature=effective_temperature,
                        max_output_tokens=phase2_max_output_tokens,
                        json_mode=True,
                        api_key=user_api_key,
                        cache_name=None,  # Phase 2 has full history; dynamic system_instruction incompatible with cache
                    )
            elif (
                prepared.provider_selection.provider
                == constants.LLM_PROVIDER_OPENROUTER
            ):
                if is_mock_mode and is_openrouter_stream_callable_mock:
                    logging_util.info(
                        "MOCK_SERVICES_MODE: phase2 streaming path using mocked OpenRouter provider"
                    )
                    phase2_source = "mock_callable"
                    phase2_executed = True
                    phase2_stream_iter = (
                        openrouter_provider.generate_content_stream_sync(
                            prompt_contents=[],
                            messages=phase2_history,
                            model_name=prepared.model_to_use,
                            system_instruction_text=prepared.system_instruction_final,
                            temperature=effective_temperature,
                            max_output_tokens=phase2_max_output_tokens,
                            json_mode=True,
                            api_key=user_api_key,
                        )
                    )
                elif is_mock_mode:
                    logging_util.info(
                        "MOCK_SERVICES_MODE: phase2 streaming path using local mock response "
                        "(is_god_mode_command=%s)",
                        is_god_mode_command,
                    )
                    phase2_source = "mock_local_fallback"
                    phase2_executed = True
                    phase2_stream_iter = iter(
                        [
                            _build_mock_streaming_text(
                                is_god_mode_command=is_god_mode_command
                            )
                        ]
                    )
                else:
                    phase2_source = "provider"
                    phase2_executed = True
                    phase2_stream_iter = (
                        openrouter_provider.generate_content_stream_sync(
                            prompt_contents=[],
                            messages=phase2_history,
                            model_name=prepared.model_to_use,
                            system_instruction_text=prepared.system_instruction_final,
                            temperature=effective_temperature,
                            max_output_tokens=phase2_max_output_tokens,
                            json_mode=True,
                            api_key=user_api_key,
                        )
                    )
            elif (
                prepared.provider_selection.provider == constants.LLM_PROVIDER_OPENCLAW
            ):
                if is_mock_mode and is_openclaw_stream_callable_mock:
                    logging_util.info(
                        "MOCK_SERVICES_MODE: phase2 streaming path using mocked OpenClaw provider"
                    )
                    phase2_source = "mock_callable"
                    phase2_executed = True
                    phase2_stream_iter = openclaw_provider.generate_content_stream_sync(
                        prompt_contents=[],
                        messages=phase2_history,
                        model_name=prepared.model_to_use,
                        system_instruction_text=prepared.system_instruction_final,
                        temperature=effective_temperature,
                        max_output_tokens=phase2_max_output_tokens,
                        json_mode=True,
                        api_key=user_api_key,
                        gateway_port=gateway_port,
                        gateway_url=gateway_url,
                        gateway_token=gateway_token,
                    )
                elif is_mock_mode:
                    logging_util.info(
                        "MOCK_SERVICES_MODE: phase2 streaming path using local mock response "
                        "(is_god_mode_command=%s)",
                        is_god_mode_command,
                    )
                    phase2_source = "mock_local_fallback"
                    phase2_executed = True
                    phase2_stream_iter = iter(
                        [
                            _build_mock_streaming_text(
                                is_god_mode_command=is_god_mode_command
                            )
                        ]
                    )
                else:
                    phase2_source = "provider"
                    phase2_executed = True
                    phase2_stream_iter = openclaw_provider.generate_content_stream_sync(
                        prompt_contents=[],
                        messages=phase2_history,
                        model_name=prepared.model_to_use,
                        system_instruction_text=prepared.system_instruction_final,
                        temperature=effective_temperature,
                        max_output_tokens=phase2_max_output_tokens,
                        json_mode=True,
                        api_key=user_api_key,
                        gateway_port=gateway_port,
                        gateway_url=gateway_url,
                        gateway_token=gateway_token,
                    )
            else:
                raise ValueError(
                    f"Unsupported streaming provider in phase2: {prepared.provider_selection.provider}"
                )
            for chunk in phase2_stream_iter:
                phase2_parts.append(chunk)
                yield StreamEvent(
                    type="chunk",
                    payload={"text": chunk, "sequence": sequence},
                )
                sequence += 1
                phase2_chunk_count += 1

            full_narrative = "".join(phase2_parts)
            if not full_narrative or not full_narrative.strip():
                error_msg = "LLM returned empty response. This may indicate a model error or timeout."
                logging_util.error(f"🔴 STREAMING_EMPTY_RESPONSE: {error_msg}")
                logging_util.error(
                    f"   chunk_count={sequence}, raw_length={len(full_narrative)}"
                )
                yield StreamEvent(
                    type="error",
                    payload={
                        "message": error_msg,
                        "error_type": "empty_response",
                        "chunk_count": sequence,
                    },
                )
                return
            try:
                narrative_text, structured_response = _parse_streamed_response(
                    full_narrative,
                )
            except Exception:
                logging_util.warning(
                    "Failed to parse Phase 2 streaming response as structured JSON, using raw text"
                )
                narrative_text = full_narrative
                structured_response = None

            _phase2_has_structured_god_mode_response = bool(
                structured_response
                and hasattr(structured_response, "god_mode_response")
                and isinstance(structured_response.god_mode_response, str)
                and structured_response.god_mode_response.strip()
            )
            _phase2_parse_returned_error = (
                narrative_text == JSON_PARSE_FALLBACK_MARKER
                or (
                    (not narrative_text or not narrative_text.strip())
                    and not _phase2_has_structured_god_mode_response
                )
            )
            _phase2_raw_narrative = (full_narrative or "").strip()
            _phase2_raw_looks_like_story = _classify_raw_narrative(
                _phase2_raw_narrative
            )
            if _phase2_parse_returned_error and _phase2_raw_looks_like_story:
                logging_util.warning(
                    "Phase 2 streaming JSON parse failed but raw text looks like narrative — "
                    "using raw accumulated text as narrative fallback (provider=%s, model=%s, chars=%d)",
                    prepared.provider_selection.provider,
                    prepared.model_to_use,
                    len(full_narrative),
                )
                narrative_text = full_narrative.strip()
                structured_response = NarrativeResponse(
                    narrative=narrative_text,
                    requires_action_resolution=prepared.agent.requires_action_resolution,
                )

        capture_raw = os.getenv("CAPTURE_RAW_LLM", "true").lower() == "true"
        if capture_raw:
            _log_raw_llm_data(
                system_instruction_final=prepared.system_instruction_final,
                gemini_request=prepared.gemini_request,
                raw_response_text=full_narrative,
                raw_limit=_get_raw_limit(),
                provider_name=prepared.provider_selection.provider,
                model_name=prepared.model_to_use,
                api_response=None,
            )

        if structured_response is not None and hasattr(
            structured_response, "debug_info"
        ):
            debug_info = structured_response.debug_info or {}
            debug_info.setdefault("llm_provider", prepared.provider_selection.provider)
            debug_info.setdefault("llm_model", prepared.model_to_use)
            debug_info.setdefault("execution_path", "streaming")
            debug_info["agent_name"] = prepared.agent.__class__.__name__
            debug_info["intent_classifier"] = prepared.classifier_metadata
            debug_info["system_instruction_files"] = get_loaded_instruction_files()
            debug_info["system_instruction_char_count"] = len(
                prepared.system_instruction_final
            )
            if include_raw_llm_payloads:
                try:
                    debug_info["raw_request_payload"] = (
                        prepared.gemini_request.to_json()
                    )
                except Exception as e:
                    logging_util.warning(
                        f"RAW_REQUEST capture failed in streaming path: {e}"
                    )
                debug_info["raw_response_text"] = full_narrative
            structured_response.debug_info = debug_info

        state_updates = {}
        if (
            structured_response is not None
            and hasattr(structured_response, "state_updates")
            and isinstance(structured_response.state_updates, dict)
        ):
            state_updates = structured_response.state_updates
        if state_updates:
            yield StreamEvent(type="state", payload=state_updates)

        # BD-0eh: Include user_scene_number for streaming done event parity with non-streaming.
        # Scene number counts only AI (gemini) responses in the story context (+1 for this response).
        user_scene_number = (
            sum(
                1
                for entry in story_context
                if isinstance(entry, dict) and entry.get("actor") == "gemini"
            )
            + 1
        )

        structured_response_payload = None
        if structured_response is not None:
            if isinstance(structured_response, dict):
                structured_response_payload = structured_response
            elif hasattr(structured_response, "model_dump"):
                structured_response_payload = structured_response.model_dump()
            elif hasattr(structured_response, "to_dict"):
                structured_response_payload = structured_response.to_dict()

        # Validate narrative_text is not empty before yielding done event
        # Empty responses cause frontend error: "Error: Empty response from server"
        # EXCEPTION: God mode responses have empty narrative but populate god_mode_response field
        has_god_mode_response = False
        god_mode_display_text = ""
        if structured_response is not None:
            if isinstance(structured_response, dict):
                raw_god_mode = structured_response.get("god_mode_response")
                if isinstance(raw_god_mode, str) and raw_god_mode.strip():
                    has_god_mode_response = True
                    god_mode_display_text = raw_god_mode
            elif hasattr(structured_response, "god_mode_response"):
                raw_god_mode = structured_response.god_mode_response
                if isinstance(raw_god_mode, str) and raw_god_mode.strip():
                    has_god_mode_response = True
                    god_mode_display_text = raw_god_mode
        if (
            not narrative_text or not narrative_text.strip()
        ) and not has_god_mode_response:
            error_msg = "LLM returned empty response. This may indicate a model error or timeout."
            logging_util.error(f"🔴 STREAMING_EMPTY_RESPONSE: {error_msg}")
            logging_util.error(
                f"   chunk_count={sequence}, raw_length={len(full_narrative)}"
            )
            yield StreamEvent(
                type="error",
                payload={
                    "message": error_msg,
                    "error_type": "empty_response",
                    "chunk_count": sequence,
                },
            )
            return

        # Finalize and save chunk logger (BD-iwr evidence standard)
        llm_log_path = finalize_chunk_logger(request_id)
        if llm_log_path:
            logging_util.info(
                f"📁 STREAMING_EVIDENCE | LLM chunk log saved | "
                f"path={llm_log_path} campaign_id={campaign_id}"
            )

        display_text = (
            narrative_text
            if isinstance(narrative_text, str) and narrative_text.strip()
            else god_mode_display_text
        )
        signing_secret = os.getenv("STREAM_RESPONSE_SIGNING_SECRET", "").strip() or None
        execution_trace = {
            "execution_path": "streaming",
            "provider": prepared.provider_selection.provider,
            "model": prepared.model_to_use,
            "tool_requests": {
                "executed": tool_requests_executed,
                "count": len(tool_requests),
            },
            "cache": {
                "explicit_cache_enabled": constants.EXPLICIT_CACHE_ENABLED,
                "requested": stream_cache_requested,
                "cache_name": stream_cache_name,
                "source": stream_cache_source,
            },
            "phase1": {
                "source": phase1_source,
                "provider": prepared.provider_selection.provider,
                "chunks": phase1_chunk_count,
            },
            "phase2": {
                "executed": phase2_executed,
                "source": phase2_source,
                "provider": prepared.provider_selection.provider
                if phase2_executed
                else "",
                "chunks": phase2_chunk_count,
            },
        }
        response_signature = _build_streaming_response_signature(
            request_id=request_id,
            response_text=full_narrative,
            execution_trace=execution_trace,
            signing_secret=signing_secret,
        )
        logging_util.info(
            "📦 STREAM_CACHE_USAGE: campaign=%s, cache_name=%s, source=%s, requested=%s",
            campaign_id,
            stream_cache_name,
            stream_cache_source,
            stream_cache_requested,
        )

        yield StreamEvent(
            type="done",
            payload={
                "execution_path": "streaming",
                "full_narrative": narrative_text,
                "display_text": display_text,
                "raw_response_text": full_narrative,
                "chunk_count": sequence,
                "agent_used": prepared.agent.__class__.__name__,
                "agent_mode": prepared.agent.MODE,
                "model_used": prepared.model_to_use,
                "provider_used": prepared.provider_selection.provider,
                "has_structured_response": structured_response is not None,
                "state_updates": state_updates,
                "structured_response": structured_response_payload,
                "user_scene_number": user_scene_number,
                "request_id": request_id,  # Include for client correlation
                "mock_services_mode": is_mock_mode,
                "test_mode": (
                    os.getenv("MCP_TEST_MODE", os.getenv("TEST_MODE", ""))
                    .strip()
                    .lower()
                    or None
                ),
                "streaming_execution_trace": execution_trace,
                "streaming_cache": execution_trace.get("cache"),
                "streaming_response_signature": response_signature,
                "stream_start_time": stream_start_time,
                "e2e_latency_seconds": time.perf_counter() - t_llm_start,
            },
        )

    except PayloadTooLargeError as e:
        logging_util.error(f"Streaming payload too large: {e}")
        yield StreamEvent(
            type="error",
            payload={
                "message": "The story context is too large. Please start a new chapter.",
                "error_type": "payload_too_large",
            },
        )

    except Exception:
        logging_util.exception("Error in continue_story_streaming")
        yield StreamEvent(
            type="error",
            payload={
                "message": "An unexpected error occurred while streaming the response.",
                "partial_text": "".join(full_text_parts) if full_text_parts else None,
            },
        )

    finally:
        # Ensure chunk logger is always cleaned up to prevent memory leaks.
        # finalize_chunk_logger is idempotent (no-op if already finalized).
        if request_id is not None:
            finalize_chunk_logger(request_id)


def _extract_multiple_think_commands(user_input: str) -> list[str]:
    """
    Extract multiple 'Main Character: think' commands from user input.

    Returns:
        list: List of individual think commands, or [user_input] if no multiple commands found
    """
    # Pattern to match "Main Character: think..." commands
    think_pattern = r"Main Character:\s*think[^\n]*"
    matches = re.findall(think_pattern, user_input, re.IGNORECASE)

    if len(matches) > 1:
        return matches
    # No multiple commands found, return original input
    return [user_input]


def _validate_companion_generation(gemini_response: LLMResponse) -> None:
    """Validate companion generation results.

    Moved from world_logic.py to maintain Single Responsibility Principle.
    Companion validation should be near companion generation logic.

    Args:
        gemini_response: The response from Gemini to validate
    """
    structured_response = getattr(gemini_response, "structured_response", None)
    if not structured_response:
        logging_util.error(
            "🎭 COMPANION GENERATION: ❌ No structured response received from Gemini!"
        )
        return

    # Access companions and npc_data from extra_fields (since they're not standard schema fields)
    extra_fields = getattr(structured_response, "extra_fields", {})
    companions = extra_fields.get("companions", {})
    npc_data = extra_fields.get("npc_data", {})

    # Also check state_updates in case they're there
    state_updates = getattr(structured_response, "state_updates", {}) or {}
    if not npc_data and "npc_data" in state_updates:
        npc_data = state_updates["npc_data"]
    if not companions and "companions" in state_updates:
        companions = state_updates["companions"]

    # Type safety check and deduplication
    if not isinstance(companions, dict):
        companions = {}
    if not isinstance(npc_data, dict):
        npc_data = {}

    # Count unique companions (avoiding double-counting)
    companion_names = set(companions.keys())
    allied_npcs = {
        name
        for name, data in npc_data.items()
        if isinstance(data, dict) and data.get("relationship") in ["companion", "ally"]
    }
    # Remove any companions already counted to avoid double-counting
    unique_allied_npcs = allied_npcs - companion_names

    companion_count = len(companion_names)
    allied_npc_count = len(unique_allied_npcs)
    total_companions = companion_count + allied_npc_count

    # Minimal logging for companion validation
    if total_companions == 0:
        logging_util.warning("🎭 No companions generated despite request")
    elif total_companions < EXPECTED_COMPANION_COUNT:
        logging_util.warning(
            f"🎭 Only {total_companions}/{EXPECTED_COMPANION_COUNT} companions generated"
        )
    else:
        logging_util.info(f"🎭 {total_companions} companions generated successfully")


# --- Main block for rapid, direct testing ---
if __name__ == "__main__":
    print("--- Running llm_service.py in chained conversation test mode ---")

    try:
        # Look for Google API key in home directory first, then project root
        home_key_path = os.path.expanduser("~/.gemini_api_key.txt")
        project_key_path = "gemini_api_key.txt"

        if os.path.exists(home_key_path):
            api_key = read_file_cached(home_key_path).strip()
            print(f"Successfully loaded API key from {home_key_path}")
        elif os.path.exists(project_key_path):
            api_key = read_file_cached(project_key_path).strip()
            print(f"Successfully loaded API key from {project_key_path}")
        else:
            print(
                "\nERROR: API key not found in ~/.gemini_api_key.txt or gemini_api_key.txt"
            )
            sys.exit(1)

        os.environ["GEMINI_API_KEY"] = api_key
    except Exception as e:
        print(f"\nERROR: Failed to load API key: {e}")
        sys.exit(1)

    get_client()  # Initialize client

    # Example usage for testing: pass all prompt types
    test_selected_prompts = ["narrative", "mechanics", "calibration"]
    test_game_state = GameState(
        player_character_data={"name": "Test Character", "hp_current": 10},
        world_data={"current_location_name": "The Testing Grounds"},
        npc_data={},
        custom_campaign_state={},
    )

    # --- Turn 1: Initial Story ---
    print("\n--- Turn 1: get_initial_story ---")
    turn_1_prompt = "start a story about a haunted lighthouse"
    print(
        f"Using prompt: '{turn_1_prompt}' with selected prompts: {test_selected_prompts}"
    )
    turn_1_response = get_initial_story(
        turn_1_prompt, selected_prompts=test_selected_prompts
    )
    print("\n--- LIVE RESPONSE 1 ---")
    print(turn_1_response)
    print("--- END OF RESPONSE 1 ---\n")

    # Create the initial history from the real response
    history = [
        {"actor": "user", "text": turn_1_prompt},
        {"actor": "gemini", "text": turn_1_response},
    ]

    # --- Turn 2: Continue Story ---
    print("\n--- Turn 2: continue_story ---")
    turn_2_prompt = "A lone ship, tossed by the raging sea, sees a faint, flickering light from the abandoned tower."
    print(f"Using prompt: '{turn_2_prompt}'")
    turn_2_response = continue_story(
        turn_2_prompt,
        "god",
        history,
        test_game_state,
        selected_prompts=test_selected_prompts,
    )
    print("\n--- LIVE RESPONSE 2 ---")
    print(turn_2_response)
    print("--- END OF RESPONSE 2 ---\n")

    # Update the history with the real response from turn 2
    history.append({"actor": "user", "text": turn_2_prompt})
    history.append({"actor": "gemini", "text": turn_2_response})

    # --- Turn 3: Continue Story Again ---
    print("\n--- Turn 3: continue_story ---")
    turn_3_prompt = "The ship's captain, a grizzled old sailor named Silas, decides to steer towards the light, ignoring the warnings of his crew."
    print(f"Using prompt: '{turn_3_prompt}'")
    turn_3_response = continue_story(
        turn_3_prompt,
        "god",
        history,
        test_game_state,
        selected_prompts=test_selected_prompts,
    )
    print("\n--- LIVE RESPONSE 3 ---")
    print(turn_3_response)
    print("--- END OF RESPONSE 3 ---\n")

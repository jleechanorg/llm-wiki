"""
Prompt building utilities for agent-based system instructions.

This module centralizes ALL prompt manipulation code for the application:
- System instruction loading and caching
- Continuation prompt building
- Temporal correction prompts
- Static prompt parts generation
- Current turn prompt formatting

llm_service and world_logic delegate prompt construction here,
focusing on request/response orchestration instead.
"""

from __future__ import annotations

import json
import os
import re
import time
from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

from mvp_site import campaign_divine, constants, dice_strategy, logging_util
from mvp_site.file_cache import read_file_cached
from mvp_site.game_state import GameState
from mvp_site.memory_utils import format_memories_for_prompt, select_memories_by_budget
from mvp_site.narrative_response_schema import (
    CHOICE_SCHEMA,
    PLANNING_BLOCK_SCHEMA,
    VALID_CONFIDENCE_LEVELS,
    VALID_QUALITY_TIERS,
    VALID_RISK_LEVELS,
)
from mvp_site.schemas.prompt_generator import (
    get_schema_fields_instructions,
    get_schema_instructions,
)
from mvp_site.schemas.validation import load_schema
from mvp_site.world_loader import load_world_content_for_system_instruction
from mvp_site.world_time import format_world_time_for_prompt

if TYPE_CHECKING:
    from mvp_site.agents import BaseAgent


@runtime_checkable
class AgentProtocol(Protocol):
    def prompt_order(self) -> tuple[str, ...]: ...

    def builder_flags(self) -> dict[str, Any]: ...


# Word count target for standard story continuations
TARGET_WORD_COUNT: int = 300

# Schema documentation cache (populated at module import time)
# Key: schema type name, Value: markdown documentation string
_SCHEMA_DOC_CACHE: dict[str, str] = {}
_FULL_CANONICAL_GAME_STATE_SCHEMA_JSON: str | None = None

# Feature flag for stripping comment-only content from prompt files
# Set ENABLE_PROMPT_COMMENT_STRIPPING=false to disable (default: enabled)
_ENABLE_PROMPT_COMMENT_STRIPPING: bool | None = None


def _is_comment_stripping_enabled() -> bool:
    """Check if prompt comment stripping is enabled via feature flag.

    Cached after first check to avoid repeated env var lookups.
    """
    global _ENABLE_PROMPT_COMMENT_STRIPPING  # noqa: PLW0603
    if _ENABLE_PROMPT_COMMENT_STRIPPING is None:
        _ENABLE_PROMPT_COMMENT_STRIPPING = os.environ.get(
            "ENABLE_PROMPT_COMMENT_STRIPPING", "true"
        ).lower() != "false"
    return _ENABLE_PROMPT_COMMENT_STRIPPING

# NEW: Centralized map of prompt types to their file paths.
# This is now the single source of truth for locating prompt files.
PATH_MAP: dict[str, str] = {
    constants.PROMPT_TYPE_NARRATIVE: constants.NARRATIVE_SYSTEM_INSTRUCTION_PATH,
    constants.PROMPT_TYPE_MECHANICS: constants.MECHANICS_SYSTEM_INSTRUCTION_PATH,
    constants.PROMPT_TYPE_DICE: constants.DICE_SYSTEM_INSTRUCTION_PATH,
    constants.PROMPT_TYPE_DICE_CODE_EXECUTION: (
        constants.DICE_SYSTEM_INSTRUCTION_CODE_EXECUTION_PATH
    ),
    constants.PROMPT_TYPE_GAME_STATE: constants.GAME_STATE_INSTRUCTION_PATH,
    constants.PROMPT_TYPE_GAME_STATE_EXAMPLES: constants.GAME_STATE_EXAMPLES_PATH,
    constants.PROMPT_TYPE_CHARACTER_TEMPLATE: constants.CHARACTER_TEMPLATE_PATH,
    constants.PROMPT_TYPE_MASTER_DIRECTIVE: constants.MASTER_DIRECTIVE_PATH,
    constants.PROMPT_TYPE_DND_SRD: constants.DND_SRD_INSTRUCTION_PATH,
    constants.PROMPT_TYPE_GOD_MODE: constants.GOD_MODE_INSTRUCTION_PATH,
    constants.PROMPT_TYPE_LIVING_WORLD: constants.LIVING_WORLD_INSTRUCTION_PATH,
    constants.PROMPT_TYPE_COMBAT: constants.COMBAT_SYSTEM_INSTRUCTION_PATH,
    constants.PROMPT_TYPE_REWARDS: constants.REWARDS_SYSTEM_INSTRUCTION_PATH,
    constants.PROMPT_TYPE_FACTION_MANAGEMENT: constants.FACTION_MANAGEMENT_INSTRUCTION_PATH,
    constants.PROMPT_TYPE_FACTION_MINIGAME: constants.FACTION_MINIGAME_INSTRUCTION_PATH,
    constants.PROMPT_TYPE_RELATIONSHIP: constants.RELATIONSHIP_INSTRUCTION_PATH,
    constants.PROMPT_TYPE_REPUTATION: constants.REPUTATION_INSTRUCTION_PATH,
    constants.PROMPT_TYPE_CHARACTER_CREATION: constants.CHARACTER_CREATION_INSTRUCTION_PATH,
    constants.PROMPT_TYPE_LEVEL_UP: constants.LEVEL_UP_INSTRUCTION_PATH,
    constants.PROMPT_TYPE_THINK: constants.THINK_MODE_INSTRUCTION_PATH,
    constants.PROMPT_TYPE_PLANNING_PROTOCOL: constants.PLANNING_PROTOCOL_PATH,
    constants.PROMPT_TYPE_DEFERRED_REWARDS: constants.DEFERRED_REWARDS_INSTRUCTION_PATH,
    constants.PROMPT_TYPE_DIALOG: constants.DIALOG_SYSTEM_INSTRUCTION_PATH,
    constants.PROMPT_TYPE_NARRATIVE_LITE: constants.NARRATIVE_LITE_SYSTEM_INSTRUCTION_PATH,
    constants.PROMPT_TYPE_SPICY_MODE: constants.SPICY_MODE_INSTRUCTION_PATH,
    # Divine Leverage (god tier) prompts
    constants.PROMPT_TYPE_DIVINE_ASCENSION: constants.DIVINE_ASCENSION_PATH,
    constants.PROMPT_TYPE_DIVINE_SYSTEM: constants.DIVINE_SYSTEM_PATH,
    # Sovereign Protocol (multiverse tier) prompts
    constants.PROMPT_TYPE_SOVEREIGN_ASCENSION: constants.SOVEREIGN_ASCENSION_PATH,
    constants.PROMPT_TYPE_SOVEREIGN_SYSTEM: constants.SOVEREIGN_SYSTEM_PATH,
}

# Store loaded instruction content in a dictionary for easy access
_loaded_instructions_cache: dict[str, str] = {}

# Store pre-stripping essentials content for essentials-only (token-constrained) mode.
# Must be populated before comment stripping so _extract_essentials still works.
_essentials_raw_cache: dict[str, str] = {}

# Track which instruction files were loaded in the current request (for evidence)
_current_request_loaded_files: list[str] = []


def clear_loaded_files_tracking() -> None:
    """Clear the loaded files tracking list. Call at start of each request."""
    global _current_request_loaded_files  # noqa: PLW0603
    _current_request_loaded_files = []


def get_loaded_instruction_files() -> list[str]:
    """Get the list of instruction files loaded in the current request."""
    return _current_request_loaded_files.copy()


def init_schema_doc_cache() -> dict[str, float]:
    """
    Pre-generate and cache schema documentation at server startup.

    Generates markdown docs for commonly used schema types and caches them
    in memory to avoid regenerating on every prompt load.

    Returns:
        dict[str, float]: Timing metrics (type_name -> generation_time_ms)
    """
    global _SCHEMA_DOC_CACHE  # noqa: PLW0603

    # Schema types to pre-generate (commonly used in prompts)
    schema_types = [
        "CombatantState",
        "CombatState",
        "EntityType",
        "CampaignTier",
        "Character",
        "NPC",
        "PlayerCharacter",
        "HealthStatus",
        "EntityStatus",
        "PlanningBlock",
        "SocialHPChallenge",
    ]

    timing_metrics = {}
    total_start = time.perf_counter()

    for type_name in schema_types:
        try:
            start = time.perf_counter()
            doc = get_schema_instructions(type_name, "game_state")
            end = time.perf_counter()

            _SCHEMA_DOC_CACHE[type_name] = doc
            timing_metrics[type_name] = (end - start) * 1000  # Convert to ms

        except (ValueError, KeyError) as e:
            logging_util.warning(
                f"Failed to generate schema doc for {type_name}: {e}"
            )
            timing_metrics[type_name] = 0.0

    total_end = time.perf_counter()
    total_time_ms = (total_end - total_start) * 1000

    logging_util.info(
        f"Schema doc cache initialized: {len(_SCHEMA_DOC_CACHE)} types, "
        f"{total_time_ms:.2f}ms total"
    )

    timing_metrics["__total__"] = total_time_ms
    return timing_metrics


def get_cached_schema_doc(type_name: str) -> str | None:
    """
    Get cached schema documentation for a type.

    Args:
        type_name: Name of the schema type (e.g., "CombatantState")

    Returns:
        Markdown documentation string, or None if not cached
    """
    return _SCHEMA_DOC_CACHE.get(type_name)


def _schema_to_json_string(schema: dict) -> str:
    """
    Convert a schema dict with Python types to a JSON-friendly string representation.

    The schema uses Python types (str, int, list, dict) as placeholders.
    This converts them to human-readable type names for prompts.
    """

    def convert_value(v: Any) -> Any:  # noqa: PLR0911
        if v is str:
            return "string"
        if v is int:
            return "integer"
        if v is bool:
            return "boolean"
        if v is float:
            return "number"
        if v is list:
            return "array"
        if v is dict:
            return "object"
        if isinstance(v, dict):
            return {k: convert_value(vv) for k, vv in v.items()}
        if isinstance(v, list):
            return [convert_value(item) for item in v]
        return v

    converted = convert_value(schema)
    return json.dumps(converted, indent=2)


# Cache for generated state examples
_STATE_EXAMPLE_CACHE: dict[str, str] = {}


def generate_state_example(type_name: str) -> str:
    """
    Generate example JSON from game_state.schema.json for a given type.

    This enables runtime injection of schema-consistent examples into prompts,
    preventing prompt-schema drift.

    Args:
        type_name: Name of the schema type (e.g., 'CombatState', 'CustomCampaignState')

    Returns:
        JSON string with example values, or error message if not found
    """
    if type_name in _STATE_EXAMPLE_CACHE:
        return _STATE_EXAMPLE_CACHE[type_name]

    schema = load_schema("game_state")
    definitions = schema.get("$defs", {})

    if type_name not in definitions:
        return f'{{"error": "Type {type_name} not found in schema"}}'

    type_def = definitions[type_name]
    example = _generate_example_from_def(type_def, definitions)
    result = json.dumps(example, indent=2)

    _STATE_EXAMPLE_CACHE[type_name] = result
    return result


def _generate_example_from_def(
    type_def: dict, definitions: dict, depth: int = 0
) -> Any:
    """Recursively generate example values from a schema definition."""
    if depth > 5:  # Prevent infinite recursion
        return "<recursive>"

    if not isinstance(type_def, dict):
        return None

    # Prefer explicit fixed/example-like values first.
    if "const" in type_def:
        return type_def["const"]
    if "enum" in type_def and isinstance(type_def["enum"], list) and type_def["enum"]:
        return type_def["enum"][0]

    # Handle $ref
    if "$ref" in type_def:
        ref_name = type_def["$ref"].split("/")[-1]
        if ref_name in definitions:
            return _generate_example_from_def(definitions[ref_name], definitions, depth + 1)
        return None

    # Handle oneOf/anyOf - take first valid option
    if "oneOf" in type_def:
        for option in type_def["oneOf"]:
            generated = _generate_example_from_def(option, definitions, depth + 1)
            if generated is not None:
                return generated
        return None
    if "anyOf" in type_def:
        for option in type_def["anyOf"]:
            generated = _generate_example_from_def(option, definitions, depth + 1)
            if generated is not None:
                return generated
        return None

    # Handle allOf - merge all options (typically $ref + inline properties)
    if "allOf" in type_def:
        result = None
        for option in type_def["allOf"]:
            generated = _generate_example_from_def(option, definitions, depth + 1)
            if generated is not None:
                # For first valid result, use it as base
                if result is None:
                    result = generated
                # For subsequent results, merge if both are dicts
                elif isinstance(result, dict) and isinstance(generated, dict):
                    result = {**result, **generated}
                # Otherwise prefer non-empty result
                elif generated:
                    result = generated
        return result

    # Handle type
    schema_type = type_def.get("type")
    if isinstance(schema_type, list):
        # Common pattern: nullable union, e.g. ["object", "null"].
        non_null_types = [t for t in schema_type if t != "null"]
        if non_null_types:
            schema_type = non_null_types[0]
        elif schema_type:
            schema_type = schema_type[0]

    if schema_type == "object":
        result = {}
        properties = type_def.get("properties", {})
        for prop_name, prop_def in properties.items():
            result[prop_name] = _generate_example_from_def(prop_def, definitions, depth + 1)
        return result
    if schema_type == "array":
        items = type_def.get("items")
        if items:
            return [_generate_example_from_def(items, definitions, depth + 1)]
        return []
    if schema_type == "string":
        return "<string>"
    if schema_type == "integer" or schema_type == "number":
        return 0
    if schema_type == "boolean":
        return False

    return None


def _inject_schema_placeholders(content: str) -> str:
    """
    Inject canonical schema definitions into prompt content.

    Replaces placeholders with actual schema JSON from narrative_response_schema.py.
    This ensures prompts and validation code use the same schema definitions.

    Supported placeholders:
    - {{PLANNING_BLOCK_SCHEMA}} - Full planning block structure
    - {{CHOICE_SCHEMA}} - Choice structure within planning blocks
    - {{VALID_RISK_LEVELS}} - Valid risk level values
    - {{VALID_CONFIDENCE_LEVELS}} - Valid confidence level values
    - {{VALID_QUALITY_TIERS}} - Valid quality tier values
    """
    if "{{" not in content:
        return content

    # Build schema JSON representations (convert Python types to strings)
    replacements = {
        "{{PLANNING_BLOCK_SCHEMA}}": _schema_to_json_string(PLANNING_BLOCK_SCHEMA),
        "{{CHOICE_SCHEMA}}": _schema_to_json_string(CHOICE_SCHEMA),
        "{{VALID_RISK_LEVELS}}": json.dumps(sorted(VALID_RISK_LEVELS)),
        "{{VALID_CONFIDENCE_LEVELS}}": json.dumps(sorted(VALID_CONFIDENCE_LEVELS)),
        "{{VALID_QUALITY_TIERS}}": json.dumps(sorted(VALID_QUALITY_TIERS)),
    }
    if "{{FULL_CANONICAL_GAME_STATE_SCHEMA}}" in content:
        global _FULL_CANONICAL_GAME_STATE_SCHEMA_JSON  # noqa: PLW0603
        if _FULL_CANONICAL_GAME_STATE_SCHEMA_JSON is None:
            full_schema = load_schema("game_state")
            # Keep minified to reduce token overhead while sending full canonical schema.
            _FULL_CANONICAL_GAME_STATE_SCHEMA_JSON = json.dumps(
                full_schema, separators=(",", ":")
            )
        replacements["{{FULL_CANONICAL_GAME_STATE_SCHEMA}}"] = (
            _FULL_CANONICAL_GAME_STATE_SCHEMA_JSON
        )

    # Inject STATE_EXAMPLE:TypeName placeholders (e.g., {{STATE_EXAMPLE:CombatState}})
    # This generates example JSON from the schema at runtime, preventing prompt-schema drift
    if "{{STATE_EXAMPLE:" in content:
        pattern = r"\{\{STATE_EXAMPLE:([A-Za-z0-9_]+)\}\}"
        matches = re.findall(pattern, content)
        for type_name in matches:
            placeholder = f"{{{{STATE_EXAMPLE:{type_name}}}}}"
            example_json = generate_state_example(type_name)
            content = content.replace(placeholder, example_json)
            logging_util.debug(f"Injected {placeholder} into prompt")

    for placeholder, value in replacements.items():
        if placeholder in content:
            content = content.replace(placeholder, value)
            logging_util.debug(f"Injected {placeholder} into prompt")

    return content


def _inject_dynamic_schema_docs(
    content: str,
    *,
    raise_on_unresolved: bool = False,
) -> str:
    """
    Injects dynamic schema documentation into the prompt.
    Looks for {{SCHEMA:TypeName}} placeholders and replaces them with cached
    schema docs generated at server startup.

    Supported patterns:
    - {{SCHEMA:TypeName}} - Full schema docs for TypeName (e.g., CombatantState)
    - {{SCHEMA_FIELDS:TypeName:field_a,field_b}} - Selected field docs for TypeName
    - Falls back to on-demand generation if not in cache

    Performance: Uses pre-generated cache (<1ms per replacement). Unknown types can
    be left as explicit unresolved markers unless raise_on_unresolved=True.
    """
    if "{{" not in content:
        return content

    field_matches = re.findall(
        r"\{\{SCHEMA_FIELDS:([A-Za-z0-9_]+):([\w,\s]+?)\}\}", content
    )
    for type_name, field_csv in field_matches:
        placeholder = f"{{{{SCHEMA_FIELDS:{type_name}:{field_csv}}}}}"
        field_names = [field.strip() for field in field_csv.split(",") if field.strip()]
        try:
            replacement = get_schema_fields_instructions(type_name, field_names)
        except (ValueError, KeyError) as exc:
            logging_util.error(
                f"Failed to inject schema field docs for {type_name} ({field_csv}): {exc}"
            )
            if raise_on_unresolved:
                raise
            replacement = f"[UNRESOLVED_SCHEMA_FIELDS:{type_name}:{field_csv}]"

        content = content.replace(placeholder, replacement)
        logging_util.debug(f"Injected schema field docs for {type_name}: {field_csv}")

    # Find all {{SCHEMA:TypeName}} patterns
    matches = re.findall(r"\{\{SCHEMA:([A-Za-z0-9_]+)\}\}", content)
    for type_name in matches:
        placeholder = f"{{{{SCHEMA:{type_name}}}}}"
        replacement: str | None = None

        # Try cached docs first (fast path)
        docs = get_cached_schema_doc(type_name)

        # Fall back to on-demand generation if not cached
        if docs is None:
            try:
                docs = get_schema_instructions(type_name, "game_state")
                _SCHEMA_DOC_CACHE[type_name] = docs
                replacement = docs
                logging_util.warning(
                    f"Schema docs for {type_name} not in cache, generated on-demand"
                )
            except (ValueError, KeyError) as exc:
                logging_util.error(
                    f"Failed to inject schema docs for {type_name}: {exc}"
                )
                if raise_on_unresolved:
                    raise

                replacement = f"[UNRESOLVED_SCHEMA:{type_name}]"
        else:
            replacement = docs

        content = content.replace(placeholder, replacement)
        logging_util.debug(f"Injected schema docs for {type_name}")

    # Verify no unresolved placeholders remain
    remaining = re.findall(r"\{\{SCHEMA:([A-Za-z0-9_]+)\}\}", content)
    if remaining:
        msg = f"Unresolved schema placeholders remain in prompt: {', '.join(remaining)}"
        logging_util.error(msg)
        if raise_on_unresolved:
            raise ValueError(msg)
        content = re.sub(
            r"\{\{SCHEMA:([A-Za-z0-9_]+)\}\}",
            lambda match: f"[UNRESOLVED_SCHEMA:{match.group(1)}]",
            content,
        )

    remaining_field_placeholders = re.findall(
        r"\{\{SCHEMA_FIELDS:([A-Za-z0-9_]+):([\w,\s]+?)\}\}", content
    )
    if remaining_field_placeholders:
        names = [
            f"{type_name}:{field_csv}"
            for type_name, field_csv in remaining_field_placeholders
        ]
        msg = "Unresolved schema field placeholders remain in prompt: " + ", ".join(names)
        logging_util.error(msg)
        if raise_on_unresolved:
            raise ValueError(msg)
        content = re.sub(
            r"\{\{SCHEMA_FIELDS:([A-Za-z0-9_]+):([\w,\s]+?)\}\}",
            lambda match: (
                "[UNRESOLVED_SCHEMA_FIELDS:"
                f"{match.group(1)}:{match.group(2)}]"
            ),
            content,
        )

    return content


# Patterns that must be actively stripped from prompt files before sending to the LLM.
# These are developer-documentation blocks that serve as source-file annotations only.
_STRIP_BLOCK_PATTERNS = [
    # ESSENTIALS block: developer summary for token-constrained mode, not for the LLM.
    # The inner content is cached to _essentials_raw_cache before stripping so
    # essentials-only (token-constrained) mode still works correctly.
    r"<!--\s*ESSENTIALS[^\n]*\n.*?\n\s*/ESSENTIALS\s*-->",
    # AUTO-GENERATED markers: schema-generation annotation comments only.
    r"<!--\s*/?AUTO-GENERATED[^>]*-->",
]


def _strip_prompt_comments(content: str) -> str:
    """
    Strip HTML comment-only content from prompt files.

    Actively strips developer-documentation blocks (_STRIP_BLOCK_PATTERNS) and
    empty/whitespace-only comments. Leaves content-bearing comments that are not
    in the strip-list intact.

    This is applied AFTER schema injection to ensure placeholders ({{...}}) are
    replaced before we analyze comment content.

    Supported comment syntaxes:
    - Standard HTML comments: <!-- comment -->
    - Multi-line comments: <!-- multi\nline comment -->

    Stripped:
    - <!-- ESSENTIALS ... /ESSENTIALS --> - Developer summary blocks (not LLM instructions)
    - <!-- AUTO-GENERATED ... -->         - Schema generation markers
    - Empty/whitespace-only comments

    Handles:
    - Malformed comments (unclosed) - preserved as-is
    - Empty/whitespace-only comments - stripped
    """
    if "<!--" not in content:
        return content

    # First, actively strip known developer-doc block patterns
    stripped_content = content
    for pattern in _STRIP_BLOCK_PATTERNS:
        stripped_content = re.sub(pattern, "", stripped_content, flags=re.DOTALL)

    # Now strip remaining HTML comments that are empty or whitespace-only
    def strip_empty_comments(match: re.Match) -> str:
        inner = match.group(1)
        if not inner or inner.strip() == "":
            return ""
        return match.group(0)

    stripped_content = re.sub(
        r"<!--\s*(.*?)\s*-->",
        strip_empty_comments,
        stripped_content,
        flags=re.DOTALL,
    )

    # Clean up any resulting double newlines from removed comments
    stripped_content = re.sub(r"\n\n\n+", "\n\n", stripped_content)

    return stripped_content


def _load_instruction_file(instruction_type: str) -> str:
    """
    Loads a prompt instruction file from the 'prompts' directory.
    This function is now strict: it will raise an exception if a file
    cannot be found, ensuring the application does not continue with
    incomplete instructions.

    Adds a filename header so the LLM can identify which content came from
    which file when prompts reference filenames (e.g., "see game_state_instruction.md").
    """
    if instruction_type not in _loaded_instructions_cache:
        relative_path = PATH_MAP.get(instruction_type)

        if not relative_path:
            logging_util.error(
                f"FATAL: Unknown instruction type requested: {instruction_type}"
            )
            raise ValueError(f"Unknown instruction type requested: {instruction_type}")

        file_path = os.path.join(os.path.dirname(__file__), relative_path)

        try:
            content = read_file_cached(file_path).strip()
            # Apply schema injection to replace placeholders with canonical schemas
            content = _inject_schema_placeholders(content)
            # Apply dynamic schema documentation injection
            content = _inject_dynamic_schema_docs(content)
            # Cache essentials BEFORE stripping so token-constrained mode still works
            # after the ESSENTIALS comment block is stripped from the live instruction.
            _essentials_raw_cache[instruction_type] = _extract_essentials(content)
            # Strip developer-doc blocks and empty HTML comments (feature-gated)
            if _is_comment_stripping_enabled():
                content = _strip_prompt_comments(content)

            # Extract filename from relative_path (e.g., "prompts/game_state_instruction.md" -> "game_state_instruction.md")
            filename = os.path.basename(relative_path)

            # Add filename header so LLM can identify which file this content came from
            # This allows cross-references like "see game_state_instruction.md" to work
            content_with_header = f"# File: {filename}\n\n{content}"

            _loaded_instructions_cache[instruction_type] = content_with_header
        except FileNotFoundError:
            logging_util.error(
                f"CRITICAL: System instruction file not found: {file_path}. This is a fatal error for this request."
            )
            raise
        except Exception as e:
            logging_util.error(
                f"CRITICAL: Error loading system instruction file {file_path}: {e}"
            )
            raise

    # Track which files are loaded for evidence (only add if not already tracked)
    relative_path = PATH_MAP.get(instruction_type)
    if relative_path and relative_path not in _current_request_loaded_files:
        _current_request_loaded_files.append(relative_path)

    return _loaded_instructions_cache[instruction_type]


def load_dice_instructions(dice_roll_strategy: str | None) -> str:
    """Load dice instructions based on the selected dice strategy.

    The LLM always sees "# File: dice_system_instruction.md" regardless of
    which variant is loaded, so cross-references work consistently.
    """
    strategy = dice_roll_strategy or dice_strategy.DICE_STRATEGY_NATIVE_TWO_PHASE
    if strategy == dice_strategy.DICE_STRATEGY_CODE_EXECUTION:
        # Normalize filename header so LLM sees consistent name
        return _load_instruction_file(
            constants.PROMPT_TYPE_DICE_CODE_EXECUTION
        ).replace(
            "# File: dice_system_instruction_code_execution.md",
            "# File: dice_system_instruction.md",
        )
    return _load_instruction_file(constants.PROMPT_TYPE_DICE)


def _extract_essentials(content: str) -> str:
    """Extract the ESSENTIALS block from instruction content.

    The instruction files include a concise, token-optimized block wrapped
    between `<!-- ESSENTIALS ...` and `/ESSENTIALS -->`. This parser confines
    the opening match to the end of the marker line and captures only the inner
    block to avoid stripping content. If no block is present, it returns a
    trimmed prefix to keep token usage bounded.
    """

    essentials_match = re.search(
        r"<!--\s*ESSENTIALS[^\n]*\n(.*?)\n\s*/ESSENTIALS\s*-->",
        content,
        re.DOTALL,
    )

    if essentials_match:
        return essentials_match.group(1).strip()

    # Fallback: return a trimmed prefix for files without an ESSENTIALS block
    # so token-constrained modes still receive a concise summary.
    return content[:2000].strip()


# Map section names to their prompt types for conditional loading
SECTION_TO_PROMPT_TYPE: dict[str, str] = {
    "relationships": constants.PROMPT_TYPE_RELATIONSHIP,
    "reputation": constants.PROMPT_TYPE_REPUTATION,
    "examples": constants.PROMPT_TYPE_GAME_STATE_EXAMPLES,
}

# List of valid sections that can be requested via `needs_detailed_instructions`
# Used for validation in tests and potentially runtime checks
DETAILED_INSTRUCTION_SECTIONS: set[str] = {
    *SECTION_TO_PROMPT_TYPE.keys(),
    "social_hp",  # Specifically handled by Social HP injection, not a loaded file
}

# 🚨 SHORT EARLY REMINDER - Prepended to system instruction for high-tier NPCs
# Uses unique box characters to stand out from markdown and reduce attention dilution
SOCIAL_HP_EARLY_REMINDER = """╔═══════════════════════════════════════════════════════════════╗
║ ⚠️  HIGH-TIER NPC ACTIVE: Social HP system is MANDATORY.      ║
║ Include `social_hp_challenge` JSON field + narrative box.     ║
║ Single-roll success on god/king tier = FORBIDDEN.             ║
╚═══════════════════════════════════════════════════════════════╝
"""

# 🚨 SOCIAL HP ENFORCEMENT REMINDER - Auto-injected when high-tier NPCs are present
SOCIAL_HP_ENFORCEMENT_REMINDER = """
🚨 HIGH-TIER NPC DETECTED - Social HP system MANDATORY.

REQUEST SEVERITY scaling applies (information=1×, favor=1×, submission=3×).
PROGRESS MECHANICS track via `request_severity` and `resistance_shown` fields.

See narrative_system_instruction.md for full instructions. Must include social_hp_challenge JSON field.
"""


def load_detailed_sections(requested_sections: list[str]) -> str:
    """
    Load detailed instruction sections based on LLM hints from previous turn.

    Args:
        requested_sections: List of section names like ["relationships", "reputation", "social_hp"]

    Returns:
        Combined detailed sections as a string
    """
    if not requested_sections:
        return ""

    parts = []
    for section in requested_sections:
        # Special handling for social_hp - use inline constant instead of file
        if section == "social_hp":
            parts.append(SOCIAL_HP_ENFORCEMENT_REMINDER)
            logging_util.info(
                "🚨 SOCIAL_HP: Loaded Social HP enforcement reminder into prompt"
            )
            continue

        prompt_type = SECTION_TO_PROMPT_TYPE.get(section)
        if prompt_type:
            try:
                content = _load_instruction_file(prompt_type)
                parts.append(f"\n--- {section.upper()} MECHANICS ---\n")
                parts.append(content)
            except (FileNotFoundError, ValueError) as e:
                logging_util.warning(f"Could not load section {section}: {e}")

    return "\n".join(parts)


def extract_llm_instruction_hints(llm_response: dict[str, Any]) -> list[str]:
    """
    Extract instruction hints from an LLM response's debug_info.meta field.

    The LLM can signal that it needs detailed instructions for the next turn
    by including: {"debug_info": {"meta": {"needs_detailed_instructions": ["relationships"]}}}

    Args:
        llm_response: The parsed JSON response from the LLM

    Returns:
        List of requested section names, or empty list if none requested
    """
    if not isinstance(llm_response, dict):
        return []

    # Look for meta inside debug_info (as documented in game_state_instruction.md)
    debug_info = llm_response.get("debug_info", {})
    if not isinstance(debug_info, dict):
        return []

    meta = debug_info.get("meta", {})
    if not isinstance(meta, dict):
        return []

    hints = meta.get("needs_detailed_instructions", [])
    if not isinstance(hints, list):
        return []

    # Validate hint values (only sections currently supported by detailed loaders)
    return [
        h for h in hints if isinstance(h, str) and h in DETAILED_INSTRUCTION_SECTIONS
    ]


def _add_world_instructions_to_system(system_instruction_parts: list[str]) -> None:
    """
    Add world content instructions to system instruction parts if world is enabled.
    Avoids code duplication between get_initial_story and continue_story.
    """

    world_instruction = (
        "\n**CRITICAL INSTRUCTION: USE ESTABLISHED WORLD LORE**\n"
        "This campaign MUST use the Celestial Wars/Assiah world setting provided below. "
        "DO NOT create new factions, characters, or locations - USE the established ones from the world content. "
        "ACTIVELY reference characters, factions, and locations from the provided lore. "
        "The Celestial Wars Alexiel Book takes precedence over World of Assiah documentation for conflicts. "
        "When introducing NPCs or factions, draw from the established character dossiers and faction information. "
        "DO NOT invent generic fantasy elements when rich, detailed lore is provided.\n\n"
    )
    system_instruction_parts.append(world_instruction)

    # Load world content directly into system instruction
    world_content = load_world_content_for_system_instruction()
    system_instruction_parts.append(world_content)


def _build_debug_instructions() -> str:
    """
    Build the debug mode instructions that are always included for game state management.
    The backend will strip debug content for users when debug_mode is False.

    Returns:
        str: The formatted debug instruction string
    """
    return (
        "\n**DEBUG MODE - ALWAYS GENERATE**\n"
        "You must ALWAYS include the following debug information in your response for game state management:\n"
        "\n"
        "1. **DM COMMENTARY**: Wrap any behind-the-scenes DM thoughts, rule considerations, or meta-game commentary in [DEBUG_START] and [DEBUG_END] tags.\n"
        "\n"
        "2. **DICE ROLLS**: Show ALL dice rolls throughout your response:\n"
        "   - **During Narrative**: Show important rolls (skill checks, saving throws, random events) using [DEBUG_ROLL_START] and [DEBUG_ROLL_END] tags\n"
        "   - **During Combat**: Show ALL combat rolls including attack rolls, damage rolls, initiative, saving throws, and any other dice mechanics\n"
        "   - Format: [DEBUG_ROLL_START]Rolling Perception check: 1d20+3 = 15+3 = 18 vs DC 15 (Success)[DEBUG_ROLL_END]\n"
        "   - Include both the dice result and the final total with modifiers, **and always state the DC/target you rolled against** (e.g., 'vs DC 15' or 'vs AC 17')\n"
        "\n"
        "3. **RESOURCES USED**: Track resources expended during the scene:\n"
        "   - Format: [DEBUG_RESOURCES_START]Resources: 1 HD used (2/3 remaining), 1 spell slot level 2 (2/3 remaining), short rests: 1/2[DEBUG_RESOURCES_END]\n"
        "   - Include: Hit Dice (HD), spell slots by level, class features (ki points, rage, etc.), consumables, exhaustion\n"
        "   - Show both used and remaining for each resource\n"
        "\n"
        "4. **STATE CHANGES**: After your main narrative, include a section wrapped in [DEBUG_STATE_START] and [DEBUG_STATE_END] tags that explains what state changes you're proposing and why.\n"
        "\n"
        "**Examples:**\n"
        "- [DEBUG_START]The player is attempting a stealth approach, so I need to roll for the guards' perception...[DEBUG_END]\n"
        "- [DEBUG_ROLL_START]Guard Perception: 1d20+2 = 12+2 = 14 vs DC 15 (Failure - guards don't notice)[DEBUG_ROLL_END]\n"
        "- [DEBUG_RESOURCES_START]Resources: 0 HD used (3/3 remaining), no spell slots used, short rests: 2/2[DEBUG_RESOURCES_END]\n"
        "- [DEBUG_STATE_START]Updating player position to 'hidden behind crates' and setting guard alertness to 'unaware'[DEBUG_STATE_END]\n"
        "\n"
        "NOTE: This debug information helps maintain game state consistency and will be conditionally shown to players based on their debug mode setting.\n\n"
    )


class PromptBuilder:
    """
    Encapsulates prompt building logic for the Gemini service.

    This class is responsible for constructing comprehensive system instructions
    that guide the AI's behavior as a digital D&D Game Master. It manages the
    complex hierarchy of instructions and ensures proper ordering and integration.

    Key Responsibilities:
    - Build core system instructions in proper precedence order
    - Add character-related instructions conditionally
    - Include selected prompt types (narrative, mechanics)
    - Add system reference instructions (D&D SRD)
    - Generate companion and background summary instructions
    - Manage world content integration
    - Ensure debug instructions are properly included

    Instruction Hierarchy (in order of loading):
    1. Master directive (establishes authority)
    2. Game state instructions (data structure compliance)
    3. Planning protocol (canonical planning_block schema)
    4. Debug instructions (technical functionality)
    5. Character template (conditional)
    6. Selected prompts (narrative/mechanics)
    7. System references (D&D SRD)
    8. World content (conditional)

    The class ensures that instructions are loaded in the correct order to
    prevent "instruction fatigue" and maintain proper AI behavior hierarchy.
    """

    def __init__(self, game_state: GameState | None = None) -> None:
        """
        Initialize the PromptBuilder.

        Args:
            game_state (GameState, optional): GameState object used for dynamic
                instruction generation, companion lists, and story summaries.
                If None, static fallback instructions will be used.
        """
        self.game_state = game_state
        # Store last-built blocks for evidence capture
        self._last_identity_block: str = ""
        self._last_directives_block: str = ""

    @property
    def last_identity_block(self) -> str:
        """Return the last-built character identity block (for evidence capture)."""
        return self._last_identity_block

    @property
    def last_directives_block(self) -> str:
        """Return the last-built god mode directives block (for evidence capture)."""
        return self._last_directives_block

    def _append_game_state_with_planning(self, parts: list[str]) -> None:
        """Append game_state plus planning_protocol in a single, centralized step."""
        # Load game_state instruction first (highest authority after master directive)
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_GAME_STATE))
        # Load planning protocol immediately after game_state to anchor schema references
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_PLANNING_PROTOCOL))

    def _append_campaign_setting_if_present(self, parts: list[str]) -> None:
        """
        Append campaign setting (world lore) from god_mode.setting if present.

        This ensures custom world lore is included in system instructions,
        which is critical for:
        1. Budget allocation to measure actual system instruction size
        2. LLM to see campaign-specific context and rules
        3. Budget warnings to trigger when setting is too large

        FIX: Bug worktree_logs6-xxx - god_mode.setting was stored but never
        included in system instructions, causing budget warnings to never trigger.
        """
        if not self.game_state:
            logging_util.debug("🔍 CAMPAIGN_SETTING: No game_state available")
            return

        # Extract god_mode data from custom_campaign_state (where it's actually stored)
        god_mode = None
        if hasattr(self.game_state, "custom_campaign_state"):
            # GameState object - access custom_campaign_state attribute
            # FIX Issue 1: Add isinstance check - custom_campaign_state can be None or non-dict
            custom_campaign_state = self.game_state.custom_campaign_state
            if isinstance(custom_campaign_state, dict):
                god_mode = custom_campaign_state.get("god_mode")
                logging_util.debug(
                    "🔍 CAMPAIGN_SETTING: Accessed from GameState.custom_campaign_state"
                )
            else:
                logging_util.debug(
                    f"🔍 CAMPAIGN_SETTING: custom_campaign_state is not dict: {type(custom_campaign_state)}"
                )
        elif isinstance(self.game_state, dict):
            # Dict format - access custom_campaign_state key
            # FIX Issue 2: Add isinstance check on custom_state - can be malformed (string, etc.)
            custom_state = self.game_state.get("custom_campaign_state", {})
            if isinstance(custom_state, dict):
                god_mode = custom_state.get("god_mode")
                logging_util.debug(
                    "🔍 CAMPAIGN_SETTING: Accessed from dict custom_campaign_state"
                )
            else:
                logging_util.debug(
                    f"🔍 CAMPAIGN_SETTING: custom_campaign_state value is not dict: {type(custom_state)}"
                )

        if god_mode is None:
            logging_util.debug(
                "🔍 CAMPAIGN_SETTING: No god_mode in custom_campaign_state"
            )
            return

        if not isinstance(god_mode, dict):
            logging_util.debug(
                f"🔍 CAMPAIGN_SETTING: god_mode is not dict: {type(god_mode)}"
            )
            return

        # Get campaign setting field
        setting = god_mode.get("setting")
        if setting is None:
            logging_util.debug("🔍 CAMPAIGN_SETTING: No setting in god_mode")
            return

        if not isinstance(setting, str):
            logging_util.debug(
                f"🔍 CAMPAIGN_SETTING: setting is not str: {type(setting)}"
            )
            return

        setting = setting.strip()
        if not setting:
            logging_util.debug("🔍 CAMPAIGN_SETTING: setting is empty after strip")
            return

        setting_chars = len(setting)
        logging_util.info(
            f"✅ CAMPAIGN_SETTING: Adding {setting_chars:,} chars to system instruction"
        )

        # Build campaign setting block
        setting_block = (
            "# Campaign Setting (Custom World Lore)\n\n"
            "**CRITICAL: This is the custom world setting for this campaign.**\n"
            "All story elements, NPCs, locations, and lore MUST align with this setting.\n\n"
            f"{setting}\n"
        )

        parts.append(setting_block)

    def _maybe_add_social_hp_early_reminder(
        self, parts: list[str], *, source: str
    ) -> None:
        """Prepend Social HP reminder when high-tier NPCs are present."""
        if self.game_state is None:
            return

        npc_data = getattr(self.game_state, "npc_data", None) or {}
        if not isinstance(npc_data, dict):
            return

        def _safe_int(value, default=0):
            try:
                return int(value)
            except (TypeError, ValueError):
                return default

        for _npc_id, npc_info in npc_data.items():
            if not isinstance(npc_info, dict):
                continue
            tier = str(npc_info.get("tier", "")).lower()
            level = _safe_int(npc_info.get("level"))
            if (
                tier in ("god_primordial", "king_ancient", "lord_general")
                or level >= 15
            ):
                parts.append(SOCIAL_HP_EARLY_REMINDER)
                logging_util.info(f"🚨 SOCIAL_HP: Prepended early reminder to {source}")
                break  # Only add once

    def build_from_order(  # noqa: PLR0912
        self,
        prompt_order: tuple[str, ...],
        *,
        include_debug: bool = False,
        dice_roll_strategy: str | None = None,
        turn_number: int = 0,
        advances_time: bool = True,
    ) -> list[str]:
        """
        Build system instructions from an ordered tuple of prompt types.

        This is the generic builder that replaces mode-specific builders.
        It loads prompts in the exact order specified, with special handling
        for the game_state + planning_protocol consecutive pair.

        Args:
            prompt_order: Ordered tuple of prompt types to load
            include_debug: Whether to append debug instructions at the end
            turn_number: Current turn number for context-aware prompts
            advances_time: Whether this request should advance world time

        Returns:
            List of instruction parts in the specified order
        """
        parts: list[str] = []
        skip_next = False

        # 🚨 EARLY REMINDER: Check for high-tier NPCs and prepend Social HP reminder
        # This appears BEFORE all other instructions to maximize attention
        # (Migrated from build_core_system_instructions to ensure consistency)
        self._maybe_add_social_hp_early_reminder(parts, source="build_from_order")

        is_code_execution = (
            dice_roll_strategy == dice_strategy.DICE_STRATEGY_CODE_EXECUTION
        )
        dice_loaded = False
        append_dice_after_combat = is_code_execution and (
            constants.PROMPT_TYPE_COMBAT in prompt_order
        )

        for i, prompt_type in enumerate(prompt_order):
            if skip_next:
                skip_next = False
                continue

            # Special handling: game_state and planning_protocol must load together
            if prompt_type == constants.PROMPT_TYPE_GAME_STATE:
                # Verify next is planning_protocol (invariant from Phase 0)
                if (
                    i + 1 < len(prompt_order)
                    and prompt_order[i + 1] == constants.PROMPT_TYPE_PLANNING_PROTOCOL
                ):
                    self._append_game_state_with_planning(parts)
                    skip_next = True
                else:
                    # Fallback: load individually (shouldn't happen with valid orders)
                    parts.append(_load_instruction_file(prompt_type))
                # Dice instructions were part of game_state_instruction.md, now isolated
                # Load them after game_state for all agents that need dice
                # Only add when dice_roll_strategy is explicitly specified (not None)
                if not dice_loaded and dice_roll_strategy is not None:
                    parts.append(load_dice_instructions(dice_roll_strategy))
                    dice_loaded = True
            elif prompt_type == constants.PROMPT_TYPE_PLANNING_PROTOCOL:
                # Should have been handled with game_state above
                # Load individually as fallback
                parts.append(_load_instruction_file(prompt_type))
            elif prompt_type == constants.PROMPT_TYPE_DEFERRED_REWARDS:
                # Use context-aware builder for deferred rewards
                # For explicit agents, we force include it
                parts.append(
                    self.build_deferred_rewards_instruction(
                        turn_number,
                        force_include=True,
                        force_reason="Explicit deferred rewards check invoked.",
                    )
                )
            elif prompt_type == constants.PROMPT_TYPE_LIVING_WORLD:
                # Use context-aware builder for living world
                # This triggers the 3-turn/24-hour logic and updates game state
                living_world_instruction = self.build_living_world_instruction(
                    turn_number
                )
                if living_world_instruction:
                    parts.append(living_world_instruction)
            else:
                # Standard prompt loading
                parts.append(_load_instruction_file(prompt_type))
                # Legacy: also load dice after mechanics for backward compatibility
                # Only add when dice_roll_strategy is explicitly specified (not None)
                if (
                    prompt_type == constants.PROMPT_TYPE_MECHANICS
                    and not dice_loaded
                    and dice_roll_strategy is not None
                ):
                    parts.append(load_dice_instructions(dice_roll_strategy))
                    dice_loaded = True
                if (
                    append_dice_after_combat
                    and not dice_loaded
                    and prompt_type == constants.PROMPT_TYPE_COMBAT
                ):
                    parts.append(load_dice_instructions(dice_roll_strategy))
                    dice_loaded = True

        # Global policy: include living world instruction every active turn,
        # even for agents whose prompt order doesn't explicitly include it.
        if (
            advances_time
            and
            turn_number >= 1
            and constants.PROMPT_TYPE_LIVING_WORLD not in prompt_order
        ):
            living_world_instruction = self.build_living_world_instruction(turn_number)
            if living_world_instruction:
                parts.append(living_world_instruction)

        # Optionally append debug instructions
        if include_debug:
            parts.append(_build_debug_instructions())

        return parts

    def build_for_agent(
        self,
        agent: BaseAgent,
        dice_roll_strategy: str | None = None,
        turn_number: int = 0,
    ) -> list[str]:
        """
        Build system instructions for a given agent using its prompt order and flags.

        This is the single entry point for prompt building (Phase 3).
        It delegates to build_from_order() with the agent's configuration.

        Args:
            agent: The agent instance to build instructions for
            dice_roll_strategy: Dice strategy for random rolls
            turn_number: Current turn number (for living world/deferred rewards)

        Returns:
            List of instruction parts in the agent's specified order
        """
        if not isinstance(agent, AgentProtocol):
            # Fallback for objects that don't explicitly inherit from AgentProtocol
            # but provide the required interface.
            required_methods = ("prompt_order", "builder_flags")
            missing = [
                method
                for method in required_methods
                if not callable(getattr(agent, method, None))
            ]
            if missing:
                raise TypeError(
                    f"Expected AgentProtocol or agent with {', '.join(missing)} methods, got "
                    f"{type(agent).__name__}"
                )

        prompt_order = agent.prompt_order()
        flags = agent.builder_flags()

        return self.build_from_order(
            prompt_order,
            include_debug=flags.get("include_debug", False),
            dice_roll_strategy=dice_roll_strategy,
            turn_number=turn_number,
            advances_time=agent.advances_time,
        )

    def build_core_system_instructions(self) -> list[str]:
        """
        Build the core system instructions that are always loaded first.
        Returns a list of instruction parts.
        """
        parts = []

        # 🚨 EARLY REMINDER: Check for high-tier NPCs and prepend Social HP reminder
        # This appears BEFORE all other instructions to maximize attention
        self._maybe_add_social_hp_early_reminder(parts, source="core instructions")

        # CRITICAL: Load master directive FIRST to establish hierarchy and authority
        # This must come before all other instructions to set the precedence rules
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_MASTER_DIRECTIVE))

        # Load game_state + planning protocol together (single entry point)
        self._append_game_state_with_planning(parts)

        # Add debug mode instructions THIRD for technical functionality
        # The backend will strip debug content for users when debug_mode is False
        parts.append(_build_debug_instructions())

        return parts

    def build_god_mode_instructions(self) -> list[str]:
        """
        Build system instructions for GOD MODE.
        God mode is for administrative control (correcting mistakes, modifying campaign),
        NOT for playing the game. Includes game rules knowledge for proper corrections.
        """
        parts = []

        # CRITICAL: Load master directive FIRST to establish hierarchy and authority
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_MASTER_DIRECTIVE))

        # Load god mode specific instruction (administrative commands)
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_GOD_MODE))

        # NOTE: Campaign setting (_append_campaign_setting_if_present) is added in
        # finalize_instructions(), not here. This method is legacy and doesn't call
        # finalize_instructions() itself, but production code does through build_from_order().
        # Adding campaign setting here would cause duplication if finalize_instructions() is called.

        # Load game_state + planning protocol together (single entry point)
        # God mode can still emit planning blocks for structured choices.
        self._append_game_state_with_planning(parts)

        # Load D&D SRD for game rules knowledge
        # (AI needs to understand game mechanics to make proper corrections)
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_DND_SRD))

        # Load mechanics instruction for detailed game rules
        # (spell slots, class features, combat rules, etc.)
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_MECHANICS))

        return parts

    def build_info_mode_instructions(self) -> list[str]:
        """
        Build TRIMMED system instructions for INFO MODE.
        Info mode is for pure information queries (equipment, inventory, stats).
        Uses minimal prompts to maximize LLM focus on Equipment Query Protocol.

        Note: NO narrative, mechanics, or combat prompts - keeps system instruction
        under ~1100 lines vs ~2000 lines for story mode, improving LLM compliance.
        The actual game state JSON is added by llm_service when building the prompt.
        """
        parts = []

        # CRITICAL: Load master directive FIRST to establish hierarchy and authority
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_MASTER_DIRECTIVE))

        # Load game_state + planning protocol together (single entry point)
        # Info mode still returns planning_block per game_state_instruction.md
        self._append_game_state_with_planning(parts)

        return parts

    def build_combat_mode_instructions(self) -> list[str]:
        """
        Build system instructions for COMBAT MODE.
        Combat mode is for active combat encounters with focused tactical prompts.
        Emphasizes: dice rolls, initiative, combat rewards, boss equipment.
        """
        parts = []

        # CRITICAL: Load master directive FIRST to establish hierarchy and authority
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_MASTER_DIRECTIVE))

        # Load game_state + planning protocol together (single entry point)
        self._append_game_state_with_planning(parts)

        # Load combat-specific instruction (tactical combat management)
        # (References game_state schema for combat_state updates)
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_COMBAT))

        # Load narrative instruction for DM Note protocol and cinematic style
        # (Enables out-of-character communication during combat)
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_NARRATIVE))

        # Load D&D SRD for combat rules
        # (Attack rolls, saving throws, damage, conditions)
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_DND_SRD))

        # Load mechanics instruction for detailed combat mechanics
        # (Initiative, action economy, combat XP, etc.)
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_MECHANICS))

        # Add debug instructions for combat logging
        parts.append(_build_debug_instructions())

        return parts

    def build_rewards_mode_instructions(self) -> list[str]:
        """
        Build system instructions for REWARDS MODE.
        Rewards mode handles XP, loot, and level-up processing from any source:
        - Combat victories (when combat_phase == "ended")
        - Non-combat encounters (heists, social victories, stealth)
        - Quest completions
        - Milestone achievements
        """
        parts = []

        # CRITICAL: Load master directive FIRST to establish hierarchy and authority
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_MASTER_DIRECTIVE))

        # Load game_state + planning protocol together (single entry point)
        self._append_game_state_with_planning(parts)

        # Load rewards-specific instruction (XP, loot, level-up rules)
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_REWARDS))

        # Load D&D SRD for XP thresholds and level rules
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_DND_SRD))

        # Load mechanics instruction for detailed level-up mechanics
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_MECHANICS))

        # Add debug instructions for reward processing logging
        parts.append(_build_debug_instructions())

        return parts

    def build_character_creation_instructions(self) -> list[str]:
        """
        Build system instructions for CHARACTER CREATION MODE.
        Character creation mode focuses on creating the character and handling
        level-ups. The story only advances when the user explicitly confirms
        they're done. TIME DOES NOT ADVANCE during this mode.

        Prompt set for character creation and level-up:
        1. Master directive (establishes AI authority)
        2. Game state instruction (canonical schemas for equipment/spells/stats)
        3. Character creation instruction (focused creation flow with level-up rules)
        4. D&D SRD (race/class/background/level-up options)
        5. Mechanics (detailed D&D rules for level-up choices)

        No narrative or combat prompts - time is frozen during this mode.
        """
        parts = []

        # Load master directive first (establishes authority)
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_MASTER_DIRECTIVE))

        # Load game state schema reference so character creation stays aligned with UI buttons.
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_GAME_STATE))

        # Load character creation instruction (the focused creation flow)
        # Contains level-up tables, XP thresholds, multiclassing prerequisites
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_CHARACTER_CREATION))

        # Load D&D SRD for mechanics reference (race/class/background options)
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_DND_SRD))

        # Load mechanics for detailed D&D rules (level-up, spells, feats, etc.)
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_MECHANICS))

        return parts

    def build_think_mode_instructions(self) -> list[str]:
        """
        Build system instructions for THINK MODE.
        Think mode is for strategic planning and tactical analysis without
        narrative advancement. Time only advances by 1 microsecond.

        Uses a focused prompt set for deep planning operations:
        - Master directive (authority)
        - Think mode instruction (planning behavior)
        - Game state instruction (state structure reference)
        - D&D SRD (game rules knowledge for informed planning)
        """
        parts = []

        # CRITICAL: Load master directive FIRST to establish hierarchy and authority
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_MASTER_DIRECTIVE))

        # Load think mode specific instruction (planning/thinking behavior)
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_THINK))

        # Load game_state + planning protocol together (single entry point)
        self._append_game_state_with_planning(parts)

        # Load D&D SRD for game rules knowledge
        # (AI needs to understand game mechanics for strategic planning)
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_DND_SRD))

        return parts

    def build_faction_mode_instructions(self) -> list[str]:
        """
        Build system instructions for FACTION/ARMY MANAGEMENT MODE.
        Faction mode is for commanding forces of 20+ units with strategic mass combat.
        Emphasizes: unit blocks, upkeep tracking, morale, mass combat resolution.
        """
        parts = []

        # CRITICAL: Load master directive FIRST to establish hierarchy and authority
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_MASTER_DIRECTIVE))

        # Load game state + planning protocol together (required adjacent to game_state)
        # (AI needs to know army_data structure and planning block format)
        self._append_game_state_with_planning(parts)

        # Load faction management instruction (mass combat, army management)
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_FACTION_MANAGEMENT))

        # Load D&D SRD for base rules reference
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_DND_SRD))

        # Load mechanics instruction for detailed game mechanics
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_MECHANICS))

        # Add debug instructions for army state logging
        parts.append(_build_debug_instructions())

        return parts

    def add_character_instructions(
        self, parts: list[str], selected_prompts: list[str]
    ) -> None:
        """
        Conditionally add character-related instructions based on selected prompts.
        """
        # Conditionally add the character template if narrative instructions are selected
        if constants.PROMPT_TYPE_NARRATIVE in selected_prompts:
            parts.append(
                _load_instruction_file(constants.PROMPT_TYPE_CHARACTER_TEMPLATE)
            )

    def add_selected_prompt_instructions(  # noqa: PLR0912
        self,
        parts: list[str],
        selected_prompts: list[str],
        llm_requested_sections: list[str] | None = None,
        essentials_only: bool = False,
        dice_roll_strategy: str | None = None,
    ) -> None:
        """
        Add instructions for selected prompt types in consistent order.

        Args:
            parts: List to append instruction parts to
            selected_prompts: List of prompt types to include
            llm_requested_sections: Sections the LLM requested via meta.needs_detailed_instructions
            essentials_only: When True, append detailed sections (for token-constrained mode).
                When False, assume the full narrative prompt already contains these sections
                and avoid duplicating them.
        """
        # Define the order for consistency (calibration archived)
        prompt_order = [
            constants.PROMPT_TYPE_NARRATIVE,
            constants.PROMPT_TYPE_MECHANICS,
        ]

        # CRITICAL: Narrative instructions are ALWAYS required when building story mode instructions
        # StoryModeAgent's job is to generate narrative, so it must always have narrative instructions
        # even if "narrative" is not explicitly in selected_prompts
        # This fixes smoke test failures where campaigns are created without narrative in selected_prompts
        # Ensure narrative is always included for story mode (this method is only called by StoryModeAgent)
        # Create a copy to avoid mutating the caller's list
        effective_prompts = list(selected_prompts) if selected_prompts else []
        # Only force narrative if we are asking for SOME prompts.
        # If the list is explicitly empty, respect that (fixes test_add_selected_prompt_instructions_handles_empty).
        if (
            effective_prompts
            and constants.PROMPT_TYPE_NARRATIVE not in effective_prompts
        ):
            effective_prompts.append(constants.PROMPT_TYPE_NARRATIVE)

        # Add in order
        for p_type in prompt_order:
            if p_type in effective_prompts:
                content = _load_instruction_file(p_type)
                parts.append(
                    _essentials_raw_cache.get(p_type, content[:2000]) if essentials_only else content
                )

        # CRITICAL: Always load dice instructions for StoryModeAgent
        # Dice instructions were previously only loaded after MECHANICS, but
        # narrative rolls require dice even without mechanics selected.
        # PR #4334: Isolated dice instructions must always be included.
        # Only include if we are actually building prompts (not empty list)
        if effective_prompts:
            parts.append(load_dice_instructions(dice_roll_strategy))

        # Identify detailed sections requested via selected_prompts (legacy support / test support)
        # Some callers/tests pass section names (e.g. "relationships") directly in selected_prompts
        # We need to extract them and treat them as requested sections.
        effective_detailed_sections = (
            set(llm_requested_sections) if llm_requested_sections else set()
        )

        # Check for section names in effective_prompts
        for p in effective_prompts:
            if p in SECTION_TO_PROMPT_TYPE:
                effective_detailed_sections.add(p)

        # Convert back to sorted list for deterministic loading order
        final_requested_sections = sorted(effective_detailed_sections)

        # Append detailed sections based on mode and LLM requests
        if essentials_only:
            # ESSENTIALS mode: Always load detailed sections (either LLM-requested or all)
            if final_requested_sections:
                requested = final_requested_sections
            elif constants.PROMPT_TYPE_NARRATIVE in effective_prompts:
                requested = list(SECTION_TO_PROMPT_TYPE.keys())
            else:
                requested = []

            detailed_content = load_detailed_sections(requested)
            if detailed_content:
                parts.append(detailed_content)
        elif final_requested_sections:
            # NON-ESSENTIALS (Story Mode): Load ONLY LLM-requested detailed sections
            # This enables dynamic prompt loading where the LLM can request specific
            # sections (e.g., relationships, reputation) for the next turn via
            # debug_info.meta.needs_detailed_instructions.
            # These detailed sections are separate files, not duplicated in narrative.
            detailed_content = load_detailed_sections(final_requested_sections)
            if detailed_content:
                parts.append(detailed_content)

    def add_system_reference_instructions(self, parts: list[str]) -> None:
        """
        Add system reference instructions that are always included.
        """
        # Always include the D&D SRD instruction (replaces complex dual-system approach)
        parts.append(_load_instruction_file(constants.PROMPT_TYPE_DND_SRD))

    def _extract_companions_from_state(
        self, state: dict[str, Any] | None
    ) -> dict[str, Any] | None:
        """
        Extract companions from game state, checking both game_state.companions and npc_data.

        Returns a dict of companions if found, None otherwise.
        Handles malformed data (non-dict companions) by falling back to npc_data scan.
        """
        if not isinstance(state, dict):
            logging_util.info(
                f"🎭 _extract_companions_from_state: State is not a dict: {type(state)}"
            )
            return None

        # First, check game_state.companions
        companions_raw = state.get("game_state", {}).get("companions")
        if companions_raw and isinstance(companions_raw, dict):
            logging_util.info(
                f"🎭 _extract_companions_from_state: Found companions in game_state.companions: {list(companions_raw.keys())}"
            )
            return companions_raw

        # Fallback: scan npc_data for companions
        npc_data = state.get("npc_data", {})
        if not isinstance(npc_data, dict):
            logging_util.info(
                f"🎭 _extract_companions_from_state: npc_data is not a dict: {type(npc_data)}"
            )
            return None

        companions = {
            name: npc
            for name, npc in npc_data.items()
            if isinstance(npc, dict) and npc.get("relationship") == "companion"
        }

        if companions:
            logging_util.info(
                f"🎭 _extract_companions_from_state: Found companions in npc_data: {list(companions.keys())}"
            )
        else:
            logging_util.info(
                f"🎭 _extract_companions_from_state: No companions found in npc_data (keys: {list(npc_data.keys())})"
            )

        return companions if companions else None

    def build_companion_instruction(self) -> str:
        """Build companion instruction text."""
        state: dict[str, Any] | None = None
        if self.game_state is not None:
            if hasattr(self.game_state, "to_dict"):
                state = self.game_state.to_dict()
            elif hasattr(self.game_state, "data"):
                state = self.game_state.data

        companions = self._extract_companions_from_state(state)

        if companions and isinstance(companions, dict):
            companion_names = list(companions.keys())
            logging_util.info(
                f"🎭 build_companion_instruction: Found {len(companion_names)} companions: {companion_names}"
            )
            lines = [
                "\n**🚨🚨🚨 CRITICAL: ACTIVE COMPANIONS - USE THESE EXACT COMPANIONS IN YOUR NARRATIVE 🚨🚨🚨**",
                "**THIS IS A MANDATORY REQUIREMENT. FAILURE TO COMPLY WILL RESULT IN INCORRECT OUTPUT.**",
                "",
                "**DO NOT GENERATE NEW COMPANIONS.**",
                "**DO NOT CREATE COMPANIONS.**",
                "**DO NOT INVENT COMPANIONS.**",
                "",
                "These companions are ALREADY part of the party and MUST appear in your story.",
                "**YOU MUST MENTION THESE COMPANIONS BY NAME IN YOUR NARRATIVE TEXT.**",
                "**YOU MUST USE THESE EXACT NAMES. NO SUBSTITUTIONS. NO VARIATIONS.**",
                "",
                "**ONLY USE THESE COMPANIONS:**",
            ]
            for name, info in companions.items():
                if not isinstance(info, dict):
                    continue
                role = info.get("role", info.get("class", "Unknown"))
                background = info.get("background", "")
                mbti = info.get("mbti", "")
                # Type-safe background formatting: only slice if it's a string
                background_str = ""
                if background and isinstance(background, str):
                    background_str = f": {background[:80]}"
                lines.append(f"- **{name}** ({role}){background_str}")
                if mbti:
                    lines.append(f"  MBTI: {mbti}")
            lines.extend(
                [
                    "",
                    "**MANDATORY NARRATIVE REQUIREMENT:**",
                    "In your opening narrative, explicitly mention these companions traveling with the player character.",
                    "Use their EXACT names: " + ", ".join(companion_names),
                    "",
                    "**EXAMPLE (CORRECT):**",
                    "'You stand at the edge of Oakhaven with "
                    + ", ".join(companion_names)
                    + " at your side...'",
                    "",
                    "**FORBIDDEN:**",
                    "- ❌ DO NOT mention any companions not listed above",
                    "- ❌ DO NOT create new companions",
                    "- ❌ DO NOT use different names",
                    "- ❌ DO NOT invent companions",
                    "",
                    "**VERIFICATION:** After generating your narrative, verify that ALL of these companions are mentioned by name: "
                    + ", ".join(companion_names),
                ]
            )
            return "\n".join(lines)

        # Fallback to static instruction used during initial story generation
        return (
            "\n**SPECIAL INSTRUCTION: COMPANION GENERATION ACTIVATED**\n"
            "You have been specifically requested to generate EXACTLY 3 starting companions for this campaign.\n\n"
            "**MANDATORY REQUIREMENTS:**\n"
            "1. Generate exactly 3 unique companions with diverse party roles (e.g., warrior, healer, scout)\n"
            "2. Each companion MUST have a valid MBTI personality type (e.g., ISTJ, INFP, ESTP)\n"
            "3. Each companion MUST include: name, background story, skills array, personality traits, equipment\n"
            "4. Set relationship field to 'companion' for all generated NPCs\n"
            "5. Include all companions in the npc_data section of your JSON response\n\n"
            "**JSON STRUCTURE EXAMPLE:**\n"
            '"npc_data": {\n'
            '  "Companion Name": {\n'
            '    "mbti": "ISTJ",\n'
            '    "role": "warrior",\n'
            '    "background": "Detailed background story",\n'
            '    "relationship": "companion",\n'
            '    "skills": ["combat", "defense", "weapon mastery"],\n'
            '    "personality_traits": ["loyal", "protective", "methodical"],\n'
            '    "equipment": ["enchanted shield", "battle axe", "chainmail"]\n'
            "  }\n"
            "}\n\n"
            "**VERIFICATION:** Ensure your response contains exactly 3 NPCs with relationship='companion' in npc_data.\n\n"
        )

    def build_background_summary_instruction(self) -> str:
        """Build background summary instruction text."""

        state: dict[str, Any] | None = None
        if self.game_state is not None:
            if hasattr(self.game_state, "to_dict"):
                state = self.game_state.to_dict()
            elif hasattr(self.game_state, "data"):
                state = self.game_state.data

        story: dict[str, Any] | None = None
        if isinstance(state, dict):
            story = state.get("game_state", {}).get("story")

        summary: str | None = None
        if isinstance(story, dict):
            summary = story.get("summary")

        if summary:
            return f"**STORY SUMMARY**\n{summary}"

        # Fallback to static background instruction
        return (
            "\n**CRITICAL INSTRUCTION: START WITH BACKGROUND SUMMARY**\n"
            "Before beginning the actual narrative, you MUST provide a background summary section that orients the player. "
            "This should be 2-4 paragraphs covering:\n"
            "1. **World Background:** A brief overview of the setting, key factions, current political situation, and important world elements (without major spoilers)\n"
            "2. **Character History:** Who the character is, their background, motivations, and current situation (based on the prompt provided)\n"
            "3. **Current Context:** What brings them to this moment and why their story is beginning now\n\n"
            "**Requirements:**\n"
            "- Keep it concise but informative (2-4 paragraphs total)\n"
            "- NO future plot spoilers or major story reveals\n"
            "- Focus on established facts the character would know\n"
            "- End with a transition into the opening scene\n"
            "- Use a clear header like '**--- BACKGROUND ---**' to separate this from the main narrative\n\n"
            "After the background summary, proceed with the normal opening scene and narrative.\n\n"
            "\n**🚨 CRITICAL: ESTABLISH INITIAL WORLD TIME (FIRST TURN ONLY)**\n"
            "This is a NEW CAMPAIGN. You MUST establish the initial `world_time` in your `state_updates.world_data`.\n\n"
            "**Required:** Include a complete `world_time` object using the setting's in-world calendar:\n"
            "- For Forgotten Realms: Use Dale Reckoning (DR), e.g., year 1492\n"
            "- For other settings: Use the appropriate lore calendar\n"
            "- NEVER use real-world dates (2025, 2026, etc.)\n\n"
            "**Example `state_updates.world_data.world_time`:**\n"
            "```json\n"
            "{\n"
            '  "year": 1492,\n'
            '  "month": 3,\n'
            '  "day": 15,\n'
            '  "hour": 14,\n'
            '  "minute": 30,\n'
            '  "second": 0,\n'
            '  "time_of_day": "afternoon"\n'
            "}\n"
            "```\n\n"
        )

    def build_character_identity_block(self) -> str:  # noqa: PLR0912, PLR0915
        """
        Build character identity block for system prompts.

        This ensures the LLM always has access to immutable character facts
        like name, gender, pronouns, and key relationships, preventing
        misgendering and identity confusion.

        Returns:
            Formatted string block or empty string if no game state
        """
        if not self.game_state:
            return ""

        # Use the GameState method if available
        if hasattr(self.game_state, "get_character_identity_block"):
            return self.game_state.get_character_identity_block()

        # Fallback for dict-based game state
        pc = None
        if hasattr(self.game_state, "player_character_data"):
            pc = self.game_state.player_character_data
        elif isinstance(self.game_state, dict):
            pc = self.game_state.get("player_character_data", {})

        if not pc or not isinstance(pc, dict):
            return ""

        lines = ["## Character Identity (IMMUTABLE)"]

        # Name
        name = pc.get("name")
        if name:
            lines.append(f"- **Name**: {name}")

        # Gender and pronouns - handle None values properly
        gender_raw = pc.get("gender")
        gender = str(gender_raw).lower() if gender_raw else ""
        if gender:
            if gender in ("female", "woman", "f"):
                lines.append("- **Gender**: Female (she/her)")
                lines.append(
                    "- **NEVER** refer to this character as 'he', 'him', "
                    "or use male-gendered familial terms for them"
                )
            elif gender in ("male", "man", "m"):
                lines.append("- **Gender**: Male (he/him)")
                lines.append(
                    "- **NEVER** refer to this character as 'she', 'her', "
                    "or use female-gendered familial terms for them"
                )
            else:
                lines.append(f"- **Gender**: {gender}")

        # Race
        race = pc.get("race")
        if race:
            lines.append(f"- **Race**: {race}")

        # Class
        char_class = pc.get("class") or pc.get("character_class")
        if char_class:
            lines.append(f"- **Class**: {char_class}")

        # Key relationships
        relationships = pc.get("relationships", {})
        if isinstance(relationships, dict) and relationships:
            lines.append("- **Key Relationships**:")
            for rel_name, rel_type in relationships.items():
                lines.append(f"  - {rel_name}: {rel_type}")

        # Parentage (important for characters like Alexiel)
        parentage = pc.get("parentage") or pc.get("parents")
        if parentage:
            if isinstance(parentage, dict):
                for parent_type, parent_name in parentage.items():
                    lines.append(f"- **{parent_type.title()}**: {parent_name}")
            elif isinstance(parentage, str):
                lines.append(f"- **Parentage**: {parentage}")

        # Active Effects (buffs, conditions, persistent effects)
        # These MUST be applied to all relevant rolls and checks
        active_effects = pc.get("active_effects", [])
        if active_effects and isinstance(active_effects, list):
            lines.append("")
            lines.append("### Active Effects (ALWAYS APPLY)")
            lines.append(
                "The following buffs/effects are ALWAYS active and MUST be applied "
                "to all relevant rolls, checks, saves, and combat calculations:"
            )
            for effect in active_effects:
                if isinstance(effect, str) and effect.strip():
                    lines.append(f"  - {effect}")
                elif isinstance(effect, dict):
                    effect_name = (
                        effect.get("name") or effect.get("effect") or str(effect)
                    )
                    lines.append(f"  - {effect_name}")

        if len(lines) == 1:
            return ""  # Only header, no actual data

        return "\n".join(lines)

    def build_god_mode_directives_block(self) -> str:  # noqa: PLR0912, PLR0915
        """
        Build god mode directives block for system prompts.

        These are player-defined rules that persist across sessions
        and MUST be followed by the LLM. Also includes DM notes that
        may contain important context the LLM wrote but didn't formally
        save as directives.

        Directives are shown NEWEST FIRST for precedence - if there are
        conflicting rules, the most recent one takes priority.

        Returns:
            Formatted string block or empty string if no directives
        """
        if not self.game_state:
            return ""

        # Fallback for dict-based game state
        custom_state = None
        debug_info = None
        if hasattr(self.game_state, "custom_campaign_state"):
            custom_state = self.game_state.custom_campaign_state
        elif isinstance(self.game_state, dict):
            custom_state = self.game_state.get("custom_campaign_state", {})

        # Get debug_info for dm_notes
        if hasattr(self.game_state, "debug_info"):
            debug_info = self.game_state.debug_info
        elif isinstance(self.game_state, dict):
            debug_info = self.game_state.get("debug_info", {})

        # Build directives section - sorted NEWEST FIRST for precedence
        base_block = ""
        if custom_state and isinstance(custom_state, dict):
            directives = custom_state.get("god_mode_directives", [])
            if directives:
                # Sort by 'added' timestamp descending (newest first)
                def get_added_ts(d):
                    if isinstance(d, dict):
                        return d.get("added", "")
                    return ""

                sorted_directives = sorted(directives, key=get_added_ts, reverse=True)

                lines = ["## Active God Mode Directives (Newest First)"]
                lines.append(
                    "The following rules were set by the player and MUST be followed."
                )
                lines.append(
                    "In case of conflicts, earlier rules take precedence (newest first):"
                )
                for i, directive in enumerate(sorted_directives, 1):
                    if isinstance(directive, dict):
                        rule = directive.get("rule", str(directive))
                    else:
                        rule = str(directive)
                    lines.append(f"{i}. {rule}")
                base_block = "\n".join(lines)

        # Add DM notes section if present (also newest first - reverse order)
        dm_notes = []
        if debug_info and isinstance(debug_info, dict):
            dm_notes = debug_info.get("dm_notes", [])

        if dm_notes:
            # Prefer timestamp-based ordering if available; otherwise fall back to reverse
            def get_note_added_ts(note: Any) -> str:
                if isinstance(note, dict):
                    return note.get("added", "")
                return ""

            has_timestamped_notes = any(
                isinstance(note, dict) and "added" in note for note in dm_notes
            )

            if has_timestamped_notes:
                ordered_notes = sorted(dm_notes, key=get_note_added_ts, reverse=True)
            else:
                # Maintain previous behavior when no timestamps are present
                ordered_notes = list(reversed(dm_notes))

            dm_lines = ["\n## DM Notes (Context from God Mode, Newest First)"]
            dm_lines.append(
                "These notes were set during God Mode and provide important context."
            )
            dm_lines.append("In case of conflicts, earlier notes take precedence:")

            for note in ordered_notes:
                if isinstance(note, dict):
                    note_text = note.get("note") or note.get("text") or str(note)
                else:
                    note_text = str(note)

                if isinstance(note_text, str):
                    note_text = note_text.strip()

                if note_text:
                    dm_lines.append(f"- {note_text}")

            # Only include the DM notes block if at least one valid note was added
            if len(dm_lines) > 3:
                dm_block = "\n".join(dm_lines)

                if base_block:
                    return base_block + "\n" + dm_block
                return dm_block

            # If no valid notes remain after filtering, fall through to base_block

        return base_block

    def build_continuation_reminder(
        self, dice_roll_strategy_param: str | None = None
    ) -> str:
        """
        Build reminders for story continuation, especially planning blocks.
        Includes temporal enforcement to prevent backward time jumps.

        Args:
            dice_roll_strategy_param: The dice strategy to use. If code_execution,
                                      adds critical dice enforcement reminder.
        """
        # Extract current world_time for temporal enforcement
        world_data = None
        if (
            self.game_state is not None
            and getattr(self.game_state, "world_data", None) is not None
        ):
            world_data = self.game_state.world_data
        world_time = (
            world_data.get("world_time", {}) if isinstance(world_data, dict) else {}
        )
        current_location = (
            world_data.get("current_location_name", "current location")
            if isinstance(world_data, dict)
            else "current location"
        )

        # Format current time for the prompt (including hidden microsecond for uniqueness)
        time_parts = []
        if world_time.get("year"):
            time_parts.append(f"{world_time.get('year')} DR")
        if world_time.get("month"):
            time_parts.append(f"{world_time.get('month')} {world_time.get('day', '')}")
        if world_time.get("hour") is not None:
            try:
                hour = int(world_time.get("hour", 0))
                minute = int(world_time.get("minute", 0))
                second = int(world_time.get("second", 0))
                time_parts.append(f"{hour:02d}:{minute:02d}:{second:02d}")
            except (ValueError, TypeError):
                time_parts.append("00:00:00")  # Fallback for invalid time values
        current_time_str = ", ".join(time_parts) if time_parts else "current timestamp"

        # Include microsecond for precise temporal tracking
        current_microsecond = world_time.get("microsecond", 0)

        temporal_enforcement = (
            f"\n**🚨 TEMPORAL CONSISTENCY ENFORCEMENT**\n"
            f"CURRENT STORY STATE: {current_time_str} at {current_location}\n"
            f"HIDDEN TIMESTAMP: microsecond={current_microsecond} (for think-block uniqueness)\n"
            f"⚠️ TIME BOUNDARY: Your response MUST have a timestamp AFTER {current_time_str}\n"
            f"- DO NOT generate events from before this time\n"
            f"- DO NOT jump backward to earlier scenes or locations\n"
            f"- Focus on the LATEST entries in the TIMELINE LOG (not older ones)\n"
            f"- For THINK/PLAN actions: increment microsecond by +1 (no narrative time advancement)\n"
            f"- For STORY actions: increment by meaningful time units (minutes/hours)\n"
            f"- EXCEPTION: Only GOD MODE commands can move time backward\n\n"
        )

        # Build arc completion reminder to prevent LLM from revisiting completed arcs
        arc_reminder = self.build_arc_completion_reminder()

        # CRITICAL FIX (DICE-s8u): Add dice enforcement reminder for code_execution strategy
        # The system prompt loads dice instructions early, but continue_story still ignores them.
        # This reminder is placed LAST in the continuation prompt - closest to where the LLM
        # generates its response - to maximize attention on dice enforcement.
        dice_enforcement = ""
        if dice_roll_strategy_param == dice_strategy.DICE_STRATEGY_CODE_EXECUTION:
            dice_enforcement = (
                "\n**🎲 DICE EXECUTION ENFORCEMENT (MANDATORY)**\n"
                "For ANY dice roll (attack, skill check, saving throw, damage):\n"
                "1. **USE Python code_execution** with `random.randint(1, N)` - NEVER fabricate\n"
                "2. **SHOW the code** in your response (the code block will be inspected)\n"
                "3. **REPORT exact result** from the executed code, not a made-up number\n"
                "⚠️ WARNING: Your code is audited. Fabricated dice = server rejection.\n\n"
            )

        return (
            temporal_enforcement
            + arc_reminder
            + "**CRITICAL REMINDER FOR STORY CONTINUATION**\n"
            "1. **MANDATORY PLANNING BLOCK FIELD**: Every STORY MODE response MUST have a `planning_block` field (JSON object) as a SEPARATE top-level field.\n"
            "2. **MANDATORY NARRATIVE FIELD**: Every response MUST have a `narrative` field with story prose. NEVER embed JSON in narrative.\n"
            "3. **FIELD SEPARATION**: `narrative` = prose text ONLY. `planning_block` = JSON object with thinking/choices. NEVER mix them.\n"
            "4. **Think Commands**: If the user says 'think', 'plan', 'consider', 'strategize', or 'options':\n"
            "   - **NARRATIVE FIELD**: Include brief text showing the character pausing to think (e.g., 'You pause to consider your options...')\n"
            "   - **PLANNING_BLOCK FIELD**: Generate deep think block with 'thinking', 'choices', and 'analysis' (pros/cons/confidence)\n"
            "   - **NO ACTIONS**: The character MUST NOT take any story-advancing actions - no combat, dialogue, movement, or decisions\n"
            "5. **Standard Responses**: Include narrative continuation in `narrative` field, planning block in `planning_block` field with 3-4 action options.\n"
            "6. **Never Skip**: Both `narrative` AND `planning_block` fields are MANDATORY - never leave either empty.\n"
            + dice_enforcement
        )

    def build_faction_continuation_reminder(self) -> str:
        """
        Build reminders for FACTION MODE continuation.
        Enforces mandatory faction header and strict JSON structure.
        """
        return (
            "\n**🚨 FACTION MODE ENFORCEMENT**\n"
            "1. **MANDATORY FACTION HEADER**: Every response MUST include a `faction_header` field with the status line.\n"
            "   - Format: `[FACTION STATUS] Turn X | Rank #Y/201 | FP: Z,ZZZ`\n"
            "   - This is REQUIRED for the user to see their faction state.\n"
            "2. **MANDATORY PLANNING BLOCK**: Every response MUST have a `planning_block` field with `thinking` and `choices`.\n"
            "3. **MANDATORY NARRATIVE**: Every response MUST have a `narrative` field with story prose. NEVER embed JSON in narrative.\n"
            "4. **FIELD SEPARATION**: `narrative` = prose text ONLY. `planning_block` = JSON object. `faction_header` = status string.\n"
            "5. **Turn Updates**: When ending a turn, ensure `state_updates.custom_campaign_state.faction_minigame.turn_number` is incremented.\n\n"
        )

    def build_arc_completion_reminder(self) -> str:
        """
        Build arc completion reminder to prevent LLM from revisiting completed arcs.

        This prevents timeline confusion where the LLM "forgets" that major
        narrative arcs have concluded and tries to revisit them as in-progress.

        Returns:
            Formatted string with completed arcs summary, or empty string if none.
        """
        if self.game_state is None:
            return ""

        summary = self.game_state.get_completed_arcs_summary()
        if not summary:
            return ""

        return (
            f"\n**🚨 ARC COMPLETION ENFORCEMENT**\n"
            f"{summary}\n"
            f"⚠️ DO NOT revisit these arcs as if they are still in progress.\n"
            f"⚠️ DO NOT reset or regress the status of completed arcs.\n"
            f"⚠️ References to these arcs should acknowledge they are COMPLETE.\n\n"
        )

    def build_living_world_instruction(self, turn_number: int) -> str:
        """
        Build living world advancement instruction for this turn.

        Companion quest arcs are PART OF the living world - the instruction file
        provides the mechanical context, while this method adds specific arc
        tracking if available.

        Args:
            turn_number: The current turn number (1-indexed)

        Returns:
            The combined living-world instruction string or empty if no event.
        """
        if turn_number < 1:
            return ""

        logging_util.info(
            "🌍 LIVING_WORLD: Including living world instruction every turn "
            f"(turn={turn_number})"
        )

        base_instruction = _load_instruction_file(constants.PROMPT_TYPE_LIVING_WORLD)

        # Get current companion arc state (if any)
        arc_context = ""
        if hasattr(self.game_state, "get_companion_arcs_summary"):
            arc_summary = self.game_state.get_companion_arcs_summary()
            if arc_summary:
                arc_context = f"\n**Current Companion Arcs:**\n{arc_summary}\n"

        # NOTE: Don't include turn_number in system instruction - it changes every turn
        # and invalidates Gemini's cache. Turn number is already in game state and
        # story history, so LLM has access to it without it being in the header.
        # (feat/optimize-prompt-order-for-caching optimization)
        turn_header = (
            "\n**🌍 LIVING WORLD ADVANCEMENT**\n"
            "Generate background events AND advance companion arcs.\n"
            "Schema requirement this turn: `state_updates.world_events` is REQUIRED.\n"
        )

        return turn_header + arc_context + base_instruction

    def should_include_deferred_rewards(self, turn_number: int) -> bool:
        """
        Check if deferred rewards instruction should be included based on turn number.

        The deferred rewards instruction runs every N scenes (configured via
        constants.DEFERRED_REWARDS_SCENE_INTERVAL, default 10) to catch any
        missed XP/loot awards without double-counting.

        Args:
            turn_number: Current turn number (1-indexed)

        Returns:
            True if deferred rewards instruction should be included this turn
        """
        if turn_number < 1:
            return False
        return turn_number % constants.DEFERRED_REWARDS_SCENE_INTERVAL == 0

    def build_deferred_rewards_instruction(
        self,
        turn_number: int,
        force_include: bool = False,
        force_reason: str | None = None,
    ) -> str:
        """
        Build deferred rewards instruction for this turn.

        This instruction triggers the LLM to scan for missed rewards from
        previous scenes and fill the rewards_box if any were missed.
        Runs in parallel with story mode (same LLM call) on the configured scene interval.

        Args:
            turn_number: Current turn number for context
            force_include: Force building the instruction even if not on interval
            force_reason: Optional override message for forced inclusion context

        Returns:
            Deferred rewards instruction with turn context, or empty string if not
            a deferred rewards turn.
        """
        if not force_include and not self.should_include_deferred_rewards(turn_number):
            return ""

        # Load the deferred rewards instruction file
        base_instruction = _load_instruction_file(
            constants.PROMPT_TYPE_DEFERRED_REWARDS
        )

        # Add turn context header
        reason_line = (
            "Explicit deferred rewards check invoked.\n"
            if force_include and force_reason is None
            else f"{force_reason}\n"
            if force_reason
            else ""
        )
        turn_context = (
            f"\n**🏆 DEFERRED REWARDS CHECK - SCENE {turn_number}**\n"
            f"This is scene {turn_number} - a deferred rewards check turn.\n"
            f"Scan the last {constants.DEFERRED_REWARDS_SCENE_INTERVAL} scenes for any missed XP/loot awards.\n"
            f"{reason_line}"
            f"Fill the rewards_box if rewards were missed, but DO NOT double-count.\n\n"
        )

        return turn_context + base_instruction

    def finalize_instructions(  # noqa: PLR0912
        self, parts: list[str], use_default_world: bool = False
    ) -> str:
        """
        Finalize the system instructions by adding world instructions.
        Returns the complete system instruction string.

        Includes:
        - Character identity block (immutable facts like name, gender, pronouns)
        - God mode directives (player-defined rules that persist across sessions)
        - Campaign setting (custom world lore from god_mode.setting)
        - World instructions (if requested)
        """
        # Add character identity block early (after core instructions)
        # This ensures the LLM always knows immutable character facts
        identity_block = self.build_character_identity_block()
        self._last_identity_block = identity_block  # Store for evidence capture
        if identity_block:
            parts.insert(1, identity_block)  # Insert after first (master directive)

        # Add god mode directives (player-defined rules)
        # These MUST be followed by the LLM
        directives_block = self.build_god_mode_directives_block()
        self._last_directives_block = directives_block  # Store for evidence capture
        if directives_block:
            # Insert after identity block (or after master directive if no identity)
            insert_pos = 2 if identity_block else 1
            parts.insert(insert_pos, directives_block)

        # FIX Bug worktree_logs6-xxx: Add campaign setting (custom world lore)
        # CRITICAL: Must be added to ALL agents (story mode, god mode, etc.)
        # This ensures budget allocation sees the full system instruction size
        if not any(
            part.startswith("# Campaign Setting (Custom World Lore)") for part in parts
        ):
            self._append_campaign_setting_if_present(parts)

        # Add campaign tier-specific prompts (Divine Leverage / Sovereign Protocol)
        # Applies to ALL agents to ensure consistent tier behavior.
        self._append_campaign_tier_prompts(parts)

        # Add world instructions if requested
        if use_default_world:
            _add_world_instructions_to_system(parts)

        # Debug instructions already added at the beginning in build_core_system_instructions

        return "\n\n".join(parts)

    def _resolve_campaign_tier(self) -> str | None:
        if self.game_state is None:
            return None
        if isinstance(self.game_state, dict):
            campaign_tier = self.game_state.get("campaign_tier")
            if campaign_tier:
                return campaign_tier
            custom_state = self.game_state.get("custom_campaign_state")
            if isinstance(custom_state, dict):
                return campaign_divine.get_campaign_tier(custom_state)
            return None
        if hasattr(self.game_state, "get_campaign_tier"):
            return self.game_state.get_campaign_tier()
        return None

    def _append_campaign_tier_prompts(self, parts: list[str]) -> None:
        campaign_tier = self._resolve_campaign_tier()
        if not campaign_tier:
            return

        divine_filename = os.path.basename(constants.DIVINE_SYSTEM_PATH)
        sovereign_filename = os.path.basename(constants.SOVEREIGN_SYSTEM_PATH)

        if campaign_tier == constants.CAMPAIGN_TIER_DIVINE and not any(
            part.startswith(f"# File: {divine_filename}") for part in parts
        ):
            divine_system = _load_instruction_file(constants.PROMPT_TYPE_DIVINE_SYSTEM)
            if divine_system:
                parts.append(divine_system)
                logging_util.debug(
                    "📿 DIVINE_TIER: Including Divine Leverage system prompt"
                )
            else:
                logging_util.warning(
                    "📿 DIVINE_TIER: Divine system prompt missing/empty"
                )
        elif campaign_tier == constants.CAMPAIGN_TIER_SOVEREIGN and not any(
            part.startswith(f"# File: {sovereign_filename}") for part in parts
        ):
            sovereign_system = _load_instruction_file(
                constants.PROMPT_TYPE_SOVEREIGN_SYSTEM
            )
            if sovereign_system:
                parts.append(sovereign_system)
                logging_util.debug(
                    "🌌 SOVEREIGN_TIER: Including Sovereign Protocol system prompt"
                )
            else:
                logging_util.warning(
                    "🌌 SOVEREIGN_TIER: Sovereign system prompt missing/empty"
                )


# =============================================================================
# CENTRALIZED PROMPT BUILDING FUNCTIONS
# =============================================================================
# These functions are centralized here from llm_service.py and world_logic.py
# to ensure all prompt manipulation code lives in one module.


def get_static_prompt_parts(
    current_game_state: GameState, story_context: list[dict[str, Any]]
) -> tuple[str, str, str]:
    """Helper to generate the non-timeline parts of the prompt.

    This builds the checkpoint block, core memories summary, and sequence ID list
    that provide stable context for story continuation.

    Args:
        current_game_state: The current GameState object
        story_context: List of story entries with sequence_id fields

    Returns:
        tuple: (checkpoint_block, core_memories_summary, sequence_id_list_string)
    """
    sequence_ids = [str(entry.get("sequence_id", "N/A")) for entry in story_context]
    sequence_id_list_string = ", ".join(sequence_ids)
    latest_seq_id = sequence_ids[-1] if sequence_ids else "N/A"

    current_location = current_game_state.world_data.get(
        "current_location_name", "Unknown"
    )

    # Handle None player_character_data for uninitialized campaigns.
    pc_data: dict[str, Any] = (
        current_game_state.player_character_data
        if isinstance(current_game_state.player_character_data, dict)
        else {}
    )
    # The key stats are now generated by the LLM in the [CHARACTER_RESOURCES] block.
    active_missions: list[Any] = current_game_state.custom_campaign_state.get(
        "active_missions", []
    )
    if active_missions:
        # Handle both old style (list of strings) and new style (list of dicts)
        mission_names = []
        for m in active_missions:
            if isinstance(m, dict):
                # For dict format, try to get 'name' field, fallback to 'title' or convert to string
                name = m.get("name") or m.get("title") or str(m)
            else:
                # For string format, use as-is
                name = str(m)
            mission_names.append(name)
        missions_summary = "Missions: " + (
            ", ".join(mission_names) if mission_names else "None"
        )
    else:
        missions_summary = "Missions: None"

    ambition: str | None = pc_data.get("core_ambition")
    milestone: str | None = pc_data.get("next_milestone")
    ambition_summary: str = ""
    if ambition and milestone:
        ambition_summary = f"Ambition: {ambition} | Next Milestone: {milestone}"

    all_core_memories: list[str] = current_game_state.custom_campaign_state.get(
        "core_memories", []
    )
    # Apply token budget to prevent memory overflow
    selected_memories = select_memories_by_budget(all_core_memories)
    core_memories_summary: str = format_memories_for_prompt(selected_memories)

    checkpoint_block: str = (
        f"[CHECKPOINT BLOCK:]\\n"
        f"Sequence ID: {latest_seq_id} | Location: {current_location}\\n"
        f"{missions_summary}\\n"
        f"{ambition_summary}"
    )

    return checkpoint_block, core_memories_summary, sequence_id_list_string


def get_current_turn_prompt(user_input: str, mode: str) -> str:
    """Helper to generate the text for the user's current action.

    Uses a consistent prompt template for all character mode inputs.
    This function does not perform keyword detection; it simply formats the
    user's input, and the LLM interprets intent from system instructions
    (game_state_instruction.md) to determine whether to generate standard
    actions or Deep Think planning blocks.

    This approach avoids false positives like "I plan to attack the goblin"
    unintentionally triggering a separate think mode based on naive keyword matching.

    Args:
        user_input: The user's raw input text
        mode: Either "character" or "god" to determine prompt formatting

    Returns:
        str: Formatted prompt text for the current turn
    """
    if mode == constants.MODE_CHARACTER:
        # Standard story continuation - LLM interprets intent from system instructions
        # Planning blocks are handled in JSON output based on LLM's understanding
        prompt_template = (
            "Main character: {user_input}. Continue the story in about {word_count} words and "
            "add details for narrative, descriptions of scenes, character dialog, character emotions."
        )
        return prompt_template.format(
            user_input=user_input, word_count=TARGET_WORD_COUNT
        )
    # god mode (and any non-character mode)
    return f"GOD MODE: {user_input}"


def build_temporal_correction_prompt(
    original_user_input: str,
    old_time: dict[str, Any],
    new_time: dict[str, Any],
    old_location: str | None,
    new_location: str | None,
) -> str:
    """Build correction prompt when temporal violation detected.

    This prompts the LLM to regenerate the ENTIRE response with correct context
    when the story timeline has gone backward (which shouldn't happen).

    Args:
        original_user_input: The original user action that triggered the response
        old_time: The correct current time state (dict with year, month, day, etc.)
        new_time: The invalid time from LLM response that went backward
        old_location: The correct current location
        new_location: The invalid location from LLM response

    Returns:
        str: Formatted correction prompt explaining the violation and how to fix it
    """
    old_time_str = format_world_time_for_prompt(old_time)
    new_time_str = format_world_time_for_prompt(new_time)
    old_loc = old_location or "Unknown location"
    new_loc = new_location or "Unknown location"

    return f"""⚠️ TEMPORAL VIOLATION - FULL REGENERATION REQUIRED

Your previous response was REJECTED because time went BACKWARD:
- CORRECT current state: {old_time_str} at {old_loc}
- YOUR invalid output: {new_time_str} at {new_loc}

🚨 CRITICAL ERROR: You appear to have lost track of the story timeline.

## ROOT CAUSE ANALYSIS
You likely focused on OLDER entries in the TIMELINE LOG instead of the MOST RECENT ones.
This caused you to generate a response for a scene that already happened in the past.

## MANDATORY CORRECTION INSTRUCTIONS

1. **FOCUS ON THE LATEST ENTRIES**: Look at the LAST 2-3 entries in the TIMELINE LOG.
   These represent where the story CURRENTLY is, not where it was earlier.

2. **IDENTIFY THE CURRENT SCENE**: The player is currently at:
   - Time: {old_time_str}
   - Location: {old_loc}
   - This is where you must CONTINUE from.

3. **GENERATE THE NEXT ENTRY**: Your response must continue the story forward.
   - Time MUST be AFTER {old_time_str} (move forward, even if just by minutes)
   - Location should logically follow from {old_loc}
   - Do NOT jump back to earlier scenes or locations

4. **IGNORE YOUR PREVIOUS ATTEMPT**: Your output of "{new_time_str} at {new_loc}" was WRONG.
   Do not use that as a reference.

## PLAYER ACTION TO RESPOND TO:
{original_user_input}

Generate a NEW response that is the NEXT logical entry in the timeline, continuing from the CURRENT state."""


def build_temporal_warning_message(
    temporal_correction_attempts: int,
    max_attempts: int = 3,
) -> str | None:
    """Build user-facing temporal warning text based on attempts taken.

    When temporal corrections are needed, this generates an appropriate
    warning message to inform the user about timeline consistency issues.

    Args:
        temporal_correction_attempts: Number of correction attempts made
        max_attempts: Maximum correction attempts allowed (default 3)

    Returns:
        Warning message string or None if no warning needed
    """
    if temporal_correction_attempts <= 0:
        return None

    # Always surface a warning once at least one correction was attempted.
    # When max_attempts is 0 (corrections disabled), we still emit a warning
    # and treat the effective max as at least one attempt so the message
    # doesn't silently disappear.
    effective_max_attempts = max(1, max_attempts)

    if temporal_correction_attempts > effective_max_attempts:
        return (
            f"⚠️ TEMPORAL CORRECTION EXCEEDED: The AI repeatedly generated responses that jumped "
            f"backward in time. After {temporal_correction_attempts} failed correction attempts "
            f"(configured max {max_attempts}), the system accepted the response "
            f"to avoid infinite loops. Timeline consistency may be compromised."
        )

    return (
        f"⚠️ TEMPORAL CORRECTION: The AI initially generated a response that jumped "
        f"backward in time. {temporal_correction_attempts} correction(s) were required "
        f"to fix the timeline continuity."
    )

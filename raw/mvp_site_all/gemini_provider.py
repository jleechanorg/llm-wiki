"""Gemini provider implementation isolated from llm_service.

Uses response_mime_type="application/json" for JSON format enforcement.
Schema validation is NOT enforced at API level due to SDK limitations with additionalProperties.
See: https://ai.google.dev/gemini-api/docs/structured-output
"""

from __future__ import annotations

import json
import os
import threading
import uuid
from collections import OrderedDict
from contextlib import contextmanager
from datetime import UTC, datetime

# NOTE: Gemini response_schema is NOT used due to SDK client-side validation limitations
#
# CONTEXT (as of Feb 2026):
# - The Gemini API itself SUPPORTS additionalProperties since Nov 2025
#   (see https://ai.google.dev/gemini-api/docs/structured-output)
# - BUT the google-genai Python SDK has stricter client-side validation that rejects it
#   (see https://github.com/googleapis/python-genai/issues/1815 - closed NOT_PLANNED)
#
# OUR CONSTRAINT: Game state has dynamic keys (NPCs, equipment, custom state) which require
# additionalProperties: true. Since the SDK blocks this, we cannot use response_schema.
#
# CURRENT APPROACH: response_mime_type="application/json" + prompt instructions
# Post-response validation in narrative_response_schema.py handles structure enforcement
#
# POTENTIAL WORKAROUNDS (not yet tested):
# 1. Use response_json_schema with manual schema dict (might bypass SDK validation)
# 2. Restructure game state to use List[KeyValuePair] instead of dynamic dicts
# 3. Wait for SDK fix (unlikely based on NOT_PLANNED status)
from typing import Any, Callable

from google import genai
from google.genai import types

from mvp_site import constants, dice_provably_fair, faction_state_util, logging_util
from mvp_site.game_state import (
    execute_tool_requests,
)
from mvp_site.llm_providers import gemini_code_execution
from mvp_site.llm_providers.provider_utils import (
    stringify_prompt_contents,
    strip_tool_requests_dice_instructions,
    update_prompt_contents_with_tool_results,
)
from mvp_site.token_utils import estimate_tokens

try:
    import httpx
except ImportError:  # pragma: no cover - dependency is present in runtime/test envs
    httpx = None

# REV-65v: Dice tool names to filter out in code_execution mode
# These tools should NEVER be exposed as function_declarations when using code_execution
# because dice rolls are handled via Python random.randint() inside code_execution.
_DICE_TOOL_NAMES = frozenset({"roll_dice", "roll_attack", "roll_skill_check", "roll_saving_throw"})
_GEMINI_HTTP_CAPTURE_LOCK = threading.Lock()

# Maximum number of BYOK clients to cache before evicting oldest entries
# This prevents unbounded memory growth in multi-user services
_MAX_BYOK_CLIENTS = 100


# NOTE: Gemini response_schema is NOT used due to SDK client-side validation limitations
#
# CONTEXT (as of Feb 2026):
# - The Gemini API itself SUPPORTS additionalProperties since Nov 2025
#   (see https://ai.google.dev/gemini-api/docs/structured-output)
# - BUT the google-genai Python SDK has stricter client-side validation that rejects it
#   (see https://github.com/googleapis/python-genai/issues/1815 - closed NOT_PLANNED)
#
# OUR CONSTRAINT: Game state has dynamic keys (NPCs, equipment, custom state) which require
# additionalProperties: true. Since the SDK blocks this, we cannot use response_schema.
#
# CURRENT APPROACH: response_mime_type="application/json" + prompt instructions
# Post-response validation in narrative_response_schema.py handles structure enforcement
#
# POTENTIAL WORKAROUNDS (not yet tested):
# 1. Use response_json_schema with manual schema dict (might bypass SDK validation)
# 2. Restructure game state to use List[KeyValuePair] instead of dynamic dicts
# 3. Wait for SDK fix (unlikely based on NOT_PLANNED status)



# Module-level constant for code_execution override instructions
# This is prepended to system instructions when using Gemini 3 code_execution strategy
CODE_EXECUTION_DICE_OVERRIDE = (
    "\n\n## 🎲 CRITICAL: DICE VALUES ARE UNKNOWABLE (Gemini 3 code_execution mode)\n\n"
    "**ABSOLUTE RULE: You CANNOT know dice values without executing code.**\n\n"
    "Dice results are quantum-random. Like checking real-world temperature, you MUST query\n"
    "the random number generator to OBSERVE the value. You cannot predict, estimate, or\n"
    "fabricate dice results - they do not exist until you execute code to generate them.\n\n"
    "Hardcoded dice outputs (e.g., `print('{\"rolls\": [16]}')` without RNG) are rejected.\n\n"
    "### 🚨 ENFORCEMENT WARNING:\n"
    "Your code IS INSPECTED. If `random.randint()` is not found in your executed code,\n"
    "your response WILL BE REJECTED and you will be asked to regenerate. Do not waste\n"
    "inference by fabricating - it will be caught and rejected every time.\n\n"
    "### Required Protocol:\n"
    "1. For ALL dice mechanics (attacks, skill checks, saving throws, damage), use code_execution with Python's random.randint(). Do NOT use tool_requests for dice.\n"
    "2. You MUST output `tool_requests` for FACTION tools when faction_minigame is enabled OR the user_action is "
    "\"enable_faction_minigame\". This is mandatory and will be validated.\n"
    "3. For EVERY dice roll, EXECUTE Python code with the appropriate format:\n\n"
    "**Attack Roll (vs AC):**\n"
    "```python\n"
    "import json, random, time\n"
    "random.seed(time.time_ns())\n"
    "roll = random.randint(1, 20)\n"
    "modifier = 5\n"
    "total = roll + modifier\n"
    "ac = 15  # Target AC\n"
    'print(json.dumps({"notation": "1d20+5", "rolls": [roll], "modifier": modifier, "total": total, "label": "Longsword Attack", "ac": ac, "hit": total >= ac}))\n'
    "```\n\n"
    "**Damage Roll (ONLY if hit):**\n"
    "```python\n"
    "import json, random, time\n"
    "random.seed(time.time_ns())\n"
    "# Roll attack first\n"
    "attack_roll = random.randint(1, 20)\n"
    "attack_mod = 5\n"
    "attack_total = attack_roll + attack_mod\n"
    "ac = 15\n"
    "hit = attack_total >= ac\n"
    "\n"
    "# ONLY roll damage if hit\n"
    "damage_total = 0\n"
    "damage_roll = None\n"
    "if hit:\n"
    "    damage_roll = random.randint(1, 8)\n"
    "    damage_total = damage_roll + 3\n"
    "\n"
    "print(json.dumps({\n"
    "    \"attack\": {\n"
    "        \"notation\": \"1d20+5\",\n"
    "        \"rolls\": [attack_roll],\n"
    "        \"modifier\": attack_mod,\n"
    "        \"total\": attack_total,\n"
    "        \"label\": \"Longsword Attack\",\n"
    "        \"ac\": ac,\n"
    "        \"hit\": hit\n"
    "    },\n"
    "    \"damage\": (\n"
    "        {\"notation\": \"1d8+3\", \"rolls\": [damage_roll], \"modifier\": 3, \"total\": damage_total, \"label\": \"Longsword Damage\"}\n"
    "        if hit else None\n"
    "    )\n"
    "} ))\n"
    "```\n\n"
    "### 🚨 Damage Rule (Critical)\n"
    "- If the attack misses, DO NOT roll damage dice. No RNG calls for damage on a miss.\n"
    "**Skill Check (DC + dc_reasoning REQUIRED):**\n"
    "```python\n"
    "import json, random, time\n"
    "random.seed(time.time_ns())\n"
    "# ⚠️ Set DC and reasoning BEFORE rolling - proves fairness\n"
    "dc = 15\n"
    'dc_reasoning = "guard is alert but area is noisy"  # WHY this DC\n'
    "roll = random.randint(1, 20)  # Roll AFTER DC is set\n"
    "modifier = 3\n"
    "total = roll + modifier\n"
    "success = total >= dc\n"
    'print(json.dumps({"notation": "1d20+3", "rolls": [roll], "modifier": modifier, "total": total, "label": "Stealth", "dc": dc, "dc_reasoning": dc_reasoning, "success": success}))\n'
    "```\n\n"
    "**Saving Throw (DC + dc_reasoning REQUIRED):**\n"
    "```python\n"
    "import json, random, time\n"
    "random.seed(time.time_ns())\n"
    "# ⚠️ Set DC and reasoning BEFORE rolling - proves fairness\n"
    "dc = 15\n"
    'dc_reasoning = "Dragon breath weapon (CR 10, standard DC 15)"  # WHY this DC\n'
    "roll = random.randint(1, 20)  # Roll AFTER DC is set\n"
    "modifier = 4\n"
    "total = roll + modifier\n"
    "success = total >= dc\n"
    'print(json.dumps({"notation": "1d20+4", "rolls": [roll], "modifier": modifier, "total": total, "label": "CON Save", "dc": dc, "dc_reasoning": dc_reasoning, "success": success}))\n'
    "```\n\n"
    "### ⚠️ DC Reasoning is MANDATORY for Skill Checks and Saving Throws\n"
    "The `dc_reasoning` field proves you set the DC BEFORE seeing the roll result.\n"
    "This prevents 'just in time' DC manipulation to fit narratives.\n\n"
)


def uses_code_execution_strategy(model_name: str) -> bool:
    """Check if a model should use Gemini 3 code_execution strategy for dice.

    Args:
        model_name: The Gemini model name

    Returns:
        True if the model should use code_execution for dice rolls
    """
    return "gemini-3" in model_name.lower()



def apply_code_execution_system_instruction(
    system_instruction_text: str | None,
    model_name: str,
    server_seed: str | None = None,
) -> str:
    """Apply code_execution overrides to system instruction if model supports it.

    This function should be called BEFORE creating explicit caches to ensure
    the cached system instruction has the correct code_execution guidance.

    Args:
        system_instruction_text: Original system instruction text
        model_name: Gemini model name to check for code_execution support
        server_seed: Optional 64-char hex server seed for provably fair dice.
            When provided, replaces ``random.seed(time.time_ns())`` in the
            generated instruction so Gemini uses a server-controlled seed.

    Returns:
        Modified system instruction with code_execution overrides if applicable,
        otherwise returns the original text unchanged.
    """
    if not uses_code_execution_strategy(model_name):
        return system_instruction_text or ""

    # Strip tool_requests dice instructions and prepend code_execution override
    cleaned = strip_tool_requests_dice_instructions(system_instruction_text or "").rstrip()
    result = f"{CODE_EXECUTION_DICE_OVERRIDE}\n\n{cleaned}" if cleaned else CODE_EXECUTION_DICE_OVERRIDE.lstrip()

    if server_seed:
        if len(server_seed) != 64 or not all(c in "0123456789abcdefABCDEF" for c in server_seed):
            logging_util.warning(
                f"PROVABLY_FAIR: server_seed must be exactly 64 hex characters; got len={len(server_seed)}. Skipping injection."
            )
        else:
            result = dice_provably_fair.inject_seed_into_prompt(result, server_seed)

    return result


# Timeout for Gemini API requests (10 minutes)
# Aligns with WORLDARCH_TIMEOUT_SECONDS in scripts/shared_config.sh
# and Gunicorn timeout in gunicorn.conf.py
_timeout_str = os.environ.get("WORLDARCH_TIMEOUT_SECONDS", "600")
try:
    GEMINI_REQUEST_TIMEOUT_SECONDS = int(_timeout_str)
except ValueError as exc:
    raise ValueError(
        f"Invalid WORLDARCH_TIMEOUT_SECONDS value {_timeout_str!r}: must be an integer"
    ) from exc

# Convert to milliseconds for HttpOptions.timeout (SDK expects ms, not seconds)
GEMINI_REQUEST_TIMEOUT_MS = GEMINI_REQUEST_TIMEOUT_SECONDS * 1000


def _use_test_stub_client(api_key: str | None = None) -> bool:
    """Whether to use a lightweight test-mode stub client."""
    if os.environ.get("TESTING_AUTH_BYPASS", "").lower() != "true":
        return False
    effective_key = (
        api_key if api_key is not None else os.environ.get("GEMINI_API_KEY", "")
    ).strip()
    if not effective_key:
        return True
    lowered = effective_key.lower()
    return lowered == "test-api-key" or lowered.startswith("test-") or lowered.startswith(
        "dummy-"
    )


def _build_test_response() -> Any:
    """Create a lightweight Gemini-like response for test mode."""

    class _TestResponse:
        def __init__(self) -> None:
            self.text = json.dumps(
                {
                    "narrative": "This is a test-mode Gemini response with simulated dice mechanics.",
                    "session_header": "Scene #Test",
                    "planning_block": {
                        "thinking": "Test stub active. No external call made.",
                        "choices": {
                            "test_choice": {
                                "text": "Continue",
                                "description": "Continue in test mode",
                                "risk_level": "none",
                            }
                        },
                    },
                    "dice_rolls": [],
                    "action_resolution": {
                        "mechanics": {
                            "rolls": [
                                {
                                    "notation": "1d20+5",
                                    "rolls": [15],
                                    "modifier": 5,
                                    "total": 20,
                                    "label": "Test Skill Check",
                                    "dc": 15,
                                    "success": True,
                                }
                            ]
                        }
                    },
                    "resources": "None",
                    "state_updates": {},
                    "world_data": {"world_time": "0000-01-01T00:00:00Z"},
                    "player_character_data": {"name": "Test Player"},
                    "debug_info": {
                        "agent_mode": "test_stub",
                        "code_execution_used": True,
                        "rng_verified": True,
                        "code_contains_rng": True,
                    },
                }
            )
            self.parts = []
            self.candidates = []
            self._tool_results = []
            self._tool_requests_executed = False

    return _TestResponse()


def _get_gemini_http_capture_path() -> str:
    """Return path for Gemini HTTP request/response capture JSONL."""
    return os.getenv("GEMINI_HTTP_REQUEST_RESPONSE_CAPTURE_PATH", "").strip()


def _redact_http_headers(headers: dict[str, str]) -> dict[str, str]:
    """Redact sensitive headers before writing transport captures."""
    redacted: dict[str, str] = {}
    for key, value in headers.items():
        lowered = key.lower()
        if (
            lowered == "authorization"
            or lowered == "cookie"
            or lowered == "set-cookie"
            or "token" in lowered
            or "auth" in lowered
            or "key" in lowered
            or "secret" in lowered
        ):
            redacted[key] = "<redacted>"
        else:
            redacted[key] = value
    return redacted


def _serialize_http_body(body: Any) -> str:
    """Serialize HTTP body into UTF-8 text for JSONL capture."""
    if body is None:
        return ""
    if isinstance(body, bytes):
        return body.decode("utf-8", errors="replace")
    if isinstance(body, str):
        return body
    return str(body)


def _append_gemini_http_capture(payload: dict[str, Any]) -> None:
    """Append a single Gemini transport capture record as JSONL."""
    capture_path = _get_gemini_http_capture_path()
    if not capture_path:
        return
    try:
        with open(capture_path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, default=str))
            handle.write("\n")
    except OSError as e:
        logging_util.warning("Gemini HTTP capture write failed: %s", e)


def _run_with_gemini_http_capture(call: Callable[[], Any]) -> Any:
    """Run a callable while capturing raw Gemini HTTP request/response exchanges."""
    with _gemini_http_capture_context():
        return call()


@contextmanager
def _gemini_http_capture_context() -> Any:
    """Context manager that patches httpx transport for Gemini capture."""
    capture_path = _get_gemini_http_capture_path()
    if not capture_path or httpx is None:
        yield
        return

    original_send = httpx.Client.send

    def _capturing_send(client_self: Any, request: Any, *args: Any, **kwargs: Any) -> Any:
        host = getattr(getattr(request, "url", None), "host", "") or ""
        if not isinstance(host, str) or "googleapis.com" not in host:
            return original_send(client_self, request, *args, **kwargs)

        exchange_id = str(uuid.uuid4())
        request_timestamp = datetime.now(UTC).isoformat()
        request_headers = (
            dict(getattr(request, "headers", {}).items())
            if hasattr(request, "headers")
            else {}
        )
        request_body = _serialize_http_body(getattr(request, "content", b""))
        _append_gemini_http_capture(
            {
                "type": "http_request",
                "exchange_id": exchange_id,
                "timestamp": request_timestamp,
                "method": str(getattr(request, "method", "")),
                "url": str(getattr(request, "url", "")),
                "headers": _redact_http_headers(request_headers),
                "body": request_body,
            }
        )

        try:
            response = original_send(client_self, request, *args, **kwargs)
        except Exception as exc:
            _append_gemini_http_capture(
                {
                    "type": "transport_error",
                    "exchange_id": exchange_id,
                    "timestamp": datetime.now(UTC).isoformat(),
                    "method": str(getattr(request, "method", "")),
                    "url": str(getattr(request, "url", "")),
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            )
            raise

        response_headers = (
            dict(getattr(response, "headers", {}).items())
            if hasattr(response, "headers")
            else {}
        )
        response_body = ""
        is_stream = bool(kwargs.get("stream"))
        if not is_stream:
            try:
                response_body = _serialize_http_body(response.read())
            except Exception as read_error:  # noqa: BLE001
                response_body = f"<failed to read response body: {read_error}>"

        _append_gemini_http_capture(
            {
                "type": "http_response",
                "exchange_id": exchange_id,
                "timestamp": datetime.now(UTC).isoformat(),
                "method": str(getattr(request, "method", "")),
                "url": str(getattr(request, "url", "")),
                "status_code": getattr(response, "status_code", None),
                "headers": _redact_http_headers(response_headers),
                "body": response_body,
                "stream": is_stream,
            }
        )
        return response

    with _GEMINI_HTTP_CAPTURE_LOCK:
        httpx.Client.send = _capturing_send
        try:
            yield
        finally:
            httpx.Client.send = original_send


class _TestTokenCount:
    def __init__(self, total_tokens: int) -> None:
        self.total_tokens = total_tokens


class _TestModels:
    def count_tokens(self, model: str, contents: list[Any]) -> Any:
        text = stringify_prompt_contents(contents)
        approx_tokens = max(1, len(text) // 4)
        return _TestTokenCount(approx_tokens)

    def generate_content(self, *args: Any, **kwargs: Any) -> Any:
        return _build_test_response()


class _TestClient:
    def __init__(self) -> None:
        self.models = _TestModels()

_client: genai.Client | None = None
_byok_clients: OrderedDict[str, genai.Client] = OrderedDict()


def get_client(api_key: str | None = None) -> genai.Client:
    """Initialize and return a singleton Gemini client with timeout configuration.

    The client uses a request timeout configured via GEMINI_REQUEST_TIMEOUT_SECONDS,
    which by default is 600 seconds (10 minutes) but can be overridden through the
    WORLDARCH_TIMEOUT_SECONDS environment variable. This aligns with the system-wide
    timeout configuration used by Gunicorn and Cloud Run.

    Args:
        api_key: Optional API key. If provided, returns a new client instance.
            Otherwise returns the cached singleton client.
    """
    global _client, _byok_clients  # noqa: PLW0603

    # BYOK: If api_key provided, use cached client or create new one
    if api_key is not None:
        if _use_test_stub_client(api_key=api_key):
            logging_util.info(
                "TESTING_AUTH_BYPASS with test API key (BYOK) - using Gemini stub client"
            )
            return _TestClient()
        # Check cache first to avoid creating duplicate clients for same API key
        if api_key in _byok_clients:
            # Move to end (most recently used)
            _byok_clients.move_to_end(api_key)
            return _byok_clients[api_key]
        # Create and cache new client for this API key
        http_options = types.HttpOptions(timeout=GEMINI_REQUEST_TIMEOUT_MS)
        client = genai.Client(api_key=api_key, http_options=http_options)
        # Evict oldest entry if we've hit the cache size limit
        if len(_byok_clients) >= _MAX_BYOK_CLIENTS:
            _byok_clients.popitem(last=False)  # Remove oldest (FIFO)
        _byok_clients[api_key] = client
        return client

    # Normal path: use cached singleton client
    if _client is None:
        if _use_test_stub_client():
            logging_util.info(
                "TESTING_AUTH_BYPASS with test API key - using Gemini stub client"
            )
            _client = _TestClient()
            return _client
        logging_util.info("Initializing Gemini Client")
        env_api_key: str | None = os.environ.get("GEMINI_API_KEY")
        if not env_api_key:
            raise ValueError("CRITICAL: GEMINI_API_KEY environment variable not found!")

        # Configure HTTP options with explicit timeout
        # Without this, httpx uses no read timeout which can cause hung requests
        # NOTE: HttpOptions.timeout expects milliseconds, not seconds
        http_options = types.HttpOptions(timeout=GEMINI_REQUEST_TIMEOUT_MS)

        _client = genai.Client(api_key=env_api_key, http_options=http_options)
        logging_util.info(
            f"Gemini Client initialized with {GEMINI_REQUEST_TIMEOUT_SECONDS}s timeout "
            f"({GEMINI_REQUEST_TIMEOUT_MS}ms)"
        )
    return _client


def clear_cached_client() -> None:
    """Clear the cached client (primarily for tests)."""
    global _client, _byok_clients  # noqa: PLW0603
    _client = None
    _byok_clients.clear()


def count_tokens(model_name: str, contents: list[Any]) -> int:
    """Count tokens for provided content using Gemini's native endpoint."""
    if _use_test_stub_client():
        text = stringify_prompt_contents(contents)
        return max(1, len(text) // 4)
    client = get_client()
    return client.models.count_tokens(model=model_name, contents=contents).total_tokens


def extract_code_execution_evidence(response: Any) -> dict[str, int | bool | str]:
    """Backward-compatible re-export (see llm_providers/gemini_code_execution.py)."""
    return gemini_code_execution.extract_code_execution_evidence(response)


def extract_code_execution_parts_summary(
    response: Any,
    *,
    max_parts: int = 5,
    max_chars: int = 500,
) -> dict[str, Any]:
    """Backward-compatible re-export (see llm_providers/gemini_code_execution.py)."""
    return gemini_code_execution.extract_code_execution_parts_summary(
        response, max_parts=max_parts, max_chars=max_chars
    )


def maybe_log_code_execution_parts(
    response: Any,
    *,
    model_name: str,
    context: str,
) -> None:
    """Backward-compatible wrapper (see llm_providers/gemini_code_execution.py)."""
    gemini_code_execution.log_code_execution_parts(
        response, model_name=model_name, context=context
    )


def generate_json_mode_content(
    prompt_contents: list[Any],
    model_name: str,
    system_instruction_text: str | None,
    temperature: float,
    safety_settings: list[Any],
    json_mode_max_output_tokens: int,
    tools: list[dict] | None = None,
    json_mode: bool = True,
    messages: list[dict] | None = None,
    enable_code_execution: bool | None = None,
    cache_name: str | None = None,
    api_key: str | None = None,
) -> Any:
    """Generate content from Gemini, optionally using tools or JSON mode.

    Note: Code execution is only compatible with JSON mode on Gemini 3.x.
    For other Gemini models, use native two-phase tool calling (Phase 1 tools,
    Phase 2 JSON) to preserve structured output.

    Explicit Caching (always enabled):
    - Caches unchanging story entries separately for 100% cache hit frequency
    - Rebuilds cache every 20 new entries to amortize creation cost
    - Provides 78% cost reduction vs 26% with implicit caching (3x improvement)

    Args:
        prompt_contents: The prompt content to send (if messages not provided)
        model_name: Gemini model name
        system_instruction_text: Optional system instruction
        temperature: Sampling temperature
        safety_settings: Safety settings list
        json_mode_max_output_tokens: Max output tokens
        tools: Optional list of tool definitions
        json_mode: Whether to enforce application/json MIME type
        messages: Optional list of previous messages (for tool loops)
        enable_code_execution: Force-enable/disable code execution tools; defaults
            to capability auto-detection for models in constants.MODELS_WITH_CODE_EXECUTION
        cache_name: Explicit cache reference (when using explicit caching)
        api_key: Optional API key for BYOK

    Returns:
        Gemini API response
    """
    if _use_test_stub_client(api_key=api_key):
        logging_util.info("TESTING_AUTH_BYPASS active - returning Gemini stub response")
        return _build_test_response()
    client = get_client(api_key=api_key)

    generation_config_params = {
        "max_output_tokens": json_mode_max_output_tokens,
        "temperature": temperature,
        "safety_settings": safety_settings,  # Must be inside GenerateContentConfig
    }

    if json_mode:
        generation_config_params["response_mime_type"] = "application/json"

    # Determine whether to attach code_execution
    allow_code_execution = (
        enable_code_execution
        if enable_code_execution is not None
        else model_name in constants.MODELS_WITH_CODE_EXECUTION
    )

    # NOTE: ThinkingConfig + code_execution triggers FAILED_PRECONDITION in Gemini API.
    # Previously enabled thinking_budget=1024 for code_execution compliance, but the
    # combination is incompatible and causes ~60% failure rate. Disabled.
    # See: PR #4534 evidence in docs/evidence/pr_4534_schema_validation/

    # Add tools if provided
    config = types.GenerateContentConfig(**generation_config_params)
    # Constraint: Only Gemini 3.x supports code_execution + JSON mode together.
    if json_mode and model_name not in constants.MODELS_WITH_CODE_EXECUTION:
        allow_code_execution = False

    gemini_tools = []

    # Handle tools conversion for Google GenAI SDK
    # The SDK expects tools as a separate argument or part of config
    if tools:
        for tool in tools:
            fn = tool["function"]
            tool_name = fn["name"]

            # REV-65v: Filter out dice tools in code_execution mode.
            # Dice rolls are handled via Python random.randint() inside code_execution,
            # so we must NOT expose dice tools as function_declarations.
            if allow_code_execution and tool_name in _DICE_TOOL_NAMES:
                logging_util.debug(
                    "Filtering dice tool %s from function_declarations (code_execution mode)",
                    tool_name,
                )
                continue

            gemini_tools.append(
                types.Tool(
                    function_declarations=[
                        types.FunctionDeclaration(
                            name=tool_name,
                            description=fn["description"],
                            parameters=fn.get("parameters"),
                        )
                    ]
                )
            )

    if allow_code_execution:
        gemini_tools.append(types.Tool(code_execution={}))
        logging_util.debug(
            "Code execution enabled for Gemini model %s (json_mode=%s)",
            model_name,
            json_mode,
        )

    # When using cached_content, do NOT set tools, tool_config, or system_instruction
    # in the GenerateContent config - these must be in the CachedContent itself.
    # Gemini API returns 400 INVALID_ARGUMENT if these are set with cached_content.
    if cache_name:
        config.cached_content = cache_name
        logging_util.info(
            f"📦 CACHE_REFERENCE: Using cached_content={cache_name} "
            "(tools/system_instruction disabled - already in cache)"
        )
    else:
        # Only set tools and system_instruction when NOT using cache
        if gemini_tools:
            config.tools = gemini_tools

        if system_instruction_text:
            # Use plain string - all current Gemini SDK versions accept string directly
            config.system_instruction = system_instruction_text

    # If messages are provided, use them (ChatSession style) or convert to contents
    # The Google GenAI SDK generate_content accepts a list of contents.
    # We need to ensure format compatibility.
    contents = []
    if messages:
        # Convert OpenAI-style messages to Gemini Content objects
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            if msg["role"] == "system":
                continue  # Handled in config
            if msg["role"] == "tool":
                # Skip tool responses in history for JSON-mode calls; the tool results
                # are already embedded in prompt_contents for Phase 2.
                continue

            parts = []
            if msg.get("content"):
                parts.append(types.Part(text=msg["content"]))

            # Helper for tool calls/responses would go here
            contents.append(types.Content(role=role, parts=parts))

    else:
        contents = prompt_contents

    # DEBUG: Log detailed request structure before API call
    try:
        # Calculate contents size
        contents_parts: list[str] = []
        if isinstance(contents, list):
            for item in contents:
                if hasattr(item, 'parts'):
                    for part in item.parts:
                        if hasattr(part, 'text') and isinstance(part.text, str):
                            contents_parts.append(part.text)
                elif isinstance(item, str):
                    contents_parts.append(item)
        elif isinstance(contents, str):
            contents_parts.append(contents)

        contents_text = "".join(contents_parts)

        contents_chars = len(contents_text)
        contents_tokens = estimate_tokens(contents_text)
        contents_bytes = len(contents_text.encode('utf-8'))

        # Calculate system instruction size
        system_chars = len(system_instruction_text) if system_instruction_text else 0
        system_tokens = estimate_tokens(system_instruction_text) if system_instruction_text else 0
        system_bytes = len(system_instruction_text.encode('utf-8')) if system_instruction_text else 0

        # Config details
        tools_count = len(config.tools) if hasattr(config, 'tools') and config.tools else 0
        has_code_exec = any(hasattr(t, 'code_execution') for t in (config.tools or [])) if hasattr(config, 'tools') and config.tools else False

        # REV-cdk: Explicit tool payload verification for dice exposure validation
        has_function_declarations = False
        function_declaration_names: list[str] = []
        if hasattr(config, 'tools') and config.tools:
            for tool in config.tools:
                if hasattr(tool, 'function_declarations') and tool.function_declarations:
                    has_function_declarations = True
                    for fd in tool.function_declarations:
                        if hasattr(fd, 'name'):
                            function_declaration_names.append(fd.name)

        # Log explicit tool payload for evidence
        logging_util.info(
            f"🔧 TOOL_PAYLOAD_VERIFICATION: "
            f"function_declarations={has_function_declarations}, "
            f"code_execution={has_code_exec}, "
            f"function_names={function_declaration_names if function_declaration_names else '[]'}"
        )


        total_chars = contents_chars + system_chars
        total_tokens = contents_tokens + system_tokens
        total_bytes = contents_bytes + system_bytes

        logging_util.info(
            f"📊 GEMINI_REQUEST: model={model_name}, "
            f"contents={contents_chars:,}ch/{contents_tokens:,}tk/{contents_bytes:,}b, "
            f"system={system_chars:,}ch/{system_tokens:,}tk/{system_bytes:,}b, "
            f"total={total_chars:,}ch/{total_tokens:,}tk/{total_bytes:,}b, "
            f"tools={tools_count}, code_exec={has_code_exec}, "
            f"max_output={json_mode_max_output_tokens}, temp={temperature}"
        )
    except Exception as log_error:
        logging_util.warning(f"Could not log request details: {log_error}")

    response = _run_with_gemini_http_capture(
        lambda: client.models.generate_content(
            model=model_name,
            contents=contents,
            config=config,
        )
    )

    return response


def _stringify_prompt_contents(prompt_contents: list[Any]) -> str:
    """Backward-compatible wrapper around provider_utils.stringify_prompt_contents."""
    return stringify_prompt_contents(prompt_contents)




def _get_text_from_response(response: Any) -> str:
    """Safely extracts text from a Gemini response object."""
    try:
        # Avoid accessing `response.text` directly; it may emit SDK warnings when
        # non-text parts are present and the SDK returns concatenated text only.
        candidates = getattr(response, "candidates", None) or []
        for candidate in candidates:
            content = getattr(candidate, "content", None)
            if content:
                parts = getattr(content, "parts", None) or []
                text_parts: list[str] = []
                for part in parts:
                    text_value = getattr(part, "text", None)
                    if isinstance(text_value, str) and text_value:
                        text_parts.append(text_value)
                if text_parts:
                    return "".join(text_parts)
    except ValueError as e:
        logging_util.warning(f"ValueError while extracting text: {e}")
    except Exception as e:
        logging_util.error(f"Unexpected error in _get_text_from_response: {e}")

    logging_util.warning(
        f"Response did not contain valid text. Response object: {response}"
    )
    return ""


def _build_gemini_tools(tool_defs: list[dict]) -> list[types.Tool]:
    """Convert tool definitions into Gemini SDK tools."""
    gemini_tools: list[types.Tool] = []
    for tool in tool_defs:
        fn = tool["function"]
        gemini_tools.append(
            types.Tool(
                function_declarations=[
                    types.FunctionDeclaration(
                        name=fn["name"],
                        description=fn["description"],
                        parameters=fn.get("parameters"),
                    )
                ]
            )
        )
    return gemini_tools


def _extract_function_calls(response: Any) -> list[dict[str, Any]]:
    """Extract Gemini function_call parts into tool request dicts.

    Only processes the first candidate to ensure 1:1 mapping with the conversation
    history construction in generate_content_with_native_tools, which only appends
    the first candidate's content. Processing multiple candidates would cause
    'function response parts' mismatch errors (INVALID_ARGUMENT).
    """
    tool_requests: list[dict[str, Any]] = []
    candidates = getattr(response, "candidates", None) or []

    # Only process the first candidate if available
    if candidates:
        candidate = candidates[0]
        content = getattr(candidate, "content", None)
        parts = getattr(content, "parts", None) if content is not None else None
        if parts:
            for part in parts:
                call = getattr(part, "function_call", None)
                if call is None:
                    continue
                name = getattr(call, "name", None)
                args = getattr(call, "args", None)
                if not name:
                    continue
                if isinstance(args, dict):
                    normalized_args = args
                elif isinstance(args, str):
                    try:
                        normalized_args = json.loads(args)
                    except json.JSONDecodeError:
                        normalized_args = {}
                else:
                    normalized_args = {}
                tool_requests.append({"tool": name, "args": normalized_args})
    return tool_requests


def _log_stream_usage_metadata(usage, model_name: str, cache_name: str | None) -> None:
    """Log Gemini usage_metadata from the final streaming chunk."""
    try:
        prompt_tokens = int(getattr(usage, "prompt_token_count", 0) or 0)
        cached_tokens = int(getattr(usage, "cached_content_token_count", 0) or 0)
        response_tokens = int(getattr(usage, "candidates_token_count", 0) or 0)
        cache_hit_rate = (
            (100 * cached_tokens / prompt_tokens) if prompt_tokens > 0 else 0
        )
        logging_util.info(
            "GEMINI_STREAM_USAGE: prompt_tokens=%d, cached_tokens=%d, "
            "response_tokens=%d, cache_hit_rate=%.1f%%, model=%s, cache_name=%s",
            prompt_tokens,
            cached_tokens,
            response_tokens,
            cache_hit_rate,
            model_name,
            cache_name or "none",
        )
    except Exception:
        pass


def generate_content_stream_sync(
    prompt_contents: list[Any],
    model_name: str,
    system_instruction_text: str | None = None,
    temperature: float = 0.7,
    safety_settings: list[Any] | None = None,
    max_output_tokens: int = 4096,
    json_mode: bool = False,
    api_key: str | None = None,
    cache_name: str | None = None,
    response_json_schema: dict[str, Any] | None = None,
):
    """Synchronous streaming from Gemini API.

    Returns a generator that yields text chunks as they are generated.

    Args:
        prompt_contents: The prompt content to send
        model_name: Gemini model name
        system_instruction_text: Optional system instruction
        temperature: Sampling temperature
        safety_settings: Safety settings list
        max_output_tokens: Maximum output tokens
        json_mode: Force JSON MIME type for structured streaming responses
        api_key: Optional API key for BYOK

    Yields:
        str: Text chunks as they are generated
    """
    logging_util.info("STREAM_CLIENT: has_byok_api_key=%s, cache_name=%s", api_key is not None, cache_name)
    client = get_client(api_key=api_key)

    config_params = {
        "max_output_tokens": max_output_tokens,
        "temperature": temperature,
    }

    # Preserve empty lists if explicitly provided.
    if safety_settings is not None:
        config_params["safety_settings"] = safety_settings

    if json_mode:
        config_params["response_mime_type"] = "application/json"
        if response_json_schema is not None:
            config_params["response_json_schema"] = response_json_schema
            logging_util.debug(
                "Streaming response schema requested; passing through while preserving JSON mode."
            )

    config = types.GenerateContentConfig(**config_params)

    # cached_content and system_instruction cannot be set together.
    if cache_name:
        config.cached_content = cache_name
        logging_util.info(
            f"📦 CACHE_REFERENCE: Using cached_content={cache_name} "
            "(streaming system_instruction disabled - already in cache)"
        )
    # Preserve empty string if explicitly provided.
    elif system_instruction_text is not None:
        config.system_instruction = system_instruction_text

    logging_util.info(f"Starting sync streaming generation with model {model_name}")

    models = getattr(client, "models", None)
    stream_method = getattr(models, "generate_content_stream", None)
    if not callable(stream_method):
        logging_util.warning(
            "Streaming method unavailable on Gemini client; falling back to single response generation."
        )
        response = _run_with_gemini_http_capture(
            lambda: client.models.generate_content(
                model=model_name,
                contents=prompt_contents,
                config=config,
            )
        )
        response_text = _get_text_from_response(response)
        if response_text:
            yield response_text
        return

    with _gemini_http_capture_context():
        stream = stream_method(
            model=model_name,
            contents=prompt_contents,
            config=config,
        )

        last_usage_metadata = None
        for chunk in stream:
            # Capture usage_metadata from each chunk (final chunk carries totals).
            if getattr(chunk, "usage_metadata", None) is not None:
                last_usage_metadata = chunk.usage_metadata

            # Handle the known Gemini issue: final chunk may have empty candidates/content/parts.
            candidate = chunk.candidates[0] if getattr(chunk, "candidates", None) else None
            content = getattr(candidate, "content", None) if candidate is not None else None
            parts = getattr(content, "parts", None) if content is not None else None
            if not parts:
                continue
            for part in parts:
                if hasattr(part, "text") and part.text:
                    yield part.text

        # Log usage metadata from the final streaming chunk (mirrors non-streaming GEMINI_USAGE).
        if last_usage_metadata is not None:
            _log_stream_usage_metadata(last_usage_metadata, model_name, cache_name)


def generate_content_with_native_tools(
    prompt_contents: list[Any],
    model_name: str,
    system_instruction_text: str | None,
    temperature: float,
    safety_settings: list[Any],
    json_mode_max_output_tokens: int,
    force_tool_mode: str | None = None,
    cache_name: str | None = None,
    native_tools: list[dict] | None = None,
    api_key: str | None = None,
) -> Any:
    """Run Gemini native two-phase tool calling to preserve JSON output.

    Args:
        force_tool_mode: If "ANY", forces LLM to call at least one tool.
            Default is "AUTO" which gives LLM discretion to skip tools.
            See bead 0kr: "Tool config mode AUTO allows LLM to skip faction tools"
        cache_name: Explicit cache reference (when using explicit caching)
        api_key: Optional API key for BYOK
    """
    client = get_client(api_key=api_key)
    # Use "ANY" mode to force tool calls when specified (e.g., for faction minigame)
    # "AUTO" mode gives LLM discretion and it often skips tools when cached data exists
    tool_calling_mode = force_tool_mode if force_tool_mode else "AUTO"
    if force_tool_mode:
        logging_util.info(f"🔧 TOOL_CONFIG_MODE: Forcing mode={tool_calling_mode} (requested)")
    # When using cached_content, system_instruction, tools, and tool_config
    # must NOT be set in GenerateContentConfig — they are already in the CachedContent.
    # Per Gemini API: "CachedContent can not be used with GenerateContent request setting
    # system_instruction, tools or tool_config"
    if cache_name:
        config = types.GenerateContentConfig(
            max_output_tokens=json_mode_max_output_tokens,
            temperature=temperature,
            safety_settings=safety_settings,
            cached_content=cache_name,
        )
        logging_util.info(
            "📦 NATIVE_TOOLS_CACHE_PHASE1: cache_name present; "
            "system_instruction and tools from cache"
        )
    else:
        config = types.GenerateContentConfig(
            max_output_tokens=json_mode_max_output_tokens,
            temperature=temperature,
            safety_settings=safety_settings,
            tool_config=types.ToolConfig(
                function_calling_config=types.FunctionCallingConfig(mode=tool_calling_mode)
            ),
        )
        # Preserve backward-compatible default tool gating when callers do not
        # provide explicit native_tools.
        all_tools = (
            native_tools
            if native_tools is not None
            else faction_state_util.build_native_tools_for_prompt_contents(prompt_contents)
        )
        gemini_tools = _build_gemini_tools(all_tools)
        if gemini_tools:
            config.tools = gemini_tools
            tool_names = [tool["function"]["name"] for tool in all_tools if "function" in tool and "name" in tool["function"]]
            logging_util.info(
                f"🔧 TOOLS_PASSED_TO_API: {len(gemini_tools)} tool groups, {len(all_tools)} total tools: {tool_names}"
            )
        else:
            logging_util.warning("⚠️ TOOLS_PASSED_TO_API: No tools built - gemini_tools is empty")
        if system_instruction_text:
            config.system_instruction = system_instruction_text

    response_1 = _run_with_gemini_http_capture(
        lambda: client.models.generate_content(
            model=model_name,
            contents=prompt_contents,
            config=config,
        )
    )

    tool_requests = _extract_function_calls(response_1)
    # Log tool invocation results for debugging
    if tool_requests:
        invoked_tools = [tr.get("tool", "unknown") for tr in tool_requests]
        logging_util.info(f"🔧 TOOLS_INVOKED_BY_LLM: {len(tool_requests)} tools called: {invoked_tools}")
    else:
        logging_util.info("🔧 TOOLS_INVOKED_BY_LLM: No tools called by LLM (tools were available but LLM chose not to use them)")

    if tool_requests:
        # Execute tools and build proper conversation history for Phase 2
        tool_results = execute_tool_requests(tool_requests)
        if len(tool_results) != len(tool_requests):
            logging_util.warning(
                "Gemini native tool loop mismatch: tool_requests=%s tool_results=%s; "
                "building function responses from tool_results only to avoid mispairing",
                len(tool_requests),
                len(tool_results),
            )

        updated_prompt_contents = update_prompt_contents_with_tool_results(
            prompt_contents, tool_results
        )

        # Build Phase 2 contents preserving conversation context:
        # 1. Original user message(s)
        # 2. Model's Phase 1 response (with function calls)
        # 3. Function responses for each tool call
        phase2_contents: list[Any] = list(updated_prompt_contents)  # Use updated prompt contents

        # Add model's Phase 1 response (preserves function call context)
        phase1_content = getattr(
            getattr(response_1, "candidates", [None])[0], "content", None
        )
        if phase1_content:
            phase2_contents.append(phase1_content)

        # Add function responses as user content with FunctionResponse parts
        function_response_parts = []
        for tool_req, result in zip(tool_requests, tool_results):
            function_response_parts.append(
                types.Part.from_function_response(
                    name=tool_req["tool"],
                    response={"result": result.get("result", str(result))},
                )
            )
        if function_response_parts:
            phase2_contents.append(
                types.Content(role="user", parts=function_response_parts)
            )

        phase2_prompt_contents = phase2_contents
    else:
        phase2_prompt_contents = prompt_contents

    # Cache provides system_instruction + tools; prompt_contents change between
    # phases but cached_content stays valid. Never disable cache.
    return generate_json_mode_content(
        prompt_contents=phase2_prompt_contents,
        model_name=model_name,
        system_instruction_text=system_instruction_text if cache_name is None else None,
        temperature=temperature,
        safety_settings=safety_settings,
        json_mode_max_output_tokens=json_mode_max_output_tokens,
        api_key=api_key,
        cache_name=cache_name,
    )


def generate_content_with_code_execution(
    prompt_contents: list[Any],
    model_name: str,
    system_instruction_text: str | None,
    temperature: float,
    safety_settings: list[Any],
    json_mode_max_output_tokens: int,
    cache_name: str | None = None,
    api_key: str | None = None,
) -> Any:
    """Generate a SINGLE JSON response using Gemini's code_execution tool.

    Gemini 3.x is the only Gemini family that supports combining:
    - response_mime_type="application/json"
    - built-in tools (code_execution)

    This should be a single inference (one generateContent call). Dice rolls are
    computed inside the model via code_execution, not via server-side tools.

    Args:
        cache_name: Explicit cache reference (when using explicit caching)
        api_key: Optional API key for BYOK
    """
    logging_util.info(
        "Gemini code_execution: Single JSON call (no tool_requests Phase 2)"
    )

    # Generate provably fair server seed and inject appropriately:
    # - With cache: seed goes into prompt_contents (content part), system_instruction
    #   stays static (time.time_ns()) for cache compatibility.
    # - Without cache: seed goes into system_instruction; cache disabled.
    _pf_seed = dice_provably_fair.generate_server_seed()
    logging_util.info(
        logging_util.with_campaign(
            f"PROVABLY_FAIR: commitment={dice_provably_fair.compute_commitment(_pf_seed)}"
        )
    )

    if cache_name:
        # Cache path: seed in prompt_contents, not system_instruction (REV-wvh, REV-lfl).
        # Cached content has its own system instruction; we cannot override it.
        # Prepend a content part so the model uses our seed in its dice code.
        system_instruction_text = apply_code_execution_system_instruction(
            system_instruction_text, model_name, server_seed=None
        )
        seed_override_text = (
            "# PROVABLY_FAIR_SEED_OVERRIDE\n"
            "# For this turn, use the following in ALL dice code instead of random.seed(time.time_ns()):\n"
            "import random\n"
            f"random.seed('{_pf_seed}')\n"
        )
        seed_content = types.Content(
            role="user",
            parts=[types.Part(text=seed_override_text)],
        )
        effective_prompt_contents = [seed_content] + list(prompt_contents)
        effective_cache_name = cache_name
    else:
        # Non-cache path: inject seed into system instruction; cache disabled.
        system_instruction_text = apply_code_execution_system_instruction(
            system_instruction_text, model_name, server_seed=_pf_seed
        )
        effective_prompt_contents = prompt_contents
        effective_cache_name = None

    # Execution-only provider call. Tool orchestration is owned by llm_service.
    _response = generate_json_mode_content(
        prompt_contents=effective_prompt_contents,
        model_name=model_name,
        system_instruction_text=system_instruction_text if effective_cache_name is None else None,
        temperature=temperature,
        safety_settings=safety_settings,
        json_mode_max_output_tokens=json_mode_max_output_tokens,
        enable_code_execution=True,
        cache_name=effective_cache_name,
        api_key=api_key,
    )
    # Attach pre-roll seed so extract_code_execution_evidence can verify the
    # extracted seed against the injected seed (real commitment verification).
    try:
        _response._pre_roll_server_seed = _pf_seed  # noqa: SLF001
    except AttributeError:
        logging_util.warning("PROVABLY_FAIR: response does not support attribute assignment; commitment verification unavailable")
    return _response

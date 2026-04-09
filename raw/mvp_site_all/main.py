from __future__ import annotations

"""
WorldArchitect.AI - Pure API Gateway (MCP Architecture)

This is the main Flask application serving as pure HTTP→MCP translation layer for
WorldArchitect.AI, an AI-powered tabletop RPG platform (digital D&D 5e Game Master).

🎭 PURE API GATEWAY ARCHITECTURE:
- Zero business logic - all game mechanics delegated to MCP server
- HTTP request translation to MCP tool calls
- Response format compatibility for existing frontend
- Authentication & authorization only
- Static file serving for frontend assets

🔌 MCP Integration:
- MCPClient: Communicates with world_logic.py MCP server on localhost:8000
- All /api/* routes call mcp_client.call_tool()
- No direct Firestore, Gemini, or game logic access
- Complete decoupling of web layer from business logic

🚀 Key Routes:
- GET /api/campaigns → get_campaigns_list
- GET /api/campaigns/<id> → get_campaign_state
- POST /api/campaigns → create_campaign
- PATCH /api/campaigns/<id> → update_campaign
- POST /api/campaigns/<id>/interaction → process_action
- GET /api/campaigns/<id>/export → export_campaign
- GET/POST /api/settings → get/update_user_settings

⚡ Dependencies (Minimal):
- Flask: Web framework & routing
- Firebase: Authentication only
- MCP Client: Business logic communication
- CORS: Frontend asset serving

🎯 Frontend Compatibility:
- Identical JSON response formats maintained
- Zero breaking changes for existing UI
- Complete NOOP for end users
"""

# Standard library imports
import argparse
import asyncio
import atexit
import concurrent.futures
import datetime
import functools
import hashlib
import hmac
import importlib
import importlib.util
import ipaddress
import json
import os

# Additional imports for conditional logic (moved from inline to meet import validation)
import re
import secrets
import subprocess
import sys
import threading
import time
import traceback
from collections.abc import Callable, Coroutine
from functools import wraps
from pathlib import Path
from typing import Any

# Firebase imports
import firebase_admin
import requests
from firebase_admin import auth, credentials

# Flask and web imports
from flask import (
    Flask,
    Response,
    g,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    send_file,
    send_from_directory,
    stream_with_context,
    url_for,
)
from flask_compress import Compress
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.middleware.proxy_fix import ProxyFix

from infrastructure.executor_config import (
    configure_asyncio_executor,
    get_blocking_io_executor,
    shutdown_executor,
)

# Infrastructure helpers
from infrastructure.mcp_helpers import create_thread_safe_mcp_getter

# Firestore service imports
from mvp_site import (
    agent_prompts,
    constants,
    equipment_display,
    input_validation,
    intent_classifier,  # Added for local intent classification
    logging_util,
    rate_limiting,
    stats_display,
)
from mvp_site.custom_types import CampaignId, UserId
from mvp_site.game_state import coerce_int
from mvp_site.llm_providers.openai_proxy_provider import (
    INFERENCE_RATE_LIMIT,
    build_openai_error_response,
    build_openclaw_payload,
    invoke_openclaw_gateway,
    invoke_openclaw_gateway_stream,
    parse_chat_completions_payload,
)

# MCP JSON-RPC handler import
from mvp_site.mcp_api import handle_jsonrpc

# MCP client import
from mvp_site.mcp_client import MCPClientError, handle_mcp_errors
from mvp_site.serialization import json_default_serializer
from mvp_site.service_account_loader import get_service_account_credentials
from mvp_site.settings_validation import (
    validate_openclaw_gateway_port,
    validate_openclaw_gateway_token,
    validate_openclaw_gateway_url,
)
from mvp_site.streaming_orchestrator import (
    StreamEvent,
    create_sse_response_headers,
    stream_story_with_game_state,
)
from mvp_site.streaming_orchestrator import (
    warm_lazy_dependencies as warm_streaming_lazy_dependencies,
)

# --- Cold-Start Optimization: Lazy Module Loading ---
# Cloud Run cold-start cost from heavy imports: google.genai (~840ms via world_logic/
# openclaw_provider), google.cloud.firestore (~500ms via firestore_service).
# Using stdlib LazyLoader keeps module references at module level per CLAUDE.md
# conventions while deferring body execution to first request.


def _lazy_module(name: str):
    """Return a lazy module proxy; body executes on first attribute access.

    If the module is already in sys.modules (e.g., test environments that eagerly
    load modules), returns the cached module unchanged.
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


firestore_service = _lazy_module("mvp_site.firestore_service")
openclaw_provider = _lazy_module("mvp_site.llm_providers.openclaw_provider")
world_logic = _lazy_module("mvp_site.world_logic")


def _warm_lazy_module_attribute(
    module_obj: Any, module_label: str, attribute_name: str
) -> bool:
    """Touch lazy-module attribute so module body loads before first request."""
    try:
        getattr(module_obj, attribute_name)
        logging_util.info("Lazy warmup ready: %s.%s", module_label, attribute_name)
        return True
    except Exception:
        logging_util.exception(
            "Lazy warmup failed for %s.%s", module_label, attribute_name
        )
        return False


def _prime_firestore_runtime_warmup() -> None:
    """Prime Firestore runtime in the background to avoid blocking startup."""
    try:
        firestore_service.get_db()
        firestore_service.get_campaigns_for_user(
            DEFAULT_TEST_USER,
            limit=1,
            sort_by="last_played",
            start_after=None,
            include_total_count=False,
        )
        logging_util.info("Lazy warmup ready: main.firestore_runtime_warmup")
    except Exception:
        logging_util.exception(
            "Runtime warmup failed for Firestore client/query priming."
        )


def _start_firestore_runtime_warmup() -> bool:
    """Start Firestore runtime warmup asynchronously; return launch status."""
    try:
        thread = threading.Thread(
            target=_prime_firestore_runtime_warmup,
            name="startup-firestore-warmup",
            daemon=True,
        )
        thread.start()
        logging_util.info(
            "Lazy warmup started: main.firestore_runtime_warmup (background thread)"
        )
        return True
    except Exception:
        logging_util.exception(
            "Runtime warmup dispatch failed for Firestore client/query priming."
        )
        return False


def _warm_startup_lazy_dependencies() -> None:
    """Preload lazy modules to avoid user-facing cold-request import penalties."""
    warmup_status: dict[str, bool] = {
        "main.firestore_service": _warm_lazy_module_attribute(
            firestore_service, "main.firestore_service", "get_campaigns_for_user"
        ),
        "main.openclaw_provider": _warm_lazy_module_attribute(
            openclaw_provider,
            "main.openclaw_provider",
            "test_openclaw_gateway_connection",
        ),
        "main.world_logic": _warm_lazy_module_attribute(
            world_logic, "main.world_logic", "get_campaigns_list_unified"
        ),
    }

    # Prime Firestore client/query off the startup critical path.
    warmup_status["main.firestore_runtime_warmup_dispatched"] = (
        _start_firestore_runtime_warmup()
    )

    semantic_routing_disabled = (
        os.getenv("ENABLE_SEMANTIC_ROUTING", "").strip().lower() == "false"
    )
    if semantic_routing_disabled:
        warmup_status["main.intent_classifier_ready"] = True
        logging_util.info(
            "Lazy warmup skipped: main.intent_classifier_ready (semantic routing disabled)"
        )
    else:
        # Best-effort wait for semantic classifier to finish anchor embedding
        # computation before serving traffic.
        classifier_timeout_raw = os.getenv(
            "INTENT_CLASSIFIER_WARMUP_TIMEOUT_SECONDS", "5.0"
        )
        try:
            classifier_timeout_s = float(classifier_timeout_raw)
        except (TypeError, ValueError):
            classifier_timeout_s = 5.0
            logging_util.warning(
                "Invalid INTENT_CLASSIFIER_WARMUP_TIMEOUT_SECONDS=%r; using default %.1fs",
                classifier_timeout_raw,
                classifier_timeout_s,
            )
        try:
            classifier = intent_classifier.LocalIntentClassifier.get_instance()
            deadline = time.perf_counter() + max(0.0, classifier_timeout_s)
            while time.perf_counter() < deadline:
                if classifier.ready:
                    break
                time.sleep(0.05)
            warmup_status["main.intent_classifier_ready"] = bool(classifier.ready)
            if classifier.ready:
                logging_util.info("Lazy warmup ready: main.intent_classifier_ready")
            else:
                logging_util.warning(
                    "Classifier warmup timeout after %.2fs; first request may finish warmup.",
                    classifier_timeout_s,
                )
        except Exception:
            warmup_status["main.intent_classifier_ready"] = False
            logging_util.exception("Classifier warmup readiness check failed.")

    streaming_status = warm_streaming_lazy_dependencies()
    for module_name, status in streaming_status.items():
        warmup_status[f"streaming.{module_name}"] = status

    failed_modules = [name for name, status in warmup_status.items() if not status]
    if failed_modules:
        logging_util.warning(
            "Lazy warmup incomplete; first-request latency may increase for: %s",
            ", ".join(failed_modules),
        )
    else:
        logging_util.info(
            "Lazy warmup complete for homepage and streaming dependencies."
        )


# Avatar functions imported from firestore_service (accessed via lazy module)
# Usage: firestore_service.upload_user_avatar(...), firestore_service.delete_user_avatar(...)

# NOTE: scripts/ is NOT copied into the Docker image (see Dockerfile).
# Do NOT import from scripts/ here — it will crash in production.
# Cache-busting hash length is defined in mvp_site.constants to avoid scripts/ imports.

# --- CONSTANTS ---
# API Configuration
cors_allow_headers = ["Content-Type", "Authorization", "X-Forwarded-For"]
TESTING_AUTH_BYPASS_MODE = os.getenv("TESTING_AUTH_BYPASS") == "true"
if TESTING_AUTH_BYPASS_MODE:
    # These headers are only honored in TESTING_AUTH_BYPASS mode; do not enable in production.
    cors_allow_headers.extend(
        ["X-Test-Bypass-Auth", "X-Test-User-ID", "X-Test-User-Email"]
    )
# Allow smoke test auth header for preview deployments
if os.getenv("ENVIRONMENT", "").lower() == "preview":
    if "X-Test-Bypass-Auth" not in cors_allow_headers:
        cors_allow_headers.append("X-Test-Bypass-Auth")
    if "X-Test-User-ID" not in cors_allow_headers:
        cors_allow_headers.append("X-Test-User-ID")
    if "X-Test-User-Email" not in cors_allow_headers:
        cors_allow_headers.append("X-Test-User-Email")

CORS_RESOURCES = {
    r"/api/*": {
        "origins": [
            "http://localhost:3000",
            "http://localhost:5000",
            "https://worldarchitect.ai",
        ],
        "methods": ["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
        "allow_headers": cors_allow_headers,
    }
}

ALLOW_TEST_AUTH_BYPASS = (
    os.getenv(
        "ALLOW_TEST_AUTH_BYPASS",
        "true" if TESTING_AUTH_BYPASS_MODE else "false",
    ).lower()
    == "true"
)

# --- VERSIONING ---
# Cache busting now handled at deploy time (not runtime)
# For production: Deploy-time script generates hashed files (app.abc123.js)
# For local dev: Cache busting runs once at server startup via run_local_server.sh

# Cache-control constants
ONE_YEAR_SECONDS = 60 * 60 * 24 * 365
CONTENT_HASH_LENGTH = constants.CACHE_BUST_HASH_LENGTH

# Request Headers
HEADER_AUTH = "Authorization"
HEADER_TEST_BYPASS = "X-Test-Bypass-Auth"
HEADER_TEST_USER_ID = "X-Test-User-ID"
HEADER_TEST_USER_EMAIL = "X-Test-User-Email"
HEADER_SMOKE_TOKEN = "X-MCP-Smoke-Token"
HEADER_MOCK_SERVICES = "X-Mock-Services"
SMOKE_TOKEN_ENV_VAR = "SMOKE_TOKEN"

# Logging Configuration (using centralized logging_util)
# LOG_DIRECTORY moved to logging_util.get_log_directory() for consistency

# Request/Response Data Keys (specific to main.py)
KEY_PROMPT = "prompt"
KEY_SELECTED_PROMPTS = "selected_prompts"
KEY_USER_INPUT = "input"
KEY_CAMPAIGN_ID = "campaign_id"
KEY_SUCCESS = "success"
MASKED_API_KEY_PLACEHOLDER = "********"


# --- Optional HTTP/SSE Capture (local debugging + evidence bundling) ---
def _get_http_capture_path() -> str:
    """Path to append HTTP request/response captures (JSONL) when enabled."""
    return os.getenv("HTTP_REQUEST_RESPONSE_CAPTURE_PATH", "").strip()


def _redact_headers(headers: dict[str, str]) -> dict[str, str]:
    """Redact sensitive headers before writing to evidence logs."""
    redacted: dict[str, str] = {}
    for key, value in headers.items():
        lowered = key.lower()
        if (
            lowered == "authorization"
            or lowered == "cookie"
            or lowered == "set-cookie"
            or "cookie" in lowered
            or "token" in lowered
            or "auth" in lowered
            or "session" in lowered
            or "email" in lowered
            or "user" in lowered
            or lowered.startswith("x-test-")
        ):
            redacted[key] = "<redacted>"
        else:
            redacted[key] = value
    return redacted


def _is_real_mcp_test_mode() -> bool:
    """Return True when MCP tests explicitly request real mode."""
    return os.getenv("MCP_TEST_MODE", "").strip().lower() == "real"


def _is_mock_services_mode() -> bool:
    """Return True when mock services are enabled."""
    return os.getenv("MOCK_SERVICES_MODE", "").strip().lower() == "true"


def _get_mode_violation() -> dict[str, str] | None:
    """Reject invalid MCP_TEST_MODE + MOCK_SERVICES_MODE combinations."""
    if _is_real_mcp_test_mode() and _is_mock_services_mode():
        return {
            KEY_ERROR: (
                "Invalid mode configuration: MCP_TEST_MODE=real "
                "cannot be combined with MOCK_SERVICES_MODE=true."
            )
        }
    return None


def extract_interaction_input(request_data: dict[str, Any]) -> Any:
    """Extract interaction user input with frontend + legacy compatibility."""
    user_input = request_data.get(KEY_USER_INPUT)
    if user_input is not None:
        return user_input
    return request_data.get("user_input")


def _is_local_loopback_remote_addr(remote_addr: str | None) -> bool:
    """Return True when request remote_addr represents a loopback host."""
    if remote_addr is None:
        return False

    normalized = remote_addr.strip().lower()
    if normalized in {"localhost", "127.0.0.1", "::1"}:
        return True

    # Handle IPv4-mapped IPv6 addresses such as ::ffff:127.0.0.1.
    if normalized.startswith("::ffff:"):
        normalized = normalized.split("::ffff:", 1)[1]

    try:
        return ipaddress.ip_address(normalized).is_loopback
    except ValueError:
        return False


def _append_http_capture(payload: dict[str, Any]) -> None:
    """Append a single capture entry as JSONL (best-effort, never breaks requests)."""
    capture_path = _get_http_capture_path()
    if not capture_path:
        return
    try:
        with open(capture_path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, default=json_default_serializer))
            handle.write("\n")
    except OSError as e:
        logging_util.warning("HTTP capture write failed: %s", e)


# Shared async/thread infrastructure reused across app instances
_background_loop: asyncio.AbstractEventLoop | None = None
_loop_thread: threading.Thread | None = None
_blocking_io_executor: concurrent.futures.ThreadPoolExecutor | None = None
_concurrent_request_count = 0
_concurrent_request_lock = threading.Lock()
_async_init_lock = threading.Lock()
_async_shutdown_registered = False
KEY_ERROR = "error"
KEY_MESSAGE = "message"
KEY_CAMPAIGN = "campaign"
KEY_STORY = "story"
KEY_DETAILS = "details"
KEY_RESPONSE = "response"

# Roles & Modes
DEFAULT_TEST_USER = "test-user"

# D&D 5e Spell Level Lookup (for legacy string-based spell data)
# Used to infer spell level when Firestore stores spells as plain strings
SPELL_LEVEL_LOOKUP: dict[str, int] = {
    # Cantrips (Level 0)
    "dancing lights": 0,
    "light": 0,
    "mage hand": 0,
    "mending": 0,
    "message": 0,
    "minor illusion": 0,
    "prestidigitation": 0,
    "vicious mockery": 0,
    "friends": 0,
    "true strike": 0,
    "blade ward": 0,
    "thunderclap": 0,
    # Level 1
    "charm person": 1,
    "comprehend languages": 1,
    "cure wounds": 1,
    "detect magic": 1,
    "disguise self": 1,
    "dissonant whispers": 1,
    "faerie fire": 1,
    "feather fall": 1,
    "healing word": 1,
    "heroism": 1,
    "hideous laughter": 1,
    "tasha's hideous laughter": 1,
    "identify": 1,
    "illusory script": 1,
    "longstrider": 1,
    "silent image": 1,
    "sleep": 1,
    "speak with animals": 1,
    "thunderwave": 1,
    "unseen servant": 1,
    "bane": 1,
    "animal friendship": 1,
    "armor of agathys": 1,
    "hex": 1,
    "hellish rebuke": 1,
    "magic missile": 1,
    "shield": 1,
    "burning hands": 1,
    "chromatic orb": 1,
    "command": 1,
    "inflict wounds": 1,
    "guiding bolt": 1,
    "bless": 1,
    "protection from evil and good": 1,
    "sanctuary": 1,
    # Level 2
    "animal messenger": 2,
    "blindness/deafness": 2,
    "calm emotions": 2,
    "cloud of daggers": 2,
    "crown of madness": 2,
    "detect thoughts": 2,
    "enhance ability": 2,
    "enthrall": 2,
    "heat metal": 2,
    "hold person": 2,
    "invisibility": 2,
    "knock": 2,
    "lesser restoration": 2,
    "locate animals or plants": 2,
    "locate object": 2,
    "magic mouth": 2,
    "phantasmal force": 2,
    "pyrotechnics": 2,
    "see invisibility": 2,
    "shatter": 2,
    "silence": 2,
    "skywrite": 2,
    "suggestion": 2,
    "warding wind": 2,
    "zone of truth": 2,
    "misty step": 2,
    "mirror image": 2,
    "scorching ray": 2,
    "web": 2,
    "spiritual weapon": 2,
    "prayer of healing": 2,
    "aid": 2,
    "darkness": 2,
    "darkvision": 2,
    # Level 3
    "bestow curse": 3,
    "clairvoyance": 3,
    "dispel magic": 3,
    "fear": 3,
    "feign death": 3,
    "glyph of warding": 3,
    "hypnotic pattern": 3,
    "leomund's tiny hut": 3,
    "major image": 3,
    "nondetection": 3,
    "plant growth": 3,
    "sending": 3,
    "speak with dead": 3,
    "speak with plants": 3,
    "stinking cloud": 3,
    "tongues": 3,
    "counterspell": 3,
    "fireball": 3,
    "fly": 3,
    "haste": 3,
    "lightning bolt": 3,
    "slow": 3,
    "revivify": 3,
    "spirit guardians": 3,
    "animate dead": 3,
    "vampiric touch": 3,
    "mass healing word": 3,
    "remove curse": 3,
    "water breathing": 3,
    # Level 4
    "compulsion": 4,
    "confusion": 4,
    "dimension door": 4,
    "freedom of movement": 4,
    "greater invisibility": 4,
    "hallucinatory terrain": 4,
    "locate creature": 4,
    "polymorph": 4,
    "banishment": 4,
    "blight": 4,
    "death ward": 4,
    "fire shield": 4,
    "ice storm": 4,
    "phantasmal killer": 4,
    "stoneskin": 4,
    "wall of fire": 4,
    "fabricate": 4,
    "resilient sphere": 4,
    # Level 5
    "animate objects": 5,
    "awaken": 5,
    "dominate person": 5,
    "dream": 5,
    "geas": 5,
    "greater restoration": 5,
    "hold monster": 5,
    "legend lore": 5,
    "mass cure wounds": 5,
    "mislead": 5,
    "modify memory": 5,
    "planar binding": 5,
    "raise dead": 5,
    "scrying": 5,
    "seeming": 5,
    "teleportation circle": 5,
    "cloudkill": 5,
    "cone of cold": 5,
    "dominate beast": 5,
    "flame strike": 5,
    "wall of force": 5,
    "telekinesis": 5,
    "bigby's hand": 5,
    # Level 6
    "eyebite": 6,
    "find the path": 6,
    "guards and wards": 6,
    "mass suggestion": 6,
    "otto's irresistible dance": 6,
    "irresistible dance": 6,
    "programmed illusion": 6,
    "true seeing": 6,
    "chain lightning": 6,
    "disintegrate": 6,
    "globe of invulnerability": 6,
    "harm": 6,
    "heal": 6,
    "sunbeam": 6,
    "word of recall": 6,
    # Level 7
    "etherealness": 7,
    "forcecage": 7,
    "mirage arcane": 7,
    "mordenkainen's magnificent mansion": 7,
    "mordenkainen's sword": 7,
    "project image": 7,
    "regenerate": 7,
    "resurrection": 7,
    "symbol": 7,
    "teleport": 7,
    "delayed blast fireball": 7,
    "finger of death": 7,
    "fire storm": 7,
    "plane shift": 7,
    "prismatic spray": 7,
    "reverse gravity": 7,
    # Level 8
    "dominate monster": 8,
    "feeblemind": 8,
    "glibness": 8,
    "mind blank": 8,
    "power word stun": 8,
    "antimagic field": 8,
    "clone": 8,
    "control weather": 8,
    "earthquake": 8,
    "incendiary cloud": 8,
    "maze": 8,
    "sunburst": 8,
    # Level 9
    "foresight": 9,
    "power word heal": 9,
    "power word kill": 9,
    "true polymorph": 9,
    "wish": 9,
    "astral projection": 9,
    "gate": 9,
    "meteor swarm": 9,
    "prismatic wall": 9,
    "shapechange": 9,
    "time stop": 9,
    "weird": 9,
}


def get_spell_level(spell_name: str) -> int:
    """Look up spell level from name. Returns 0 (cantrip) if unknown."""
    normalized = spell_name.lower().strip()
    return SPELL_LEVEL_LOOKUP.get(normalized, 0)


# --- END CONSTANTS ---


def setup_file_logging() -> None:
    """
    Configure unified logging for Flask server.

    Uses centralized logging_util.setup_unified_logging() to ensure
    consistent logging across all entry points (Flask, MCP, tests).
    Logs go to both Cloud Logging (stdout/stderr) and local file.
    """
    logging_util.setup_unified_logging("flask-server")


def safe_jsonify(data: Any) -> Response:
    """
    Safely serialize data to JSON, handling Firestore Sentinels and other special objects.

    This function processes the data through json_default_serializer to handle
    Firestore SERVER_TIMESTAMP and DELETE_FIELD sentinels before calling Flask's jsonify.
    """
    # First convert the data using our custom serializer
    json_string = json.dumps(data, default=json_default_serializer)
    # Then parse it back to get clean, serializable data
    clean_data = json.loads(json_string)
    # Finally use Flask's jsonify on the clean data
    return jsonify(clean_data)


def generic_error_response(
    operation: str, status_code: int = 500
) -> tuple[Response, int]:
    """
    Return a generic error response without exposing internal details.

    Args:
        operation: Brief description of what failed (e.g., "create campaign", "authentication")
        status_code: HTTP status code to return

    Returns:
        Tuple of JSON response and status code
    """
    return jsonify(
        {"error": f"Failed to {operation}. Please try again.", "status": "error"}
    ), status_code


def _shutdown_async_resources() -> None:
    """Stop shared background loop and executor gracefully."""

    global _background_loop, _loop_thread, _blocking_io_executor
    loop = _background_loop
    thread = _loop_thread

    if loop and loop.is_running():
        loop.call_soon_threadsafe(loop.stop)
    if thread:
        thread.join(timeout=1)
    # Use centralized shutdown for the shared executor
    shutdown_executor(wait=True)
    _blocking_io_executor = None


def _ensure_async_infrastructure() -> None:
    """Lazily initialize shared event loop and executor once per process.

    Uses centralized executor from infrastructure.executor_config with 100 workers.
    Configures asyncio.to_thread() to use this executor by default.
    """

    global \
        _background_loop, \
        _loop_thread, \
        _blocking_io_executor, \
        _async_shutdown_registered

    with _async_init_lock:
        if _background_loop is None:
            background_loop = asyncio.new_event_loop()

            def _start_loop(loop: asyncio.AbstractEventLoop) -> None:
                asyncio.set_event_loop(loop)
                # Configure the loop to use our centralized 100-thread executor
                # This makes asyncio.to_thread() use our executor automatically
                configure_asyncio_executor(loop)
                loop.run_forever()

            loop_thread = threading.Thread(
                target=_start_loop, args=(background_loop,), daemon=True
            )
            loop_thread.start()

            _background_loop = background_loop
            _loop_thread = loop_thread

        if _blocking_io_executor is None:
            # Use centralized executor from infrastructure (100 workers)
            _blocking_io_executor = get_blocking_io_executor()

        if not _async_shutdown_registered:
            atexit.register(_shutdown_async_resources)
            _async_shutdown_registered = True


async def run_blocking_io(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """
    Run a blocking I/O function in a thread pool executor.

    This prevents blocking database calls (Firestore, etc.) from serializing
    the shared asyncio event loop. Without this, multiple concurrent requests
    would be processed serially instead of in parallel.

    Usage:
        # Instead of: result = firestore_service.get_campaign_by_id(user_id, campaign_id)
        # Use: result = await run_blocking_io(firestore_service.get_campaign_by_id, user_id, campaign_id)

    Performance improvement:
    - Before: N concurrent requests × 100ms each = N×100ms total (serial)
    - After: N concurrent requests × 100ms each = ~100ms total (parallel)

    Args:
        func: The blocking function to call
        *args: Positional arguments for the function
        **kwargs: Keyword arguments for the function

    Returns:
        The result of the blocking function call
    """
    global _concurrent_request_count

    # Track concurrent operations for debugging
    func_name = getattr(func, "__name__", str(func))
    with _concurrent_request_lock:
        _concurrent_request_count += 1
        current_count = _concurrent_request_count

    start_time = datetime.datetime.now()
    logging_util.info(
        f"🔄 PARALLEL I/O START: {func_name} "
        f"[concurrent={current_count}, thread={threading.current_thread().name}]"
    )

    try:
        loop = asyncio.get_running_loop()
        executor = _blocking_io_executor
        if executor is None:
            raise RuntimeError("Blocking I/O executor not initialized")
        if kwargs:
            # functools.partial to handle kwargs
            func_with_kwargs = functools.partial(func, *args, **kwargs)
            result = await loop.run_in_executor(executor, func_with_kwargs)
        else:
            result = await loop.run_in_executor(executor, func, *args)

        duration_ms = (datetime.datetime.now() - start_time).total_seconds() * 1000
        with _concurrent_request_lock:
            _concurrent_request_count -= 1
            remaining = _concurrent_request_count

        logging_util.info(
            f"✅ PARALLEL I/O END: {func_name} "
            f"[duration={duration_ms:.1f}ms, remaining={remaining}]"
        )
        return result

    except Exception as e:
        with _concurrent_request_lock:
            _concurrent_request_count -= 1
        logging_util.error(f"❌ PARALLEL I/O ERROR: {func_name} - {e}")
        raise


async def _load_campaign_page_data(
    user_id: UserId, campaign_id: CampaignId, story_limit: int
) -> tuple[dict[str, Any] | None, dict[str, Any], dict[str, Any], Any]:
    """
    Fetch campaign page data in parallel to reduce latency.

    Returns: (campaign_data, story_result, user_settings, game_state)
    """
    campaign_task = asyncio.create_task(
        run_blocking_io(firestore_service.get_campaign_metadata, user_id, campaign_id)
    )
    story_task = asyncio.create_task(
        run_blocking_io(
            firestore_service.get_story_paginated,
            user_id,
            campaign_id,
            limit=story_limit,
        )
    )
    settings_task = asyncio.create_task(
        run_blocking_io(firestore_service.get_user_settings, user_id)
    )
    game_state_task = asyncio.create_task(
        run_blocking_io(firestore_service.get_campaign_game_state, user_id, campaign_id)
    )

    results = await asyncio.gather(
        campaign_task,
        story_task,
        settings_task,
        game_state_task,
        return_exceptions=True,
    )
    for result in results:
        if isinstance(result, Exception):
            raise result
    campaign_data, story_result, user_settings, game_state = results
    return campaign_data, story_result, user_settings or {}, game_state


AVATAR_CONTENT_TYPES = {
    "image/jpeg": "jpeg",
    "image/png": "png",
    "image/gif": "gif",
    "image/webp": "webp",
}


def _is_webp_image(file_data: bytes) -> bool:
    return (
        len(file_data) >= 12 and file_data[:4] == b"RIFF" and file_data[8:12] == b"WEBP"
    )


def _detect_image_extension(file_data: bytes) -> str | None:
    """Detect image type from magic bytes (replaces deprecated imghdr)."""
    if len(file_data) < 12:
        return None
    if file_data[:3] == b"\xff\xd8\xff":
        return "jpeg"
    if file_data[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    if file_data[:6] in (b"GIF87a", b"GIF89a"):
        return "gif"
    if _is_webp_image(file_data):
        return "webp"
    return None


def _read_stream_with_limit(
    file_stream: Any,
    max_size: int,
    chunk_size: int = 1024 * 1024,
) -> bytes | None:
    total_size = 0
    chunks: list[bytes] = []
    while True:
        chunk = file_stream.read(chunk_size)
        if not chunk:
            break
        total_size += len(chunk)
        if total_size > max_size:
            return None
        chunks.append(chunk)
    return b"".join(chunks)


# --- OpenAI-compatible inference proxy helpers (module-level for testability) ---
def _proxy_gateway_get(url: str, headers: dict[str, str], timeout: int = 8):
    return requests.get(
        url,
        headers=headers,
        timeout=timeout,
        allow_redirects=False,
    )


def create_app() -> Flask:
    """
    Create and configure the Flask application.

    This function initializes the Flask application with all necessary configuration,
    middleware, and route handlers. It sets up CORS, authentication, and all API endpoints.

    Key Configuration:
    - Frontend asset serving from 'frontend_v1' folder (with /static/ redirect compatibility)
    - CORS enabled for all /api/* routes
    - Testing mode configuration from environment
    - Firebase Admin SDK initialization
    - Authentication decorator for protected routes
    - File logging to /tmp/worldarchitect.ai/{branch}/flask-server.log

    Routes Configured:
    - GET /api/campaigns - List user's campaigns
    - GET /api/campaigns/<id> - Get specific campaign
    - POST /api/campaigns - Create new campaign
    - PATCH /api/campaigns/<id> - Update campaign
    - POST /api/campaigns/<id>/interaction - Handle user interactions
    - GET /api/campaigns/<id>/export - Export campaign documents
    - /* - Frontend SPA fallback

    Returns:
        Configured Flask application instance
    """
    global _background_loop, _loop_thread, _blocking_io_executor

    # Ensure shared async infrastructure is initialized before use
    _ensure_async_infrastructure()

    # Set up file logging before creating app
    setup_file_logging()

    # Initialize local intent classifier (async load in background)
    # Set ENABLE_SEMANTIC_ROUTING=false to skip initialization if needed
    disable_classifier = (
        os.environ.get("ENABLE_SEMANTIC_ROUTING", "").lower() == "false"
    )

    if not disable_classifier:
        intent_classifier.initialize()
    else:
        logging_util.info(
            "🔧 SEMANTIC_ROUTING_DISABLED: Skipping classifier initialization (ENABLE_SEMANTIC_ROUTING=false)"
        )

    if not disable_classifier and os.environ.get("TESTING", "").lower() != "true":
        classifier_instance = intent_classifier.LocalIntentClassifier.get_instance()
        startup_timeout_seconds = int(
            os.environ.get("CLASSIFIER_STARTUP_TIMEOUT_SECONDS", "60")
        )
        intent_classifier.check_classifier_startup(
            classifier_instance,
            startup_timeout_seconds=startup_timeout_seconds,
        )

    # Initialize schema documentation cache at startup
    agent_prompts.init_schema_doc_cache()

    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = int(
        os.environ.get("MAX_REQUEST_SIZE_BYTES", str(10 * 1024 * 1024))
    )  # 10MB default (supports 5MB avatars + multipart overhead)

    @app.errorhandler(RequestEntityTooLarge)
    def handle_request_too_large(e):
        return safe_jsonify({"error": "Request too large", "message": str(e)}), 413

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)
    CORS(app, resources=CORS_RESOURCES)

    # Enable gzip compression for all responses (CSS, JS, HTML, JSON)
    # Reduces transfer size by ~75% (405KB → ~100KB for static assets) with gzip.
    app.config["COMPRESS_MIMETYPES"] = [
        "text/html",
        "text/css",
        "text/xml",
        "text/javascript",
        "application/javascript",
        "application/json",
        "application/xml",
        "image/svg+xml",
    ]
    app.config["COMPRESS_MIN_SIZE"] = 500  # Don't compress tiny responses
    # send_from_directory/send_file responses are streamed by default.
    # Enable stream compression so static assets (CSS/JS) get gzip headers.
    app.config["COMPRESS_STREAMS"] = True
    app.config["COMPRESS_ALGORITHM"] = [
        "gzip",
        "br",
        "deflate",
    ]
    # Flask-Compress default streaming algorithms omit gzip. Include it so
    # Accept-Encoding: gzip works for streamed static responses.
    app.config["COMPRESS_ALGORITHM_STREAMING"] = [
        "gzip",
        "br",
        "deflate",
    ]
    Compress(app)

    # Context processor for template variables (e.g., cache busting)
    @app.context_processor
    def inject_app_version() -> dict[str, str]:
        """Inject APP_VERSION into all templates for cache busting."""
        return {"app_version": constants.APP_VERSION}

    def run_in_background_loop(coro: Coroutine[Any, Any, Any]) -> Any:
        if _background_loop is None:
            raise RuntimeError("Background event loop not initialized")
        return asyncio.run_coroutine_threadsafe(coro, _background_loop).result()

    def client_ip() -> str:
        """Extract client IP using ProxyFix-processed remote_addr.

        ProxyFix with x_for=1 already processes X-Forwarded-For securely,
        setting request.remote_addr to the rightmost external IP.
        This prevents IP spoofing attacks on rate limiting.
        """
        return str(get_remote_address())

    # Configure rate limiting
    # NOTE: No default_limits - we only rate limit specific API routes
    # Static files and frontend routes are exempt to prevent CSS/JS loading failures
    limiter = Limiter(
        app=app,
        key_func=client_ip,
        default_limits=[],  # No default limits - only apply to specific routes
        # Use Redis (or any shared backend) in production to avoid per-process buckets.
        storage_uri=os.environ.get("RATE_LIMIT_STORAGE_URI", "memory://"),
    )

    campaign_rate_limit = os.environ.get(
        "CAMPAIGN_RATE_LIMIT", "100 per hour, 20 per minute"
    )
    campaign_create_rate_limit = os.environ.get(
        "CAMPAIGN_CREATE_RATE_LIMIT", campaign_rate_limit
    )
    settings_rate_limit = os.environ.get(
        "SETTINGS_RATE_LIMIT", "100 per hour, 20 per minute"
    )

    # Add security headers
    @app.after_request
    def add_security_headers(response):
        """Add security headers to all responses."""
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        # Each directive omits the trailing semicolon so we can join them once,
        # ensuring consistent "directive; " spacing without duplicated suffixes.
        csp_directives = [
            "default-src 'self'",
            # Inline scripts/styles removed; strict CSP enabled.
            "script-src 'self' https://cdn.jsdelivr.net https://www.gstatic.com https://apis.google.com",
            # Legacy frontend_v1 applies inline style attributes (spinner, animations), so allow unsafe-inline
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net",
            "font-src 'self' https://cdn.jsdelivr.net https://r2cdn.perplexity.ai data:",
            "connect-src 'self' https://identitytoolkit.googleapis.com https://securetoken.googleapis.com https://*.firebaseio.com https://cdn.jsdelivr.net https://www.gstatic.com",
            "img-src 'self' data: https://cdn.jsdelivr.net https://*.googleapis.com https://*.gstatic.com https://images.unsplash.com",
            "frame-src https://worldarchitecture-ai.firebaseapp.com",
            "object-src 'none'",
            "base-uri 'self'",
            "form-action 'self'",
            "frame-ancestors 'none'",
        ]
        response.headers["Content-Security-Policy"] = "; ".join(csp_directives)
        return response

    # Defer MCP client initialization until first use to avoid race condition
    # with command-line argument configuration
    # Use infrastructure helper for thread-safe lazy initialization
    get_mcp_client = create_thread_safe_mcp_getter(app, world_logic_module=world_logic)

    def _is_dev_or_test_mode() -> bool:
        """Return True when running in local dev/test modes."""
        if os.getenv("WORLDAI_DEV_MODE", "").lower() == "true":
            return True
        if os.getenv("TESTING_AUTH_BYPASS", "").lower() == "true":
            return True
        if os.getenv("FLASK_ENV", "").lower() == "development":
            return True
        return False

    def _resolve_frontend_folder() -> str:
        """Resolve the frontend directory, respecting FRONTEND_V1_DIR override."""
        frontend_override = os.getenv("FRONTEND_V1_DIR")
        if frontend_override is not None:
            frontend_override = frontend_override.strip() or None
        if frontend_override is not None:
            frontend_override = os.path.abspath(os.path.expanduser(frontend_override))
            if os.path.isdir(frontend_override):
                return frontend_override
            logging_util.warning(
                "FRONTEND_V1_DIR set but not a directory: %s; using repo frontend_v1",
                frontend_override,
            )
        return os.path.join(os.path.dirname(__file__), "frontend_v1")

    def _strip_content_hash(filename: str) -> str | None:
        """Strip content hash from filename if present (e.g., app.ffe0ba12.js)."""
        path = Path(filename)
        parts = path.name.rsplit(".", 2)
        if len(parts) != 3:
            return None
        name, hash_part, ext = parts
        if len(hash_part) == CONTENT_HASH_LENGTH and all(
            c in "0123456789abcdef" for c in hash_part.lower()
        ):
            return str(path.with_name(f"{name}.{ext}"))
        return None

    def _is_content_hashed_filename(filename: str) -> bool:
        """Return True if filename looks like a content-hashed asset."""
        return _strip_content_hash(filename) is not None

    # Cache busting route for testing - only activates with special header
    @app.route("/frontend_v1/<path:filename>")
    @limiter.exempt  # Exempt static files from rate limiting
    def frontend_files_with_cache_busting(filename):
        """Serve frontend files with cache-aware headers.

        Primary strategy: frontend assets use content-hashed filenames
        (e.g., app.<hash>.js), allowing aggressive long-lived caching.

        This route also supports an optional `v` query parameter for
        legacy/auxiliary cache busting. When `?v=...` is present (or
        the filename is content-hashed), the response is treated as
        versioned and can be cached immutably for a long duration.
        HTML and other unversioned assets receive more conservative
        cache headers to ensure clients pick up new deployments promptly.
        """
        frontend_folder = _resolve_frontend_folder()
        fallback_frontend_folder = os.path.join(
            os.path.dirname(__file__), "frontend_v1"
        )
        is_content_hashed = _is_content_hashed_filename(filename)
        full_path = os.path.join(frontend_folder, filename)
        serve_from_dir = frontend_folder
        if is_content_hashed and not os.path.exists(full_path):
            if _is_dev_or_test_mode():
                # Dev/test mode: fallback to non-hashed version
                fallback_name = _strip_content_hash(filename)
                if fallback_name:
                    fallback_path = os.path.join(frontend_folder, fallback_name)
                    if os.path.exists(fallback_path):
                        filename = fallback_name
                        full_path = fallback_path
                        is_content_hashed = False
            else:
                # Production: log missing hashed asset for observability
                logging_util.warning(
                    "Content-hashed asset not found: %s (cache busting may have failed)",
                    filename,
                )
        elif not os.path.exists(full_path):
            fallback_path = os.path.join(fallback_frontend_folder, filename)
            if os.path.exists(fallback_path):
                full_path = fallback_path
                serve_from_dir = fallback_frontend_folder

        response = send_from_directory(serve_from_dir, filename)
        response.direct_passthrough = False

        # Check if this is a versioned asset (query param OR content-hashed filename)
        version_param = request.args.get("v")

        if version_param is not None or is_content_hashed:
            # Versioned asset: aggressive 1-year cache with immutable flag
            # URL changes when code changes, so cache forever
            response.headers["Cache-Control"] = (
                f"public, max-age={ONE_YEAR_SECONDS}, immutable"
            )
        # Non-versioned: Set cache based on file type
        elif filename.endswith(".html"):
            # HTML: Always revalidate to pick up new version params
            response.headers["Cache-Control"] = "no-cache, must-revalidate"
        elif filename.endswith((".js", ".css")):
            # Unversioned JS/CSS: Short cache to reduce stale code exposure
            response.headers["Cache-Control"] = "public, max-age=300, must-revalidate"
        elif filename.endswith(
            (".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".woff", ".woff2")
        ):
            # Static assets: Moderate cache (1 day)
            response.headers["Cache-Control"] = "public, max-age=86400"

        # Testing override: X-No-Cache header disables all caching
        if request.headers.get("X-No-Cache") is not None:
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"

        return response

    # Backward compatibility route for /static/ paths
    @app.route("/static/<path:filename>")
    @limiter.exempt  # Exempt static redirects from rate limiting
    def static_files_redirect(filename):
        """Redirect old /static/ paths to /frontend_v1/ for backward compatibility"""
        return redirect(
            url_for("frontend_files_with_cache_busting", filename=filename), code=301
        )

    # Testing mode removed - Flask TESTING config no longer set from environment

    # Check if we should use mock services (for testing/CI without credentials)
    # This prevents application startup crash when no Google credentials are present
    mock_mode = os.getenv("MOCK_SERVICES_MODE", "").lower() == "true"

    if mock_mode:
        logging_util.info(
            "🔧 MOCK_SERVICES_MODE: Skipping real Firebase initialization"
        )
    else:
        # Initialize Firebase with explicit project override when provided
        # WORLDAI_* vars take precedence for WorldArchitect.AI repo-specific config
        firebase_project_id = os.getenv("WORLDAI_FIREBASE_PROJECT_ID") or os.getenv(
            "FIREBASE_PROJECT_ID"
        )
        firebase_options = (
            {"projectId": firebase_project_id} if firebase_project_id else {}
        )

        # Check for repo-specific service account credentials
        worldai_creds_path = os.getenv("WORLDAI_GOOGLE_APPLICATION_CREDENTIALS")
        worldai_creds_path = (
            os.path.expanduser(worldai_creds_path) if worldai_creds_path else None
        )

        try:
            firebase_admin.get_app()
        except ValueError:
            if firebase_project_id:
                logging_util.info(
                    f"Initializing Firebase with projectId={firebase_project_id}"
                )

            # Use the service account loader
            try:
                creds_dict = get_service_account_credentials(
                    file_path=worldai_creds_path,
                    fallback_to_env=True,
                    require_env_vars=False,
                )
                logging_util.info("Successfully loaded service account credentials")
                firebase_admin.initialize_app(
                    credentials.Certificate(creds_dict), firebase_options or None
                )
            except Exception as creds_error:
                # Fallback to default credentials (for GCP environments)
                logging_util.warning(
                    f"Failed to load explicit credentials: {creds_error}. "
                    "Attempting default application credentials."
                )
                firebase_admin.initialize_app(
                    credentials.ApplicationDefault(), firebase_options or None
                )

    # Warm lazy dependencies at startup so first user request is not penalized.
    # Run this after Firebase initialization so Firestore warmup uses final app config.
    disable_startup_warmup = (
        os.getenv("DISABLE_STARTUP_WARMUP", "").strip().lower() == "true"
    )
    should_warm_startup = not mock_mode and not disable_startup_warmup
    if should_warm_startup:
        _warm_startup_lazy_dependencies()
    elif mock_mode:
        logging_util.info("Skipping startup lazy warmup (MOCK_SERVICES_MODE=true).")
    else:
        logging_util.info("Skipping startup lazy warmup (DISABLE_STARTUP_WARMUP=true).")

    def check_token(f):
        @wraps(f)
        def wrap(*args: Any, **kwargs: Any) -> Response:
            # Allow local/dev MCP usage without auth (production must require auth)
            # Rationale: Claude Code and other local MCP clients need to call /mcp
            # during development without Firebase auth setup. In this mode, user_id=None
            # so tools will use the client-provided user_id from request arguments.
            # SECURITY: Production deployments MUST set PRODUCTION_MODE=true to enforce auth.
            # NOTE: Only bypass when NO auth credentials supplied. If an Authorization header
            # or test bypass header is present, let normal auth flow handle it so clients
            # get proper user_id injection.
            if (
                request.path == "/mcp"
                and os.getenv("PRODUCTION_MODE", "").lower() != "true"
                and not request.headers.get(HEADER_AUTH)
                and not request.headers.get(HEADER_TEST_BYPASS)
            ):
                kwargs["user_id"] = None
                kwargs["user_email"] = None
                logging_util.info("MCP auth bypass for non-production /mcp (no token)")
                return f(*args, **kwargs)

            # Allow CI smoke tests to authenticate to production preview without exposing
            # production auth tokens. Preview services get SMOKE_TOKEN injected from CI.
            # Paths: /mcp (MCP tool calls) and /api/campaigns/<id>/interaction/stream
            # (streaming contract smoke tests require both to use the same user_id).
            smoke_token = os.getenv(SMOKE_TOKEN_ENV_VAR, "").strip()
            is_production_mode = (
                os.getenv("PRODUCTION_MODE", "").strip().lower() == "true"
            )
            is_preview = os.getenv("ENVIRONMENT", "").strip().lower() == "preview"
            is_stream_route = (
                re.fullmatch(r"/api/campaigns/[^/]+/interaction/stream", request.path)
                is not None
            )
            is_smoke_allowed_path = request.path == "/mcp" or is_stream_route

            if (
                is_smoke_allowed_path
                and smoke_token
                and is_production_mode
                and is_preview
                and hmac.compare_digest(
                    request.headers.get(HEADER_SMOKE_TOKEN, "").strip(), smoke_token
                )
            ):
                kwargs["user_id"] = request.headers.get(
                    HEADER_TEST_USER_ID, "smoke-user"
                )
                kwargs["user_email"] = (
                    request.headers.get(HEADER_TEST_USER_EMAIL, "").strip()
                    or "smoke-test@example.com"
                )
                # Only activate mock LLM when the client explicitly requests it via
                # X-Mock-Services: true. Real-mode smoke tests send SMOKE_TOKEN for
                # auth only; they expect real LLM responses, not mock fallbacks.
                if (
                    request.headers.get(HEADER_MOCK_SERVICES, "").strip().lower()
                    == "true"
                ):
                    g.mock_services_mode = True
                    logging_util.info(
                        "SMOKE_TOKEN auth bypass + mock_services_mode activated for user_id=%s path=%s",
                        kwargs["user_id"],
                        request.path,
                    )
                else:
                    logging_util.info(
                        "SMOKE_TOKEN auth bypass activated (real mode) for user_id=%s path=%s",
                        kwargs["user_id"],
                        request.path,
                    )
                return f(*args, **kwargs)

            # Security hardening: preview environments require SMOKE_TOKEN (handled above).
            # X-Test-Bypass-Auth is rejected on preview; use SMOKE_TOKEN for CI access instead.

            # Allow automated test flows to bypass Firebase verification (TESTING_AUTH_BYPASS mode only).
            # Blocked on preview to enforce SMOKE_TOKEN as the only CI auth path there.
            # Skip this block if query-parameter bypass is being used (checked in next block)
            if (
                request.headers.get(HEADER_TEST_BYPASS, "").lower() == "true"
                and not is_preview
                and (
                    (TESTING_AUTH_BYPASS_MODE and ALLOW_TEST_AUTH_BYPASS)
                    # Flask test_client() runs set app.testing / app.config["TESTING"]=True.
                    # Permit test bypass headers in that context so unittest-style test
                    # modules can be executed directly without pre-setting env vars.
                    or bool(app.config.get("TESTING"))
                )
            ):
                kwargs["user_id"] = request.headers.get(
                    HEADER_TEST_USER_ID, "test-user-123"
                )
                # Test users get exempt email by default for rate limiting
                kwargs["user_email"] = request.headers.get(
                    "X-Test-User-Email", "test@example.com"
                )
                logging_util.info(
                    "TESTING_AUTH_BYPASS auth bypass activated for user_id=%s",
                    kwargs["user_id"],
                )
                return f(*args, **kwargs)

            # URL parameter-based test bypass (used by automated tests and scripts)
            # SECURITY: Require X-Test-Bypass-Auth header to prevent URL-based impersonation
            # Query params alone are too easy to inject via browser navigation or forms
            is_localhost = _is_local_loopback_remote_addr(request.remote_addr)
            if (
                request.headers.get(HEADER_TEST_BYPASS, "").lower() == "true"
                and request.args.get("test_mode", "").lower() == "true"
                and request.args.get("test_user_id")
                and os.getenv("PRODUCTION_MODE", "").lower() != "true"
                and (TESTING_AUTH_BYPASS_MODE and ALLOW_TEST_AUTH_BYPASS)
                and is_localhost
            ):
                kwargs["user_id"] = request.args.get("test_user_id", "test-user-123")
                kwargs["user_email"] = request.args.get(
                    "test_user_email", "test@example.com"
                )
                logging_util.info(
                    "TESTING_AUTH_BYPASS auth bypass activated via query params for user_id=%s",
                    kwargs["user_id"],
                )
                return f(*args, **kwargs)

            # In mock mode without TESTING_AUTH_BYPASS, reject auth attempts
            # (Firebase isn't initialized so verify_id_token would fail anyway)
            # BUT: When TESTING_AUTH_BYPASS=true, allow requests through so tests
            # that patch auth.verify_id_token can still run their patched auth
            if (
                mock_mode
                and not TESTING_AUTH_BYPASS_MODE
                and os.getenv("PRODUCTION_MODE", "").lower() != "true"
                and request.headers.get(HEADER_AUTH)
            ):
                logging_util.warning(
                    "MOCK_SERVICES_MODE: Firebase auth disabled; rejecting token validation"
                )
                return jsonify({KEY_MESSAGE: "Auth unavailable in mock mode"}), 503

            # Authentication uses real Firebase; bypass is only available in TESTING_AUTH_BYPASS mode
            if not request.headers.get(HEADER_AUTH):
                return jsonify({KEY_MESSAGE: "No token provided"}), 401
            try:
                auth_header = request.headers.get(HEADER_AUTH, "")
                parts = auth_header.split()
                if len(parts) != 2 or parts[0].lower() != "bearer":
                    raise ValueError("Invalid authorization scheme")
                id_token = parts[1].strip()
                if not id_token:
                    raise ValueError("Empty token")

                # Personal API key auth — prefix "worldai_" distinguishes from Firebase JWTs
                if id_token.startswith("worldai_"):
                    key_hash = hashlib.sha256(id_token.encode()).hexdigest()
                    uid, user_email = firestore_service.lookup_personal_api_key(
                        key_hash
                    )
                    if not uid:
                        return jsonify({KEY_MESSAGE: "Invalid API key"}), 401
                    kwargs["user_id"] = uid
                    kwargs["user_email"] = user_email
                    return f(*args, **kwargs)

                # Firebase token verification using Admin SDK
                # When clock skew patch is active (local clock ahead), we need to:
                # 1. Use actual time for verification (tokens issued at Google's actual time)
                # 2. Disable check_revoked (requires backend call which would fail)
                from mvp_site.clock_skew_credentials import (
                    UseActualTime,
                    get_clock_skew_seconds,
                )

                clock_skew = get_clock_skew_seconds()

                try:
                    # When clock skew > 60s, use actual time and disable revocation check
                    if clock_skew > 60:
                        with UseActualTime():
                            decoded_token = auth.verify_id_token(
                                id_token,
                                check_revoked=False,
                                clock_skew_seconds=60,
                            )
                    else:
                        decoded_token = auth.verify_id_token(
                            id_token,
                            check_revoked=True,
                            clock_skew_seconds=60,
                        )
                except Exception:
                    # Only Firebase-verified tokens or UseActualTime() tokens are accepted.
                    # Decoding the JWT payload without signature verification is a P0 security
                    # issue — an attacker could forge any user_id with a valid exp claim.
                    raise
                kwargs["user_id"] = decoded_token["uid"]
                # Pass user email for rate limiting checks
                kwargs["user_email"] = decoded_token.get("email")
            except Exception as e:
                error_message = str(e)
                logging_util.error(f"Auth failed: {e}")
                # Do not log tokens or Authorization headers
                logging_util.error(traceback.format_exc())

                # Generic error response - don't expose internal error details
                response_data = {
                    KEY_SUCCESS: False,
                    KEY_ERROR: "Authentication failed",
                }

                # Add clock skew guidance for specific errors
                if (
                    "Token used too early" in error_message
                    or "clock" in error_message.lower()
                ):
                    response_data["error_type"] = "clock_skew"
                    response_data["server_time_ms"] = int(
                        datetime.datetime.now(datetime.UTC).timestamp() * 1000
                    )
                    response_data["hint"] = (
                        "Clock synchronization issue detected. The client and server clocks may be out of sync."
                    )
                return jsonify(response_data), 401
            return f(*args, **kwargs)

        return wrap

    def async_route(f):
        """Decorator to handle async Flask routes with proper event loop management"""

        @wraps(f)
        def wrapper(*args, **kwargs):
            if asyncio.iscoroutinefunction(f):
                return run_in_background_loop(f(*args, **kwargs))
            return f(*args, **kwargs)

        return wrapper

    # --- OpenAI-Compatible Inference Proxy Routes ---
    # Forward external /v1/chat/completions calls to the authenticated user's OpenClaw gateway.
    # Auth: worldai_ personal API keys (same as /mcp — no new auth layer needed).
    # URL: user's gateway_url from Firestore settings; token from their gateway_token field.

    @app.route("/v1/models", methods=["GET"])
    @limiter.limit(INFERENCE_RATE_LIMIT)
    @check_token
    def openai_list_models(
        user_id: UserId, user_email: str | None = None
    ) -> tuple[Any, int] | tuple[dict[str, Any], int]:
        """OpenAI-compatible /v1/models endpoint.

        Returns the list of models the authenticated user can access via their gateway.
        The model list is determined by what their gateway reports at /v1/models.
        """
        del user_email
        try:
            user_settings = firestore_service.get_user_settings(user_id)
            if not isinstance(user_settings, dict):
                return {
                    "error": {
                        "message": "No settings found",
                        "type": "invalid_request_error",
                    }
                }, 400

            raw_url = user_settings.get("openclaw_gateway_url", "")
            raw_token = user_settings.get("openclaw_gateway_token", "")
            if not raw_url:
                return {
                    "error": {
                        "message": "No gateway URL configured",
                        "type": "invalid_request_error",
                    }
                }, 400

            url, url_err = validate_openclaw_gateway_url(raw_url)
            if url_err:
                return {
                    "error": {
                        "message": f"Invalid gateway URL: {url_err}",
                        "type": "invalid_request_error",
                    }
                }, 400
            if url is None:
                return {
                    "error": {
                        "message": "No gateway URL configured",
                        "type": "invalid_request_error",
                    }
                }, 400

            headers = {"Content-Type": "application/json"}
            if raw_token:
                headers["Authorization"] = f"Bearer {raw_token}"

            try:
                resp = _proxy_gateway_get(f"{url}/v1/models", headers=headers)
                if resp.is_redirect or resp.history:
                    logging_util.error(
                        "openai_list_models: gateway redirect forbidden url=%s",
                        url,
                    )
                    return {
                        "error": {
                            "message": "Gateway returned redirect",
                            "type": "gateway_error",
                        }
                    }, 502

                status_code = resp.status_code
                if 200 <= status_code < 300:
                    try:
                        return resp.json(), 200
                    except ValueError as exc:
                        logging_util.error(
                            "openai_list_models: invalid JSON from gateway: %s", exc
                        )
                        return {
                            "error": {
                                "message": "Invalid JSON from gateway response",
                                "type": "gateway_error",
                            }
                        }, 502

                if status_code >= 400:
                    try:
                        data = resp.json()
                    except ValueError:
                        data = None

                    if isinstance(data, dict) and "error" in data:
                        return data, status_code

                    text = getattr(resp, "text", "") or ""
                    logging_util.error(
                        "openai_list_models: gateway HTTP %s: %s",
                        status_code,
                        text[:500],
                    )
                    return {
                        "error": {
                            "message": f"Gateway HTTP {status_code}: {text[:500]}",
                            "type": "gateway_error",
                        }
                    }, status_code

                logging_util.error(
                    "openai_list_models: unexpected gateway response status=%s",
                    status_code,
                )
                return {
                    "error": {
                        "message": "Unexpected gateway response",
                        "type": "gateway_error",
                    }
                }, 502
            except requests.exceptions.RequestException as exc:
                logging_util.error("openai_list_models: gateway error: %s", exc)
                return {
                    "error": {"message": "Gateway unreachable", "type": "gateway_error"}
                }, 502

        except Exception as e:
            logging_util.error("openai_list_models: unexpected error: %s", e)
            return {
                "error": {"message": "Internal server error", "type": "internal_error"}
            }, 500

    @app.route("/v1/chat/completions", methods=["POST"])
    @limiter.limit(INFERENCE_RATE_LIMIT)
    @check_token
    def openai_chat_completions(user_id: UserId, user_email: str | None = None) -> Any:
        """OpenAI-compatible /v1/chat/completions proxy.

        Authenticates the caller via worldai_ personal API key, resolves their
        OpenClaw gateway URL from Firestore settings, and forwards the request.
        Returns responses in OpenAI-compatible format (non-streaming JSON or streaming SSE).
        """
        try:
            user_settings = firestore_service.get_user_settings(user_id)
            if not isinstance(user_settings, dict):
                return jsonify(build_openai_error_response("No settings found")), 400

            raw_url = user_settings.get("openclaw_gateway_url", "")
            raw_token = user_settings.get("openclaw_gateway_token", "")
            if not raw_url:
                return jsonify(
                    build_openai_error_response(
                        "No gateway URL configured. Set openclaw_gateway_url in your settings."
                    )
                ), 400

            url, url_err = validate_openclaw_gateway_url(raw_url)
            if url_err:
                return jsonify(
                    build_openai_error_response(f"Invalid gateway URL: {url_err}")
                ), 400
            if url is None:
                return jsonify(
                    build_openai_error_response(
                        "No gateway URL configured. Set openclaw_gateway_url in your settings."
                    )
                ), 400

            try:
                data = request.get_json(force=True)
            except Exception:
                return jsonify(build_openai_error_response("Invalid JSON body")), 400

            try:
                payload = parse_chat_completions_payload(data)
            except ValueError as ve:
                return jsonify(build_openai_error_response(str(ve))), 400

            openclaw_payload = build_openclaw_payload(payload)

            if payload.stream:
                return _openai_stream_response(
                    url, raw_token if raw_token else None, openclaw_payload
                )
            result = invoke_openclaw_gateway(
                gateway_url=url,
                gateway_token=raw_token if raw_token else None,
                payload=openclaw_payload,
            )
            flask_response, status = result.to_flask_response()
            return jsonify(flask_response), status

        except Exception as e:
            logging_util.error("openai_chat_completions: unexpected error: %s", e)
            return jsonify(
                build_openai_error_response(
                    "Internal server error",
                    code="internal_error",
                    error_type="internal_error",
                )
            ), 500

    def _openai_stream_response(
        gateway_url: str,
        gateway_token: str | None,
        openclaw_payload: dict[str, Any],
    ) -> Response:
        """Streaming handler — yields SSE lines from the gateway as OpenAI stream chunks."""

        def generate():
            for is_done, line in invoke_openclaw_gateway_stream(
                gateway_url=gateway_url,
                gateway_token=gateway_token,
                payload=openclaw_payload,
            ):
                if is_done:
                    return
                yield line

        return Response(
            stream_with_context(generate()),
            mimetype="text/event-stream",
            headers={
                **create_sse_response_headers(),
                # Extra buffering headers for proxies
                "X-Accel-Buffering": "no",
            },
        )

    # --- API Routes ---
    @app.route("/api/campaigns", methods=["GET"])
    @limiter.limit(campaign_rate_limit)
    @check_token
    @async_route
    async def get_campaigns(
        user_id: UserId, user_email: str | None = None
    ) -> Response | tuple[Response, int]:
        try:
            # Get query parameters with proper validation
            limit = request.args.get("limit")
            if limit is not None:
                try:
                    limit = int(limit)
                    if limit < 1 or limit > 100:
                        return jsonify(
                            {
                                "error": "Invalid limit parameter. Must be between 1 and 100."
                            }
                        ), 400
                except ValueError:
                    return jsonify(
                        {"error": "Invalid limit parameter. Must be a number."}
                    ), 400
            else:
                # Default limit of 50 for pagination (display full campaigns list)
                limit = 50

            sort_by = request.args.get("sort_by")
            # Whitelist allowed sort fields for security
            allowed_sort_fields = ["created_at", "last_played", "title"]
            if sort_by is not None and sort_by not in allowed_sort_fields:
                return jsonify(
                    {
                        "error": f"Invalid sort_by parameter. Must be one of: {', '.join(allowed_sort_fields)}"
                    }
                ), 400

            # Get pagination cursor
            start_after = None
            if request.args.get("start_after_timestamp") and request.args.get(
                "start_after_id"
            ):
                start_after = {
                    "timestamp": request.args.get("start_after_timestamp"),
                    "id": request.args.get("start_after_id"),
                }

            data = {
                "user_id": user_id,
                "limit": limit,
                "sort_by": sort_by,
                "start_after": start_after,
            }
            result = await get_mcp_client().call_tool("get_campaigns_list", data)

            # Determine if we should return paginated format or legacy array
            # If start_after is provided, it's definitely a paginated request
            # If paginate=true is provided, it's an explicit opt-in
            is_paginated_request = (
                request.args.get("start_after_timestamp") is not None
                or request.args.get("start_after_id") is not None
                or request.args.get("paginate") == "true"
            )

            # Maintain backward compatibility: return campaigns array directly
            # Legacy format: [campaigns...]
            # New MCP format: {"campaigns": [...], "success": true, "has_more": bool, "next_cursor": {...}}
            if isinstance(result, dict) and "campaigns" in result:
                if is_paginated_request:
                    # Return format with pagination info
                    response_data = {
                        "campaigns": result["campaigns"],
                    }
                    # Include pagination metadata if available
                    if "has_more" in result:
                        response_data["has_more"] = result["has_more"]
                    if "next_cursor" in result:
                        response_data["next_cursor"] = result["next_cursor"]
                    if "total_count" in result:
                        response_data["total_count"] = result["total_count"]
                    return jsonify(response_data)
                # Return legacy format (array directly) for backward compatibility
                return jsonify(result["campaigns"])

            # Fallback if format is unexpected
            status_code = (
                result.get("status_code", 200) if isinstance(result, dict) else 200
            )
            return safe_jsonify(result), status_code
        except MCPClientError as e:
            return handle_mcp_errors(e)
        except Exception as e:
            logging_util.error(f"Get campaigns error: {e}")
            logging_util.error(traceback.format_exc())
            return jsonify(
                {
                    KEY_SUCCESS: False,
                    KEY_ERROR: "Failed to retrieve campaigns",
                }
            ), 500

    @app.route("/api/campaigns/<campaign_id>", methods=["GET"])
    @limiter.limit(campaign_rate_limit)
    @check_token
    @async_route
    async def get_campaign(
        user_id: UserId, campaign_id: CampaignId, user_email: str | None = None
    ) -> Response | tuple[Response, int]:
        # Validate campaign_id format
        if not input_validation.validate_campaign_id(campaign_id):
            return jsonify({"error": "Invalid campaign ID format"}), 400

        try:
            # Parse pagination params from query string
            story_limit = request.args.get("story_limit", 300, type=int)
            story_limit = min(max(story_limit, 10), 500)  # Clamp between 10-500

            logging_util.info(
                f"🎮 LOADING GAME PAGE: user={user_id}, campaign={campaign_id}, "
                f"story_limit={story_limit}"
            )

            # OPTIMIZED: Fetch campaign data in parallel to reduce latency
            # This avoids loading all 30MB+ of story into memory for large campaigns
            (
                campaign_data,
                story_result,
                user_settings,
                game_state,
            ) = await _load_campaign_page_data(
                user_id=user_id,
                campaign_id=campaign_id,
                story_limit=story_limit,
            )
            if not campaign_data:
                return jsonify({"error": "Campaign not found"}), 404

            story = story_result.get("entries", [])

            debug_mode = bool(user_settings.get("debug_mode", False))

            if game_state:
                game_state.debug_mode = debug_mode

            # Process story entries based on debug mode
            if debug_mode:
                processed_story = story or []
            else:
                # Strip debug fields when debug mode is off
                processed_story = world_logic._strip_game_state_fields(story or [])

            # Reload resilience: if latest story entry lacks per-turn living-world
            # payload but cumulative living-world state exists in game_state,
            # inject fallback payload so debug UI remains visible after refresh.
            processed_story = world_logic.inject_persisted_living_world_fallback(
                processed_story,
                game_state.to_dict() if game_state is not None else None,
                debug_mode,
            )

            # Debug logging with size diagnostics to identify bloat
            total_story_size = sum(
                len(json.dumps(e, default=str)) for e in processed_story
            )
            avg_entry_size = (
                total_story_size // len(processed_story) if processed_story else 0
            )
            logging_util.info(
                f"Campaign {campaign_id} story: {len(processed_story)} entries, "
                f"total={total_story_size / 1024:.1f}KB, avg={avg_entry_size / 1024:.1f}KB/entry"
            )
            # Log size breakdown for first 3 AI entries to identify bloat sources
            for i, entry in enumerate(processed_story[:3]):
                if entry.get("actor") == constants.ACTOR_GEMINI:
                    size_breakdown = {
                        k: len(json.dumps(v, default=str))
                        for k, v in entry.items()
                        if k not in ["actor", "mode", "timestamp"]
                    }
                    top_fields = sorted(size_breakdown.items(), key=lambda x: -x[1])[:5]
                    logging_util.info(
                        f"Entry {i} size breakdown (top 5): "
                        + ", ".join(f"{k}={v / 1024:.1f}KB" for k, v in top_fields)
                    )

            # Map to original response format with pagination metadata
            response_data = {
                KEY_CAMPAIGN: campaign_data,
                KEY_STORY: processed_story,
                "game_state": game_state.to_dict() if game_state is not None else {},
                # Pagination metadata for frontend "load older" functionality
                "story_pagination": {
                    "total_count": story_result.get(
                        "total_count", len(processed_story)
                    ),
                    "fetched_count": story_result.get(
                        "fetched_count", len(processed_story)
                    ),
                    "has_older": story_result.get("has_older", False),
                    "oldest_timestamp": story_result.get("oldest_timestamp"),
                    "oldest_id": story_result.get("oldest_id"),
                },
            }

            # Enhanced debug logging
            logging_util.info(f"🎯 BACKEND RESPONSE for campaign {campaign_id}:")
            logging_util.info(
                f"  Campaign Title: '{campaign_data.get('title', 'NO_TITLE')}'"
            )
            logging_util.info(f"  Story entries: {len(processed_story)}")
            logging_util.info(
                f"  Pagination: {story_result.get('fetched_count')}/{story_result.get('total_count')} "
                f"(has_older={story_result.get('has_older')})"
            )

            return jsonify(response_data)
        except MCPClientError as e:
            return handle_mcp_errors(e)
        except Exception as e:
            logging_util.error(f"Get campaign error: {e}")
            logging_util.error(traceback.format_exc())
            return jsonify(
                {
                    KEY_SUCCESS: False,
                    KEY_ERROR: "Failed to retrieve campaign",
                }
            ), 500

    @app.route("/api/campaigns/<campaign_id>/story", methods=["GET"])
    @limiter.limit(campaign_rate_limit)
    @check_token
    @async_route
    async def get_story_paginated(
        user_id: UserId, campaign_id: CampaignId, user_email: str | None = None
    ) -> Response | tuple[Response, int]:
        """
        Paginated story endpoint for loading older entries.

        Query params:
            limit: Number of entries to return (default 100, max 500)
            before: ISO timestamp to fetch entries before (for pagination)

        Returns:
            {
                story: [...entries...],
                pagination: {total_count, fetched_count, has_older, oldest_timestamp}
            }
        """
        try:
            limit = request.args.get("limit", 100, type=int)
            limit = min(max(limit, 1), 500)  # Clamp between 1-500
            before_timestamp = request.args.get("before")
            before_id = request.args.get("before_id")
            newer_count = max(request.args.get("newer_count", 0, type=int) or 0, 0)
            newer_gemini_count = max(
                request.args.get("newer_gemini_count", 0, type=int) or 0,
                0,
            )

            if before_timestamp:
                try:
                    datetime.datetime.fromisoformat(
                        before_timestamp.replace("Z", "+00:00")
                    )
                except (ValueError, TypeError):
                    return jsonify(
                        {
                            KEY_ERROR: "Invalid 'before' timestamp; expected ISO-8601 string"
                        }
                    ), 400

            # Ensure campaign exists (mirror GET /api/campaigns/<id>)
            campaign_meta = await run_blocking_io(
                firestore_service.get_campaign_metadata, user_id, campaign_id
            )
            if not campaign_meta:
                return jsonify(
                    {KEY_SUCCESS: False, KEY_ERROR: "Campaign not found"}
                ), 404

            logging_util.info(
                f"📖 STORY PAGINATION: campaign={campaign_id}, limit={limit}, "
                f"before={before_timestamp}"
            )

            # Get paginated story entries
            story_result = await run_blocking_io(
                firestore_service.get_story_paginated,
                user_id,
                campaign_id,
                limit=limit,
                before_timestamp=before_timestamp,
                before_id=before_id,
                newer_count=newer_count,
                newer_gemini_count=newer_gemini_count,
            )
            story = story_result.get("entries", [])

            # Get user settings for debug mode
            user_settings = (
                await run_blocking_io(firestore_service.get_user_settings, user_id)
                or {}
            )
            debug_mode = bool(user_settings.get("debug_mode", False))

            # Process story entries based on debug mode
            if not debug_mode:
                story = world_logic._strip_game_state_fields(story)

            response_data = {
                KEY_STORY: story,
                "pagination": {
                    "total_count": story_result.get("total_count", len(story)),
                    "fetched_count": story_result.get("fetched_count", len(story)),
                    "has_older": story_result.get("has_older", False),
                    "oldest_timestamp": story_result.get("oldest_timestamp"),
                    "oldest_id": story_result.get("oldest_id"),
                },
            }

            return jsonify(response_data)
        except ValueError as e:
            logging_util.warning(f"Get story paginated validation error: {e}")
            return jsonify({KEY_ERROR: str(e)}), 400
        except Exception as e:
            logging_util.error(f"Get story paginated error: {e}")
            logging_util.error(traceback.format_exc())
            return jsonify(
                {
                    KEY_SUCCESS: False,
                    KEY_ERROR: "Failed to retrieve story entries",
                }
            ), 500

    @app.route("/api/campaigns", methods=["POST"])
    @limiter.limit(campaign_create_rate_limit)
    @check_token
    @async_route
    async def create_campaign_route(
        user_id: UserId, user_email: str | None = None
    ) -> Response | tuple[Response, int]:
        try:
            data = request.get_json()
            if data is None or not isinstance(data, dict):
                return jsonify({KEY_ERROR: "Invalid JSON payload"}), 400

            # Debug logging
            logging_util.info("Received campaign creation request:")
            logging_util.info(f"  Character: {data.get('character', '')}")
            logging_util.info(f"  Setting: {data.get('setting', '')}")
            logging_util.info(f"  Description: {data.get('description', '')}")
            logging_util.info(f"  Custom options: {data.get('custom_options', [])}")
            logging_util.info(f"  Selected prompts: {data.get('selected_prompts', [])}")

            # Add user_id to request data
            data["user_id"] = user_id

            result = await get_mcp_client().call_tool("create_campaign", data)

            if not result.get(KEY_SUCCESS):
                return safe_jsonify(result), result.get("status_code", 400)

            # Map to original response format for frontend compatibility
            response_data = {
                KEY_SUCCESS: True,
                KEY_CAMPAIGN_ID: result.get(KEY_CAMPAIGN_ID),
            }

            return jsonify(response_data), 201
        except MCPClientError as e:
            return handle_mcp_errors(e)
        except Exception as e:
            logging_util.error(f"Failed to create campaign: {e}")
            return generic_error_response("create campaign")

    @app.route("/api/campaigns/<campaign_id>", methods=["PATCH"])
    @limiter.limit("50000 per hour, 1000 per minute")  # High limits, sanity checks only
    @check_token
    @async_route
    async def update_campaign(
        user_id: UserId, campaign_id: CampaignId, user_email: str | None = None
    ) -> Response | tuple[Response, int]:
        try:
            data = request.get_json()
            if data is None or not isinstance(data, dict):
                return jsonify({KEY_ERROR: "Invalid JSON payload"}), 400

            # Handle legacy title-only updates
            if constants.KEY_TITLE in data and len(data) == 1:
                new_title = data.get(constants.KEY_TITLE)
                if not isinstance(new_title, str) or new_title.strip() == "":
                    return jsonify({KEY_ERROR: "New title is required"}), 400
                updates = {constants.KEY_TITLE: new_title.strip()}
            else:
                # General updates
                updates = data

            request_data = {
                "user_id": user_id,
                "campaign_id": campaign_id,
                "updates": updates,
            }

            # Direct service calls (testing mode removed - always use direct approach)
            result = await world_logic.update_campaign_unified(request_data)

            if not result.get(KEY_SUCCESS):
                return safe_jsonify(result), result.get("status_code", 400)

            # Map to original response format for frontend compatibility
            response_data = {
                KEY_SUCCESS: True,
                KEY_MESSAGE: result.get("message", "Campaign updated successfully."),
            }

            return jsonify(response_data)
        except MCPClientError as e:
            return handle_mcp_errors(e)
        except Exception:
            logging_util.error(traceback.format_exc())
            return generic_error_response("update campaign")

    @app.route("/api/campaigns/<campaign_id>/equipment", methods=["GET"])
    @limiter.limit(campaign_rate_limit)
    @check_token
    @async_route
    async def get_equipment(
        user_id: UserId, campaign_id: CampaignId, user_email: str | None = None
    ) -> Response | tuple[Response, int]:
        """Fetch and format equipment from game state without hitting LLM.

        Returns formatted equipment summary directly from game_state.
        This is a fast, deterministic operation - no AI processing required.
        """
        try:
            # Get game state from Firestore
            game_state = await run_blocking_io(
                firestore_service.get_campaign_game_state, user_id, campaign_id
            )
            if not game_state:
                return (
                    jsonify({KEY_SUCCESS: False, KEY_ERROR: "Campaign not found"}),
                    404,
                )

            # Extract equipment using deterministic function (no LLM)
            equipment_list = equipment_display.extract_equipment_display(game_state)

            # Build formatted summary
            if equipment_list:
                summary = equipment_display.build_equipment_summary(
                    equipment_list, "Your Equipment"
                )
            else:
                summary = "You don't have any equipment yet."

            return jsonify(
                {
                    KEY_SUCCESS: True,
                    "equipment_summary": summary,
                    "equipment_list": equipment_list,
                }
            )

        except Exception as e:
            logging_util.error(f"Get equipment error: {e}")
            logging_util.error(traceback.format_exc())
            return jsonify(
                {
                    KEY_SUCCESS: False,
                    KEY_ERROR: "Failed to retrieve equipment",
                }
            ), 500

    @app.route("/api/campaigns/<campaign_id>/stats", methods=["GET"])
    @limiter.limit(campaign_rate_limit)
    @check_token
    @async_route
    async def get_stats(
        user_id: UserId, campaign_id: CampaignId, user_email: str | None = None
    ) -> Response | tuple[Response, int]:
        """Fetch character stats from game state without hitting LLM.

        Returns:
        - Base stats (naked, without equipment bonuses)
        - Effective stats (with equipment bonuses applied)
        - HP, level, AC, and other combat-relevant stats

        Game state locations:
        - game_state.player_character_data.stats: {str, dex, con, int, wis, cha}
        - game_state.player_character_data.hp_current, hp_max
        - game_state.player_character_data.level
        - game_state.player_character_data.equipment: items with potential bonuses
        - game_state.item_registry: item definitions with stats/bonuses
        """
        try:
            game_state = await run_blocking_io(
                firestore_service.get_campaign_game_state, user_id, campaign_id
            )
            if not game_state:
                return (
                    jsonify({KEY_SUCCESS: False, KEY_ERROR: "Campaign not found"}),
                    404,
                )

            pc_data_raw = (
                game_state.player_character_data
                if hasattr(game_state, "player_character_data")
                else {}
            ) or {}
            pc_data_dict = (
                pc_data_raw
                if isinstance(pc_data_raw, dict)
                else vars(pc_data_raw)
                if hasattr(pc_data_raw, "__dict__")
                else {}
            )

            # Helper to safely get values from pc_data (handles both dict and object)
            def safe_get(key: str, default: Any = None) -> Any:
                if key in pc_data_dict:
                    return pc_data_dict.get(key, default)
                if hasattr(pc_data_raw, key):
                    return getattr(pc_data_raw, key, default)
                return default

            # Extract base stats
            stat_keys = {
                "str": "strength",
                "dex": "dexterity",
                "con": "constitution",
                "int": "intelligence",
                "wis": "wisdom",
                "cha": "charisma",
            }

            naked_stats: dict[str, Any] = {}
            effective_stats_raw: dict[str, Any] = {}

            def coerce_stat_source(raw_source: Any, label: str) -> dict[str, Any]:
                """Return a dict-like stat source or log and fall back to empty."""
                if isinstance(raw_source, dict):
                    return raw_source
                if raw_source not in (None, {}):
                    logging_util.warning(
                        f"Stats parse fallback: ignoring non-dict {label} source type {type(raw_source).__name__}"
                    )
                return {}

            # Check for base_attributes (naked stats) first - new schema
            base_attrs = coerce_stat_source(
                safe_get("base_attributes"), "base_attributes"
            )

            # Check multiple possible locations for effective stats: attributes, stats, aptitudes
            aptitudes = safe_get("aptitudes") or {}
            stat_sources = [
                coerce_stat_source(safe_get("attributes"), "attributes"),
                coerce_stat_source(safe_get("stats"), "stats"),
                coerce_stat_source(aptitudes, "aptitudes"),
                pc_data_dict if isinstance(pc_data_dict, dict) else {},
            ]

            def extract_stat_value(
                source: dict, short_key: str, long_key: str, upper_key: str
            ) -> Any:
                """Extract stat value from a source dict, handling various formats."""
                for key in [short_key, upper_key, long_key]:
                    if key in source:
                        val = source[key]
                        if isinstance(val, dict) and "score" in val:
                            return val["score"]
                        return val
                return None

            # Extract naked stats from base_attributes (new schema)
            for short_key, long_key in stat_keys.items():
                upper_key = short_key.upper()
                val = extract_stat_value(base_attrs, short_key, long_key, upper_key)
                if val is not None:
                    naked_stats[short_key] = val

            # Extract effective stats from attributes/stats/aptitudes
            for short_key, long_key in stat_keys.items():
                upper_key = short_key.upper()
                for source in stat_sources:
                    if not isinstance(source, dict):
                        continue
                    val = extract_stat_value(source, short_key, long_key, upper_key)
                    if val is not None:
                        effective_stats_raw[short_key] = val
                        break
                if short_key not in effective_stats_raw:
                    logging_util.warning(
                        f"Stats parse fallback: missing {short_key}/{long_key}; defaulting to 10"
                    )
                    effective_stats_raw[short_key] = 10

            # If no base_attributes (legacy schema), use effective as naked
            # This maintains backward compatibility
            if not naked_stats:
                naked_stats = dict(effective_stats_raw)

            # Calculate modifiers
            def calc_modifier(score: int) -> int:
                return (score - 10) // 2

            naked_with_mods = {}
            for stat, value in naked_stats.items():
                try:
                    score = int(value) if value is not None else 10
                except (ValueError, TypeError):
                    logging_util.warning(
                        f"Stats parse fallback: invalid value for {stat} -> {value!r}; defaulting to 10"
                    )
                    score = 10
                mod = calc_modifier(score)
                sign = "+" if mod >= 0 else ""
                naked_with_mods[stat] = {"score": score, "modifier": f"{sign}{mod}"}

            # Get equipment bonuses from item_registry
            item_registry = getattr(game_state, "item_registry", {}) or {}
            # Check both 'equipment' and 'inventory' keys (game state uses 'inventory')
            equipment = safe_get("equipment") or safe_get("inventory") or {}
            equipment_bonuses = stats_display.extract_equipment_bonuses(
                {
                    "equipment": equipment if isinstance(equipment, dict) else {},
                    "item_registry": item_registry,
                },
                base_stats=naked_with_mods,
                item_registry=item_registry,
            )
            # Calculate effective stats (base + equipment bonuses)
            effective_stats = {}
            for stat, data in naked_with_mods.items():
                bonus = equipment_bonuses.get(stat, 0)
                effective_score = data["score"] + bonus
                effective_mod = calc_modifier(effective_score)
                sign = "+" if effective_mod >= 0 else ""
                effective_stats[stat] = {
                    "score": effective_score,
                    "modifier": f"{sign}{effective_mod}",
                    "bonus_from_equipment": bonus if bonus else None,
                }

            # Get other combat stats
            hp_current = safe_get("hp_current", safe_get("hp", 0))
            hp_max = safe_get("hp_max", 0)
            level = safe_get("level", 1)
            ac = safe_get("ac", safe_get("armor_class", 10))
            try:
                ac_base_val = int(ac)
            except (TypeError, ValueError):
                ac_base_val = 10
            ac_bonus = equipment_bonuses.get("ac", 0)
            effective_ac = ac_base_val + ac_bonus

            # Build formatted summary using shared stats_display module
            # This includes BG3-style combat stats: proficiency, initiative, spell DC, spell attack, weapon stats
            game_state_dict = {
                "item_registry": item_registry,
                "player_character_data": {
                    **pc_data_dict,
                    "stats": {
                        stat: data["score"] for stat, data in naked_with_mods.items()
                    },
                    "level": level,
                    "hp_current": hp_current,
                    "hp_max": hp_max,
                    "armor_class": ac_base_val,
                    "equipment": equipment if isinstance(equipment, dict) else {},
                },
            }
            stats_summary = stats_display.build_stats_summary(game_state_dict)

            # Extract and deduplicate features/feats using shared module
            features = safe_get("features", [])
            unique_features = stats_display.deduplicate_features(features)

            # Calculate combat stats for JSON response
            proficiency_bonus = stats_display.get_proficiency_bonus(level)
            dex_mod = stats_display.calc_modifier(
                effective_stats.get("dex", {}).get("score", 10)
            )
            class_name = safe_get("class_name", safe_get("class", ""))
            spellcasting_ability = stats_display.get_spellcasting_ability(
                class_name, pc_data_dict
            )

            # Spell stats (if spellcaster)
            spell_stats = None
            if spellcasting_ability:
                spell_mod = stats_display.calc_modifier(
                    effective_stats.get(spellcasting_ability, {}).get("score", 10)
                )
                spell_stats = {
                    "spellcasting_ability": spellcasting_ability.upper(),
                    "spell_save_dc": 8 + proficiency_bonus + spell_mod,
                    "spell_attack_bonus": proficiency_bonus + spell_mod,
                }

            # Saving throws (structured)
            effective_scores = {
                stat: data.get("score", 10) for stat, data in effective_stats.items()
            }
            explicit_saves = safe_get("saving_throw_proficiencies", [])
            saving_throws = stats_display.compute_saving_throws(
                class_name, effective_scores, proficiency_bonus, explicit_saves
            )

            speed_val = safe_get("speed", safe_get("movement_speed"))

            # Calculate hit dice
            # Clamp level to 1-20 for consistency with get_hit_dice
            level_int = coerce_int(level, 1) or 1
            level_int = max(1, min(20, level_int))
            hit_dice = stats_display.get_hit_dice(class_name, level_int)
            hit_dice_current = safe_get("hit_dice_current")
            hit_dice_max = safe_get("hit_dice_max", level_int)

            # Calculate unarmed strike
            str_mod = stats_display.calc_modifier(effective_scores.get("str", 10))
            is_monk = (
                "monk" in class_name.lower()
                if isinstance(class_name, str) and class_name
                else False
            )
            unarmed_strike = stats_display.calculate_unarmed_strike(
                str_mod, proficiency_bonus, is_monk
            )

            return jsonify(
                {
                    KEY_SUCCESS: True,
                    "stats_summary": stats_summary,
                    "naked_stats": naked_with_mods,
                    "effective_stats": effective_stats,
                    "equipment_bonuses": equipment_bonuses,
                    "combat_stats": {
                        "level": level,
                        "hp_current": hp_current,
                        "hp_max": hp_max,
                        "ac": ac_base_val,
                        "effective_ac": effective_ac,
                        "proficiency_bonus": proficiency_bonus,
                        "initiative": dex_mod,
                        "speed": speed_val,
                        "hit_dice": hit_dice,
                        "hit_dice_current": hit_dice_current,
                        "hit_dice_max": hit_dice_max,
                        "spell_stats": spell_stats,
                        "saving_throws": saving_throws,
                        "unarmed_strike": unarmed_strike,
                    },
                    "features": unique_features,
                }
            )

        except Exception as e:
            logging_util.error(f"Get stats error: {e}")
            logging_util.error(traceback.format_exc())
            return jsonify(
                {
                    KEY_SUCCESS: False,
                    KEY_ERROR: "Failed to retrieve stats",
                }
            ), 500

    @app.route("/api/campaigns/<campaign_id>/spells", methods=["GET"])
    @limiter.limit(campaign_rate_limit)
    @check_token
    @async_route
    async def get_spells(
        user_id: UserId, campaign_id: CampaignId, user_email: str | None = None
    ) -> Response | tuple[Response, int]:
        """Fetch spells and class resources from game state without hitting LLM.

        Returns:
        - Spells known/available
        - Spells prepared/memorized
        - Spell slots (current/max by level)
        - Class resources (ki points, rage, channel divinity, etc.)

        Game state locations:
        - game_state.player_character_data.spells: list of known spells
        - game_state.player_character_data.spells_prepared: prepared spell list
        - game_state.player_character_data.spell_slots: {level: {current, max}}
        - game_state.player_character_data.resources: class features and uses
        - game_state.player_character_data.cantrips: cantrips known
        """
        try:
            game_state = await run_blocking_io(
                firestore_service.get_campaign_game_state, user_id, campaign_id
            )
            if not game_state:
                return (
                    jsonify({KEY_SUCCESS: False, KEY_ERROR: "Campaign not found"}),
                    404,
                )

            pc_data_raw = (
                game_state.player_character_data
                if hasattr(game_state, "player_character_data")
                else {}
            ) or {}
            pc_data_dict = (
                pc_data_raw
                if isinstance(pc_data_raw, dict)
                else vars(pc_data_raw)
                if hasattr(pc_data_raw, "__dict__")
                else {}
            )

            # Helper to safely get values from pc_data (handles both dict and object)
            def safe_get(key: str, default: Any = None) -> Any:
                if key in pc_data_dict:
                    return pc_data_dict.get(key, default)
                if hasattr(pc_data_raw, key):
                    return getattr(pc_data_raw, key, default)
                return default

            # Extract spell information
            def normalize_spell_list(raw: Any) -> list[Any]:
                if raw is None:
                    return []
                if isinstance(raw, list):
                    return raw
                if isinstance(raw, str):
                    return [raw]
                return []

            cantrips = normalize_spell_list(safe_get("cantrips", []))
            spells_known = normalize_spell_list(
                safe_get("spells", safe_get("spells_known", []))
            )
            spells_prepared = normalize_spell_list(
                safe_get("spells_prepared", safe_get("spells_memorized", []))
            )

            # Extract spell slots - handle various formats
            spell_slots_raw = safe_get("spell_slots", {})
            spell_slots = {}
            if isinstance(spell_slots_raw, dict):
                for level, data in spell_slots_raw.items():
                    if isinstance(data, dict):
                        spell_slots[level] = {
                            "current": data.get("current", data.get("remaining", 0)),
                            "max": data.get("max", data.get("total", 0)),
                        }
                    elif isinstance(data, (int, str)):
                        # Simple format: level -> remaining slots (max unknown)
                        try:
                            remaining = int(data)
                        except (ValueError, TypeError):
                            logging_util.warning(
                                f"Spells parse fallback: invalid spell slot value for level {level}: {data!r}; skipping"
                            )
                            continue
                        spell_slots[level] = {"current": remaining, "max": 0}

            # Also check for spell_slots_level_X format
            pc_items = pc_data_dict.items() if isinstance(pc_data_dict, dict) else []
            for key, value in pc_items:
                if key.startswith("spell_slots_level_"):
                    level = key.replace("spell_slots_level_", "")
                    if level not in spell_slots:
                        try:
                            max_slots = int(value)
                        except (ValueError, TypeError):
                            # Ignore malformed slot values; treat as unavailable
                            logging_util.warning(
                                f"Spells parse fallback: invalid spell_slots_level_{level} value {value!r}; skipping"
                            )
                            continue
                        spell_slots[level] = {"current": max_slots, "max": max_slots}

            # Extract class resources (HD, lay on hands, divine sense, ki, rage, etc.)
            resources_raw = safe_get("resources", {})
            class_resources = {}

            if isinstance(resources_raw, dict):
                # Copy to avoid mutating game state, but exclude spell_slots
                # (spell_slots are displayed separately in the Spell Slots section)
                class_resources = {
                    k: v for k, v in resources_raw.items() if k != "spell_slots"
                }

                # Also check for spell_slots inside resources (format: {level_X: {used, max}})
                resources_spell_slots = resources_raw.get("spell_slots", {})
                if isinstance(resources_spell_slots, dict):
                    for level_key, slot_data in resources_spell_slots.items():
                        if isinstance(slot_data, dict):
                            # Format: level_1: {used: 1, max: 4} -> current = max - used
                            # Convert to int to handle string values from Firestore
                            try:
                                max_val = int(slot_data.get("max", 0))
                                used_val = int(slot_data.get("used", 0))
                                current_val = max_val - used_val
                            except (ValueError, TypeError):
                                max_val = 0
                                used_val = 0
                                current_val = 0
                            # Extract level number from "level_1" format
                            level = (
                                level_key.replace("level_", "")
                                if level_key.startswith("level_")
                                else level_key
                            )
                            # Only add if not already populated from top-level spell_slots
                            if level not in spell_slots:
                                spell_slots[level] = {
                                    "current": current_val,
                                    "max": max_val,
                                }
            elif isinstance(resources_raw, str):
                # Parse string format like "HD: 3/5 | Lay on Hands: 15/15"
                parts = resources_raw.split("|")
                for part in parts:
                    if ":" in part:
                        name, value = part.split(":", 1)
                        class_resources[name.strip()] = value.strip()

            # Also check for common resource fields at top level
            resource_fields = [
                "hit_dice",
                "hd",
                "lay_on_hands",
                "divine_sense",
                "channel_divinity",
                "ki_points",
                "ki",
                "rage",
                "rages",
                "bardic_inspiration",
                "sorcery_points",
                "superiority_dice",
                "second_wind",
                "action_surge",
                "arcane_recovery",
                "wild_shape",
                "infusions",
            ]
            for field in resource_fields:
                field_value = safe_get(field)
                if field_value is not None and field not in class_resources:
                    class_resources[field] = field_value

            # Normalize spells for comparison (handles dicts vs. strings and ordering)
            def spell_signature(spell: Any) -> tuple[str, str]:
                if isinstance(spell, dict):
                    name = spell.get("name", "")
                    level_val = spell.get("level", "")
                else:
                    name = spell
                    level_val = ""

                name_norm = str(name).strip().lower() if name is not None else ""
                level_norm = (
                    str(level_val).strip().lower()
                    if level_val not in (None, "")
                    else ""
                )
                return name_norm, level_norm

            normalized_spells_known: set[tuple[str, str]] = set()
            for spell in spells_known or []:
                signature = spell_signature(spell)
                if signature[0]:
                    normalized_spells_known.add(signature)

            normalized_spells_prepared: set[tuple[str, str]] = set()
            for spell in spells_prepared or []:
                signature = spell_signature(spell)
                if signature[0]:
                    normalized_spells_prepared.add(signature)

            # Build formatted summary
            lines = ["━━━ Spells & Resources ━━━"]

            # Cantrips
            if cantrips:
                lines.append("")
                lines.append("▸ Cantrips (at will):")
                for cantrip in cantrips:
                    name = (
                        cantrip.get("name", "Unknown Cantrip")
                        if isinstance(cantrip, dict)
                        else str(cantrip)
                    )
                    lines.append(f"  • {name}")

            # Spell slots
            if spell_slots:
                lines.append("")
                lines.append("▸ Spell Slots:")
                for level in sorted(
                    spell_slots.keys(),
                    key=lambda x: (0, int(x)) if str(x).isdigit() else (1, str(x)),
                ):
                    data = spell_slots[level]
                    max_display = (
                        data["max"] if data.get("max") not in (0, None, "") else "?"
                    )
                    lines.append(f"  • Level {level}: {data['current']}/{max_display}")

            # Missing spell list warning for spellcasters with slots but no spells
            if (
                spell_slots
                and not spells_known
                and not cantrips
                and not spells_prepared
            ):
                lines.append("")
                lines.append("▸ Spells:")
                lines.append(
                    '  No spell list recorded. Type: "What spells do I know?" to set them up.'
                )

            # Spells prepared - grouped by level
            if spells_prepared:
                lines.append("")
                lines.append("▸ Spells Prepared:")
                # Group spells by level
                prepared_by_level: dict[str, list[str]] = {}
                for spell in spells_prepared:
                    name = (
                        spell.get("name", "Unknown Spell")
                        if isinstance(spell, dict)
                        else str(spell)
                    )
                    # Get level from dict, or look up from spell name for legacy string data
                    if isinstance(spell, dict):
                        level = spell.get("level", 0)
                    else:
                        level = get_spell_level(name)
                    level_str = str(level) if level is not None else "0"
                    if level_str not in prepared_by_level:
                        prepared_by_level[level_str] = []
                    prepared_by_level[level_str].append(name)
                # Sort by level and display
                for level_key in sorted(
                    prepared_by_level.keys(), key=lambda x: int(x) if x.isdigit() else 0
                ):
                    spell_names = prepared_by_level[level_key]
                    if level_key == "0":
                        level_label = "Cantrips"
                    else:
                        level_label = f"Level {level_key}"
                    lines.append(f"  {level_label}: {', '.join(sorted(spell_names))}")

            # Spells known (if different from prepared) - grouped by level
            if spells_known and normalized_spells_known != normalized_spells_prepared:
                lines.append("")
                lines.append("▸ Spells Known:")
                # Group spells by level
                spells_by_level: dict[str, list[str]] = {}
                for spell in spells_known:
                    name = (
                        spell.get("name", "Unknown Spell")
                        if isinstance(spell, dict)
                        else str(spell)
                    )
                    # Get level from dict, or look up from spell name for legacy string data
                    if isinstance(spell, dict):
                        level = spell.get("level", 0)
                    else:
                        level = get_spell_level(name)
                    # Normalize level to string
                    level_str = str(level) if level is not None else "0"
                    if level_str not in spells_by_level:
                        spells_by_level[level_str] = []
                    spells_by_level[level_str].append(name)
                # Sort by level and display
                for level_key in sorted(
                    spells_by_level.keys(), key=lambda x: int(x) if x.isdigit() else 0
                ):
                    spell_names = spells_by_level[level_key]
                    if level_key == "0":
                        level_label = "Cantrips"
                    else:
                        level_label = f"Level {level_key}"
                    lines.append(f"  {level_label}: {', '.join(sorted(spell_names))}")

            # Class resources
            if class_resources:
                lines.append("")
                lines.append("▸ Class Resources:")
                for resource_name, value in class_resources.items():
                    display_name = resource_name.replace("_", " ").title()
                    if isinstance(value, dict):
                        current = value.get("current", value.get("remaining", "?"))
                        maximum = value.get("max", value.get("total", "?"))
                        lines.append(f"  • {display_name}: {current}/{maximum}")
                    else:
                        lines.append(f"  • {display_name}: {value}")

            # If nothing found
            if len(lines) == 1:
                lines.append("")
                lines.append("No spells or special resources found.")
                lines.append("(Non-spellcasting classes may not have spell slots)")

            # Calculate spell stats (spell DC and spell attack) for spellcasters
            spell_stats = None
            class_name = safe_get("class_name", safe_get("class", ""))
            spellcasting_ability = stats_display.get_spellcasting_ability(
                class_name, pc_data_dict
            )
            if spellcasting_ability:
                level = safe_get("level", 1)
                proficiency_bonus = stats_display.get_proficiency_bonus(level)

                # Get ability scores
                stats_raw = (
                    safe_get("stats")
                    or safe_get("attributes")
                    or safe_get("ability_scores")
                    or {}
                )
                normalized_stats = stats_display.normalize_stats(stats_raw)

                # Get spellcasting modifier
                spell_score_raw = normalized_stats.get(spellcasting_ability, 10)
                if isinstance(spell_score_raw, dict):
                    spell_score = spell_score_raw.get("score", 10)
                else:
                    spell_score = spell_score_raw
                try:
                    spell_score = int(spell_score)
                except (TypeError, ValueError):
                    spell_score = 10

                spell_mod = stats_display.calc_modifier(spell_score)
                spell_stats = {
                    "spellcasting_ability": spellcasting_ability.upper(),
                    "spell_save_dc": 8 + proficiency_bonus + spell_mod,
                    "spell_attack_bonus": proficiency_bonus + spell_mod,
                }

            return jsonify(
                {
                    KEY_SUCCESS: True,
                    "spells_summary": "\n".join(lines),
                    "cantrips": cantrips,
                    "spells_known": spells_known,
                    "spells_prepared": spells_prepared,
                    "spell_slots": spell_slots,
                    "class_resources": class_resources,
                    "spell_stats": spell_stats,
                }
            )

        except Exception as e:
            logging_util.error(f"Get spells error: {e}")
            logging_util.error(traceback.format_exc())
            return jsonify(
                {
                    KEY_SUCCESS: False,
                    KEY_ERROR: "Failed to retrieve spells",
                }
            ), 500

    @app.route("/api/campaigns/<campaign_id>/interaction", methods=["POST"])
    @limiter.limit(
        "30000 per hour, 1000 per minute"
    )  # High limits for normal conversation flow
    @check_token
    @async_route
    async def handle_interaction(
        user_id: UserId, campaign_id: CampaignId, user_email: str | None = None
    ) -> Response | tuple[Response, int]:
        campaign_ctx_token = logging_util.push_campaign_id(campaign_id)
        try:
            logging_util.info("DEBUG: handle_interaction START - testing mode removed")

            data = request.get_json()
            if data is None or not isinstance(data, dict):
                return jsonify({KEY_ERROR: "Invalid JSON payload"}), 400

            logging_util.info(f"DEBUG: request data = {data}")
            user_input = extract_interaction_input(data)
            logging_util.info(
                f"DEBUG: user_input = {user_input} (KEY_USER_INPUT='{KEY_USER_INPUT}')"
            )
            mode = data.get(constants.KEY_MODE, constants.MODE_CHARACTER)
            mode_violation = _get_mode_violation()
            if mode_violation:
                return jsonify(mode_violation), 500
            # Security: Strict boolean check - only allow explicit True or "true" string
            # bool("false") = True, so we must check explicitly
            raw_payloads_raw = data.get("include_raw_llm_payloads", False)
            include_raw_llm_payloads = raw_payloads_raw is True or (
                isinstance(raw_payloads_raw, str) and raw_payloads_raw.lower() == "true"
            )

            # Security: Restrict raw LLM payload capture to admin/developer users only
            # Harden: Use strict boolean check and require ALLOW_TEST_AUTH_BYPASS for test bypass
            if include_raw_llm_payloads:
                # Strict boolean check: only allow if explicitly "true" (case-insensitive)
                is_dev_mode = os.getenv("WORLDAI_DEV_MODE", "").lower() == "true"
                # Test bypass requires both TESTING_AUTH_BYPASS_MODE AND ALLOW_TEST_AUTH_BYPASS
                is_test_bypass = TESTING_AUTH_BYPASS_MODE and ALLOW_TEST_AUTH_BYPASS
                is_dev_or_test = is_dev_mode or is_test_bypass

                admin_ids = [
                    uid.strip()
                    for uid in os.getenv("WORLDAI_ADMIN_USER_IDS", "").split(",")
                    if uid.strip()
                ]
                if not is_dev_or_test and user_id not in admin_ids:
                    logging_util.warning(
                        "UNAUTHORIZED_RAW_PAYLOAD_REQUEST: User %s requested raw LLM payloads but is not authorized.",
                        user_id,
                    )
                    include_raw_llm_payloads = False

            # Validate user_input is provided (None only, empty strings are allowed)
            if user_input is None:
                return jsonify({KEY_ERROR: "User input is required"}), 400

            _append_http_capture(
                {
                    "type": "http_request",
                    "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
                    "path": request.path,
                    "method": request.method,
                    "campaign_id": campaign_id,
                    "user_id": user_id,
                    "headers": _redact_headers(dict(request.headers)),
                    "json": data,
                }
            )

            # Check rate limits before processing (also consume the turn atomically)
            # NOTE: We check this AFTER validation to avoid consuming turns on invalid requests
            rate_limit_result = await run_blocking_io(
                rate_limiting.check_rate_limit, user_id, user_email, True
            )
            if not rate_limit_result.get("allowed", True):
                logging_util.warning(
                    f"Rate limit exceeded for user {user_id} (email: {user_email})"
                )
                response_data = {
                    KEY_SUCCESS: False,
                    KEY_ERROR: rate_limit_result.get("error_message"),
                    "error_type": "rate_limit",
                    "daily_remaining": rate_limit_result.get("daily_remaining", 0),
                    "hourly_remaining": rate_limit_result.get("hourly_remaining", 0),
                }
                # Include reset time fields for frontend countdown timer
                if "reset_time_daily" in rate_limit_result:
                    response_data["reset_time_daily"] = rate_limit_result[
                        "reset_time_daily"
                    ]
                if "reset_time_hourly" in rate_limit_result:
                    response_data["reset_time_hourly"] = rate_limit_result[
                        "reset_time_hourly"
                    ]
                _append_http_capture(
                    {
                        "type": "http_response",
                        "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
                        "path": request.path,
                        "method": request.method,
                        "campaign_id": campaign_id,
                        "user_id": user_id,
                        "status_code": 429,
                        "json": response_data,
                    }
                )
                return jsonify(response_data), 429

            # Use MCP client for processing action (testing mode removed)
            logging_util.info(
                f"DEBUG: Processing interaction - user_id={user_id}, campaign_id={campaign_id}"
            )

            try:
                # Prepare request data for unified API
                request_data = {
                    "user_id": user_id,
                    "campaign_id": campaign_id,
                    "user_input": user_input,
                    "mode": mode,
                    "include_raw_llm_payloads": include_raw_llm_payloads,
                }
                result = await get_mcp_client().call_tool(
                    "process_action", request_data
                )
                logging_util.info(
                    f"DEBUG: MCP process_action returned result: {result.get('success', False)}"
                )
                if not result.get("success"):
                    error_msg = result.get(
                        "error", result.get("error_message", "Unknown error")
                    )
                    logging_util.error(f"DEBUG: MCP process_action failed: {error_msg}")

                    # Return appropriate error response based on error type
                    if (
                        "not found" in error_msg.lower()
                        or "campaign not found" in error_msg.lower()
                    ):
                        return jsonify({"error": "Campaign not found"}), 404
                    return jsonify({"error": error_msg}), 400
            except MCPClientError as e:
                # Handle MCP-specific errors with proper status code translation
                return handle_mcp_errors(e)
            except Exception as e:
                logging_util.error(f"DEBUG: MCP process_action exception: {e}")
                return jsonify({"error": "Internal server error"}), 500

            if not result.get(KEY_SUCCESS):
                return safe_jsonify(result), result.get("status_code", 400)

            # Debug logging for Cloud Run troubleshooting
            logging_util.info(f"MCP process_action result keys: {list(result.keys())}")
            if "story" in result:
                story_entries = result.get("story", [])
                logging_util.info(
                    f"Story field type: {type(story_entries)}, length: {len(story_entries) if hasattr(story_entries, '__len__') else 'N/A'}"
                )

            # Translate MCP response to frontend-compatible format
            # MCP returns 'story' field, frontend expects 'narrative' or 'response'
            if "story" in result:
                # Extract first story entry text for backward compatibility
                story_entries = result.get("story", [])
                if (
                    story_entries
                    and isinstance(story_entries, list)
                    and len(story_entries) > 0
                ):
                    first_entry = story_entries[0]
                    narrative_text = (
                        first_entry.get("text", "")
                        if isinstance(first_entry, dict)
                        else str(first_entry)
                    )
                    result["narrative"] = narrative_text
                    result["response"] = narrative_text  # Fallback compatibility
                else:
                    logging_util.warning(
                        f"Empty or invalid story entries in MCP response for campaign {campaign_id}"
                    )
                    result["narrative"] = ""
                    result["response"] = ""
            else:
                # Missing story field - this is likely the cause of [Error: No response from server]
                logging_util.warning(
                    f"Missing 'story' field in MCP response for campaign {campaign_id}. Available fields: {list(result.keys())}"
                )
                result["narrative"] = ""
                result["response"] = ""

            # Return the translated result using safe_jsonify to handle Firestore Sentinels
            _append_http_capture(
                {
                    "type": "http_response",
                    "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
                    "path": request.path,
                    "method": request.method,
                    "campaign_id": campaign_id,
                    "user_id": user_id,
                    "status_code": 200,
                    "json": result,
                }
            )
            return safe_jsonify(result), 200

        except MCPClientError as e:
            # Handle MCP-specific errors with proper translation
            return handle_mcp_errors(e)
        except Exception as e:
            # Critical security fix: Never expose raw exceptions to frontend
            logging_util.error(
                f"Critical error in handle_interaction for campaign {campaign_id}: {e}"
            )
            logging_util.error(
                f"User input: {user_input if 'user_input' in locals() else 'N/A'}"
            )
            logging_util.error(traceback.format_exc())

            # Return sanitized error response that cannot leak JSON or internal details
            return jsonify(
                {
                    KEY_SUCCESS: False,
                    KEY_ERROR: "An error occurred processing your request.",
                    KEY_RESPONSE: "I encountered an issue and cannot continue at this time. Please try again, or contact support if the problem persists.",
                }
            ), 500
        finally:
            logging_util.pop_campaign_id(campaign_ctx_token)

    @app.route("/api/campaigns/<campaign_id>/interaction/stream", methods=["POST"])
    @limiter.limit("30000 per hour, 1000 per minute")
    @check_token
    def handle_interaction_stream(
        user_id: UserId, campaign_id: CampaignId, user_email: str | None = None
    ) -> Response | tuple[Response, int]:
        """Stream LLM response via Server-Sent Events.

        This endpoint provides real-time streaming of LLM responses,
        allowing the frontend to display text as it's generated.

        Uses the full game state flow:
        - Loads campaign data and game state from Firestore
        - Uses appropriate agent for system instructions
        - Streams narrative chunks in real-time
        - Persists story entries upon completion

        Returns SSE events with types:
        - chunk: Incremental text content
        - status: Progress status updates
        - warning: Non-fatal issues
        - error: Error information
        - done: Stream complete with full response
        """
        campaign_ctx_token = logging_util.push_campaign_id(campaign_id)
        try:
            data = request.get_json()

            if data is None or not isinstance(data, dict):
                return jsonify({KEY_ERROR: "Invalid JSON payload"}), 400

            user_input = extract_interaction_input(data)
            mode = data.get(constants.KEY_MODE, constants.MODE_CHARACTER)
            mode_violation = _get_mode_violation()
            if mode_violation:
                return jsonify(mode_violation), 500

            if user_input is None:
                return jsonify({KEY_ERROR: "User input is required"}), 400

            handler_entry_utc = datetime.datetime.now(datetime.UTC).isoformat()
            _append_http_capture(
                {
                    "type": "http_request",
                    "timestamp": handler_entry_utc,
                    "handler_entry_utc": handler_entry_utc,
                    "path": request.path,
                    "method": request.method,
                    "campaign_id": campaign_id,
                    "user_id": user_id,
                    "headers": _redact_headers(dict(request.headers)),
                    "json": data,
                }
            )

            # BD-4k0: Streaming endpoint must also enforce per-user turn-based rate limiting.
            # NOTE: We check this AFTER basic validation to avoid consuming turns on invalid requests.
            rate_limit_result = rate_limiting.check_rate_limit(
                user_id, user_email, consume_turn=True
            )
            if not rate_limit_result.get("allowed", True):
                logging_util.warning(
                    "Rate limit exceeded for user %s (email: %s) [streaming]",
                    user_id,
                    user_email,
                )
                response_data = {
                    KEY_SUCCESS: False,
                    KEY_ERROR: rate_limit_result.get("error_message"),
                    "error_type": "rate_limit",
                    "daily_remaining": rate_limit_result.get("daily_remaining", 0),
                    "hourly_remaining": rate_limit_result.get("hourly_remaining", 0),
                }
                if "reset_time_daily" in rate_limit_result:
                    response_data["reset_time_daily"] = rate_limit_result[
                        "reset_time_daily"
                    ]
                if "reset_time_hourly" in rate_limit_result:
                    response_data["reset_time_hourly"] = rate_limit_result[
                        "reset_time_hourly"
                    ]
                _append_http_capture(
                    {
                        "type": "http_response",
                        "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
                        "path": request.path,
                        "method": request.method,
                        "campaign_id": campaign_id,
                        "user_id": user_id,
                        "status_code": 429,
                        "json": response_data,
                    }
                )
                return jsonify(response_data), 429

            # Quick campaign existence check before streaming (avoid fetching full story).
            if not firestore_service.campaign_exists(user_id, campaign_id):
                return jsonify({KEY_ERROR: "Campaign not found"}), 404

            logging_util.info(
                f"Streaming interaction (full flow) - user_id={user_id}, "
                f"campaign_id={campaign_id}, mode={mode}"
            )

            def generate():
                """Generator function for SSE response with full game state."""
                stream_ctx_token = logging_util.push_campaign_id(campaign_id)
                t_handler_start = time.perf_counter()
                handler_start_utc = datetime.datetime.now(datetime.UTC).isoformat()
                chunk_count = 0
                try:
                    # Use the full game state streaming flow
                    for event in stream_story_with_game_state(
                        user_id=user_id,
                        campaign_id=campaign_id,
                        user_input=user_input,
                        mode=mode,
                    ):
                        # Capture SSE payloads for auditable evidence (best-effort only).
                        try:
                            _append_http_capture(
                                {
                                    "type": "sse_event",
                                    "timestamp": datetime.datetime.now(
                                        datetime.UTC
                                    ).isoformat(),
                                    "path": request.path,
                                    "campaign_id": campaign_id,
                                    "user_id": user_id,
                                    "event": event.to_dict()
                                    if hasattr(event, "to_dict")
                                    else str(event),
                                }
                            )
                        except Exception:
                            logging_util.exception(
                                "SSE capture failed (non-fatal): campaign_id=%s user_id=%s",
                                campaign_id,
                                user_id,
                            )
                        yield event.to_sse()
                        chunk_count += 1
                        if chunk_count == 1:
                            t_first_yield = time.perf_counter()
                            logging_util.info(
                                "⏱️ STREAM_TIMING | flask_handler_first_yield: %.3fs | handler_start_utc=%s",
                                t_first_yield - t_handler_start,
                                handler_start_utc,
                            )

                except (GeneratorExit, ConnectionError, OSError):
                    logging_util.info("Streaming connection closed by client")
                except Exception:
                    logging_util.exception(
                        "Unexpected error while streaming LLM response"
                    )
                    error_event = StreamEvent(
                        type="error",
                        payload={
                            "message": "An unexpected error occurred while streaming the response.",
                        },
                    )
                    yield error_event.to_sse()
                finally:
                    try:
                        t_handler_end = time.perf_counter()
                        logging_util.info(
                            "⏱️ STREAM_TIMING | flask_handler_total: %.3fs | chunks_yielded=%d | handler_start_utc=%s",
                            t_handler_end - t_handler_start,
                            chunk_count,
                            handler_start_utc,
                        )
                    finally:
                        logging_util.pop_campaign_id(stream_ctx_token)

            headers = create_sse_response_headers()
            return Response(
                stream_with_context(generate()),
                mimetype="text/event-stream",
                headers=headers,
            )

        except Exception as e:
            logging_util.error(f"Stream setup error: {e}")
            logging_util.error(traceback.format_exc())
            return jsonify(
                {
                    KEY_SUCCESS: False,
                    KEY_ERROR: "Failed to start streaming response.",
                }
            ), 500
        finally:
            logging_util.pop_campaign_id(campaign_ctx_token)

    @app.route("/api/campaigns/<campaign_id>/export", methods=["GET"])
    @limiter.limit("10 per hour, 2 per minute")  # Exporting is infrequent
    @check_token
    @async_route
    async def export_campaign(
        user_id: UserId, campaign_id: CampaignId, user_email: str | None = None
    ) -> Response | tuple[Response, int]:
        try:
            export_format = request.args.get("format", "txt").lower()

            # Use MCP client for export generation
            request_data = {
                "user_id": user_id,
                "campaign_id": campaign_id,
                "format": export_format,
            }

            result = await get_mcp_client().call_tool("export_campaign", request_data)

            if not result.get(KEY_SUCCESS):
                return safe_jsonify(result), result.get("status_code", 400)

            # Get export details from unified API
            export_path = result.get("export_path")
            campaign_title = result.get("campaign_title", "Untitled Campaign")
            desired_download_name = f"{campaign_title}.{export_format}"

            if not export_path or not os.path.exists(export_path):
                return jsonify({KEY_ERROR: "Failed to create export file."}), 500

            logging_util.info(
                f"Exporting file '{export_path}' with download_name='{desired_download_name}'"
            )

            # Use the standard send_file call for file serving
            response = send_file(
                export_path,
                download_name=desired_download_name,
                as_attachment=True,
            )

            @response.call_on_close
            def cleanup() -> None:
                try:
                    os.remove(export_path)
                    logging_util.info(f"Cleaned up temporary file: {export_path}")
                except Exception as e:
                    logging_util.error(f"Error cleaning up file {export_path}: {e}")

            return response

        except MCPClientError as e:
            return handle_mcp_errors(e)
        except Exception as e:
            logging_util.error(f"Export failed: {e}")
            traceback.print_exc()
            return generic_error_response("export campaign")

    # --- Time Sync Route for Clock Skew Detection ---
    @app.route("/api/time", methods=["GET"])
    @limiter.limit("200 per hour, 30 per minute")  # Time sync can be frequent
    def get_server_time() -> Response:
        """
        Get current server time for client clock skew detection and compensation.

        This endpoint is used by the frontend to detect differences between client
        and server clocks, enabling compensation for authentication timing issues.
        """
        current_time = datetime.datetime.now(datetime.UTC)

        return jsonify(
            {
                "server_time_utc": current_time.isoformat(),
                "server_timestamp": int(current_time.timestamp()),
                "server_timestamp_ms": int(current_time.timestamp() * 1000),
            }
        )

    # --- Health Check Route ---
    @app.route("/health", methods=["GET"])
    @limiter.exempt  # Health checks should not be rate limited
    def health_check() -> Response:
        """
        Health check endpoint for deployment verification.

        Used by Cloud Run and deployment workflows to verify service availability.
        Returns 200 OK with service status information including concurrency configuration.
        """
        # Gather system information for monitoring
        health_info = {
            "status": "healthy",
            "service": "worldarchitect-ai",
            "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
        }

        # Include Gunicorn worker configuration if available (from environment)
        gunicorn_workers_raw = os.getenv("GUNICORN_WORKERS")
        gunicorn_threads_raw = os.getenv("GUNICORN_THREADS")

        concurrency: dict[str, int] = {}

        def _safe_parse_int(value: str | None, env_name: str) -> int | None:
            """Safely parse an integer environment variable."""

            if value is None:
                return None

            try:
                return int(value)
            except ValueError:
                logging_util.warning(
                    "Invalid %s value %r provided; ignoring for /health response",
                    env_name,
                    value,
                )
                return None

        gunicorn_workers = _safe_parse_int(gunicorn_workers_raw, "GUNICORN_WORKERS")
        gunicorn_threads = _safe_parse_int(gunicorn_threads_raw, "GUNICORN_THREADS")

        if gunicorn_workers is not None:
            concurrency["workers"] = gunicorn_workers
        if gunicorn_threads is not None:
            concurrency["threads"] = gunicorn_threads
        if gunicorn_workers is not None and gunicorn_threads is not None:
            concurrency["max_concurrent_requests"] = gunicorn_workers * gunicorn_threads

        if concurrency:
            health_info["concurrency"] = concurrency

        # Include MCP client status (check if already initialized, don't trigger initialization)
        # Health checks should be fast and not trigger expensive operations
        if hasattr(app, "_mcp_client") and app._mcp_client is not None:
            health_info["mcp_client"] = {
                "initialized": True,
                "base_url": app._mcp_client.base_url,
                "skip_http": app._mcp_client.skip_http,
            }
        else:
            health_info["mcp_client"] = {"initialized": False}

        return jsonify(health_info)

    # --- MCP JSON-RPC Endpoint ---
    @app.route("/mcp", methods=["POST"])
    @limiter.exempt  # MCP endpoint should not be rate limited (used by internal tools)
    @check_token
    def mcp_endpoint(
        user_id: UserId | None,
        user_email: str | None = None,
    ) -> Response | tuple[Response, int]:
        """
        MCP JSON-RPC 2.0 endpoint for Cloud Run deployment.

        Handles JSON-RPC 2.0 requests for MCP tools without requiring a separate
        HTTP server process. This enables MCP functionality in Cloud Run's single-port
        architecture.

        Supported methods:
        - tools/list: List available MCP tools
        - tools/call: Execute an MCP tool
        - resources/list: List available resources
        - resources/read: Read a resource

        Returns:
            JSON-RPC 2.0 response with result or error
        """
        request_data = None  # Initialize before try block for error handling
        try:
            # Get JSON-RPC request data
            request_data = request.get_json()
            if not request_data:
                response_data = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32700,
                        "message": "Parse error: No JSON data in request",
                    },
                    "id": None,
                }
                _append_http_capture(
                    {
                        "type": "http_response",
                        "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
                        "path": request.path,
                        "method": request.method,
                        "user_id": user_id,
                        "status_code": 400,
                        "json": response_data,
                    }
                )
                return jsonify(response_data), 400

            _append_http_capture(
                {
                    "type": "http_request",
                    "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
                    "path": request.path,
                    "method": request.method,
                    "user_id": user_id,
                    "headers": _redact_headers(dict(request.headers)),
                    "json": request_data,
                }
            )

            # Call the standalone JSON-RPC handler from mcp_api.py (auth-derived user_id)
            response_data = handle_jsonrpc(request_data, user_id=user_id)

            _append_http_capture(
                {
                    "type": "http_response",
                    "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
                    "path": request.path,
                    "method": request.method,
                    "user_id": user_id,
                    "status_code": 200,
                    "json": response_data,
                }
            )

            # Return JSON-RPC response
            return jsonify(response_data)

        except Exception as e:
            # Log error for debugging
            logging_util.error(f"MCP endpoint error: {e}")
            logging_util.error(traceback.format_exc())

            # Return JSON-RPC 2.0 error response
            error_response = {
                "jsonrpc": "2.0",
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"},
                "id": request_data.get("id") if request_data else None,
            }
            _append_http_capture(
                {
                    "type": "http_response",
                    "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
                    "path": request.path,
                    "method": request.method,
                    "user_id": user_id,
                    "status_code": 500,
                    "json": error_response,
                }
            )
            return jsonify(error_response), 500

    # --- Settings Routes ---
    @app.route("/settings")
    @limiter.limit("120 per hour, 20 per minute")  # Prevent brute-force refreshes
    def settings_page() -> Response:
        """Settings page for authenticated users (auth handled client-side)."""
        logging_util.info("Visitor accessed settings page")
        return render_template("settings.html")

    @app.route("/api/settings", methods=["GET", "POST"])
    @limiter.limit(settings_rate_limit)  # Settings access is moderate frequency
    @check_token
    @async_route
    async def api_settings(
        user_id: UserId, user_email: str | None = None
    ) -> Response | tuple[Response, int]:
        """Get or update user settings."""
        try:
            if request.method == "GET":
                # Use MCP client for getting settings
                request_data = {"user_id": user_id}

                # Delegate to world_logic for centralized defaults handling
                result = await world_logic.get_user_settings_unified(
                    {"user_id": user_id}
                )

                if not result.get(KEY_SUCCESS):
                    return jsonify(result), result.get("status_code", 400)

                # Return the settings directly (remove success wrapper for GET compatibility)
                settings = {k: v for k, v in result.items() if k != KEY_SUCCESS}
                return jsonify(settings)

            if request.method == "POST":
                # Use MCP client for updating settings
                # Handle different content types
                if (
                    request.content_type
                    and "application/x-www-form-urlencoded" in request.content_type
                ):
                    # Parse form data and normalize boolean strings
                    data = {}
                    for key, value in request.form.items():
                        # Convert string booleans to actual booleans
                        if isinstance(value, str) and value.lower() in (
                            "true",
                            "false",
                        ):
                            data[key] = value.lower() == "true"
                        else:
                            data[key] = value
                else:
                    # Default to JSON - force parsing even without content type
                    try:
                        data = request.get_json(force=True)
                    except Exception:
                        return jsonify({KEY_ERROR: "Invalid request data"}), 400

                # Validate settings data to maintain API contract
                valid_settings_keys = {
                    "gemini_model",
                    "openrouter_model",
                    "cerebras_model",
                    "openclaw_gateway_port",
                    "openclaw_gateway_url",
                    "openclaw_gateway_token",
                    "llm_provider",
                    "theme",
                    "auto_save",
                    "debug_mode",
                    "spicy_mode",
                    "pre_spicy_model",
                    "pre_spicy_provider",
                    "faction_minigame_enabled",
                    # BYOK API keys
                    "gemini_api_key",
                    "openrouter_api_key",
                    "cerebras_api_key",
                    # Avatar
                    "avatar_url",
                }
                if not data or not any(key in valid_settings_keys for key in data):
                    return jsonify({KEY_ERROR: "Invalid settings data"}), 400

                # Filter out invalid fields
                filtered_data = {
                    k: v for k, v in data.items() if k in valid_settings_keys
                }

                # Auto-infer provider from model selection if provider not explicitly set
                # This preserves legacy behavior for pure model-only updates while
                # avoiding accidental provider flips when settings payloads include
                # additional unrelated fields (e.g. openclaw_gateway_port).
                if "llm_provider" not in filtered_data:
                    model_keys = {
                        "gemini_model": constants.LLM_PROVIDER_GEMINI,
                        "openrouter_model": constants.LLM_PROVIDER_OPENROUTER,
                        "cerebras_model": constants.LLM_PROVIDER_CEREBRAS,
                    }
                    present_model_keys = model_keys.keys() & filtered_data.keys()

                    # Infer only when the payload is model-only (or solely model+provider fields).
                    # If other keys are present, leave llm_provider unchanged so
                    # callers can update misc settings without drifting provider state.
                    is_model_only_update = all(
                        key in model_keys or key == "llm_provider"
                        for key in filtered_data
                    )

                    if is_model_only_update and len(present_model_keys) == 1:
                        model_key = next(iter(present_model_keys))
                        filtered_data["llm_provider"] = (
                            constants.infer_provider_from_model(
                                filtered_data[model_key],
                                provider_hint=model_keys[model_key],
                            )
                        )

                # Auto-infer pre_spicy_provider from pre_spicy_model if not explicitly set
                if (
                    "pre_spicy_provider" not in filtered_data
                    and "pre_spicy_model" in filtered_data
                ):
                    # Infer provider from model name
                    filtered_data["pre_spicy_provider"] = (
                        constants.infer_provider_from_model(
                            filtered_data["pre_spicy_model"]
                        )
                    )

                request_data = {"user_id": user_id, "settings": filtered_data}

                # Use world_logic.update_user_settings_unified for validation
                result = await world_logic.update_user_settings_unified(request_data)

                if not result.get(KEY_SUCCESS):
                    return jsonify(result), result.get("status_code", 400)

                # Keep rate-limit BYOK decisions aligned with just-saved settings.
                rate_limiting.invalidate_user_settings_cache(user_id)

                # Return success response compatible with frontend expectations
                return jsonify({"success": True, "message": "Settings saved"})

        except MCPClientError as e:
            return handle_mcp_errors(e)
        except Exception as e:
            logging_util.error(f"Settings API error: {str(e)}")
            return jsonify({"error": "Internal server error", "success": False}), 500

    @app.route("/api/settings/reveal-key", methods=["POST"])
    @limiter.limit(settings_rate_limit)
    @check_token
    @async_route
    async def api_settings_reveal_key(
        user_id: UserId, user_email: str | None = None
    ) -> Response | tuple[Response, int]:
        """Reveal a stored BYOK key for the authenticated owner."""
        try:
            try:
                data = request.get_json(force=True) or {}
            except Exception:
                return jsonify({KEY_ERROR: "Invalid request data"}), 400

            provider = str(data.get("provider") or "").strip().lower()
            result = await world_logic.reveal_user_api_key_unified(
                {"user_id": user_id, "provider": provider}
            )
            if not result.get(KEY_SUCCESS):
                return jsonify(result), result.get("status_code", 400)

            response = jsonify(
                {
                    "success": True,
                    "provider": result.get("provider"),
                    "api_key": result.get("api_key", ""),
                }
            )
            response.headers["Cache-Control"] = "no-store, max-age=0"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            return response
        except Exception as e:
            logging_util.error(f"Settings reveal-key API error: {str(e)}")
            return jsonify({"error": "Internal server error", "success": False}), 500

    @app.route("/api/settings/personal-access-token", methods=["POST"])
    @limiter.limit(settings_rate_limit)
    @check_token
    @async_route
    async def api_settings_personal_access_token(
        user_id: UserId, user_email: str | None = None
    ) -> Response | tuple[Response, int]:
        """Generate or revoke a personal access token for programmatic MCP access.

        POST with {"action": "generate"} creates a new token, replacing any existing one.
        POST with {"action": "revoke"} deletes the existing token.
        The plaintext token is returned once on generate and never again.
        """
        del user_email
        try:
            try:
                data = request.get_json(force=True) or {}
            except Exception:
                return jsonify({KEY_ERROR: "Invalid request data"}), 400

            action = str(data.get("action", "generate")).strip().lower()

            if action == "revoke":
                # Atomic transaction: reads old hash inside txn, deletes key doc,
                # and clears pointer — concurrency-safe, no partial-failure window.
                revoked = await run_blocking_io(
                    firestore_service.revoke_personal_api_key, user_id
                )
                if not revoked:
                    return jsonify({KEY_ERROR: "Failed to revoke key"}), 500
                response = jsonify({"success": True, "revoked": True})
                response.headers["Cache-Control"] = "no-store, max-age=0"
                return response

            if action != "generate":
                return jsonify(
                    {KEY_ERROR: "action must be 'generate' or 'revoke'"}
                ), 400

            # Generate new key: "worldai_" prefix + 32 random bytes (64 hex chars)
            raw_key = "worldai_" + secrets.token_hex(32)
            key_hash = hashlib.sha256(raw_key.encode()).hexdigest()

            # Atomic transaction: reads old hash inside txn, deletes old key doc,
            # sets new key doc, and updates settings pointer — concurrency-safe.
            rotated = await run_blocking_io(
                firestore_service.rotate_personal_api_key, user_id, key_hash
            )
            if not rotated:
                return jsonify({KEY_ERROR: "Failed to generate key"}), 500

            response = jsonify({"success": True, "token": raw_key})
            response.headers["Cache-Control"] = "no-store, max-age=0"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            return response
        except Exception as e:
            logging_util.error(f"Settings personal-access-token API error: {str(e)}")
            return jsonify({"error": "Internal server error", "success": False}), 500

    @app.route("/api/settings/test-openclaw-connection", methods=["POST"])
    @limiter.limit(settings_rate_limit)
    @check_token
    @async_route
    async def api_settings_test_openclaw_connection(
        user_id: UserId, user_email: str | None = None
    ) -> Response | tuple[Response, int]:
        """Test OpenClaw gateway connection using current or provided settings."""
        del user_email
        try:
            try:
                payload = request.get_json(force=True) or {}
            except Exception:
                return jsonify({KEY_ERROR: "Invalid request data"}), 400

            settings_result = await world_logic.get_user_settings_unified(
                {"user_id": user_id}
            )
            if not isinstance(settings_result, dict) or not settings_result.get(
                KEY_SUCCESS
            ):
                message = (
                    settings_result.get(KEY_ERROR)
                    if isinstance(settings_result, dict)
                    else "Failed to load user settings"
                )
                status_code = (
                    settings_result.get("status_code", 502)
                    if isinstance(settings_result, dict)
                    else 502
                )
                return jsonify(
                    {KEY_ERROR: message or "Failed to load user settings"}
                ), status_code

            loaded_settings = {
                key: value
                for key, value in settings_result.items()
                if key != KEY_SUCCESS
            }

            gateway_port_raw = payload.get(
                "openclaw_gateway_port",
                loaded_settings.get(
                    "openclaw_gateway_port", constants.DEFAULT_OPENCLAW_GATEWAY_PORT
                ),
            )
            gateway_url_raw = payload.get(
                "openclaw_gateway_url", loaded_settings.get("openclaw_gateway_url", "")
            )
            gateway_token_raw = payload.get("openclaw_gateway_token")
            if (
                gateway_token_raw is None
                or gateway_token_raw == MASKED_API_KEY_PLACEHOLDER
            ):
                # get_user_settings_unified strips sensitive fields for the UI; read raw
                # Firestore settings to recover the actual gateway token for server-side use.
                _raw = await run_blocking_io(
                    firestore_service.get_user_settings, user_id
                )
                gateway_token_raw = (
                    (_raw or {}).get("openclaw_gateway_token", "") if _raw else ""
                )
            proof_prompt = payload.get("proof_prompt")
            if not isinstance(proof_prompt, str):
                proof_prompt = None

            gateway_url, url_error = validate_openclaw_gateway_url(gateway_url_raw)
            if url_error:
                return jsonify({KEY_ERROR: url_error}), 400
            gateway_port, port_error = validate_openclaw_gateway_port(gateway_port_raw)
            if port_error:
                return jsonify({KEY_ERROR: port_error}), 400
            gateway_token, token_error = validate_openclaw_gateway_token(
                gateway_token_raw
            )
            if token_error:
                return jsonify({KEY_ERROR: token_error}), 400

            result = openclaw_provider.test_openclaw_gateway_connection(
                gateway_url=gateway_url,
                gateway_port=gateway_port,
                gateway_token=gateway_token,
                proof_prompt=proof_prompt,
            )
            if not result.get("success"):
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": result.get(
                                "message", "OpenClaw gateway connection failed"
                            ),
                            "status_code": result.get("status_code"),
                            "gateway_url": result.get("gateway_url"),
                            "mode": result.get("mode"),
                        }
                    ),
                    502,
                )

            # Emit proof hash so preview-side logs can be correlated with client evidence.
            if result.get("response_hash"):
                logging_util.info(
                    "OpenClaw connection proof hash user=%s hash=%s",
                    user_id,
                    result.get("response_hash"),
                )

            return jsonify(
                {
                    "success": True,
                    "message": "OpenClaw gateway connection succeeded",
                    "gateway_url": result.get("gateway_url"),
                    "status_code": result.get("status_code"),
                    "mode": result.get("mode"),
                    "response_hash": result.get("response_hash"),
                    "proof_prompt_used": result.get("proof_prompt_used", False),
                    "response_text_preview": result.get("response_text_preview"),
                }
            )
        except Exception as e:
            logging_util.error(f"Settings test-openclaw-connection API error: {str(e)}")
            return jsonify({"error": "Internal server error", "success": False}), 500

    @app.route("/api/constants/models", methods=["GET"])
    @limiter.limit(settings_rate_limit)
    @check_token
    def get_model_constants(user_id: UserId, user_email: str | None = None) -> Response:  # noqa: ARG001
        """Expose model defaults to keep frontend aligned with backend constants."""

        return jsonify(
            {
                "SPICY_MODEL": constants.SPICY_OPENROUTER_MODEL,
                "DEFAULT_GEMINI_MODEL": constants.DEFAULT_GEMINI_MODEL,
                "DEFAULT_OPENROUTER_MODEL": constants.DEFAULT_OPENROUTER_MODEL,
                "DEFAULT_CEREBRAS_MODEL": constants.DEFAULT_CEREBRAS_MODEL,
            }
        )

    # --- Avatar Management ---
    @app.route("/api/avatar", methods=["POST"])
    @limiter.limit(settings_rate_limit)
    @check_token
    @async_route
    async def upload_avatar(
        user_id: UserId, user_email: str | None = None
    ) -> Response | tuple[Response, int]:
        """Upload user avatar image."""
        del user_email
        try:
            if "file" not in request.files:
                return jsonify({"success": False, "error": "No file provided"}), 400

            file = request.files["file"]
            if file.filename == "":
                return jsonify({"success": False, "error": "No file selected"}), 400

            # Validate file type
            expected_extension = AVATAR_CONTENT_TYPES.get(file.content_type)
            if not expected_extension:
                return (
                    jsonify({"success": False, "error": "Invalid file type"}),
                    400,
                )

            # Validate file size (max 5MB)
            max_size = 5 * 1024 * 1024
            if request.content_length is not None and request.content_length > (
                max_size + 1024 * 1024
            ):
                return (
                    jsonify({"success": False, "error": "File too large (max 5MB)"}),
                    400,
                )

            file_data = _read_stream_with_limit(file.stream, max_size)
            if file_data is None:
                return (
                    jsonify({"success": False, "error": "File too large (max 5MB)"}),
                    400,
                )

            detected_extension = _detect_image_extension(file_data)
            if not detected_extension or detected_extension != expected_extension:
                return (
                    jsonify({"success": False, "error": "Invalid image content"}),
                    400,
                )

            # Upload to Firebase Storage
            avatar_url = firestore_service.upload_user_avatar(
                user_id, file_data, file.content_type, detected_extension
            )

            # Save URL to user settings via MCP
            request_data = {"user_id": user_id, "settings": {"avatar_url": avatar_url}}
            result = await get_mcp_client().call_tool(
                "update_user_settings", request_data
            )

            if not result.get(KEY_SUCCESS):
                return jsonify(result), result.get("status_code", 400)

            return jsonify({"success": True, "avatar_url": avatar_url})

        except MCPClientError as e:
            return handle_mcp_errors(e)
        except Exception as e:
            logging_util.error(f"Avatar upload error: {str(e)}")
            return jsonify({"error": "Internal server error", "success": False}), 500

    @app.route("/api/avatar", methods=["DELETE"])
    @limiter.limit(settings_rate_limit)
    @check_token
    @async_route
    async def delete_avatar(
        user_id: UserId, user_email: str | None = None
    ) -> Response | tuple[Response, int]:
        """Delete user avatar."""
        del user_email
        try:
            # Delete from Firebase Storage
            firestore_service.delete_user_avatar(user_id)

            # Remove URL from user settings via MCP
            request_data = {"user_id": user_id, "settings": {"avatar_url": None}}
            result = await get_mcp_client().call_tool(
                "update_user_settings", request_data
            )

            if not result.get(KEY_SUCCESS):
                return jsonify(result), result.get("status_code", 400)

            try:
                await run_blocking_io(firestore_service.delete_user_avatar, user_id)
            except Exception as exc:  # noqa: BLE001 - best-effort storage cleanup
                logging_util.warning(f"Failed to delete avatar from storage: {exc}")

            return jsonify({"success": True})

        except MCPClientError as e:
            return handle_mcp_errors(e)
        except Exception as e:
            logging_util.error(f"Avatar delete error: {str(e)}")
            return jsonify({"error": "Internal server error", "success": False}), 500

    @app.route("/api/campaign/<campaign_id>/avatar", methods=["POST"])
    @limiter.limit(settings_rate_limit)
    @check_token
    @async_route
    async def upload_campaign_avatar_route(
        campaign_id: str, user_id: UserId, user_email: str | None = None
    ) -> Response | tuple[Response, int]:
        """Upload avatar for a specific campaign."""
        del user_email
        try:
            if "avatar" not in request.files:
                return jsonify({"success": False, "error": "No file provided"}), 400

            file = request.files["avatar"]
            if file.filename == "":
                return jsonify({"success": False, "error": "No file selected"}), 400

            # Validate file type
            expected_extension = AVATAR_CONTENT_TYPES.get(file.content_type)
            if not expected_extension:
                return (
                    jsonify({"success": False, "error": "Invalid file type"}),
                    400,
                )

            # Validate file size (max 5MB)
            max_size = 5 * 1024 * 1024
            file_data = _read_stream_with_limit(file.stream, max_size)
            if file_data is None:
                return (
                    jsonify({"success": False, "error": "File too large (max 5MB)"}),
                    400,
                )

            detected_extension = _detect_image_extension(file_data)
            if not detected_extension or detected_extension != expected_extension:
                return (
                    jsonify({"success": False, "error": "Invalid image content"}),
                    400,
                )

            # Upload to Firebase Storage
            avatar_url = firestore_service.upload_campaign_avatar(
                user_id, campaign_id, file_data, file.content_type
            )

            # Store avatar_url in the campaign document
            db = firestore_service.get_db()
            campaign_ref = (
                db.collection("users")
                .document(user_id)
                .collection("campaigns")
                .document(campaign_id)
            )
            campaign_ref.update({"avatar_url": avatar_url})

            return jsonify({"success": True, "avatar_url": avatar_url})

        except Exception as e:
            import traceback

            logging_util.error(
                f"Campaign avatar upload error: {str(e)}\n{traceback.format_exc()}"
            )
            return jsonify({"error": "Internal server error", "success": False}), 500

    @app.route("/api/campaign/<campaign_id>/avatar", methods=["DELETE"])
    @limiter.limit(settings_rate_limit)
    @check_token
    @async_route
    async def delete_campaign_avatar_route(
        campaign_id: str, user_id: UserId, user_email: str | None = None
    ) -> Response | tuple[Response, int]:
        """Delete avatar for a specific campaign."""
        del user_email
        try:
            # Delete from Firebase Storage
            firestore_service.delete_campaign_avatar(user_id, campaign_id)

            # Clear avatar_url in the campaign document
            db = firestore_service.get_db()
            campaign_ref = (
                db.collection("users")
                .document(user_id)
                .collection("campaigns")
                .document(campaign_id)
            )
            campaign_ref.update(
                {"avatar_url": firestore_service.firestore.DELETE_FIELD}
            )

            return jsonify({"success": True})

        except Exception as e:
            logging_util.error(f"Campaign avatar delete error: {str(e)}")
            return jsonify({"error": "Internal server error", "success": False}), 500

    @app.route("/api/avatar", methods=["GET"])
    @limiter.limit(settings_rate_limit)
    @check_token
    @async_route
    async def download_avatar(
        user_id: UserId, user_email: str | None = None
    ) -> Response | tuple[Response, int]:
        """Download the authenticated user's avatar image."""
        del user_email
        try:
            # Fetch stored avatar_url from user settings to avoid GCS probe.
            user_settings = await run_blocking_io(
                firestore_service.get_user_settings, user_id
            )
            avatar_url_hint = (user_settings or {}).get("avatar_url")
            data, content_type = await run_blocking_io(
                firestore_service.download_user_avatar,
                user_id,
                avatar_url_from_firestore=avatar_url_hint,
            )

            ext = AVATAR_CONTENT_TYPES.get(content_type, "png")
            filename = f"avatar.{ext}"
            response = make_response(data)
            response.headers["Content-Type"] = content_type
            response.headers["Content-Disposition"] = f"attachment; filename={filename}"
            response.headers["Cache-Control"] = "private, max-age=60"
            return response

        except ValueError:
            return jsonify({"success": False, "error": "Avatar not found"}), 404
        except Exception as e:
            logging_util.error(f"User avatar download error: {str(e)}")
            return jsonify({"error": "Internal server error", "success": False}), 500

    @app.route("/api/campaign/<campaign_id>/avatar", methods=["GET"])
    @limiter.limit(settings_rate_limit)
    @check_token
    @async_route
    async def download_campaign_avatar_route(
        campaign_id: str, user_id: UserId, user_email: str | None = None
    ) -> Response | tuple[Response, int]:
        """Download a campaign's avatar image."""
        del user_email
        try:
            # Fetch stored avatar_url from campaign document to avoid GCS probe.
            campaign_meta = await run_blocking_io(
                firestore_service.get_campaign_metadata, user_id, campaign_id
            )
            avatar_url_hint = (campaign_meta or {}).get("avatar_url")
            data, content_type = await run_blocking_io(
                firestore_service.download_campaign_avatar,
                user_id,
                campaign_id,
                avatar_url_from_firestore=avatar_url_hint,
            )

            ext = AVATAR_CONTENT_TYPES.get(content_type, "png")
            filename = f"campaign_avatar.{ext}"
            response = make_response(data)
            response.headers["Content-Type"] = content_type
            response.headers["Content-Disposition"] = f"attachment; filename={filename}"
            response.headers["Cache-Control"] = "private, max-age=60"
            return response

        except ValueError:
            return jsonify({"success": False, "error": "Avatar not found"}), 404
        except Exception as e:
            logging_util.error(f"Campaign avatar download error: {str(e)}")
            return jsonify({"error": "Internal server error", "success": False}), 500

    # --- Frontend Serving ---
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    @limiter.exempt  # Exempt frontend routes from rate limiting
    def serve_frontend(path: str) -> Response:
        """Serve the frontend files with cache-aware HTML headers."""
        frontend_folder = _resolve_frontend_folder()
        fallback_frontend_folder = os.path.join(
            os.path.dirname(__file__), "frontend_v1"
        )

        # Serve non-HTML files directly (no special cache headers)
        if (
            path
            and not path.endswith(".html")
            and os.path.exists(os.path.join(frontend_folder, path))
        ):
            response = send_from_directory(frontend_folder, path)
            response.direct_passthrough = False
            return response

        # Serve HTML (either explicit /index.html or SPA fallback for /)
        # Cache busting handled at build/deploy time, not runtime
        if path and path.endswith(".html"):
            candidate = os.path.join(frontend_folder, path)
            if os.path.exists(candidate):
                response = send_from_directory(frontend_folder, path)
            else:
                fallback_candidate = os.path.join(fallback_frontend_folder, path)
                if os.path.exists(fallback_candidate):
                    response = send_from_directory(fallback_frontend_folder, path)
                else:
                    response = send_from_directory(frontend_folder, "index.html")
        else:
            response = send_from_directory(frontend_folder, "index.html")
        response.direct_passthrough = False

        # HTML must never be cached — cached HTML may reference old hashed
        # assets that no longer exist, causing 404s after deployments.
        # Content-hashed assets (JS/CSS) get long cache via /frontend_v1/ route.
        response.headers["Cache-Control"] = "no-cache, must-revalidate"
        return response

    # Fallback route for old cached frontend code calling /handle_interaction
    @app.route("/handle_interaction", methods=["POST"])
    @limiter.limit(
        "30000 per hour, 1000 per minute"
    )  # Match main interaction endpoint limits
    def handle_interaction_fallback():
        """Fallback for cached frontend code calling old endpoint"""
        return jsonify(
            {
                "error": "This endpoint has been moved. Please refresh your browser (Ctrl+Shift+R) to get the latest version.",
                "redirect_message": "Hard refresh required to clear browser cache",
                "status": "cache_issue",
            }
        ), 410  # 410 Gone - indicates this endpoint no longer exists

    @app.teardown_appcontext
    def cleanup_mcp_client(exception):  # noqa: ARG001
        """Cleanup MCP client session on app context teardown"""
        # Note: Since mcp_client is created at app startup and reused,
        # we don't close it here to avoid issues with subsequent requests.
        # The session will be closed when the app shuts down.

    # Register cleanup handler for app shutdown
    def cleanup_resources():
        """Cleanup resources on app shutdown"""
        # Close file handlers to prevent ResourceWarning
        root_logger = logging_util.getLogger()
        for handler in root_logger.handlers[:]:
            if isinstance(handler, logging_util.FileHandler):
                try:
                    handler.close()
                    root_logger.removeHandler(handler)
                except Exception as e:
                    logging_util.error(f"Error closing file handler: {e}")

        # Close MCP client session
        if (
            app._mcp_client
            and hasattr(app._mcp_client, "session")
            and app._mcp_client.session
        ):
            try:
                app._mcp_client.session.close()
                logging_util.info("Closed MCP client session")
            except Exception as e:
                logging_util.error(f"Error closing MCP client session: {e}")

    atexit.register(cleanup_resources)

    return app


def run_test_command(command: str) -> None:
    """
    Run a test command.

    Args:
        command: The test command to run ('testui', 'testuif', 'testhttp', 'testhttpf')
    """
    if command == "testui":
        # Run browser tests with mock APIs
        test_runner = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "testing_ui",
            "run_all_browser_tests.py",
        )
        if os.path.exists(test_runner):
            logging_util.info(
                "🌐 Running WorldArchitect.AI Browser Tests (Mock APIs)..."
            )
            logging_util.info("   Using real browser automation with mocked backend")
            browser_timeout = int(os.environ.get("BROWSER_TEST_TIMEOUT", "300"))
            result = subprocess.run(
                [sys.executable, test_runner],
                shell=False,
                timeout=browser_timeout,
                check=False,
            )
            sys.exit(result.returncode)
        else:
            logging_util.error(f"Test runner not found: {test_runner}")
            sys.exit(1)

    elif command == "testuif":
        # Run browser tests with REAL APIs
        test_runner = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "testing_ui",
            "run_all_browser_tests.py",
        )
        if os.path.exists(test_runner):
            logging_util.info(
                "🌐 Running WorldArchitect.AI Browser Tests (REAL APIs)..."
            )
            logging_util.warning(
                "⚠️  WARNING: These tests use REAL APIs and cost money!"
            )
            env = os.environ.copy()
            env["REAL_APIS"] = "true"
            # Real API tests need longer timeout (5 min default)
            full_api_timeout = int(os.environ.get("FULL_API_TEST_TIMEOUT", "300"))
            result = subprocess.run(
                [sys.executable, test_runner],
                shell=False,
                timeout=full_api_timeout,
                check=False,
                env=env,
            )
            sys.exit(result.returncode)
        else:
            logging_util.error(f"Test runner not found: {test_runner}")
            sys.exit(1)

    elif command == "testhttp":
        # Run HTTP tests with mock APIs
        test_runner = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "testing_http",
            "run_all_http_tests.py",
        )
        if os.path.exists(test_runner):
            logging_util.info("🔗 Running WorldArchitect.AI HTTP Tests (Mock APIs)...")
            logging_util.info("   Using direct HTTP requests with mocked backend")
            http_timeout = int(os.environ.get("HTTP_TEST_TIMEOUT", "300"))
            result = subprocess.run(
                [sys.executable, test_runner],
                shell=False,
                timeout=http_timeout,
                check=False,
            )
            sys.exit(result.returncode)
        else:
            logging_util.error(f"Test runner not found: {test_runner}")
            sys.exit(1)

    elif command == "testhttpf":
        # Run HTTP tests with REAL APIs
        test_runner = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "testing_http",
            "testing_full",
            "run_all_full_tests.py",
        )
        if os.path.exists(test_runner):
            logging_util.info("🔗 Running WorldArchitect.AI HTTP Tests (REAL APIs)...")
            logging_util.warning(
                "⚠️  WARNING: These tests use REAL APIs and cost money!"
            )
            # Real API tests need longer timeout (5 min default)
            full_api_timeout = int(os.environ.get("FULL_API_TEST_TIMEOUT", "300"))
            result = subprocess.run(
                [sys.executable, test_runner],
                shell=False,
                timeout=full_api_timeout,
                check=False,
            )
            sys.exit(result.returncode)
        else:
            logging_util.error(f"Full API test runner not found: {test_runner}")
            sys.exit(1)

    else:
        logging_util.error(f"Unknown test command: {command}")
        sys.exit(1)


# Don't create global app instance - let each execution context create its own
app = None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="World Architect AI Server & Tools")
    parser.add_argument(
        "command",
        nargs="?",
        default="serve",
        help="Command to run ('serve', 'testui', 'testuif', 'testhttp', or 'testhttpf')",
    )
    parser.add_argument(
        "--mcp-http",
        action="store_true",
        help="Use HTTP communication with MCP server (default: direct calls)",
    )
    parser.add_argument(
        "--mcp-server-url",
        default="http://localhost:8000",
        help="MCP server URL (default: http://localhost:8000)",
    )

    # Check for test commands first
    if len(sys.argv) > 1 and sys.argv[1] in [
        "testui",
        "testuif",
        "testhttp",
        "testhttpf",
    ]:
        run_test_command(sys.argv[1])
    else:
        # Standard server execution
        args = parser.parse_args()
        if args.command == "serve":
            # Create app instance with MCP configuration for serve command
            app = create_app()
            # Skip MCP HTTP calls unless explicitly requested via CLI
            app._skip_mcp_http = not args.mcp_http
            app._mcp_server_url = args.mcp_server_url

            # Robust port parsing to handle descriptive PORT environment variables
            def parse_port_robust(port_string):
                """
                Parse port number from environment variable that may contain descriptive text.
                Handles cases like: "ℹ️ Port 8081 in use, trying 8082...\n8082"
                """
                default_port = 8081

                if not port_string or not isinstance(port_string, str):
                    return default_port

                # Clean the string - remove extra whitespace and newlines
                port_string = port_string.strip()

                # Try direct conversion first (normal case)
                try:
                    return int(port_string)
                except ValueError:
                    pass

                # Extract all numbers from the string
                numbers = re.findall(r"\d+", port_string)

                if not numbers:
                    return default_port

                # Use the last number found (often the actual port after conflicts)
                try:
                    port = int(numbers[-1])
                    # Validate port range
                    if 1024 <= port <= 65535:
                        return port
                    return default_port
                except (ValueError, IndexError):
                    return default_port

            port = parse_port_robust(os.environ.get("PORT", "8081"))
            mode = (
                "direct calls"
                if app._skip_mcp_http
                else f"HTTP to {app._mcp_server_url}"
            )
            logging_util.info(
                f"Development server running: http://localhost:{port} (MCP: {mode})"
            )
            debug_enabled = (
                os.getenv("WORLDAI_FLASK_DEBUG", "true").strip().lower() == "true"
            )
            use_reloader = (
                os.getenv("WORLDAI_USE_RELOADER", "true").strip().lower() == "true"
            )
            app.run(
                host="0.0.0.0",
                port=port,
                debug=debug_enabled,
                use_reloader=use_reloader,
            )
        elif args.command in ["testui", "testuif", "testhttp", "testhttpf"]:
            run_test_command(args.command)
        else:
            parser.error(f"Unknown command: {args.command}")

# Create app instance for module-level imports (like gunicorn)
if app is None:
    app = create_app()

"""
Rate Limiting Logic

This module handles rate limiting logic for the application.
It separates the business logic of rate limiting from the general Firestore service.
"""

import os
import threading
import time
from typing import Any

from cachetools import TTLCache
from firebase_admin import firestore

from mvp_site import constants, logging_util
from mvp_site.custom_types import UserId
from mvp_site.decorators import log_exceptions
from mvp_site.firestore_service import get_user_settings

try:
    from google.api_core.exceptions import GoogleAPIError
except ImportError:
    # Avoid catching all exceptions as "infrastructure errors" when google libs aren't present.
    class GoogleAPIError(Exception):
        pass


def _parse_rate_limit_exempt_emails(raw_emails: str | None) -> set[str]:
    """Parse comma-separated list of exempt emails."""
    if not raw_emails:
        return set()
    return {
        email.strip().lower()
        for email in raw_emails.split(",")
        if email and email.strip()
    }


# Exempt users (no rate limits). Configure via `RATE_LIMIT_EXEMPT_EMAILS` (comma-separated).
RATE_LIMIT_EXEMPT_EMAILS: set[str] = _parse_rate_limit_exempt_emails(
    os.environ.get("RATE_LIMIT_EXEMPT_EMAILS")
)
# Always exempt jleechan@gmail.com as a default
RATE_LIMIT_EXEMPT_EMAILS.add("jleechan@gmail.com")
if os.getenv("TESTING_AUTH_BYPASS") == "true":
    RATE_LIMIT_EXEMPT_EMAILS.add("test@example.com")
    RATE_LIMIT_EXEMPT_EMAILS.add("jleechantest@gmail.com")  # MCP test default

# Contact email for rate limit escalation
RATE_LIMIT_CONTACT_EMAIL = os.environ.get(
    "RATE_LIMIT_CONTACT_EMAIL", "jleechan@gmail.com"
)

# Rate limit configuration (configurable via environment variables for testing)
RATE_LIMIT_DAILY_TURNS = int(
    os.environ.get("RATE_LIMIT_DAILY_TURNS", "50")
)  # Max turns per 24 hours
RATE_LIMIT_5HOUR_TURNS = int(
    os.environ.get("RATE_LIMIT_5HOUR_TURNS", "25")
)  # Max turns per 5 hours
# Keep BYOK limits deploy-tunable while guaranteeing they are never lower than defaults.
RATE_LIMIT_BYOK_PROVIDER_DAILY_TURNS = max(
    RATE_LIMIT_DAILY_TURNS,
    int(
        os.environ.get(
            "RATE_LIMIT_BYOK_PROVIDER_DAILY_TURNS",
            str(constants.RATE_LIMIT_BYOK_PROVIDER_DAILY_TURNS),
        )
    ),
)
RATE_LIMIT_BYOK_PROVIDER_5HOUR_TURNS = max(
    RATE_LIMIT_5HOUR_TURNS,
    int(
        os.environ.get(
            "RATE_LIMIT_BYOK_PROVIDER_5HOUR_TURNS",
            str(constants.RATE_LIMIT_BYOK_PROVIDER_5HOUR_TURNS),
        )
    ),
)
RATE_LIMIT_DAILY_WINDOW_SECONDS = 24 * 60 * 60  # 24 hours
RATE_LIMIT_5HOUR_WINDOW_SECONDS = 5 * 60 * 60  # 5 hours

_USER_SETTINGS_CACHE_TTL_SECONDS = constants.RATE_LIMIT_USER_SETTINGS_CACHE_TTL_SECONDS
_USER_SETTINGS_CACHE_MAX_SIZE = 4096
_USER_SETTINGS_CACHE: TTLCache = TTLCache(
    maxsize=_USER_SETTINGS_CACHE_MAX_SIZE,
    ttl=_USER_SETTINGS_CACHE_TTL_SECONDS,
)
_USER_SETTINGS_CACHE_LOCK = threading.Lock()

_FIRESTORE_TRANSACTION_ATTRS = (
    "_begin", "_commit", "_rollback", "_clean_up", "_max_attempts", "_read_only",
)


def is_byok_provider_active(user_settings: dict[str, Any] | None) -> bool:
    """Return True when a stored BYOK key matches the active provider."""
    settings = user_settings if isinstance(user_settings, dict) else {}
    active_provider = str(
        settings.get("llm_provider") or constants.DEFAULT_LLM_PROVIDER
    ).strip().lower()
    if active_provider not in constants.ALLOWED_LLM_PROVIDERS:
        return False

    byok_key_value = settings.get(f"{active_provider}_api_key")
    return isinstance(byok_key_value, str) and bool(byok_key_value.strip())


def _get_user_settings_cached(user_id: UserId) -> dict[str, Any]:
    """Return user settings with a short-lived, bounded in-process cache."""
    with _USER_SETTINGS_CACHE_LOCK:
        cached_settings = _USER_SETTINGS_CACHE.get(user_id)
        if isinstance(cached_settings, dict):
            return cached_settings

    settings = get_user_settings(user_id) or {}

    with _USER_SETTINGS_CACHE_LOCK:
        _USER_SETTINGS_CACHE[user_id] = settings

    return settings


def invalidate_user_settings_cache(user_id: UserId) -> None:
    """Invalidate cached settings for a specific user."""
    with _USER_SETTINGS_CACHE_LOCK:
        _USER_SETTINGS_CACHE.pop(user_id, None)


def _get_user_turn_limits(user_id: UserId) -> tuple[int, int]:
    """Return (daily_limit, window_limit) for a user. BYOK users get elevated limits."""
    settings = _get_user_settings_cached(user_id)
    if is_byok_provider_active(settings):
        return RATE_LIMIT_BYOK_PROVIDER_DAILY_TURNS, RATE_LIMIT_BYOK_PROVIDER_5HOUR_TURNS
    return RATE_LIMIT_DAILY_TURNS, RATE_LIMIT_5HOUR_TURNS


def is_rate_limit_exempt(user_email: str | None) -> bool:
    """Check if user email is exempt from rate limiting."""
    if not user_email:
        return False
    return user_email.lower() in RATE_LIMIT_EXEMPT_EMAILS


def _is_firestore_transaction(transaction: Any) -> bool:
    return all(hasattr(transaction, attr) for attr in _FIRESTORE_TRANSACTION_ATTRS)


def _evaluate_rate_limit(
    turn_timestamps: list[float],
    daily_cutoff: float,
    window_cutoff: float,
    current_time: float,
    daily_limit: int,
    window_limit: int,
) -> dict[str, Any] | None:
    """Evaluate timestamps against limits. Returns blocked response or None if allowed."""
    daily_turns = [ts for ts in turn_timestamps if ts > daily_cutoff]
    window_turns = [ts for ts in turn_timestamps if ts > window_cutoff]

    daily_count = len(daily_turns)
    window_count = len(window_turns)

    window_remaining = max(0, window_limit - window_count)

    if daily_count >= daily_limit:
        return {
            "allowed": False,
            "error_type": "rate_limit",
            "error_message": (
                f"You've reached your daily limit of {daily_limit} turns. "
                "Your limit will reset in 24 hours. "
                "Want unlimited turns? Add your own API key in Settings."
            ),
            "daily_remaining": 0,
            "hourly_remaining": window_remaining,
            "reset_time_daily": int(
                min(daily_turns) + RATE_LIMIT_DAILY_WINDOW_SECONDS
            )
            if daily_turns
            else None,
        }

    daily_remaining = max(0, daily_limit - daily_count)

    if window_count >= window_limit:
        oldest_in_window = min(window_turns) if window_turns else current_time
        reset_minutes = int(
            (oldest_in_window + RATE_LIMIT_5HOUR_WINDOW_SECONDS - current_time) / 60
        )
        return {
            "allowed": False,
            "error_type": "rate_limit",
            "error_message": (
                f"You've reached your limit of {window_limit} turns per 5 hours. "
                f"Your limit will reset in about {reset_minutes} minutes. "
                "Want unlimited turns? Add your own API key in Settings."
            ),
            "daily_remaining": daily_remaining,
            "hourly_remaining": 0,
            "reset_time_hourly": int(
                oldest_in_window + RATE_LIMIT_5HOUR_WINDOW_SECONDS
            ),
        }

    return None


def _build_allowed_response(
    turn_timestamps: list[float],
    daily_cutoff: float,
    window_cutoff: float,
    daily_limit: int,
    window_limit: int,
) -> dict[str, Any]:
    """Build the allowed response with remaining counts from timestamps."""
    daily_count = len([ts for ts in turn_timestamps if ts > daily_cutoff])
    window_count = len([ts for ts in turn_timestamps if ts > window_cutoff])
    return {
        "allowed": True,
        "daily_remaining": max(0, daily_limit - daily_count),
        "hourly_remaining": max(0, window_limit - window_count),
    }


@log_exceptions
def check_rate_limit(  # noqa: PLR0915
    user_id: UserId,
    user_email: str | None = None,
    consume_turn: bool = False,
) -> dict[str, Any]:
    """Check if user has exceeded rate limits.

    Tracks turn usage in Firestore and returns rate limit status.

    Args:
        user_id: Firebase user ID
        user_email: User's email for exemption check
        consume_turn: Whether to record a turn consumption

    Returns:
        dict with keys:
            - allowed: bool - whether the action is allowed
            - error_type: str - "rate_limit" if blocked
            - error_message: str - user-friendly message if blocked
            - daily_remaining: int - turns remaining in 24h window
            - hourly_remaining: int - turns remaining in 5h window
    """
    # Import get_db here to avoid circular imports with firestore_service
    from mvp_site.firestore_service import get_db

    # Check exemptions first
    if is_rate_limit_exempt(user_email):
        return {
            "allowed": True,
            "daily_remaining": -1,  # Unlimited
            "hourly_remaining": -1,  # Unlimited
        }

    db = get_db()
    daily_limit, window_limit = _get_user_turn_limits(user_id)
    current_time = time.time()
    daily_cutoff = current_time - RATE_LIMIT_DAILY_WINDOW_SECONDS
    window_cutoff = current_time - RATE_LIMIT_5HOUR_WINDOW_SECONDS

    rate_limit_ref = db.collection("rate_limits").document(user_id)

    def _check_and_maybe_consume(turn_timestamps: list[float], write_fn) -> dict[str, Any]:
        """Shared logic for both transactional and non-transactional paths."""
        blocked = _evaluate_rate_limit(
            turn_timestamps, daily_cutoff, window_cutoff, current_time,
            daily_limit, window_limit,
        )
        if blocked:
            return blocked

        if consume_turn:
            pruned = [ts for ts in turn_timestamps if ts > daily_cutoff]
            pruned.append(current_time)
            write_fn(pruned)
            return _build_allowed_response(
                pruned, daily_cutoff, window_cutoff, daily_limit, window_limit,
            )

        return _build_allowed_response(
            turn_timestamps, daily_cutoff, window_cutoff, daily_limit, window_limit,
        )

    def _non_transactional_check() -> dict[str, Any]:
        rate_limit_doc = rate_limit_ref.get()
        data = rate_limit_doc.to_dict() if rate_limit_doc else None
        turn_timestamps = (data or {}).get("turn_timestamps", [])

        def write_fn(pruned_timestamps):
            payload = {
                "turn_timestamps": pruned_timestamps,
                "last_updated": firestore.SERVER_TIMESTAMP,
                "user_id": user_id,
            }
            try:
                rate_limit_ref.set(payload, merge=True)
            except TypeError:
                rate_limit_ref.set(payload)

        return _check_and_maybe_consume(turn_timestamps, write_fn)

    @firestore.transactional
    def transactional_check(transaction: firestore.Transaction) -> dict[str, Any]:
        rate_limit_doc = transaction.get(rate_limit_ref)
        if rate_limit_doc.exists:
            turn_timestamps = rate_limit_doc.to_dict().get("turn_timestamps", [])
        else:
            turn_timestamps = []

        def write_fn(pruned_timestamps):
            transaction.set(
                rate_limit_ref,
                {
                    "turn_timestamps": pruned_timestamps,
                    "last_updated": firestore.SERVER_TIMESTAMP,
                    "user_id": user_id,
                },
                merge=True,
            )

        return _check_and_maybe_consume(turn_timestamps, write_fn)

    try:
        transaction = None
        if hasattr(db, "transaction"):
            transaction = db.transaction()
        if transaction and _is_firestore_transaction(transaction):
            return transactional_check(transaction)
        # Fallback for fake or non-transactional Firestore clients (tests).
        return _non_transactional_check()
    except GoogleAPIError as e:
        # Infrastructure error (e.g., Firestore unavailable) - fail open to prioritize availability
        logging_util.warning(f"Rate limit check failed (infrastructure): {e}")
        return {
            "allowed": True,
            "daily_remaining": -1,
            "hourly_remaining": -1,
        }
    except Exception as e:
        # Unexpected error (e.g., bug in logic) - fail closed to prevent bypass
        logging_util.error(f"Rate limit check failed (unexpected): {e}")
        return {
            "allowed": False,
            "error_type": "rate_limit_error",
            "error_message": (
                "An unexpected error occurred while checking rate limits. "
                f"Please try again or contact {RATE_LIMIT_CONTACT_EMAIL}."
            ),
            "daily_remaining": 0,
            "hourly_remaining": 0,
        }


@log_exceptions
def record_turn_usage(user_id: UserId) -> bool:
    """Record a turn usage for rate limiting purposes.

    Args:
        user_id: Firebase user ID

    Returns:
        bool: True if recorded successfully
    """
    # Import get_db here to avoid circular imports
    from mvp_site.firestore_service import get_db

    db = get_db()
    current_time = time.time()
    daily_cutoff = current_time - RATE_LIMIT_DAILY_WINDOW_SECONDS

    rate_limit_ref = db.collection("rate_limits").document(user_id)

    def _do_record(turn_timestamps: list[float], write_fn) -> bool:
        pruned = [ts for ts in turn_timestamps if ts > daily_cutoff]
        pruned.append(current_time)
        write_fn(pruned)
        logging_util.debug(
            f"Recorded turn for user {user_id}. Total turns in window: {len(pruned)}"
        )
        return True

    def _non_transactional_record() -> bool:
        rate_limit_doc = rate_limit_ref.get()
        data = rate_limit_doc.to_dict() if rate_limit_doc else None
        turn_timestamps = (data or {}).get("turn_timestamps", [])

        def write_fn(pruned):
            payload = {
                "turn_timestamps": pruned,
                "last_updated": firestore.SERVER_TIMESTAMP,
                "user_id": user_id,
            }
            try:
                rate_limit_ref.set(payload, merge=True)
            except TypeError:
                rate_limit_ref.set(payload)

        return _do_record(turn_timestamps, write_fn)

    @firestore.transactional
    def transactional_record(transaction: firestore.Transaction) -> bool:
        rate_limit_doc = transaction.get(rate_limit_ref)
        if rate_limit_doc.exists:
            turn_timestamps = rate_limit_doc.to_dict().get("turn_timestamps", [])
        else:
            turn_timestamps = []

        def write_fn(pruned):
            transaction.set(
                rate_limit_ref,
                {
                    "turn_timestamps": pruned,
                    "last_updated": firestore.SERVER_TIMESTAMP,
                    "user_id": user_id,
                },
                merge=True,
            )

        return _do_record(turn_timestamps, write_fn)

    try:
        transaction = None
        if hasattr(db, "transaction"):
            transaction = db.transaction()
        if transaction and _is_firestore_transaction(transaction):
            return transactional_record(transaction)
        # Fallback for fake or non-transactional Firestore clients (tests).
        return _non_transactional_record()
    except Exception as e:
        logging_util.error(f"Failed to record turn for user {user_id}: {e}")
        return False

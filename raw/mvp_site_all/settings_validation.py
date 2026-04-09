"""
Settings validation helpers extracted from world_logic.py.

This module centralizes all user settings validation logic for reuse
across the API layer, MCP tools, and other entry points.

All validation functions return a tuple of (validated_value, error_message).
On success: (value, None)
On failure: (None, error_message)
"""

import os
import socket
from ipaddress import IPv4Address, IPv6Address, ip_address
from urllib.parse import urlsplit
from typing import Any

from mvp_site import constants


def _is_tsnet_hostname(hostname: str) -> bool:
    """Return True if the hostname uses the `.ts.net` suffix."""
    lowered = hostname.lower().strip().rstrip(".")
    return lowered.endswith(".ts.net")


def _is_disallowed_gateway_hostname(hostname: str) -> str | None:
    lowered = hostname.lower().strip()
    if not lowered:
        return "OpenClaw gateway hostname is required"
    if lowered in {
        "localhost",
        "localhost.local",
        "localhost.localdomain",
        "localhost4",
        "localhost4.localdomain4",
        "localhost6",
        "localhost6.localdomain6",
    }:
        return "OpenClaw gateway URL cannot target localhost"
    if lowered.endswith(".localhost") or lowered.endswith(".local"):
        return "OpenClaw gateway URL cannot target local-host domains"
    if lowered in {
        "metadata.google.internal",
        "instance-data.google.internal",
    }:
        return "OpenClaw gateway URL cannot target cloud metadata endpoints"
    if lowered == "169.254.169.254" or lowered == "[::ffff:169.254.169.254]":
        return "OpenClaw gateway URL cannot target cloud metadata endpoints"
    return None


def _resolve_gateway_host_ips(hostname: str) -> list[IPv4Address | IPv6Address]:
    if not hostname:
        return []
    addresses = []
    try:
        infos = socket.getaddrinfo(hostname, None)
    except Exception:
        return addresses
    for info in infos:
        sockaddr = info[4]
        if not sockaddr:
            continue
        ip_candidate = sockaddr[0]
        if not isinstance(ip_candidate, str):
            continue
        try:
            addresses.append(ip_address(ip_candidate))
        except Exception:
            continue
    return addresses


def _is_disallowed_openclaw_gateway_ip(value: IPv4Address | IPv6Address) -> bool:
    return (
        value.is_loopback
        or value.is_link_local
        or value.is_multicast
        or value.is_private
        or value.is_reserved
        or value.is_unspecified
        or value == ip_address("169.254.169.254")
    )


def validate_llm_provider(provider: Any) -> tuple[str | None, str | None]:
    """Validate LLM provider selection.

    Args:
        provider: The provider value to validate.

    Returns:
        Tuple of (normalized_provider, error_message).
        On success: (lowercase_provider, None)
        On failure: (None, error_message)
    """
    if not isinstance(provider, str):
        return None, "Invalid provider value - must be a string"

    # Normalize to lowercase for comparison
    normalized = provider.lower()

    # Check against allowed providers (also lowercase)
    allowed_lower = {p.lower() for p in constants.ALLOWED_LLM_PROVIDERS}
    if normalized not in allowed_lower:
        return None, f"Invalid provider selection: '{provider}'"

    return normalized, None


def validate_gemini_model(model: Any) -> tuple[str | None, str | None]:
    """Validate Gemini model selection.

    Args:
        model: The model value to validate.

    Returns:
        Tuple of (validated_model, error_message).
        On success: (model, None)
        On failure: (None, error_message)
    """
    if not isinstance(model, str):
        return None, "Invalid model selection - must be a string"

    # Case-insensitive validation to prevent case manipulation attacks
    model_lower = model.lower()
    allowed_models = {m.lower() for m in constants.ALLOWED_GEMINI_MODELS}

    # Also allow legacy models that have a mapping
    allowed_models.update(k.lower() for k in constants.GEMINI_MODEL_MAPPING)

    if model_lower not in allowed_models:
        return None, f"Invalid Gemini model selection: '{model}'"

    return model, None


def validate_openrouter_model(model: Any) -> tuple[str | None, str | None]:
    """Validate OpenRouter model selection.

    Args:
        model: The model value to validate.

    Returns:
        Tuple of (validated_model, error_message).
        On success: (model, None)
        On failure: (None, error_message)
    """
    if not isinstance(model, str):
        return None, "Invalid model selection - must be a string"

    allowed_openrouter = {m.lower() for m in constants.ALLOWED_OPENROUTER_MODELS}
    if model.lower() not in allowed_openrouter:
        return None, f"Invalid OpenRouter model selection: '{model}'"

    return model, None


def validate_cerebras_model(model: Any) -> tuple[str | None, str | None]:
    """Validate Cerebras model selection.

    Args:
        model: The model value to validate.

    Returns:
        Tuple of (validated_model, error_message).
        On success: (model, None)
        On failure: (None, error_message)
    """
    if not isinstance(model, str):
        return None, "Invalid model selection - must be a string"

    allowed_cerebras = {m.lower() for m in constants.ALLOWED_CEREBRAS_MODELS}
    if model.lower() not in allowed_cerebras:
        return None, f"Invalid Cerebras model selection: '{model}'"

    return model, None



def validate_openclaw_gateway_url(url: Any) -> tuple[str | None, str | None]:
    """Validate OpenClaw gateway URL setting (e.g. Tailscale Funnel or Cloudflare Tunnel URL)."""
    if url is None or url == "":
        return None, None
    if not isinstance(url, str):
        return None, "Invalid OpenClaw gateway URL - must be a string"
    stripped = url.strip()
    if not stripped:
        return None, None
    try:
        parsed = urlsplit(stripped)
    except Exception:
        return None, "Invalid OpenClaw gateway URL - must be a valid URL"

    if parsed.scheme not in {"http", "https"}:
        return None, "Invalid OpenClaw gateway URL - must start with http:// or https://"

    hostname = parsed.hostname
    if hostname is None:
        return None, "Invalid OpenClaw gateway URL - missing host"

    host_error = _is_disallowed_gateway_hostname(hostname)
    if host_error is not None:
        return None, host_error

    try:
        parsed_ip = ip_address(hostname)
        if _is_disallowed_openclaw_gateway_ip(parsed_ip):
            return (
                None,
                "Invalid OpenClaw gateway URL - resolved to disallowed address",
            )
        return stripped, None
    except ValueError:
        pass

    resolved_ips = _resolve_gateway_host_ips(hostname)
    if not resolved_ips:
        if _is_tsnet_hostname(hostname):
            return None, (
                "Invalid OpenClaw gateway URL - cannot resolve hostname. "
                "Cloud Run needs a public Tailscale Funnel URL; tailnet-only "
                "MagicDNS or tailscale serve hostnames are not reachable."
            )
        return None, "Invalid OpenClaw gateway URL - cannot resolve hostname"

    for ip in resolved_ips:
        if _is_disallowed_openclaw_gateway_ip(ip):
            return None, "Invalid OpenClaw gateway URL - resolved to disallowed address"

    return stripped, None


def validate_openclaw_gateway_port(port: Any) -> tuple[int | None, str | None]:
    """Validate OpenClaw gateway localhost port setting."""
    if isinstance(port, bool):
        return None, "Invalid OpenClaw gateway port - must be an integer"

    parsed: int | None = None
    if isinstance(port, int):
        parsed = port
    elif isinstance(port, str):
        stripped = port.strip()
        if not stripped:
            return None, "Invalid OpenClaw gateway port: value is required"
        if not stripped.isdigit():
            return None, "Invalid OpenClaw gateway port - must be numeric"
        parsed = int(stripped)
    else:
        return None, "Invalid OpenClaw gateway port - must be an integer"

    if parsed < 1 or parsed > 65535:
        return None, f"Invalid OpenClaw gateway port: '{port}'"

    return parsed, None


def validate_openclaw_gateway_token(token: Any) -> tuple[str | None, str | None]:
    """Validate a per-user OpenClaw gateway token."""
    if token is None:
        return "", None

    if not isinstance(token, str):
        return None, "Invalid OpenClaw gateway token - must be a string"

    cleaned_token = token.strip()
    if cleaned_token == "":
        return "", None

    if len(cleaned_token) < 16:
        return None, "Invalid OpenClaw gateway token - token is too short"

    if len(cleaned_token) > 4096:
        return None, "Invalid OpenClaw gateway token - token is too long"

    return cleaned_token, None


def validate_boolean_setting(
    value: Any, field_name: str
) -> tuple[bool | None, str | None]:
    """Validate a boolean setting value.

    Args:
        value: The value to validate.
        field_name: Name of the field for error messages.

    Returns:
        Tuple of (validated_bool, error_message).
        On success: (bool_value, None)
        On failure: (None, error_message)
    """
    if not isinstance(value, bool):
        return None, f"Invalid {field_name} value - must be a boolean"

    return value, None


def validate_theme(theme: Any) -> tuple[str | None, str | None]:
    """Validate theme setting.

    Args:
        theme: The theme value to validate.

    Returns:
        Tuple of (validated_theme, error_message).
        On success: (theme, None)
        On failure: (None, error_message)
    """
    if not isinstance(theme, str):
        return None, "Invalid theme value - must be a string"

    # Limit length to prevent abuse (malicious long strings)
    if len(theme) > 50:
        return None, "Theme value is too long (max 50 characters)"

    return theme, None


def validate_avatar_url(value: Any) -> tuple[str | None, str | None]:
    """Validate avatar URL setting.

    Accepts None (to clear avatar) or a public URL string.
    """
    if value is None:
        return None, None
    if not isinstance(value, str):
        return None, "Invalid avatar URL - must be a string or null"
    stripped = value.strip()
    if not stripped:
        return None, None
    if len(stripped) > 2048:
        return None, "Avatar URL is too long (max 2048 characters)"
    return stripped, None


def validate_api_key(value: Any, provider_name: str) -> tuple[str | None, str | None]:
    """Validate a BYOK API key for a provider.

    Args:
        value: The API key value to validate.
        provider_name: Name of the provider for error messages.

    Returns:
        Tuple of (validated_key, error_message).
        On success: (cleaned_key_or_empty_string, None)
        On failure: (None, error_message)
    """
    bypass_auth = os.environ.get("TESTING_AUTH_BYPASS", "").lower() == "true"
    enforce_flag = (os.environ.get("BYOK_ENFORCE_KEY_VALIDATION") or "").strip().lower()
    enforce_validation = enforce_flag in {"1", "true", "yes", "on"}
    if bypass_auth and not enforce_flag:
        # Default secure behavior: enforce key validation when auth bypass is active.
        # Tests can opt out explicitly with BYOK_ENFORCE_KEY_VALIDATION=false.
        enforce_validation = True

    # Allow None or empty string to clear the key.
    if value is None:
        return "", None

    if not isinstance(value, str):
        return None, f"{provider_name} API key must be a string"

    cleaned_value = value.strip()

    # Allow clearing the key with empty string
    if cleaned_value == "":
        return "", None

    # In TESTING_AUTH_BYPASS mode, length validation is skipped unless
    # BYOK_ENFORCE_KEY_VALIDATION is explicitly enabled.
    if bypass_auth and not enforce_validation:
        return cleaned_value, None

    # Validate key length (reasonable bounds for API keys)
    if len(cleaned_value) < 16 or len(cleaned_value) > 200:
        return (
            None,
            f"{provider_name} API key must be between 16 and 200 characters",
        )

    return cleaned_value, None


def validate_gemini_api_key(value: Any) -> tuple[str | None, str | None]:
    """Validate Gemini API key."""
    return validate_api_key(value, "Gemini")


def validate_openrouter_api_key(value: Any) -> tuple[str | None, str | None]:
    """Validate OpenRouter API key."""
    return validate_api_key(value, "OpenRouter")


def validate_cerebras_api_key(value: Any) -> tuple[str | None, str | None]:
    """Validate Cerebras API key."""
    return validate_api_key(value, "Cerebras")


def validate_pre_spicy_model(model: Any) -> tuple[str | None, str | None, str | None]:
    """Validate pre_spicy_model and infer provider.

    Args:
        model: The model name to validate.

    Returns:
        Tuple of (validated_model, inferred_provider, error_message).
        On success: (model, provider, None)
        On failure: (None, None, error_message)
    """
    if not isinstance(model, str):
        return None, None, "Invalid pre-spicy model value"

    # Build set of all allowed models (case-insensitive)
    all_allowed_models_lower = {
        m.lower()
        for m in (
            constants.ALLOWED_GEMINI_MODELS
            + constants.ALLOWED_OPENROUTER_MODELS
            + constants.ALLOWED_CEREBRAS_MODELS
        )
    }
    if model.lower().startswith("openclaw/") and len(model) > len("openclaw/"):
        return model, constants.LLM_PROVIDER_OPENCLAW, None
    # Also allow legacy Gemini models that have a mapping
    all_allowed_models_lower.update(k.lower() for k in constants.GEMINI_MODEL_MAPPING)

    if model.lower() not in all_allowed_models_lower:
        return None, None, "Invalid pre-spicy model selection"

    # Infer provider from model for cross-validation
    inferred_provider = constants.infer_provider_from_model(model)
    return model, inferred_provider, None


def validate_pre_spicy_provider(provider: Any) -> tuple[str | None, str | None]:
    """Validate and normalize pre_spicy_provider.

    Args:
        provider: The provider name to validate.

    Returns:
        Tuple of (normalized_provider, error_message).
        On success: (lowercase_provider, None)
        On failure: (None, error_message)
    """
    if not isinstance(provider, str):
        return None, "Invalid pre-spicy provider value"

    # Normalize to lowercase for storage
    normalized = provider.lower()

    # Validate against allowed providers (also lowercase)
    allowed_lower = [p.lower() for p in constants.ALLOWED_LLM_PROVIDERS]
    if normalized not in allowed_lower:
        return None, "Invalid pre-spicy provider selection"

    return normalized, None


def validate_model_provider_match(model: str, provider: str) -> str | None:
    """Validate that model and provider are compatible.

    Args:
        model: The model name.
        provider: The provider name (should be lowercase).

    Returns:
        Error message if incompatible, None if compatible.
    """
    if not isinstance(model, str) or not model:
        return None

    model_lower = model.lower()
    if model_lower.startswith("openclaw/") and len(model_lower) > len("openclaw/"):
        if provider.lower() == constants.LLM_PROVIDER_OPENCLAW:
            return None
        return (
            f"Model '{model}' belongs to provider 'openclaw', "
            f"not '{provider}'. Use matching provider or remove pre_spicy_provider "
            f"to auto-infer from model."
        )
    if model_lower == "openclaw/":
        return "Unknown pre-spicy model format"

    known_models = {
        m.lower()
        for m in (
            constants.ALLOWED_GEMINI_MODELS
            + constants.ALLOWED_OPENROUTER_MODELS
            + constants.ALLOWED_CEREBRAS_MODELS
        )
    }
    known_models.update(k.lower() for k in constants.GEMINI_MODEL_MAPPING)
    if model_lower not in known_models:
        # Unknown/custom model: skip provider compatibility checks
        return None

    inferred = constants.infer_provider_from_model(model)

    # Check if inferred provider matches the specified provider
    if inferred.lower() != provider.lower():
        return (
            f"Model '{model}' belongs to provider '{inferred}', "
            f"not '{provider}'. Use matching provider or remove pre_spicy_provider "
            f"to auto-infer from model."
        )

    return None


# =============================================================================
# Batch Validation Helper
# =============================================================================

# Registry of standard validators (key -> validator function)
# All validators return (validated_value, error_message) tuple
_STANDARD_VALIDATORS = {
    "llm_provider": validate_llm_provider,
    "gemini_model": validate_gemini_model,
    "openrouter_model": validate_openrouter_model,
    "cerebras_model": validate_cerebras_model,
    "openclaw_gateway_port": validate_openclaw_gateway_port,
    "openclaw_gateway_url": validate_openclaw_gateway_url,
    "openclaw_gateway_token": validate_openclaw_gateway_token,
    "theme": validate_theme,
    "pre_spicy_provider": validate_pre_spicy_provider,
    # BYOK API keys
    "gemini_api_key": validate_gemini_api_key,
    "openrouter_api_key": validate_openrouter_api_key,
    "cerebras_api_key": validate_cerebras_api_key,
    "avatar_url": validate_avatar_url,
}

_OPENCLAW_SETTINGS_KEYS = {
    "openclaw_gateway_port",
    "openclaw_gateway_url",
    "openclaw_gateway_token",
}

# Boolean settings that use validate_boolean_setting with field name
_BOOLEAN_SETTINGS = {
    "debug_mode",
    "faction_minigame_enabled",
    "spicy_mode",
    "auto_save",
}


def validate_settings_batch(
    settings_data: dict[str, Any],
    target_llm_provider: Any = None,
) -> tuple[dict[str, Any], str | None]:
    """Validate multiple settings in one call.

    Args:
        settings_data: Dict of setting_name -> value to validate.

    Returns:
        Tuple of (validated_settings_dict, first_error_message).
        On success: ({validated settings}, None)
        On first error: ({partial results}, error_message)
        If ALL keys are unknown: ({}, error_message)

    Note:
        - pre_spicy_model is handled specially (returns 3-tuple with inferred provider)
        - Cross-validation of model/provider must be done separately
        - Unknown keys are skipped, but if ALL keys are unknown, returns error
          to prevent silent no-op from typos
    """
    normalized_target_provider = (
        target_llm_provider.strip().lower()
        if isinstance(target_llm_provider, str)
        else None
    )

    filtered_settings_data = dict(settings_data)
    if (
        normalized_target_provider is not None
        and normalized_target_provider != constants.LLM_PROVIDER_OPENCLAW
    ):
        for key in _OPENCLAW_SETTINGS_KEYS:
            filtered_settings_data.pop(key, None)

    validated = {}
    unknown_keys = []

    for key, value in filtered_settings_data.items():
        # Handle standard validators
        if key in _STANDARD_VALIDATORS:
            result, error = _STANDARD_VALIDATORS[key](value)
            if error:
                return validated, error
            validated[key] = result

        # Handle boolean settings
        elif key in _BOOLEAN_SETTINGS:
            result, error = validate_boolean_setting(value, key)
            if error:
                return validated, error
            validated[key] = result

        # Handle pre_spicy_model specially (3-tuple return)
        elif key == "pre_spicy_model":
            result, _provider, error = validate_pre_spicy_model(value)
            if error:
                return validated, error
            validated[key] = result

        # Unknown setting - track for error reporting
        else:
            unknown_keys.append(key)

    # If ALL keys were unknown, return error to prevent silent no-op from typos
    if filtered_settings_data and not validated and unknown_keys:
        return {}, f"No recognized settings in request. Unknown keys: {unknown_keys}"

    return validated, None


def validate_settings_with_cross_validation(
    settings_data: dict[str, Any],
    existing_settings: Any = None,
    target_llm_provider: Any = None,
) -> tuple[dict[str, Any], str | None]:
    """Validate settings with model/provider cross-validation.

    This is the recommended entry point for settings validation. It:
    1. Validates all individual settings via validate_settings_batch
    2. Cross-validates model/provider compatibility using existing settings

    Args:
        settings_data: Dict of setting_name -> value to validate.
        existing_settings: Current user settings from Firestore (optional).
            Used to validate model/provider compatibility when only one is updated.
            Guards against non-dict values (legacy/corrupt data).
        target_llm_provider: Provider to use when deciding whether to validate
            OpenClaw gateway settings. Useful when request is partial and does
            not include llm_provider directly.

    Returns:
        Tuple of (validated_settings_dict, error_message).
        On success: ({validated settings}, None)
        On error: ({partial or empty}, error_message)
    """
    # Step 1: Batch validate all settings
    validated, error = validate_settings_batch(
        settings_data,
        target_llm_provider=target_llm_provider,
    )
    if error:
        return validated, error

    # Step 2: Cross-validate model/provider compatibility
    model_to_validate: str | None = validated.get("pre_spicy_model")
    provider_to_validate: str | None = validated.get("pre_spicy_provider")

    # Only cross-validate if model or provider is being updated
    if model_to_validate or provider_to_validate:
        # Guard against non-dict existing_settings (legacy/corrupt Firestore data)
        if existing_settings is not None and not isinstance(existing_settings, dict):
            existing_settings = {}

        existing = existing_settings or {}

        # If only provider is being updated, get existing model for validation
        if provider_to_validate and not model_to_validate:
            existing_model = existing.get("pre_spicy_model")
            # Only use if it's a valid string (guard against legacy/corrupted data)
            if isinstance(existing_model, str) and existing_model:
                model_to_validate = existing_model

        # If only model is being updated, get existing provider for validation
        if model_to_validate and not provider_to_validate:
            existing_provider = existing.get("pre_spicy_provider")
            # Only use if it's a valid string (guard against legacy/corrupted data)
            if isinstance(existing_provider, str) and existing_provider:
                provider_to_validate = existing_provider

        # Cross-validate if we have both valid string values
        if model_to_validate and provider_to_validate:
            cross_error = validate_model_provider_match(
                model_to_validate,
                provider_to_validate,
            )
            if cross_error:
                return validated, cross_error

    return validated, None

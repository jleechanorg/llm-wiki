"""Cerebras direct API provider implementation.

Uses the Cerebras OpenAI-compatible chat completions endpoint to keep
llm_service orchestration provider-agnostic.

IMPORTANT: Uses json_schema (strict:false) instead of legacy json_object
to prevent schema echo issues where API returns {"type": "object"} instead
of actual content. strict:false keeps planning_block flexible for dynamic
choice keys.
"""

from __future__ import annotations

import json
import os
from typing import Any

import requests

from mvp_site import constants, logging_util
from mvp_site.dice import DICE_ROLL_TOOLS, execute_dice_tool, execute_unified_tool
from mvp_site.game_state import execute_tool_requests, format_tool_results_text
from mvp_site.llm_providers.openai_chat_common import (
    extract_tool_calls as extract_openai_tool_calls,
)
from mvp_site.llm_providers.openai_compatible_provider_core import (
    generate_openai_compatible_content,
)
from mvp_site.llm_providers.provider_utils import (
    ContextTooLargeError,
    check_context_too_large,
    get_openai_json_schema_format,
    run_openai_json_first_tool_requests_flow,
    run_openai_native_two_phase_flow,
    stringify_chat_parts,
)

CEREBRAS_URL = "https://api.cerebras.ai/v1/chat/completions"


class CerebrasSchemaEchoError(Exception):
    """Raised when Cerebras API returns the response_format schema instead of content.

    This is a retriable error - the API echoed back the schema configuration
    instead of generating content.
    """

    # Docstring-only exception.


def _is_model_not_found_http_error(exc: requests.HTTPError) -> bool:
    """Return True when an HTTP error indicates model-not-found access issues."""
    response = exc.response
    if response is None or response.status_code != 404:
        return False

    body_text = ""
    try:
        body_text = response.text or ""
    except Exception:  # noqa: BLE001
        body_text = ""
    body_lower = body_text.lower()
    if "model_not_found" in body_lower:
        return True
    if "does not exist or you do not have access" in body_lower:
        return True

    try:
        payload = response.json()
    except Exception:  # noqa: BLE001
        payload = None
    if isinstance(payload, dict):
        code = str(payload.get("code", "")).lower()
        message = str(payload.get("message", "")).lower()
        if code == "model_not_found":
            return True
        if "does not exist or you do not have access" in message:
            return True

    return False


def _is_response_format_retryable_http_error(exc: requests.HTTPError) -> bool:
    """Return True when Cerebras rejects/timeout response_format handling."""
    response = exc.response
    if response is None or response.status_code != 422:
        return False

    payload = None
    try:
        payload = response.json()
    except Exception:  # noqa: BLE001
        payload = None
    if not isinstance(payload, dict):
        return False

    code = str(payload.get("code", "")).lower()
    param = str(payload.get("param", "")).lower()
    message = str(payload.get("message", "")).lower()
    if code != "wrong_api_format":
        return False
    if param == "response_format":
        return True
    return "structured output state machine" in message


def _ensure_json_response_instruction(system_instruction_text: str | None) -> str:
    """Ensure prompt explicitly asks for JSON when using json_object fallback."""
    if system_instruction_text and "json" in system_instruction_text.lower():
        return system_instruction_text
    if system_instruction_text:
        return f"{system_instruction_text}\n\nReturn JSON only."
    return "Return JSON only."


def _extract_text_from_message(message: dict[str, Any]) -> Any:
    """Extract content text from a message, tolerating model-specific keys."""
    lowered_keys = {str(key).lower(): key for key in message}
    for preferred in ("content", "reasoning"):
        actual = lowered_keys.get(preferred)
        if actual is not None:
            return message.get(actual)
    return None


def _validate_has_content_or_tool_calls(
    *,
    text: Any,
    has_tool_calls: bool,
    finish_reason: str | None,
    prompt_tokens: int,
    completion_tokens: int,
) -> None:
    if text is None and not has_tool_calls:
        check_context_too_large(
            finish_reason=finish_reason,
            completion_tokens=completion_tokens,
            prompt_tokens=prompt_tokens,
            has_content=False,
        )
        raise KeyError("No 'content' or 'reasoning' field in message")


def _postprocess_response_text(text: Any) -> str:
    """Normalize a successful content payload into a text string."""
    if text is None:
        return ""

    # Some models can return non-string content; coerce defensively.
    text_str = str(text)

    if _is_schema_echo(text_str):
        logging_util.warning(
            "CEREBRAS_SCHEMA_ECHO: API returned schema config instead of content"
        )
        raise CerebrasSchemaEchoError(
            f"Cerebras API echoed schema config instead of content: {text_str[:100]}"
        )

    unwrapped, was_unwrapped = _unwrap_nested_json(text_str)
    if was_unwrapped:
        logging_util.info(
            "CEREBRAS_WRAPPER_FIX: Unwrapped nested JSON wrapper in response"
        )
    return unwrapped


def _is_schema_echo(text: str) -> bool:
    """Check if response is a schema echo (API returning config instead of content)."""
    if not text:
        return False
    stripped = text.strip()
    # Known schema echo patterns
    schema_echo_patterns = [
        '{"type": "object"}',
        '{"type":"object"}',
        '{ "type": "object" }',
        '{"type": "json_object"}',
        '{"type":"json_object"}',
    ]
    if stripped in schema_echo_patterns:
        return True
    # Also check for minimal object with only "type" key
    try:
        parsed = json.loads(stripped)
        if isinstance(parsed, dict) and list(parsed.keys()) == ["type"]:
            return True
    except json.JSONDecodeError:
        pass
    return False


def _unwrap_nested_json(text: str) -> tuple[str, bool]:
    """Unwrap nested JSON wrapper pattern from Cerebras API.

    Cerebras sometimes wraps actual content in: {"type": "object", "json": {...actual...}}

    Returns:
        tuple: (unwrapped_content, was_unwrapped)
    """
    if not text:
        return text, False
    try:
        parsed = json.loads(text.strip())
        if isinstance(parsed, dict):
            for key in ("json", "response", "content"):
                if key in parsed and isinstance(parsed[key], dict):
                    inner = parsed[key]
                    if "narrative" in inner or "entities_mentioned" in inner:
                        logging_util.info(
                            f"CEREBRAS_WRAPPER_UNWRAP: Extracted content from nested '{key}' wrapper"
                        )
                        return json.dumps(inner), True
    except json.JSONDecodeError:
        pass
    return text, False


class CerebrasResponse:
    """Wrapper exposing a `.text` attribute for downstream parsing."""

    def __init__(self, text: str, raw_response: Any):
        self.text = text
        self.raw_response = raw_response

    def __repr__(self) -> str:  # pragma: no cover - debugging helper
        return f"CerebrasResponse(text_length={len(self.text)})"

    def get_tool_calls(self) -> list[dict] | None:
        """Extract tool_calls from the raw response if present."""
        return extract_openai_tool_calls(self.raw_response)

    @property
    def tool_calls(self) -> list[dict] | None:
        """Property accessor for tool_calls."""
        return self.get_tool_calls()


def generate_content(
    prompt_contents: list[Any],
    model_name: str,
    system_instruction_text: str | None,
    temperature: float,
    max_output_tokens: int,
    tools: list[dict] | None = None,
    messages: list[dict] | None = None,
    api_key: str | None = None,
    json_mode: bool = True,
) -> CerebrasResponse:
    """Call the Cerebras chat completions API.

    Args:
        prompt_contents: List of prompt content parts
        model_name: Model name to use
        system_instruction_text: Optional system instruction
        temperature: Sampling temperature
        max_output_tokens: Maximum output tokens
        tools: Optional list of tool definitions for function calling
        messages: Optional pre-built messages list (for tool loop continuation)
        api_key: Optional API key for BYOK (falls back to env var if not provided)
        json_mode: Whether to enforce JSON response format (default True)

    Raises:
        ValueError: If the API key is missing or the response is invalid.
    """
    # Use provided key (BYOK) or fall back to environment variable
    effective_api_key = (
        api_key if api_key is not None else os.environ.get("CEREBRAS_API_KEY")
    )
    if not effective_api_key:
        raise ValueError("CRITICAL: CEREBRAS_API_KEY environment variable not found!")

    headers = {
        "Authorization": f"Bearer {effective_api_key}",
        "Content-Type": "application/json",
    }

    def _validate_response(
        data: dict[str, Any],
        _message: dict[str, Any],
        raw_text: Any,
        tool_calls: list[dict] | None,
    ) -> None:
        try:
            choice = (
                data.get("choices", [{}])[0]
                if isinstance(data.get("choices"), list)
                else {}
            )
            finish_reason = choice.get("finish_reason")
            usage = data.get("usage", {}) or {}
            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)
            _validate_has_content_or_tool_calls(
                text=raw_text,
                has_tool_calls=bool(tool_calls),
                finish_reason=finish_reason,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
            )
        except ContextTooLargeError:
            raise

    def _call_model(
        selected_model: str,
        response_format: dict[str, Any],
        system_instruction: str | None,
    ) -> tuple[str, dict[str, Any]]:
        logging_util.info(
            f"CEREBRAS REQUEST model={selected_model} max_tokens={max_output_tokens}"
        )
        return generate_openai_compatible_content(
            url=CEREBRAS_URL,
            headers=headers,
            model_name=selected_model,
            prompt_contents=prompt_contents,
            system_instruction_text=system_instruction,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            stringify_chat_parts_fn=stringify_chat_parts,
            tools=tools,
            messages=messages,
            response_format=response_format,
            tool_choice=None,
            timeout=300,
            logger=logging_util,
            error_log_prefix="CEREBRAS",
            extract_text_from_message_fn=_extract_text_from_message,
            postprocess_text_fn=_postprocess_response_text,
            validate_response_fn=_validate_response,
        )

    def _call_model_with_response_format_retries(
        selected_model: str,
    ) -> tuple[str, dict[str, Any]]:
        if not json_mode:
            # When json_mode is False, skip JSON enforcement
            return _call_model(
                selected_model=selected_model,
                response_format=None,
                system_instruction=system_instruction_text,
            )
        try:
            return _call_model(
                selected_model=selected_model,
                response_format=get_openai_json_schema_format(),
                system_instruction=system_instruction_text,
            )
        except requests.HTTPError as exc:
            if not _is_response_format_retryable_http_error(exc):
                raise
            logging_util.warning(
                "CEREBRAS RESPONSE_FORMAT FALLBACK: "
                f"model={selected_model} json_schema failed; retrying with json_object"
            )
            return _call_model(
                selected_model=selected_model,
                response_format={"type": "json_object"},
                system_instruction=_ensure_json_response_instruction(
                    system_instruction_text
                ),
            )

    text, data = _call_model_with_response_format_retries(model_name)
    return CerebrasResponse(text, data)


def generate_content_with_tool_requests(
    prompt_contents: list[Any],
    model_name: str,
    system_instruction_text: str | None,
    temperature: float,
    max_output_tokens: int,
    api_key: str | None = None,
    json_mode: bool = True,
) -> CerebrasResponse:
    """Generate content with JSON-first tool request flow.

    This is the preferred flow that keeps JSON schema enforcement throughout:
    1. First call: JSON mode with response_format (like origin/main)
       - LLM can include tool_requests array if it needs dice/skills
    2. If tool_requests present: Execute tools, inject results, second JSON call
    3. If no tool_requests: Return first response as-is

    This avoids the API limitation where tools + response_format cannot be used together.

    Args:
        prompt_contents: List of prompt content parts
        model_name: Model name to use
        system_instruction_text: Optional system instruction
        temperature: Sampling temperature
        max_output_tokens: Maximum output tokens
        api_key: Optional API key for BYOK
        json_mode: Whether to enforce JSON response format (default True)

    Returns:
        Final CerebrasResponse with complete JSON
    """
    return run_openai_json_first_tool_requests_flow(
        generate_content_fn=generate_content,
        api_key=api_key,
        prompt_contents=prompt_contents,
        model_name=model_name,
        system_instruction_text=system_instruction_text,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        json_mode=json_mode,
        provider_no_tool_requests_log_prefix="CEREBRAS_TOOL_REQUESTS",
        execute_tool_requests_fn=execute_tool_requests,
        format_tool_results_text_fn=format_tool_results_text,
        logger=logging_util,
    )


def generate_content_with_native_tools(
    prompt_contents: list[Any],
    model_name: str,
    system_instruction_text: str | None,
    temperature: float,
    max_output_tokens: int,
    native_tools: list[dict] | None = None,
    api_key: str | None = None,
) -> CerebrasResponse:
    """Generate content with native two-phase tool calling.

    This flow uses the native API tool calling that ALL models support:
    1. Phase 1: `tools` parameter (no response_format) → model returns `tool_calls`
    2. Execute tools locally (roll_dice, roll_attack, etc.)
    3. Phase 2: `response_format` parameter (no tools) → structured JSON with results

    This approach works for GLM-4.6 and other models that ignore prompt-based
    tool_requests but properly support native API tool calling.

    Args:
        prompt_contents: List of prompt content parts
        model_name: Model name to use
        system_instruction_text: Optional system instruction
        temperature: Sampling temperature
        max_output_tokens: Maximum output tokens
        api_key: Optional API key for BYOK

    Returns:
        Final CerebrasResponse with structured JSON
    """
    dice_roll_tools = native_tools if native_tools is not None else DICE_ROLL_TOOLS

    # Create bound version of generate_content that includes api_key
    def bound_generate_content(**kwargs):
        if kwargs.get("api_key") is None:
            kwargs["api_key"] = api_key
        return generate_content(**kwargs)

    return run_openai_native_two_phase_flow(
        generate_content_fn=bound_generate_content,
        prompt_contents=prompt_contents,
        model_name=model_name,
        system_instruction_text=system_instruction_text,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        dice_roll_tools=dice_roll_tools,
        execute_tool_fn=execute_unified_tool,
        logger=logging_util,
    )

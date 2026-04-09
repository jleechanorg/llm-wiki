"""OpenRouter provider implementation for LLM interactions.

Uses json_schema (strict:false) for models that support it (e.g., Grok).
Other models fall back to json_object mode.
"""

from __future__ import annotations

import json
import os
from collections.abc import Generator
from typing import Any

import requests

from mvp_site import logging_util
from mvp_site.dice import DICE_ROLL_TOOLS, execute_unified_tool
from mvp_site.game_state import execute_tool_requests, format_tool_results_text
from mvp_site.llm_providers.openai_chat_common import (
    build_chat_payload,
    build_messages,
)
from mvp_site.llm_providers.openai_chat_common import (
    extract_tool_calls as extract_openai_tool_calls,
)
from mvp_site.llm_providers.openai_compatible_provider_core import (
    generate_openai_compatible_content,
)
from mvp_site.llm_providers.provider_utils import (
    get_openai_json_schema_format,
    run_openai_json_first_tool_requests_flow,
    run_openai_native_two_phase_flow,
    stringify_chat_parts,
)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_SITE = "https://worldarchitect.ai"
DEFAULT_TITLE = "WorldArchitect.AI"

# Models that support json_schema with strict:false (dynamic choices)
# Other models ignore strict and fall back to best-effort JSON
MODELS_WITH_JSON_SCHEMA_SUPPORT = {
    "x-ai/grok-4.1-fast",  # xAI direct provider - enforces schema
    "x-ai/grok-4.1",  # Full Grok 4.1 also supports it
}


class OpenRouterResponse:
    """Simple response wrapper matching the .text interface used by llm_service."""

    def __init__(self, text: str, raw_response: Any = None):
        self.text = text
        self.raw_response = raw_response or {}

    def __repr__(self) -> str:  # pragma: no cover - debugging helper
        return f"OpenRouterResponse(text_length={len(self.text)})"

    def get_tool_calls(self) -> list[dict] | None:
        """Extract tool_calls from the raw response if present."""
        return extract_openai_tool_calls(self.raw_response)

    @property
    def tool_calls(self) -> list[dict] | None:
        """Property accessor for tool_calls."""
        return self.get_tool_calls()


def _build_headers(api_key: str) -> dict[str, str]:
    site_url = os.environ.get("OPENROUTER_SITE_URL", DEFAULT_SITE)
    title = os.environ.get("OPENROUTER_APP_TITLE", DEFAULT_TITLE)
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key.strip()}",
        "HTTP-Referer": site_url,
        "X-Title": title,
    }


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
) -> OpenRouterResponse:
    """Generate JSON-oriented content using OpenRouter's chat API.

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
    effective_api_key = (
        api_key if api_key is not None else os.environ.get("OPENROUTER_API_KEY")
    )
    if not effective_api_key:
        raise ValueError("CRITICAL: OPENROUTER_API_KEY environment variable not found!")

    # Keep non-streaming response format policy centralized with helper.
    response_format = _get_response_format(
        model_name=model_name,
        json_mode=json_mode,
        response_json_schema=None,
    )
    if response_format and model_name in MODELS_WITH_JSON_SCHEMA_SUPPORT:
        logging_util.info(
            f"OpenRouter using json_schema (strict:false) for {model_name}"
        )

    logging_util.info(f"Calling OpenRouter model: {model_name}")
    text, data = generate_openai_compatible_content(
        url=OPENROUTER_URL,
        headers=_build_headers(effective_api_key),
        model_name=model_name,
        prompt_contents=prompt_contents,
        system_instruction_text=system_instruction_text,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        stringify_chat_parts_fn=stringify_chat_parts,
        tools=tools,
        messages=messages,
        response_format=response_format,
        tool_choice=None,
        timeout=300,
        logger=logging_util,
        error_log_prefix="OPENROUTER",
    )

    return OpenRouterResponse(text, data)


def generate_content_with_tool_requests(
    prompt_contents: list[Any],
    model_name: str,
    system_instruction_text: str | None,
    temperature: float,
    max_output_tokens: int,
    api_key: str | None = None,
    json_mode: bool = True,
) -> OpenRouterResponse:
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
        json_mode: Whether to enforce JSON response format (default True)

    Returns:
        Final OpenRouterResponse with complete JSON
    """
    return run_openai_json_first_tool_requests_flow(
        generate_content_fn=generate_content,
        prompt_contents=prompt_contents,
        model_name=model_name,
        system_instruction_text=system_instruction_text,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        tools=None,
        messages=None,
        api_key=api_key,
        json_mode=json_mode,
        provider_no_tool_requests_log_prefix="OPENROUTER_TOOL_REQUESTS",
        execute_tool_requests_fn=execute_tool_requests,
        format_tool_results_text_fn=format_tool_results_text,
        logger=logging_util,
    )


def _extract_stream_chunk_text(chunk_data: dict[str, Any]) -> str:
    """Extract text from an OpenAI-compatible streamed chunk payload."""
    choices = chunk_data.get("choices")
    if not isinstance(choices, list) or not choices:
        return ""

    first_choice = choices[0]
    if not isinstance(first_choice, dict):
        return ""

    delta = first_choice.get("delta")
    if not isinstance(delta, dict):
        return ""

    content = delta.get("content")
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""

    text_parts: list[str] = []
    for part in content:
        if not isinstance(part, dict):
            continue
        if part.get("type") == "text" and isinstance(part.get("text"), str):
            text_parts.append(part["text"])
    return "".join(text_parts)


def _resolve_messages(
    prompt_contents: list[Any],
    system_instruction_text: str | None,
    messages: list[dict] | None,
) -> list[dict]:
    """Resolve messages from either pre-built messages or prompt contents."""
    if messages is not None:
        if system_instruction_text is not None:
            has_system = any(
                isinstance(msg, dict) and msg.get("role") == "system"
                for msg in messages
            )
            if not has_system:
                return [{"role": "system", "content": system_instruction_text}, *messages]
        return messages
    return build_messages(
        prompt_contents=prompt_contents,
        system_instruction_text=system_instruction_text,
        stringify_chat_parts_fn=stringify_chat_parts,
    )


def _get_response_format(model_name: str, json_mode: bool, response_json_schema: dict | None) -> dict | None:
    """Determine response format based on model capabilities and json_mode flag."""
    if not json_mode:
        return None
    if model_name in MODELS_WITH_JSON_SCHEMA_SUPPORT:
        return get_openai_json_schema_format(schema=response_json_schema)
    return {"type": "json_object"}


def _get_streaming_response_format(model_name: str, json_mode: bool, response_json_schema: dict | None) -> dict | None:
    """Determine response format for streaming requests.

    Most OpenRouter models do not correctly honour response_format when stream=True
    is also set.  Llama 3.1 70B, for example, returns a bare JSON array like
    [4214.03] instead of a narrative dict when json_object mode is combined with
    streaming.  The system prompt already contains JSON formatting instructions,
    so response_format is only applied here for models that explicitly support it.
    """
    if not json_mode:
        return None
    if model_name in MODELS_WITH_JSON_SCHEMA_SUPPORT:
        return get_openai_json_schema_format(schema=response_json_schema)
    # Do not set response_format for other models in streaming mode — rely on
    # system-prompt JSON instructions to avoid malformed responses.
    return None


def generate_content_stream_sync(
    prompt_contents: list[Any],
    model_name: str,
    system_instruction_text: str | None,
    temperature: float,
    max_output_tokens: int,
    json_mode: bool = True,
    messages: list[dict] | None = None,
    api_key: str | None = None,
    response_json_schema: dict[str, Any] | None = None,
) -> Generator[str, None, None]:
    """Synchronous streaming from OpenRouter chat completions API."""
    effective_api_key = (
        api_key if api_key is not None else os.environ.get("OPENROUTER_API_KEY")
    )
    if not effective_api_key:
        raise ValueError("CRITICAL: OPENROUTER_API_KEY environment variable not found!")

    resolved_messages = _resolve_messages(
        prompt_contents=prompt_contents,
        system_instruction_text=system_instruction_text,
        messages=messages,
    )

    response_format = _get_streaming_response_format(
        model_name=model_name,
        json_mode=json_mode,
        response_json_schema=response_json_schema,
    )

    payload = build_chat_payload(
        model_name=model_name,
        messages=resolved_messages,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        tools=None,
        tool_choice=None,
        response_format=response_format,
    )
    payload["stream"] = True

    response = requests.post(
        OPENROUTER_URL,
        json=payload,
        headers=_build_headers(effective_api_key),
        timeout=600,
        stream=True,
    )

    try:
        if not response.ok:
            logging_util.error(
                "OPENROUTER ERROR %s during stream request",
                response.status_code,
            )
        response.raise_for_status()

        for raw_line in response.iter_lines(decode_unicode=True):
            if not raw_line:
                continue
            line = raw_line.strip()
            if not line.startswith("data:"):
                continue

            event_data = line[5:].strip()
            if event_data == "[DONE]":
                break

            try:
                chunk_data = json.loads(event_data)
            except json.JSONDecodeError:
                logging_util.warning(
                    "OPENROUTER stream decode error: could not parse chunk: %r",
                    event_data[:200],
                )
                continue

            chunk_text = _extract_stream_chunk_text(chunk_data)
            if chunk_text:
                yield chunk_text
    finally:
        response.close()


def generate_content_with_native_tools(
    prompt_contents: list[Any],
    model_name: str,
    system_instruction_text: str | None,
    temperature: float,
    max_output_tokens: int,
    native_tools: list[dict] | None = None,
    api_key: str | None = None,
) -> OpenRouterResponse:
    """Generate content with native two-phase tool calling.

    This flow uses the native API tool calling that ALL models support:
    1. Phase 1: `tools` parameter (no response_format) → model returns `tool_calls`
    2. Execute tools locally (roll_dice, roll_attack, etc.)
    3. Phase 2: `response_format` parameter (no tools) → structured JSON with results

    This approach works for GLM-4.6, Llama, Grok, and other models that support
    native API tool calling.

    Args:
        prompt_contents: List of prompt content parts
        model_name: Model name to use
        system_instruction_text: Optional system instruction
        temperature: Sampling temperature
        max_output_tokens: Maximum output tokens
        api_key: Optional API key for BYOK

    Returns:
        Final OpenRouterResponse with structured JSON
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

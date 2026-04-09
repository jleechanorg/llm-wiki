"""Shared core for OpenAI-compatible chat-completions providers.

This is the next layer above `openai_chat_common.py`.

Goal: keep each provider module focused on:
- endpoint + auth headers
- response_format choice (json_schema vs json_object)
- provider-specific postprocessing (if any)

Everything else (message building, payload shape, tool_calls detection, and
robust first-choice parsing) is centralized here.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

from mvp_site import logging_util
from mvp_site.llm_providers.openai_chat_common import (
    build_chat_payload,
    build_messages,
    extract_first_choice,
    extract_first_choice_message,
    extract_tool_calls,
    post_chat_completions,
)


def generate_openai_compatible_content(
    *,
    url: str,
    headers: dict[str, str],
    model_name: str,
    prompt_contents: list[Any],
    system_instruction_text: str | None,
    temperature: float,
    max_output_tokens: int,
    stringify_chat_parts_fn: Callable[[list[Any]], str],
    tools: list[dict] | None = None,
    messages: list[dict] | None = None,
    response_format: dict[str, Any] | None = None,
    tool_choice: str | None = None,
    timeout: int = 300,
    logger: Any | None = None,
    error_log_prefix: str = "",
    extract_text_from_message_fn: Callable[[dict[str, Any]], Any] | None = None,
    postprocess_text_fn: Callable[[Any], str] | None = None,
    validate_response_fn: Callable[
        [dict[str, Any], dict[str, Any], Any, list[dict] | None], None
    ]
    | None = None,
) -> tuple[str, dict[str, Any]]:
    """Call an OpenAI-compatible chat-completions endpoint and return (text, raw_json)."""
    # Use provided messages or build from prompt_contents.
    if messages is None:
        messages = build_messages(
            prompt_contents=prompt_contents,
            system_instruction_text=system_instruction_text,
            stringify_chat_parts_fn=stringify_chat_parts_fn,
        )

    payload = build_chat_payload(
        model_name=model_name,
        messages=messages,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        tools=tools,
        tool_choice=tool_choice if tools else None,
        response_format=response_format,
    )

    data = post_chat_completions(
        url=url,
        headers=headers,
        payload=payload,
        timeout=timeout,
        logger=logger,
        error_log_prefix=error_log_prefix,
    )

    # Log finish_reason and usage for debugging truncation issues
    if logger is not None:
        try:
            try:
                first_choice = extract_first_choice(data)
                finish_reason = (
                    first_choice.get("finish_reason", "unknown")
                    if isinstance(first_choice, dict)
                    else "unknown"
                )
            except ValueError:
                finish_reason = "unknown"

            if isinstance(data, dict):
                usage_value = data.get("usage") or {}
                usage = usage_value if isinstance(usage_value, dict) else {}
            else:
                usage = {}
            prefix = f"{error_log_prefix} " if error_log_prefix else ""
            completion_tokens = usage.get("completion_tokens", "N/A")
            prompt_tokens = usage.get("prompt_tokens", "N/A")
            logging_util.info(
                f"{prefix}finish_reason={finish_reason}, "
                f"prompt_tokens={prompt_tokens}, completion_tokens={completion_tokens}",
                logger=logger,
            )
            if finish_reason == "length":
                logging_util.warning(
                    f"{prefix}RESPONSE_TRUNCATED: finish_reason=length - "
                    f"model hit max_tokens ({max_output_tokens}) or provider limit. "
                    f"completion_tokens={completion_tokens}",
                    logger=logger,
                )
        except Exception:  # noqa: BLE001 - logging must never crash
            pass

    # Log full response body on parsing errors for debugging API issues
    try:
        extract_first_choice(data)  # Validate choices[0] exists
        message = extract_first_choice_message(data)
    except ValueError as e:
        if logger is not None:
            # Truncate response to avoid log spam (500 chars max)
            try:
                response_str = json.dumps(data)[:500]
            except Exception:  # noqa: BLE001
                response_str = str(data)[:500]
            prefix = f"{error_log_prefix} " if error_log_prefix else ""
            try:
                logger.error(f"{prefix}API parsing error ({e}): {response_str}")
            except Exception:  # noqa: BLE001 - logging must never crash
                pass
        raise
    raw_text: Any
    if extract_text_from_message_fn is None:
        raw_text = message.get("content") if isinstance(message, dict) else None
    else:
        raw_text = extract_text_from_message_fn(message)

    # Accept content-less responses only if tool_calls exist.
    tool_calls = extract_tool_calls(data)
    if validate_response_fn is not None:
        validate_response_fn(data, message, raw_text, tool_calls)
    elif raw_text is None and not tool_calls:
        raise ValueError("No content and no tool_calls in response message")

    if postprocess_text_fn is None:
        text = "" if raw_text is None else str(raw_text)
    else:
        text = postprocess_text_fn(raw_text)

    return text, data

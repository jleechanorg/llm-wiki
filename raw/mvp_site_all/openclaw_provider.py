from __future__ import annotations

import hashlib
import json
import os
from collections.abc import Generator
from dataclasses import dataclass
from typing import Any

import requests

from mvp_site import logging_util
from mvp_site.game_state import execute_tool_requests, format_tool_results_text
from mvp_site.llm_providers.provider_utils import (
    get_openai_json_schema_format,
    run_openai_json_first_tool_requests_flow,
)
from mvp_site.settings_validation import validate_openclaw_gateway_url

DEFAULT_GATEWAY_HOST = os.getenv("OPENCLAW_GATEWAY_HOST", "127.0.0.1")
DEFAULT_GATEWAY_PORT = os.getenv("OPENCLAW_GATEWAY_PORT", "18789")
DEFAULT_GATEWAY_TOKEN = os.getenv("OPENCLAW_GATEWAY_TOKEN", "")
REQUEST_TIMEOUT_SECONDS = 600
CONNECTION_TEST_TIMEOUT_SECONDS = int(
    os.getenv("OPENCLAW_CONNECTION_TEST_TIMEOUT_SECONDS", "8")
)
OPENCLAW_PHASE1_INVALID_JSON_RETRIES = int(
    os.getenv("OPENCLAW_PHASE1_INVALID_JSON_RETRIES", "3")
)


def _get_gateway_url() -> str:
    explicit_url = os.getenv("OPENCLAW_GATEWAY_URL")
    if explicit_url is not None:
        explicit_url = explicit_url.strip()
        if explicit_url:
            # Server-level env var is operator-controlled; trust it without SSRF validation.
            # It may legitimately point to localhost (e.g. http://127.0.0.1:18789) or a sidecar.
            if not explicit_url.startswith(("http://", "https://")):
                raise ValueError(
                    "Invalid OPENCLAW_GATEWAY_URL: must start with http:// or https://"
                )
            return explicit_url
    host = os.getenv("OPENCLAW_GATEWAY_HOST", "127.0.0.1")
    port = os.getenv("OPENCLAW_GATEWAY_PORT", "18789")
    return f"http://{host}:{port}"


@dataclass
class OpenClawResponse:
    text: str
    raw_response: dict[str, Any] | None = None


class OpenClawHTTPClient:
    """HTTP client for OpenClaw gateway chat completions."""

    def __init__(
        self, gateway_url: str | None = None, gateway_token: str | None = None
    ):
        self._gateway_url = gateway_url or _get_gateway_url()
        self._token = (
            gateway_token if gateway_token is not None else DEFAULT_GATEWAY_TOKEN
        )

    def _get_headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        return headers

    def invoke(
        self,
        *,
        messages: list[dict[str, Any]],
        model_name: str,
        system_instruction_text: str | None,
        temperature: float,
        max_output_tokens: int,
        stream: bool,
        response_format: dict[str, Any] | None = None,
    ) -> OpenClawResponse | Generator[str, None]:
        payload: dict[str, Any] = {
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_output_tokens,
            "stream": stream,
        }
        model_value = model_name.removeprefix("openclaw/")
        if model_value:
            payload["model"] = model_value
        if response_format:
            payload["response_format"] = response_format

        if system_instruction_text is not None:
            payload["messages"] = [
                {"role": "system", "content": system_instruction_text}
            ] + messages

        if stream:
            return self._invoke_stream(payload)
        return self._invoke_non_stream(payload)

    def _invoke_non_stream(self, payload: dict[str, Any]) -> OpenClawResponse:
        try:
            response = requests.post(
                f"{self._gateway_url}/v1/chat/completions",
                headers=self._get_headers(),
                json=payload,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            data = response.json()

            # Check for gateway-level error field (BD-iwr)
            if isinstance(data, dict) and "error" in data:
                error_info = data["error"]
                raise RuntimeError(f"OpenClaw invoke failed: {error_info}")

            text = ""
            if "choices" in data and len(data["choices"]) > 0:
                choice = data["choices"][0]
                if "message" in choice:
                    text = choice["message"].get("content", "")

            return OpenClawResponse(text=text, raw_response=data)
        except requests.exceptions.RequestException as exc:
            raise RuntimeError(f"OpenClaw request failed: {exc}") from exc

    def _invoke_stream(self, payload: dict[str, Any]) -> Generator[str, None, None]:  # noqa: PLR0915
        payload["stream"] = True
        target_url = f"{self._gateway_url}/v1/chat/completions"
        logging_util.info("OpenClaw: POST %s", target_url)
        current_event = "message"

        def _extract_content_and_done(  # noqa: PLR0911, PLR0912
            payload_data: str,
            *,
            event_hint: str | None = None,
        ) -> tuple[str | None, bool]:
            """Return (chunk_text, is_done) for one SSE payload."""
            payload_data = payload_data.strip()
            if not payload_data:
                return None, False

            if payload_data == "[DONE]":
                return None, True

            try:
                chunk = json.loads(payload_data)
            except json.JSONDecodeError as exc:
                logging_util.warning(
                    "OpenClaw stream decode error: %s (raw=%r)", exc, payload_data
                )
                return None, False

            if not isinstance(chunk, dict):
                if isinstance(chunk, str):
                    return chunk, False
                return None, False

            if "error" in chunk:
                error_info = chunk["error"]
                raise RuntimeError(f"OpenClaw invoke failed: {error_info}")

            event_type = str(event_hint or "").strip().lower()
            chunk_event_type = str(chunk.get("type", "")).strip().lower()
            if not event_type or event_type == "message":
                event_type = chunk_event_type

            if chunk_event_type == "done":
                return None, True

            payload_obj = chunk

            if event_type and event_type != "message" and "payload" in chunk:
                payload_obj = chunk.get("payload")
            elif "type" in chunk and "payload" in chunk:
                payload_obj = chunk.get("payload")
                event_type = str(chunk.get("type", "")).strip().lower()

            if event_type == "done":
                return None, True

            if isinstance(payload_obj, str):
                return payload_obj, False

            if not isinstance(payload_obj, dict):
                return None, False

            if event_type in {"done", "error"}:
                return None, event_type == "done"

            if isinstance(payload_obj.get("choices"), list) and payload_obj["choices"]:
                choice = payload_obj["choices"][0]
                if isinstance(choice, dict):
                    delta = choice.get("delta", {})
                    if isinstance(delta, dict):
                        content = delta.get("content")
                        if isinstance(content, str) and content:
                            return content, False

            if isinstance(payload_obj.get("content"), str):
                content = payload_obj["content"]
                if content:
                    return content, False

            return None, False

        try:
            with requests.post(
                target_url,
                headers=self._get_headers(),
                json=payload,
                stream=True,
                timeout=REQUEST_TIMEOUT_SECONDS,
            ) as response:
                response.raise_for_status()

                for line in response.iter_lines():
                    if not line:
                        continue
                    decoded_line = line.decode("utf-8").strip()
                    if not decoded_line:
                        continue
                    if decoded_line.startswith(":"):
                        continue

                    if decoded_line.startswith("event:"):
                        current_event = decoded_line.split(":", 1)[1].strip()
                        continue

                    if decoded_line.startswith("data:"):
                        payload_data = decoded_line.split(":", 1)[1].lstrip()
                    else:
                        payload_data = decoded_line

                    text, is_done = _extract_content_and_done(
                        payload_data,
                        event_hint=current_event,
                    )
                    current_event = "message"
                    if text:
                        yield text
                    if is_done:
                        return
        except requests.exceptions.RequestException as exc:
            raise RuntimeError(f"OpenClaw stream request failed: {exc}") from exc


def _build_messages(prompt_contents: list[Any]) -> list[dict[str, str]]:
    if not prompt_contents:
        return []
    # If it looks like it's already a list of messages, return as is
    if isinstance(prompt_contents[0], dict) and "role" in prompt_contents[0]:
        return prompt_contents

    content = "\n\n".join(str(item) for item in prompt_contents)
    return [{"role": "user", "content": content}]


def _resolve_gateway_url(
    gateway_port: int | None = None,
    gateway_url: str | None = None,
) -> str:
    # Per-user gateway URL (Tailscale Funnel / Cloudflare Tunnel) takes highest priority
    if gateway_url is not None:
        gateway_url = gateway_url.strip()
        if gateway_url:
            url, error = validate_openclaw_gateway_url(gateway_url)
            if error is None:
                return url
            raise ValueError(
                f"Invalid OpenClaw gateway URL passed to provider: {error}"
            )

    if gateway_port is None:
        return _get_gateway_url()
    if not isinstance(gateway_port, int) or not (1 <= gateway_port <= 65535):
        raise ValueError(f"Invalid OpenClaw gateway port: {gateway_port!r}")

    # Check if OPENCLAW_GATEWAY_URL was explicitly set (not the default)
    # If explicitly set to a non-default value, gateway_port should NOT override it
    # This prevents: (1) breaking production, (2) localhost SSRF surface
    explicit_gateway_url = os.getenv("OPENCLAW_GATEWAY_URL")
    if explicit_gateway_url is not None:
        # Server-level URL set - respect it, don't allow port override.
        # Operator-controlled; trust without SSRF validation (may be localhost/sidecar).
        explicit_gateway_url = explicit_gateway_url.strip()
        if explicit_gateway_url:
            if not explicit_gateway_url.startswith(("http://", "https://")):
                raise ValueError(
                    "Invalid OPENCLAW_GATEWAY_URL environment value: must start with http:// or https://"
                )
            return explicit_gateway_url

    # No explicit URL set - use default host with user-provided port
    return f"http://{DEFAULT_GATEWAY_HOST}:{gateway_port}"


def get_gateway_client(
    gateway_url: str | None = None, gateway_token: str | None = None
) -> OpenClawHTTPClient:
    return OpenClawHTTPClient(
        gateway_url=gateway_url or _get_gateway_url(),
        gateway_token=gateway_token,
    )


def test_openclaw_gateway_connection(  # noqa: PLR0911, PLR0912
    gateway_url: str | None = None,  # noqa: PT028
    gateway_port: int | None = None,  # noqa: PT028
    gateway_token: str | None = None,  # noqa: PT028
    *,
    model_name: str = "gemini-3-flash-preview",  # noqa: PT028
    proof_prompt: str | None = None,  # noqa: PT028
) -> dict[str, Any]:
    """Send a lightweight request to verify OpenClaw gateway connectivity."""
    resolved_url = _resolve_gateway_url(gateway_port, gateway_url)

    headers = {"Content-Type": "application/json"}
    if gateway_token:
        headers["Authorization"] = f"Bearer {gateway_token}"

    base_timeout = CONNECTION_TEST_TIMEOUT_SECONDS
    models_url = f"{resolved_url}/v1/models"
    payload = {
        "messages": [{"role": "user", "content": "ping"}],
        "temperature": 0.0,
        "max_tokens": 2,
        "model": model_name,
        "stream": False,
    }
    proof_payload = None
    if isinstance(proof_prompt, str) and proof_prompt.strip():
        proof_payload = {
            "messages": [{"role": "user", "content": proof_prompt.strip()}],
            "temperature": 0.0,
            "max_tokens": 80,
            "model": model_name,
            "stream": False,
        }

    try:
        response = requests.get(models_url, headers=headers, timeout=base_timeout)
        models_payload: dict[str, Any] | list[Any] | None = None
        if response.status_code == 200:
            try:
                parsed_models = response.json()
            except ValueError:
                parsed_models = None
            if isinstance(parsed_models, (dict, list)):
                models_payload = parsed_models
            # When /v1/models returns non-JSON (e.g. HTML from Tailscale Funnel UI),
            # fall through to chat/completions regardless of proof_prompt — the gateway
            # may still serve inference even if models listing returns HTML.
        # When models probe succeeds with JSON and no proof needed, return immediately.
        # When models probe returns non-JSON or non-200, fall through to chat/completions.
        if (
            response.status_code == 200
            and models_payload is not None
            and proof_payload is None
        ):
            return {
                "success": True,
                "gateway_url": resolved_url,
                "status_code": response.status_code,
                "mode": "models",
                "models_json_type": type(models_payload).__name__,
            }

        completion_url = f"{resolved_url}/v1/chat/completions"
        completion_timeout = (
            REQUEST_TIMEOUT_SECONDS if proof_payload is not None else base_timeout
        )
        response = requests.post(
            completion_url,
            headers=headers,
            json=proof_payload or payload,
            timeout=completion_timeout,
        )
        if response.status_code == 200:
            response_hash = None
            response_content = ""
            if proof_payload is not None:
                try:
                    data = response.json()
                    if isinstance(data, dict):
                        choices = data.get("choices")
                        if isinstance(choices, list) and choices:
                            first_choice = choices[0]
                            if isinstance(first_choice, dict):
                                message = first_choice.get("message")
                                if isinstance(message, dict):
                                    content = message.get("content")
                                    if isinstance(content, str):
                                        response_content = content
                    response_hash = hashlib.sha256(
                        response_content.encode("utf-8")
                    ).hexdigest()
                except Exception:
                    return {
                        "success": False,
                        "gateway_url": resolved_url,
                        "status_code": response.status_code,
                        "mode": "chat_completions",
                        "message": "Proof validation failed: chat response was non-JSON",
                    }
                if not response_content.strip():
                    return {
                        "success": False,
                        "gateway_url": resolved_url,
                        "status_code": response.status_code,
                        "mode": "chat_completions",
                        "message": "Proof validation failed: empty content in chat response",
                    }
            return {
                "success": True,
                "gateway_url": resolved_url,
                "status_code": response.status_code,
                "mode": "chat_completions",
                "proof_prompt_used": proof_payload is not None,
                "response_hash": response_hash,
                "response_text_preview": response_content[:200],
            }

        detail = response.text.strip()
        return {
            "success": False,
            "gateway_url": resolved_url,
            "status_code": response.status_code,
            "message": detail[:240] or "Connection attempt returned failure",
        }
    except requests.exceptions.Timeout as exc:
        return {
            "success": False,
            "gateway_url": resolved_url,
            "status_code": 408,
            "message": f"Connection timed out: {exc}",
        }
    except requests.exceptions.RequestException as exc:
        return {
            "success": False,
            "gateway_url": resolved_url,
            "status_code": 502,
            "message": f"Connection error: {exc}",
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
    gateway_port: int | None = None,
    gateway_url: str | None = None,
    gateway_token: str | None = None,
    json_mode: bool = True,
) -> OpenClawResponse:
    del tools, api_key
    resolved_url = _resolve_gateway_url(gateway_port, gateway_url)
    # If the caller supplied a user-controlled gateway_url, don't fall back to the
    # server-level DEFAULT_GATEWAY_TOKEN — that would leak the shared server secret
    # to an endpoint the user controls.
    effective_token = gateway_token
    if gateway_url and gateway_url.strip() and gateway_token is None:
        effective_token = ""
    client = get_gateway_client(
        gateway_url=resolved_url,
        gateway_token=effective_token,
    )

    # Use response_format to enforce JSON mode (like Cerebras/OpenRouter)
    response_format = None
    if json_mode:
        response_format = get_openai_json_schema_format()

    resolved_messages = (
        messages if messages is not None else _build_messages(prompt_contents)
    )
    response = client.invoke(
        messages=resolved_messages,
        model_name=model_name,
        system_instruction_text=system_instruction_text,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        stream=False,
        response_format=response_format,
    )
    if isinstance(response, OpenClawResponse):
        return response
    return OpenClawResponse(text="".join(response))


def generate_content_stream_sync(
    prompt_contents: list[Any],
    model_name: str,
    system_instruction_text: str | None,
    temperature: float,
    max_output_tokens: int,
    json_mode: bool = True,
    messages: list[dict] | None = None,
    api_key: str | None = None,
    gateway_port: int | None = None,
    response_json_schema: dict[str, Any] | None = None,
    gateway_url: str | None = None,
    gateway_token: str | None = None,
) -> Generator[str, None, None]:
    del api_key
    resolved_url = _resolve_gateway_url(gateway_port, gateway_url)
    # Don't leak the server-level DEFAULT_GATEWAY_TOKEN to a user-controlled URL.
    effective_token = gateway_token
    if gateway_url and gateway_url.strip() and gateway_token is None:
        effective_token = ""
    client = get_gateway_client(
        gateway_url=resolved_url,
        gateway_token=effective_token,
    )

    response_format = (
        get_openai_json_schema_format(schema=response_json_schema)
        if json_mode
        else None
    )
    resolved_messages = (
        messages if messages is not None else _build_messages(prompt_contents)
    )
    response = client.invoke(
        messages=resolved_messages,
        model_name=model_name,
        system_instruction_text=system_instruction_text,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        stream=True,
        response_format=response_format,
    )
    if isinstance(response, OpenClawResponse):
        yield response.text
        return
    yield from response


def generate_content_with_tool_requests(
    prompt_contents: list[Any],
    model_name: str,
    system_instruction_text: str | None,
    temperature: float,
    max_output_tokens: int,
    api_key: str | None = None,
    gateway_port: int | None = None,
    gateway_url: str | None = None,
    gateway_token: str | None = None,
    messages: list[dict] | None = None,
) -> OpenClawResponse:
    def _generate_content_with_gateway_port(**kwargs: Any) -> OpenClawResponse:
        kwargs["gateway_port"] = gateway_port
        kwargs["gateway_url"] = gateway_url
        kwargs["gateway_token"] = gateway_token
        return generate_content(**kwargs)

    return run_openai_json_first_tool_requests_flow(
        generate_content_fn=_generate_content_with_gateway_port,
        prompt_contents=prompt_contents,
        model_name=model_name,
        system_instruction_text=system_instruction_text,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        tools=None,
        messages=messages,
        api_key=api_key,
        provider_no_tool_requests_log_prefix="OPENCLAW_TOOL_REQUESTS",
        execute_tool_requests_fn=execute_tool_requests,
        format_tool_results_text_fn=format_tool_results_text,
        logger=logging_util,
        phase1_invalid_json_retries=OPENCLAW_PHASE1_INVALID_JSON_RETRIES,
    )

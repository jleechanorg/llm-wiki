"""OpenAI-compatible inference proxy — Flask server routes → user's OpenClaw gateway.

This module exposes server-side endpoints that forward requests from external clients
(CLI tools, other applications) to each user's personal OpenClaw gateway.

Architecture:
    External caller
        → POST /v1/chat/completions (this server, authenticated via worldai_ personal key)
        → User's OpenClaw gateway (via Tailscale Funnel / Cloudflare Tunnel URL)
        → OpenClaw inference (Claude Code, Gemini, etc. running on user's machine)

Auth: worldai_ personal API keys are resolved to user_id via Firestore
      (same mechanism as /mcp endpoint — no new auth to build).

URL resolution: user's gateway_url + gateway_token read from their Firestore settings
                (same get_user_settings() path as existing OpenClaw client code).
"""

from __future__ import annotations

import hashlib
import json
import os
from collections.abc import Generator
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlsplit

import requests

from mvp_site import logging_util
from mvp_site.llm_providers.openclaw_provider import (
    REQUEST_TIMEOUT_SECONDS,
)


def _safe_gateway_url_for_log(raw_url: str) -> str:
    """Redact user-controlled gateway URLs for logs (host + port only, no path/credentials)."""
    try:
        parts = urlsplit(raw_url)
        if parts.scheme and parts.hostname:
            host = parts.hostname
            if parts.port:
                host = f"{host}:{parts.port}"
            return f"{parts.scheme}://{host}"
    except Exception:  # noqa: S110
        pass
    digest = hashlib.sha256(raw_url.encode("utf-8", errors="replace")).hexdigest()[:8]
    return f"<redacted:{digest}>"


def _reject_if_gateway_redirect(response: requests.Response, safe_url: str) -> bool:
    """Return True if response indicates a redirect (SSRF bypass attempt)."""
    if response.is_redirect or response.history:
        logging_util.error(
            "OpenAI proxy: gateway returned redirect (forbidden) url=%s",
            safe_url,
        )
        return True
    return False


# Maximum tokens cap — prevent runaway inference costs
MAX_PROXY_MAX_TOKENS = int(os.getenv("OPENAI_PROXY_MAX_TOKENS", "8192"))
INFERENCE_RATE_LIMIT = os.getenv(
    "OPENAI_PROXY_RATE_LIMIT", "2000 per hour, 200 per minute"
)


@dataclass
class ProxyPayload:
    """Validated OpenAI /chat/completions payload."""

    messages: list[dict[str, Any]]
    model: str
    temperature: float
    max_tokens: int
    stream: bool
    # Optional fields we pass through
    response_format: dict[str, Any] | None = None
    tools: list[dict[str, Any]] | None = None
    tool_choice: str | dict[str, Any] | None = None


def parse_chat_completions_payload(data: dict[str, Any]) -> ProxyPayload:  # noqa: PLR0912
    """Validate and extract fields from an OpenAI /chat/completions request body.

    Raises ValueError on invalid payloads.
    """
    if not isinstance(data, dict):
        raise ValueError("Request body must be a JSON object")

    messages = data.get("messages")
    if not isinstance(messages, list) or not messages:
        raise ValueError("'messages' must be a non-empty array")
    for msg in messages:
        if not isinstance(msg, dict):
            raise ValueError(
                "'messages' must be an array of objects each with a non-empty 'role'"
            )
        role = msg.get("role")
        if not isinstance(role, str) or not role.strip():
            raise ValueError(
                "'messages' must be an array of objects each with a non-empty 'role'"
            )

    model = data.get("model")
    if not isinstance(model, str) or not model.strip():
        raise ValueError("'model' is required and must be a non-empty string")

    temperature = data.get("temperature")
    if temperature is not None:
        if not isinstance(temperature, (int, float)):
            raise ValueError("'temperature' must be a number")
        if not (0.0 <= temperature <= 2.0):
            raise ValueError("'temperature' must be between 0 and 2")

    max_tokens = data.get("max_tokens")
    if max_tokens is not None:
        if not isinstance(max_tokens, int) or max_tokens < 1:
            raise ValueError("'max_tokens' must be a positive integer")
        max_tokens = min(max_tokens, MAX_PROXY_MAX_TOKENS)

    if "stream" in data:
        stream_val = data["stream"]
        if not isinstance(stream_val, bool):
            raise ValueError("'stream' must be a boolean")
        stream = stream_val
    else:
        stream = False
    if stream and max_tokens is None:
        # OpenAI default for max_tokens when streaming with no explicit value
        max_tokens = MAX_PROXY_MAX_TOKENS

    response_format = data.get("response_format")
    if response_format is not None and not isinstance(response_format, dict):
        raise ValueError("'response_format' must be an object")

    tools = data.get("tools")
    if tools is not None and not isinstance(tools, list):
        raise ValueError("'tools' must be an array")

    tool_choice = data.get("tool_choice")
    if tool_choice is not None and not isinstance(tool_choice, (str, dict)):
        raise ValueError("'tool_choice' must be a string or an object")

    return ProxyPayload(
        messages=messages,
        model=model.strip(),
        temperature=float(temperature) if temperature is not None else 1.0,
        max_tokens=max_tokens or MAX_PROXY_MAX_TOKENS,
        stream=stream,
        response_format=response_format,
        tools=tools,
        tool_choice=tool_choice,
    )


def build_openclaw_payload(payload: ProxyPayload) -> dict[str, Any]:
    """Convert an OpenAI payload into the OpenClaw gateway request shape."""
    msgs = payload.messages
    system_text: str | None = None

    # Extract system message for explicit top-level field — but keep it in msgs
    # so the gateway sees it regardless of whether it prefers messages[] or
    # system_instruction_text.
    if msgs and msgs[0].get("role") == "system":
        system_text = msgs[0].get("content", "")

    request: dict[str, Any] = {
        "messages": msgs,
        "model": payload.model,
        "temperature": payload.temperature,
        "max_tokens": payload.max_tokens,
        "stream": payload.stream,
    }
    if system_text:
        request["system_instruction_text"] = system_text
    if payload.response_format:
        request["response_format"] = payload.response_format
    if payload.tools:
        request["tools"] = payload.tools
    if payload.tool_choice:
        request["tool_choice"] = payload.tool_choice

    return request


# ---------------------------------------------------------------------------
# Non-streaming
# ---------------------------------------------------------------------------


@dataclass
class ProxyResult:
    """Result from a proxy invocation."""

    ok: bool
    status_code: int
    # For ok=True: OpenAI-compatible response dict
    data: dict[str, Any] | None = None
    # For ok=False: error dict with "message" and optional "type" / "code"
    error: dict[str, str] | None = None

    def to_flask_response(self) -> tuple[Any, int]:
        """Convert to (flask_response_body, status_code)."""
        if self.ok:
            return self.data, self.status_code
        return {"error": self.error}, self.status_code


def invoke_openclaw_gateway(
    *,
    gateway_url: str,
    gateway_token: str | None,
    payload: dict[str, Any],
) -> ProxyResult:
    """Call the user's OpenClaw gateway and return an OpenAI-compatible response.

    Handles the full request/response cycle including error normalization.
    """
    headers = {"Content-Type": "application/json"}
    if gateway_token:
        headers["Authorization"] = f"Bearer {gateway_token}"

    safe_url = _safe_gateway_url_for_log(gateway_url)
    try:
        response = requests.post(
            f"{gateway_url}/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=REQUEST_TIMEOUT_SECONDS,
            allow_redirects=False,
        )
    except requests.exceptions.Timeout:
        logging_util.error("OpenAI proxy: gateway timeout url=%s", safe_url)
        return ProxyResult(
            ok=False,
            status_code=504,
            error={"message": "Gateway timed out", "type": "gateway_timeout"},
        )
    except requests.exceptions.RequestException as exc:
        # Base class of ConnectionError, HTTPError, etc. (but not Timeout, caught above)
        logging_util.error(
            "OpenAI proxy: gateway request error url=%s: %s", safe_url, exc
        )
        return ProxyResult(
            ok=False,
            status_code=502,
            error={"message": "Gateway unreachable", "type": "gateway_error"},
        )

    if _reject_if_gateway_redirect(response, safe_url):
        return ProxyResult(
            ok=False,
            status_code=502,
            error={
                "message": "Gateway returned redirect",
                "type": "gateway_error",
            },
        )

    # Normalize 4xx/5xx from gateway
    if response.status_code >= 400:
        try:
            err_body = response.json()
            if isinstance(err_body, dict) and "error" in err_body:
                inner = err_body["error"]
                if isinstance(inner, dict):
                    err_msg = inner.get("message", response.text[:200] or str(inner))
                else:
                    err_msg = str(inner)
            elif isinstance(err_body, dict):
                err_msg = err_body.get("message", response.text[:200])
            else:
                err_msg = response.text[:200]
        except Exception:
            err_msg = response.text[:200] or f"HTTP {response.status_code}"
        return ProxyResult(
            ok=False,
            status_code=min(response.status_code, 599),
            error={"message": err_msg, "type": "gateway_error"},
        )

    # Success — return gateway's response as-is (already OpenAI-shaped)
    try:
        data = response.json()
    except Exception:
        # Catches JSONDecodeError and any unexpected .json() breakage.
        # Returns a clean 502 rather than propagating.
        return ProxyResult(
            ok=False,
            status_code=502,
            error={
                "message": "Gateway returned non-JSON response",
                "type": "gateway_error",
            },
        )
    return ProxyResult(ok=True, status_code=200, data=data)


# ---------------------------------------------------------------------------
# Streaming
# ---------------------------------------------------------------------------


def _yield_sse_error_and_done(
    message: str, err_type: str
) -> Generator[tuple[bool, str], None, None]:
    """Emit one OpenAI-shaped error SSE event, [DONE], then stream terminator."""
    payload = json.dumps({"error": {"message": message, "type": err_type}})
    yield False, f"data: {payload}\n\ndata: [DONE]\n\n"
    yield True, ""


def invoke_openclaw_gateway_stream(  # noqa: PLR0912, PLR0915
    *,
    gateway_url: str,
    gateway_token: str | None,
    payload: dict[str, Any],
) -> Generator[tuple[bool, str], None, None]:
    """Stream from the OpenClaw gateway, yielding SSE lines.

    Yields:
        (False, line) — non-terminal SSE line
        (True, "")   — stream complete (no more data)

    On error yields a synthetic error SSE event, a single [DONE], then the terminator.
    """
    headers = {"Content-Type": "application/json"}
    if gateway_token:
        headers["Authorization"] = f"Bearer {gateway_token}"

    payload = dict(payload, stream=True)
    safe_url = _safe_gateway_url_for_log(gateway_url)

    try:
        http_response = requests.post(
            f"{gateway_url}/v1/chat/completions",
            headers=headers,
            json=payload,
            stream=True,
            timeout=REQUEST_TIMEOUT_SECONDS,
            allow_redirects=False,
        )
    except requests.exceptions.Timeout:
        yield from _yield_sse_error_and_done("Gateway timed out", "gateway_timeout")
        return
    except requests.exceptions.ConnectionError as exc:
        logging_util.error("OpenAI proxy stream: connection error: %s", exc)
        yield from _yield_sse_error_and_done("Gateway unreachable", "gateway_error")
        return
    except requests.exceptions.RequestException as exc:
        logging_util.error(
            "OpenAI proxy stream: request error url=%s: %s", safe_url, exc
        )
        yield from _yield_sse_error_and_done("Gateway unreachable", "gateway_error")
        return

    with http_response:
        if _reject_if_gateway_redirect(http_response, safe_url):
            yield from _yield_sse_error_and_done(
                "Gateway returned redirect", "gateway_error"
            )
            return

        try:
            http_response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            err_msg = str(exc)
            resp = getattr(exc, "response", None)
            if resp is not None:
                try:
                    err_body = resp.json()
                    if isinstance(err_body, dict):
                        inner = err_body.get("error")
                        if isinstance(inner, dict):
                            err_msg = str(inner.get("message", err_msg))
                        elif inner is not None:
                            err_msg = str(inner)
                except ValueError:
                    pass
            yield from _yield_sse_error_and_done(err_msg, "gateway_error")
            return

        saw_done = False
        for line in http_response.iter_lines(decode_unicode=True):
            if line is None:
                continue
            text = line.decode("utf-8") if isinstance(line, bytes) else line

            if text == "":
                yield False, "\n\n"
                continue

            decoded = text.rstrip("\r")
            if not decoded:
                continue

            if decoded.startswith(":"):
                yield False, f"{decoded}\n"
                continue

            if decoded.strip() == "data: [DONE]":
                saw_done = True
                continue

            yield False, f"{decoded}\n"

        if not saw_done:
            yield False, "data: [DONE]\n\n"
        yield True, ""


def build_openai_error_response(
    message: str,
    code: str | None = None,
    *,
    error_type: str = "invalid_request_error",
) -> dict[str, Any]:
    """Build an OpenAI-shaped non-streaming error response."""
    err: dict[str, Any] = {"message": message, "type": error_type}
    if code:
        err["code"] = code
    return {"error": err}

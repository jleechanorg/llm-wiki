"""Tests for the OpenAI-compatible inference proxy (/v1/chat/completions and /v1/models).

Covers:
- Payload validation (parse_chat_completions_payload)
- Non-streaming gateway forwarding (invoke_openclaw_gateway)
- Streaming gateway forwarding (invoke_openclaw_gateway_stream)
- Flask route auth (valid/invalid/revoked worldai_ keys)
- Flask route 4xx/5xx from gateway
- Gateway unreachable (502)
- Invalid JSON body (400)
- Missing gateway_url in settings (400)
"""

from __future__ import annotations

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

import pytest

# Ensure project root is in sys.path so 'mvp_site' package imports work.
_project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

# Set required env vars before any mvp_site imports (e.g. world_logic clock-skew
# patch). Direct assignment so empty-string values from shell profiles are overridden.
# Must be at module level so they are set before unittest.main() discovers tests.
os.environ["TESTING_AUTH_BYPASS"] = "true"
os.environ["ALLOW_TEST_AUTH_BYPASS"] = "true"
os.environ["WORLDAI_DEV_MODE"] = "true"
os.environ["MOCK_SERVICES_MODE"] = "true"


# ---------------------------------------------------------------------------
# Payload validation tests
# ---------------------------------------------------------------------------


class TestParsePayload(unittest.TestCase):
    """Validate the OpenAI /chat/completions payload parser."""

    def _valid_payload(self, **overrides):
        base = {
            "model": "gemini-3-flash-preview",
            "messages": [{"role": "user", "content": "hello"}],
        }
        base.update(overrides)
        return base

    def _parse(self, data):
        from mvp_site.llm_providers.openai_proxy_provider import (
            parse_chat_completions_payload,
        )

        return parse_chat_completions_payload(data)

    def test_minimal_valid_payload(self):
        p = self._parse(self._valid_payload())
        assert p.model == "gemini-3-flash-preview"
        assert p.stream is False
        assert p.temperature == 1.0

    def test_stream_flag(self):
        p = self._parse(self._valid_payload(stream=True))
        assert p.stream is True

    def test_temperature_and_max_tokens(self):
        p = self._parse(self._valid_payload(temperature=0.7, max_tokens=512))
        assert p.temperature == 0.7
        assert p.max_tokens == 512

    def test_temperature_accepts_in_range_values(self):
        p = self._parse(self._valid_payload(temperature=1.5))
        assert p.temperature == 1.5

    def test_stream_non_bool_rejected(self):
        with pytest.raises(ValueError, match="stream"):
            self._parse(self._valid_payload(stream="false"))

    def test_messages_items_must_be_objects_with_role(self):
        with pytest.raises(ValueError, match="messages"):
            self._parse(self._valid_payload(messages=[1]))
        with pytest.raises(ValueError, match="role"):
            self._parse(self._valid_payload(messages=[{"content": "x"}]))
        with pytest.raises(ValueError, match="role"):
            self._parse(self._valid_payload(messages=[{"role": "", "content": "x"}]))

    def test_temperature_rejected_above_2(self):
        with pytest.raises(ValueError, match="temperature"):
            self._parse(self._valid_payload(temperature=2.5))

    def test_temperature_rejected_below_0(self):
        with pytest.raises(ValueError, match="temperature"):
            self._parse(self._valid_payload(temperature=-0.1))

    def test_missing_model_rejected(self):
        data = self._valid_payload()
        del data["model"]
        with pytest.raises(ValueError, match="model"):
            self._parse(data)

    def test_empty_messages_rejected(self):
        with pytest.raises(ValueError, match="messages"):
            self._parse(self._valid_payload(messages=[]))

    def test_non_list_messages_rejected(self):
        with pytest.raises(ValueError, match="messages"):
            self._parse(self._valid_payload(messages="hello"))

    def test_max_tokens_capped(self):
        from mvp_site.llm_providers.openai_proxy_provider import (
            MAX_PROXY_MAX_TOKENS,
        )

        p = self._parse(self._valid_payload(max_tokens=999999))
        assert p.max_tokens == MAX_PROXY_MAX_TOKENS

    def test_tools_passed_through(self):
        tools = [
            {"type": "function", "function": {"name": "roll_dice", "parameters": {}}}
        ]
        p = self._parse(self._valid_payload(tools=tools))
        assert p.tools == tools

    def test_response_format_passed_through(self):
        rf = {"type": "json_object"}
        p = self._parse(self._valid_payload(response_format=rf))
        assert p.response_format == rf

    def test_tool_choice_auto(self):
        p = self._parse(self._valid_payload(tool_choice="auto"))
        assert p.tool_choice == "auto"

    def test_tool_choice_object(self):
        choice = {"type": "function", "function": {"name": "roll_dice"}}
        p = self._parse(self._valid_payload(tool_choice=choice))
        assert p.tool_choice == choice

    def test_invalid_tool_choice_rejected(self):
        with pytest.raises(ValueError, match="tool_choice"):
            self._parse(self._valid_payload(tool_choice=123))

    def test_non_dict_body_rejected(self):
        with pytest.raises(ValueError, match="must be a JSON object"):
            self._parse("not a dict")


def _mock_http_response(**kwargs):
    """MagicMock for requests.Response; is_redirect/history default safe (not truthy MagicMocks)."""
    m = MagicMock(**kwargs)
    m.is_redirect = False
    m.history = []
    return m


# ---------------------------------------------------------------------------
# Non-streaming gateway invocation
# ---------------------------------------------------------------------------


class TestInvokeGateway(unittest.TestCase):
    """Test invoke_openclaw_gateway with mocked HTTP responses."""

    def _invoke(
        self,
        gateway_url="https://gateway.example.com",
        gateway_token=None,
        payload=None,
    ):
        from mvp_site.llm_providers.openai_proxy_provider import invoke_openclaw_gateway

        if payload is None:
            payload = {
                "model": "gemini",
                "messages": [{"role": "user", "content": "hi"}],
                "temperature": 1.0,
                "max_tokens": 100,
                "stream": False,
            }
        return invoke_openclaw_gateway(
            gateway_url=gateway_url,
            gateway_token=gateway_token,
            payload=payload,
        )

    @patch("mvp_site.llm_providers.openai_proxy_provider.requests.post")
    def test_success_returns_openai_shape(self, mock_post):
        mock_post.return_value = _mock_http_response(
            status_code=200,
            json=lambda: {"choices": [{"message": {"content": "hello"}}]},
        )
        result = self._invoke()
        assert result.ok is True
        assert result.status_code == 200
        assert result.data["choices"][0]["message"]["content"] == "hello"
        mock_post.assert_called_once()
        call_url = mock_post.call_args[0][0]
        assert "/v1/chat/completions" in call_url
        assert mock_post.call_args[1]["allow_redirects"] is False

    @patch("mvp_site.llm_providers.openai_proxy_provider.requests.post")
    def test_token_sent_when_present(self, mock_post):
        mock_post.return_value = _mock_http_response(
            status_code=200,
            json=lambda: {"choices": [{"message": {"content": ""}}]},
        )
        self._invoke(gateway_token="my-secret-token")
        headers = mock_post.call_args[1]["headers"]
        assert headers["Authorization"] == "Bearer my-secret-token"

    @patch("mvp_site.llm_providers.openai_proxy_provider.requests.post")
    def test_no_token_sent_when_absent(self, mock_post):
        mock_post.return_value = _mock_http_response(
            status_code=200,
            json=lambda: {"choices": [{"message": {"content": ""}}]},
        )
        self._invoke(gateway_token=None)
        headers = mock_post.call_args[1]["headers"]
        assert "Authorization" not in headers

    @patch("mvp_site.llm_providers.openai_proxy_provider.requests.post")
    def test_gateway_4xx_returns_error(self, mock_post):
        # Return {"message": ...} at top level so err_body.get("message") succeeds.
        # Many gateways return this flat shape on error.
        mock_post.return_value = _mock_http_response(
            status_code=401,
            json=lambda: {"message": "Unauthorized"},
            text="Unauthorized",
        )
        result = self._invoke()
        assert result.ok is False
        assert result.status_code == 401
        assert "Unauthorized" in result.error["message"]

    @patch("mvp_site.llm_providers.openai_proxy_provider.requests.post")
    def test_gateway_5xx_propagates_gateway_status(self, mock_post):
        mock_response = _mock_http_response(
            status_code=500,
            json=lambda: {"error": {"message": "Internal error"}},
        )
        mock_response.text = "Internal error"
        mock_post.return_value = mock_response
        result = self._invoke()
        assert result.ok is False
        assert result.status_code == 500

    @patch("mvp_site.llm_providers.openai_proxy_provider.requests.post")
    def test_connection_error_returns_502(self, mock_post):
        import requests

        mock_post.side_effect = requests.exceptions.ConnectionError("DNS failure")
        result = self._invoke()
        assert result.ok is False
        assert result.status_code == 502
        assert result.error["type"] == "gateway_error"

    @patch("mvp_site.llm_providers.openai_proxy_provider.requests.post")
    def test_timeout_returns_504(self, mock_post):
        import requests

        mock_post.side_effect = requests.exceptions.Timeout("timed out")
        result = self._invoke()
        assert result.ok is False
        assert result.status_code == 504
        assert result.error["type"] == "gateway_timeout"

    @patch("mvp_site.llm_providers.openai_proxy_provider.requests.post")
    def test_non_json_response_returns_502(self, mock_post):
        mock_post.return_value = _mock_http_response(
            status_code=200,
            json=lambda: (_ for _ in ()).throw(ValueError("not json")),
        )
        result = self._invoke()
        assert result.ok is False
        assert result.status_code == 502

    @patch("mvp_site.llm_providers.openai_proxy_provider.requests.post")
    def test_gateway_redirect_returns_502(self, mock_post):
        redir = _mock_http_response(
            status_code=302, headers={"Location": "http://127.0.0.1/"}
        )
        redir.is_redirect = True
        mock_post.return_value = redir
        result = self._invoke()
        assert result.ok is False
        assert result.status_code == 502
        assert "redirect" in result.error["message"].lower()


# ---------------------------------------------------------------------------
# Streaming gateway invocation
# ---------------------------------------------------------------------------


class TestInvokeGatewayStream(unittest.TestCase):
    """Test invoke_openclaw_gateway_stream with mocked HTTP responses."""

    @patch("mvp_site.llm_providers.openai_proxy_provider.requests.post")
    def test_yields_sse_lines(self, mock_post):
        from mvp_site.llm_providers.openai_proxy_provider import (
            invoke_openclaw_gateway_stream,
        )

        lines = [
            b'data: {"choices":[{"delta":{"content":"hello"}}]}',
            b"data: [DONE]",
        ]
        mock_resp = MagicMock()
        mock_resp.is_redirect = False
        mock_resp.history = []
        mock_resp.raise_for_status = MagicMock()
        mock_resp.iter_lines = MagicMock(return_value=iter(lines))
        mock_post.return_value = mock_resp

        payload = {"model": "gemini", "messages": [{"role": "user", "content": "hi"}]}
        chunks = list(
            invoke_openclaw_gateway_stream(
                gateway_url="https://gateway.example.com",
                gateway_token=None,
                payload=payload,
            )
        )
        # Last item is (True, "")
        assert chunks[-1][0] is True
        # Non-terminal items are (False, line)
        text_chunks = [c for c in chunks if c[0] is False]
        assert len(text_chunks) >= 1

    @patch("mvp_site.llm_providers.openai_proxy_provider.requests.post")
    def test_connection_error_yields_error_sse(self, mock_post):
        import requests

        mock_post.side_effect = requests.exceptions.ConnectionError("failed")
        from mvp_site.llm_providers.openai_proxy_provider import (
            invoke_openclaw_gateway_stream,
        )

        payload = {"model": "gemini", "messages": [{"role": "user", "content": "hi"}]}
        chunks = list(
            invoke_openclaw_gateway_stream(
                gateway_url="https://gateway.example.com",
                gateway_token=None,
                payload=payload,
            )
        )
        is_done, line = chunks[0]
        assert is_done is False
        assert "error" in line
        assert "gateway_error" in line


# ---------------------------------------------------------------------------
# Flask route tests — integration via test client
# ---------------------------------------------------------------------------


class TestOpenAIProxyRoutes(unittest.TestCase):
    """Test the /v1/chat/completions and /v1/models Flask routes.

    Uses the Flask test client so the full request/response cycle runs,
    with Firestore and requests patched at the appropriate layers.
    """

    @classmethod
    def setup_class(cls):
        # Env vars are set at module level above; nothing to do here.
        pass

    def _client(self):
        # Import here so env vars are set before create_app() runs.
        # Reload so newly added routes (e.g. /v1/chat/completions) are registered.
        # NOTE: reload() updates sys.modules["mvp_site.main"] but NOT the mvp_site.main
        # attribute on the package — reassign it so the binding used below is fresh.
        import importlib

        import mvp_site.main as _m

        importlib.reload(_m)
        # Re-bind so subsequent getattr (e.g. in route handlers) uses the new module
        import mvp_site

        mvp_site.main = _m
        app = _m.create_app()
        app.config["TESTING"] = True
        app.config["PRODUCTION_MODE"] = "false"
        return app.test_client()

    def _auth_headers(self, user_id="test-user-123", email="test@example.com"):
        return {
            "Authorization": "Bearer test-bearer-token",
            "X-Test-Bypass-Auth": "true",
            "X-Test-User-Id": user_id,
            "X-Test-User-Email": email,
        }

    def _patch_url_validation(self):
        """Bypass validate_openclaw_gateway_url so test URLs pass.

        The real validator rejects hostnames that don't resolve in the test environment.
        Patching here lets tests exercise the gateway forwarding logic without DNS.
        The route calls validate_openclaw_gateway_url from main.py (where it's imported).
        """
        return patch(
            "mvp_site.main.validate_openclaw_gateway_url",
            return_value=(
                "https://mock-gateway.test:18789",
                None,
            ),
        )

    def test_chat_completions_no_gateway_url_returns_400(self):
        client = self._client()
        with patch("mvp_site.firestore_service.get_user_settings", return_value={}):
            resp = client.post(
                "/v1/chat/completions",
                headers=self._auth_headers(),
                json={
                    "model": "gemini",
                    "messages": [{"role": "user", "content": "hi"}],
                },
            )
        assert resp.status_code == 400
        body = resp.get_json()
        assert "error" in body
        assert "gateway" in body["error"]["message"].lower()

    def test_chat_completions_invalid_json_returns_400(self):
        client = self._client()
        settings = {
            "openclaw_gateway_url": "https://mock-gateway.test:18789",
            "openclaw_gateway_token": "test-token",
        }
        with patch(
            "mvp_site.firestore_service.get_user_settings", return_value=settings
        ):
            with self._patch_url_validation():
                resp = client.post(
                    "/v1/chat/completions",
                    headers=self._auth_headers(),
                    data="not json",
                    content_type="application/json",
                )
        assert resp.status_code == 400
        body = resp.get_json()
        assert "Invalid JSON" in body["error"]["message"]

    def test_chat_completions_invalid_payload_returns_400(self):
        client = self._client()
        settings = {
            "openclaw_gateway_url": "https://mock-gateway.test:18789",
            "openclaw_gateway_token": "test-token",
        }
        with patch(
            "mvp_site.firestore_service.get_user_settings", return_value=settings
        ):
            with self._patch_url_validation():
                resp = client.post(
                    "/v1/chat/completions",
                    headers=self._auth_headers(),
                    json={
                        "model": "",
                        "messages": [],
                    },  # invalid: empty model + messages
                )
        assert resp.status_code == 400
        body = resp.get_json()
        assert "messages" in body["error"]["message"].lower()

    def test_chat_completions_gateway_unreachable_returns_502(self):
        import requests

        client = self._client()
        settings = {
            "openclaw_gateway_url": "https://jeffreys-macbook.tail5eb762.ts.net:18789",
            "openclaw_gateway_token": "test-token",
        }
        with patch(
            "mvp_site.firestore_service.get_user_settings", return_value=settings
        ):
            with self._patch_url_validation():
                with patch(
                    "mvp_site.llm_providers.openai_proxy_provider.requests.post"
                ) as mock_post:
                    mock_post.side_effect = requests.exceptions.ConnectionError(
                        "DNS failure"
                    )
                    resp = client.post(
                        "/v1/chat/completions",
                        headers=self._auth_headers(),
                        json={
                            "model": "gemini",
                            "messages": [{"role": "user", "content": "hi"}],
                        },
                    )
        assert resp.status_code == 502

    def test_chat_completions_success_non_streaming(self):
        client = self._client()
        settings = {
            "openclaw_gateway_url": "https://jeffreys-macbook.tail5eb762.ts.net:18789",
            "openclaw_gateway_token": "test-token",
        }
        with patch(
            "mvp_site.firestore_service.get_user_settings", return_value=settings
        ):
            with self._patch_url_validation():
                with patch(
                    "mvp_site.llm_providers.openai_proxy_provider.requests.post"
                ) as mock_post:
                    mock_post.return_value = _mock_http_response(
                        status_code=200,
                        json=lambda: {"choices": [{"message": {"content": "Hello!"}}]},
                    )
                    resp = client.post(
                        "/v1/chat/completions",
                        headers=self._auth_headers(),
                        json={
                            "model": "gemini",
                            "messages": [{"role": "user", "content": "hi"}],
                        },
                    )
        assert resp.status_code == 200
        body = resp.get_json()
        assert body["choices"][0]["message"]["content"] == "Hello!"

    def test_chat_completions_success_streaming(self):
        client = self._client()
        settings = {
            "openclaw_gateway_url": "https://jeffreys-macbook.tail5eb762.ts.net:18789",
            "openclaw_gateway_token": "test-token",
        }
        with patch(
            "mvp_site.firestore_service.get_user_settings", return_value=settings
        ):
            with self._patch_url_validation():
                with patch(
                    "mvp_site.llm_providers.openai_proxy_provider.requests.post"
                ) as mock_post:
                    mock_resp = MagicMock()
                    mock_resp.is_redirect = False
                    mock_resp.history = []
                    mock_resp.raise_for_status = MagicMock()
                    mock_resp.iter_lines = MagicMock(
                        return_value=iter(
                            [
                                b'data: {"choices":[{"delta":{"content":"Hi"}}]}',
                                b"data: [DONE]",
                            ]
                        )
                    )
                    mock_post.return_value = mock_resp

                    resp = client.post(
                        "/v1/chat/completions",
                        headers=self._auth_headers(),
                        json={
                            "model": "gemini",
                            "messages": [{"role": "user", "content": "hi"}],
                            "stream": True,
                        },
                    )
        assert resp.status_code == 200
        assert resp.content_type == "text/event-stream; charset=utf-8"

    def test_chat_completions_no_auth_returns_401(self):
        client = self._client()
        resp = client.post(
            "/v1/chat/completions",
            json={
                "model": "gemini",
                "messages": [{"role": "user", "content": "hi"}],
            },
        )
        assert resp.status_code == 401

    def test_chat_completions_revoked_key_returns_401(self):
        client = self._client()
        with patch(
            "mvp_site.firestore_service.lookup_personal_api_key",
            return_value=(None, None),
        ):
            resp = client.post(
                "/v1/chat/completions",
                headers={
                    "Authorization": "Bearer worldai_00000000000000000000000000000000",
                },
                json={
                    "model": "gemini",
                    "messages": [{"role": "user", "content": "hi"}],
                },
            )
        assert resp.status_code == 401

    def test_list_models_no_gateway_url_returns_400(self):
        client = self._client()
        with patch("mvp_site.firestore_service.get_user_settings", return_value={}):
            resp = client.get("/v1/models", headers=self._auth_headers())
        assert resp.status_code == 400

    def test_list_models_gateway_returns_200(self):
        client = self._client()
        settings = {
            "openclaw_gateway_url": "https://jeffreys-macbook.tail5eb762.ts.net:18789",
            "openclaw_gateway_token": "test-token",
        }
        with patch(
            "mvp_site.firestore_service.get_user_settings", return_value=settings
        ):
            with self._patch_url_validation():
                with patch("mvp_site.main._proxy_gateway_get") as mock_get:
                    mock_get.return_value = _mock_http_response(
                        status_code=200,
                        json=lambda: {"data": [{"id": "gemini-3-flash-preview"}]},
                    )
                    resp = client.get("/v1/models", headers=self._auth_headers())
        assert resp.status_code == 200
        body = resp.get_json()
        assert body["data"][0]["id"] == "gemini-3-flash-preview"

    def test_list_models_no_auth_returns_401(self):
        client = self._client()
        resp = client.get("/v1/models")
        assert resp.status_code == 401


if __name__ == "__main__":
    unittest.main()

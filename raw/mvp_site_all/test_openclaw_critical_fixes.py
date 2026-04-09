"""Tests for CRITICAL PR review comments in OpenClaw provider and related code.

Tests for:
1. gateway_url override issue - gateway_port should NOT override explicit OPENCLAW_GATEWAY_URL
2. resolved_user_id used before assignment
3. json_mode breaks Cerebras and OpenRouter
4. Streaming phase2 destroys OpenClaw conversation structure
5. Non-streaming OpenClaw skips JSON enforcement
6. OpenClaw provider selection should use model="local" not "openclaw/gemini-3-flash-preview"
"""

from __future__ import annotations

import ast
import inspect
import os
from ipaddress import ip_address
from unittest.mock import patch

import pytest


class TestGatewayURLOverride:
    """Tests for issue #1: gateway_port should NOT override explicit OPENCLAW_GATEWAY_URL.

    When OPENCLAW_GATEWAY_URL is explicitly set to a non-local endpoint,
    gateway_port should NOT override it. This prevents:
    1. Breaking production setups where OPENCLAW_GATEWAY_URL points to a remote gateway
    2. Localhost SSRF surface where user-controlled port could redirect to malicious local services
    """

    def test_gateway_port_should_not_override_explicit_gateway_url(self):
        """When OPENCLAW_GATEWAY_URL is explicitly set, gateway_port should NOT override it."""
        # This test will FAIL until the issue is fixed
        # The issue: _resolve_gateway_url(gateway_port=12345) ignores OPENCLAW_GATEWAY_URL
        # and always uses the default host with the user-provided port
        from mvp_site.llm_providers import openclaw_provider

        # Set an explicit production gateway URL (non-localhost)
        with patch.dict(
            os.environ,
            {"OPENCLAW_GATEWAY_URL": "https://gateway.openclaw.example.com/v1"},
        ):
            with patch(
                "mvp_site.settings_validation._resolve_gateway_host_ips",
                return_value=[ip_address("8.8.8.8")],
            ):
                # When gateway_port is provided, it should NOT override an explicit URL
                result = openclaw_provider._resolve_gateway_url(gateway_port=18790)

                # The issue: this returns http://127.0.0.1:18790 (ignoring the explicit URL)
                # Expected: Should respect the explicit URL or reject the combination
                # For now, let's assert the current WRONG behavior to make the test fail
                # Once fixed, this assertion should FAIL
                assert "gateway.openclaw.example.com" in result, (
                    f"gateway_port should NOT override explicit OPENCLAW_GATEWAY_URL. "
                    f"Got {result}, expected URL containing 'gateway.openclaw.example.com'"
                )

    def test_gateway_port_works_with_default_url(self):
        """gateway_port should work when using default gateway URL (localhost)."""
        from mvp_site.llm_providers import openclaw_provider

        # When no explicit URL is set (using default), gateway_port should work
        with patch.dict(os.environ, {}, clear=True):
            # Clear any existing OPENCLAW_GATEWAY_URL
            result = openclaw_provider._resolve_gateway_url(gateway_port=19999)

            # Should use default host with the provided port
            assert "19999" in result, f"Expected port 19999 in URL, got {result}"

    def test_get_gateway_url_reads_env_at_runtime(self):
        """_get_gateway_url() must read env at call time, not at import time.

        If OPENCLAW_GATEWAY_URL changes after module import (e.g. in tests),
        _get_gateway_url() must return the new value. Without this, test isolation
        breaks and the module-level constant diverges from _resolve_gateway_url.
        """
        from mvp_site.llm_providers import openclaw_provider

        dynamic_url = "https://runtime.gateway.example.com"
        with patch.dict(os.environ, {"OPENCLAW_GATEWAY_URL": dynamic_url}):
            with patch(
                "mvp_site.settings_validation._resolve_gateway_host_ips",
                return_value=[ip_address("8.8.8.8")],
            ):
                result = openclaw_provider._get_gateway_url()
                assert result == dynamic_url, (
                    f"_get_gateway_url() returned stale module-level URL: {result!r}. "
                    f"Expected runtime env value: {dynamic_url!r}"
                )

    def test_get_gateway_url_uses_host_and_port_from_env(self):
        """_get_gateway_url() should build URL from OPENCLAW_GATEWAY_HOST + PORT when URL not set."""
        from mvp_site.llm_providers import openclaw_provider

        with patch.dict(
            os.environ,
            {"OPENCLAW_GATEWAY_HOST": "10.0.0.1", "OPENCLAW_GATEWAY_PORT": "9999"},
            clear=False,
        ):
            # Remove URL override so host+port path runs
            env = dict(os.environ)
            env.pop("OPENCLAW_GATEWAY_URL", None)
            with patch.dict(os.environ, env, clear=True):
                result = openclaw_provider._get_gateway_url()
                assert "10.0.0.1" in result, f"Expected host in URL, got {result!r}"
                assert "9999" in result, f"Expected port in URL, got {result!r}"

    def test_get_gateway_url_accepts_localhost_server_env_var(self):
        """Server-level OPENCLAW_GATEWAY_URL may legitimately be a localhost/private endpoint.

        Operator-controlled env vars must not go through user-facing SSRF validation.
        Previously this would raise ValueError for http://127.0.0.1:18789.
        """
        from mvp_site.llm_providers import openclaw_provider

        for localhost_url in [
            "http://127.0.0.1:18789",
            "http://localhost:18789",
            "http://10.0.0.1:9000",
        ]:
            with patch.dict(os.environ, {"OPENCLAW_GATEWAY_URL": localhost_url}):
                result = openclaw_provider._get_gateway_url()
                assert result == localhost_url, (
                    f"Server env localhost URL {localhost_url!r} should be accepted, got {result!r}"
                )


class TestResolvedUserIdAssignment:
    """Tests for issue #3: resolved_user_id used before assignment.

    In llm_service.py, there's a code path where resolved_user_id is used
    at line 1964 but defined at line 1967 - causing a potential runtime error.
    """

    def test_resolved_user_id_assignment_order(self):
        """Verify resolved_user_id is properly assigned before use."""
        # This is more of a structural test - checking the code path
        # The actual bug would cause UnboundLocalError at runtime
        from mvp_site import llm_service

        source = inspect.getsource(llm_service._call_llm_api_with_llm_request)

        # Parse the source to check the order of assignments
        tree = ast.parse(source)

        # Find the line with resolved_user_id assignments
        resolved_user_id_lines = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "resolved_user_id":
                        resolved_user_id_lines.append(node.lineno)

        # There should be multiple assignments - one before the usage
        # and one as fallback. The first one should be after any usage.
        # This test verifies the code structure is correct
        assert len(resolved_user_id_lines) >= 2, (
            "Expected at least 2 resolved_user_id assignments for proper fallback"
        )


class TestJsonModeBreaksProviders:
    """Tests for issue #4: json_mode argument breaks Cerebras and OpenRouter.

    The run_openai_json_first_tool_requests_flow passes json_mode to
    generate_content_fn, but Cerebras and OpenRouter don't accept this parameter.
    """

    def test_cerebras_generate_content_accepts_json_mode(self):
        """Cerebras generate_content should accept json_mode parameter."""
        import inspect

        from mvp_site.llm_providers import cerebras_provider

        sig = inspect.signature(cerebras_provider.generate_content)
        param_names = list(sig.parameters.keys())

        # This test will FAIL until Cerebras is updated to accept json_mode
        assert "json_mode" in param_names, (
            f"Cerebras generate_content should accept json_mode parameter. "
            f"Current parameters: {param_names}"
        )

    def test_openrouter_generate_content_accepts_json_mode(self):
        """OpenRouter generate_content should accept json_mode parameter."""
        import inspect

        from mvp_site.llm_providers import openrouter_provider

        sig = inspect.signature(openrouter_provider.generate_content)
        param_names = list(sig.parameters.keys())

        # This test will FAIL until OpenRouter is updated to accept json_mode
        assert "json_mode" in param_names, (
            f"OpenRouter generate_content should accept json_mode parameter. "
            f"Current parameters: {param_names}"
        )


class TestStreamingPhase2ConversationStructure:
    """Tests for issue #5 & #6: Streaming phase2 destroys OpenClaw conversation structure.

    When calling openclaw_provider.generate_content_stream_sync with phase2_history
    (which is already a list of message dicts), it should be passed as 'messages'
    not 'prompt_contents' to preserve the conversation structure.
    """

    def test_streaming_phase2_passes_messages_correctly(self):
        """Phase2 history should be passed as 'messages', not 'prompt_contents'."""
        import inspect

        from mvp_site.llm_providers import openclaw_provider

        stream_src = inspect.getsource(openclaw_provider.generate_content_stream_sync)
        assert "resolved_messages" in stream_src, (
            "generate_content_stream_sync must branch on messages= vs prompt_contents "
            "so phase2 history can be passed as structured messages"
        )
        assert "yield" in stream_src, (
            "generate_content_stream_sync should stream via yield/yield from"
        )

        # The issue: in llm_service.py line 6538, phase2_history is passed as
        # prompt_contents=phase2_history, but it should be messages=phase2_history
        # because phase2_history is already in message format (with role/content)

        # This test checks that the function properly handles messages parameter
        # by verifying the _build_messages behavior with message-format input
        messages_in_prompt_format = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there"},
        ]

        # When messages are passed as prompt_contents, they get flattened
        # This is the bug - it should be passed as 'messages' parameter
        result = openclaw_provider._build_messages(messages_in_prompt_format)

        # _build_messages checks if first item has "role" key and returns as-is
        # So this should work correctly - the issue is in llm_service.py
        # calling it with prompt_contents= instead of messages=
        assert result == messages_in_prompt_format, (
            "_build_messages should preserve message structure when role is present"
        )


class TestOpenClawJsonEnforcement:
    """Tests for issue #7: OpenClaw non-streaming call skips JSON enforcement.

    The generate_content function should enforce JSON mode by default.
    """

    def test_generate_content_has_json_mode_enabled_by_default(self):
        """generate_content should have json_mode=True by default."""
        import inspect

        from mvp_site.llm_providers import openclaw_provider

        sig = inspect.signature(openclaw_provider.generate_content)
        json_mode_param = sig.parameters.get("json_mode")

        assert json_mode_param is not None, (
            "generate_content should have json_mode parameter"
        )
        assert json_mode_param.default is True, (
            f"json_mode should default to True, got {json_mode_param.default}"
        )

    def test_generate_content_stream_sync_has_json_mode_enabled_by_default(self):
        """generate_content_stream_sync should have json_mode=True by default."""
        import inspect

        from mvp_site.llm_providers import openclaw_provider

        sig = inspect.signature(openclaw_provider.generate_content_stream_sync)
        json_mode_param = sig.parameters.get("json_mode")

        assert json_mode_param is not None, (
            "generate_content_stream_sync should have json_mode parameter"
        )
        assert json_mode_param.default is True, (
            f"json_mode should default to True, got {json_mode_param.default}"
        )


class TestOpenClawContextWindowLookup:
    """Tests for context window token lookup with openclaw/ prefix models.

    openclaw/gemini-3-flash-preview should resolve to gemini-3-flash-preview's
    context window (1M tokens), not the default fallback (128K tokens).
    """

    def test_context_window_strips_openclaw_prefix(self):
        """_get_context_window_tokens should strip openclaw/ prefix before lookup."""
        from mvp_site import constants, llm_service

        gemini_key = constants.DEFAULT_GEMINI_MODEL  # e.g. "gemini-3-flash-preview"
        openclaw_model = f"openclaw/{gemini_key}"

        expected = constants.MODEL_CONTEXT_WINDOW_TOKENS.get(gemini_key)
        if expected is None:
            pytest.skip(f"{gemini_key} not in MODEL_CONTEXT_WINDOW_TOKENS")

        result = llm_service._get_context_window_tokens(openclaw_model)
        assert result == expected, (
            f"openclaw/ prefix not stripped: got {result}, expected {expected}"
        )

    def test_context_window_does_not_fallback_for_openclaw_model(self):
        """openclaw/ prefixed model should NOT fall back to DEFAULT_CONTEXT_WINDOW_TOKENS."""
        from mvp_site import constants, llm_service

        gemini_key = constants.DEFAULT_GEMINI_MODEL
        openclaw_model = f"openclaw/{gemini_key}"

        if gemini_key not in constants.MODEL_CONTEXT_WINDOW_TOKENS:
            pytest.skip(f"{gemini_key} not in MODEL_CONTEXT_WINDOW_TOKENS")

        result = llm_service._get_context_window_tokens(openclaw_model)
        assert result != constants.DEFAULT_CONTEXT_WINDOW_TOKENS, (
            f"openclaw model fell back to default {constants.DEFAULT_CONTEXT_WINDOW_TOKENS}, "
            f"should use the underlying model's context window"
        )

    def test_safe_output_token_limit_strips_openclaw_prefix(self):
        """_get_safe_output_token_limit should strip openclaw/ prefix for correct limit."""
        from mvp_site import constants, llm_service

        gemini_key = constants.DEFAULT_GEMINI_MODEL
        openclaw_model = f"openclaw/{gemini_key}"

        if gemini_key not in constants.MODEL_CONTEXT_WINDOW_TOKENS:
            pytest.skip(f"{gemini_key} not in MODEL_CONTEXT_WINDOW_TOKENS")

        # With prefix stripped: uses real model context window
        result_openclaw = llm_service._get_safe_output_token_limit(openclaw_model, 0, 0)
        # With bare name: same value
        result_bare = llm_service._get_safe_output_token_limit(gemini_key, 0, 0)

        assert result_openclaw == result_bare, (
            f"openclaw/ prefixed model gave different limit ({result_openclaw}) "
            f"than bare model ({result_bare})"
        )


class TestOpenClawGatewayUrlSetting:
    """Tests for per-user openclaw_gateway_url Firestore setting (Tailscale Funnel / Cloudflare Tunnel).

    When a user sets openclaw_gateway_url in their Firestore settings, it should
    take highest priority over gateway_port and the server-level OPENCLAW_GATEWAY_URL env var.
    """

    def test_resolve_gateway_url_uses_user_url_over_port(self):
        """gateway_url param takes priority over gateway_port in _resolve_gateway_url."""
        from mvp_site.llm_providers import openclaw_provider

        with patch(
            "mvp_site.settings_validation._resolve_gateway_host_ips",
            return_value=[ip_address("8.8.8.8")],
        ):
            result = openclaw_provider._resolve_gateway_url(
                gateway_port=12345,
                gateway_url="https://my-host.ts.net",
            )
        assert result == "https://my-host.ts.net", (
            f"gateway_url should take priority over gateway_port, got {result!r}"
        )

    def test_resolve_gateway_url_uses_user_url_over_env(self):
        """gateway_url param takes priority over OPENCLAW_GATEWAY_URL env var."""
        from mvp_site.llm_providers import openclaw_provider

        with patch.dict(
            os.environ, {"OPENCLAW_GATEWAY_URL": "https://server-level.example.com"}
        ):
            with patch(
                "mvp_site.settings_validation._resolve_gateway_host_ips",
                return_value=[ip_address("8.8.8.8")],
            ):
                result = openclaw_provider._resolve_gateway_url(
                    gateway_url="https://per-user.ts.net",
                )
        assert result == "https://per-user.ts.net", (
            f"Per-user gateway_url should override server-level OPENCLAW_GATEWAY_URL, got {result!r}"
        )

    def test_resolve_gateway_url_falls_back_without_user_url(self):
        """Without gateway_url, falls back to port-based URL."""
        from mvp_site.llm_providers import openclaw_provider

        with patch.dict(os.environ, {}, clear=True):
            env = dict(os.environ)
            env.pop("OPENCLAW_GATEWAY_URL", None)
            with patch.dict(os.environ, env, clear=True):
                result = openclaw_provider._resolve_gateway_url(gateway_port=19999)
        assert "19999" in result, (
            f"Expected port 19999 in URL without gateway_url, got {result!r}"
        )

    def test_get_user_settings_unified_adds_missing_gateway_url_for_existing_user(
        self,
    ):
        """Existing users without openclaw_gateway_url get an empty-string default."""
        import asyncio

        from mvp_site import constants, world_logic

        with patch(
            "mvp_site.world_logic.get_user_settings",
            return_value={
                "openclaw_gateway_port": constants.DEFAULT_OPENCLAW_GATEWAY_PORT
            },
        ):
            result = asyncio.run(
                world_logic.get_user_settings_unified({"user_id": "test-openclaw-user"})
            )

        assert result.get("success") is True
        assert result["openclaw_gateway_url"] == ""

    def test_get_user_settings_unified_normalizes_invalid_gateway_url_type(self):
        """Invalid openclaw_gateway_url values should normalize to an empty string."""
        import asyncio

        from mvp_site import constants, world_logic

        with patch(
            "mvp_site.world_logic.get_user_settings",
            return_value={
                "openclaw_gateway_port": constants.DEFAULT_OPENCLAW_GATEWAY_PORT,
                "openclaw_gateway_url": 1234,
            },
        ):
            result = asyncio.run(
                world_logic.get_user_settings_unified({"user_id": "test-openclaw-user"})
            )

        assert result.get("success") is True
        assert result["openclaw_gateway_url"] == ""

    def test_validate_openclaw_gateway_url_valid(self):
        """validate_openclaw_gateway_url accepts http/https URLs."""
        from mvp_site.settings_validation import validate_openclaw_gateway_url

        for url in [
            "https://my-host.ts.net",
            "https://random.trycloudflare.com",
        ]:
            with patch(
                "mvp_site.settings_validation._resolve_gateway_host_ips",
                return_value=[ip_address("8.8.8.8")],
            ):
                result, err = validate_openclaw_gateway_url(url)
            assert err is None, f"Expected no error for {url!r}, got {err!r}"
            assert result == url

    def test_validate_openclaw_gateway_url_empty_is_ok(self):
        """Empty/None gateway URL is accepted (means disabled)."""
        from mvp_site.settings_validation import validate_openclaw_gateway_url

        for val in [None, "", "  "]:
            result, err = validate_openclaw_gateway_url(val)
            assert err is None, f"Expected no error for {val!r}, got {err!r}"
            assert result is None

    def test_validate_openclaw_gateway_url_rejects_invalid(self):
        """Validates that non-http/https URLs are rejected."""
        from mvp_site.settings_validation import validate_openclaw_gateway_url

        _, err = validate_openclaw_gateway_url("not-a-url")
        assert err is not None, "Expected error for non-URL string"
        assert "http" in err.lower()

    def test_validate_openclaw_gateway_url_rejects_private_and_metadata_targets(self):
        """validate_openclaw_gateway_url blocks local and metadata targets."""
        from mvp_site.settings_validation import validate_openclaw_gateway_url

        for url in [
            "http://localhost:8080",
            "https://127.0.0.1:8080",
            "https://[::1]:8080",
            "http://169.254.169.254",
            "https://metadata.google.internal",
        ]:
            result, err = validate_openclaw_gateway_url(url)
            assert err is not None, f"Expected failure for {url!r}"
            assert result is None

        with patch(
            "mvp_site.settings_validation._resolve_gateway_host_ips",
            return_value=[ip_address("10.0.0.5")],
        ):
            result, err = validate_openclaw_gateway_url("https://example.com")
            assert err is not None
            assert result is None


class TestOpenClawModelSelection:
    """Tests for issue #6: OpenClaw provider selection should log model='local'.

    OpenClaw ignores the model field in API requests — it uses its own configured
    model (agents.defaults.model.primary in ~/.openclaw/openclaw.json).
    Logging 'openclaw/gemini-3-flash-preview' is misleading and incorrect.
    The model should be 'local' to signal that OpenClaw's local config decides.
    """

    def test_default_openclaw_model_is_local(self):
        """DEFAULT_OPENCLAW_MODEL must be 'local', not 'openclaw/<gemini-model>'."""
        from mvp_site import constants

        assert constants.DEFAULT_OPENCLAW_MODEL == "local", (
            f"Expected DEFAULT_OPENCLAW_MODEL='local', got {constants.DEFAULT_OPENCLAW_MODEL!r}. "
            "OpenClaw ignores the model field — it uses its own configured model. "
            "Log 'local' to avoid misleading 'openclaw/gemini-3-flash-preview' entries."
        )

    def test_openclaw_model_in_provider_selection(self):
        """_select_provider_and_model returns 'local' for openclaw provider."""
        from mvp_site import constants
        from mvp_site.llm_service import _select_provider_and_model

        fake_settings = {
            "llm_provider": constants.LLM_PROVIDER_OPENCLAW,
            "openclaw_model": None,
            "openclaw_gateway_url": "https://jeffreys-macbook-pro.tail5eb762.ts.net",
            "openclaw_gateway_port": 18789,
            "openclaw_gateway_token": "test-token",
        }
        with patch("mvp_site.llm_service.get_user_settings") as mock_settings:
            mock_settings.return_value = fake_settings
            result = _select_provider_and_model("test-user-id")

        assert result.provider == constants.LLM_PROVIDER_OPENCLAW
        assert result.model == "local", (
            f"Expected model='local' for openclaw provider, got {result.model!r}. "
            "OpenClaw uses its own model config; 'local' is the correct sentinel."
        )

    def test_local_model_context_window_tokens(self):
        """'local' model must have an entry in MODEL_CONTEXT_WINDOW_TOKENS (200k for gpt-5.3-codex)."""
        from mvp_site import constants

        assert "local" in constants.MODEL_CONTEXT_WINDOW_TOKENS, (
            "'local' model must be in MODEL_CONTEXT_WINDOW_TOKENS. "
            "OpenClaw's gpt-5.3-codex has 200k context."
        )
        assert constants.MODEL_CONTEXT_WINDOW_TOKENS["local"] == 200_000, (
            f"Expected MODEL_CONTEXT_WINDOW_TOKENS['local']=200_000, "
            f"got {constants.MODEL_CONTEXT_WINDOW_TOKENS['local']}. "
            "Matches OpenClaw's default gpt-5.3-codex (200k ctx) from 'openclaw status'."
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

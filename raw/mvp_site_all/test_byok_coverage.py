from __future__ import annotations

import contextlib
import os
from unittest.mock import MagicMock, patch

import pytest

from mvp_site.llm_providers import gemini_provider
from mvp_site.llm_providers.gemini_provider import _TestClient
from testing_ui.lib.byok_browser_base import ByokBrowserTestBase


@pytest.fixture
def mock_genai_client():
    with patch("mvp_site.llm_providers.gemini_provider.genai.Client") as mock:
        yield mock


def test_get_client_byok_creates_new_client(mock_genai_client):
    """Verify that get_client with an API key creates a new genai.Client."""
    api_key = "custom-user-key"
    client = gemini_provider.get_client(api_key=api_key)

    mock_genai_client.assert_called_once()
    call_args = mock_genai_client.call_args
    assert call_args.kwargs["api_key"] == api_key
    assert client == mock_genai_client.return_value


@patch.dict(os.environ, {"TESTING_AUTH_BYPASS": "true"})
def test_get_client_byok_respects_test_bypass_with_test_key():
    """Verify that get_client returns a TestClient if bypass is on and key looks like a test key."""
    api_key = "test-api-key-123"
    client = gemini_provider.get_client(api_key=api_key)
    assert isinstance(client, _TestClient)


@patch.dict(os.environ, {"TESTING_AUTH_BYPASS": "true"})
def test_get_client_byok_ignores_test_bypass_with_real_key(mock_genai_client):
    """Verify that get_client returns a real Client if bypass is on but key looks real."""
    api_key = "real-api-key-123"
    client = gemini_provider.get_client(api_key=api_key)

    # Should NOT be a _TestClient
    assert not isinstance(client, _TestClient)
    # Should have initialized a real client
    mock_genai_client.assert_called_once()


def test_generate_json_mode_content_propagates_api_key(mock_genai_client):
    """Verify that generate_json_mode_content passes the api_key to get_client."""
    # Mock the client instance returned by get_client
    mock_client_instance = mock_genai_client.return_value
    
    # Mock the models.generate_content method that generate_json_mode_content actually calls
    mock_response = MagicMock()
    mock_response.text = '{"key": "value"}'
    mock_response.candidates = []
    mock_client_instance.models.generate_content.return_value = mock_response
    
    gemini_provider.generate_json_mode_content(
        prompt_contents="test prompt",
        model_name="gemini-pro",
        system_instruction_text="You are a helper.",
        temperature=0.7,
        safety_settings=[],
        json_mode_max_output_tokens=100,
        json_mode=True,
        api_key="propagated-key"
    )

    # Check that genai.Client was initialized with the key
    mock_genai_client.assert_called()
    call_args = mock_genai_client.call_args
    assert call_args.kwargs["api_key"] == "propagated-key"


@patch.dict(
    os.environ,
    {"MCP_TEST_USER_EMAIL": "mcp-worker@example.com", "TEST_EMAIL": "legacy@example.com"},
)
def test_byok_browser_base_prefers_generic_test_user_email_env():
    base = ByokBrowserTestBase(testing_auth_bypass=True)
    assert base.test_user_email == "mcp-worker@example.com"


@patch.dict(os.environ, {"MCP_TEST_USER_EMAIL": "", "TEST_EMAIL": "legacy@example.com"})
def test_byok_browser_base_falls_back_to_test_email_env():
    base = ByokBrowserTestBase(testing_auth_bypass=True)
    assert base.test_user_email == "legacy@example.com"


@pytest.mark.skipif(
    os.getenv("RUN_REAL_UI_TESTS", "").strip().lower() not in {"1", "true", "yes", "on"},
    reason="Set RUN_REAL_UI_TESTS=true to run real Playwright BYOK flow.",
)
def test_byok_settings_controls_present_real_playwright_flow():
    """Exercise real settings DOM via Playwright and BYOK browser base helpers."""
    base = ByokBrowserTestBase(testing_auth_bypass=True)
    try:
        base.setup_server()
        base.setup_browser()
        assert base.navigate_to_settings() is True
        assert base.page.locator("#geminiApiKey").count() == 1
        assert base.page.locator("#toggleGeminiKey").count() == 1
        assert base.page.locator("#clearGeminiKey").count() == 1
        assert base.ensure_provider_visibility("openrouter") is True
        assert base.page.locator("#openrouterApiKey").count() == 1
    finally:
        with contextlib.suppress(Exception):
            base.teardown_browser()
        with contextlib.suppress(Exception):
            base.stop_server()

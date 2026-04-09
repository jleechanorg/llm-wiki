"""
Test coverage for Gemini request size logging in generate_json_mode_content.

Ensures that request size metrics (characters, tokens, bytes) are correctly logged
before API calls, including defensive handling for various content structures.
"""

# ruff: noqa: PT009

import contextlib
import os
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import httpx
import pytest

from mvp_site import constants, llm_service
from mvp_site.custom_types import UserId
from mvp_site.game_state import GameState
from mvp_site.gemini_cache_manager import CampaignCacheManager, get_cache_manager
from mvp_site.llm_providers import gemini_provider
from mvp_site.llm_request import LLMRequest
from mvp_site.tests.fake_llm import FakeLLMResponse, FakePart

def create_llm_response_mock(prompt_tokens=100, cached_tokens=0, text="{}"):
    """Helper to create a robust LLMResponse mock for testing."""
    mock = FakeLLMResponse(text=text)
    mock.usage_metadata = SimpleNamespace(
        prompt_token_count=prompt_tokens,
        cached_content_token_count=cached_tokens,
        candidates_token_count=10,
    )
    candidate = SimpleNamespace(content=SimpleNamespace(parts=[FakePart(text=text)]))
    mock.candidates = [candidate]
    return mock



@pytest.fixture(autouse=True)
def clear_testing_env(monkeypatch):
    """Clear testing environment variables."""
    monkeypatch.delenv("TESTING", raising=False)
    monkeypatch.delenv("MOCK_SERVICES_MODE", raising=False)


@pytest.fixture
def mock_gemini_client():
    """Create a mock Gemini client."""
    client = MagicMock()
    response = create_llm_response_mock(text="{\"narrative\": \"Test response\"}")
    client.models.generate_content.return_value = response
    return client


@pytest.fixture
def mock_contents_with_parts():
    """Create mock contents with parts attribute (google.genai.types.Content)."""
    part1 = SimpleNamespace(text="Hello world")
    part2 = SimpleNamespace(text=" from Gemini")
    content_item = SimpleNamespace(parts=[part1, part2])
    return [content_item]


@pytest.fixture
def mock_contents_with_strings():
    """Create mock contents as list of strings."""
    return ["First string", " and second string"]


@pytest.fixture
def mock_contents_single_string():
    """Create mock contents as single string."""
    return "Single string content"


def test_logs_request_size_with_parts_content(
    mock_gemini_client, mock_contents_with_parts, caplog
):
    """Test request size logging with Content objects containing parts."""
    caplog.set_level("INFO")

    with patch("mvp_site.llm_providers.gemini_provider.get_client") as mock_get_client:
        mock_get_client.return_value = mock_gemini_client

        gemini_provider.generate_json_mode_content(
            prompt_contents=mock_contents_with_parts,
            model_name="gemini-2.5-flash",
            system_instruction_text="You are a helpful assistant",
            temperature=0.7,
            safety_settings=[],
            json_mode_max_output_tokens=2048,
        )

        # Verify request size was logged
        log_messages = [record.message for record in caplog.records]
        request_logs = [msg for msg in log_messages if "GEMINI_REQUEST" in msg]
        assert len(request_logs) == 1

        # Verify content metrics are present
        log_msg = request_logs[0]
        assert "contents=" in log_msg
        assert "ch/" in log_msg  # characters
        assert "tk/" in log_msg  # tokens
        assert "b," in log_msg  # bytes
        assert "system=" in log_msg
        assert "total=" in log_msg
        assert "model=gemini-2.5-flash" in log_msg


def test_logs_request_size_with_string_list_content(
    mock_gemini_client, mock_contents_with_strings, caplog
):
    """Test request size logging with list of strings."""
    caplog.set_level("INFO")

    with patch("mvp_site.llm_providers.gemini_provider.get_client") as mock_get_client:
        mock_get_client.return_value = mock_gemini_client

        gemini_provider.generate_json_mode_content(
            prompt_contents=mock_contents_with_strings,
            model_name="gemini-2.5-flash",
            system_instruction_text=None,
            temperature=0.7,
            safety_settings=[],
            json_mode_max_output_tokens=2048,
        )

        # Verify request size was logged
        log_messages = [record.message for record in caplog.records]
        request_logs = [msg for msg in log_messages if "GEMINI_REQUEST" in msg]
        assert len(request_logs) == 1

        # Verify system instruction is 0 when None
        log_msg = request_logs[0]
        assert "system=0ch/0tk/0b" in log_msg


def test_logs_request_size_with_single_string_content(
    mock_gemini_client, mock_contents_single_string, caplog
):
    """Test request size logging with single string content."""
    caplog.set_level("INFO")

    with patch("mvp_site.llm_providers.gemini_provider.get_client") as mock_get_client:
        mock_get_client.return_value = mock_gemini_client

        gemini_provider.generate_json_mode_content(
            prompt_contents=[mock_contents_single_string],
            model_name="gemini-2.5-flash",
            system_instruction_text="System prompt",
            temperature=1.0,
            safety_settings=[],
            json_mode_max_output_tokens=4096,
        )

        # Verify request size was logged with correct parameters
        log_messages = [record.message for record in caplog.records]
        request_logs = [msg for msg in log_messages if "GEMINI_REQUEST" in msg]
        assert len(request_logs) == 1

        log_msg = request_logs[0]
        assert "max_output=4096" in log_msg
        assert "temp=1.0" in log_msg


def test_logs_tools_count_and_code_execution(
    mock_gemini_client, mock_contents_with_parts, caplog
):
    """Test logging includes tool count and code execution detection."""
    caplog.set_level("INFO")

    # Create tools with correct structure (OpenAI format)
    tools_list = [
        {
            "function": {
                "name": "get_weather",
                "description": "Get weather info",
                "parameters": {"type": "object", "properties": {}},
            }
        }
    ]

    with patch("mvp_site.llm_providers.gemini_provider.get_client") as mock_get_client:
        mock_get_client.return_value = mock_gemini_client

        # Use Gemini 3.x model to enable code execution
        gemini_provider.generate_json_mode_content(
            prompt_contents=mock_contents_with_parts,
            model_name="gemini-3.0-flash",
            system_instruction_text=None,
            temperature=0.7,
            safety_settings=[],
            json_mode_max_output_tokens=2048,
            tools=tools_list,
            enable_code_execution=True,
        )

        # Verify tools count and code execution are logged
        log_messages = [record.message for record in caplog.records]
        request_logs = [msg for msg in log_messages if "GEMINI_REQUEST" in msg]
        assert len(request_logs) == 1

        log_msg = request_logs[0]
        # Should log function tool count and code execution separately
        assert "tools=" in log_msg
        assert "code_exec=True" in log_msg


def test_logs_without_tools(mock_gemini_client, mock_contents_with_parts, caplog):
    """Test logging when no tools are present."""
    caplog.set_level("INFO")

    with patch("mvp_site.llm_providers.gemini_provider.get_client") as mock_get_client:
        mock_get_client.return_value = mock_gemini_client

        gemini_provider.generate_json_mode_content(
            prompt_contents=mock_contents_with_parts,
            model_name="gemini-2.5-flash",
            system_instruction_text=None,
            temperature=0.7,
            safety_settings=[],
            json_mode_max_output_tokens=2048,
            tools=None,
        )

        # Verify tools count is 0
        log_messages = [record.message for record in caplog.records]
        request_logs = [msg for msg in log_messages if "GEMINI_REQUEST" in msg]
        assert len(request_logs) == 1

        log_msg = request_logs[0]
        assert "tools=0" in log_msg
        assert "code_exec=False" in log_msg


def test_logging_exception_handled_gracefully(mock_gemini_client, caplog):
    """Test that logging exceptions are caught and logged as warnings."""
    caplog.set_level("WARNING")

    with patch("mvp_site.llm_providers.gemini_provider.get_client") as mock_get_client:
        mock_get_client.return_value = mock_gemini_client

        # Patch estimate_tokens to raise an exception
        with patch(
            "mvp_site.llm_providers.gemini_provider.estimate_tokens"
        ) as mock_estimate:
            mock_estimate.side_effect = Exception("Test logging error")

            # Should not raise - exception should be caught
            gemini_provider.generate_json_mode_content(
                prompt_contents=["test content"],
                model_name="gemini-2.5-flash",
                system_instruction_text=None,
                temperature=0.7,
                safety_settings=[],
                json_mode_max_output_tokens=2048,
            )

            # Verify warning was logged and exception was caught
            log_messages = [record.message for record in caplog.records]
            warning_logs = [
                msg for msg in log_messages if "Could not log request details" in msg
            ]
            assert len(warning_logs) == 1
            # Verify the exception message is included
            assert "Test logging error" in warning_logs[0]

            # Verify API call still happened despite logging error
            assert mock_gemini_client.models.generate_content.called


def test_token_estimation_accuracy(mock_gemini_client, caplog):
    """Test that token estimation matches expected ratio (1 token per 4 chars)."""
    caplog.set_level("INFO")

    # Create content with known character count (100 chars = ~25 tokens)
    test_text = "a" * 100
    part = SimpleNamespace(text=test_text)
    content = SimpleNamespace(parts=[part])

    with patch("mvp_site.llm_providers.gemini_provider.get_client") as mock_get_client:
        mock_get_client.return_value = mock_gemini_client

        gemini_provider.generate_json_mode_content(
            prompt_contents=[content],
            model_name="gemini-2.5-flash",
            system_instruction_text=None,
            temperature=0.7,
            safety_settings=[],
            json_mode_max_output_tokens=2048,
        )

        # Verify token estimation
        log_messages = [record.message for record in caplog.records]
        request_logs = [msg for msg in log_messages if "GEMINI_REQUEST" in msg]
        assert len(request_logs) == 1

        log_msg = request_logs[0]
        # 100 chars = 25 tokens (100 // 4)
        assert "contents=100ch/25tk/100b" in log_msg


def test_mixed_content_types_in_list(mock_gemini_client, caplog):
    """Test logging with mixed content types (parts and strings)."""
    caplog.set_level("INFO")

    # Mix of Content with parts and plain strings
    part = SimpleNamespace(text="Part text")
    content_with_parts = SimpleNamespace(parts=[part])
    plain_string = "Plain string"
    mixed_contents = [content_with_parts, plain_string]

    with patch("mvp_site.llm_providers.gemini_provider.get_client") as mock_get_client:
        mock_get_client.return_value = mock_gemini_client

        gemini_provider.generate_json_mode_content(
            prompt_contents=mixed_contents,
            model_name="gemini-2.5-flash",
            system_instruction_text="System instruction",
            temperature=0.7,
            safety_settings=[],
            json_mode_max_output_tokens=2048,
        )

        # Verify both content types were processed
        log_messages = [record.message for record in caplog.records]
        request_logs = [msg for msg in log_messages if "GEMINI_REQUEST" in msg]
        assert len(request_logs) == 1

        # Should include text from both content types
        log_msg = request_logs[0]
        assert "contents=" in log_msg
        # Combined length: "Part text" (9) + "Plain string" (12) = 21 chars
        assert "21ch" in log_msg


def test_empty_content_handled(mock_gemini_client, caplog):
    """Test logging with empty content."""
    caplog.set_level("INFO")

    with patch("mvp_site.llm_providers.gemini_provider.get_client") as mock_get_client:
        mock_get_client.return_value = mock_gemini_client

        gemini_provider.generate_json_mode_content(
            prompt_contents=[],
            model_name="gemini-2.5-flash",
            system_instruction_text="",
            temperature=0.7,
            safety_settings=[],
            json_mode_max_output_tokens=2048,
        )

        # Verify 0 size is logged
        log_messages = [record.message for record in caplog.records]
        request_logs = [msg for msg in log_messages if "GEMINI_REQUEST" in msg]
        assert len(request_logs) == 1

        log_msg = request_logs[0]
        assert "contents=0ch/0tk/0b" in log_msg
        assert "system=0ch/0tk/0b" in log_msg
        assert "total=0ch/0tk/0b" in log_msg


def test_transport_capture_writes_http_exchange_jsonl(tmp_path, monkeypatch):
    """Enabling transport capture should write full request/response JSONL entries."""
    capture_path = tmp_path / "gemini_http_request_responses.jsonl"
    monkeypatch.setenv(
        "GEMINI_HTTP_REQUEST_RESPONSE_CAPTURE_PATH",
        str(capture_path),
    )

    mock_client = MagicMock()

    def _fake_generate_content(**_kwargs):
        with httpx.Client() as local_client:
            req = local_client.build_request(
                "POST",
                "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent",
                content='{"contents":"hello"}',
                headers={"Authorization": "Bearer test-secret"},
            )
            return local_client.send(req)

    mock_client.models.generate_content.side_effect = _fake_generate_content

    def _fake_send(self, request, *args, **kwargs):  # noqa: ARG001
        return httpx.Response(
            200,
            request=request,
            headers={"content-type": "application/json"},
            content=b'{"candidates":[{"content":{"parts":[{"text":"ok"}]}}]}',
        )

    monkeypatch.setattr(httpx.Client, "send", _fake_send, raising=True)

    with patch("mvp_site.llm_providers.gemini_provider.get_client", return_value=mock_client):
        gemini_provider.generate_json_mode_content(
            prompt_contents=["hello"],
            model_name="gemini-3-flash-preview",
            system_instruction_text=None,
            temperature=0.7,
            safety_settings=[],
            json_mode_max_output_tokens=1024,
        )

    content = capture_path.read_text(encoding="utf-8")
    assert '"type": "http_request"' in content
    assert '"type": "http_response"' in content
    assert '"method": "POST"' in content
    assert "generativelanguage.googleapis.com" in content
    assert "hello" in content


def test_transport_capture_logs_transport_errors(tmp_path, monkeypatch):
    """Transport exceptions should still be captured with error metadata."""
    capture_path = tmp_path / "gemini_http_request_responses.jsonl"
    monkeypatch.setenv(
        "GEMINI_HTTP_REQUEST_RESPONSE_CAPTURE_PATH",
        str(capture_path),
    )

    mock_client = MagicMock()

    def _fake_generate_content(**_kwargs):
        with httpx.Client() as local_client:
            req = local_client.build_request(
                "POST",
                "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent",
                content='{"contents":"hello"}',
            )
            return local_client.send(req)

    mock_client.models.generate_content.side_effect = _fake_generate_content

    def _fake_send(self, request, *args, **kwargs):  # noqa: ARG001
        raise httpx.ReadTimeout("timed out", request=request)

    monkeypatch.setattr(httpx.Client, "send", _fake_send, raising=True)

    with patch("mvp_site.llm_providers.gemini_provider.get_client", return_value=mock_client):
        with pytest.raises(httpx.ReadTimeout):
            gemini_provider.generate_json_mode_content(
                prompt_contents=["hello"],
                model_name="gemini-3-flash-preview",
                system_instruction_text=None,
                temperature=0.7,
                safety_settings=[],
                json_mode_max_output_tokens=1024,
            )

    content = capture_path.read_text(encoding="utf-8")
    assert '"type": "transport_error"' in content
    assert "ReadTimeout" in content


def test_transport_capture_streaming_keeps_patch_during_iteration(tmp_path, monkeypatch):
    """Streaming calls should capture Gemini HTTP request/response entries."""
    capture_path = tmp_path / "gemini_http_request_responses.jsonl"
    monkeypatch.setenv(
        "GEMINI_HTTP_REQUEST_RESPONSE_CAPTURE_PATH",
        str(capture_path),
    )

    mock_client = MagicMock()

    def _fake_generate_content_stream(**_kwargs):
        def _chunk_stream():
            with httpx.Client() as local_client:
                req = local_client.build_request(
                    "POST",
                    "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:streamGenerateContent?alt=sse",
                    content='{"contents":"hello"}',
                    headers={"Authorization": "Bearer test-secret"},
                )
                local_client.send(req, stream=True)

            chunk = SimpleNamespace(
                candidates=[
                    SimpleNamespace(
                        content=SimpleNamespace(parts=[SimpleNamespace(text="chunk-text")])
                    )
                ]
            )
            yield chunk

        return _chunk_stream()

    mock_client.models.generate_content_stream.side_effect = _fake_generate_content_stream

    def _fake_send(self, request, *args, **kwargs):  # noqa: ARG001
        return httpx.Response(
            200,
            request=request,
            headers={"content-type": "text/event-stream"},
            content=b"",
        )

    monkeypatch.setattr(httpx.Client, "send", _fake_send, raising=True)

    with patch("mvp_site.llm_providers.gemini_provider.get_client", return_value=mock_client):
        chunks = list(
            gemini_provider.generate_content_stream_sync(
                prompt_contents=["hello"],
                model_name="gemini-3-flash-preview",
                system_instruction_text=None,
                temperature=0.7,
                safety_settings=[],
                json_mode=False,
                json_mode_max_output_tokens=1024,
            )
        )

    assert chunks == ["chunk-text"]
    content = capture_path.read_text(encoding="utf-8")
    assert '"type": "http_request"' in content
    assert '"type": "http_response"' in content
    assert '"stream": true' in content
    assert "streamGenerateContent" in content


class TestGeminiSafetySettings(unittest.TestCase):
    def setUp(self):
        self._original_mock_mode = os.environ.get("MOCK_SERVICES_MODE")
        self._original_testing_bypass = os.environ.get("TESTING_AUTH_BYPASS")
        self._original_api_key = os.environ.get("GEMINI_API_KEY")

        gemini_provider.clear_cached_client()

        self.mock_client = MagicMock()
        self.mock_models = MagicMock()
        self.mock_client.models = self.mock_models

        self.client_patcher = patch(
            "mvp_site.llm_providers.gemini_provider.get_client",
            return_value=self.mock_client,
        )
        self.client_patcher.start()

        self.stub_patcher = patch(
            "mvp_site.llm_providers.gemini_provider._use_test_stub_client",
            return_value=False,
        )
        self.stub_patcher.start()

        os.environ["MOCK_SERVICES_MODE"] = "false"
        os.environ["TESTING_AUTH_BYPASS"] = "true"
        os.environ["GEMINI_API_KEY"] = "realish-key"

    def tearDown(self):
        self.stub_patcher.stop()
        self.client_patcher.stop()
        gemini_provider.clear_cached_client()

        if self._original_mock_mode is None:
            os.environ.pop("MOCK_SERVICES_MODE", None)
        else:
            os.environ["MOCK_SERVICES_MODE"] = self._original_mock_mode

        if self._original_testing_bypass is None:
            os.environ.pop("TESTING_AUTH_BYPASS", None)
        else:
            os.environ["TESTING_AUTH_BYPASS"] = self._original_testing_bypass

        if self._original_api_key is None:
            os.environ.pop("GEMINI_API_KEY", None)
        else:
            os.environ["GEMINI_API_KEY"] = self._original_api_key

    def test_safety_settings_passed_correctly(self):
        """Verify safety_settings are passed inside GenerateContentConfig."""
        mock_response = create_llm_response_mock(text="{\"narrative\": \"test\"}")
        mock_response.text = '{"narrative": "test"}'
        self.mock_models.generate_content.return_value = mock_response

        with patch("mvp_site.llm_service._select_provider_and_model") as mock_select:
            mock_select.return_value.provider = constants.LLM_PROVIDER_GEMINI
            mock_select.return_value.model = constants.DEFAULT_GEMINI_MODEL

            llm_service.continue_story(
                user_input="test input",
                mode="action",
                story_context=[],
                current_game_state=GameState(),
                user_id=UserId("test_user"),
            )

        call_args = self.mock_models.generate_content.call_args
        assert call_args is not None, "generate_content was not called"

        kwargs = call_args.kwargs

        if "safety_settings" in kwargs:
            self.fail(
                "safety_settings should NOT be a top-level argument! "
                "SDK only accepts model, contents, config."
            )

        config = kwargs.get("config")
        if not config:
            self.fail("config is missing from generate_content call")

        if not hasattr(config, "safety_settings") or config.safety_settings is None:
            self.fail(
                "safety_settings MISSING from GenerateContentConfig! "
                "They must be passed inside the config object."
            )

    def test_continue_story_excludes_debug_info_from_llm_request_game_state(self):
        """Regression: debug_info must persist in state but not be sent to LLM."""
        game_state = GameState(user_id="test_user")
        game_state.debug_info = {
            "dm_notes": ["keep persisted"],
            "internal_trace": "sensitive",
        }
        captured: dict[str, dict] = {}

        def _capture_request(*args, **kwargs):
            gemini_request = kwargs["gemini_request"]
            captured["payload"] = gemini_request.to_json()
            response = MagicMock()
            response.text = '{"narrative":"ok","state_updates":{}}'
            return response

        with patch("mvp_site.llm_service._select_provider_and_model") as mock_select:
            mock_select.return_value.provider = constants.LLM_PROVIDER_GEMINI
            mock_select.return_value.model = constants.DEFAULT_GEMINI_MODEL
            with patch(
                "mvp_site.llm_service._call_llm_api_with_llm_request",
                side_effect=_capture_request,
            ):
                llm_service.continue_story(
                    user_input="Continue",
                    mode=constants.MODE_CHARACTER,
                    story_context=[],
                    current_game_state=game_state,
                    user_id=UserId("test_user"),
                )

        self.assertIn("payload", captured)
        llm_game_state = captured["payload"].get("game_state", {})
        self.assertNotIn("debug_info", llm_game_state)
        self.assertIn("debug_info", game_state.to_dict())


class TestCampaignCacheManager(unittest.TestCase):
    """Unit tests for CampaignCacheManager."""

    def test_should_rebuild_when_no_cache_exists(self):
        manager = CampaignCacheManager("test-campaign-1")
        self.assertIsNone(manager.cache_name)
        self.assertEqual(manager.cached_entry_count, 0)
        self.assertTrue(manager.should_rebuild(current_entry_count=1))
        self.assertTrue(manager.should_rebuild(current_entry_count=10))

    def test_should_rebuild_at_threshold(self):
        manager = CampaignCacheManager("test-campaign-2")
        manager.cache_name = "cachedContents/existing-cache"
        manager.cached_entry_count = 10

        self.assertFalse(manager.should_rebuild(current_entry_count=11))
        self.assertFalse(manager.should_rebuild(current_entry_count=14))

        self.assertTrue(manager.should_rebuild(current_entry_count=15))
        self.assertTrue(manager.should_rebuild(current_entry_count=20))

    def test_rebuild_threshold_is_5(self):
        self.assertEqual(CampaignCacheManager.REBUILD_THRESHOLD, 5)

    def test_cache_ttl_is_1_hour(self):
        self.assertEqual(CampaignCacheManager.CACHE_TTL, "3600s")

    def test_get_cache_manager_returns_same_instance(self):
        manager1 = get_cache_manager("same-campaign")
        manager2 = get_cache_manager("same-campaign")
        self.assertIs(manager1, manager2)

    def test_get_cache_manager_returns_different_for_different_campaigns(self):
        manager1 = get_cache_manager("campaign-a")
        manager2 = get_cache_manager("campaign-b")
        self.assertIsNot(manager1, manager2)


class TestExplicitCacheIntegration(unittest.TestCase):
    """Integration tests for explicit caching in llm_service."""

    def setUp(self):
        self._original_testing = os.environ.get("TESTING")
        self._original_testing_bypass = os.environ.get("TESTING_AUTH_BYPASS")
        self._original_mock_services_mode = os.environ.get("MOCK_SERVICES_MODE")
        self._original_enable_explicit_cache = os.environ.get("ENABLE_EXPLICIT_CACHE")
        self._original_gemini_key = os.environ.get("GEMINI_API_KEY")
        self._original_cerebras_key = os.environ.get("CEREBRAS_API_KEY")

        os.environ["TESTING"] = "true"
        os.environ["TESTING_AUTH_BYPASS"] = "true"
        os.environ["MOCK_SERVICES_MODE"] = "false"
        if self._original_gemini_key is None:
            os.environ["GEMINI_API_KEY"] = "test-api-key"
        if self._original_cerebras_key is None:
            os.environ["CEREBRAS_API_KEY"] = "test-cerebras-key"

    def tearDown(self):
        if self._original_enable_explicit_cache is None:
            os.environ.pop("ENABLE_EXPLICIT_CACHE", None)
        else:
            os.environ["ENABLE_EXPLICIT_CACHE"] = self._original_enable_explicit_cache

        if self._original_testing is None:
            os.environ.pop("TESTING", None)
        else:
            os.environ["TESTING"] = self._original_testing

        if self._original_testing_bypass is None:
            os.environ.pop("TESTING_AUTH_BYPASS", None)
        else:
            os.environ["TESTING_AUTH_BYPASS"] = self._original_testing_bypass

        if self._original_mock_services_mode is None:
            os.environ.pop("MOCK_SERVICES_MODE", None)
        else:
            os.environ["MOCK_SERVICES_MODE"] = self._original_mock_services_mode

        if self._original_gemini_key is None:
            os.environ.pop("GEMINI_API_KEY", None)
        else:
            os.environ["GEMINI_API_KEY"] = self._original_gemini_key

        if self._original_cerebras_key is None:
            os.environ.pop("CEREBRAS_API_KEY", None)
        else:
            os.environ["CEREBRAS_API_KEY"] = self._original_cerebras_key

    def _create_mock_response_with_cache_miss(self):
        return create_llm_response_mock(
            prompt_tokens=230197, 
            cached_tokens=0, 
            text="{\"narrative\": \"No context.\", \"choices\": {}}"
        )

    def _create_mock_response_with_cache_hit(self):
        return create_llm_response_mock(
            prompt_tokens=230197, 
            cached_tokens=183000, 
            text="{\"narrative\": \"With context.\", \"choices\": {}}"
        )

    def _create_mock_llm_request(self):
        return LLMRequest(
            user_action="test action",
            game_mode=constants.MODE_CHARACTER,
            user_id="test-user",
            game_state={"campaign_id": "test-campaign"},
            story_history=[{"entry": "Story 1"} for _ in range(5)],
        )

    def test_explicit_cache_miss_logs_warning(self):
        """Cache miss (cached_tokens=0) should log warning about missing context."""
        os.environ["ENABLE_EXPLICIT_CACHE"] = "true"

        mock_response = self._create_mock_response_with_cache_miss()
        request = self._create_mock_llm_request()

        with patch("mvp_site.llm_providers.gemini_provider.get_client") as mock_client:
            mock_client.return_value.models.generate_content.return_value = (
                mock_response
            )

            with patch("mvp_site.logging_util.warning") as mock_warning:
                llm_service._call_llm_api_with_explicit_cache(
                    gemini_request=request,
                    campaign_id="test-campaign",
                    model_name=constants.DEFAULT_GEMINI_MODEL,
                    system_instruction_text="Test system instruction",
                    provider_name=constants.LLM_PROVIDER_GEMINI,
                )

        assert mock_warning.called, (
            "Should log warning when cache miss results in missing context."
        )

    def test_explicit_cache_hit_includes_cached_tokens(self):
        """Cache hit should include cached tokens in response usage metadata."""
        os.environ["ENABLE_EXPLICIT_CACHE"] = "true"

        mock_response = self._create_mock_response_with_cache_hit()
        request = self._create_mock_llm_request()

        with patch("mvp_site.llm_providers.gemini_provider.get_client") as mock_client:
            mock_client.return_value.models.generate_content.return_value = (
                mock_response
            )

            response = llm_service._call_llm_api_with_explicit_cache(
                gemini_request=request,
                campaign_id="test-campaign",
                model_name=constants.DEFAULT_GEMINI_MODEL,
                system_instruction_text="Test system instruction",
                provider_name=constants.LLM_PROVIDER_GEMINI,
            )
            usage = response.usage_metadata

        assert usage.cached_content_token_count == 183000
        assert usage.prompt_token_count == 230197

    def test_explicit_cache_disabled_fallbacks_to_regular_call(self):
        """Cache creation failure should fall back to one regular LLM call."""
        os.environ["ENABLE_EXPLICIT_CACHE"] = "false"

        request = self._create_mock_llm_request()
        get_cache_manager("test-campaign").reset_cache()

        with patch("mvp_site.llm_service._call_llm_api") as mock_regular, patch(
            "mvp_site.llm_providers.gemini_provider.get_client",
            return_value=object(),
        ):
            mock_regular.return_value = create_llm_response_mock()
            llm_service._call_llm_api_with_explicit_cache(
                gemini_request=request,
                campaign_id="test-campaign",
                model_name=constants.DEFAULT_GEMINI_MODEL,
                system_instruction_text="Test system instruction",
                provider_name=constants.LLM_PROVIDER_GEMINI,
            )

        mock_regular.assert_called_once()

    def test_explicit_cache_handles_missing_cache_name(self):
        """If no cache_name, should skip explicit cache logic."""
        os.environ["ENABLE_EXPLICIT_CACHE"] = "true"

        request = self._create_mock_llm_request()

        # Mock cache manager to return False for should_rebuild so it proceeds
        # to reuse existing cache (which defaults to None)
        with patch("mvp_site.llm_service._call_llm_api") as mock_regular, \
             patch("mvp_site.llm_service.get_cache_manager") as mock_get_mgr:
            
            mock_mgr = MagicMock()
            mock_mgr.should_rebuild.return_value = False
            mock_mgr.get_cache_name.return_value = None # Simulate missing cache name
            mock_mgr.cached_entry_count = 0
            mock_get_mgr.return_value = mock_mgr

            mock_regular.return_value = create_llm_response_mock()
            llm_service._call_llm_api_with_explicit_cache(
                gemini_request=request,
                campaign_id="test-campaign",
                model_name=constants.DEFAULT_GEMINI_MODEL,
                system_instruction_text="Test system instruction",
                provider_name=constants.LLM_PROVIDER_GEMINI,
            )

        mock_regular.assert_called_once()

    def test_cache_manager_tracks_request_counts(self):
        """Verify cache manager tracks request counts and rebuilds when needed."""
        manager = CampaignCacheManager("test-tracking")
        manager.cache_name = "cachedContents/test-cache"
        manager.cached_entry_count = 10

        for i in range(1, 6):
            should_rebuild = manager.should_rebuild(current_entry_count=10 + i)
            if i < 5:
                self.assertFalse(should_rebuild)
            else:
                self.assertTrue(should_rebuild)

    def test_cache_rebuild_clears_old_cache_name(self):
        """Test cache rebuild resets cache name when new cache created."""
        manager = CampaignCacheManager("test-reset")
        manager.cache_name = "cachedContents/old-cache"

        manager.reset_cache()

        self.assertIsNone(manager.cache_name)
        self.assertEqual(manager.cached_entry_count, 0)

    def test_cache_miss_metrics_logged(self):
        """Verify cache miss metrics are logged for observability."""
        os.environ["ENABLE_EXPLICIT_CACHE"] = "true"

        mock_response = self._create_mock_response_with_cache_miss()
        request = self._create_mock_llm_request()

        with patch("mvp_site.llm_providers.gemini_provider.get_client") as mock_client:
            mock_client.return_value.models.generate_content.return_value = (
                mock_response
            )

            with contextlib.ExitStack() as stack:
                log_capture = stack.enter_context(self.assertLogs(level="WARNING"))
                llm_service._call_llm_api_with_explicit_cache(
                    gemini_request=request,
                    campaign_id="test-campaign",
                    model_name=constants.DEFAULT_GEMINI_MODEL,
                    system_instruction_text="Test system instruction",
                    provider_name=constants.LLM_PROVIDER_GEMINI,
                )

        assert any("EXPLICIT_CACHE_NOT_HIT" in message for message in log_capture.output), (
            "Should log cache miss warning"
        )

    def test_cache_hit_metrics_logged(self):
        """Verify cache hit metrics are logged."""
        os.environ["ENABLE_EXPLICIT_CACHE"] = "true"

        mock_response = self._create_mock_response_with_cache_hit()
        request = self._create_mock_llm_request()

        with patch("mvp_site.llm_providers.gemini_provider.get_client") as mock_client:
            mock_client.return_value.models.generate_content.return_value = (
                mock_response
            )

            with contextlib.ExitStack() as stack:
                log_capture = stack.enter_context(self.assertLogs(level="INFO"))
                llm_service._call_llm_api_with_explicit_cache(
                    gemini_request=request,
                    campaign_id="test-campaign",
                    model_name=constants.DEFAULT_GEMINI_MODEL,
                    system_instruction_text="Test system instruction",
                    provider_name=constants.LLM_PROVIDER_GEMINI,
                )

        assert any(
            "cached_tokens=183000" in message for message in log_capture.output
        ), "Should log cache hit with cached_tokens"

    def test_cache_rebuild_warning_on_missing_system_instructions(self):
        """RED test: Ensure warning when system_instruction is missing on cache miss."""
        os.environ["ENABLE_EXPLICIT_CACHE"] = "true"

        mock_response = self._create_mock_response_with_cache_miss()
        request = self._create_mock_llm_request()

        with patch("mvp_site.llm_providers.gemini_provider.get_client") as mock_client:
            mock_client.return_value.models.generate_content.return_value = (
                mock_response
            )

            with patch.object(
                llm_service, "_call_llm_api", wraps=llm_service._call_llm_api
            ) as mock_regular:
                llm_service._call_llm_api_with_explicit_cache(
                    gemini_request=request,
                    campaign_id="test-campaign",
                    model_name=constants.DEFAULT_GEMINI_MODEL,
                    system_instruction_text="Test system instruction",
                    provider_name=constants.LLM_PROVIDER_GEMINI,
                )

                assert mock_regular.called, (
                    "Should fall back to regular call on cache miss"
                )

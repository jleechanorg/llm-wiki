import json
from unittest.mock import MagicMock, patch

import pytest

from mvp_site import constants, llm_service
from mvp_site.llm_providers.provider_utils import ContextTooLargeError


def test_mock_mode_response_contains_valid_planning_choice_schema():
    with patch.dict("os.environ", {"MOCK_SERVICES_MODE": "true"}, clear=False):
        response = llm_service._call_llm_api(["prompt"], "model")

    payload = json.loads(response.text)
    choices = payload.get("planning_block", {}).get("choices", {})
    assert isinstance(choices, dict)
    assert choices

    for choice_data in choices.values():
        assert isinstance(choice_data, dict)
        assert choice_data.get("text")
        assert choice_data.get("description")


def test_model_call_surfaces_context_too_large_error():
    context_error = ContextTooLargeError(
        "Context exceeded",
        prompt_tokens=400_000,
        completion_tokens=0,
        finish_reason="context_exceeded",
    )

    with (
        patch(
            "mvp_site.llm_service._calculate_prompt_and_system_tokens",
            return_value=(1, 1),
        ),
        patch("mvp_site.llm_service._log_token_count"),
        patch(
            "mvp_site.llm_service._get_safe_output_token_limit",
            side_effect=context_error,
        ),
        patch.dict("os.environ", {"MOCK_SERVICES_MODE": "false"}, clear=False),
        pytest.raises(llm_service.LLMRequestError) as exc_info,
    ):
        llm_service._call_llm_api(["prompt"], "model")

    assert exc_info.value.status_code == 422
    assert "context" in str(exc_info.value).lower()


def test_model_call_surfaces_provider_overload_without_retry():
    overload_error = Exception("503 UNAVAILABLE: overloaded")

    with (
        patch(
            "mvp_site.llm_service._calculate_prompt_and_system_tokens",
            return_value=(10, 0),
        ),
        patch("mvp_site.llm_service._log_token_count"),
        patch("mvp_site.llm_service._get_safe_output_token_limit", return_value=100),
        patch(
            "mvp_site.llm_service.gemini_provider.generate_content_with_native_tools",
            side_effect=overload_error,
        ) as mock_generate,
        patch.dict("os.environ", {"MOCK_SERVICES_MODE": "false"}, clear=False),
        pytest.raises(llm_service.LLMRequestError) as exc_info,
    ):
        llm_service._call_llm_api(
            ["prompt"], "model", provider_name=constants.LLM_PROVIDER_GEMINI
        )

    assert exc_info.value.status_code == 503
    mock_generate.assert_called_once()


def test_model_call_surfaces_rate_limit_without_retry():
    rate_limit_error = Exception("429 RESOURCE_EXHAUSTED: rate limited")

    with (
        patch(
            "mvp_site.llm_service._calculate_prompt_and_system_tokens",
            return_value=(10, 0),
        ),
        patch("mvp_site.llm_service._log_token_count"),
        patch("mvp_site.llm_service._get_safe_output_token_limit", return_value=100),
        patch(
            "mvp_site.llm_service.gemini_provider.generate_content_with_native_tools",
            side_effect=rate_limit_error,
        ) as mock_generate,
        patch.dict("os.environ", {"MOCK_SERVICES_MODE": "false"}, clear=False),
        pytest.raises(llm_service.LLMRequestError) as exc_info,
    ):
        llm_service._call_llm_api(
            ["prompt"], "model", provider_name=constants.LLM_PROVIDER_GEMINI
        )

    assert exc_info.value.status_code == 429
    assert "rate limit" in str(exc_info.value).lower()
    mock_generate.assert_called_once()


class TestErrorDiagnostics:
    """Tests for enhanced error diagnostics in _call_llm_api."""

    def _disable_mock_mode(self):
        """Return a patch that disables MOCK_SERVICES_MODE."""
        return patch.dict("os.environ", {"MOCK_SERVICES_MODE": "false"}, clear=False)

    def test_error_code_type_validation_with_valid_int(self):
        """Test that e.code is properly converted to int when valid."""
        error = Exception("API error")
        error.code = 400  # Valid integer code

        with (
            self._disable_mock_mode(),
            patch(
                "mvp_site.llm_service._calculate_prompt_and_system_tokens",
                return_value=(10, 0),
            ),
            patch("mvp_site.llm_service._log_token_count"),
            patch(
                "mvp_site.llm_service._get_safe_output_token_limit", return_value=100
            ),
            patch(
                "mvp_site.llm_service.gemini_provider.generate_content_with_native_tools",
                side_effect=error,
            ),
            patch("mvp_site.llm_service.logging_util") as mock_logging,
            pytest.raises(Exception),
        ):
            llm_service._call_llm_api(
                ["prompt"], "model", provider_name=constants.LLM_PROVIDER_GEMINI
            )

        # Verify the error diagnostics logging includes code=400
        error_calls = [
            call
            for call in mock_logging.error.call_args_list
            if "diagnostics" in str(call)
        ]
        assert len(error_calls) > 0
        assert "code=400" in str(error_calls[0])

    def test_error_code_type_validation_with_string_int(self):
        """Test that string integer e.code is converted to int."""
        error = Exception("API error")
        error.code = "500"  # String that can be converted to int

        with (
            self._disable_mock_mode(),
            patch(
                "mvp_site.llm_service._calculate_prompt_and_system_tokens",
                return_value=(10, 0),
            ),
            patch("mvp_site.llm_service._log_token_count"),
            patch(
                "mvp_site.llm_service._get_safe_output_token_limit", return_value=100
            ),
            patch(
                "mvp_site.llm_service.gemini_provider.generate_content_with_native_tools",
                side_effect=error,
            ),
            patch("mvp_site.llm_service.logging_util") as mock_logging,
            pytest.raises(Exception),
        ):
            llm_service._call_llm_api(
                ["prompt"], "model", provider_name=constants.LLM_PROVIDER_GEMINI
            )

        # Verify the error diagnostics logging includes code=500
        error_calls = [
            call
            for call in mock_logging.error.call_args_list
            if "diagnostics" in str(call)
        ]
        assert len(error_calls) > 0
        assert "code=500" in str(error_calls[0])

    def test_error_code_type_validation_with_invalid_string(self):
        """Test that invalid string e.code results in status_code=None."""
        error = Exception("API error")
        error.code = "INVALID_CODE"  # Cannot be converted to int

        with (
            self._disable_mock_mode(),
            patch(
                "mvp_site.llm_service._calculate_prompt_and_system_tokens",
                return_value=(10, 0),
            ),
            patch("mvp_site.llm_service._log_token_count"),
            patch(
                "mvp_site.llm_service._get_safe_output_token_limit", return_value=100
            ),
            patch(
                "mvp_site.llm_service.gemini_provider.generate_content_with_native_tools",
                side_effect=error,
            ),
            patch("mvp_site.llm_service.logging_util") as mock_logging,
            pytest.raises(Exception),
        ):
            llm_service._call_llm_api(
                ["prompt"], "model", provider_name=constants.LLM_PROVIDER_GEMINI
            )

        # Verify the error diagnostics logging includes code=None
        error_calls = [
            call
            for call in mock_logging.error.call_args_list
            if "diagnostics" in str(call)
        ]
        assert len(error_calls) > 0
        assert "code=None" in str(error_calls[0])

    def test_error_code_type_validation_with_none(self):
        """Test that None e.code results in status_code=None."""
        error = Exception("API error")
        error.code = None

        with (
            self._disable_mock_mode(),
            patch(
                "mvp_site.llm_service._calculate_prompt_and_system_tokens",
                return_value=(10, 0),
            ),
            patch("mvp_site.llm_service._log_token_count"),
            patch(
                "mvp_site.llm_service._get_safe_output_token_limit", return_value=100
            ),
            patch(
                "mvp_site.llm_service.gemini_provider.generate_content_with_native_tools",
                side_effect=error,
            ),
            patch("mvp_site.llm_service.logging_util") as mock_logging,
            pytest.raises(Exception),
        ):
            llm_service._call_llm_api(
                ["prompt"], "model", provider_name=constants.LLM_PROVIDER_GEMINI
            )

        # Verify the error diagnostics logging includes code=None
        error_calls = [
            call
            for call in mock_logging.error.call_args_list
            if "diagnostics" in str(call)
        ]
        assert len(error_calls) > 0
        assert "code=None" in str(error_calls[0])

    def test_null_headers_does_not_raise_typeerror(self):
        """Test that null response headers doesn't cause TypeError."""
        error = Exception("API error")
        error.response = MagicMock()
        error.response.headers = None  # Headers is None

        with (
            self._disable_mock_mode(),
            patch(
                "mvp_site.llm_service._calculate_prompt_and_system_tokens",
                return_value=(10, 0),
            ),
            patch("mvp_site.llm_service._log_token_count"),
            patch(
                "mvp_site.llm_service._get_safe_output_token_limit", return_value=100
            ),
            patch(
                "mvp_site.llm_service.gemini_provider.generate_content_with_native_tools",
                side_effect=error,
            ),
            patch("mvp_site.llm_service.logging_util"),
            pytest.raises(Exception),
        ):
            # Should not raise TypeError when iterating over None headers
            llm_service._call_llm_api(
                ["prompt"], "model", provider_name=constants.LLM_PROVIDER_GEMINI
            )

    def test_response_headers_are_extracted_for_logging(self):
        """Test that response headers are extracted and logged."""
        error = Exception("API error")
        error.response = MagicMock()
        error.response.headers = {
            "x-request-id": "req-12345",
            "x-goog-request-id": "goog-67890",
            "content-type": "application/json",  # Should not be logged
        }

        with (
            self._disable_mock_mode(),
            patch(
                "mvp_site.llm_service._calculate_prompt_and_system_tokens",
                return_value=(10, 0),
            ),
            patch("mvp_site.llm_service._log_token_count"),
            patch(
                "mvp_site.llm_service._get_safe_output_token_limit", return_value=100
            ),
            patch(
                "mvp_site.llm_service.gemini_provider.generate_content_with_native_tools",
                side_effect=error,
            ),
            patch("mvp_site.llm_service.logging_util") as mock_logging,
            pytest.raises(Exception),
        ):
            llm_service._call_llm_api(
                ["prompt"], "model", provider_name=constants.LLM_PROVIDER_GEMINI
            )

        # Verify headers are logged
        error_calls = [
            call
            for call in mock_logging.error.call_args_list
            if "diagnostics" in str(call)
        ]
        assert len(error_calls) > 0
        log_message = str(error_calls[0])
        assert "x-request-id=req-12345" in log_message
        assert "x-goog-request-id=goog-67890" in log_message
        # content-type should NOT be logged (not in headers_to_log list)
        assert "content-type" not in log_message

    def test_error_details_attribute_extraction(self):
        """Test that e.details, e.status, e.message are extracted."""
        error = Exception("API error")
        error.details = "FAILED_PRECONDITION"
        error.status = "400"
        error.message = "Request failed precondition check"

        with (
            self._disable_mock_mode(),
            patch(
                "mvp_site.llm_service._calculate_prompt_and_system_tokens",
                return_value=(10, 0),
            ),
            patch("mvp_site.llm_service._log_token_count"),
            patch(
                "mvp_site.llm_service._get_safe_output_token_limit", return_value=100
            ),
            patch(
                "mvp_site.llm_service.gemini_provider.generate_content_with_native_tools",
                side_effect=error,
            ),
            patch("mvp_site.llm_service.logging_util") as mock_logging,
            pytest.raises(Exception),
        ):
            llm_service._call_llm_api(
                ["prompt"], "model", provider_name=constants.LLM_PROVIDER_GEMINI
            )

        # Verify error attributes are logged
        error_calls = [
            call
            for call in mock_logging.error.call_args_list
            if "diagnostics" in str(call)
        ]
        assert len(error_calls) > 0
        log_message = str(error_calls[0])
        assert "details=FAILED_PRECONDITION" in log_message
        assert "status=400" in log_message
        assert "message=Request failed precondition check" in log_message


class TestStreamCacheFallback:
    """Unit tests for _gemini_stream_with_cache_fallback stale-cache handling."""

    _VALID_DONE_JSON = (
        '{"narrative": "You step forward.", "planning_block": {"choices": {'
        '"a": {"text": "Go left", "description": "Turn left"}}}}'
    )

    def _make_mock_prep(self):
        mock_prep = MagicMock()
        mock_prep.agent = MagicMock()
        mock_prep.agent.__class__.__name__ = "TestAgent"
        mock_prep.agent.MODE = "character"
        mock_prep.agent.requires_action_resolution = False
        mock_prep.model_to_use = "gemini-3-flash-preview"
        mock_prep.provider_selection.provider = "gemini"
        mock_prep.system_instruction_final = "system"
        mock_prep.temperature_override = None
        mock_prep.gemini_request = MagicMock()
        mock_prep.gemini_request.to_json = lambda: {
            "game_state": {"campaign_id": "test-cam-123"},
            "story_history": [],
        }
        mock_prep.gemini_request.game_state = {"campaign_id": "test-cam-123"}
        mock_prep.gemini_request.story_history = [
            {"role": "user", "content": "I look around"}
        ]
        mock_prep.gemini_request.to_explicit_cache_parts = MagicMock(
            return_value=(
                {"story_history": [], "cached_data": True},
                {"story_history": [], "user_action": "look"},
            )
        )
        return mock_prep

    def _run_stream(self):
        from mvp_site.game_state import GameState
        from mvp_site.llm_service import continue_story_streaming

        return list(
            continue_story_streaming(
                user_input="I look around",
                mode="character",
                story_context=[],
                current_game_state=GameState.from_dict({}),
                selected_prompts=[],
                use_default_world=False,
                user_id="test-user",
                campaign_id="test-cam-123",
            )
        )

    @staticmethod
    def _iter_raises(exc: Exception):
        """Generator that raises exc on first iteration — mimics lazy Gemini streaming error."""
        raise exc
        yield  # pragma: no cover — makes this a generator function

    def test_failed_precondition_triggers_stale_fallback(self):
        """FAILED_PRECONDITION on streaming should fall back to uncached call."""
        mock_prep = self._make_mock_prep()
        mock_cache_mgr = MagicMock()
        mock_cache_mgr.get_cache_name.return_value = "cachedContents/fake-cache-abc"
        mock_cache_mgr.cached_entry_count = 5
        mock_cache_mgr.should_rebuild.return_value = False
        mock_cache_mgr.has_pending_cache.return_value = False

        with (
            patch(
                "mvp_site.llm_service._prepare_story_continuation",
                return_value=mock_prep,
            ),
            patch(
                "mvp_site.llm_service.get_cache_manager", return_value=mock_cache_mgr
            ),
            patch("mvp_site.llm_service.gemini_provider") as mock_gemini,
            patch(
                "mvp_site.llm_service._calculate_prompt_and_system_tokens",
                return_value=(100, 50),
            ),
            patch(
                "mvp_site.llm_service._get_safe_output_token_limit", return_value=4096
            ),
            patch("mvp_site.llm_service.logging_util") as mock_log,
            patch.dict(
                "os.environ",
                {"TESTING_AUTH_BYPASS": "true", "MOCK_SERVICES_MODE": "false"},
            ),
            patch("mvp_site.llm_service.constants.EXPLICIT_CACHE_ENABLED", True),
        ):

            def _stream_side_effect(**kwargs):
                # Real Gemini raises lazily during iteration, not at call time
                if kwargs.get("cache_name"):
                    return self._iter_raises(
                        Exception(
                            "400 FAILED_PRECONDITION. {'error': {'code': 400, "
                            "'message': 'Precondition check failed.', 'status': 'FAILED_PRECONDITION'}}"
                        )
                    )
                return iter([self._VALID_DONE_JSON])

            mock_gemini.generate_content_stream_sync.side_effect = _stream_side_effect
            mock_gemini.get_client.return_value = MagicMock()

            events = self._run_stream()

        # The fallback should have been logged
        warning_calls = [str(c) for c in mock_log.warning.call_args_list]
        stale_logged = any("STREAM_CACHE_STALE" in w for w in warning_calls)
        assert stale_logged, (
            f"Expected STREAM_CACHE_STALE warning. Got: {warning_calls}"
        )

        # And the stream should have yielded a done event (not an error)
        done_events = [e for e in events if getattr(e, "type", None) == "done"]
        assert done_events, (
            f"Expected done event after fallback. Events: {[getattr(e, 'type', None) for e in events]}"
        )

    def test_precondition_check_failed_message_triggers_stale_fallback(self):
        """'Precondition check failed' message variant also triggers fallback."""
        mock_prep = self._make_mock_prep()
        mock_cache_mgr = MagicMock()
        mock_cache_mgr.get_cache_name.return_value = "cachedContents/another-cache"
        mock_cache_mgr.cached_entry_count = 3
        mock_cache_mgr.should_rebuild.return_value = False
        mock_cache_mgr.has_pending_cache.return_value = False

        with (
            patch(
                "mvp_site.llm_service._prepare_story_continuation",
                return_value=mock_prep,
            ),
            patch(
                "mvp_site.llm_service.get_cache_manager", return_value=mock_cache_mgr
            ),
            patch("mvp_site.llm_service.gemini_provider") as mock_gemini,
            patch(
                "mvp_site.llm_service._calculate_prompt_and_system_tokens",
                return_value=(100, 50),
            ),
            patch(
                "mvp_site.llm_service._get_safe_output_token_limit", return_value=4096
            ),
            patch("mvp_site.llm_service.logging_util") as mock_log,
            patch.dict(
                "os.environ",
                {"TESTING_AUTH_BYPASS": "true", "MOCK_SERVICES_MODE": "false"},
            ),
            patch("mvp_site.llm_service.constants.EXPLICIT_CACHE_ENABLED", True),
        ):

            def _stream_side_effect(**kwargs):
                if kwargs.get("cache_name"):
                    return self._iter_raises(Exception("Precondition check failed."))
                return iter([self._VALID_DONE_JSON])

            mock_gemini.generate_content_stream_sync.side_effect = _stream_side_effect
            mock_gemini.get_client.return_value = MagicMock()

            self._run_stream()

        warning_calls = [str(c) for c in mock_log.warning.call_args_list]
        assert any("STREAM_CACHE_STALE" in w for w in warning_calls), (
            f"Expected STREAM_CACHE_STALE warning. Got: {warning_calls}"
        )

    def test_failed_precondition_without_cache_name_reraises(self):
        """FAILED_PRECONDITION when no cache is set should propagate (not silently swallowed)."""
        mock_prep = self._make_mock_prep()
        # No cache → should_rebuild=True but we mock the whole cache path off
        mock_cache_mgr = MagicMock()
        mock_cache_mgr.get_cache_name.return_value = None
        mock_cache_mgr.cached_entry_count = 0
        mock_cache_mgr.should_rebuild.return_value = False
        mock_cache_mgr.has_pending_cache.return_value = False

        with (
            patch(
                "mvp_site.llm_service._prepare_story_continuation",
                return_value=mock_prep,
            ),
            patch(
                "mvp_site.llm_service.get_cache_manager", return_value=mock_cache_mgr
            ),
            patch("mvp_site.llm_service.gemini_provider") as mock_gemini,
            patch(
                "mvp_site.llm_service._calculate_prompt_and_system_tokens",
                return_value=(100, 50),
            ),
            patch(
                "mvp_site.llm_service._get_safe_output_token_limit", return_value=4096
            ),
            patch.dict(
                "os.environ",
                {"TESTING_AUTH_BYPASS": "true", "MOCK_SERVICES_MODE": "false"},
            ),
            patch("mvp_site.llm_service.constants.EXPLICIT_CACHE_ENABLED", True),
        ):
            mock_gemini.generate_content_stream_sync.return_value = self._iter_raises(
                Exception("400 FAILED_PRECONDITION. Precondition check failed.")
            )
            mock_gemini.get_client.return_value = MagicMock()

            from mvp_site.game_state import GameState
            from mvp_site.llm_service import continue_story_streaming

            events = list(
                continue_story_streaming(
                    user_input="I look around",
                    mode="character",
                    story_context=[],
                    current_game_state=GameState.from_dict({}),
                    selected_prompts=[],
                    use_default_world=False,
                    user_id="test-user",
                    campaign_id="test-cam-123",
                )
            )

        # Without a cache name, the error should surface as an error event
        error_events = [e for e in events if getattr(e, "type", None) == "error"]
        assert error_events, (
            "Expected error event when FAILED_PRECONDITION without cache"
        )

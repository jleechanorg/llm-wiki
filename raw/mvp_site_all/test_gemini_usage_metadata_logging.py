"""
Test coverage for Gemini usage_metadata logging in _call_llm_api.

Ensures that usage metadata is correctly logged for implicit caching verification,
including defensive null handling for None values.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from mvp_site import constants, llm_service


@pytest.fixture(autouse=True)
def clear_testing_env(monkeypatch):
    """Clear testing environment variables."""
    monkeypatch.delenv("TESTING", raising=False)
    monkeypatch.delenv("MOCK_SERVICES_MODE", raising=False)


@pytest.fixture
def mock_gemini_response_with_cache():
    """Create a mock Gemini response with cache hit metadata."""
    response = MagicMock()
    response.usage_metadata = SimpleNamespace(
        prompt_token_count=230197,
        cached_content_token_count=172648,  # 75% cache hit
        candidates_token_count=1234,
    )
    response.text = '{"narrative": "Test", "choices": {"A": "Option A"}}'
    return response


@pytest.fixture
def mock_gemini_response_no_cache():
    """Create a mock Gemini response with no cache hits."""
    response = MagicMock()
    response.usage_metadata = SimpleNamespace(
        prompt_token_count=230197,
        cached_content_token_count=0,  # No cache hits
        candidates_token_count=1234,
    )
    response.text = '{"narrative": "Test", "choices": {"A": "Option A"}}'
    return response


@pytest.fixture
def mock_gemini_response_with_none_values():
    """Create a mock Gemini response with None values (edge case)."""
    response = MagicMock()
    response.usage_metadata = SimpleNamespace(
        prompt_token_count=None,
        cached_content_token_count=None,
        candidates_token_count=None,
    )
    response.text = '{"narrative": "Test", "choices": {"A": "Option A"}}'
    return response


@pytest.fixture
def mock_gemini_response_missing_cached_tokens():
    """Create a mock Gemini response missing cached_content_token_count."""
    response = MagicMock()
    # Simulate attribute not existing (AttributeError on access)
    response.usage_metadata = SimpleNamespace(
        prompt_token_count=230197,
        candidates_token_count=1234,
    )
    # Delete the cached_content_token_count attribute if it exists
    if hasattr(response.usage_metadata, "cached_content_token_count"):
        delattr(response.usage_metadata, "cached_content_token_count")
    response.text = '{"narrative": "Test", "choices": {"A": "Option A"}}'
    return response


def test_logs_cache_hit_usage_metadata(mock_gemini_response_with_cache, caplog):
    """Test that usage metadata with cache hits is logged correctly."""
    caplog.set_level("INFO")

    with patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_native_tools"
    ) as mock_generate:
        with patch(
            "mvp_site.llm_service.dice_strategy.get_dice_roll_strategy"
        ) as mock_strategy:
            mock_strategy.return_value = "native_two_phase"  # Use native tools path
            mock_generate.return_value = mock_gemini_response_with_cache

            # Call the function
            response = llm_service._call_llm_api(
                prompt_contents=["test prompt"],
                model_name="gemini-2-5-flash-preview",
                provider_name=constants.LLM_PROVIDER_GEMINI,
            )

            # Verify response returned
            assert response == mock_gemini_response_with_cache

            # Verify usage metadata was logged
            log_messages = [record.message for record in caplog.records]
            usage_logs = [msg for msg in log_messages if "GEMINI_USAGE" in msg]
            assert len(usage_logs) == 1

            usage_log = usage_logs[0]
            assert "prompt_tokens=230197" in usage_log
            assert "cached_tokens=172648" in usage_log
            assert "response_tokens=1234" in usage_log
            assert "cache_hit_rate=75.0%" in usage_log


def test_logs_no_cache_usage_metadata(mock_gemini_response_no_cache, caplog):
    """Test that usage metadata with zero cache hits is logged correctly."""
    caplog.set_level("INFO")

    with patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    ) as mock_generate:
        with patch(
            "mvp_site.llm_service.dice_strategy.get_dice_roll_strategy"
        ) as mock_strategy:
            mock_strategy.return_value = "code_execution"  # Use code execution path
            mock_generate.return_value = mock_gemini_response_no_cache

            response = llm_service._call_llm_api(
                prompt_contents=["test prompt"],
                model_name="gemini-3-flash-preview",
                provider_name=constants.LLM_PROVIDER_GEMINI,
            )

            assert response == mock_gemini_response_no_cache

            log_messages = [record.message for record in caplog.records]
            usage_logs = [msg for msg in log_messages if "GEMINI_USAGE" in msg]
            assert len(usage_logs) == 1

            usage_log = usage_logs[0]
            assert "prompt_tokens=230197" in usage_log
            assert "cached_tokens=0" in usage_log
            assert "cache_hit_rate=0.0%" in usage_log


def test_handles_none_values_safely(mock_gemini_response_with_none_values, caplog):
    """Test that None values in usage_metadata are coalesced to 0."""
    caplog.set_level("INFO")

    with patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_native_tools"
    ) as mock_generate:
        with patch(
            "mvp_site.llm_service.dice_strategy.get_dice_roll_strategy"
        ) as mock_strategy:
            mock_strategy.return_value = "native_two_phase"
            mock_generate.return_value = mock_gemini_response_with_none_values

            # Should not raise TypeError
            response = llm_service._call_llm_api(
                prompt_contents=["test prompt"],
                model_name="gemini-2-5-flash-preview",
                provider_name=constants.LLM_PROVIDER_GEMINI,
            )

            assert response == mock_gemini_response_with_none_values

            log_messages = [record.message for record in caplog.records]
            usage_logs = [msg for msg in log_messages if "GEMINI_USAGE" in msg]
            assert len(usage_logs) == 1

            usage_log = usage_logs[0]
            # All None values should be coalesced to 0
            assert "prompt_tokens=0" in usage_log
            assert "cached_tokens=0" in usage_log
            assert "response_tokens=0" in usage_log
            assert "cache_hit_rate=0.0%" in usage_log


def test_handles_missing_cached_tokens_attribute(
    mock_gemini_response_missing_cached_tokens, caplog
):
    """Test that missing cached_content_token_count attribute defaults to 0."""
    caplog.set_level("INFO")

    with patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_native_tools"
    ) as mock_generate:
        with patch(
            "mvp_site.llm_service.dice_strategy.get_dice_roll_strategy"
        ) as mock_strategy:
            mock_strategy.return_value = "native_two_phase"
            mock_generate.return_value = mock_gemini_response_missing_cached_tokens

            response = llm_service._call_llm_api(
                prompt_contents=["test prompt"],
                model_name="gemini-2-5-flash-preview",
                provider_name=constants.LLM_PROVIDER_GEMINI,
            )

            assert response == mock_gemini_response_missing_cached_tokens

            log_messages = [record.message for record in caplog.records]
            usage_logs = [msg for msg in log_messages if "GEMINI_USAGE" in msg]
            assert len(usage_logs) == 1

            usage_log = usage_logs[0]
            assert "prompt_tokens=230197" in usage_log
            assert "cached_tokens=0" in usage_log  # Missing attribute defaults to 0
            assert "cache_hit_rate=0.0%" in usage_log


def test_no_logging_for_non_gemini_providers(caplog):
    """Test that usage metadata is NOT logged for non-Gemini providers."""
    caplog.set_level("INFO")

    mock_response = MagicMock()
    mock_response.text = '{"narrative": "Test"}'

    with patch(
        "mvp_site.llm_providers.openrouter_provider.generate_content_with_tool_requests"
    ) as mock_generate:
        mock_generate.return_value = mock_response

        response = llm_service._call_llm_api(
            prompt_contents=["test prompt"],
            model_name="meta-llama/llama-3.1-70b-instruct",
            provider_name=constants.LLM_PROVIDER_OPENROUTER,
        )

        assert response == mock_response

        log_messages = [record.message for record in caplog.records]
        usage_logs = [msg for msg in log_messages if "GEMINI_USAGE" in msg]
        # Should be NO usage metadata logs for non-Gemini providers
        assert len(usage_logs) == 0


def test_no_logging_when_no_usage_metadata(caplog):
    """Test that no logging occurs when response has no usage_metadata attribute."""
    caplog.set_level("INFO")

    mock_response = MagicMock(spec=["text"])  # Only has 'text', no 'usage_metadata'
    mock_response.text = '{"narrative": "Test"}'

    with patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_native_tools"
    ) as mock_generate:
        with patch(
            "mvp_site.llm_service.dice_strategy.get_dice_roll_strategy"
        ) as mock_strategy:
            mock_strategy.return_value = "native_two_phase"
            mock_generate.return_value = mock_response

            response = llm_service._call_llm_api(
                prompt_contents=["test prompt"],
                model_name="gemini-2-5-flash-preview",
                provider_name=constants.LLM_PROVIDER_GEMINI,
            )

            assert response == mock_response

            log_messages = [record.message for record in caplog.records]
            usage_logs = [msg for msg in log_messages if "GEMINI_USAGE" in msg]
            # Should be NO logs when usage_metadata doesn't exist
            assert len(usage_logs) == 0


# NOTE: Comprehensive test for explicit cache miss detection is in:
# mvp_site/tests/test_end2end/test_explicit_cache_miss_end2end.py
#
# That test covers the critical bug (2026-01-25) where cache_name is set but
# cached_tokens=0, causing system_instruction to be missing from LLM requests.

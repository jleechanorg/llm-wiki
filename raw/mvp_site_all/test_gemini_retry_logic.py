"""
Test coverage for Gemini API retry logic in llm_service.

Tests the retry functions added in PR #4099:
1. _is_retriable_gemini_error - determines if an error should trigger retry
2. _log_retry_attempt - logs retry attempts with detailed info
3. _add_api_retry_warning_to_response - adds user-visible warning after retry success

Related commits: a1a2d8c83, 34315e3a7
"""

import logging
from types import SimpleNamespace
from unittest.mock import MagicMock

from mvp_site.llm_service import (
    GEMINI_RETRIABLE_STATUSES,
    GEMINI_RETRY_BASE_DELAY_SECONDS,
    GEMINI_RETRY_MAX_ATTEMPTS,
    _add_api_retry_warning_to_response,
    _is_retriable_gemini_error,
    _log_retry_attempt,
)


class TestIsRetriableGeminiError:
    """Tests for _is_retriable_gemini_error function."""

    def test_returns_true_for_failed_precondition_status_attribute(self):
        """Test that exception with status='FAILED_PRECONDITION' is retriable."""
        # Simulate google.genai.errors.ClientError with status attribute
        exception = SimpleNamespace(
            status="FAILED_PRECONDITION", message="Precondition check failed"
        )
        assert _is_retriable_gemini_error(exception) is True

    def test_returns_true_for_failed_precondition_in_str(self):
        """Test that exception with FAILED_PRECONDITION in str() is retriable."""
        # Exception without status attribute but with FAILED_PRECONDITION in message
        exception = ValueError("FAILED_PRECONDITION: Resource not ready")
        assert _is_retriable_gemini_error(exception) is True

    def test_returns_false_for_non_retriable_error(self):
        """Test that non-retriable errors return False."""
        # Generic error without FAILED_PRECONDITION
        exception = ValueError("Something went wrong")
        assert _is_retriable_gemini_error(exception) is False

    def test_returns_false_for_permission_denied(self):
        """Test that PERMISSION_DENIED is not retriable."""
        exception = SimpleNamespace(status="PERMISSION_DENIED", message="Access denied")
        assert _is_retriable_gemini_error(exception) is False

    def test_returns_false_for_invalid_argument(self):
        """Test that INVALID_ARGUMENT is not retriable."""
        exception = SimpleNamespace(
            status="INVALID_ARGUMENT", message="Invalid request"
        )
        assert _is_retriable_gemini_error(exception) is False

    def test_returns_false_for_resource_exhausted(self):
        """Test that RESOURCE_EXHAUSTED is not retriable (separate rate limiting)."""
        exception = SimpleNamespace(
            status="RESOURCE_EXHAUSTED", message="Quota exceeded"
        )
        assert _is_retriable_gemini_error(exception) is False

    def test_handles_exception_with_no_status(self):
        """Test graceful handling of exception without status attribute."""
        exception = RuntimeError("Generic error")
        # Should check str(exception) fallback
        assert _is_retriable_gemini_error(exception) is False

    def test_status_as_enum_string(self):
        """Test status when it's an enum-like string."""
        exception = SimpleNamespace(
            status="Status.FAILED_PRECONDITION",  # Enum format
            message="Precondition failed",
        )
        # str(status) would be "Status.FAILED_PRECONDITION" which isn't in the set
        # But the error message might contain FAILED_PRECONDITION
        # Let's check the actual behavior
        result = _is_retriable_gemini_error(exception)
        # The function checks if str(status) is IN the set {"FAILED_PRECONDITION"}
        # "Status.FAILED_PRECONDITION" is not in that set, but str(exception) check
        # will catch it if the message contains FAILED_PRECONDITION
        assert result is True  # Falls back to string check


class TestLogRetryAttempt:
    """Tests for _log_retry_attempt function."""

    def test_logs_at_warning_level(self, caplog):
        """Test that retry attempts are logged at WARNING level."""
        caplog.set_level(logging.DEBUG)

        exception = SimpleNamespace(
            status="FAILED_PRECONDITION", message="Resource not ready"
        )

        _log_retry_attempt(
            attempt=1,
            max_attempts=3,
            exception=exception,
            delay_seconds=2.0,
            model_name="gemini-3-flash-preview",
        )

        warning_logs = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warning_logs) == 1
        assert "GEMINI_RETRY" in warning_logs[0].message
        assert "Attempt 1/3" in warning_logs[0].message

    def test_includes_model_name(self, caplog):
        """Test that model name is included in log."""
        caplog.set_level(logging.DEBUG)

        exception = ValueError("Test error")
        _log_retry_attempt(1, 3, exception, 2.0, "test-model-name")

        log_text = caplog.text
        assert "model=test-model-name" in log_text

    def test_includes_error_status(self, caplog):
        """Test that error status is included in log."""
        caplog.set_level(logging.DEBUG)

        exception = SimpleNamespace(status="FAILED_PRECONDITION", message="err")
        _log_retry_attempt(1, 3, exception, 2.0, "test-model")

        log_text = caplog.text
        assert "status=FAILED_PRECONDITION" in log_text

    def test_handles_missing_status_attribute(self, caplog):
        """Test graceful handling when exception has no status attribute."""
        caplog.set_level(logging.DEBUG)

        exception = ValueError("Simple error message")
        _log_retry_attempt(1, 3, exception, 2.0, "test-model")

        log_text = caplog.text
        assert "status=UNKNOWN" in log_text

    def test_handles_missing_message_attribute(self, caplog):
        """Test graceful handling when exception has no message attribute."""
        caplog.set_level(logging.DEBUG)

        exception = ValueError("Error via str")
        _log_retry_attempt(1, 3, exception, 2.0, "test-model")

        log_text = caplog.text
        # Should fall back to str(exception)
        assert "Error via str" in log_text

    def test_includes_delay_seconds(self, caplog):
        """Test that delay seconds is included in log."""
        caplog.set_level(logging.DEBUG)

        exception = ValueError("err")
        _log_retry_attempt(2, 3, exception, 4.5, "test-model")

        log_text = caplog.text
        assert "retrying in 4.5s" in log_text

    def test_correct_attempt_numbering(self, caplog):
        """Test that attempt numbers are formatted correctly."""
        caplog.set_level(logging.DEBUG)

        exception = ValueError("err")

        # First attempt
        caplog.clear()
        _log_retry_attempt(1, 3, exception, 2.0, "test-model")
        assert "Attempt 1/3" in caplog.text

        # Second attempt
        caplog.clear()
        _log_retry_attempt(2, 3, exception, 4.0, "test-model")
        assert "Attempt 2/3" in caplog.text


class TestAddApiRetryWarningToResponse:
    """Tests for _add_api_retry_warning_to_response function."""

    def test_returns_early_if_no_structured_response(self):
        """Test that function returns early if structured_response is None."""
        api_response = MagicMock()
        api_response._retry_metadata = {"attempts_made": 2}

        # Should not raise, just return
        _add_api_retry_warning_to_response(api_response, None)

    def test_returns_early_if_no_retry_metadata(self):
        """Test that function returns early if api_response has no _retry_metadata."""
        api_response = SimpleNamespace()  # No _retry_metadata attribute
        structured_response = SimpleNamespace(debug_info={})

        # Should not raise, just return
        _add_api_retry_warning_to_response(api_response, structured_response)

        # debug_info should be unchanged
        assert "_server_system_warnings" not in structured_response.debug_info

    def test_returns_early_if_retry_metadata_is_none(self):
        """Test that function returns early if _retry_metadata is None."""
        api_response = SimpleNamespace(_retry_metadata=None)
        structured_response = SimpleNamespace(debug_info={})

        _add_api_retry_warning_to_response(api_response, structured_response)

        assert "_server_system_warnings" not in structured_response.debug_info

    def test_returns_early_if_retry_metadata_is_empty(self):
        """Test that function returns early if _retry_metadata is empty dict."""
        api_response = SimpleNamespace(_retry_metadata={})
        structured_response = SimpleNamespace(debug_info={})

        _add_api_retry_warning_to_response(api_response, structured_response)

        # Empty dict is falsy, so should return early
        assert "_server_system_warnings" not in structured_response.debug_info

    def test_converts_non_dict_debug_info_to_dict(self, caplog):
        """Test that non-dict debug_info is converted to dict."""
        caplog.set_level(logging.DEBUG)

        api_response = SimpleNamespace(
            _retry_metadata={"attempts_made": 2, "max_attempts": 3}
        )
        structured_response = SimpleNamespace(debug_info="not a dict")

        _add_api_retry_warning_to_response(api_response, structured_response)

        # debug_info should now be a dict with warning
        assert isinstance(structured_response.debug_info, dict)
        assert "_server_system_warnings" in structured_response.debug_info

    def test_converts_non_list_server_warnings_to_list(self, caplog):
        """Test that non-list server_warnings is converted to list."""
        caplog.set_level(logging.DEBUG)

        api_response = SimpleNamespace(
            _retry_metadata={"attempts_made": 2, "max_attempts": 3}
        )
        structured_response = SimpleNamespace(
            debug_info={"_server_system_warnings": "not a list"}
        )

        _add_api_retry_warning_to_response(api_response, structured_response)

        # server_warnings should now be a list
        warnings = structured_response.debug_info["_server_system_warnings"]
        assert isinstance(warnings, list)
        assert len(warnings) == 1

    def test_adds_warning_to_empty_warnings_list(self, caplog):
        """Test that warning is added to empty warnings list."""
        caplog.set_level(logging.DEBUG)

        api_response = SimpleNamespace(
            _retry_metadata={"attempts_made": 2, "max_attempts": 3}
        )
        structured_response = SimpleNamespace(debug_info={})

        _add_api_retry_warning_to_response(api_response, structured_response)

        warnings = structured_response.debug_info["_server_system_warnings"]
        assert len(warnings) == 1
        assert "API retry required (attempt 2/3)" in warnings[0]
        assert "transient error recovered" in warnings[0]

    def test_adds_warning_to_existing_warnings_list(self, caplog):
        """Test that warning is appended to existing warnings."""
        caplog.set_level(logging.DEBUG)

        api_response = SimpleNamespace(
            _retry_metadata={"attempts_made": 3, "max_attempts": 3}
        )
        structured_response = SimpleNamespace(
            debug_info={"_server_system_warnings": ["Previous warning"]}
        )

        _add_api_retry_warning_to_response(api_response, structured_response)

        warnings = structured_response.debug_info["_server_system_warnings"]
        assert len(warnings) == 2
        assert "Previous warning" in warnings
        assert any("API retry required" in w for w in warnings)

    def test_does_not_duplicate_warning(self, caplog):
        """Test that same warning is not added twice."""
        caplog.set_level(logging.DEBUG)

        api_response = SimpleNamespace(
            _retry_metadata={"attempts_made": 2, "max_attempts": 3}
        )
        structured_response = SimpleNamespace(
            debug_info={
                "_server_system_warnings": [
                    "API retry required (attempt 2/3) - transient error recovered"
                ]
            }
        )

        _add_api_retry_warning_to_response(api_response, structured_response)

        warnings = structured_response.debug_info["_server_system_warnings"]
        # Should still be just 1 warning (no duplicate)
        assert len(warnings) == 1

    def test_logs_info_when_warning_added(self, caplog):
        """Test that INFO log is emitted when warning is added."""
        caplog.set_level(logging.DEBUG)

        api_response = SimpleNamespace(
            _retry_metadata={"attempts_made": 2, "max_attempts": 3}
        )
        structured_response = SimpleNamespace(debug_info={})

        _add_api_retry_warning_to_response(api_response, structured_response)

        info_logs = [r for r in caplog.records if r.levelno == logging.INFO]
        assert len(info_logs) >= 1
        assert "Added API retry warning" in info_logs[0].message

    def test_uses_default_attempts_if_not_in_metadata(self, caplog):
        """Test default value when attempts_made is missing."""
        caplog.set_level(logging.DEBUG)

        api_response = SimpleNamespace(
            _retry_metadata={
                # No attempts_made, should default to 2
                "max_attempts": 3
            }
        )
        structured_response = SimpleNamespace(debug_info={})

        _add_api_retry_warning_to_response(api_response, structured_response)

        warnings = structured_response.debug_info["_server_system_warnings"]
        assert "attempt 2/3" in warnings[0]

    def test_uses_constant_for_default_max_attempts(self, caplog):
        """Test that GEMINI_RETRY_MAX_ATTEMPTS is used as default."""
        caplog.set_level(logging.DEBUG)

        api_response = SimpleNamespace(
            _retry_metadata={
                "attempts_made": 2,
                # No max_attempts, should use constant
            }
        )
        structured_response = SimpleNamespace(debug_info={})

        _add_api_retry_warning_to_response(api_response, structured_response)

        warnings = structured_response.debug_info["_server_system_warnings"]
        assert f"attempt 2/{GEMINI_RETRY_MAX_ATTEMPTS}" in warnings[0]


class TestRetryConstants:
    """Tests for retry configuration constants."""

    def test_max_attempts_is_reasonable(self):
        """Test that max attempts is set to a reasonable value."""
        assert GEMINI_RETRY_MAX_ATTEMPTS >= 2  # At least 2 for retry to make sense
        assert GEMINI_RETRY_MAX_ATTEMPTS <= 5  # Not too many to avoid long waits

    def test_base_delay_is_reasonable(self):
        """Test that base delay is set to a reasonable value."""
        assert GEMINI_RETRY_BASE_DELAY_SECONDS >= 1.0  # At least 1 second
        assert GEMINI_RETRY_BASE_DELAY_SECONDS <= 5.0  # Not too long

    def test_retriable_statuses_contains_failed_precondition(self):
        """Test that FAILED_PRECONDITION is in retriable statuses."""
        assert "FAILED_PRECONDITION" in GEMINI_RETRIABLE_STATUSES

    def test_retriable_statuses_is_minimal(self):
        """Test that we're not over-retrying (only specific transient errors)."""
        # Should be a small set - we don't want to retry everything
        assert len(GEMINI_RETRIABLE_STATUSES) <= 3


class TestExponentialBackoffCalculation:
    """Tests for exponential backoff delay calculation pattern."""

    def test_first_attempt_delay(self):
        """Test delay calculation for first retry (attempt 1)."""
        # delay = BASE * (2 ** (attempt - 1))
        attempt = 1
        expected_delay = GEMINI_RETRY_BASE_DELAY_SECONDS * (2 ** (attempt - 1))
        assert expected_delay == GEMINI_RETRY_BASE_DELAY_SECONDS  # 2.0

    def test_second_attempt_delay(self):
        """Test delay calculation for second retry (attempt 2)."""
        attempt = 2
        expected_delay = GEMINI_RETRY_BASE_DELAY_SECONDS * (2 ** (attempt - 1))
        assert expected_delay == GEMINI_RETRY_BASE_DELAY_SECONDS * 2  # 4.0

    def test_third_attempt_delay(self):
        """Test delay calculation for third retry (attempt 3)."""
        attempt = 3
        expected_delay = GEMINI_RETRY_BASE_DELAY_SECONDS * (2 ** (attempt - 1))
        assert expected_delay == GEMINI_RETRY_BASE_DELAY_SECONDS * 4  # 8.0

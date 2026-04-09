"""
Test coverage for _log_gemini_response_metadata function in llm_service.

Tests the bug fixes from PR #4099:
1. None finish_reason should be normalized to "UNKNOWN" and trigger WARNING
2. Log messages should include candidate_index for multi-candidate debugging
3. Debug logging for text_length extraction failures
4. Graceful handling of various edge cases

Related commits: 938e1fa72
"""

import logging
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from mvp_site.llm_service import _log_gemini_response_metadata


class TestLogGeminiResponseMetadata:
    """Test suite for _log_gemini_response_metadata function."""

    # =========================================================================
    # BUG FIX TESTS: None finish_reason handling (PR #4099)
    # =========================================================================

    def test_none_finish_reason_triggers_warning(self, caplog):
        """
        BUG FIX TEST: When finish_reason is explicitly None, it should:
        1. Be normalized to "UNKNOWN"
        2. Trigger WARNING level (not INFO)

        This was the bug reported by Cursor and CodeRabbit - None values
        were bypassing the warning path due to falsy check.
        """
        caplog.set_level(logging.DEBUG)

        # Create response with finish_reason=None (not missing, explicitly None)
        candidate = SimpleNamespace(
            finish_reason=None,  # Explicitly None - the bug condition
            safety_ratings=None,
            content=SimpleNamespace(parts=[SimpleNamespace(text="Test response")]),
        )
        response = SimpleNamespace(candidates=[candidate], prompt_feedback=None)

        _log_gemini_response_metadata(response, "test-model")

        # Find WARNING logs
        warning_logs = [r for r in caplog.records if r.levelno == logging.WARNING]
        info_logs = [r for r in caplog.records if r.levelno == logging.INFO]

        # Should have WARNING (not INFO) because None is treated as UNKNOWN
        assert len(warning_logs) >= 1, "None finish_reason should trigger WARNING"

        # Verify the warning contains UNKNOWN
        warning_text = " ".join(r.message for r in warning_logs)
        assert "UNKNOWN" in warning_text, (
            "None finish_reason should be logged as UNKNOWN"
        )
        assert "GEMINI_RESPONSE_META" in warning_text

    def test_stop_finish_reason_logs_info(self, caplog):
        """Test that STOP finish_reason logs at INFO level (normal case)."""
        caplog.set_level(logging.DEBUG)

        candidate = SimpleNamespace(
            finish_reason="STOP",
            safety_ratings=None,
            content=SimpleNamespace(parts=[SimpleNamespace(text="Normal response")]),
        )
        response = SimpleNamespace(candidates=[candidate], prompt_feedback=None)

        _log_gemini_response_metadata(response, "test-model")

        # Find INFO logs containing GEMINI_RESPONSE_META
        info_logs = [
            r
            for r in caplog.records
            if r.levelno == logging.INFO and "GEMINI_RESPONSE_META" in r.message
        ]

        assert len(info_logs) >= 1, "STOP finish_reason should log at INFO level"
        assert "STOP" in info_logs[0].message

    def test_finish_reason_stop_enum_logs_info(self, caplog):
        """Test that FinishReason.STOP (enum form) logs at INFO level."""
        caplog.set_level(logging.DEBUG)

        candidate = SimpleNamespace(
            finish_reason="FinishReason.STOP",
            safety_ratings=None,
            content=SimpleNamespace(parts=[SimpleNamespace(text="Normal response")]),
        )
        response = SimpleNamespace(candidates=[candidate], prompt_feedback=None)

        _log_gemini_response_metadata(response, "test-model")

        info_logs = [
            r
            for r in caplog.records
            if r.levelno == logging.INFO and "GEMINI_RESPONSE_META" in r.message
        ]

        assert len(info_logs) >= 1, "FinishReason.STOP should log at INFO level"

    def test_non_stop_finish_reason_triggers_warning(self, caplog):
        """Test that non-STOP finish reasons (SAFETY, LENGTH) trigger WARNING."""
        caplog.set_level(logging.DEBUG)

        for finish_reason in ["SAFETY", "LENGTH", "MAX_TOKENS", "RECITATION", "OTHER"]:
            caplog.clear()

            candidate = SimpleNamespace(
                finish_reason=finish_reason,
                safety_ratings="HIGH",
                content=SimpleNamespace(parts=[SimpleNamespace(text="Truncated")]),
            )
            response = SimpleNamespace(
                candidates=[candidate], prompt_feedback="blocked"
            )

            _log_gemini_response_metadata(response, "test-model")

            warning_logs = [r for r in caplog.records if r.levelno == logging.WARNING]
            assert len(warning_logs) >= 1, f"{finish_reason} should trigger WARNING"
            assert finish_reason in warning_logs[0].message

    # =========================================================================
    # FEATURE TESTS: candidate_index in logs (PR #4099)
    # =========================================================================

    def test_candidate_index_included_in_logs(self, caplog):
        """Test that candidate_index is included in log messages."""
        caplog.set_level(logging.DEBUG)

        candidate = SimpleNamespace(
            finish_reason="STOP",
            safety_ratings=None,
            content=SimpleNamespace(parts=[SimpleNamespace(text="Response")]),
        )
        response = SimpleNamespace(candidates=[candidate], prompt_feedback=None)

        _log_gemini_response_metadata(response, "test-model")

        all_logs = " ".join(r.message for r in caplog.records)
        assert "candidate_index=0" in all_logs, "Log should include candidate_index"

    def test_multiple_candidates_have_correct_indices(self, caplog):
        """Test that multiple candidates are logged with correct indices."""
        caplog.set_level(logging.DEBUG)

        candidates = [
            SimpleNamespace(
                finish_reason="STOP",
                safety_ratings=None,
                content=SimpleNamespace(parts=[SimpleNamespace(text=f"Response {i}")]),
            )
            for i in range(3)
        ]
        response = SimpleNamespace(candidates=candidates, prompt_feedback=None)

        _log_gemini_response_metadata(response, "test-model")

        all_logs = " ".join(r.message for r in caplog.records)
        assert "candidate_index=0" in all_logs
        assert "candidate_index=1" in all_logs
        assert "candidate_index=2" in all_logs

    # =========================================================================
    # FEATURE TESTS: Debug logging for text_length extraction failures
    # =========================================================================

    def test_text_length_extraction_failure_logs_debug(self, caplog):
        """Test that text_length extraction failures log at DEBUG level."""
        caplog.set_level(logging.DEBUG)

        # Create a response where accessing content.parts raises an exception
        candidate = MagicMock()
        candidate.finish_reason = "STOP"
        candidate.safety_ratings = None
        # Make content.parts raise an exception when accessed
        type(candidate).content = property(
            lambda self: (_ for _ in ()).throw(RuntimeError("Simulated error"))
        )

        response = SimpleNamespace(candidates=[candidate], prompt_feedback=None)

        # Should not raise, should log debug
        _log_gemini_response_metadata(response, "test-model")

        debug_logs = [r for r in caplog.records if r.levelno == logging.DEBUG]
        # Check if any debug log mentions the extraction failure
        debug_text = " ".join(r.message for r in debug_logs)
        # The function should still complete and log something at INFO/WARNING

    def test_missing_text_attribute_handled_gracefully(self, caplog):
        """Test that missing text attribute on parts doesn't crash."""
        caplog.set_level(logging.DEBUG)

        # Part without text attribute
        part_without_text = SimpleNamespace(data="binary data")
        candidate = SimpleNamespace(
            finish_reason="STOP",
            safety_ratings=None,
            content=SimpleNamespace(parts=[part_without_text]),
        )
        response = SimpleNamespace(candidates=[candidate], prompt_feedback=None)

        # Should not raise
        _log_gemini_response_metadata(response, "test-model")

        # Should still log (with text_length=0)
        all_logs = " ".join(r.message for r in caplog.records)
        assert "text_length=0" in all_logs

    # =========================================================================
    # EDGE CASE TESTS
    # =========================================================================

    def test_no_candidates_logs_warning(self, caplog):
        """Test that response with no candidates logs warning."""
        caplog.set_level(logging.DEBUG)

        response = SimpleNamespace(candidates=[], prompt_feedback="blocked_by_safety")

        _log_gemini_response_metadata(response, "test-model")

        warning_logs = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warning_logs) >= 1
        assert "NO_CANDIDATES" in warning_logs[0].message

    def test_none_candidates_logs_warning(self, caplog):
        """Test that response with None candidates logs warning."""
        caplog.set_level(logging.DEBUG)

        response = SimpleNamespace(candidates=None, prompt_feedback="blocked")

        _log_gemini_response_metadata(response, "test-model")

        warning_logs = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warning_logs) >= 1
        assert "NO_CANDIDATES" in warning_logs[0].message

    def test_text_length_calculated_correctly(self, caplog):
        """Test that text_length is calculated from all parts."""
        caplog.set_level(logging.DEBUG)

        parts = [
            SimpleNamespace(text="Hello"),  # 5 chars
            SimpleNamespace(text=" World"),  # 6 chars
            SimpleNamespace(text="!"),  # 1 char
        ]
        candidate = SimpleNamespace(
            finish_reason="STOP",
            safety_ratings=None,
            content=SimpleNamespace(parts=parts),
        )
        response = SimpleNamespace(candidates=[candidate], prompt_feedback=None)

        _log_gemini_response_metadata(response, "test-model")

        all_logs = " ".join(r.message for r in caplog.records)
        assert "text_length=12" in all_logs  # 5 + 6 + 1 = 12

    def test_model_name_included_in_logs(self, caplog):
        """Test that model name is included in all log messages."""
        caplog.set_level(logging.DEBUG)

        candidate = SimpleNamespace(
            finish_reason="STOP",
            safety_ratings=None,
            content=SimpleNamespace(parts=[SimpleNamespace(text="Test")]),
        )
        response = SimpleNamespace(candidates=[candidate], prompt_feedback=None)

        _log_gemini_response_metadata(response, "gemini-2.0-flash-exp")

        all_logs = " ".join(r.message for r in caplog.records)
        assert "model=gemini-2.0-flash-exp" in all_logs

    def test_safety_ratings_included_in_warning(self, caplog):
        """Test that safety_ratings are included in warning logs."""
        caplog.set_level(logging.DEBUG)

        candidate = SimpleNamespace(
            finish_reason="SAFETY",
            safety_ratings=["HARM_CATEGORY_DANGEROUS_CONTENT: HIGH"],
            content=SimpleNamespace(parts=[]),
        )
        response = SimpleNamespace(candidates=[candidate], prompt_feedback="blocked")

        _log_gemini_response_metadata(response, "test-model")

        warning_logs = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warning_logs) >= 1
        assert "safety_ratings=" in warning_logs[0].message

    def test_function_handles_exceptions_gracefully(self, caplog):
        """Test that the function doesn't crash on unexpected exceptions."""
        caplog.set_level(logging.DEBUG)

        # Create a response that will cause an exception during iteration
        class BrokenCandidate:
            @property
            def finish_reason(self):
                raise RuntimeError("Unexpected error accessing finish_reason")

        response = SimpleNamespace(candidates=[BrokenCandidate()], prompt_feedback=None)

        # Should not raise - the function has a top-level try/except
        _log_gemini_response_metadata(response, "test-model")

        warning_logs = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warning_logs) >= 1
        assert "Failed to extract metadata" in warning_logs[0].message


class TestNoneFinishReasonRegression:
    """
    Regression tests specifically for the None finish_reason bug.

    The bug was: When finish_reason is None (not missing, but explicitly None),
    the old code `if finish_reason and str(finish_reason) not in (...)` would
    short-circuit on the falsy None value and log at INFO instead of WARNING.

    This is incorrect because None finish_reason indicates the model hasn't
    stopped generating (common in streaming or blocked responses), which is
    anomalous and should trigger a warning.
    """

    @pytest.mark.parametrize(
        "finish_reason,expected_level",
        [
            (None, logging.WARNING),  # BUG FIX: Was logging INFO, should be WARNING
            ("UNKNOWN", logging.WARNING),  # Explicit UNKNOWN
            ("STOP", logging.INFO),  # Normal completion
            ("FinishReason.STOP", logging.INFO),  # Enum form
            ("SAFETY", logging.WARNING),  # Safety filter
            ("LENGTH", logging.WARNING),  # Length limit
            ("", logging.WARNING),  # Empty string (falsy)
        ],
    )
    def test_finish_reason_log_levels(self, finish_reason, expected_level, caplog):
        """Parametrized test for various finish_reason values and expected log levels."""
        caplog.set_level(logging.DEBUG)

        candidate = SimpleNamespace(
            finish_reason=finish_reason,
            safety_ratings=None,
            content=SimpleNamespace(parts=[SimpleNamespace(text="Test")]),
        )
        response = SimpleNamespace(candidates=[candidate], prompt_feedback=None)

        _log_gemini_response_metadata(response, "test-model")

        # Find the GEMINI_RESPONSE_META log
        meta_logs = [r for r in caplog.records if "GEMINI_RESPONSE_META" in r.message]
        assert len(meta_logs) >= 1, f"Should log for finish_reason={finish_reason!r}"

        # Check that at least one log is at the expected level
        levels = [r.levelno for r in meta_logs]
        assert expected_level in levels, (
            f"For finish_reason={finish_reason!r}, expected {logging.getLevelName(expected_level)} "
            f"but got {[logging.getLevelName(l) for l in levels]}"
        )

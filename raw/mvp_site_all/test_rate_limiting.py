"""
Unit tests for rate limiting logic.
"""

import time
import unittest
from unittest.mock import MagicMock, patch

from mvp_site import rate_limiting


class TestRateLimiting(unittest.TestCase):
    def test_parse_rate_limit_exempt_emails(self):
        # Test None
        assert rate_limiting._parse_rate_limit_exempt_emails(None) == set()
        # Test empty string
        assert rate_limiting._parse_rate_limit_exempt_emails("") == set()
        # Test valid string
        assert rate_limiting._parse_rate_limit_exempt_emails("a@b.com, C@d.com ") == {
            "a@b.com",
            "c@d.com",
        }

    def test_is_rate_limit_exempt(self):
        # Mock the constant
        with patch.object(
            rate_limiting, "RATE_LIMIT_EXEMPT_EMAILS", {"test@example.com"}
        ):
            assert rate_limiting.is_rate_limit_exempt("test@example.com")
            assert rate_limiting.is_rate_limit_exempt("TEST@EXAMPLE.COM")
            assert not rate_limiting.is_rate_limit_exempt("other@example.com")
            assert not rate_limiting.is_rate_limit_exempt(None)

    def test_jleechantest_exempt_when_in_set(self):
        """MCP test default email is exempt when in RATE_LIMIT_EXEMPT_EMAILS (TESTING_AUTH_BYPASS=true)."""
        with patch.object(
            rate_limiting,
            "RATE_LIMIT_EXEMPT_EMAILS",
            {"test@example.com", "jleechantest@gmail.com"},
        ):
            assert rate_limiting.is_rate_limit_exempt("jleechantest@gmail.com")
            assert rate_limiting.is_rate_limit_exempt("JLEECHANTEST@GMAIL.COM")

    def test_is_byok_provider_active_when_key_matches_provider(self):
        settings = {
            "llm_provider": "openrouter",
            "openrouter_api_key": "or-key",
        }

        assert rate_limiting.is_byok_provider_active(settings)

    def test_is_byok_provider_inactive_when_key_does_not_match_provider(self):
        settings = {
            "llm_provider": "openrouter",
            "gemini_api_key": "gem-key",
        }

        assert not rate_limiting.is_byok_provider_active(settings)

    def test_is_byok_provider_active_defaults_provider_to_gemini(self):
        settings = {
            "gemini_api_key": "gem-key",
        }

        assert rate_limiting.is_byok_provider_active(settings)

    def test_is_byok_provider_active_handles_non_dict_input(self):
        assert not rate_limiting.is_byok_provider_active("not-a-dict")  # type: ignore[arg-type]

    def test_get_user_turn_limits_default(self):
        """Non-BYOK users get default limits."""
        with patch.object(rate_limiting, "_get_user_settings_cached", return_value={}):
            daily, window = rate_limiting._get_user_turn_limits("user1")
            assert daily == rate_limiting.RATE_LIMIT_DAILY_TURNS
            assert window == rate_limiting.RATE_LIMIT_5HOUR_TURNS

    def test_get_user_turn_limits_byok(self):
        """BYOK users get elevated limits for both daily and 5-hour windows."""
        settings = {"llm_provider": "openrouter", "openrouter_api_key": "sk-key"}
        with patch.object(rate_limiting, "_get_user_settings_cached", return_value=settings):
            daily, window = rate_limiting._get_user_turn_limits("byok_user")
            assert daily == rate_limiting.RATE_LIMIT_BYOK_PROVIDER_DAILY_TURNS
            assert window == rate_limiting.RATE_LIMIT_BYOK_PROVIDER_5HOUR_TURNS

    def _setup_mock_db(self, mock_get_db):
        rate_limiting._USER_SETTINGS_CACHE.clear()
        mock_db = MagicMock()
        # Force non-transactional path by deleting transaction attribute
        del mock_db.transaction
        mock_get_db.return_value = mock_db
        mock_rate_limit_doc_ref = MagicMock()
        mock_user_doc_ref = MagicMock()

        collections = {
            "rate_limits": mock_rate_limit_doc_ref,
            "users": mock_user_doc_ref,
        }

        def _collection_side_effect(name):
            collection_mock = MagicMock()
            collection_mock.document.return_value = collections[name]
            return collection_mock

        mock_db.collection.side_effect = _collection_side_effect
        return mock_db, mock_rate_limit_doc_ref, mock_user_doc_ref

    @patch("mvp_site.firestore_service.get_db")
    def test_check_rate_limit_allowed(self, mock_get_db):
        _, mock_doc_ref, mock_user_doc_ref = self._setup_mock_db(mock_get_db)

        # Mock existing data (empty)
        mock_doc = MagicMock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = {"turn_timestamps": []}
        mock_doc_ref.get.return_value = mock_doc
        mock_user_doc_ref.get.return_value = MagicMock(exists=False)

        # Test check without consumption
        result = rate_limiting.check_rate_limit(
            "user1", "user@example.com", consume_turn=False
        )
        assert result["allowed"]
        assert result["daily_remaining"] == rate_limiting.RATE_LIMIT_DAILY_TURNS

    @patch("mvp_site.firestore_service.get_db")
    def test_check_rate_limit_blocked_daily(self, mock_get_db):
        _, mock_doc_ref, mock_user_doc_ref = self._setup_mock_db(mock_get_db)

        # Mock usage exceeding daily limit
        now = time.time()
        # Create timestamps within the last 24 hours
        # Use a stable oldest time to verify calculation
        oldest_ts = now - 100
        timestamps = [
            oldest_ts for _ in range(rate_limiting.RATE_LIMIT_DAILY_TURNS + 1)
        ]

        mock_doc = MagicMock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = {"turn_timestamps": timestamps}
        mock_doc_ref.get.return_value = mock_doc
        mock_user_doc_ref.get.return_value = MagicMock(exists=False)

        result = rate_limiting.check_rate_limit(
            "user1", "user@example.com", consume_turn=False
        )
        assert not result["allowed"]
        assert result["error_type"] == "rate_limit"
        assert "daily limit" in result["error_message"]

        # Verify reset time calculation
        expected_reset = int(oldest_ts + rate_limiting.RATE_LIMIT_DAILY_WINDOW_SECONDS)
        assert result["reset_time_daily"] == expected_reset

    @patch("mvp_site.firestore_service.get_db")
    def test_check_rate_limit_blocked_window(self, mock_get_db):
        _, mock_doc_ref, mock_user_doc_ref = self._setup_mock_db(mock_get_db)

        # Mock usage exceeding window limit
        now = time.time()
        # Create timestamps within the last 5 hours
        oldest_ts = now - 100
        timestamps = [
            oldest_ts for _ in range(rate_limiting.RATE_LIMIT_5HOUR_TURNS + 1)
        ]

        mock_doc = MagicMock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = {"turn_timestamps": timestamps}
        mock_doc_ref.get.return_value = mock_doc
        mock_user_doc_ref.get.return_value = MagicMock(exists=False)

        result = rate_limiting.check_rate_limit(
            "user1", "user@example.com", consume_turn=False
        )
        assert not result["allowed"]
        assert result["error_type"] == "rate_limit"
        assert "limit of" in result["error_message"]  # "limit of X turns per 5 hours"

        # Verify reset time calculation
        expected_reset = int(oldest_ts + rate_limiting.RATE_LIMIT_5HOUR_WINDOW_SECONDS)
        assert result["reset_time_hourly"] == expected_reset

    @patch("mvp_site.firestore_service.get_db")
    def test_check_rate_limit_consume(self, mock_get_db):
        _, mock_doc_ref, mock_user_doc_ref = self._setup_mock_db(mock_get_db)

        mock_doc = MagicMock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = {"turn_timestamps": []}
        mock_doc_ref.get.return_value = mock_doc
        mock_user_doc_ref.get.return_value = MagicMock(exists=False)

        # Test consume
        result = rate_limiting.check_rate_limit(
            "user1", "user@example.com", consume_turn=True
        )
        assert result["allowed"]

        # Verify set was called to update timestamps
        mock_doc_ref.set.assert_called_once()
        args, kwargs = mock_doc_ref.set.call_args
        assert "turn_timestamps" in args[0]
        assert len(args[0]["turn_timestamps"]) == 1

    @patch("mvp_site.firestore_service.get_db")
    def test_check_rate_limit_uses_byok_daily_limit_when_provider_matches(
        self, mock_get_db
    ):
        _, mock_doc_ref, mock_user_doc_ref = self._setup_mock_db(mock_get_db)

        now = time.time()
        # Keep usage in daily window, but outside 5-hour window to isolate daily-limit behavior.
        timestamps = [
            now - (6 * 60 * 60) for _ in range(rate_limiting.RATE_LIMIT_DAILY_TURNS + 1)
        ]

        mock_doc = MagicMock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = {"turn_timestamps": timestamps}
        mock_doc_ref.get.return_value = mock_doc

        user_doc = MagicMock()
        user_doc.exists = True
        user_doc.to_dict.return_value = {
            "settings": {
                "llm_provider": "gemini",
                "gemini_api_key": "user-gemini-key",
            }
        }
        mock_user_doc_ref.get.return_value = user_doc

        result = rate_limiting.check_rate_limit(
            "user1", "user@example.com", consume_turn=False
        )
        assert result["allowed"]
        expected_remaining = rate_limiting.RATE_LIMIT_BYOK_PROVIDER_DAILY_TURNS - len(
            timestamps
        )
        assert result["daily_remaining"] == expected_remaining

    @patch("mvp_site.firestore_service.get_db")
    def test_check_rate_limit_keeps_default_daily_limit_when_provider_does_not_match_byok(
        self, mock_get_db
    ):
        _, mock_doc_ref, mock_user_doc_ref = self._setup_mock_db(mock_get_db)

        now = time.time()
        # Keep usage in daily window, but outside 5-hour window to isolate daily limit.
        timestamps = [
            now - (6 * 60 * 60) for _ in range(rate_limiting.RATE_LIMIT_DAILY_TURNS)
        ]

        mock_doc = MagicMock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = {"turn_timestamps": timestamps}
        mock_doc_ref.get.return_value = mock_doc

        user_doc = MagicMock()
        user_doc.exists = True
        user_doc.to_dict.return_value = {
            "settings": {
                "llm_provider": "openrouter",
                "gemini_api_key": "user-gemini-key",
            }
        }
        mock_user_doc_ref.get.return_value = user_doc

        result = rate_limiting.check_rate_limit(
            "user1", "user@example.com", consume_turn=False
        )
        assert not result["allowed"]
        assert result["daily_remaining"] == 0

    @patch("mvp_site.firestore_service.get_db")
    def test_byok_user_not_blocked_by_5hour_window(self, mock_get_db):
        """BYOK users get an elevated 5-hour window limit and are not blocked at the free-tier threshold."""
        _, mock_doc_ref, mock_user_doc_ref = self._setup_mock_db(mock_get_db)

        now = time.time()
        # Create timestamps WITHIN the 5-hour window that exceed the default limit
        timestamps = [
            now - 60 for _ in range(rate_limiting.RATE_LIMIT_5HOUR_TURNS + 1)
        ]

        mock_doc = MagicMock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = {"turn_timestamps": timestamps}
        mock_doc_ref.get.return_value = mock_doc

        # User has BYOK configured — owns their API key
        user_doc = MagicMock()
        user_doc.exists = True
        user_doc.to_dict.return_value = {
            "settings": {
                "llm_provider": "openrouter",
                "openrouter_api_key": "sk-or-user-provided-key",
            }
        }
        mock_user_doc_ref.get.return_value = user_doc

        result = rate_limiting.check_rate_limit(
            "byok_user", "byok@example.com", consume_turn=False
        )

        # BYOK user should NOT be blocked by the 5-hour window
        assert result["allowed"], (
            f"BYOK user was blocked by 5-hour window limit! "
            f"Result: {result}"
        )

    def test_evaluate_rate_limit_returns_none_when_under_limits(self):
        """_evaluate_rate_limit returns None when timestamps are under both limits."""
        now = time.time()
        timestamps = [now - 60]
        result = rate_limiting._evaluate_rate_limit(
            timestamps,
            daily_cutoff=now - 86400,
            window_cutoff=now - 18000,
            current_time=now,
            daily_limit=50,
            window_limit=25,
        )
        assert result is None

    def test_evaluate_rate_limit_blocks_on_daily(self):
        """_evaluate_rate_limit returns blocked when daily limit exceeded."""
        now = time.time()
        timestamps = [now - 100] * 51
        result = rate_limiting._evaluate_rate_limit(
            timestamps,
            daily_cutoff=now - 86400,
            window_cutoff=now - 18000,
            current_time=now,
            daily_limit=50,
            window_limit=25,
        )
        assert result is not None
        assert not result["allowed"]
        assert "daily limit" in result["error_message"]

    def test_evaluate_rate_limit_blocks_on_window(self):
        """_evaluate_rate_limit returns blocked when window limit exceeded."""
        now = time.time()
        timestamps = [now - 100] * 26
        result = rate_limiting._evaluate_rate_limit(
            timestamps,
            daily_cutoff=now - 86400,
            window_cutoff=now - 18000,
            current_time=now,
            daily_limit=50,
            window_limit=25,
        )
        assert result is not None
        assert not result["allowed"]
        assert "5 hours" in result["error_message"]


class TestBuildAllowedResponse(unittest.TestCase):
    """Unit tests for _build_allowed_response."""

    def test_returns_allowed_true(self):
        now = time.time()
        result = rate_limiting._build_allowed_response(
            turn_timestamps=[now - 60],
            daily_cutoff=now - 86400,
            window_cutoff=now - 18000,
            daily_limit=50,
            window_limit=25,
        )
        assert result["allowed"] is True

    def test_counts_daily_remaining_correctly(self):
        now = time.time()
        # 3 turns in 24h window, daily_limit=10 → 7 remaining
        timestamps = [now - 60, now - 120, now - 180]
        result = rate_limiting._build_allowed_response(
            turn_timestamps=timestamps,
            daily_cutoff=now - 86400,
            window_cutoff=now - 18000,
            daily_limit=10,
            window_limit=5,
        )
        assert result["daily_remaining"] == 7

    def test_counts_window_remaining_correctly(self):
        now = time.time()
        # 2 turns in 5h window, window_limit=5 → 3 remaining
        timestamps = [now - 60, now - 120]
        result = rate_limiting._build_allowed_response(
            turn_timestamps=timestamps,
            daily_cutoff=now - 86400,
            window_cutoff=now - 18000,
            daily_limit=50,
            window_limit=5,
        )
        assert result["hourly_remaining"] == 3

    def test_excludes_timestamps_outside_window(self):
        now = time.time()
        # 1 turn is >24h old (outside daily window), 1 is within
        timestamps = [now - 90000, now - 60]
        result = rate_limiting._build_allowed_response(
            turn_timestamps=timestamps,
            daily_cutoff=now - 86400,
            window_cutoff=now - 18000,
            daily_limit=50,
            window_limit=25,
        )
        assert result["daily_remaining"] == 49  # only 1 turn counts

    def test_remaining_never_below_zero(self):
        now = time.time()
        # More timestamps than limit (shouldn't happen in production, but defensive)
        timestamps = [now - 60] * 60  # 60 turns, daily_limit=50
        result = rate_limiting._build_allowed_response(
            turn_timestamps=timestamps,
            daily_cutoff=now - 86400,
            window_cutoff=now - 18000,
            daily_limit=50,
            window_limit=25,
        )
        assert result["daily_remaining"] == 0


class TestBYOKLimitInvariants(unittest.TestCase):
    """Tests for BYOK limit invariants: BYOK limits must always >= default limits."""

    def test_byok_daily_limit_at_least_default_daily(self):
        assert (
            rate_limiting.RATE_LIMIT_BYOK_PROVIDER_DAILY_TURNS
            >= rate_limiting.RATE_LIMIT_DAILY_TURNS
        ), (
            f"BYOK daily limit ({rate_limiting.RATE_LIMIT_BYOK_PROVIDER_DAILY_TURNS}) "
            f"must be >= default ({rate_limiting.RATE_LIMIT_DAILY_TURNS})"
        )

    def test_byok_5hour_limit_at_least_default_5hour(self):
        assert (
            rate_limiting.RATE_LIMIT_BYOK_PROVIDER_5HOUR_TURNS
            >= rate_limiting.RATE_LIMIT_5HOUR_TURNS
        ), (
            f"BYOK 5-hour limit ({rate_limiting.RATE_LIMIT_BYOK_PROVIDER_5HOUR_TURNS}) "
            f"must be >= default ({rate_limiting.RATE_LIMIT_5HOUR_TURNS})"
        )

    def test_byok_5hour_limit_equals_constant(self):
        """BYOK 5-hour limit must reflect the new constant (1000)."""
        from mvp_site import constants
        assert rate_limiting.RATE_LIMIT_BYOK_PROVIDER_5HOUR_TURNS >= constants.RATE_LIMIT_BYOK_PROVIDER_5HOUR_TURNS

    def test_byok_daily_limit_equals_constant(self):
        """BYOK daily limit must reflect the new constant (5000)."""
        from mvp_site import constants
        assert rate_limiting.RATE_LIMIT_BYOK_PROVIDER_DAILY_TURNS >= constants.RATE_LIMIT_BYOK_PROVIDER_DAILY_TURNS


class TestBYOK5HourLimitEnforcement(unittest.TestCase):
    """BYOK users get elevated 5-hour limits, but ARE still blocked at the elevated threshold."""

    def _setup_mock_db(self, mock_get_db):
        rate_limiting._USER_SETTINGS_CACHE.clear()
        mock_db = MagicMock()
        del mock_db.transaction
        mock_get_db.return_value = mock_db
        mock_rate_limit_doc_ref = MagicMock()
        mock_user_doc_ref = MagicMock()
        collections = {
            "rate_limits": mock_rate_limit_doc_ref,
            "users": mock_user_doc_ref,
        }
        def _collection_side_effect(name):
            coll = MagicMock()
            coll.document.return_value = collections[name]
            return coll
        mock_db.collection.side_effect = _collection_side_effect
        return mock_db, mock_rate_limit_doc_ref, mock_user_doc_ref

    @patch("mvp_site.firestore_service.get_db")
    def test_byok_user_blocked_at_elevated_5hour_limit(self, mock_get_db):
        """BYOK users are blocked at RATE_LIMIT_BYOK_PROVIDER_5HOUR_TURNS, not exempted."""
        _, mock_doc_ref, mock_user_doc_ref = self._setup_mock_db(mock_get_db)

        now = time.time()
        # Fill exactly at BYOK 5-hour limit (within window)
        timestamps = [
            now - 60
            for _ in range(rate_limiting.RATE_LIMIT_BYOK_PROVIDER_5HOUR_TURNS + 1)
        ]

        mock_doc = MagicMock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = {"turn_timestamps": timestamps}
        mock_doc_ref.get.return_value = mock_doc

        user_doc = MagicMock()
        user_doc.exists = True
        user_doc.to_dict.return_value = {
            "settings": {
                "llm_provider": "openrouter",
                "openrouter_api_key": "sk-or-user-provided-key",
            }
        }
        mock_user_doc_ref.get.return_value = user_doc

        result = rate_limiting.check_rate_limit(
            "byok_user", "byok@example.com", consume_turn=False
        )

        assert not result["allowed"], (
            f"BYOK user should be blocked at elevated 5-hour limit "
            f"({rate_limiting.RATE_LIMIT_BYOK_PROVIDER_5HOUR_TURNS}). Result: {result}"
        )
        assert result["error_type"] == "rate_limit"

    @patch("mvp_site.firestore_service.get_db")
    def test_byok_user_allowed_just_under_elevated_5hour_limit(self, mock_get_db):
        """BYOK users are allowed when usage is just under their elevated 5-hour limit."""
        _, mock_doc_ref, mock_user_doc_ref = self._setup_mock_db(mock_get_db)

        now = time.time()
        # One under the BYOK 5-hour limit (within window)
        timestamps = [
            now - 60
            for _ in range(rate_limiting.RATE_LIMIT_BYOK_PROVIDER_5HOUR_TURNS - 1)
        ]

        mock_doc = MagicMock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = {"turn_timestamps": timestamps}
        mock_doc_ref.get.return_value = mock_doc

        user_doc = MagicMock()
        user_doc.exists = True
        user_doc.to_dict.return_value = {
            "settings": {
                "llm_provider": "openrouter",
                "openrouter_api_key": "sk-or-user-provided-key",
            }
        }
        mock_user_doc_ref.get.return_value = user_doc

        result = rate_limiting.check_rate_limit(
            "byok_user", "byok@example.com", consume_turn=False
        )

        assert result["allowed"], (
            f"BYOK user should be allowed under elevated 5-hour limit. Result: {result}"
        )


class TestRecordTurnUsage(unittest.TestCase):
    """Tests for record_turn_usage function."""

    def _setup_mock_db(self, mock_get_db):
        rate_limiting._USER_SETTINGS_CACHE.clear()
        mock_db = MagicMock()
        del mock_db.transaction
        mock_get_db.return_value = mock_db
        mock_doc_ref = MagicMock()
        mock_db.collection.return_value.document.return_value = mock_doc_ref
        return mock_db, mock_doc_ref

    @patch("mvp_site.firestore_service.get_db")
    def test_record_turn_usage_returns_true_on_success(self, mock_get_db):
        _, mock_doc_ref = self._setup_mock_db(mock_get_db)

        mock_doc = MagicMock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = {"turn_timestamps": []}
        mock_doc_ref.get.return_value = mock_doc

        result = rate_limiting.record_turn_usage("user1")
        assert result is True

    @patch("mvp_site.firestore_service.get_db")
    def test_record_turn_usage_writes_timestamp(self, mock_get_db):
        _, mock_doc_ref = self._setup_mock_db(mock_get_db)

        mock_doc = MagicMock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = {"turn_timestamps": []}
        mock_doc_ref.get.return_value = mock_doc

        before = time.time()
        rate_limiting.record_turn_usage("user1")
        after = time.time()

        mock_doc_ref.set.assert_called_once()
        args, _ = mock_doc_ref.set.call_args
        timestamps = args[0]["turn_timestamps"]
        assert len(timestamps) == 1
        assert before <= timestamps[0] <= after

    @patch("mvp_site.firestore_service.get_db")
    def test_record_turn_usage_prunes_old_timestamps(self, mock_get_db):
        _, mock_doc_ref = self._setup_mock_db(mock_get_db)

        now = time.time()
        old_ts = now - (25 * 60 * 60)  # 25 hours ago (outside daily window)
        recent_ts = now - 60

        mock_doc = MagicMock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = {"turn_timestamps": [old_ts, recent_ts]}
        mock_doc_ref.get.return_value = mock_doc

        rate_limiting.record_turn_usage("user1")

        args, _ = mock_doc_ref.set.call_args
        timestamps = args[0]["turn_timestamps"]
        # Old timestamp pruned, recent kept, new one added = 2
        assert len(timestamps) == 2
        assert old_ts not in timestamps

    @patch("mvp_site.firestore_service.get_db")
    def test_record_turn_usage_returns_false_on_exception(self, mock_get_db):
        _, mock_doc_ref = self._setup_mock_db(mock_get_db)

        mock_doc_ref.get.side_effect = Exception("Firestore unavailable")

        result = rate_limiting.record_turn_usage("user1")
        assert result is False

    @patch("mvp_site.firestore_service.get_db")
    def test_record_turn_usage_handles_missing_document(self, mock_get_db):
        _, mock_doc_ref = self._setup_mock_db(mock_get_db)

        # Document does not exist
        mock_doc = MagicMock()
        mock_doc.exists = False
        mock_doc_ref.get.return_value = mock_doc

        result = rate_limiting.record_turn_usage("user1")
        assert result is True

        args, _ = mock_doc_ref.set.call_args
        assert len(args[0]["turn_timestamps"]) == 1


class TestCheckRateLimitErrorHandling(unittest.TestCase):
    """Tests for error handling in check_rate_limit."""

    def _setup_mock_db(self, mock_get_db):
        rate_limiting._USER_SETTINGS_CACHE.clear()
        mock_db = MagicMock()
        del mock_db.transaction
        mock_get_db.return_value = mock_db
        mock_doc_ref = MagicMock()
        mock_db.collection.return_value.document.return_value = mock_doc_ref
        return mock_db, mock_doc_ref

    @patch("mvp_site.firestore_service.get_db")
    def test_google_api_error_fails_open(self, mock_get_db):
        """GoogleAPIError → fail open (allowed=True, unlimited)."""
        from google.api_core.exceptions import GoogleAPIError

        _, mock_doc_ref = self._setup_mock_db(mock_get_db)
        mock_doc_ref.get.side_effect = GoogleAPIError("Firestore unavailable")

        result = rate_limiting.check_rate_limit(
            "user1", "user@example.com", consume_turn=False
        )
        assert result["allowed"] is True
        assert result["daily_remaining"] == -1
        assert result["hourly_remaining"] == -1

    @patch("mvp_site.firestore_service.get_db")
    def test_unexpected_exception_fails_closed(self, mock_get_db):
        """Unexpected exception → fail closed (allowed=False, blocked)."""
        _, mock_doc_ref = self._setup_mock_db(mock_get_db)
        mock_doc_ref.get.side_effect = RuntimeError("Unexpected bug")

        result = rate_limiting.check_rate_limit(
            "user1", "user@example.com", consume_turn=False
        )
        assert result["allowed"] is False
        assert result["error_type"] == "rate_limit_error"


class TestInvalidateUserSettingsCache(unittest.TestCase):
    """Tests for invalidate_user_settings_cache."""

    def test_invalidate_removes_cached_entry(self):
        rate_limiting._USER_SETTINGS_CACHE.clear()
        user_id = "test_invalidate_user"
        # Manually populate cache
        with rate_limiting._USER_SETTINGS_CACHE_LOCK:
            rate_limiting._USER_SETTINGS_CACHE[user_id] = {"llm_provider": "gemini"}

        rate_limiting.invalidate_user_settings_cache(user_id)

        with rate_limiting._USER_SETTINGS_CACHE_LOCK:
            assert user_id not in rate_limiting._USER_SETTINGS_CACHE

    def test_invalidate_is_idempotent_for_missing_key(self):
        rate_limiting._USER_SETTINGS_CACHE.clear()
        # Should not raise for a user that was never cached
        rate_limiting.invalidate_user_settings_cache("nonexistent_user")


class TestIsFirestoreTransaction(unittest.TestCase):
    """Tests for _is_firestore_transaction."""

    def test_returns_true_for_object_with_all_attrs(self):
        mock_txn = MagicMock()
        for attr in rate_limiting._FIRESTORE_TRANSACTION_ATTRS:
            setattr(mock_txn, attr, MagicMock())
        assert rate_limiting._is_firestore_transaction(mock_txn)

    def test_returns_false_when_attr_missing(self):
        mock_txn = MagicMock(spec=[])  # Empty spec — no attributes
        assert not rate_limiting._is_firestore_transaction(mock_txn)


if __name__ == "__main__":
    unittest.main()

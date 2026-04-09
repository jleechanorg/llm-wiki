"""Unit tests for testing_ui DEFAULT_TEST_EMAIL / jleechantest default."""

from unittest.mock import patch

from testing_ui.config import DEFAULT_TEST_EMAIL
from testing_ui.lib.browser_test_base import BrowserTestBase
from testing_ui.lib.byok_browser_base import ByokBrowserTestBase


def test_browser_test_base_uses_jleechantest_when_env_unset():
    """BrowserTestBase defaults to jleechantest@gmail.com when TEST_USER_EMAIL not set."""
    with patch.dict("os.environ", {}, clear=False):
        # Remove TEST_USER_EMAIL if present
        import os

        os.environ.pop("TEST_USER_EMAIL", None)
        base = BrowserTestBase(testing_auth_bypass=True)
        assert base.test_user_email == DEFAULT_TEST_EMAIL
        assert base.test_user_email == "jleechantest@gmail.com"


def test_browser_test_base_respects_test_user_email_env():
    """BrowserTestBase uses TEST_USER_EMAIL when set."""
    with patch.dict("os.environ", {"TEST_USER_EMAIL": "custom@test.local"}):
        base = BrowserTestBase(testing_auth_bypass=True)
        assert base.test_user_email == "custom@test.local"


def test_byok_browser_base_uses_jleechantest_when_env_unset():
    """ByokBrowserTestBase defaults to jleechantest@gmail.com when BYOK_TEST_USER_EMAIL not set."""
    with patch.dict("os.environ", {}, clear=False):
        import os

        os.environ.pop("BYOK_TEST_USER_EMAIL", None)
        base = ByokBrowserTestBase(testing_auth_bypass=True)
        assert base.test_user_email == DEFAULT_TEST_EMAIL
        assert base.test_user_email == "jleechantest@gmail.com"


def test_byok_browser_base_respects_byok_test_user_email_env():
    """ByokBrowserTestBase uses BYOK_TEST_USER_EMAIL when set."""
    with patch.dict("os.environ", {"BYOK_TEST_USER_EMAIL": "byok@test.local"}):
        base = ByokBrowserTestBase(testing_auth_bypass=True)
        assert base.test_user_email == "byok@test.local"

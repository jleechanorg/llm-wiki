"""
Common test utilities shared across test files.
"""

import unittest


def has_firebase_credentials():
    """Check if Firebase credentials are available.

    Note: End2end tests use complete mocking and don't require real credentials.
    This function returns False to ensure tests use mocked services.
    """
    # End2end tests should always use mocked services, not real credentials
    return False


class TestCommon(unittest.TestCase):
    """Test cases for common utilities."""

    def test_firebase_credentials_check(self):
        """Test that Firebase credentials check returns False for mocked tests."""
        # Ensures end2end tests use mocked services, not real Firebase
        assert not has_firebase_credentials(), (
            "Firebase credentials should return False in test environment"
        )


if __name__ == "__main__":
    unittest.main()

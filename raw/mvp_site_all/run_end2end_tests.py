#!/usr/bin/env python3
"""
Runner script for end-to-end integration tests.
Run this from the project root with the virtual environment activated.

Usage:
    python mvp_site/tests/run_end2end_tests.py
"""

import sys
import unittest
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TEST_DIR.parents[2]

# Add the project root to the path (same as test files)
sys.path.insert(0, str(PROJECT_ROOT))


def run_tests():
    """Run all end-to-end integration tests."""

    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(TEST_DIR), pattern="test_*.py")

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return exit code based on test results
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    print("Running End-to-End Integration Tests")
    print("=" * 60)
    print("These tests mock only external services (Firestore & Gemini)")
    print("and test the full application flow through all layers.")
    print("=" * 60)

    exit_code = run_tests()

    if exit_code == 0:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed.")

    sys.exit(exit_code)

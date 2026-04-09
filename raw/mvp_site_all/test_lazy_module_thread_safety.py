"""Tests for _LazyModule thread safety."""

import sys
import threading
import unittest
from types import ModuleType
from unittest.mock import patch

from mvp_site import _LazyModule


class TestLazyModuleThreadSafety(unittest.TestCase):
    """Test that _LazyModule handles concurrent access safely."""

    def setUp(self):
        """Set up test fixtures."""
        # Clean up any test modules from previous runs
        test_modules = [k for k in sys.modules if k.startswith("_test_lazy")]
        for mod in test_modules:
            del sys.modules[mod]

    def test_concurrent_loading_does_not_double_import(self):
        """
        TDD RED: Concurrent threads accessing _LazyModule should not cause double imports.

        Race condition scenario:
        1. Thread A checks _real_module is None
        2. Thread B checks _real_module is None (before A finishes)
        3. Both threads call importlib.import_module()
        4. Module imported twice (side effects, performance issue)

        Expected: Only ONE import should occur, protected by lock.
        """
        # Track how many times the module is actually imported
        import_count = {"count": 0}
        import_lock = threading.Lock()

        def mock_import(module_path):
            """Mock importlib.import_module to count imports."""
            with import_lock:
                import_count["count"] += 1
            # Simulate slow import to increase race window
            threading.Event().wait(0.01)
            # Return a mock module
            return ModuleType(module_path)

        # Create a LazyModule for testing
        lazy_mod = _LazyModule("_test_lazy_concurrent", "mvp_site.constants")

        # Patch import_module to track calls
        with patch("importlib.import_module", side_effect=mock_import):
            # Launch multiple threads that all try to access the lazy module
            num_threads = 10
            threads = []
            results = [None] * num_threads

            def access_lazy_module(index):
                """Thread worker: access the lazy module."""
                try:
                    # Trigger lazy loading by accessing an attribute
                    _ = lazy_mod._load_real_module()
                    results[index] = "success"
                except (ModuleNotFoundError, ImportError) as e:
                    results[index] = f"error: {e}"

            # Start all threads
            for i in range(num_threads):
                t = threading.Thread(target=access_lazy_module, args=(i,))
                threads.append(t)
                t.start()

            # Wait for all threads to complete
            for t in threads:
                t.join(timeout=2.0)

            # ASSERTION: Module should be imported exactly ONCE despite 10 threads
            assert import_count["count"] == 1, (
                f"Module was imported {import_count['count']} times, expected 1. "
                "This indicates a race condition in _LazyModule._load_real_module()."
            )

            # All threads should succeed
            assert results.count("success") == num_threads, (
                f"Some threads failed: {results}"
            )

    def test_load_real_module_is_idempotent(self):
        """Multiple calls to _load_real_module should return the same object."""
        lazy_mod = _LazyModule("_test_lazy_idempotent", "mvp_site.constants")

        # Load the module multiple times
        result1 = lazy_mod._load_real_module()
        result2 = lazy_mod._load_real_module()
        result3 = lazy_mod._load_real_module()

        # All should be the exact same object (not just equal, but identical)
        assert result1 is result2
        assert result2 is result3


if __name__ == "__main__":
    unittest.main()

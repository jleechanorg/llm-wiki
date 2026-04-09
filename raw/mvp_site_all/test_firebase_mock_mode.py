"""
Test that Firebase initialization is skipped when MOCK_SERVICES_MODE is set.

This is a simplified test that verifies both main.py and world_logic.py
properly check for MOCK_SERVICES_MODE environment variable.
"""

import importlib
import os
import sys
import threading
import time
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from mvp_site import firestore_service

# Import proper fakes library


class TestFirebaseMockMode(unittest.TestCase):
    """Test Firebase initialization with MOCK_SERVICES_MODE."""

    def test_warmup_firestore_query_does_not_block_startup_path(self):
        """Warmup should not synchronously block on Firestore query latency."""
        original_semantic = os.environ.get("ENABLE_SEMANTIC_ROUTING")

        try:
            os.environ["ENABLE_SEMANTIC_ROUTING"] = "false"

            from mvp_site import main as main_module

            def _slow_query(*args, **kwargs):
                del args, kwargs
                time.sleep(0.35)
                return [], None, None

            spawned_threads: list[threading.Thread] = []
            base_thread_class = main_module.threading.Thread

            class _TrackingThread(base_thread_class):
                def start(self, *args, **kwargs):
                    spawned_threads.append(self)
                    return super().start(*args, **kwargs)

            with (
                patch.object(main_module.threading, "Thread", _TrackingThread),
                patch.object(main_module, "_warm_lazy_module_attribute", return_value=True),
                patch.object(main_module.firestore_service, "get_db", return_value=MagicMock()),
                patch.object(
                    main_module.firestore_service,
                    "get_campaigns_for_user",
                    side_effect=_slow_query,
                ),
                patch.object(main_module, "warm_streaming_lazy_dependencies", return_value={}),
            ):
                start = time.perf_counter()
                main_module._warm_startup_lazy_dependencies()
                elapsed = time.perf_counter() - start

                for warmup_thread in spawned_threads:
                    warmup_thread.join(timeout=1.0)
                    self.assertFalse(
                        warmup_thread.is_alive(),
                        "Warmup test thread did not finish before patch teardown.",
                    )

            self.assertLess(
                elapsed,
                0.25,
                "Warmup path must not block startup on Firestore query latency.",
            )

        finally:
            if original_semantic is not None:
                os.environ["ENABLE_SEMANTIC_ROUTING"] = original_semantic
            elif "ENABLE_SEMANTIC_ROUTING" in os.environ:
                del os.environ["ENABLE_SEMANTIC_ROUTING"]

    def test_create_app_skips_warmup_in_mock_mode(self):
        """Mock mode should skip startup lazy warmup side effects."""
        original_mock = os.environ.get("MOCK_SERVICES_MODE")
        original_semantic = os.environ.get("ENABLE_SEMANTIC_ROUTING")
        original_disable_warmup = os.environ.get("DISABLE_STARTUP_WARMUP")

        try:
            os.environ["MOCK_SERVICES_MODE"] = "true"
            os.environ["ENABLE_SEMANTIC_ROUTING"] = "false"
            if "DISABLE_STARTUP_WARMUP" in os.environ:
                del os.environ["DISABLE_STARTUP_WARMUP"]

            from mvp_site import main as main_module

            with (
                patch.object(main_module, "_ensure_async_infrastructure"),
                patch.object(main_module, "intent_classifier"),
                patch.object(main_module, "_warm_startup_lazy_dependencies") as mock_warmup,
            ):
                app = main_module.create_app()
                self.assertIsNotNone(app)
                mock_warmup.assert_not_called()

        finally:
            if original_mock is not None:
                os.environ["MOCK_SERVICES_MODE"] = original_mock
            elif "MOCK_SERVICES_MODE" in os.environ:
                del os.environ["MOCK_SERVICES_MODE"]

            if original_semantic is not None:
                os.environ["ENABLE_SEMANTIC_ROUTING"] = original_semantic
            elif "ENABLE_SEMANTIC_ROUTING" in os.environ:
                del os.environ["ENABLE_SEMANTIC_ROUTING"]

            if original_disable_warmup is not None:
                os.environ["DISABLE_STARTUP_WARMUP"] = original_disable_warmup
            elif "DISABLE_STARTUP_WARMUP" in os.environ:
                del os.environ["DISABLE_STARTUP_WARMUP"]

    def test_create_app_skips_warmup_when_explicitly_disabled(self):
        """Explicit env flag should disable startup warmup."""
        original_mock = os.environ.get("MOCK_SERVICES_MODE")
        original_semantic = os.environ.get("ENABLE_SEMANTIC_ROUTING")
        original_disable_warmup = os.environ.get("DISABLE_STARTUP_WARMUP")

        try:
            if "MOCK_SERVICES_MODE" in os.environ:
                del os.environ["MOCK_SERVICES_MODE"]
            os.environ["ENABLE_SEMANTIC_ROUTING"] = "false"
            os.environ["DISABLE_STARTUP_WARMUP"] = "true"

            from mvp_site import main as main_module

            mock_firebase = MagicMock()
            mock_firebase.get_app = MagicMock(return_value=MagicMock(name="app"))
            mock_credentials = MagicMock()

            with (
                patch.object(main_module, "_ensure_async_infrastructure"),
                patch.object(main_module, "intent_classifier"),
                patch.object(main_module, "firebase_admin", mock_firebase),
                patch.object(main_module, "credentials", mock_credentials),
                patch.object(main_module, "_warm_startup_lazy_dependencies") as mock_warmup,
            ):
                app = main_module.create_app()
                self.assertIsNotNone(app)
                mock_warmup.assert_not_called()

        finally:
            if original_mock is not None:
                os.environ["MOCK_SERVICES_MODE"] = original_mock
            elif "MOCK_SERVICES_MODE" in os.environ:
                del os.environ["MOCK_SERVICES_MODE"]

            if original_semantic is not None:
                os.environ["ENABLE_SEMANTIC_ROUTING"] = original_semantic
            elif "ENABLE_SEMANTIC_ROUTING" in os.environ:
                del os.environ["ENABLE_SEMANTIC_ROUTING"]

            if original_disable_warmup is not None:
                os.environ["DISABLE_STARTUP_WARMUP"] = original_disable_warmup
            elif "DISABLE_STARTUP_WARMUP" in os.environ:
                del os.environ["DISABLE_STARTUP_WARMUP"]

    def test_create_app_handles_invalid_classifier_timeout(self):
        """Invalid classifier timeout env should not crash startup."""
        original_mock = os.environ.get("MOCK_SERVICES_MODE")
        original_semantic = os.environ.get("ENABLE_SEMANTIC_ROUTING")
        original_disable_warmup = os.environ.get("DISABLE_STARTUP_WARMUP")
        original_timeout = os.environ.get("INTENT_CLASSIFIER_WARMUP_TIMEOUT_SECONDS")

        try:
            if "MOCK_SERVICES_MODE" in os.environ:
                del os.environ["MOCK_SERVICES_MODE"]
            os.environ["ENABLE_SEMANTIC_ROUTING"] = "true"
            os.environ["INTENT_CLASSIFIER_WARMUP_TIMEOUT_SECONDS"] = "not-a-number"
            if "DISABLE_STARTUP_WARMUP" in os.environ:
                del os.environ["DISABLE_STARTUP_WARMUP"]

            from mvp_site import main as main_module

            fake_classifier = SimpleNamespace(ready=True)
            mock_firebase = MagicMock()
            mock_firebase.get_app = MagicMock(return_value=MagicMock(name="app"))
            mock_credentials = MagicMock()

            with (
                patch.object(main_module, "_ensure_async_infrastructure"),
                patch.object(main_module.intent_classifier, "initialize"),
                patch.object(main_module, "firebase_admin", mock_firebase),
                patch.object(main_module, "credentials", mock_credentials),
                patch.object(
                    main_module.intent_classifier.LocalIntentClassifier,
                    "get_instance",
                    return_value=fake_classifier,
                ),
                patch.object(main_module.firestore_service, "get_db"),
                patch.object(main_module, "_start_firestore_runtime_warmup", return_value=True),
                patch.object(main_module, "warm_streaming_lazy_dependencies", return_value={}),
                patch.object(main_module.logging_util, "warning") as mock_warning,
                patch(
                    "mvp_site.service_account_loader.get_service_account_credentials",
                    side_effect=Exception("no creds"),
                ),
            ):
                app = main_module.create_app()
                self.assertIsNotNone(app)
                self.assertTrue(
                    any(
                        call.args
                        and "Invalid INTENT_CLASSIFIER_WARMUP_TIMEOUT_SECONDS" in str(call.args[0])
                        for call in mock_warning.call_args_list
                    ),
                    "Invalid timeout path should emit a warning and use default.",
                )

        finally:
            if original_mock is not None:
                os.environ["MOCK_SERVICES_MODE"] = original_mock
            elif "MOCK_SERVICES_MODE" in os.environ:
                del os.environ["MOCK_SERVICES_MODE"]

            if original_semantic is not None:
                os.environ["ENABLE_SEMANTIC_ROUTING"] = original_semantic
            elif "ENABLE_SEMANTIC_ROUTING" in os.environ:
                del os.environ["ENABLE_SEMANTIC_ROUTING"]

            if original_disable_warmup is not None:
                os.environ["DISABLE_STARTUP_WARMUP"] = original_disable_warmup
            elif "DISABLE_STARTUP_WARMUP" in os.environ:
                del os.environ["DISABLE_STARTUP_WARMUP"]

            if original_timeout is not None:
                os.environ["INTENT_CLASSIFIER_WARMUP_TIMEOUT_SECONDS"] = original_timeout
            elif "INTENT_CLASSIFIER_WARMUP_TIMEOUT_SECONDS" in os.environ:
                del os.environ["INTENT_CLASSIFIER_WARMUP_TIMEOUT_SECONDS"]

    def test_create_app_skips_classifier_readiness_when_semantic_routing_disabled(self):
        """Semantic routing disable should skip classifier readiness warmup path."""
        original_mock = os.environ.get("MOCK_SERVICES_MODE")
        original_semantic = os.environ.get("ENABLE_SEMANTIC_ROUTING")

        try:
            if "MOCK_SERVICES_MODE" in os.environ:
                del os.environ["MOCK_SERVICES_MODE"]
            os.environ["ENABLE_SEMANTIC_ROUTING"] = "false"

            from mvp_site import main as main_module
            mock_firebase = MagicMock()
            mock_firebase.get_app = MagicMock(return_value=MagicMock(name="app"))
            mock_credentials = MagicMock()

            with (
                patch.object(main_module, "_ensure_async_infrastructure"),
                patch.object(main_module, "firebase_admin", mock_firebase),
                patch.object(main_module, "credentials", mock_credentials),
                patch.object(main_module, "_start_firestore_runtime_warmup", return_value=True),
                patch.object(main_module, "warm_streaming_lazy_dependencies", return_value={}),
                patch.object(
                    main_module.intent_classifier.LocalIntentClassifier,
                    "get_instance",
                    side_effect=AssertionError("Classifier get_instance should not be called."),
                ) as mock_get_instance,
                patch(
                    "mvp_site.service_account_loader.get_service_account_credentials",
                    side_effect=Exception("no creds"),
                ),
            ):
                app = main_module.create_app()
                self.assertIsNotNone(app)
                mock_get_instance.assert_not_called()

        finally:
            if original_mock is not None:
                os.environ["MOCK_SERVICES_MODE"] = original_mock
            elif "MOCK_SERVICES_MODE" in os.environ:
                del os.environ["MOCK_SERVICES_MODE"]

            if original_semantic is not None:
                os.environ["ENABLE_SEMANTIC_ROUTING"] = original_semantic
            elif "ENABLE_SEMANTIC_ROUTING" in os.environ:
                del os.environ["ENABLE_SEMANTIC_ROUTING"]

    def test_create_app_initializes_firebase_before_warmup(self):
        """Non-mock startup should initialize Firebase before warmup runs."""
        original_mock = os.environ.get("MOCK_SERVICES_MODE")
        original_semantic = os.environ.get("ENABLE_SEMANTIC_ROUTING")

        try:
            if "MOCK_SERVICES_MODE" in os.environ:
                del os.environ["MOCK_SERVICES_MODE"]
            os.environ["ENABLE_SEMANTIC_ROUTING"] = "false"

            from mvp_site import main as main_module

            events: list[str] = []
            mock_firebase = MagicMock()

            def _get_app_side_effect():
                events.append("firebase_get_app")
                raise ValueError("No Firebase app")

            def _initialize_app_side_effect(*args, **kwargs):
                del args, kwargs
                events.append("firebase_initialize_app")
                return MagicMock(name="firebase_app")

            mock_firebase.get_app = MagicMock(side_effect=_get_app_side_effect)
            mock_firebase.initialize_app = MagicMock(side_effect=_initialize_app_side_effect)

            mock_credentials = MagicMock()
            mock_credentials.ApplicationDefault.return_value = MagicMock(name="default")

            def _warmup_side_effect():
                events.append("warmup")

            with (
                patch.object(main_module, "_ensure_async_infrastructure"),
                patch.object(main_module, "firebase_admin", mock_firebase),
                patch.object(main_module, "credentials", mock_credentials),
                patch.object(main_module, "_warm_startup_lazy_dependencies", side_effect=_warmup_side_effect),
                patch.object(main_module, "intent_classifier"),
                patch(
                    "mvp_site.service_account_loader.get_service_account_credentials",
                    side_effect=Exception("no creds"),
                ),
            ):
                app = main_module.create_app()
                self.assertIsNotNone(app)

            self.assertIn("firebase_initialize_app", events)
            self.assertIn("warmup", events)
            self.assertLess(
                events.index("firebase_initialize_app"),
                events.index("warmup"),
                "Firebase must initialize before warmup touches Firestore dependencies.",
            )

        finally:
            if original_mock is not None:
                os.environ["MOCK_SERVICES_MODE"] = original_mock
            elif "MOCK_SERVICES_MODE" in os.environ:
                del os.environ["MOCK_SERVICES_MODE"]

            if original_semantic is not None:
                os.environ["ENABLE_SEMANTIC_ROUTING"] = original_semantic
            elif "ENABLE_SEMANTIC_ROUTING" in os.environ:
                del os.environ["ENABLE_SEMANTIC_ROUTING"]

    def test_main_skips_firebase_init_in_mock_mode(self):
        """
        Test that main.py skips Firebase initialization in MOCK_SERVICES_MODE.
        """
        original_testing = os.environ.get("TESTING_AUTH_BYPASS")
        original_mock = os.environ.get("MOCK_SERVICES_MODE")
        original_semantic = os.environ.get("ENABLE_SEMANTIC_ROUTING")

        try:
            os.environ["MOCK_SERVICES_MODE"] = "true"
            os.environ["ENABLE_SEMANTIC_ROUTING"] = "false"

            from mvp_site import main as main_module

            mock_firebase = MagicMock()
            mock_firebase.get_app = MagicMock(side_effect=ValueError("No Firebase app"))
            mock_firebase.initialize_app = MagicMock(return_value=MagicMock(name="app"))

            with (
                patch.object(main_module, "_ensure_async_infrastructure"),
                patch.object(main_module, "firebase_admin", mock_firebase),
                patch.object(main_module, "intent_classifier"),
                patch.object(main_module.logging_util, "info") as mock_info,
            ):
                app = main_module.create_app()
                self.assertIsNotNone(app)
                mock_firebase.initialize_app.assert_not_called()
                mock_info.assert_any_call(
                    "🔧 SEMANTIC_ROUTING_DISABLED: Skipping classifier initialization (ENABLE_SEMANTIC_ROUTING=false)"
                )

        finally:
            # Restore environment
            if original_testing is not None:
                os.environ["TESTING_AUTH_BYPASS"] = original_testing
            elif "TESTING_AUTH_BYPASS" in os.environ:
                del os.environ["TESTING_AUTH_BYPASS"]

            if original_mock is not None:
                os.environ["MOCK_SERVICES_MODE"] = original_mock
            elif "MOCK_SERVICES_MODE" in os.environ:
                del os.environ["MOCK_SERVICES_MODE"]

            if original_semantic is not None:
                os.environ["ENABLE_SEMANTIC_ROUTING"] = original_semantic
            elif "ENABLE_SEMANTIC_ROUTING" in os.environ:
                del os.environ["ENABLE_SEMANTIC_ROUTING"]

    def test_main_initializes_firebase_when_not_mock(self):
        """
        Test that main.py initializes Firebase when MOCK_SERVICES_MODE is not set.
        """
        original_mock = os.environ.get("MOCK_SERVICES_MODE")
        original_semantic = os.environ.get("ENABLE_SEMANTIC_ROUTING")

        try:
            if "MOCK_SERVICES_MODE" in os.environ:
                del os.environ["MOCK_SERVICES_MODE"]
            os.environ["ENABLE_SEMANTIC_ROUTING"] = "false"

            from mvp_site import main as main_module

            mock_firebase = MagicMock()
            mock_firebase.get_app = MagicMock(side_effect=ValueError("No Firebase app"))
            mock_firebase.initialize_app = MagicMock(return_value=MagicMock(name="app"))

            mock_credentials = MagicMock()
            mock_credentials.ApplicationDefault.return_value = MagicMock(name="default")

            with (
                patch.object(main_module, "_ensure_async_infrastructure"),
                patch.object(main_module, "firebase_admin", mock_firebase),
                patch.object(main_module, "credentials", mock_credentials),
                patch.object(main_module, "intent_classifier"),
                patch(
                    "mvp_site.service_account_loader.get_service_account_credentials",
                    side_effect=Exception("no creds"),
                ),
            ):
                app = main_module.create_app()
                self.assertIsNotNone(app)
                mock_firebase.initialize_app.assert_called()

        finally:
            if original_mock is not None:
                os.environ["MOCK_SERVICES_MODE"] = original_mock
            elif "MOCK_SERVICES_MODE" in os.environ:
                del os.environ["MOCK_SERVICES_MODE"]

            if original_semantic is not None:
                os.environ["ENABLE_SEMANTIC_ROUTING"] = original_semantic
            elif "ENABLE_SEMANTIC_ROUTING" in os.environ:
                del os.environ["ENABLE_SEMANTIC_ROUTING"]

    def test_world_logic_initializes_firebase_regardless_of_mock_mode(self):
        """
        Test that world_logic.py initializes Firebase regardless of MOCK_SERVICES_MODE (testing mode removed).
        """
        # Save original environment
        original_testing = os.environ.get("TESTING_AUTH_BYPASS")
        original_mock = os.environ.get("MOCK_SERVICES_MODE")

        try:
            # Set up CI-like environment
            if "TESTING_AUTH_BYPASS" in os.environ:
                del os.environ["TESTING_AUTH_BYPASS"]
            os.environ["MOCK_SERVICES_MODE"] = "true"

            # Mock firebase_admin to control init path
            mock_firebase = MagicMock()
            mock_firebase.auth = MagicMock()
            mock_firebase.get_app = MagicMock(side_effect=ValueError("No Firebase app"))
            mock_firebase.initialize_app = MagicMock(return_value=MagicMock(name="app"))

            # Mock logging_util with proper methods
            mock_logging_util = MagicMock()
            mock_logging_util.LoggingUtil.get_log_file.return_value = "/tmp/test.log"
            mock_logging_util.info = MagicMock()
            mock_logging_util.error = MagicMock()

            mocks = {
                "firebase_admin": mock_firebase,
                "logging_util": mock_logging_util,
                "mvp_site.logging_util": mock_logging_util,
                # Fallbacks for package imports:
                "constants": MagicMock(),
                "mvp_site.constants": MagicMock(),
                "custom_types": MagicMock(),
                "mvp_site.custom_types": MagicMock(),
                "document_generator": MagicMock(),
                "mvp_site.document_generator": MagicMock(),
                "structured_fields_utils": MagicMock(),
                "mvp_site.structured_fields_utils": MagicMock(),
                "debug_hybrid_system": MagicMock(),
                "mvp_site.debug_hybrid_system": MagicMock(),
                "firestore_service": MagicMock(),
                "mvp_site.firestore_service": MagicMock(),
                "llm_service": MagicMock(),
                "mvp_site.llm_service": MagicMock(),
                "game_state": MagicMock(),
                "mvp_site.game_state": MagicMock(),
            }

            # firebase_utils removed - Firebase now always initializes

            with patch.dict("sys.modules", mocks):
                # Clear any cached imports
                for mod in ("mvp_site.world_logic", "world_logic"):
                    if mod in sys.modules:
                        del sys.modules[mod]
                importlib.invalidate_caches()

                # Import world_logic - should initialize Firebase regardless of MOCK_SERVICES_MODE
                importlib.import_module("mvp_site.world_logic")

                # Verify Firebase WAS initialized (testing mode removed)
                # May be called multiple times if multiple modules initialize Firebase
                mock_firebase.initialize_app.assert_called()

        finally:
            # Restore environment
            if original_testing is not None:
                os.environ["TESTING_AUTH_BYPASS"] = original_testing
            elif "TESTING_AUTH_BYPASS" in os.environ:
                del os.environ["TESTING_AUTH_BYPASS"]

            if original_mock is not None:
                os.environ["MOCK_SERVICES_MODE"] = original_mock
            elif "MOCK_SERVICES_MODE" in os.environ:
                del os.environ["MOCK_SERVICES_MODE"]

            # Clean up any test imports from sys.modules to avoid interference
            if "world_logic" in sys.modules:
                del sys.modules["world_logic"]

    def test_get_campaigns_for_user_uses_mock_select_without_crash(self):
        """Regression: ensure mock Firestore query supports .select in campaign listing."""
        original_testing = os.environ.get("TESTING_AUTH_BYPASS")
        original_mock = os.environ.get("MOCK_SERVICES_MODE")

        try:
            if "TESTING_AUTH_BYPASS" in os.environ:
                del os.environ["TESTING_AUTH_BYPASS"]
            os.environ["MOCK_SERVICES_MODE"] = "true"

            firestore_service.reset_mock_firestore()
            db = firestore_service.get_db()
            campaigns_ref = (
                db.collection("users")
                .document("test-user")
                .collection("campaigns")
            )
            campaigns_ref.add(
                {
                    "title": "First Campaign",
                    "created_at": "2026-01-01T10:00:00Z",
                    "last_played": "2026-01-02T10:00:00Z",
                    "prompt": "prompt one",
                    "initial_prompt": "initial one",
                    "secret": "internal",
                }
            )
            campaigns_ref.add(
                {
                    "title": "Second Campaign",
                    "created_at": "2026-01-03T10:00:00Z",
                    "last_played": "2026-01-04T10:00:00Z",
                    "prompt": "prompt two",
                    "initial_prompt": "initial two",
                    "secret": "internal",
                }
            )

            first_page, next_cursor, _ = firestore_service.get_campaigns_for_user(
                "test-user", limit=1, sort_by="last_played"
            )

            self.assertEqual(len(first_page), 1)
            self.assertIn("title", first_page[0])
            self.assertNotIn("prompt", first_page[0])  # prompt removed for payload optimization
            self.assertIn("initial_prompt", first_page[0])
            self.assertNotIn("secret", first_page[0])
            self.assertIsNotNone(next_cursor)

            second_page, _, _ = firestore_service.get_campaigns_for_user(
                "test-user", limit=1, sort_by="last_played", start_after=next_cursor
            )

            self.assertEqual(len(second_page), 1)
            self.assertIn("title", second_page[0])
            self.assertNotIn("secret", second_page[0])

        finally:
            if original_testing is not None:
                os.environ["TESTING_AUTH_BYPASS"] = original_testing
            elif "TESTING_AUTH_BYPASS" in os.environ:
                del os.environ["TESTING_AUTH_BYPASS"]

            if original_mock is not None:
                os.environ["MOCK_SERVICES_MODE"] = original_mock
            elif "MOCK_SERVICES_MODE" in os.environ:
                del os.environ["MOCK_SERVICES_MODE"]


if __name__ == "__main__":
    print("🟢 GREEN PHASE: Testing MOCK_SERVICES_MODE support...")
    print(
        f"Environment: TESTING_AUTH_BYPASS={os.environ.get('TESTING_AUTH_BYPASS', 'NOT SET')}, "
        f"MOCK_SERVICES_MODE={os.environ.get('MOCK_SERVICES_MODE', 'NOT SET')}"
    )

    unittest.main()

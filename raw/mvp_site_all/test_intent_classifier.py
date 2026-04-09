import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np

from mvp_site import constants, intent_classifier


class TestIntentClassifier(unittest.TestCase):
    def setUp(self):
        # Reset singleton
        intent_classifier.LocalIntentClassifier._instance = None

    def test_initialize_skips_when_semantic_routing_disabled(self):
        original_setting = os.environ.get("ENABLE_SEMANTIC_ROUTING")
        try:
            os.environ["ENABLE_SEMANTIC_ROUTING"] = "false"
            with (
                patch.object(
                    intent_classifier.LocalIntentClassifier, "get_instance"
                ) as mock_get_instance,
                patch.object(intent_classifier.logging_util, "info") as mock_info,
            ):
                intent_classifier.initialize()
                mock_get_instance.assert_not_called()
                mock_info.assert_called_once()
        finally:
            if original_setting is not None:
                os.environ["ENABLE_SEMANTIC_ROUTING"] = original_setting
            elif "ENABLE_SEMANTIC_ROUTING" in os.environ:
                del os.environ["ENABLE_SEMANTIC_ROUTING"]

    def test_initialize_honors_explicit_enablement_in_tests(self):
        original_testing = os.environ.get("TESTING")
        original_semantic = os.environ.get("ENABLE_SEMANTIC_ROUTING")
        try:
            os.environ["TESTING"] = "true"
            os.environ["ENABLE_SEMANTIC_ROUTING"] = "true"
            with patch.object(
                intent_classifier.LocalIntentClassifier, "get_instance"
            ) as mock_get_instance:
                mock_instance = MagicMock()
                mock_get_instance.return_value = mock_instance
                intent_classifier.initialize()
                mock_instance.initialize_async.assert_called_once()
        finally:
            if original_testing is not None:
                os.environ["TESTING"] = original_testing
            else:
                os.environ.pop("TESTING", None)

            if original_semantic is not None:
                os.environ["ENABLE_SEMANTIC_ROUTING"] = original_semantic
            else:
                os.environ.pop("ENABLE_SEMANTIC_ROUTING", None)

    @patch.object(intent_classifier, "_FASTEMBED_CACHE_DIR", "/tmp/test-fastembed-cache")
    @patch.object(intent_classifier, "TextEmbedding")
    @patch.object(intent_classifier, "FASTEMBED_AVAILABLE", True)
    @patch.object(intent_classifier, "ONNXRUNTIME_AVAILABLE", True)
    @patch.object(intent_classifier, "_text_embedding_supports_local_files_only", return_value=True)
    def test_initialization_uses_local_files_only_when_offline(
        self,
        mock_supports_local_files_only,
        mock_text_embedding_cls,
    ):
        original_offline = os.environ.get("HF_HUB_OFFLINE")
        os.environ["HF_HUB_OFFLINE"] = "1"
        try:
            mock_model = MagicMock()
            mock_text_embedding_cls.return_value = mock_model

            def mock_embed(texts):
                for _ in texts:
                    yield np.array([0.1, 0.2, 0.3])

            mock_model.embed = mock_embed

            classifier = intent_classifier.LocalIntentClassifier.get_instance()
            classifier._initialize_model()

            self.assertTrue(classifier.ready)
            mock_supports_local_files_only.assert_called_once()
            mock_text_embedding_cls.assert_called_once_with(
                model_name="BAAI/bge-small-en-v1.5",
                threads=1,
                cache_dir="/tmp/test-fastembed-cache",
                local_files_only=True,
            )
        finally:
            if original_offline is None:
                os.environ.pop("HF_HUB_OFFLINE", None)
            else:
                os.environ["HF_HUB_OFFLINE"] = original_offline

    @patch.object(intent_classifier, "_FASTEMBED_CACHE_DIR", "/tmp/test-fastembed-cache")
    @patch.object(intent_classifier, "TextEmbedding")
    @patch.object(intent_classifier, "FASTEMBED_AVAILABLE", True)
    @patch.object(intent_classifier, "ONNXRUNTIME_AVAILABLE", True)
    def test_initialization(self, mock_text_embedding_cls):
        """Test classifier initialization with mocked FastEmbed model."""
        # Configure the mock model
        mock_model = MagicMock()
        mock_text_embedding_cls.return_value = mock_model

        def mock_embed(texts):
            for _ in texts:
                yield np.array([0.1, 0.2, 0.3])

        mock_model.embed = mock_embed

        classifier = intent_classifier.LocalIntentClassifier.get_instance()
        classifier._initialize_model()

        self.assertTrue(classifier.ready)
        self.assertIsNotNone(classifier.model)
        self.assertGreater(len(classifier.anchor_embeddings), 0)
        # Verify mock was called with expected parameters including cache_dir
        mock_text_embedding_cls.assert_called_once_with(
            model_name="BAAI/bge-small-en-v1.5", threads=1, cache_dir="/tmp/test-fastembed-cache"
        )

    @patch.object(intent_classifier.LocalIntentClassifier, "_MIN_BLOBS_TOTAL_SIZE_BYTES", 1)
    def test_validate_and_repair_cache_removes_corrupted_dir(self):
        model_cache_name = f"models--{intent_classifier.MODEL_NAME.replace('/', '--')}"
        with tempfile.TemporaryDirectory() as tmp_dir:
            cache_dir = os.path.join(tmp_dir, model_cache_name)
            snapshots_dir = os.path.join(cache_dir, "snapshots")
            blobs_dir = os.path.join(cache_dir, "blobs")
            os.makedirs(snapshots_dir, exist_ok=True)
            os.makedirs(blobs_dir, exist_ok=True)
            with open(os.path.join(blobs_dir, "blob.bin"), "wb") as f:
                f.write(b"xx")
            # Add a dangling symlink to force cache repair.
            try:
                os.symlink(
                    os.path.join(cache_dir, "missing-target"),
                    os.path.join(snapshots_dir, "model_optimized.onnx"),
                )
            except OSError:
                self.skipTest("Symlinks not supported on this platform")
            with patch.object(intent_classifier, "_FASTEMBED_CACHE_DIR", tmp_dir):
                classifier = intent_classifier.LocalIntentClassifier.get_instance()

                # Verify corruption is detected BEFORE repair
                self.assertTrue(
                    classifier._is_corrupted_cache_dir(Path(cache_dir)),
                    "Expected corruption to be detected before repair",
                )

                # Verify repair runs and, when emitted, warning logs mention corrupted cache.
                with patch.object(intent_classifier.logging_util, "warning") as mock_warning:
                    classifier._validate_and_repair_cache()
                    warning_messages = [
                        str(call.args[0])
                        for call in mock_warning.call_args_list
                        if getattr(call, "args", None)
                    ]
                    self.assertTrue(
                        any("corrupted cache" in message.lower() for message in warning_messages),
                        "Expected warning about corrupted cache detection",
                    )

                # Verify directory was removed after repair
                self.assertFalse(os.path.exists(cache_dir))

    @patch.object(intent_classifier.LocalIntentClassifier, "_MIN_BLOBS_TOTAL_SIZE_BYTES", 1)
    def test_validate_and_repair_cache_skips_purge_when_lock_present(self):
        model_cache_name = f"models--{intent_classifier.MODEL_NAME.replace('/', '--')}"
        with tempfile.TemporaryDirectory() as tmp_dir:
            cache_dir = os.path.join(tmp_dir, model_cache_name)
            snapshots_dir = os.path.join(cache_dir, "snapshots")
            blobs_dir = os.path.join(cache_dir, "blobs")
            os.makedirs(snapshots_dir, exist_ok=True)
            os.makedirs(blobs_dir, exist_ok=True)

            # Corrupt via dangling symlink
            with open(os.path.join(blobs_dir, "blob.bin"), "wb") as f:
                f.write(b"x")
            try:
                os.symlink(
                    os.path.join(cache_dir, "missing-target"),
                    os.path.join(snapshots_dir, "model_optimized.onnx"),
                )
            except OSError:
                self.skipTest("Symlinks not supported on this platform")

            # Active download marker should block purge
            with open(os.path.join(cache_dir, "download.lock"), "w") as f:
                f.write("locked")

            with patch.object(intent_classifier, "_FASTEMBED_CACHE_DIR", tmp_dir):
                classifier = intent_classifier.LocalIntentClassifier.get_instance()

                self.assertTrue(classifier._is_corrupted_cache_dir(Path(cache_dir)))
                self.assertTrue(classifier._has_active_download_lock(Path(cache_dir)))

                classifier._validate_and_repair_cache()

            # Must keep directory intact while lock marker exists
            self.assertTrue(os.path.exists(cache_dir))

    def test_is_corrupted_cache_dir_detects_missing_blobs(self):
        """Test that _is_corrupted_cache_dir correctly detects missing blobs directory."""
        model_cache_name = f"models--{intent_classifier.MODEL_NAME.replace('/', '--')}"
        with tempfile.TemporaryDirectory() as tmp_dir:
            cache_dir = os.path.join(tmp_dir, model_cache_name)
            snapshots_dir = os.path.join(cache_dir, "snapshots")
            os.makedirs(snapshots_dir, exist_ok=True)
            # Note: blobs_dir is NOT created - this should trigger corruption detection
            classifier = intent_classifier.LocalIntentClassifier.get_instance()
            # Should detect as corrupted due to missing blobs directory
            self.assertTrue(classifier._is_corrupted_cache_dir(Path(cache_dir)))

    def test_is_corrupted_cache_dir_detects_small_blobs(self):
        """Test that _is_corrupted_cache_dir correctly detects undersized blobs."""
        model_cache_name = f"models--{intent_classifier.MODEL_NAME.replace('/', '--')}"
        with tempfile.TemporaryDirectory() as tmp_dir:
            cache_dir = os.path.join(tmp_dir, model_cache_name)
            blobs_dir = os.path.join(cache_dir, "blobs")
            os.makedirs(blobs_dir, exist_ok=True)
            # Create a small blob file (under default 1MB threshold)
            small_blob = os.path.join(blobs_dir, "small-model-part.bin")
            with open(small_blob, "wb") as f:
                f.write(b"x" * 500)  # 500 bytes - below 1MB threshold
            classifier = intent_classifier.LocalIntentClassifier.get_instance()
            # Should detect as corrupted due to small blob size
            self.assertTrue(classifier._is_corrupted_cache_dir(Path(cache_dir)))

    def test_is_corrupted_cache_dir_allows_empty_cache(self):
        """Test that _is_corrupted_cache_dir does NOT flag an empty cache dir as corrupted."""
        model_cache_name = f"models--{intent_classifier.MODEL_NAME.replace('/', '--')}"
        with tempfile.TemporaryDirectory() as tmp_dir:
            cache_dir = os.path.join(tmp_dir, model_cache_name)
            # Create an empty cache directory (no blobs, no snapshots)
            os.makedirs(cache_dir, exist_ok=True)
            classifier = intent_classifier.LocalIntentClassifier.get_instance()
            # Empty cache dir should NOT be detected as corrupted - it's just uninitialized
            self.assertFalse(classifier._is_corrupted_cache_dir(Path(cache_dir)))

    def test_is_corrupted_cache_dir_detects_corruption_with_other_content(self):
        """Test that _is_corrupted_cache_dir detects corruption when blobs is missing but other content exists."""
        model_cache_name = f"models--{intent_classifier.MODEL_NAME.replace('/', '--')}"
        with tempfile.TemporaryDirectory() as tmp_dir:
            cache_dir = os.path.join(tmp_dir, model_cache_name)
            snapshots_dir = os.path.join(cache_dir, "snapshots")
            os.makedirs(snapshots_dir, exist_ok=True)
            # Create some file in snapshots but no blobs dir
            with open(os.path.join(snapshots_dir, "some-file.txt"), "w") as f:
                f.write("some content")
            classifier = intent_classifier.LocalIntentClassifier.get_instance()
            # Has other content but no blobs - should be detected as corrupted
            self.assertTrue(classifier._is_corrupted_cache_dir(Path(cache_dir)))

    def test_predict_think_mode(self):
        classifier = intent_classifier.LocalIntentClassifier.get_instance()
        classifier.ready = True

        classifier.anchor_embeddings = {
            constants.MODE_THINK: np.array([[1.0, 0.0]]),
            constants.MODE_INFO: np.array([[0.0, 1.0]]),
            constants.MODE_GOD: np.array([[0.0, 0.0]]),
        }

        mock_model = MagicMock()
        classifier.model = mock_model

        def mock_embed(texts):
            for _ in texts:
                # Provide a vector that normalizes to the exact anchor match.
                yield np.array([1.0, 0.0])

        mock_model.embed.side_effect = mock_embed

        mode, score = classifier.predict("I need a plan")

        self.assertEqual(mode, constants.MODE_THINK)
        # Exact anchor match returns 1.0 confidence (fast path for contamination prevention)
        self.assertAlmostEqual(score, 1.0)


    def test_classifier_startup_check_degrades_on_load_failure(self):
        """create_app() classifier check must warn, not raise, when model download fails.

        Reproduces: Cloud Run crash loop where fastembed gets rate-limited by HuggingFace
        (429), classifier retries exhaust, _load_error is set, and create_app() raises
        RuntimeError killing the server. The fix: warn and continue instead of crashing.
        """
        classifier = intent_classifier.LocalIntentClassifier.get_instance()
        # Simulate: retries exhausted, _load_error set, _initializing done
        classifier._load_error = "Could not load model BAAI/bge-small-en-v1.5 from any source."
        classifier._initializing = False
        classifier.ready = False

        # Import the extracted startup check (lives in intent_classifier to avoid Flask deps)
        from mvp_site.intent_classifier import check_classifier_startup

        # startup_timeout_seconds=1 so the while-loop enters, then breaks
        # immediately (because _initializing=False), keeping timed_out=False.
        # This exercises the _load_error branch specifically.
        try:
            check_classifier_startup(classifier, startup_timeout_seconds=1)
        except RuntimeError as e:
            if "Classifier initialization failed" in str(e):
                self.fail(
                    f"check_classifier_startup() raised RuntimeError instead of "
                    f"degrading gracefully: {e}"
                )
            raise


if __name__ == "__main__":
    unittest.main()

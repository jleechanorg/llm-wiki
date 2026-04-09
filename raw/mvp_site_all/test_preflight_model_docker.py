"""
TDD tests for scripts/preflight_model_docker.py (CodeRabbit PR #5861 fixes).

Tests verify:
1. _restore_cache_from_gcs return value is checked when FASTEMBED_GCS_REQUIRED=true
2. _safe_extract_tar accepts tar -C archives with . root entry
3. _parse_gcs_uri rejects gs://bucket/ (empty object_name)
4. _safe_extract_tar validates member.linkname for symlink path traversal
5. (Dockerfile change tested separately - no Python test)
"""

import importlib.util
import os
import tarfile
import tempfile
import unittest

# Load preflight_model_docker module from scripts/
_REPO_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
_PREFLIGHT_PATH = os.path.join(_REPO_ROOT, "scripts", "preflight_model_docker.py")
spec = importlib.util.spec_from_file_location("preflight_model_docker", _PREFLIGHT_PATH)
preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight)

_parse_gcs_uri = preflight._parse_gcs_uri
_safe_extract_tar = preflight._safe_extract_tar
_restore_cache_from_gcs = preflight._restore_cache_from_gcs


class TestParseGcsUri(unittest.TestCase):
    """Tests for _parse_gcs_uri (CodeRabbit issue #3)."""

    def test_valid_uri_returns_bucket_and_object(self):
        bucket, obj = _parse_gcs_uri("gs://bucket/path/to/object.tar")
        self.assertEqual(bucket, "bucket")
        self.assertEqual(obj, "path/to/object.tar")

    def test_rejects_gs_bucket_only_trailing_slash(self):
        """Issue #3: gs://bucket/ yields empty object_name - must reject."""
        with self.assertRaises(ValueError) as ctx:
            _parse_gcs_uri("gs://bucket/")
        self.assertIn("Invalid GCS URI", str(ctx.exception))

    def test_rejects_empty_path_after_bucket(self):
        """gs://bucket with no path also invalid."""
        with self.assertRaises(ValueError):
            _parse_gcs_uri("gs://bucket")


class TestSafeExtractTar(unittest.TestCase):
    """Tests for _safe_extract_tar (CodeRabbit issues #2, #4)."""

    def test_accepts_tar_c_style_archive_with_dot_root(self):
        """Issue #2: Archives from `tar -C dir -cf archive.tar .` must work."""
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "src")
            os.makedirs(src)
            with open(os.path.join(src, "file.txt"), "w") as f:
                f.write("content")
            archive_path = os.path.join(tmp, "archive.tar")
            with tarfile.open(archive_path, "w") as tf:
                tf.add(src, arcname=".")
            dest = os.path.join(tmp, "dest")
            os.makedirs(dest)
            # Member names are typically "./" and "./file.txt" from tar -C
            _safe_extract_tar(archive_path, dest)
            extracted = os.path.join(dest, "file.txt")
            self.assertTrue(os.path.isfile(extracted), "file.txt should be extracted")
            with open(extracted) as f:
                self.assertEqual(f.read(), "content")

    def test_rejects_symlink_escaping_via_linkname(self):
        """Issue #4: Symlink with linkname outside dest must be rejected."""
        with tempfile.TemporaryDirectory() as tmp:
            archive_path = os.path.join(tmp, "evil.tar")
            with tarfile.open(archive_path, "w") as tf:
                info = tarfile.TarInfo("safe/path")
                info.type = tarfile.SYMTYPE
                info.linkname = "../../../etc/passwd"
                tf.addfile(info)
            dest = os.path.join(tmp, "dest")
            os.makedirs(dest)
            with self.assertRaises(ValueError) as ctx:
                _safe_extract_tar(archive_path, dest)
            self.assertIn("Blocked unsafe", str(ctx.exception))


class TestRestoreCacheFromGcsReturnValue(unittest.TestCase):
    """Tests for _restore_cache_from_gcs return check (CodeRabbit issue #1)."""

    def test_main_fails_when_gcs_required_and_restore_returns_false(self):
        """Issue #1: When _restore_cache_from_gcs returns False and FASTEMBED_GCS_REQUIRED=true, main must return 1.
        Without the fix, validation could pass (e.g. cached model from prior layer) and we'd wrongly return 0."""
        with tempfile.TemporaryDirectory() as tmp:
            cache_dir = os.path.join(tmp, "cache")
            os.makedirs(cache_dir, exist_ok=True)
            orig_cache = os.environ.get("FASTEMBED_CACHE_PATH")
            orig_uri = os.environ.get("FASTEMBED_GCS_ARCHIVE_URI")
            orig_req = os.environ.get("FASTEMBED_GCS_REQUIRED")
            os.environ["FASTEMBED_CACHE_PATH"] = cache_dir
            os.environ["FASTEMBED_GCS_ARCHIVE_URI"] = "gs://bucket/path/to/cache.tar"
            os.environ["FASTEMBED_GCS_REQUIRED"] = "true"
            try:
                original_restore = preflight._restore_cache_from_gcs
                original_load = preflight._load_and_validate_model
                preflight._restore_cache_from_gcs = lambda *_, **__: False
                preflight._load_and_validate_model = lambda *_, **__: True
                try:
                    exit_code = preflight.main()
                    self.assertEqual(
                        exit_code, 1,
                        "Must fail when FASTEMBED_GCS_REQUIRED=true and _restore_cache_from_gcs returns False"
                    )
                finally:
                    preflight._restore_cache_from_gcs = original_restore
                    preflight._load_and_validate_model = original_load
            finally:
                for k, v in [("FASTEMBED_CACHE_PATH", orig_cache), ("FASTEMBED_GCS_ARCHIVE_URI", orig_uri), ("FASTEMBED_GCS_REQUIRED", orig_req)]:
                    if v is not None:
                        os.environ[k] = v
                    else:
                        os.environ.pop(k, None)


if __name__ == "__main__":
    unittest.main()

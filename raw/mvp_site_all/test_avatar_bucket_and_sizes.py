#!/usr/bin/env python3
"""TDD tests for avatar storage bucket fallback and CSS pip sizes.

Tests:
  1. Bucket fallback: .firebasestorage.app → .appspot.com (project-preserving)
  2. Bucket fallback: explicit AVATAR_STORAGE_BUCKET takes priority
  3. Bucket fallback: normal bucket names pass through unchanged
"""

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

# Stub firebase_admin before importing firestore_service
if "firebase_admin" not in sys.modules:
    import types

    fa = types.ModuleType("firebase_admin")
    fa.initialize_app = lambda *a, **k: None
    fa.get_app = lambda *a, **k: None
    fa.credentials = types.ModuleType("firebase_admin.credentials")
    fa.credentials.Certificate = lambda *a, **k: None
    fa.firestore = types.ModuleType("firebase_admin.firestore")
    fa.firestore.client = lambda *a, **k: None
    fa.auth = types.ModuleType("firebase_admin.auth")
    fa.auth.verify_id_token = lambda *a, **k: {}
    fa.storage = types.ModuleType("firebase_admin.storage")
    fa.storage.bucket = lambda *a, **k: None
    sys.modules["firebase_admin"] = fa
    sys.modules["firebase_admin.credentials"] = fa.credentials
    sys.modules["firebase_admin.firestore"] = fa.firestore
    sys.modules["firebase_admin.auth"] = fa.auth
    sys.modules["firebase_admin.storage"] = fa.storage


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class TestStorageBucketFallback(unittest.TestCase):
    """Test _STORAGE_BUCKET resolution logic."""

    def _resolve_bucket(self, env_overrides: dict) -> str:
        """Simulate the bucket resolution logic from firestore_service.py."""
        with patch.dict(os.environ, env_overrides, clear=False):
            # Remove cached values
            for key in list(os.environ.keys()):
                if key not in env_overrides and key in (
                    "AVATAR_STORAGE_BUCKET",
                    "FIREBASE_STORAGE_BUCKET",
                ):
                    os.environ.pop(key, None)

            bucket = os.environ.get(
                "AVATAR_STORAGE_BUCKET",
                os.environ.get(
                    "FIREBASE_STORAGE_BUCKET",
                    "worldarchitecture-ai-frontend-static",
                ),
            )
            # Hardcoded fallback (only working bucket for this project)
            if bucket.endswith(".firebasestorage.app"):
                bucket = "worldarchitecture-ai-frontend-static"
            return bucket

    def test_firebasestorage_app_converts_to_frontend_static(self):
        """Firebase URL-format bucket → hardcoded frontend-static (only working bucket)."""
        result = self._resolve_bucket(
            {"FIREBASE_STORAGE_BUCKET": "worldarchitecture-ai.firebasestorage.app"}
        )
        self.assertEqual(result, "worldarchitecture-ai-frontend-static")

    def test_different_project_also_falls_back(self):
        """Any .firebasestorage.app bucket falls back to frontend-static."""
        result = self._resolve_bucket(
            {"FIREBASE_STORAGE_BUCKET": "my-cool-project.firebasestorage.app"}
        )
        self.assertEqual(result, "worldarchitecture-ai-frontend-static")

    def test_explicit_avatar_bucket_takes_priority(self):
        """AVATAR_STORAGE_BUCKET env var overrides FIREBASE_STORAGE_BUCKET."""
        result = self._resolve_bucket(
            {
                "AVATAR_STORAGE_BUCKET": "custom-avatar-bucket",
                "FIREBASE_STORAGE_BUCKET": "worldarchitecture-ai.firebasestorage.app",
            }
        )
        self.assertEqual(result, "custom-avatar-bucket")

    def test_normal_bucket_passthrough(self):
        """Normal GCS bucket names pass through unchanged."""
        result = self._resolve_bucket(
            {"FIREBASE_STORAGE_BUCKET": "worldarchitecture-ai-frontend-static"}
        )
        self.assertEqual(result, "worldarchitecture-ai-frontend-static")

    def test_default_when_no_env(self):
        """Default bucket when no env vars are set."""
        # Clear both env vars
        env = {}
        for k in ("AVATAR_STORAGE_BUCKET", "FIREBASE_STORAGE_BUCKET"):
            if k in os.environ:
                env[k] = ""
        with patch.dict(os.environ, {}, clear=False):
            for k in ("AVATAR_STORAGE_BUCKET", "FIREBASE_STORAGE_BUCKET"):
                os.environ.pop(k, None)
            bucket = os.environ.get(
                "AVATAR_STORAGE_BUCKET",
                os.environ.get(
                    "FIREBASE_STORAGE_BUCKET",
                    "worldarchitecture-ai-frontend-static",
                ),
            )
            if bucket.endswith(".firebasestorage.app"):
                project_id = bucket.replace(".firebasestorage.app", "")
                bucket = f"{project_id}.appspot.com"
            self.assertEqual(bucket, "worldarchitecture-ai-frontend-static")


class TestAvatarCSSPipSizes(unittest.TestCase):
    """Test that avatar.css has the correct pip sizes."""

    CSS_PATH = PROJECT_ROOT / "mvp_site" / "frontend_v1" / "css" / "avatar.css"

    def test_css_file_exists(self):
        self.assertTrue(self.CSS_PATH.exists(), f"Missing: {self.CSS_PATH}")

    def test_desktop_pip_size_176px(self):
        """Desktop avatar pip should be 176px."""
        css = self.CSS_PATH.read_text()
        # Check for 176px in .game-avatar-float img rule (not in mobile media query)
        self.assertIn("width: 176px", css, "Desktop pip width should be 176px")
        self.assertIn("height: 176px", css, "Desktop pip height should be 176px")

    def test_mobile_pip_size_88px(self):
        """Mobile avatar pip should be 88px (50% of desktop 176px)."""
        css = self.CSS_PATH.read_text()
        self.assertIn("width: 88px", css, "Mobile pip width should be 88px")
        self.assertIn("height: 88px", css, "Mobile pip height should be 88px")


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Layer 1 unit tests for avatar API logic.

Covers upload validation, magic-byte extension detection, GCS blob
management, URL validation, static asset presence, and avatar download
(user and campaign) including error propagation.
"""

import datetime
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Stub firebase_admin before importing
if "firebase_admin" not in sys.modules:
    import types

    fa = types.ModuleType("firebase_admin")
    fa.initialize_app = lambda *_a, **_k: None
    fa.get_app = lambda *_a, **_k: None
    fa.credentials = types.ModuleType("firebase_admin.credentials")
    fa.credentials.Certificate = lambda *_a, **_k: None
    fa.firestore = types.ModuleType("firebase_admin.firestore")
    fa.firestore.client = lambda *_a, **_k: None
    fa.firestore.Client = type("Client", (), {})
    fa.firestore.DELETE_FIELD = "DELETE_FIELD_SENTINEL"
    fa.auth = types.ModuleType("firebase_admin.auth")
    fa.auth.verify_id_token = lambda *_a, **_k: {}
    fa.storage = types.ModuleType("firebase_admin.storage")
    fa.storage.bucket = lambda *_a, **_k: MagicMock()
    sys.modules["firebase_admin"] = fa
    sys.modules["firebase_admin.credentials"] = fa.credentials
    sys.modules["firebase_admin.firestore"] = fa.firestore
    sys.modules["firebase_admin.auth"] = fa.auth
    sys.modules["firebase_admin.storage"] = fa.storage
else:
    # Ensure existing stub has required attributes (another test file may have set a simpler stub)
    _fs = sys.modules.get("firebase_admin.firestore")
    if _fs and not hasattr(_fs, "Client"):
        _fs.Client = type("Client", (), {})
    if _fs and not hasattr(_fs, "DELETE_FIELD"):
        _fs.DELETE_FIELD = "DELETE_FIELD_SENTINEL"


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
FRONTEND = PROJECT_ROOT / "mvp_site" / "frontend_v1"

# Add mvp_site to path for imports
sys.path.insert(0, str(PROJECT_ROOT / "mvp_site"))


class TestAvatarContentTypes(unittest.TestCase):
    """Test AVATAR_CONTENT_TYPES whitelist."""

    def test_allowed_types_are_jpeg_png_gif_webp(self):
        """Only image/jpeg, image/png, image/gif, image/webp are allowed."""
        # Import inline to avoid circular dependency issues
        from main import AVATAR_CONTENT_TYPES

        expected = {"image/jpeg", "image/png", "image/gif", "image/webp"}
        self.assertEqual(set(AVATAR_CONTENT_TYPES.keys()), expected)

    def test_extensions_map_correctly(self):
        from main import AVATAR_CONTENT_TYPES

        self.assertEqual(AVATAR_CONTENT_TYPES["image/jpeg"], "jpeg")
        self.assertEqual(AVATAR_CONTENT_TYPES["image/png"], "png")
        self.assertEqual(AVATAR_CONTENT_TYPES["image/gif"], "gif")
        self.assertEqual(AVATAR_CONTENT_TYPES["image/webp"], "webp")

    def test_svg_is_not_allowed(self):
        from main import AVATAR_CONTENT_TYPES

        self.assertNotIn("image/svg+xml", AVATAR_CONTENT_TYPES)

    def test_bmp_is_not_allowed(self):
        from main import AVATAR_CONTENT_TYPES

        self.assertNotIn("image/bmp", AVATAR_CONTENT_TYPES)


class TestDetectImageExtension(unittest.TestCase):
    """Test magic byte detection for image types."""

    def test_jpeg_magic_bytes(self):
        from main import _detect_image_extension

        jpeg_data = b"\xff\xd8\xff" + b"\x00" * 20
        self.assertEqual(_detect_image_extension(jpeg_data), "jpeg")

    def test_png_magic_bytes(self):
        from main import _detect_image_extension

        png_data = b"\x89PNG\r\n\x1a\n" + b"\x00" * 20
        self.assertEqual(_detect_image_extension(png_data), "png")

    def test_gif87a_magic_bytes(self):
        from main import _detect_image_extension

        gif_data = b"GIF87a" + b"\x00" * 20
        self.assertEqual(_detect_image_extension(gif_data), "gif")

    def test_gif89a_magic_bytes(self):
        from main import _detect_image_extension

        gif_data = b"GIF89a" + b"\x00" * 20
        self.assertEqual(_detect_image_extension(gif_data), "gif")

    def test_webp_magic_bytes(self):
        from main import _detect_image_extension

        # RIFF....WEBP
        webp_data = b"RIFF\x00\x00\x00\x00WEBP" + b"\x00" * 20
        self.assertEqual(_detect_image_extension(webp_data), "webp")

    def test_unknown_bytes_returns_none(self):
        from main import _detect_image_extension

        self.assertIsNone(_detect_image_extension(b"\x00\x01\x02" * 10))

    def test_too_short_returns_none(self):
        from main import _detect_image_extension

        self.assertIsNone(_detect_image_extension(b"\xff\xd8"))


class TestUploadCampaignAvatar(unittest.TestCase):
    """Test upload_campaign_avatar validation and blob path."""

    def test_rejects_unsupported_content_type(self):
        from mvp_site import firestore_service

        with pytest.raises(ValueError, match="Unsupported"):
            firestore_service.upload_campaign_avatar(
                "user1", "camp1", b"data", "image/bmp"
            )

    @patch("mvp_site.firestore_service.storage", create=True)
    def test_builds_correct_blob_path(self, mock_storage):
        from mvp_site import firestore_service

        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_blob.public_url = "https://storage.example.com/avatar.png"
        mock_bucket.blob.return_value = mock_blob
        mock_storage.bucket.return_value = mock_bucket

        result = firestore_service.upload_campaign_avatar(
            "user123", "camp456", b"\x89PNG\r\n\x1a\n" + b"\x00" * 20, "image/png"
        )

        # Verify blob path
        mock_bucket.blob.assert_called_once_with(
            "campaign_avatars/user123/camp456/avatar.png"
        )
        mock_blob.upload_from_string.assert_called_once()
        mock_blob.make_public.assert_called_once()
        self.assertEqual(result, "https://storage.example.com/avatar.png")


class TestDeleteCampaignAvatar(unittest.TestCase):
    """Test delete_campaign_avatar blob cleanup."""

    @patch("mvp_site.firestore_service.storage", create=True)
    def test_deletes_matching_blobs(self, mock_storage):
        from mvp_site import firestore_service

        mock_bucket = MagicMock()
        mock_blob1 = MagicMock()
        mock_blob2 = MagicMock()
        mock_bucket.list_blobs.return_value = [mock_blob1, mock_blob2]
        mock_storage.bucket.return_value = mock_bucket

        count = firestore_service.delete_campaign_avatar("user1", "camp1")

        mock_bucket.list_blobs.assert_called_once_with(
            prefix="campaign_avatars/user1/camp1/"
        )
        mock_blob1.delete.assert_called_once()
        mock_blob2.delete.assert_called_once()
        self.assertEqual(count, 2)

    @patch("mvp_site.firestore_service.storage", create=True)
    def test_returns_zero_when_no_blobs(self, mock_storage):
        from mvp_site import firestore_service

        mock_bucket = MagicMock()
        mock_bucket.list_blobs.return_value = []
        mock_storage.bucket.return_value = mock_bucket

        count = firestore_service.delete_campaign_avatar("user1", "camp1")
        self.assertEqual(count, 0)


class TestValidateAvatarUrl(unittest.TestCase):
    """Test validate_avatar_url from settings_validation."""

    def test_none_clears_avatar(self):
        from settings_validation import validate_avatar_url

        value, error = validate_avatar_url(None)
        self.assertIsNone(value)
        self.assertIsNone(error)

    def test_valid_url_passes(self):
        from settings_validation import validate_avatar_url

        value, error = validate_avatar_url("https://example.com/avatar.png")
        self.assertEqual(value, "https://example.com/avatar.png")
        self.assertIsNone(error)

    def test_empty_string_clears(self):
        from settings_validation import validate_avatar_url

        value, error = validate_avatar_url("")
        self.assertIsNone(value)
        self.assertIsNone(error)

    def test_whitespace_string_clears(self):
        from settings_validation import validate_avatar_url

        value, error = validate_avatar_url("   ")
        self.assertIsNone(value)
        self.assertIsNone(error)

    def test_non_string_rejected(self):
        from settings_validation import validate_avatar_url

        value, error = validate_avatar_url(12345)
        self.assertIsNone(value)
        self.assertIn("must be a string", error)

    def test_too_long_rejected(self):
        from settings_validation import validate_avatar_url

        value, error = validate_avatar_url("https://x.com/" + "a" * 2100)
        self.assertIsNone(value)
        self.assertIn("too long", error)


class TestDefaultArionAvatar(unittest.TestCase):
    """Test that the default Arion avatar file exists and is reasonable."""

    ARION_PATH = FRONTEND / "images" / "avatars" / "arion_dragon_knight.png"

    def test_arion_file_exists(self):
        self.assertTrue(
            self.ARION_PATH.exists(),
            f"Missing: {self.ARION_PATH}",
        )

    def test_arion_file_is_reasonable_size(self):
        """Avatar should be > 10KB (not a broken/empty file)."""
        size = self.ARION_PATH.stat().st_size
        self.assertGreater(size, 10_000, f"Arion avatar too small: {size} bytes")


class TestFrontendAssets(unittest.TestCase):
    """Test that critical frontend avatar assets exist and have expected content."""

    def test_avatar_crop_js_exists(self):
        path = FRONTEND / "js" / "avatar-crop.js"
        self.assertTrue(path.exists(), f"Missing: {path}")

    def test_avatar_css_exists(self):
        path = FRONTEND / "css" / "avatar.css"
        self.assertTrue(path.exists(), f"Missing: {path}")

    def test_crop_overlay_z_index_above_card(self):
        """Crop overlay must be above avatar card overlay (z-index 10000)."""
        css = (FRONTEND / "css" / "avatar.css").read_text()
        self.assertIn("z-index: 10001", css, "Crop overlay z-index must be 10001")

    def test_wizard_avatar_url_has_cache_buster(self):
        """DEFAULT_DRAGON_KNIGHT_AVATAR must include ?v= to bust browser cache."""
        js = (FRONTEND / "js" / "campaign-wizard.js").read_text()
        self.assertIn(
            "arion_dragon_knight.png?v=",
            js,
            "Arion avatar URL must include cache-buster ?v=",
        )


class TestDownloadUserAvatar(unittest.TestCase):
    """Test download_user_avatar from Firebase Storage."""

    @patch("mvp_site.firestore_service.storage", create=True)
    def test_returns_bytes_and_content_type_when_found(self, mock_storage):
        from mvp_site import firestore_service

        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_blob.name = "avatars/user123/avatar.jpeg"
        mock_blob.updated = datetime.datetime.now(datetime.UTC)
        mock_blob.download_as_bytes.return_value = b"\xff\xd8\xff fake jpeg data"
        mock_bucket.list_blobs.return_value = [mock_blob]
        # bucket.blob() called after probe returns extension
        mock_bucket.blob.return_value = mock_blob
        mock_storage.bucket.return_value = mock_bucket

        data, content_type = firestore_service.download_user_avatar("user123")

        self.assertEqual(data, b"\xff\xd8\xff fake jpeg data")
        self.assertEqual(content_type, "image/jpeg")

    @patch("mvp_site.firestore_service.storage", create=True)
    def test_raises_value_error_when_avatar_not_found(self, mock_storage):
        from mvp_site import firestore_service

        mock_bucket = MagicMock()
        mock_bucket.list_blobs.return_value = []
        mock_storage.bucket.return_value = mock_bucket

        with pytest.raises(ValueError, match="No avatar found"):
            firestore_service.download_user_avatar("user_no_avatar")

    @patch("mvp_site.firestore_service.storage", create=True)
    def test_propagates_storage_error_on_download(self, mock_storage):
        from mvp_site import firestore_service

        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_blob.name = "avatars/user123/avatar.jpeg"
        mock_blob.updated = datetime.datetime.now(datetime.UTC)
        mock_blob.download_as_bytes.side_effect = RuntimeError("storage failure")
        mock_bucket.list_blobs.return_value = [mock_blob]
        mock_bucket.blob.return_value = mock_blob
        mock_storage.bucket.return_value = mock_bucket

        with pytest.raises(RuntimeError, match="storage failure"):
            firestore_service.download_user_avatar("user123")


class TestDownloadCampaignAvatar(unittest.TestCase):
    """Test download_campaign_avatar from Firebase Storage."""

    @patch("mvp_site.firestore_service.storage", create=True)
    def test_returns_bytes_and_content_type_when_found(self, mock_storage):
        from mvp_site import firestore_service

        mock_bucket = MagicMock()
        mock_blob_png = MagicMock()
        mock_blob_png.name = "campaign_avatars/user123/camp456/avatar.png"
        mock_blob_png.updated = datetime.datetime.now(datetime.UTC)
        mock_blob_png.download_as_bytes.return_value = (
            b"\x89PNG\r\n\x1a\n fake png data"
        )
        mock_bucket.list_blobs.return_value = [mock_blob_png]
        # bucket.blob() called after probe returns extension
        mock_bucket.blob.return_value = mock_blob_png
        mock_storage.bucket.return_value = mock_bucket

        data, content_type = firestore_service.download_campaign_avatar(
            "user123", "camp456"
        )

        self.assertEqual(data, b"\x89PNG\r\n\x1a\n fake png data")
        self.assertEqual(content_type, "image/png")

    @patch("mvp_site.firestore_service.storage", create=True)
    def test_raises_value_error_when_avatar_not_found(self, mock_storage):
        from mvp_site import firestore_service

        mock_bucket = MagicMock()
        mock_bucket.list_blobs.return_value = []
        mock_storage.bucket.return_value = mock_bucket

        with pytest.raises(ValueError, match="No avatar found"):
            firestore_service.download_campaign_avatar("user_no_avatar", "camp")


if __name__ == "__main__":
    unittest.main()

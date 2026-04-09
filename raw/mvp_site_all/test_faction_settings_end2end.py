"""End-to-end test for faction_minigame_enabled and other settings persistence.

Tests the complete flow of:
1. Saving faction_minigame_enabled (and other previously broken settings)
2. Verifying they persist correctly
3. Round-trip validation (save → retrieve → verify)

This test validates the fix for Bug #1 where faction_minigame_enabled was silently
dropped because it had no validation block in update_user_settings_unified().
"""

import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ["TESTING_AUTH_BYPASS"] = "true"
os.environ.setdefault("GEMINI_API_KEY", "test-api-key")


# Ensure both the repo root (for `infrastructure`) and mvp_site (for `main`) are importable
PROJECT_ROOT = Path(__file__).resolve().parents[3]
MVP_SITE_ROOT = PROJECT_ROOT / "mvp_site"
for path in (PROJECT_ROOT, MVP_SITE_ROOT):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)


from main import create_app  # noqa: E402

from tests.fake_firestore import FakeFirestoreClient  # noqa: E402
from tests.test_end2end import End2EndBaseTestCase  # noqa: E402


class TestFactionSettingsEndToEnd(End2EndBaseTestCase):
    """Verify faction_minigame_enabled and other previously broken settings persist correctly."""

    CREATE_APP = create_app
    AUTH_PATCH_TARGET = "main.auth.verify_id_token"
    TEST_USER_ID = "faction-settings-e2e-user"

    def setUp(self):
        super().setUp()

        # Use FakeFirestore instead of mocking firestore_service functions
        self.fake_firestore = FakeFirestoreClient()
        self._db_patcher = patch(
            "firestore_service.get_db", return_value=self.fake_firestore
        )
        self._db_patcher.start()
        self.addCleanup(self._db_patcher.stop)
        self.headers = self.test_headers

    def test_faction_minigame_enabled_roundtrip(self):
        """Verify faction_minigame_enabled persists correctly."""
        # Save faction_minigame_enabled = True
        save_payload = {"faction_minigame_enabled": True}
        save_resp = self.client.post(
            "/api/settings", data=json.dumps(save_payload), headers=self.headers
        )
        assert save_resp.status_code == 200, f"Save failed: {save_resp.data}"

        # Retrieve settings
        get_resp = self.client.get("/api/settings", headers=self.headers)
        assert get_resp.status_code == 200
        settings = json.loads(get_resp.data)

        # Verify faction_minigame_enabled is True
        assert settings.get("faction_minigame_enabled") is True, (
            "faction_minigame_enabled should be True after save"
        )

    def test_faction_minigame_enabled_false_roundtrip(self):
        """Verify faction_minigame_enabled = False persists correctly."""
        # Save faction_minigame_enabled = False
        save_payload = {"faction_minigame_enabled": False}
        save_resp = self.client.post(
            "/api/settings", data=json.dumps(save_payload), headers=self.headers
        )
        assert save_resp.status_code == 200, f"Save failed: {save_resp.data}"

        # Retrieve settings
        get_resp = self.client.get("/api/settings", headers=self.headers)
        assert get_resp.status_code == 200
        settings = json.loads(get_resp.data)

        # Verify faction_minigame_enabled is False
        assert settings.get("faction_minigame_enabled") is False, (
            "faction_minigame_enabled should be False after save"
        )

    def test_spicy_mode_roundtrip(self):
        """Verify spicy_mode persists correctly."""
        # Save spicy_mode = True
        save_payload = {"spicy_mode": True}
        save_resp = self.client.post(
            "/api/settings", data=json.dumps(save_payload), headers=self.headers
        )
        assert save_resp.status_code == 200, f"Save failed: {save_resp.data}"

        # Retrieve settings
        get_resp = self.client.get("/api/settings", headers=self.headers)
        assert get_resp.status_code == 200
        settings = json.loads(get_resp.data)

        # Verify spicy_mode is True
        assert settings.get("spicy_mode") is True, (
            "spicy_mode should be True after save"
        )

    def test_auto_save_roundtrip(self):
        """Verify auto_save persists correctly."""
        # Save auto_save = True
        save_payload = {"auto_save": True}
        save_resp = self.client.post(
            "/api/settings", data=json.dumps(save_payload), headers=self.headers
        )
        assert save_resp.status_code == 200, f"Save failed: {save_resp.data}"

        # Retrieve settings
        get_resp = self.client.get("/api/settings", headers=self.headers)
        assert get_resp.status_code == 200
        settings = json.loads(get_resp.data)

        # Verify auto_save is True
        assert settings.get("auto_save") is True, "auto_save should be True after save"

    def test_theme_roundtrip(self):
        """Verify theme persists correctly."""
        # Save theme = "dark"
        save_payload = {"theme": "dark"}
        save_resp = self.client.post(
            "/api/settings", data=json.dumps(save_payload), headers=self.headers
        )
        assert save_resp.status_code == 200, f"Save failed: {save_resp.data}"

        # Retrieve settings
        get_resp = self.client.get("/api/settings", headers=self.headers)
        assert get_resp.status_code == 200
        settings = json.loads(get_resp.data)

        # Verify theme is "dark"
        assert settings.get("theme") == "dark", "theme should be 'dark' after save"

    def test_pre_spicy_model_roundtrip(self):
        """Verify pre_spicy_model persists correctly."""
        # Save pre_spicy_model
        save_payload = {"pre_spicy_model": "gemini-3-flash-preview"}
        save_resp = self.client.post(
            "/api/settings", data=json.dumps(save_payload), headers=self.headers
        )
        assert save_resp.status_code == 200, f"Save failed: {save_resp.data}"

        # Retrieve settings
        get_resp = self.client.get("/api/settings", headers=self.headers)
        assert get_resp.status_code == 200
        settings = json.loads(get_resp.data)

        # Verify pre_spicy_model
        assert settings.get("pre_spicy_model") == "gemini-3-flash-preview", (
            "pre_spicy_model should persist"
        )

    def test_pre_spicy_provider_roundtrip(self):
        """Verify pre_spicy_provider persists correctly."""
        # Save pre_spicy_provider
        save_payload = {"pre_spicy_provider": "openrouter"}
        save_resp = self.client.post(
            "/api/settings", data=json.dumps(save_payload), headers=self.headers
        )
        assert save_resp.status_code == 200, f"Save failed: {save_resp.data}"

        # Retrieve settings
        get_resp = self.client.get("/api/settings", headers=self.headers)
        assert get_resp.status_code == 200
        settings = json.loads(get_resp.data)

        # Verify pre_spicy_provider
        assert settings.get("pre_spicy_provider") == "openrouter", (
            "pre_spicy_provider should persist"
        )

    def test_all_six_settings_together(self):
        """Verify all 6 previously broken settings persist when saved together."""
        # Save all 6 settings at once
        save_payload = {
            "faction_minigame_enabled": True,
            "spicy_mode": False,
            "auto_save": True,
            "theme": "dark",
            "pre_spicy_model": "gemini-3-flash-preview",
            "pre_spicy_provider": "gemini",
        }
        save_resp = self.client.post(
            "/api/settings", data=json.dumps(save_payload), headers=self.headers
        )
        assert save_resp.status_code == 200, f"Save failed: {save_resp.data}"

        # Retrieve settings
        get_resp = self.client.get("/api/settings", headers=self.headers)
        assert get_resp.status_code == 200
        settings = json.loads(get_resp.data)

        # Verify all 6 settings
        assert settings.get("faction_minigame_enabled") is True
        assert settings.get("spicy_mode") is False
        assert settings.get("auto_save") is True
        assert settings.get("theme") == "dark"
        assert settings.get("pre_spicy_model") == "gemini-3-flash-preview"
        assert settings.get("pre_spicy_provider") == "gemini"

    def test_invalid_faction_minigame_value_rejected(self):
        """Verify non-boolean faction_minigame_enabled is rejected."""
        # Try to save invalid value (string instead of bool)
        save_payload = {"faction_minigame_enabled": "true"}  # String, not bool
        save_resp = self.client.post(
            "/api/settings", data=json.dumps(save_payload), headers=self.headers
        )

        # Should return 400 or error response
        assert save_resp.status_code != 200, "Invalid value should be rejected"

    def test_invalid_pre_spicy_provider_rejected(self):
        """Verify invalid pre_spicy_provider is rejected."""
        # Try to save invalid provider
        save_payload = {"pre_spicy_provider": "invalid-provider"}
        save_resp = self.client.post(
            "/api/settings", data=json.dumps(save_payload), headers=self.headers
        )

        # Should return error response
        assert save_resp.status_code != 200, "Invalid provider should be rejected"

    # ========================================================================
    # Settings Validation Module Integration Tests
    # These tests verify that the extracted settings_validation module
    # is properly integrated into the API flow (Bug #1 fix verification)
    # ========================================================================

    def test_case_insensitive_llm_provider_normalized(self):
        """Verify LLM provider is normalized to lowercase (via settings_validation)."""
        # Save with uppercase provider
        save_payload = {"llm_provider": "GEMINI"}
        save_resp = self.client.post(
            "/api/settings", data=json.dumps(save_payload), headers=self.headers
        )
        assert save_resp.status_code == 200, f"Save failed: {save_resp.data}"

        # Retrieve and verify it's normalized to lowercase
        get_resp = self.client.get("/api/settings", headers=self.headers)
        assert get_resp.status_code == 200
        settings = json.loads(get_resp.data)

        assert settings.get("llm_provider") == "gemini", (
            "LLM provider should be normalized to lowercase"
        )

    def test_invalid_llm_provider_rejected(self):
        """Verify invalid LLM provider is rejected (via settings_validation)."""
        save_payload = {"llm_provider": "not-a-real-provider"}
        save_resp = self.client.post(
            "/api/settings", data=json.dumps(save_payload), headers=self.headers
        )

        # Should return error
        assert save_resp.status_code != 200, "Invalid LLM provider should be rejected"

    def test_non_string_llm_provider_rejected(self):
        """Verify non-string LLM provider is rejected (type validation)."""
        save_payload = {"llm_provider": 12345}  # Integer instead of string
        save_resp = self.client.post(
            "/api/settings", data=json.dumps(save_payload), headers=self.headers
        )

        # Should return error
        assert save_resp.status_code != 200, (
            "Non-string LLM provider should be rejected"
        )

    def test_byok_api_key_clear_roundtrip(self):
        """Verify BYOK key persistence and clear flag behavior through real settings endpoints."""
        save_payload = {"gemini_api_key": "integration-gemini-key-123456789"}
        save_resp = self.client.post(
            "/api/settings", data=json.dumps(save_payload), headers=self.headers
        )
        assert save_resp.status_code == 200

        saved_settings = json.loads(self.client.get("/api/settings", headers=self.headers).data)
        assert saved_settings.get("has_custom_gemini_key") is True

        clear_payload = {"gemini_api_key": ""}
        clear_resp = self.client.post(
            "/api/settings", data=json.dumps(clear_payload), headers=self.headers
        )
        assert clear_resp.status_code == 200

        cleared_settings = json.loads(self.client.get("/api/settings", headers=self.headers).data)
        assert cleared_settings.get("has_custom_gemini_key") is False
        assert "gemini_api_key" not in cleared_settings

    def test_theme_length_validation(self):
        """Verify excessively long theme values are rejected."""
        # Theme over 50 characters should be rejected
        long_theme = "a" * 51
        save_payload = {"theme": long_theme}
        save_resp = self.client.post(
            "/api/settings", data=json.dumps(save_payload), headers=self.headers
        )

        # Should return error
        assert save_resp.status_code != 200, "Theme over 50 chars should be rejected"

    def test_case_insensitive_gemini_model_accepted(self):
        """Verify Gemini model validation is case-insensitive."""
        # Save with different case
        save_payload = {"gemini_model": "GEMINI-3-FLASH-PREVIEW"}
        save_resp = self.client.post(
            "/api/settings", data=json.dumps(save_payload), headers=self.headers
        )
        assert save_resp.status_code == 200, f"Save failed: {save_resp.data}"

    def test_invalid_gemini_model_rejected(self):
        """Verify invalid Gemini model is rejected."""
        save_payload = {"gemini_model": "not-a-real-model"}
        save_resp = self.client.post(
            "/api/settings", data=json.dumps(save_payload), headers=self.headers
        )

        # Should return error
        assert save_resp.status_code != 200, "Invalid Gemini model should be rejected"

    def test_non_boolean_debug_mode_rejected(self):
        """Verify non-boolean debug_mode is rejected (type validation)."""
        save_payload = {"debug_mode": "yes"}  # String instead of boolean
        save_resp = self.client.post(
            "/api/settings", data=json.dumps(save_payload), headers=self.headers
        )

        # Should return error
        assert save_resp.status_code != 200, "Non-boolean debug_mode should be rejected"

    def test_pre_spicy_model_provider_mismatch_rejected(self):
        """Verify model-provider mismatch is rejected (cross-validation)."""
        # Gemini model with OpenRouter provider should fail
        save_payload = {
            "pre_spicy_model": "gemini-3-flash-preview",
            "pre_spicy_provider": "openrouter",
        }
        save_resp = self.client.post(
            "/api/settings", data=json.dumps(save_payload), headers=self.headers
        )

        # Should return error for mismatch
        assert save_resp.status_code != 200, (
            "Model-provider mismatch should be rejected"
        )


if __name__ == "__main__":
    unittest.main()

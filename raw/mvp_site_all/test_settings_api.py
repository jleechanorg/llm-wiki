"""
Tests for settings page API endpoints in MCP architecture.
These tests verify that the API gateway properly handles settings requests.
"""

import os
import sys
import threading
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from google.api_core.exceptions import GoogleAPICallError

# Setup path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import create_app

from mvp_site import constants, firestore_service


class TestSettingsAPI(unittest.TestCase):
    """Tests for settings API endpoints in MCP architecture."""

    def setUp(self):
        """Set up test client and authentication headers."""
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
        self.test_user_id = "test-user-123"

        # Use stable test UID and stub Firebase verification - patch fully-qualified target
        self._auth_patcher = patch(
            "mvp_site.main.auth.verify_id_token",
            return_value={"uid": self.test_user_id},
        )
        self._auth_patcher.start()
        self.addCleanup(self._auth_patcher.stop)

        # Bypass Firestore during tests
        # Patch both locations: firestore_service (for direct calls) and world_logic (for imported reference)
        self._settings_get_patcher = patch(
            "mvp_site.firestore_service.get_user_settings", return_value={}
        )
        self._settings_get_wl_patcher = patch(
            "mvp_site.world_logic.get_user_settings", return_value={}
        )
        self._settings_update_patcher = patch(
            "mvp_site.firestore_service.update_user_settings", return_value=True
        )
        self._settings_get_patcher.start()
        self._settings_get_wl_patcher.start()
        self._settings_update_patcher.start()
        self.addCleanup(self._settings_get_patcher.stop)
        self.addCleanup(self._settings_get_wl_patcher.stop)
        self.addCleanup(self._settings_update_patcher.stop)

        # Test headers with Authorization token
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer test-id-token",
        }

    def test_settings_page_route_works(self):
        """Test that settings page route works in MCP architecture."""
        # Test with auth headers - should not crash
        response = self.client.get("/settings", headers=self.headers)
        # In MCP architecture, may return various status codes depending on server state
        assert response.status_code == 200, (
            "Settings page should return successfully with test headers"
        )

        # If successful, should return HTML
        if response.status_code == 200:
            assert len(response.data) > 0, "Should return content"

    def test_settings_api_endpoint_works(self):
        """Test that settings API endpoint works in MCP architecture."""
        response = self.client.get("/api/settings", headers=self.headers)

        # Should handle request gracefully in MCP architecture
        assert response.status_code == 200, (
            "Settings API should return successfully with test headers"
        )

        # Response should be valid JSON if successful
        if response.status_code == 200:
            try:
                data = response.get_json()
                assert isinstance(data, dict), "Settings should return dict"
                assert data.get("llm_provider") == constants.DEFAULT_LLM_PROVIDER
                assert data.get("gemini_model") == constants.DEFAULT_GEMINI_MODEL
            except Exception as e:
                self.fail(f"Response should be valid JSON: {e}")

    def test_update_settings_api_works(self):
        """Test that settings update API works in MCP architecture."""
        test_settings = {"gemini_model": "gemini-3-flash-preview", "debug_mode": True}

        response = self.client.post(
            "/api/settings", json=test_settings, headers=self.headers
        )

        # Should handle request gracefully in MCP architecture
        assert response.status_code == 200, (
            "Settings update should return successfully with valid data and test headers"
        )

        # Response should be valid JSON
        try:
            data = response.get_json()
            assert data is not None, "Should return valid JSON response"
        except Exception as e:
            # If not JSON, surface failure explicitly for debugging
            self.fail(f"Should handle non-JSON gracefully: {e}")

    def test_update_settings_allows_openrouter_provider(self):
        """Ensure OpenRouter provider and model settings save successfully."""

        test_settings = {
            "llm_provider": "openrouter",
            "openrouter_model": "meta-llama/llama-3.1-70b-instruct",
        }

        response = self.client.post(
            "/api/settings", json=test_settings, headers=self.headers
        )

        assert response.status_code == 200

    def test_update_settings_allows_cerebras_provider(self):
        """Ensure Cerebras provider and model settings save successfully."""

        test_settings = {
            "llm_provider": "cerebras",
            "cerebras_model": "llama-3.3-70b",  # Updated: 3.1-70b retired from Cerebras
        }

        response = self.client.post(
            "/api/settings", json=test_settings, headers=self.headers
        )

        assert response.status_code == 200

    def test_update_settings_allows_byok_api_keys(self):
        """Ensure BYOK API keys can be saved successfully."""
        test_settings = {
            "gemini_api_key": "test-gemini-key-long-enough",
            "openrouter_api_key": "test-openrouter-key-long-enough",
            "cerebras_api_key": "test-cerebras-key-long-enough",
        }

        response = self.client.post(
            "/api/settings", json=test_settings, headers=self.headers
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data.get("success") is True

    def test_switching_to_gemini_ignores_openclaw_gateway_validation(self):
        """Switch to Gemini should ignore invalid OpenClaw gateway inputs."""
        update_calls: list[tuple[str, dict[str, str]]] = []

        def fake_update_user_settings(
            user_id: str, settings_update: dict[str, str]
        ) -> bool:
            update_calls.append((user_id, settings_update))
            return True

        with (
            patch(
                "mvp_site.world_logic.get_user_settings",
                return_value={"llm_provider": "openclaw"},
            ),
            patch(
                "mvp_site.firestore_service.update_user_settings",
                side_effect=fake_update_user_settings,
            ),
        ):
            response = self.client.post(
                "/api/settings",
                json={
                    "llm_provider": "gemini",
                    "openclaw_gateway_url": "https://definitely-not-a-real-host-for-openclaw.example",
                },
                headers=self.headers,
            )

        assert response.status_code == 200
        assert update_calls, "Expected settings save call to run"
        _, settings_update = update_calls[0]
        assert "openclaw_gateway_url" not in settings_update

    def test_settings_api_masks_byok_keys(self):
        """Verify that BYOK API keys are never returned in plaintext in settings responses."""
        # Setup mock settings with keys
        mock_settings = {
            "gemini_api_key": "secret-gemini-key",
            "openrouter_api_key": "secret-openrouter-key",
            "cerebras_api_key": "secret-cerebras-key",
            "llm_provider": "gemini",
            "gemini_model": constants.DEFAULT_GEMINI_MODEL,
        }

        with patch(
            "mvp_site.world_logic.get_user_settings", return_value=mock_settings
        ):
            response = self.client.get("/api/settings", headers=self.headers)
            assert response.status_code == 200
            data = response.get_json()

            # Verify keys are removed from the top-level response
            # (Note: API response is usually wrapped in success: true, so check data['data'] if wrapped)
            settings_data = data
            if "data" in data and isinstance(data["data"], dict):
                settings_data = data["data"]

            assert "gemini_api_key" not in settings_data
            assert "openrouter_api_key" not in settings_data
            assert "cerebras_api_key" not in settings_data

            # Verify status flags are present and correct
            assert settings_data.get("has_custom_gemini_key") is True
            assert settings_data.get("has_custom_openrouter_key") is True
            assert settings_data.get("has_custom_cerebras_key") is True

    def test_reveal_key_endpoint_returns_key_for_valid_provider(self):
        """Reveal endpoint should return plaintext key only for explicit provider request."""
        mock_settings = {
            "gemini_api_key": "secret-gemini-key",
            "llm_provider": "gemini",
            "gemini_model": constants.DEFAULT_GEMINI_MODEL,
        }

        with patch(
            "mvp_site.world_logic.get_user_settings", return_value=mock_settings
        ):
            response = self.client.post(
                "/api/settings/reveal-key",
                json={"provider": "gemini"},
                headers=self.headers,
            )
            assert response.status_code == 200
            data = response.get_json()
            assert data.get("success") is True
            assert data.get("provider") == "gemini"
            assert data.get("api_key") == "secret-gemini-key"

    def test_reveal_key_endpoint_returns_openclaw_gateway_token(self):
        """Reveal endpoint must look up openclaw_gateway_token (not openclaw_api_key)."""
        mock_settings = {
            "openclaw_gateway_token": "secret-openclaw-token",
            "llm_provider": "openclaw",
        }

        with patch(
            "mvp_site.world_logic.get_user_settings", return_value=mock_settings
        ):
            response = self.client.post(
                "/api/settings/reveal-key",
                json={"provider": "openclaw"},
                headers=self.headers,
            )
            assert response.status_code == 200
            data = response.get_json()
            assert data.get("success") is True
            assert data.get("provider") == "openclaw"
            assert data.get("api_key") == "secret-openclaw-token"

    def test_reveal_key_endpoint_rejects_invalid_provider(self):
        response = self.client.post(
            "/api/settings/reveal-key",
            json={"provider": "bad-provider"},
            headers=self.headers,
        )
        assert response.status_code == 400

    def test_test_openclaw_connection_endpoint_works_with_patched_provider(self):
        """Connection test endpoint should call provider test helper and report success."""
        with patch(
            "mvp_site.llm_providers.openclaw_provider.test_openclaw_gateway_connection",
            return_value={
                "success": True,
                "gateway_url": "http://127.0.0.1:18789",
                "status_code": 200,
                "mode": "chat_completions",
            },
        ) as mock_test:
            response = self.client.post(
                "/api/settings/test-openclaw-connection",
                json={
                    "openclaw_gateway_port": 18889,
                    "openclaw_gateway_token": "abcdefghi-jklmnop-12345",
                },
                headers=self.headers,
            )

            assert response.status_code == 200
            data = response.get_json()
            assert data.get("success") is True
            assert data.get("gateway_url") == "http://127.0.0.1:18789"
            assert data.get("status_code") == 200
            mock_test.assert_called_once_with(
                gateway_url=None,
                gateway_port=18889,
                gateway_token="abcdefghi-jklmnop-12345",
                proof_prompt=None,
            )

    def test_test_openclaw_connection_endpoint_rejects_invalid_payload(self):
        """Invalid token payload should return a validation error."""
        response = self.client.post(
            "/api/settings/test-openclaw-connection",
            json={"openclaw_gateway_token": "short"},
            headers=self.headers,
        )
        assert response.status_code == 400
        data = response.get_json()
        assert (
            data.get("error") == "Invalid OpenClaw gateway token - token is too short"
        )

    def test_test_openclaw_connection_uses_raw_firestore_token_when_payload_omits_it(
        self,
    ):
        """Regression: when the browser omits the token (masked placeholder → key deleted),
        the endpoint must read the raw token from Firestore, not the stripped settings response.

        Bug: get_user_settings_unified strips sensitive fields; using loaded_settings fallback
        returned "" and the gateway got no Authorization header → 401 Unauthorized.
        Fix: read raw Firestore settings when token absent from payload.
        """
        stored_token = "raw-secret-token-from-firestore-12345"
        with (
            patch(
                "mvp_site.firestore_service.get_user_settings",
                return_value={"openclaw_gateway_token": stored_token},
            ),
            patch(
                "mvp_site.world_logic.get_user_settings",
                return_value={"openclaw_gateway_token": stored_token},
            ),
            patch(
                "mvp_site.llm_providers.openclaw_provider.test_openclaw_gateway_connection",
                return_value={
                    "success": True,
                    "gateway_url": "http://127.0.0.1:18789",
                    "status_code": 200,
                    "mode": "models",
                },
            ) as mock_test,
        ):
            # Mimic browser: no openclaw_gateway_token key in payload (masked → deleted)
            response = self.client.post(
                "/api/settings/test-openclaw-connection",
                json={"openclaw_gateway_port": 18789},
                headers=self.headers,
            )

            assert response.status_code == 200
            data = response.get_json()
            assert data.get("success") is True
            # Verify the raw Firestore token was forwarded to the provider, not ""
            _call_kwargs = mock_test.call_args[1]
            assert _call_kwargs["gateway_token"] == stored_token

    def test_update_and_clear_byok_key_reflects_has_custom_flag(self):
        """Verify saving then clearing a BYOK key flips has_custom_gemini_key correctly."""
        store = {"gemini_api_key": "secret-gemini-key"}

        def fake_get_user_settings(user_id: str) -> dict[str, str]:
            return dict(store)

        def fake_update_user_settings(
            user_id: str, settings_update: dict[str, str]
        ) -> bool:
            value = settings_update.get("gemini_api_key")
            if value is None:
                return True
            if value == "":
                store.pop("gemini_api_key", None)
            else:
                store["gemini_api_key"] = value
            return True

        with (
            patch(
                "mvp_site.world_logic.get_user_settings",
                side_effect=fake_get_user_settings,
            ),
            patch(
                "mvp_site.firestore_service.update_user_settings",
                side_effect=fake_update_user_settings,
            ),
        ):
            save_response = self.client.post(
                "/api/settings",
                json={"gemini_api_key": "new-gemini-key-123456"},
                headers=self.headers,
            )
            assert save_response.status_code == 200

            clear_response = self.client.post(
                "/api/settings",
                json={"gemini_api_key": ""},
                headers=self.headers,
            )
            assert clear_response.status_code == 200

            get_response = self.client.get("/api/settings", headers=self.headers)
            assert get_response.status_code == 200
            settings_data = get_response.get_json()
            assert settings_data.get("has_custom_gemini_key") is False
            assert "gemini_api_key" not in settings_data

    def test_settings_endpoints_auth_behavior(self):
        """Test that settings endpoints handle authentication in MCP architecture."""
        # Test without auth headers
        no_auth_response = self.client.get("/api/settings")

        # Should either require auth (401) or handle gracefully (500)
        assert no_auth_response.status_code == 401, (
            "Should require authentication without test headers"
        )

        # Test with auth headers
        auth_response = self.client.get("/api/settings", headers=self.headers)

        # Should not return 401 when auth headers are provided
        assert auth_response.status_code != 401, (
            "Should not return 401 when auth headers provided"
        )

    def test_openclaw_frontend_download_script_matches_canonical_script(self):
        """Downloaded frontend script must stay in sync with canonical script."""
        repo_root = Path(__file__).resolve().parents[2]
        canonical_path = repo_root / "scripts" / "openclaw_tailscale_tunnel.sh"
        frontend_path = (
            repo_root / "mvp_site" / "frontend_v1" / "openclaw_gateway_tunnel.sh"
        )

        canonical = canonical_path.read_text(encoding="utf-8")
        frontend = frontend_path.read_text(encoding="utf-8")

        assert frontend == canonical, (
            "Frontend downloadable script diverged from canonical script; "
            "update mvp_site/frontend_v1/openclaw_gateway_tunnel.sh to match "
            "scripts/openclaw_tailscale_tunnel.sh exactly."
        )


class TestPersonalAccessToken(unittest.TestCase):
    """Tests for the /api/settings/personal-access-token endpoint."""

    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
        self.test_user_id = "test-user-pat-456"

        self._auth_patcher = patch(
            "mvp_site.main.auth.verify_id_token",
            return_value={"uid": self.test_user_id},
        )
        self._auth_patcher.start()
        self.addCleanup(self._auth_patcher.stop)

        self._settings_get_patcher = patch(
            "mvp_site.firestore_service.get_user_settings", return_value={}
        )
        self._settings_get_patcher.start()
        self.addCleanup(self._settings_get_patcher.stop)

        self._settings_update_patcher = patch(
            "mvp_site.firestore_service.update_user_settings", return_value=True
        )
        self._settings_update_patcher.start()
        self.addCleanup(self._settings_update_patcher.stop)

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer test-id-token",
        }

    def test_generate_returns_worldai_token(self):
        """Generated token must have 'worldai_' prefix and be 72 chars total."""
        with patch(
            "mvp_site.firestore_service.rotate_personal_api_key", return_value=True
        ):
            resp = self.client.post(
                "/api/settings/personal-access-token",
                json={"action": "generate"},
                headers=self.headers,
            )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data["success"])
        token = data["token"]
        self.assertTrue(
            token.startswith("worldai_"), f"Token must start with 'worldai_': {token}"
        )
        # "worldai_" (8) + 64 hex chars = 72
        self.assertEqual(len(token), 72, f"Expected 72 chars, got {len(token)}")

    def test_generate_no_cache_headers(self):
        """Generate response must have no-store Cache-Control."""
        with patch(
            "mvp_site.firestore_service.rotate_personal_api_key", return_value=True
        ):
            resp = self.client.post(
                "/api/settings/personal-access-token",
                json={"action": "generate"},
                headers=self.headers,
            )
        self.assertIn("no-store", resp.headers.get("Cache-Control", ""))

    def test_generate_atomic_transaction_called(self):
        """Generate uses rotate_personal_api_key (transaction), not separate store+update."""
        with patch(
            "mvp_site.firestore_service.rotate_personal_api_key", return_value=True
        ) as mock_rotate:
            self.client.post(
                "/api/settings/personal-access-token",
                json={"action": "generate"},
                headers=self.headers,
            )
        mock_rotate.assert_called_once()
        args = mock_rotate.call_args[0]
        self.assertEqual(args[0], self.test_user_id)  # user_id
        self.assertRegex(args[1], r"^[0-9a-f]{64}$")  # new sha256 hash
        # old_hash is no longer passed — transaction reads it from Firestore internally
        self.assertEqual(len(args), 2)

    def test_generate_returns_500_when_transaction_fails(self):
        """Generate returns 500 if the atomic transaction fails."""
        with patch(
            "mvp_site.firestore_service.rotate_personal_api_key", return_value=False
        ):
            resp = self.client.post(
                "/api/settings/personal-access-token",
                json={"action": "generate"},
                headers=self.headers,
            )
        self.assertEqual(resp.status_code, 500)

    def test_generate_passes_only_user_id_and_new_hash_to_rotate(self):
        """rotate_personal_api_key receives exactly (user_id, new_hash) — no old_hash arg.

        old_hash is read from Firestore inside the transaction, not passed from main.py,
        so concurrent generate requests cannot race on a stale pre-read value.
        """
        captured_args = []

        def capturing_rotate(user_id, new_hash):
            captured_args.extend([user_id, new_hash])
            return True

        with patch(
            "mvp_site.firestore_service.rotate_personal_api_key",
            side_effect=capturing_rotate,
        ):
            self.client.post(
                "/api/settings/personal-access-token",
                json={"action": "generate"},
                headers=self.headers,
            )

        self.assertEqual(
            len(captured_args), 2, "Must receive exactly 2 positional args"
        )
        self.assertEqual(captured_args[0], self.test_user_id)
        self.assertRegex(captured_args[1], r"^[0-9a-f]{64}$")

    def test_concurrent_generate_calls_rotate_twice(self):
        """Two concurrent generate requests each succeed and produce distinct tokens.

        rotate_personal_api_key uses @firestore.transactional, so both callers get a
        unique key and neither errors.  The mock simulates that transactional safety:
        both calls return True and the tokens generated by the endpoint are unique.
        """
        results = []
        lock = threading.Lock()

        def do_request():
            # Each thread gets its own test client to avoid shared request-context state.
            client = self.app.test_client()
            resp = client.post(
                "/api/settings/personal-access-token",
                json={"action": "generate"},
                headers=self.headers,
            )
            with lock:
                results.append(resp)

        with patch(
            "mvp_site.firestore_service.rotate_personal_api_key", return_value=True
        ) as mock_rotate:
            t1 = threading.Thread(target=do_request)
            t2 = threading.Thread(target=do_request)
            t1.start()
            t2.start()
            t1.join()
            t2.join()

        # Both requests must have completed.
        self.assertEqual(len(results), 2)

        # Neither call returns an error.
        for resp in results:
            self.assertEqual(
                resp.status_code, 200, f"Unexpected status: {resp.get_json()}"
            )
            data = resp.get_json()
            self.assertTrue(data["success"])

        # rotate_personal_api_key was called exactly once per request.
        self.assertEqual(mock_rotate.call_count, 2)

        # Both responses return a valid worldai_ token.
        tokens = [resp.get_json()["token"] for resp in results]
        for token in tokens:
            self.assertTrue(
                token.startswith("worldai_"),
                f"Token must start with 'worldai_': {token}",
            )
            self.assertEqual(len(token), 72, f"Expected 72 chars, got {len(token)}")

        # The two concurrent requests must have generated distinct tokens
        # (each generates its own random key independently).
        self.assertNotEqual(
            tokens[0], tokens[1], "Concurrent requests must produce unique tokens"
        )

    def test_revoke_calls_atomic_transaction(self):
        """Revoking calls revoke_personal_api_key (atomic transaction) with the user_id."""
        with patch(
            "mvp_site.firestore_service.revoke_personal_api_key", return_value=True
        ) as mock_revoke:
            resp = self.client.post(
                "/api/settings/personal-access-token",
                json={"action": "revoke"},
                headers=self.headers,
            )
            self.assertEqual(resp.status_code, 200)
            data = resp.get_json()
            self.assertTrue(data["success"])
            self.assertTrue(data["revoked"])
            mock_revoke.assert_called_once_with(self.test_user_id)

    def test_revoke_returns_500_when_transaction_fails(self):
        """Revoke returns 500 (not 200) when the Firestore transaction fails."""
        with patch(
            "mvp_site.firestore_service.revoke_personal_api_key", return_value=False
        ):
            resp = self.client.post(
                "/api/settings/personal-access-token",
                json={"action": "revoke"},
                headers=self.headers,
            )
        self.assertEqual(resp.status_code, 500)

    def test_revoke_no_key_still_succeeds(self):
        """Revoking when no key exists returns 200 — the transaction handles the no-op."""
        with patch(
            "mvp_site.firestore_service.revoke_personal_api_key", return_value=True
        ):
            resp = self.client.post(
                "/api/settings/personal-access-token",
                json={"action": "revoke"},
                headers=self.headers,
            )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data["success"])
        self.assertTrue(data["revoked"])

    def test_invalid_action_returns_400(self):
        """Unknown action returns 400."""
        resp = self.client.post(
            "/api/settings/personal-access-token",
            json={"action": "nuke"},
            headers=self.headers,
        )
        self.assertEqual(resp.status_code, 400)

    def test_unauthenticated_returns_401(self):
        """Request without Authorization header returns 401."""
        resp = self.client.post(
            "/api/settings/personal-access-token",
            json={"action": "generate"},
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(resp.status_code, 401)


class TestPersonalApiKeyAuth(unittest.TestCase):
    """Tests for the personal API key auth branch in check_token."""

    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
        self.test_user_id = "key-auth-user-789"
        self.raw_key = "worldai_" + "a" * 64

        patch(
            "mvp_site.firestore_service.update_user_settings", return_value=True
        ).start()
        self.addCleanup(patch.stopall)

    def test_valid_worldai_key_authenticates(self):
        """A valid 'worldai_' Bearer token authenticates via Firestore lookup."""
        import hashlib

        key_hash = hashlib.sha256(self.raw_key.encode()).hexdigest()

        with patch(
            "mvp_site.firestore_service.lookup_personal_api_key",
            return_value=(self.test_user_id, None),
        ) as mock_lookup:
            with patch("mvp_site.firestore_service.get_user_settings", return_value={}):
                resp = self.client.get(
                    "/api/settings",
                    headers={"Authorization": f"Bearer {self.raw_key}"},
                )
            mock_lookup.assert_called_once_with(key_hash)
        self.assertEqual(resp.status_code, 200)

    def test_invalid_worldai_key_returns_401(self):
        """An unknown 'worldai_' Bearer token returns 401."""
        with patch(
            "mvp_site.firestore_service.lookup_personal_api_key",
            return_value=(None, None),
        ):
            resp = self.client.get(
                "/api/settings",
                headers={"Authorization": f"Bearer {self.raw_key}"},
            )
        self.assertEqual(resp.status_code, 401)

    def test_firebase_token_still_works(self):
        """Normal Firebase Bearer tokens still route through Firebase verification."""
        with (
            patch(
                "mvp_site.main.auth.verify_id_token",
                return_value={"uid": self.test_user_id},
            ),
            patch("mvp_site.firestore_service.get_user_settings", return_value={}),
        ):
            resp = self.client.get(
                "/api/settings",
                headers={"Authorization": "Bearer firebase-style-token"},
            )
        self.assertEqual(resp.status_code, 200)

    def test_worldai_key_authenticates_mcp_endpoint_directly(self):
        """`worldai_` key must authenticate POST /mcp — the actual MCP route."""
        import hashlib

        key_hash = hashlib.sha256(self.raw_key.encode()).hexdigest()
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {},
        }
        # /mcp uses @check_token — worldai_ key must pass through to the handler
        with patch(
            "mvp_site.firestore_service.lookup_personal_api_key",
            return_value=(self.test_user_id, None),
        ) as mock_lookup:
            with patch(
                "mvp_site.mcp_api.handle_jsonrpc",
                return_value=(
                    {"jsonrpc": "2.0", "id": 1, "result": {"tools": []}},
                    None,
                ),
            ):
                resp = self.client.post(
                    "/mcp",
                    json=mcp_request,
                    headers={
                        "Authorization": f"Bearer {self.raw_key}",
                        "Content-Type": "application/json",
                    },
                )
        # auth passed (not 401/403) — handler was reached
        self.assertNotEqual(
            resp.status_code, 401, "worldai_ key should authenticate /mcp"
        )
        self.assertNotEqual(
            resp.status_code, 403, "worldai_ key should not be forbidden on /mcp"
        )
        mock_lookup.assert_called_once_with(key_hash)

    def test_invalid_worldai_key_blocked_on_mcp_endpoint(self):
        """Invalid `worldai_` key returns 401 on /mcp — not silently allowed."""
        mcp_request = {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}
        with patch(
            "mvp_site.firestore_service.lookup_personal_api_key",
            return_value=(None, None),
        ):
            resp = self.client.post(
                "/mcp",
                json=mcp_request,
                headers={
                    "Authorization": f"Bearer {self.raw_key}",
                    "Content-Type": "application/json",
                },
            )
        self.assertEqual(resp.status_code, 401)


class TestLookupPersonalApiKeyTupleContract(unittest.TestCase):
    """Direct unit tests for lookup_personal_api_key tuple contract.

    Covers: uid+email tuple return, missing doc, missing uid, best-effort email.
    """

    def test_returns_tuple_of_uid_and_email_when_both_found(self):
        """Returns (uid, email) when api_keys doc and users doc both exist."""
        fake_api_key_doc = MagicMock()
        fake_api_key_doc.exists = True
        fake_api_key_doc.to_dict.return_value = {"uid": "test-uid-abc"}

        fake_user_doc = MagicMock()
        fake_user_doc.exists = True
        fake_user_doc.to_dict.return_value = {"email": "test@example.com"}

        fake_db = MagicMock()
        # Each collection() call gets its own mock chain
        fake_db.collection.side_effect = [
            # First call: collection("api_keys").document(key_hash).get()
            MagicMock(
                document=MagicMock(
                    return_value=MagicMock(get=MagicMock(return_value=fake_api_key_doc))
                )
            ),
            # Second call: collection("users").document(uid).get()
            MagicMock(
                document=MagicMock(
                    return_value=MagicMock(get=MagicMock(return_value=fake_user_doc))
                )
            ),
        ]

        with patch("mvp_site.firestore_service.get_db", return_value=fake_db):
            uid, email = firestore_service.lookup_personal_api_key("somehash")

        self.assertEqual(uid, "test-uid-abc")
        self.assertEqual(email, "test@example.com")

    def test_returns_tuple_with_none_email_when_user_doc_missing(self):
        """Returns (uid, None) when api_keys doc exists but user email lookup raises."""
        fake_api_key_doc = MagicMock()
        fake_api_key_doc.exists = True
        fake_api_key_doc.to_dict.return_value = {"uid": "test-uid-abc"}

        fake_db = MagicMock()
        fake_db.collection.side_effect = [
            # First call: collection("api_keys").document(key_hash).get()
            MagicMock(
                document=MagicMock(
                    return_value=MagicMock(get=MagicMock(return_value=fake_api_key_doc))
                )
            ),
            # Second call: collection("users").document(uid).get() — raises
            MagicMock(
                document=MagicMock(
                    return_value=MagicMock(
                        get=MagicMock(
                            side_effect=GoogleAPICallError("user doc read failed")
                        )
                    )
                )
            ),
        ]

        with patch("mvp_site.firestore_service.get_db", return_value=fake_db):
            uid, email = firestore_service.lookup_personal_api_key("somehash")

        self.assertEqual(uid, "test-uid-abc")
        self.assertIsNone(email)

    def test_returns_none_tuple_when_api_key_doc_missing(self):
        """Returns (None, None) when api_keys doc does not exist."""
        fake_db = MagicMock()
        fake_db.collection.return_value.document.return_value.get.return_value = (
            MagicMock(exists=False)
        )

        with patch("mvp_site.firestore_service.get_db", return_value=fake_db):
            uid, email = firestore_service.lookup_personal_api_key("badhash")

        self.assertIsNone(uid)
        self.assertIsNone(email)

    def test_returns_none_tuple_when_uid_missing_from_doc(self):
        """Returns (None, None) when api_keys doc exists but uid field is absent."""
        fake_api_key_doc = MagicMock()
        fake_api_key_doc.exists = True
        fake_api_key_doc.to_dict.return_value = {}  # no uid

        fake_db = MagicMock()
        fake_db.collection.return_value.document.return_value.get.return_value = (
            fake_api_key_doc
        )

        with patch("mvp_site.firestore_service.get_db", return_value=fake_db):
            uid, email = firestore_service.lookup_personal_api_key("somehash")

        self.assertIsNone(uid)
        self.assertIsNone(email)

    def test_returns_none_when_uid_is_not_a_string(self):
        """Returns (None, None) when uid field is present but not a string."""
        fake_api_key_doc = MagicMock()
        fake_api_key_doc.exists = True
        fake_api_key_doc.to_dict.return_value = {"uid": 12345}  # uid as int, not str

        fake_db = MagicMock()
        fake_db.collection.side_effect = [
            MagicMock(
                document=MagicMock(
                    return_value=MagicMock(get=MagicMock(return_value=fake_api_key_doc))
                )
            ),
        ]

        with patch("mvp_site.firestore_service.get_db", return_value=fake_db):
            uid, email = firestore_service.lookup_personal_api_key("somehash")

        self.assertIsNone(uid)
        self.assertIsNone(email)

    def test_coerces_non_string_email_to_string(self):
        """Non-string email (e.g. int 123) is coerced to str to prevent downstream .lower() crashes."""
        fake_api_key_doc = MagicMock()
        fake_api_key_doc.exists = True
        fake_api_key_doc.to_dict.return_value = {"uid": "test-uid-abc"}

        fake_user_doc = MagicMock()
        fake_user_doc.exists = True
        fake_user_doc.to_dict.return_value = {"email": 123}  # int, not str

        fake_db = MagicMock()
        fake_db.collection.side_effect = [
            MagicMock(
                document=MagicMock(
                    return_value=MagicMock(get=MagicMock(return_value=fake_api_key_doc))
                )
            ),
            MagicMock(
                document=MagicMock(
                    return_value=MagicMock(get=MagicMock(return_value=fake_user_doc))
                )
            ),
        ]

        with patch("mvp_site.firestore_service.get_db", return_value=fake_db):
            uid, email = firestore_service.lookup_personal_api_key("somehash")

        self.assertEqual(uid, "test-uid-abc")
        self.assertEqual(email, "123")  # coerced from int 123 to str "123"


if __name__ == "__main__":
    unittest.main()

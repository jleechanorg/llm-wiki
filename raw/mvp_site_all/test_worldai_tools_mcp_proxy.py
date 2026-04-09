"""Unit tests for WorldAI tools MCP proxy runtime."""

from __future__ import annotations

import http.client
import json
import socket
import threading
import unittest
from datetime import datetime, timezone
from http.server import ThreadingHTTPServer
from unittest import mock

import requests

from mvp_site.worldai_tools_mcp_proxy import (
    MAX_REQUEST_SIZE,
    AuthContext,
    LOCAL_TOOL_SCHEMAS,
    ProxyJsonRpcError,
    WorldAIToolsProxy,
    _build_auth_context,
    _build_auth_context_for_stdio,
    _validate_deploy_confirm_token,
    create_proxy_handler,
)


class WorldAIToolsMCPProxyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.proxy = WorldAIToolsProxy("http://127.0.0.1:65535/mcp")
        self.auth = AuthContext(
            actor_user_id="user-1",
            actor_email=None,
            roles={"support_admin", "ops_admin", "deploy_admin"},
        )

    def test_local_tools_catalog_contains_expected_names(self):
        names = {tool["name"] for tool in LOCAL_TOOL_SCHEMAS}
        self.assertIn("diag_evaluate_campaign_dice", names)
        self.assertIn("admin_copy_campaign_user_to_user", names)
        self.assertIn("admin_download_campaign", names)
        self.assertIn("admin_download_campaign_entries", names)
        self.assertIn("ops_gcloud_logs_read", names)
        self.assertIn("ops_firestore_read_document", names)
        self.assertIn("ops_firestore_query_collection_group", names)
        self.assertIn("ops_run_mcp_local", names)
        self.assertIn("ops_run_mcp_production", names)
        self.assertIn("ops_deploy_mcp_service", names)

    def test_admin_tools_require_reason_and_ticket(self):
        request = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "tools/call",
            "params": {
                "name": "admin_download_campaign",
                "arguments": {
                    "target_user_id": "u",
                    "campaign_id": "c",
                    "ticket_id": "INC-1",
                },
            },
        }
        response = self.proxy.handle_jsonrpc(request, self.auth)
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32602)
        self.assertIn("reason", response["error"]["message"])

    def test_deploy_confirm_token_accepts_exact_format(self):
        fresh_timestamp = datetime.now(tz=timezone.utc).strftime("%Y%m%d-%H%M%S")
        _validate_deploy_confirm_token(f"DEPLOY-prod-{fresh_timestamp}", "prod")
        _validate_deploy_confirm_token(f"DEPLOY-preview-{fresh_timestamp}", "preview")

    def test_deploy_confirm_token_rejects_wrong_target(self):
        with self.assertRaises(ProxyJsonRpcError) as cm:
            _validate_deploy_confirm_token("DEPLOY-preview-20260303-091500", "prod")
        self.assertIn("does not match", str(cm.exception))

    def test_deploy_confirm_token_rejects_invalid_shape(self):
        with self.assertRaises(ProxyJsonRpcError) as cm:
            _validate_deploy_confirm_token("DEPLOY-prod-2026", "prod")
        self.assertIn("confirm must be", str(cm.exception))


    def test_gcloud_logs_rejects_invalid_service_name(self):
        """ops_gcloud_logs_read rejects service names with injection chars."""
        request = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "tools/call",
            "params": {
                "name": "ops_gcloud_logs_read",
                "arguments": {
                    "service": "my-service AND severity>=DEBUG",
                    "project_id": "test-project",
                    "reason": "test",
                    "ticket_id": "INC-1",
                },
            },
        }
        response = self.proxy.handle_jsonrpc(request, self.auth)
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32602)
        self.assertIn("invalid", response["error"]["message"].lower())

    def test_gcloud_logs_rejects_invalid_severity(self):
        """ops_gcloud_logs_read rejects severity values not in the known set."""
        request = {
            "jsonrpc": "2.0",
            "id": "2",
            "method": "tools/call",
            "params": {
                "name": "ops_gcloud_logs_read",
                "arguments": {
                    "service": "valid-service",
                    "project_id": "test-project",
                    "severity": "BADLEVEL OR 1=1",
                    "reason": "test",
                    "ticket_id": "INC-1",
                },
            },
        }
        response = self.proxy.handle_jsonrpc(request, self.auth)
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32602)

    @mock.patch("mvp_site.worldai_tools_mcp_proxy._run_command")
    def test_diag_evaluate_campaign_dice_wires_include_recent_and_parses_entries(self, run_command):
        run_command.return_value = mock.Mock(
            command=["python", "scripts/audit_dice_rolls.py"],
            exit_code=0,
            stdout=(
                "Total rolls with results: 7/7\n"
                "Entries with dice rolls: 3\n"
                "By source: {\"chat\": 7}\n"
            ),
            stderr="",
        )

        request = {
            "jsonrpc": "2.0",
            "id": "3",
            "method": "tools/call",
            "params": {
                "name": "diag_evaluate_campaign_dice",
                "arguments": {
                    "campaign_id": "camp-1",
                    "include_recent": 33,
                },
            },
        }

        response = self.proxy.handle_jsonrpc(request, self.auth)
        self.assertIn("result", response)
        content = response["result"]["content"][0]["text"]
        self.assertIn('"entries_with_dice": 3', content)

        called_command = run_command.call_args.args[0]
        self.assertIn("--recent", called_command)
        self.assertIn("33", called_command)

    @mock.patch("mvp_site.worldai_tools_mcp_proxy._run_command")
    def test_diag_evaluate_campaign_dice_raises_when_by_source_is_malformed(self, run_command):
        run_command.return_value = mock.Mock(
            command=["python", "scripts/audit_dice_rolls.py"],
            exit_code=0,
            stdout=(
                "Total rolls with results: 7/7\n"
                "Entries with dice rolls: 3\n"
                "By source: {invalid-json}\n"
            ),
            stderr="boom",
        )

        with self.assertRaises(ProxyJsonRpcError) as ctx:
            self.proxy._tool_diag_evaluate_campaign_dice(
                {"campaign_id": "camp-1", "include_recent": 20},
                self.auth,
            )

        self.assertEqual(ctx.exception.code, -32020)
        self.assertIn("Failed to parse dice audit by_source summary", str(ctx.exception))

    @mock.patch.dict("os.environ", {
        "WORLDTOOLS_SUPPORT_ADMINS": "verified@example.com",
        "WORLDTOOLS_TRUST_ACTOR_EMAIL_HEADERS": "false",
    }, clear=False)
    def test_untrusted_actor_email_header_does_not_grant_roles(self):
        proxy = WorldAIToolsProxy("http://127.0.0.1:65535/mcp")
        auth = _build_auth_context({
            "X-Worldtools-Actor-Email": "verified@example.com",
        }, proxy)
        self.assertEqual(auth.roles, set())

    @mock.patch.dict("os.environ", {
        "WORLDTOOLS_SUPPORT_ADMINS": "verified@example.com",
        "WORLDTOOLS_TRUST_ACTOR_EMAIL_HEADERS": "true",
    }, clear=False)
    def test_trusted_actor_email_header_grants_roles(self):
        proxy = WorldAIToolsProxy("http://127.0.0.1:65535/mcp")
        auth = _build_auth_context({
            "X-Worldtools-Actor-Email": "verified@example.com",
        }, proxy)
        self.assertIn("support_admin", auth.roles)

    @mock.patch.dict("os.environ", {
        "WORLDTOOLS_SUPPORT_ADMINS": "verified@example.com",
        "WORLDTOOLS_ACTOR_EMAIL": "verified@example.com",
        "WORLDTOOLS_TRUST_ACTOR_EMAIL_HEADERS": "true",
    }, clear=False)
    def test_build_auth_context_for_stdio_populates_roles(self):
        """Stdio adapter: actor email from env + trust flag grants roles."""
        proxy = WorldAIToolsProxy("http://127.0.0.1:65535/mcp")
        auth = _build_auth_context_for_stdio(proxy)
        self.assertIn("support_admin", auth.roles)

    @mock.patch.dict("os.environ", {
        "WORLDTOOLS_SUPPORT_ADMINS": "verified@example.com",
        "WORLDTOOLS_ACTOR_EMAIL": "verified@example.com",
        "WORLDTOOLS_TRUST_ACTOR_EMAIL_HEADERS": "false",
    }, clear=False)
    def test_build_auth_context_for_stdio_respects_trust_flag(self):
        """Stdio adapter: without trust flag, roles stay empty."""
        proxy = WorldAIToolsProxy("http://127.0.0.1:65535/mcp")
        auth = _build_auth_context_for_stdio(proxy)
        self.assertEqual(auth.roles, set())

    def test_deploy_confirm_token_rejects_stale_timestamp(self):
        with self.assertRaisesRegex(ProxyJsonRpcError, "stale"):
            _validate_deploy_confirm_token("DEPLOY-prod-20200101-000000", "prod")

    def test_deploy_confirm_token_rejects_unscoped_confirmed_literal(self):
        with self.assertRaisesRegex(ProxyJsonRpcError, "confirm must be"):
            _validate_deploy_confirm_token("CONFIRMED", "prod")

    def test_dry_run_copy_campaign_skips_subcollection_reads(self):
        class _Doc:
            exists = True

            @staticmethod
            def to_dict():
                return {"title": "campaign"}

        class _Collection:
            @staticmethod
            def document(*_args, **_kwargs):
                return _DocumentRef()

        class _DocumentRef:
            @staticmethod
            def collection(*_args, **_kwargs):
                class _NoStreamCollection:
                    @staticmethod
                    def stream():
                        raise AssertionError("dry_run should not stream subcollections")

                return _NoStreamCollection()

            @staticmethod
            def get():
                return _Doc()

        class _DB:
            @staticmethod
            def collection(_name):
                return _Collection()

        with mock.patch("mvp_site.worldai_tools_mcp_proxy._get_firestore_db", return_value=_DB()):
            result = self.proxy._tool_admin_copy_campaign_user_to_user(
                {
                    "source_user_id": "source",
                    "source_campaign_id": "camp",
                    "dest_user_id": "dest",
                    "dry_run": True,
                },
                self.auth,
            )

        self.assertTrue(result["dry_run"])

    def test_download_entries_rejects_invalid_timestamp_as_invalid_params(self):
        with self.assertRaisesRegex(ProxyJsonRpcError, "from_timestamp/to_timestamp") as ctx:
            self.proxy._tool_admin_download_campaign_entries(
                {
                    "target_user_id": "u1",
                    "campaign_id": "c1",
                    "from_timestamp": "invalid",
                    "to_timestamp": "invalid",
                },
                self.auth,
            )

        self.assertEqual(ctx.exception.code, -32602)

    @mock.patch("requests.post")
    def test_upstream_non_json_response_includes_body_preview(self, mock_post):
        """Upstream JSONDecodeError raises ProxyJsonRpcError with body_preview."""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Expecting value", "", 0)
        mock_response.text = "Internal Server Error from upstream"
        mock_post.return_value = mock_response

        with self.assertRaises(ProxyJsonRpcError) as ctx:
            self.proxy._passthrough_jsonrpc("tools/list", {}, "1")

        self.assertEqual(ctx.exception.code, -32033)
        self.assertIsNotNone(ctx.exception.data)
        self.assertIn("body_preview", ctx.exception.data)
        self.assertIn("Internal Server Error", ctx.exception.data["body_preview"])

    def test_http_handler_rejects_oversized_payload_with_413(self):
        """Content-Length > MAX_REQUEST_SIZE returns 413, handle_jsonrpc not called."""
        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            port = s.getsockname()[1]

        proxy = WorldAIToolsProxy("http://127.0.0.1:65535/mcp")
        proxy.handle_jsonrpc = mock.Mock(return_value={"jsonrpc": "2.0", "id": "x", "result": {}})
        handler = create_proxy_handler(proxy)
        server = ThreadingHTTPServer(("127.0.0.1", port), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()

        try:
            body = b"x" * (MAX_REQUEST_SIZE + 1)
            response = requests.post(
                f"http://127.0.0.1:{port}/mcp",
                data=body,
                headers={"Content-Type": "application/json"},
                timeout=5,
            )
            self.assertEqual(response.status_code, 413)
            data = json.loads(response.text)
            self.assertIn("error", data)
            self.assertEqual(data["error"]["code"], -32600)
            proxy.handle_jsonrpc.assert_not_called()
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)

class TestProxyBearerTokenForwarding(unittest.TestCase):
    """Verify WORLDTOOLS_BEARER_TOKEN is forwarded as Authorization header upstream.

    This closes the end-to-end MCP personal API key flow:
      user token  →  worldai_mcp_stdio (env WORLDTOOLS_BEARER_TOKEN)
                  →  _passthrough_jsonrpc sends Authorization: Bearer <token>
                  →  upstream server check_token validates worldai_ key via Firestore
    """

    def test_bearer_token_forwarded_when_env_set(self):
        """Proxy sends Authorization header when WORLDTOOLS_BEARER_TOKEN is set."""
        captured = {}

        def fake_post(url, json=None, headers=None, timeout=None):
            captured["headers"] = headers or {}
            m = mock.MagicMock()
            m.status_code = 200
            m.json.return_value = {"jsonrpc": "2.0", "id": 1, "result": {"tools": []}}
            return m

        with mock.patch.dict("os.environ", {"WORLDTOOLS_BEARER_TOKEN": "worldai_abc123"}):
            proxy = WorldAIToolsProxy("http://fake-upstream/mcp")

        self.assertEqual(proxy.upstream_bearer_token, "worldai_abc123")

        with mock.patch("mvp_site.worldai_tools_mcp_proxy.requests.post", side_effect=fake_post):
            proxy._passthrough_jsonrpc("tools/list", {}, 1)

        self.assertEqual(
            captured["headers"].get("Authorization"),
            "Bearer worldai_abc123",
            "Bearer token must be forwarded as Authorization header to upstream",
        )

    def test_no_auth_header_when_token_absent(self):
        """Proxy sends no Authorization header when WORLDTOOLS_BEARER_TOKEN is unset."""
        captured = {}

        def fake_post(url, json=None, headers=None, timeout=None):
            captured["headers"] = headers
            m = mock.MagicMock()
            m.status_code = 200
            m.json.return_value = {"jsonrpc": "2.0", "id": 1, "result": {"tools": []}}
            return m

        with mock.patch.dict("os.environ", {}, clear=False):
            import os
            os.environ.pop("WORLDTOOLS_BEARER_TOKEN", None)
            proxy = WorldAIToolsProxy("http://fake-upstream/mcp")

        with mock.patch("mvp_site.worldai_tools_mcp_proxy.requests.post", side_effect=fake_post):
            proxy._passthrough_jsonrpc("tools/list", {}, 1)

        self.assertIsNone(
            captured.get("headers"),
            "No Authorization header should be sent when token is absent",
        )


if __name__ == "__main__":
    unittest.main()

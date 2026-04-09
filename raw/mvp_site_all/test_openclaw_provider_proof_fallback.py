"""TDD tests for PR #5879 review comment fixes.

Tests cover:
1. proof mode fallback to chat/completions when /v1/models fails
2. tunnel command fallback strips --url-file for Tailscale compatibility
3. auth bypass gated on TESTING_AUTH_BYPASS env var
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class _FakeResponse:
    def __init__(self, status_code, json_data=None, text=""):
        self.status_code = status_code
        self._json_data = json_data
        self.text = text
        self.headers = {"Content-Type": "application/json"}

    def json(self):
        if self._json_data is None:
            raise ValueError("No JSON")
        return self._json_data


class TestProofModeFallback(unittest.TestCase):
    """Verify proof_prompt fallback to chat/completions when models probe fails."""

    def _call(self, mock_get, mock_post, **kwargs):
        from mvp_site.llm_providers.openclaw_provider import test_openclaw_gateway_connection
        # Use gateway_port to avoid URL validation of localhost addresses
        return test_openclaw_gateway_connection(gateway_port=19999, **kwargs)

    @patch("mvp_site.llm_providers.openclaw_provider.requests.post")
    @patch("mvp_site.llm_providers.openclaw_provider.requests.get")
    def test_proof_prompt_falls_through_on_models_404(self, mock_get, mock_post):
        """proof_prompt + models 404 => should try chat/completions."""
        mock_get.return_value = _FakeResponse(404, text="Not Found")
        mock_post.return_value = _FakeResponse(200, json_data={
            "choices": [{"message": {"content": "hello"}}]
        })
        result = self._call(mock_get, mock_post, proof_prompt="say hello")
        self.assertTrue(result["success"], f"Expected success: {result}")
        self.assertEqual(result["mode"], "chat_completions")
        self.assertTrue(result.get("proof_prompt_used"))
        mock_post.assert_called_once()

    @patch("mvp_site.llm_providers.openclaw_provider.requests.post")
    @patch("mvp_site.llm_providers.openclaw_provider.requests.get")
    def test_proof_prompt_falls_through_on_models_503(self, mock_get, mock_post):
        """proof_prompt + models 503 => should try chat/completions."""
        mock_get.return_value = _FakeResponse(503, text="Service Unavailable")
        mock_post.return_value = _FakeResponse(200, json_data={
            "choices": [{"message": {"content": "pong"}}]
        })
        result = self._call(mock_get, mock_post, proof_prompt="ping")
        self.assertTrue(result["success"])
        self.assertEqual(result["mode"], "chat_completions")

    @patch("mvp_site.llm_providers.openclaw_provider.requests.get")
    def test_no_proof_prompt_models_200_succeeds_no_chat(self, mock_get):
        """No proof_prompt + models 200 => succeed immediately, no chat call."""
        from mvp_site.llm_providers.openclaw_provider import test_openclaw_gateway_connection
        mock_get.return_value = _FakeResponse(200, json_data={"data": [{"id": "m1"}]})
        result = test_openclaw_gateway_connection(gateway_port=19999)
        self.assertTrue(result["success"])
        self.assertEqual(result["mode"], "models")

    @patch("mvp_site.llm_providers.openclaw_provider.requests.post")
    @patch("mvp_site.llm_providers.openclaw_provider.requests.get")
    def test_no_proof_models_404_tries_chat(self, mock_get, mock_post):
        """No proof_prompt + models 404 => tries chat/completions as fallback."""
        mock_get.return_value = _FakeResponse(404, text="Not Found")
        mock_post.return_value = _FakeResponse(200, json_data={
            "choices": [{"message": {"content": "ok"}}]
        })
        result = self._call(mock_get, mock_post)
        self.assertTrue(result["success"])
        self.assertEqual(result["mode"], "chat_completions")

    @patch("mvp_site.llm_providers.openclaw_provider.requests.post")
    @patch("mvp_site.llm_providers.openclaw_provider.requests.get")
    def test_proof_prompt_models_200_still_calls_chat_for_hash(self, mock_get, mock_post):
        """proof_prompt + models 200 => should call chat for proof hash."""
        mock_get.return_value = _FakeResponse(200, json_data={"data": [{"id": "m"}]})
        mock_post.return_value = _FakeResponse(200, json_data={
            "choices": [{"message": {"content": "proof response"}}]
        })
        result = self._call(mock_get, mock_post, proof_prompt="prove it")
        self.assertTrue(result["success"])
        self.assertEqual(result["mode"], "chat_completions")
        self.assertIsNotNone(result.get("response_hash"))
        self.assertEqual(result.get("response_text_preview"), "proof response")

    @patch("mvp_site.llm_providers.openclaw_provider.requests.post")
    @patch("mvp_site.llm_providers.openclaw_provider.requests.get")
    def test_proof_prompt_chat_200_invalid_json_fails(self, mock_get, mock_post):
        """proof_prompt mode must fail if chat returns non-JSON payload."""
        mock_get.return_value = _FakeResponse(200, json_data={"data": [{"id": "m"}]})
        mock_post.return_value = _FakeResponse(
            200, json_data=None, text="<html>gateway ok but invalid payload</html>"
        )

        result = self._call(mock_get, mock_post, proof_prompt="prove response")

        self.assertFalse(result["success"])
        self.assertEqual(result["mode"], "chat_completions")
        self.assertIn("non-JSON", result["message"])

    @patch("mvp_site.llm_providers.openclaw_provider.requests.post")
    @patch("mvp_site.llm_providers.openclaw_provider.requests.get")
    def test_proof_prompt_chat_200_empty_content_fails(self, mock_get, mock_post):
        """proof_prompt mode must fail if chat content is empty."""
        mock_get.return_value = _FakeResponse(200, json_data={"data": [{"id": "m"}]})
        mock_post.return_value = _FakeResponse(
            200, json_data={"choices": [{"message": {"content": "   "}}]}
        )

        result = self._call(mock_get, mock_post, proof_prompt="prove response")

        self.assertFalse(result["success"])
        self.assertEqual(result["mode"], "chat_completions")
        self.assertIn("empty content", result["message"])


class TestTunnelCommandFallback(unittest.TestCase):
    """Verify candidate_cmds fallback strips --url-file and --provider."""

    def test_fallback_command_structure(self):
        """Second candidate cmd must NOT have --url-file or --provider."""
        import ast
        source_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "..", "testing_ui", "test_openclaw_e2e.py",
        )
        with open(source_path) as f:
            tree = ast.parse(f.read())
        found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    if isinstance(t, ast.Name) and t.id == "candidate_cmds":
                        found = True
                        elts = node.value.elts
                        self.assertEqual(len(elts), 2)
                        second_strs = [
                            n.value for n in ast.walk(elts[1])
                            if isinstance(n, ast.Constant) and isinstance(n.value, str)
                        ]
                        self.assertNotIn("--url-file", second_strs)
                        self.assertNotIn("--provider", second_strs)
                        self.assertIn("--port", second_strs)
        self.assertTrue(found, "candidate_cmds not found")


def _ensure_mcp_mocked():
    """Inject fake mcp modules into sys.modules if mcp isn't installed."""
    if "mcp" not in sys.modules:
        mock = MagicMock()
        for mod_name in ("mcp", "mcp.server", "mcp.server.stdio", "mcp.types"):
            sys.modules.setdefault(mod_name, mock)


class TestMcpApiAuthBypass(unittest.TestCase):
    """Verify _inject_authenticated_user_id gating on TESTING_AUTH_BYPASS."""

    @classmethod
    def setUpClass(cls):
        _ensure_mcp_mocked()

    def _call_fn(self, tool_name, arguments, user_id):
        """Call _inject_authenticated_user_id with _get_tool_schema_map mocked."""
        from mvp_site.mcp_api import _inject_authenticated_user_id
        schema_map = {
            "create_campaign": {
                "properties": {
                    "user_id": {"type": "string"},
                    "campaign_name": {"type": "string"},
                }
            }
        }
        with patch("mvp_site.mcp_api._get_tool_schema_map", return_value=schema_map):
            return _inject_authenticated_user_id(tool_name, arguments, user_id)

    def test_bypass_blocked_without_env_var(self):
        """Without TESTING_AUTH_BYPASS=true, test- user should NOT bypass."""
        with patch.dict(os.environ, {"TESTING_AUTH_BYPASS": "false"}):
            result = self._call_fn(
                "create_campaign", {"user_id": "victim-user"}, "test-attacker"
            )
            self.assertEqual(result["user_id"], "test-attacker",
                             "Should override user_id when bypass not enabled")

    def test_bypass_allowed_with_env_var(self):
        """With TESTING_AUTH_BYPASS=true and test- prefix, provided user_id passes through."""
        with patch.dict(os.environ, {"TESTING_AUTH_BYPASS": "true"}):
            result = self._call_fn(
                "create_campaign", {"user_id": "other-test-user"}, "test-caller"
            )
            self.assertEqual(result["user_id"], "other-test-user",
                             "Should keep provided user_id when bypass enabled")

    def test_non_test_user_always_overridden(self):
        """Real Firebase user_id always overrides even with TESTING_AUTH_BYPASS=true."""
        with patch.dict(os.environ, {"TESTING_AUTH_BYPASS": "true"}):
            result = self._call_fn(
                "create_campaign", {"user_id": "supplied-uid"}, "real-firebase-uid"
            )
            self.assertEqual(result["user_id"], "real-firebase-uid",
                             "Non-test user should always have user_id overridden")


if __name__ == "__main__":
    unittest.main()

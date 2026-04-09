"""
TDD: Test that base_test.py properly defines test_file for capture_provenance()

RED PHASE: This test should FAIL before the fix is applied.
The test verifies that test_file is defined and passed to capture_provenance.

Bug: Line 654 in testing_mcp/lib/base_test.py uses undefined variable test_file
"""

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Use absolute imports
from testing_mcp.lib.base_test import MCPTestBase


class TestBaseTestProvenance(unittest.TestCase):
    """Test that test_file is properly defined in run() method."""

    def test_external_server_client_factory_is_extracted(self):
        """Refactor guard: external-server MCP client creation should be centralized."""
        self.assertTrue(hasattr(MCPTestBase, "_create_external_server_client"))

    def test_test_file_is_defined_when_calling_capture_provenance(self):
        """
        RED TEST: test_file should be defined before calling capture_provenance.

        This test verifies that when run() method calls capture_provenance(),
        the test_file parameter is defined and points to the test class file.
        """

        # Create a concrete test class
        class ConcreteTest(MCPTestBase):
            TEST_NAME = "concrete_test"
            MODEL = "gemini-1.5-flash-002"

            def run_scenarios(self, ctx):
                return [{"name": "dummy", "passed": True}]

        test_instance = ConcreteTest()

        # Setup mocks
        mock_server = MagicMock()
        mock_server.pid = 12345
        mock_server.base_url = "http://localhost:8000"
        mock_server.env = {}
        mock_server.stop = MagicMock()

        mock_client = MagicMock()
        mock_client.wait_healthy = MagicMock()

        # Mock all external dependencies, including start_server to keep this unit-scoped.
        with patch.object(ConcreteTest, "start_server", return_value=(mock_client, mock_server)), \
             patch("testing_mcp.lib.base_test.settings_for_model") as mock_settings, \
             patch("testing_mcp.lib.base_test.update_user_settings") as mock_update, \
             patch("testing_mcp.lib.base_test.get_branch_scoped_tmp_root") as mock_tmp_root, \
             patch("testing_mcp.lib.base_test.get_evidence_dir") as mock_get_evidence, \
             patch("testing_mcp.lib.base_test.capture_provenance") as mock_capture_prov, \
             patch("testing_mcp.lib.base_test.create_evidence_bundle") as mock_create_bundle, \
             patch("sys.argv", ["test_script.py", "--work-name", "test_work"]):

            mock_settings.return_value = {}
            mock_tmp_root.return_value = Path("/tmp")
            mock_get_evidence.return_value = Path("/tmp/test_evidence")
            mock_create_bundle.return_value = {"_bundle_dir": Path("/tmp/test_evidence/iter_1")}

            # Run the test
            try:
                exit_code = test_instance.run()
            except Exception as e:
                # If test_file is undefined, we'll get NameError
                if "test_file" in str(e):
                    self.fail(f"test_file is undefined: {e}")
                raise

            # ASSERTION: capture_provenance should be called with test_file parameter
            self.assertTrue(
                mock_capture_prov.called,
                "capture_provenance should have been called"
            )

            # Get the call arguments
            call_args = mock_capture_prov.call_args

            # ASSERTION: test_file should be in kwargs and should be a valid path
            self.assertIn(
                "test_file",
                call_args.kwargs,
                "test_file parameter should be passed to capture_provenance"
            )

            test_file_arg = call_args.kwargs["test_file"]
            self.assertIsNotNone(
                test_file_arg,
                "test_file should not be None"
            )

            # ASSERTION: test_file should point to the test class file
            # It should end with the module file
            self.assertTrue(
                str(test_file_arg).endswith(".py"),
                f"test_file should be a Python file, got: {test_file_arg}"
            )

    def test_start_server_bootstraps_classifier_dependencies(self):
        """Local start_server should enforce classifier dependency bootstrap."""

        class ConcreteTest(MCPTestBase):
            TEST_NAME = "dep_bootstrap_test"
            MODEL = "gemini-1.5-flash-002"

            def run_scenarios(self, ctx):
                return [{"name": "dummy", "passed": True}]

        test_instance = ConcreteTest()
        test_instance.args = type(
            "Args",
            (),
            {"server": None, "reuse_existing_server": False},
        )()

        with patch.dict(
            os.environ,
            {"ENABLE_SEMANTIC_ROUTING": "true"},
            clear=False,
        ), patch(
            "testing_mcp.lib.base_test._ensure_runtime_dependencies_installed"
        ) as mock_ensure_deps, patch(
            "testing_mcp.lib.base_test.is_port_free", return_value=True
        ), patch(
            "testing_mcp.lib.base_test.start_local_mcp_server"
        ) as mock_start_server, patch(
            "testing_mcp.lib.base_test.MCPClient"
        ) as mock_client_class:
            mock_server = MagicMock()
            mock_server.base_url = "http://127.0.0.1:8095"
            mock_server.stop = MagicMock()
            mock_server.pid = 12345
            mock_start_server.return_value = mock_server

            mock_client = MagicMock()
            mock_client.wait_healthy = MagicMock()
            mock_client_class.return_value = mock_client

            test_instance.start_server()

            mock_ensure_deps.assert_called_once()

    def test_base_test_default_user_email_is_empty_when_not_configured(self):
        """MCPTestBase should not hardcode a default test user email."""

        class ConcreteTest(MCPTestBase):
            TEST_NAME = "email_default_test"
            MODEL = "gemini-1.5-flash-002"

            def run_scenarios(self, ctx):
                return [{"name": "dummy", "passed": True}]

        test_instance = ConcreteTest()
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(test_instance.test_user_email, "")

    def test_start_server_sets_test_user_email_header_from_env(self):
        """Local MCP client should inherit configured test email header from base class."""

        class ConcreteTest(MCPTestBase):
            TEST_NAME = "email_header_test"
            MODEL = "gemini-1.5-flash-002"

            def run_scenarios(self, ctx):
                return [{"name": "dummy", "passed": True}]

        test_instance = ConcreteTest()
        test_instance.args = type(
            "Args",
            (),
            {"server": None, "reuse_existing_server": False},
        )()

        with patch.dict(
            os.environ,
            {
                "ENABLE_SEMANTIC_ROUTING": "false",
                "MCP_TEST_USER_EMAIL": "test-default@example.com",
            },
            clear=False,
        ), patch(
            "testing_mcp.lib.base_test.is_port_free", return_value=True
        ), patch(
            "testing_mcp.lib.base_test.start_local_mcp_server"
        ) as mock_start_server, patch(
            "testing_mcp.lib.base_test.MCPClient"
        ) as mock_client_class:
            mock_server = MagicMock()
            mock_server.base_url = "http://127.0.0.1:8095"
            mock_server.stop = MagicMock()
            mock_server.pid = 12345
            mock_start_server.return_value = mock_server

            mock_client = MagicMock()
            mock_client.wait_healthy = MagicMock()
            mock_client_class.return_value = mock_client

            test_instance.start_server()

            _, kwargs = mock_client_class.call_args
            self.assertIn("default_headers", kwargs)
            self.assertEqual(
                kwargs["default_headers"]["X-Test-User-Email"],
                "test-default@example.com",
            )

    def test_require_full_trace_logs_forced_true_by_default(self):
        """Full trace logs are enforced by default even if a test disables class flag."""

        class ConcreteTest(MCPTestBase):
            TEST_NAME = "trace_default_on"
            MODEL = "gemini-1.5-flash-002"
            REQUIRE_FULL_TRACE_LOGS = False

            def run_scenarios(self, ctx):
                return [{"name": "dummy", "passed": True}]

        test_instance = ConcreteTest()
        with patch.dict(os.environ, {}, clear=False):
            self.assertTrue(test_instance._require_full_trace_logs())

    def test_require_full_trace_logs_can_be_relaxed_with_env_override(self):
        """MCP_FORCE_FULL_TRACE_LOGS=false allows class-level disablement."""

        class ConcreteTest(MCPTestBase):
            TEST_NAME = "trace_env_override"
            MODEL = "gemini-1.5-flash-002"
            REQUIRE_FULL_TRACE_LOGS = False

            def run_scenarios(self, ctx):
                return [{"name": "dummy", "passed": True}]

        test_instance = ConcreteTest()
        with patch.dict(
            os.environ,
            {"MCP_FORCE_FULL_TRACE_LOGS": "false"},
            clear=False,
        ):
            self.assertFalse(test_instance._require_full_trace_logs())

    def test_start_server_does_not_reuse_existing_server_when_strict_trace_enabled(self):
        """Strict trace logging should force a fresh local server start."""

        class ConcreteTest(MCPTestBase):
            TEST_NAME = "strict_no_reuse"
            MODEL = "gemini-1.5-flash-002"

            def run_scenarios(self, ctx):
                return [{"name": "dummy", "passed": True}]

        test_instance = ConcreteTest()
        test_instance.args = type(
            "Args",
            (),
            {"server": None, "reuse_existing_server": True},
        )()

        with patch.dict(
            os.environ,
            {"ENABLE_SEMANTIC_ROUTING": "false", "MCP_FORCE_FULL_TRACE_LOGS": "true"},
            clear=False,
        ), patch(
            "testing_mcp.lib.base_test.is_server_healthy", return_value=True
        ), patch(
            "testing_mcp.lib.base_test.is_port_free", return_value=True
        ), patch(
            "testing_mcp.lib.base_test.start_local_mcp_server"
        ) as mock_start_server, patch(
            "testing_mcp.lib.base_test.MCPClient"
        ) as mock_client_class:
            mock_server = MagicMock()
            mock_server.base_url = "http://127.0.0.1:8095"
            mock_server.stop = MagicMock()
            mock_server.pid = 12345
            mock_start_server.return_value = mock_server

            mock_client = MagicMock()
            mock_client.wait_healthy = MagicMock()
            mock_client_class.return_value = mock_client

            test_instance.start_server()

            mock_start_server.assert_called_once()


if __name__ == "__main__":
    unittest.main()

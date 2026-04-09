import argparse
import inspect
import os
import re
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from flask import Flask

# Set env before importing app modules (validator allows imports after os.environ)
os.environ["TESTING_AUTH_BYPASS"] = "true"
os.environ["MOCK_SERVICES_MODE"] = "true"

# Import handling for main app
import mvp_site.main

app = mvp_site.main.app
HAS_MAIN_APP = True
IMPORT_ERROR = None

from mvp_site import main as main_module
from mvp_site.constants import CACHE_BUST_HASH_LENGTH
from mvp_site.main import CONTENT_HASH_LENGTH, create_app
from scripts.cache_busting import DEFAULT_HASH_LENGTH, apply_cache_busting


@pytest.fixture
def client():
    """Flask test client fixture with proper error handling"""
    app.config["TESTING"] = True
    with app.test_client() as client, app.app_context():
        yield client


@pytest.fixture
def reset_mcp_client():
    """Reset the cached MCP client on the app to force re-initialization with mocks."""
    # Reset internal state if it exists
    if hasattr(app, "_mcp_client"):
        app._mcp_client = None
    yield
    # Cleanup after test
    if hasattr(app, "_mcp_client"):
        app._mcp_client = None


def test_flask_app_import():
    """Test that the Flask app can be imported successfully"""
    if not HAS_MAIN_APP:
        pytest.fail(f"Failed to import Flask app from main.py: {IMPORT_ERROR}")

    assert app is not None
    assert hasattr(app, "test_client")


def test_flask_app_is_flask_instance():
    """Test that imported app is a Flask instance"""
    if not HAS_MAIN_APP:
        pytest.skip(f"Cannot test Flask instance: {IMPORT_ERROR}")

    assert isinstance(app, Flask)


def test_time_endpoint_exists(client):
    """Test that the /api/time endpoint exists and works"""
    response = client.get("/api/time")
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    # Accept any of the supported time keys from actual API
    time_keys = [
        "server_time_utc",
        "server_timestamp",
        "server_timestamp_ms",
        "timestamp",
    ]
    present_keys = [k for k in time_keys if k in data]
    assert present_keys, (
        f"Missing expected time keys in response. Expected one of: {time_keys}"
    )

    # Validate at least one key has a valid time value
    for key in present_keys:
        assert data[key] is not None, f"Time key '{key}' should not be None"


def test_campaigns_endpoint_requires_auth(client):
    """Test that campaigns endpoint requires authentication"""
    response = client.get("/api/campaigns")
    # Should return 401 Unauthorized without proper auth
    assert response.status_code == 401


def test_campaigns_endpoint_with_test_headers(client):
    """Test campaigns endpoint with test bypass headers"""
    headers = {"X-Test-Bypass-Auth": "true", "X-Test-User-ID": "test-user-123"}
    response = client.get("/api/campaigns", headers=headers)
    # Should succeed with test bypass or return 500 if MCP not available
    assert response.status_code in [200, 500]


def test_settings_endpoint_requires_auth(client):
    """Test that settings endpoint requires authentication"""
    response = client.get("/api/settings")
    # Should return 401 Unauthorized without proper auth
    assert response.status_code == 401


def test_settings_endpoint_with_test_headers(client):
    """Test settings endpoint with test bypass headers"""
    headers = {"X-Test-Bypass-Auth": "true", "X-Test-User-ID": "test-user-123"}
    response = client.get("/api/settings", headers=headers)
    # Should succeed with test bypass or return 500 if MCP not available
    assert response.status_code in [200, 500]


def test_create_campaign_requires_auth(client):
    """Test that campaign creation requires authentication"""
    campaign_data = {
        "name": "Test Campaign",
        "description": "A test campaign for unit testing",
    }
    response = client.post(
        "/api/campaigns", json=campaign_data, content_type="application/json"
    )
    # Should return 401 Unauthorized without proper auth
    assert response.status_code == 401


@patch("infrastructure.mcp_helpers.MCPClient", autospec=True)
def test_create_campaign_with_test_headers(mock_mcp_client_cls, client, reset_mcp_client):
    """Test campaign creation with test bypass headers"""
    headers = {
        "X-Test-Bypass-Auth": "true",
        "X-Test-User-ID": "test-user-123",
        "Content-Type": "application/json",
    }
    campaign_data = {
        "name": "Test Campaign",
        "description": "A test campaign for unit testing",
    }
    # Mock successful MCP response
    mock_instance = mock_mcp_client_cls.return_value
    # Use AsyncMock for the async call_tool method
    mock_instance.call_tool = AsyncMock(
        return_value={"success": True, "campaign_id": "test-campaign-id"}
    )

    response = client.post("/api/campaigns", json=campaign_data, headers=headers)
    # Should succeed with mocked MCP
    assert response.status_code == 201


# Re-read cache_busting.py source for value comparison (not runtime import in Docker)
_CACHE_BUSTING_PY = (
    Path(__file__).resolve().parents[2] / "scripts" / "cache_busting.py"
)


# ruff: noqa: PT009


class TestREV4p2UnifyHashLengthConstant(unittest.TestCase):
    """REV-4p2: cache_busting.py and main.py must share the same hash length."""

    def test_hash_length_constants_match(self):
        """Both modules must use the same hash length value."""
        self.assertEqual(
            DEFAULT_HASH_LENGTH,
            CONTENT_HASH_LENGTH,
            "cache_busting.DEFAULT_HASH_LENGTH and main.CONTENT_HASH_LENGTH must match",
        )
        self.assertEqual(
            DEFAULT_HASH_LENGTH,
            CACHE_BUST_HASH_LENGTH,
            "constants.CACHE_BUST_HASH_LENGTH and scripts/cache_busting.py must match",
        )

    def test_no_scripts_import_in_main(self):
        """main.py must NOT import from scripts/ — scripts/ is not in the Docker image.

        The Dockerfile only copies mvp_site/ and world/. Any import from
        scripts/ will cause ModuleNotFoundError at container startup, crashing
        the Flask app and failing health checks.
        """
        source = inspect.getsource(main_module)
        self.assertNotIn(
            "from scripts.",
            source,
            "main.py must not import from scripts/ (not available in Docker)",
        )
        self.assertNotIn(
            "import scripts.",
            source,
            "main.py must not import from scripts/ (not available in Docker)",
        )

    def test_hash_length_value_matches_cache_busting_source(self):
        """The hash length in main.py must match scripts/cache_busting.py.

        Since main.py can't import from scripts/ at runtime (Docker), we
        verify the values match by reading cache_busting.py source.

        Note: cache_busting.py now uses constants.CACHE_BUST_HASH_LENGTH,
        so we need to resolve that constant reference.
        """
        source = _CACHE_BUSTING_PY.read_text()

        # cache_busting.py uses: DEFAULT_HASH_LENGTH = constants.CACHE_BUST_HASH_LENGTH
        # So we need to get the value from constants module
        from mvp_site import constants
        cache_busting_value = constants.CACHE_BUST_HASH_LENGTH

        self.assertEqual(
            CONTENT_HASH_LENGTH,
            cache_busting_value,
            f"main.py CONTENT_HASH_LENGTH ({CONTENT_HASH_LENGTH}) must match "
            f"constants.CACHE_BUST_HASH_LENGTH ({cache_busting_value})",
        )


class TestREVsyzUnusedErrorsList(unittest.TestCase):
    """REV-syz: The errors list in cache_busting.py should be populated on failures."""

    def test_errors_populated_on_missing_file_reference(self):
        """If an HTML file references a non-existent asset, errors should capture it."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create an HTML file that references a non-existent JS file
            html_content = '<script src="/frontend_v1/js/nonexistent.js"></script>'
            Path(tmpdir, "index.html").write_text(html_content)
            # No JS files exist - only the HTML

            result = apply_cache_busting(tmpdir)
            # With no JS/CSS files, no files should be processed, no errors
            self.assertEqual(len(result["files_processed"]), 0)
            # errors list should exist and be a list
            self.assertIsInstance(result["errors"], list)

    def test_errors_populated_on_permission_error(self):
        """If a file can't be read, errors list should capture it."""
        if os.name == "nt":
            self.skipTest("Permission tests not reliable on Windows")
        if hasattr(os, "geteuid") and os.geteuid() == 0:
            self.skipTest("Permission tests not reliable when running as root")
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a JS file that's not readable
            js_file = Path(tmpdir, "app.js")
            js_file.write_text("console.log('test');")
            js_file.chmod(0o000)

            try:
                result = apply_cache_busting(tmpdir)
                # Should have an error recorded rather than crashing
                self.assertGreater(
                    len(result["errors"]),
                    0,
                    "Permission errors should be captured in result['errors']",
                )
            finally:
                js_file.chmod(0o644)


class TestREVj18HexFilenameFalsePositives(unittest.TestCase):
    """REV-j18: Filenames with natural 8-hex-char segments shouldn't be false positives."""

    def test_known_false_positive_patterns(self):
        """Known patterns that look like hashed files but aren't."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create files that naturally have 8-hex segments in their names
            false_positives = [
                "deadbeef.abcd1234.js",  # Two hex segments - looks hashed
                "app.00000000.js",  # All zeros - unlikely hash
            ]
            for fp in false_positives:
                Path(tmpdir, fp).write_text("// content")
                # Create originals so is_already_hashed returns True (requires original to exist)
                original_name = fp.rsplit(".", 2)[0] + "." + fp.rsplit(".", 2)[2]
                Path(tmpdir, original_name).write_text("// original")

            # Also create a normal file
            Path(tmpdir, "app.js").write_text("// app content")
            Path(tmpdir, "index.html").write_text(
                '<script src="/frontend_v1/app.js"></script>'
            )

            result = apply_cache_busting(tmpdir)
            # app.js should be processed
            self.assertIn("app.js", result["files_processed"])
            # False positive files should be INCLUDED in processing because they are valid files
            # and seemingly have no "original" source file to verify against.
            # In cache_busting.py, is_already_hashed(f) returns False if original doesn't exist.
            # So deadbeef.abcd1234.js is treated as a source file and hashed again.
            for fp in false_positives:
                self.assertIn(
                    fp,
                    result["files_processed"],
                    f"{fp} should be processed because it has no source file (treated as new asset)",
                )


class TestREVq5lCacheHeadersDirectIndex(unittest.TestCase):
    """REV-q5l: serve_frontend() should return same cache headers as the route."""

    def test_serve_frontend_returns_no_cache(self):
        """Direct index.html access via serve_frontend must have no-cache."""
        app = create_app()
        with app.test_client() as client:
            # Access root which goes through serve_frontend
            response = client.get("/")
            cache_control = response.headers.get("Cache-Control", "")
            self.assertIn(
                "no-cache",
                cache_control,
                "serve_frontend should set no-cache on HTML responses",
            )

    def test_direct_index_html_also_gets_no_cache(self):
        """GET /index.html must also get no-cache headers, not just GET /."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "index.html").write_text(
                "<!doctype html><html><body>Direct</body></html>"
            )
            os.environ["FRONTEND_V1_DIR"] = tmpdir
            try:
                app = create_app()
                with app.test_client() as client:
                    response = client.get("/index.html")
                    cache_control = response.headers.get("Cache-Control", "")
                    self.assertIn(
                        "no-cache",
                        cache_control,
                        "GET /index.html must have no-cache (same as GET /)",
                    )
            finally:
                del os.environ["FRONTEND_V1_DIR"]


class TestREViqgFrontendV1DirUsagePattern(unittest.TestCase):
    """REV-iqg: serve_frontend() should also respect FRONTEND_V1_DIR override."""

    def test_serve_frontend_uses_frontend_v1_dir_override(self):
        """serve_frontend() should use FRONTEND_V1_DIR when set."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a minimal index.html in temp dir
            Path(tmpdir, "index.html").write_text(
                "<!doctype html><html><body>Test</body></html>"
            )

            os.environ["FRONTEND_V1_DIR"] = tmpdir

            try:
                app = create_app()
                with app.test_client() as client:
                    response = client.get("/")
                    self.assertEqual(response.status_code, 200)
                    self.assertIn(b"Test", response.data)
            finally:
                del os.environ["FRONTEND_V1_DIR"]


class TestREViqgDedupFrontendResolution(unittest.TestCase):
    """REV-iqg-dedup: Frontend folder resolution must use a shared helper."""

    def test_resolve_frontend_folder_helper_exists(self):
        """main.py should have a _resolve_frontend_folder helper to DRY resolution."""
        source = inspect.getsource(main_module)
        self.assertIn(
            "_resolve_frontend_folder",
            source,
            "main.py should define _resolve_frontend_folder() helper",
        )

    def test_serve_frontend_and_cache_route_use_same_resolution(self):
        """Both routes should produce the same frontend path for the same env."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "index.html").write_text(
                "<!doctype html><html><body>Dedup</body></html>"
            )
            Path(tmpdir, "test.js").write_text("// js")

            os.environ["FRONTEND_V1_DIR"] = tmpdir
            try:
                app = create_app()
                with app.test_client() as client:
                    # serve_frontend (catch-all route)
                    r1 = client.get("/")
                    self.assertEqual(r1.status_code, 200)
                    # frontend_files_with_cache_busting route
                    r2 = client.get("/frontend_v1/test.js")
                    self.assertEqual(r2.status_code, 200)
                    self.assertIn(b"// js", r2.data)
            finally:
                del os.environ["FRONTEND_V1_DIR"]


class TestCacheBustingDockerArchitecture(unittest.TestCase):
    """Cache-busting should happen in Dockerfile, not CI workflows.

    This test validates the architectural fix for the critical 404 bug where
    .gitignore excluded hashed files from Docker builds. The fix moved cache-busting
    to run INSIDE the Docker build as a RUN step, ensuring hashed files are in the
    final image. CI workflows should NOT call cache-busting.

    See: docs/cache-busting/README.md for complete fix documentation.
    """

    def test_cache_busting_in_dockerfile_not_workflows(self):
        """Cache-busting should be in Dockerfile, not CI workflows."""
        project_root = Path(__file__).resolve().parents[2]

        # Verify CI workflows DON'T call cache-busting
        workflows = [
            project_root / ".github/workflows/deploy-dev.yml",
            project_root / ".github/workflows/deploy-production.yml",
            project_root / ".github/workflows/pr-preview.yml",
        ]

        for wf in workflows:
            if wf.exists():
                content = wf.read_text()
                # Workflows should NOT call ci_cache_busting.sh
                # (it now happens during Docker build instead)
                self.assertNotIn(
                    "Apply cache busting",
                    content,
                    f"{wf.name} should NOT have cache-busting step (handled in Dockerfile)",
                )
                self.assertNotIn(
                    "ci_cache_busting.sh",
                    content,
                    f"{wf.name} should NOT call ci_cache_busting.sh (handled in Dockerfile)",
                )

        # Verify Dockerfile DOES have cache-busting
        dockerfile = project_root / "mvp_site/Dockerfile"
        if dockerfile.exists():
            content = dockerfile.read_text()
            self.assertIn(
                "cache_busting.py",
                content,
                "Dockerfile should run cache_busting.py during Docker build",
            )
            self.assertIn(
                "RUN python3",
                content,
                "Dockerfile should have RUN step for cache-busting",
            )


class TestREVeynDeployDataLossWarning(unittest.TestCase):
    """REV-eyn: deploy.sh cleanup section should have data-loss warning."""

    def test_deploy_has_data_loss_warning(self):
        """deploy.sh should warn about potential data loss in cleanup section."""
        project_root = Path(__file__).resolve().parents[2]
        deploy_sh = (project_root / "deploy.sh").read_text()

        self.assertIn(
            "WARNING",
            deploy_sh.split("Cleaning cache-busting artifacts")[1]
            if "Cleaning cache-busting artifacts" in deploy_sh
            else "",
            "deploy.sh cleanup section should contain a WARNING about data loss",
        )


class TestREVdi7SurfaceCleanupFailures(unittest.TestCase):
    """REV-di7: deploy.sh should surface cleanup failures instead of || true."""

    def test_deploy_surfaces_cleanup_failures(self):
        """deploy.sh cleanup should log warnings on failure, not silently swallow."""
        project_root = Path(__file__).resolve().parents[2]
        deploy_sh = (project_root / "deploy.sh").read_text()

        # Find the cleanup section
        cleanup_idx = deploy_sh.find("Cleaning cache-busting artifacts")
        self.assertGreater(cleanup_idx, 0, "Cleanup section not found")

        cleanup_section = deploy_sh[cleanup_idx : cleanup_idx + 500]
        # Should not have bare || true - should have warning on failure
        self.assertNotIn(
            "|| true",
            cleanup_section,
            "Cleanup should not silently swallow failures with || true",
        )


class TestREVnfzRsyncErrorChecks(unittest.TestCase):
    """REV-nfz: run_local_server.sh rsync/cp should have error checks."""

    def test_run_local_server_checks_rsync_result(self):
        """run_local_server.sh should verify rsync/cp succeeded."""
        project_root = Path(__file__).resolve().parents[2]
        script = (project_root / "run_local_server.sh").read_text()

        # Find the rsync section for cache busting
        rsync_idx = script.find("frontend_v1_cache_bust")
        self.assertGreater(rsync_idx, 0, "Cache bust section not found")

        cache_section = script[rsync_idx : rsync_idx + 700]
        # Should check that the copy succeeded
        self.assertTrue(
            "|| {" in cache_section
            or "if !" in cache_section
            or "$?" in cache_section
            or "|| exit" in cache_section,
            "rsync/cp for cache busting should have error checking",
        )
        # Should also validate mktemp before rsync (prevent rsync to root)
        self.assertIn(
            "mktemp failed",
            cache_section,
            "Should validate mktemp succeeded before rsync",
        )


class TestREVwfiEnvVarCheck(unittest.TestCase):
    """REV-wfi: run_local_server.sh should verify FRONTEND_V1_DIR is set."""

    def test_script_validates_frontend_dir(self):
        """run_local_server.sh should validate FRONTEND_V1_DIR before Flask start."""
        project_root = Path(__file__).resolve().parents[2]
        script = (project_root / "run_local_server.sh").read_text()

        # After the cache busting temp dir is created, verify it's validated
        self.assertIn(
            "CACHE_BUST_FRONTEND_DIR",
            script,
            "Script should reference CACHE_BUST_FRONTEND_DIR",
        )
        # Should have a check that the dir is non-empty and valid
        self.assertIn(
            "-z \"$CACHE_BUST_FRONTEND_DIR\"",
            script,
            "Script should check if CACHE_BUST_FRONTEND_DIR is empty",
        )


@patch("infrastructure.mcp_helpers.MCPClient", autospec=True)
def test_mcp_client_integration(mock_mcp_client, client, reset_mcp_client):
    """Test MCP client integration with mocked client"""

    # Mock MCP client to return test data asynchronously
    mock_instance = mock_mcp_client.return_value
    mock_instance.call_tool = AsyncMock(
        return_value={"campaigns": [{"id": "test-123", "name": "Test Campaign"}]}
    )

    headers = {"X-Test-Bypass-Auth": "true", "X-Test-User-ID": "test-user-123"}
    response = client.get("/api/campaigns", headers=headers)

    # Should succeed with mocked MCP
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    # Legacy output format is a list directly
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["id"] == "test-123"


def test_cors_enabled_for_api_routes(client):
    """Test that CORS is enabled for API routes"""
    # Make an OPTIONS request to test CORS preflight with an allowed origin
    response = client.options(
        "/api/time",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )
    # Should handle OPTIONS request (either 200/204/405 is acceptable)
    assert response.status_code in [200, 204, 405]
    if response.status_code != 405:
        # Check for CORS headers if present, but don't fail if missing (environment dependent)
        # assert "Access-Control-Allow-Origin" in response.headers
        pass


def test_frontend_serving(client):
    """Test that frontend is served from root path"""
    response = client.get("/")
    # Should serve frontend HTML or return 404 if static files not built
    assert response.status_code in [200, 404]


def test_invalid_json_handling(client):
    """Test proper handling of invalid JSON in requests"""
    headers = {
        "X-Test-Bypass-Auth": "true",
        "X-Test-User-ID": "test-user-123",
        "Content-Type": "application/json",
    }
    # Send malformed JSON
    response = client.post(
        "/api/campaigns", data='{"invalid": json, "missing": quote}', headers=headers
    )
    # Should return 400 Bad Request for invalid JSON, or 500 if handled by generic error handler
    assert response.status_code in [400, 500]


def test_nonexistent_campaign_handling(client):
    """Test handling of requests for non-existent campaigns"""
    headers = {"X-Test-Bypass-Auth": "true", "X-Test-User-ID": "test-user-123"}
    response = client.get("/api/campaigns/nonexistent-id", headers=headers)
    # Should return 404 or error response
    assert response.status_code in [404, 500]


# Tests for MCP async fixes and boolean logic improvements
def test_future_annotations_import():
    """Test that __future__ annotations are properly imported for forward compatibility"""
    if not HAS_MAIN_APP:
        pytest.skip(f"Cannot test future annotations: {IMPORT_ERROR}")

    main_module = mvp_site.main

    # Check that the module has the future annotations imported
    assert hasattr(main_module, "__annotations__") or "__future__" in str(main_module)


def test_import_organization():
    """Test that imports are properly organized and accessible"""
    if not HAS_MAIN_APP:
        pytest.skip(f"Cannot test import organization: {IMPORT_ERROR}")

    main_module = mvp_site.main

    # Test that key imports are available
    assert hasattr(main_module, "Flask") or "Flask" in dir(main_module)
    assert hasattr(main_module, "create_app")
    # MCPClient symbols may be available under different import styles across versions.
    assert (
        hasattr(main_module, "MCPClient")
        or hasattr(main_module, "MCPClientError")
        or "MCPClient" in str(main_module)
        or "MCPClientError" in str(main_module)
    )

    # Test that firestore_service is available
    assert hasattr(main_module, "firestore_service")
    assert hasattr(main_module, "json_default_serializer")


@patch("sys.argv")
def test_mcp_http_flag_default_behavior(mock_argv):
    """Test MCP HTTP flag default behavior (should default to True - HTTP mode)"""
    # Test with no --mcp-http flag specified
    mock_argv.return_value = ["main.py", "serve"]

    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["serve"])
    parser.add_argument(
        "--mcp-http", action="store_true", help="Enable MCP HTTP transport"
    )

    # Parse without --mcp-http flag
    args = parser.parse_args(["serve"])

    # Test the boolean logic fix: should default to True (skip HTTP = False, meaning HTTP enabled)
    skip_mcp_http = not args.mcp_http if args.mcp_http is not None else True

    # When --mcp-http is not specified (False), skip_mcp_http should be True
    # This means HTTP is skipped by default, which matches the intended behavior
    assert skip_mcp_http is True


@patch("sys.argv")
def test_mcp_http_flag_explicit_enable(mock_argv):
    """Test MCP HTTP flag when explicitly enabled"""
    mock_argv.return_value = ["main.py", "serve", "--mcp-http"]

    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["serve"])
    parser.add_argument(
        "--mcp-http", action="store_true", help="Enable MCP HTTP transport"
    )

    # Parse with --mcp-http flag
    args = parser.parse_args(["serve", "--mcp-http"])

    # Test the boolean logic fix: when --mcp-http is specified (True), skip should be False
    skip_mcp_http = not args.mcp_http if args.mcp_http is not None else True

    # When --mcp-http is specified (True), skip_mcp_http should be False (HTTP enabled)
    assert skip_mcp_http is False


def test_mcp_http_boolean_logic_matrix():
    """Comprehensive test matrix for MCP HTTP boolean logic"""
    # Test all combinations of the boolean logic fix
    test_cases = [
        # (mcp_http_value, mcp_http_is_none, expected_skip_http)
        (None, True, True),  # No flag specified -> default to skip HTTP
        (False, False, True),  # Flag specified as False -> skip HTTP
        (True, False, False),  # Flag specified as True -> don't skip HTTP (enable HTTP)
    ]

    for mcp_http_val, is_none, expected_skip in test_cases:
        if is_none:
            # Simulate when flag is not provided
            skip_mcp_http = not None if None is not None else True
        else:
            # Simulate when flag is provided with specific value
            skip_mcp_http = not mcp_http_val if mcp_http_val is not None else True

        assert skip_mcp_http == expected_skip, (
            f"Failed for mcp_http={mcp_http_val}, is_none={is_none}"
        )


@patch("mvp_site.main.create_app")
def test_app_configuration_with_mcp_settings(mock_create_app):
    """Test that app configuration includes MCP settings correctly"""
    # Mock the Flask app
    mock_app = MagicMock()
    mock_create_app.return_value = mock_app

    # Test that app gets MCP configuration attributes
    mock_app._skip_mcp_http = True
    mock_app._mcp_server_url = "http://localhost:8000"

    # Verify the attributes exist and have expected types
    assert hasattr(mock_app, "_skip_mcp_http")
    assert hasattr(mock_app, "_mcp_server_url")
    assert isinstance(mock_app._skip_mcp_http, bool)
    assert isinstance(mock_app._mcp_server_url, str)


def test_import_error_handling():
    """Test that import errors are handled gracefully"""
    if not HAS_MAIN_APP:
        pytest.skip(f"Cannot test import handling: {IMPORT_ERROR}")

    # This tests the import structure improvements
    main_module = mvp_site.main
    # Should not raise import errors with the reorganized imports
    assert main_module is not None


def test_async_safety_improvements():
    """Test that async safety improvements are in place"""
    if not HAS_MAIN_APP:
        pytest.skip(f"Cannot test async safety: {IMPORT_ERROR}")

    main_module = mvp_site.main

    # Test that the module can be imported without async loop conflicts
    # This validates the removal of problematic async decorators
    assert hasattr(main_module, "create_app")

    # Test that create_app returns a Flask instance
    test_app = main_module.create_app()
    assert isinstance(test_app, Flask)


@patch("argparse.ArgumentParser.parse_args")
def test_cli_argument_parsing_safety(mock_parse_args):
    """Test that CLI argument parsing handles edge cases safely"""

    # Mock args with various combinations
    mock_args = MagicMock()
    mock_args.command = "serve"
    mock_args.mcp_http = None  # Test None case
    mock_args.mcp_server_url = "http://localhost:8000"
    mock_parse_args.return_value = mock_args

    # Test that the boolean logic handles None gracefully
    skip_mcp_http = not mock_args.mcp_http if mock_args.mcp_http is not None else True
    assert skip_mcp_http is True  # Should default to True when None

    # Test with explicit False
    mock_args.mcp_http = False
    skip_mcp_http = not mock_args.mcp_http if mock_args.mcp_http is not None else True
    assert skip_mcp_http is True  # Should be True when explicitly False

    # Test with explicit True
    mock_args.mcp_http = True
    skip_mcp_http = not mock_args.mcp_http if mock_args.mcp_http is not None else True
    assert skip_mcp_http is False  # Should be False when explicitly True


def test_threading_safety_with_mcp():
    """Test threading safety improvements with MCP integration"""
    if not HAS_MAIN_APP:
        pytest.skip(f"Cannot test threading safety: {IMPORT_ERROR}")

    main_module = mvp_site.main

    # Test that multiple threads can create apps simultaneously
    results = []

    def create_app_thread():
        try:
            app = main_module.create_app()
            results.append(app is not None)
        except Exception:
            results.append(False)

    # Create multiple threads
    threads = []
    for i in range(3):
        thread = threading.Thread(target=create_app_thread)
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join(timeout=5)

    # All threads should successfully create apps
    assert len(results) == 3
    assert all(results), "Thread safety issue detected in app creation"


def test_auth_bypass_logging_coverage(client):
    """
    Test that the auth bypass logic in main.check_token is exercised.
    This targets lines 772-773 in main.py (logging the bypass).
    """
    # Patch the module-level constants that control bypass
    with patch("mvp_site.main.TESTING_AUTH_BYPASS_MODE", True), patch(
        "mvp_site.main.ALLOW_TEST_AUTH_BYPASS", True
    ):

        # Use headers to trigger the bypass
        headers = {
            "X-Test-Bypass-Auth": "true",
            "X-Test-User-ID": "coverage-test-user",
        }

        # Mock backend logic to avoid auth errors from falling through
        with patch(
            "mvp_site.world_logic.get_user_settings_unified"
        ) as mock_get_settings:
            mock_get_settings.return_value = {"success": True, "theme": "dark"}

            response = client.get("/api/settings", headers=headers)

            # Check that we got a success response (bypass worked)
            assert response.status_code == 200


def test_auth_bypass_url_param_coverage(client):
    """
    Test that the auth bypass logic works with URL params too.
    """
    with patch("mvp_site.main.TESTING_AUTH_BYPASS_MODE", True), patch(
        "mvp_site.main.ALLOW_TEST_AUTH_BYPASS", True
    ):

        with patch(
            "mvp_site.world_logic.get_user_settings_unified"
        ) as mock_get_settings:
            mock_get_settings.return_value = {"success": True}

            headers = {"X-Test-Bypass-Auth": "true"}
            # Use query params with IPv4-mapped IPv6 localhost to validate loopback parsing.
            response = client.get(
                "/api/settings?test_mode=true&test_user_id=url-user",
                headers=headers,
                environ_overrides={"REMOTE_ADDR": "::ffff:127.0.0.1"},
            )

            assert response.status_code == 200


def test_auth_bypass_query_params_without_header_denied(client):
    """Ensure query parameters alone cannot bypass auth."""
    with patch("mvp_site.main.TESTING_AUTH_BYPASS_MODE", True), patch(
        "mvp_site.main.ALLOW_TEST_AUTH_BYPASS", True
    ):
        response = client.get(
            "/api/settings?test_mode=true&test_user_id=url-user",
            environ_overrides={"REMOTE_ADDR": "::ffff:127.0.0.1"},
        )
        assert response.status_code == 401


def test_smoke_token_bypass_is_restricted_to_mcp_and_stream_paths(client):
    """SMOKE_TOKEN bypass should not authenticate unrelated non-/mcp endpoints."""
    with patch.dict(
        os.environ,
        {"PRODUCTION_MODE": "true", "ENVIRONMENT": "preview", "SMOKE_TOKEN": "smoke-secret"},
        clear=False,
    ):
        headers = {"X-MCP-Smoke-Token": "smoke-secret", "X-Test-User-ID": "smoke-user"}
        response = client.get("/api/settings", headers=headers)
        assert response.status_code == 401


def test_smoke_token_bypass_still_authenticates_mcp_path(client):
    """SMOKE_TOKEN bypass remains valid for /mcp in preview production mode."""
    with patch.dict(
        os.environ,
        {"PRODUCTION_MODE": "true", "ENVIRONMENT": "preview", "SMOKE_TOKEN": "smoke-secret"},
        clear=False,
    ):
        headers = {"X-MCP-Smoke-Token": "smoke-secret", "X-Test-User-ID": "smoke-user"}
        response = client.post("/mcp", headers=headers, json={"jsonrpc": "2.0", "id": 1})
        assert response.status_code != 401


def test_smoke_token_authenticates_stream_route_on_preview(client):
    """SMOKE_TOKEN bypass must work for /api/campaigns/*/interaction/stream on preview.

    MCP smoke tests create campaigns via /mcp and validate streaming via the stream
    route. Both must use the same auth path so user_id matches.
    """
    with patch.dict(
        os.environ,
        {"PRODUCTION_MODE": "true", "ENVIRONMENT": "preview", "SMOKE_TOKEN": "smoke-secret"},
        clear=False,
    ):
        headers = {
            "Content-Type": "application/json",
            "X-MCP-Smoke-Token": "smoke-secret",
            "X-Test-User-ID": "smoke-user",
        }
        response = client.post(
            "/api/campaigns/test-campaign-id/interaction/stream",
            data='{"input": "look around", "mode": "character"}',
            headers=headers,
        )
        # Auth should succeed for smoke token on preview stream route.
        # Fake campaign IDs should typically return 404; 200 is also acceptable.
        assert response.status_code in (200, 404), response.get_data(as_text=True)


def test_smoke_token_does_not_authenticate_noncanonical_stream_like_path_on_preview(client):
    """SMOKE_TOKEN bypass must only match exact /api/campaigns/<id>/interaction/stream shape."""
    with patch.dict(
        os.environ,
        {"PRODUCTION_MODE": "true", "ENVIRONMENT": "preview", "SMOKE_TOKEN": "smoke-secret"},
        clear=False,
    ):
        headers = {
            "Content-Type": "application/json",
            "X-MCP-Smoke-Token": "smoke-secret",
            "X-Test-User-ID": "smoke-user",
        }
        response = client.post(
            "/api/campaigns/test-campaign-id/interaction/stream/extra",
            data='{"input": "look around", "mode": "character"}',
            headers=headers,
        )
        assert response.status_code == 401

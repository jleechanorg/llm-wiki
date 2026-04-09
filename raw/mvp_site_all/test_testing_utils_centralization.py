"""Tests verifying code centralization into testing_utils.

RED phase: These tests assert that duplicate functions have been removed
from consumer modules (testing_mcp, testing_ui) and replaced with
delegations to the canonical testing_utils implementations.
"""

import inspect

import testing_utils.browser as tu_browser
import testing_utils.evidence as tu_evidence
import testing_utils.http_client as tu_http_client
import testing_utils.http_test as tu_http_test
from testing_http.lib.server_utils import ensure_screenshot_dir, start_test_server
from testing_http.lib.session_utils import (
    generate_test_user_id as http_generate_test_user_id,
    get_test_headers,
)
from testing_http.lib.validation import (
    validate_api_response_structure as http_validate_api_response_structure,
    validate_browser_element_text as http_validate_browser_element_text,
)
from testing_mcp.lib import server_utils
from testing_mcp.lib.evidence_utils import (
    _capture_working_tree_state,
    _extract_payload_error_summary,
    _generate_run_id,
    _get_next_iteration,
    capture_server_health,
    capture_server_runtime,
    create_checksum_for_file,
    get_current_branch_name,
    save_request_responses,
    write_with_checksum,
)
from testing_mcp.lib.server_utils import wait_for_server_healthy  # noqa: F811
from testing_ui.config import is_video_recording_enabled
from testing_utils.browser import (
    is_video_recording_enabled as tu_is_video_recording_enabled,
)
import testing_ui.config as config_module


# -----------------------------------------------------------------------
# BD-5762-01: _wait_for_server_ready removed from testing_mcp/lib/server_utils
# -----------------------------------------------------------------------


class TestServerUtilsDedup:
    """Verify _wait_for_server_ready has been removed."""

    def test_no_local_wait_for_server_ready(self):
        """_wait_for_server_ready must not be defined in server_utils module."""
        assert not hasattr(server_utils, "_wait_for_server_ready"), (
            "_wait_for_server_ready should be deleted; "
            "use wait_for_server_healthy from testing_utils.server"
        )

    def test_wait_for_server_healthy_exported(self):
        """wait_for_server_healthy must be importable from server_utils."""
        assert wait_for_server_healthy is not None


# -----------------------------------------------------------------------
# BD-5762-02: evidence_utils generic functions → testing_utils.evidence
# -----------------------------------------------------------------------


class TestEvidenceUtilsDelegation:
    """Verify generic functions delegate to testing_utils.evidence."""

    def test_get_next_iteration_is_delegated(self):
        """_get_next_iteration should be imported from testing_utils.evidence."""
        # Same object means it was imported, not re-implemented
        assert _get_next_iteration is tu_evidence.get_next_iteration, (
            "_get_next_iteration should be the exact same object from testing_utils.evidence"
        )

    def test_generate_run_id_is_delegated(self):
        """_generate_run_id should be imported from testing_utils.evidence."""
        assert _generate_run_id is tu_evidence.generate_run_id, (
            "_generate_run_id should be the exact same object from testing_utils.evidence"
        )

    def test_get_current_branch_name_is_not_reimplemented(self):
        """get_current_branch_name should not have its own subprocess calls."""
        source = inspect.getsource(get_current_branch_name)
        assert "subprocess" not in source, (
            "get_current_branch_name should delegate to testing_utils, "
            "not contain its own subprocess calls"
        )

    def test_write_with_checksum_is_delegated(self):
        """write_with_checksum should be imported from testing_utils.evidence."""
        # Verify the function originates from testing_utils, not evidence_utils
        assert write_with_checksum.__module__ == "testing_utils.testing_utils.evidence" or \
            write_with_checksum.__module__ == "testing_utils.evidence", (
            f"write_with_checksum should originate from testing_utils.evidence, "
            f"got {write_with_checksum.__module__}"
        )

    def test_create_checksum_for_file_is_delegated(self):
        """create_checksum_for_file should be imported from testing_utils.evidence."""
        assert create_checksum_for_file.__module__ == "testing_utils.testing_utils.evidence" or \
            create_checksum_for_file.__module__ == "testing_utils.evidence", (
            f"create_checksum_for_file should originate from testing_utils.evidence, "
            f"got {create_checksum_for_file.__module__}"
        )

    def test_save_request_responses_uses_centralized_redaction(self):
        """save_request_responses should use centralized credential redaction."""
        source = inspect.getsource(save_request_responses)
        # WA-specific: uses MCPClient._sanitize_for_capture which delegates to
        # testing_utils.http_client.sanitize_for_capture
        assert "_sanitize_for_capture" in source, (
            "save_request_responses should use _sanitize_for_capture for redaction"
        )


# -----------------------------------------------------------------------
# BD-5762-03: Credential redaction centralization
# -----------------------------------------------------------------------


class TestCredentialRedactionCentralized:
    """Verify credential redaction is centralized in testing_utils.http_client."""

    def test_is_sensitive_key_public_in_http_client(self):
        """is_sensitive_key should be a public module-level function."""
        assert hasattr(tu_http_client, "is_sensitive_key"), (
            "testing_utils.http_client should expose is_sensitive_key as module-level function"
        )

    def test_sanitize_for_capture_public_in_http_client(self):
        """sanitize_for_capture should be a public module-level function."""
        assert hasattr(tu_http_client, "sanitize_for_capture"), (
            "testing_utils.http_client should expose sanitize_for_capture as module-level function"
        )

# -----------------------------------------------------------------------
# BD-5762-04: testing_ui/config.py branch-scoped helpers → testing_utils.browser
# -----------------------------------------------------------------------


class TestConfigDelegation:
    """Verify testing_ui/config.py delegates to testing_utils.browser."""

    def test_is_video_recording_enabled_delegates(self):
        """is_video_recording_enabled should be imported from testing_utils.browser."""
        # Should be the exact same function object (imported, not re-implemented)
        assert is_video_recording_enabled is tu_is_video_recording_enabled, (
            "is_video_recording_enabled should be the same object from testing_utils.browser"
        )

    def test_config_imports_from_testing_utils(self):
        """config.py should import resolve functions from testing_utils.browser."""
        source = inspect.getsource(config_module)
        assert "testing_utils.browser" in source or "testing_utils.evidence" in source, (
            "testing_ui/config.py should import from testing_utils"
        )


# =======================================================================
# Phase 2: testing_http/lib/ extractions
# =======================================================================


# -----------------------------------------------------------------------
# testing_http/lib/server_utils.py → testing_utils
# -----------------------------------------------------------------------


class TestHttpServerUtilsDelegation:
    """Verify testing_http/lib/server_utils.py delegates to testing_utils."""

    def test_start_test_server_uses_wait_for_server_healthy(self):
        """start_test_server should use wait_for_server_healthy, not inline poll."""
        source = inspect.getsource(start_test_server)
        assert "wait_for_server_healthy" in source, (
            "start_test_server should use wait_for_server_healthy from testing_utils"
        )

    def test_ensure_screenshot_dir_delegates(self):
        """ensure_screenshot_dir should delegate to testing_utils.browser."""
        source = inspect.getsource(ensure_screenshot_dir)
        assert "resolve_screenshot_dir" in source or "testing_utils" in source, (
            "ensure_screenshot_dir should delegate to testing_utils.browser"
        )


# -----------------------------------------------------------------------
# testing_http/lib/session_utils.py → testing_utils.http_test
# -----------------------------------------------------------------------


class TestHttpSessionUtilsDelegation:
    """Verify testing_http/lib/session_utils.py delegates to testing_utils."""

    def test_generate_test_user_id_in_testing_utils(self):
        """generate_test_user_id should exist in testing_utils.http_test."""
        assert hasattr(tu_http_test, "generate_test_user_id"), (
            "testing_utils.http_test should expose generate_test_user_id"
        )

    def test_build_test_headers_in_testing_utils(self):
        """build_test_headers should exist in testing_utils.http_test."""
        assert hasattr(tu_http_test, "build_test_headers"), (
            "testing_utils.http_test should expose build_test_headers"
        )

    def test_session_utils_delegates_user_id(self):
        """session_utils.generate_test_user_id should delegate to testing_utils."""
        assert http_generate_test_user_id is tu_http_test.generate_test_user_id, (
            "generate_test_user_id should be the same object from testing_utils"
        )

    def test_session_utils_delegates_headers(self):
        """session_utils.get_test_headers should delegate to testing_utils."""
        source = inspect.getsource(get_test_headers)
        assert "build_test_headers" in source or "testing_utils" in source, (
            "get_test_headers should delegate to testing_utils.http_test.build_test_headers"
        )


# -----------------------------------------------------------------------
# testing_http/lib/validation.py → testing_utils
# -----------------------------------------------------------------------


class TestHttpValidationDelegation:
    """Verify generic validation functions are in testing_utils."""

    def test_validate_api_response_in_testing_utils(self):
        """validate_api_response_structure should exist in testing_utils.http_test."""
        assert hasattr(tu_http_test, "validate_api_response_structure"), (
            "testing_utils.http_test should expose validate_api_response_structure"
        )

    def test_validate_browser_element_in_testing_utils(self):
        """validate_browser_element_text should exist in testing_utils.browser."""
        assert hasattr(tu_browser, "validate_browser_element_text"), (
            "testing_utils.browser should expose validate_browser_element_text"
        )

    def test_validation_delegates_api_response(self):
        """validation.validate_api_response_structure should delegate."""
        assert http_validate_api_response_structure is tu_http_test.validate_api_response_structure, (
            "validate_api_response_structure should be the same object from testing_utils"
        )

    def test_validation_delegates_browser_element(self):
        """validation.validate_browser_element_text should delegate."""
        assert http_validate_browser_element_text is tu_browser.validate_browser_element_text, (
            "validate_browser_element_text should be the same object from testing_utils"
        )


# =======================================================================
# Phase 3: Generic function extraction
# =======================================================================


class TestGenericFunctionExtraction:
    """Verify generic functions are extracted into testing_utils.evidence."""

    def test_capture_working_tree_state_in_testing_utils(self):
        """capture_working_tree_state should exist in testing_utils.evidence."""
        assert hasattr(tu_evidence, "capture_working_tree_state"), (
            "testing_utils.evidence should expose capture_working_tree_state"
        )

    def test_capture_raw_git_provenance_in_testing_utils(self):
        """capture_raw_git_provenance should exist in testing_utils.evidence."""
        assert hasattr(tu_evidence, "capture_raw_git_provenance"), (
            "testing_utils.evidence should expose capture_raw_git_provenance"
        )

    def test_capture_server_runtime_in_testing_utils(self):
        """capture_server_runtime should exist in testing_utils.evidence."""
        assert hasattr(tu_evidence, "capture_server_runtime"), (
            "testing_utils.evidence should expose capture_server_runtime"
        )

    def test_capture_server_health_in_testing_utils(self):
        """capture_server_health should exist in testing_utils.evidence."""
        assert hasattr(tu_evidence, "capture_server_health"), (
            "testing_utils.evidence should expose capture_server_health"
        )

    def test_extract_payload_error_summary_in_testing_utils(self):
        """extract_payload_error_summary should exist in testing_utils.evidence."""
        assert hasattr(tu_evidence, "extract_payload_error_summary"), (
            "testing_utils.evidence should expose extract_payload_error_summary"
        )

    def test_evidence_utils_delegates_capture_working_tree(self):
        """_capture_working_tree_state should delegate to testing_utils."""
        source = inspect.getsource(_capture_working_tree_state)
        assert "subprocess" not in source, (
            "_capture_working_tree_state should delegate to testing_utils, "
            "not contain its own subprocess calls"
        )

    def test_evidence_utils_delegates_capture_server_runtime(self):
        """capture_server_runtime should delegate to testing_utils."""
        source = inspect.getsource(capture_server_runtime)
        assert "lsof" not in source, (
            "capture_server_runtime should delegate to testing_utils, "
            "not contain its own lsof calls"
        )

    def test_evidence_utils_delegates_capture_server_health(self):
        """capture_server_health should delegate to testing_utils."""
        source = inspect.getsource(capture_server_health)
        assert "urlopen" not in source, (
            "capture_server_health should delegate to testing_utils, "
            "not contain its own urllib calls"
        )

    def test_evidence_utils_delegates_extract_payload_error_summary(self):
        """_extract_payload_error_summary should delegate to testing_utils."""
        source = inspect.getsource(_extract_payload_error_summary)
        assert "json.loads" not in source, (
            "_extract_payload_error_summary should delegate to testing_utils, "
            "not reimplement JSONL parsing"
        )

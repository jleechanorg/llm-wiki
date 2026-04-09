"""
Unit tests for evidence_utils.py steps-to-scenarios conversion.

Validates that steps dict format is correctly converted to scenarios list
without duplication or data loss.
"""

import shutil
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from types import SimpleNamespace

# Add testing_mcp to path for imports
testing_mcp_path = Path(__file__).parent.parent.parent / "testing_mcp"
sys.path.insert(0, str(testing_mcp_path))

import pytest

from testing_mcp.lib import base_test as base_test_module
from testing_mcp.lib.evidence_utils import (
    capture_provenance,
    create_evidence_bundle,
    has_critical_warnings,
    validate_provenance,
)


def test_steps_to_scenarios_no_duplicates():
    """Verify steps dict conversion doesn't create duplicate scenario entries."""
    # Simulate test results with "steps" dict format (not "scenarios" list)
    test_results = {
        "test_name": "example_test",
        "steps": {
            "step_1": {"success": True},
            "step_2": {"success": True},
            "step_3": {"success": False, "error": "Step 3 failed"},
        },
    }

    # Create minimal evidence bundle
    evidence_dir = Path("/tmp/test_evidence_steps_conversion")
    evidence_dir.mkdir(parents=True, exist_ok=True)

    files = create_evidence_bundle(
        evidence_dir=evidence_dir,
        test_name="example_test",
        provenance={"git_head": "abc123", "git_branch": "test"},
        results=test_results,
    )
    bundle_path = Path(files["_bundle_dir"])

    # Read evidence.md to verify scenario counts
    evidence_md = (bundle_path / "evidence.md").read_text()

    # Verify: Should show 3 scenarios (not 6 due to duplicates)
    assert "Total Scenarios:** 3" in evidence_md, (
        f"Expected 3 scenarios, evidence.md shows different count:\n{evidence_md}"
    )

    # Verify: Should show 2 passed, 1 failed
    assert "Passed:** 2" in evidence_md, "Expected 2 passed scenarios"
    assert "Failed:** 1" in evidence_md, "Expected 1 failed scenario"

    # Verify: Each step name appears exactly once
    assert evidence_md.count("### step_1") == 1, "step_1 should appear once"
    assert evidence_md.count("### step_2") == 1, "step_2 should appear once"
    assert evidence_md.count("### step_3") == 1, "step_3 should appear once"


def test_steps_to_scenarios_with_error_details():
    """Verify error details are preserved during conversion."""
    test_results = {
        "test_name": "error_detail_test",
        "steps": {
            "validation_step": {
                "success": False,
                "error": "Validation failed: missing required field",
            },
            "success_step": {"success": True},
        },
    }

    evidence_dir = Path("/tmp/test_evidence_error_details")
    evidence_dir.mkdir(parents=True, exist_ok=True)

    files = create_evidence_bundle(
        evidence_dir=evidence_dir,
        test_name="error_detail_test",
        provenance={"git_head": "def456", "git_branch": "test"},
        results=test_results,
    )
    bundle_path = Path(files["_bundle_dir"])

    evidence_md = (bundle_path / "evidence.md").read_text()

    # Verify error message is captured
    assert "Validation failed: missing required field" in evidence_md, (
        "Error message should be preserved in evidence"
    )


def test_steps_invalid_data_type():
    """Verify invalid step data type is handled gracefully."""
    test_results = {
        "test_name": "invalid_type_test",
        "steps": {
            "valid_step": {"success": True},
            "invalid_step": "this_is_a_string_not_a_dict",  # Invalid type
        },
    }

    evidence_dir = Path("/tmp/test_evidence_invalid_type")
    evidence_dir.mkdir(parents=True, exist_ok=True)

    files = create_evidence_bundle(
        evidence_dir=evidence_dir,
        test_name="invalid_type_test",
        provenance={"git_head": "ghi789", "git_branch": "test"},
        results=test_results,
    )
    bundle_path = Path(files["_bundle_dir"])

    evidence_md = (bundle_path / "evidence.md").read_text()

    # Verify invalid type is reported as error
    assert "Invalid step data type" in evidence_md, (
        "Invalid step data should be reported"
    )
    # Should still show 2 scenarios (not 4 due to duplicates)
    assert "Total Scenarios:** 2" in evidence_md, "Expected 2 scenarios"


def test_scenarios_list_format_unchanged():
    """Verify scenarios list format passes through unchanged."""
    test_results = {
        "test_name": "scenarios_list_test",
        "scenarios": [
            {"name": "scenario_1", "errors": []},
            {"name": "scenario_2", "errors": ["Failed"]},
        ],
    }

    evidence_dir = Path("/tmp/test_evidence_scenarios_list")
    evidence_dir.mkdir(parents=True, exist_ok=True)

    files = create_evidence_bundle(
        evidence_dir=evidence_dir,
        test_name="scenarios_list_test",
        provenance={"git_head": "jkl012", "git_branch": "test"},
        results=test_results,
    )
    bundle_path = Path(files["_bundle_dir"])

    evidence_md = (bundle_path / "evidence.md").read_text()

    # Verify scenarios list format works correctly (no conversion needed)
    assert "Total Scenarios:** 2" in evidence_md, "Expected 2 scenarios"
    assert "Passed:** 1" in evidence_md, "Expected 1 passed"
    assert "Failed:** 1" in evidence_md, "Expected 1 failed"


def test_evidence_bundle_no_request_responses_claims():
    """Ensure evidence docs don't claim MCP payloads or raw LLM outputs when absent."""
    test_results = {
        "test_name": "classifier_only_test",
        "scenarios": [
            {"name": "scenario_1", "errors": []},
        ],
    }

    evidence_dir = Path("/tmp/test_evidence_no_request_responses")
    evidence_dir.mkdir(parents=True, exist_ok=True)

    files = create_evidence_bundle(
        evidence_dir=evidence_dir,
        test_name="classifier_only_test",
        provenance={"git_head": "mno345", "git_branch": "test"},
        results=test_results,
        request_responses=None,
        server_log_path=None,
        has_llm_calls=False,
    )
    bundle_path = Path(files["_bundle_dir"])

    evidence_md = (bundle_path / "evidence.md").read_text()
    methodology_md = (bundle_path / "methodology.md").read_text()

    assert "request_responses.jsonl" not in evidence_md, (
        "Should not claim request_responses.jsonl"
    )
    assert "raw_*.txt" not in evidence_md, "Should not claim raw LLM outputs"
    assert "server.log" not in evidence_md, "Should not claim server logs"
    assert "Raw LLM outputs" not in methodology_md, (
        "Methodology should not claim raw outputs"
    )


def test_god_mode_setup_disclosure_detected():
    """Ensure GOD_MODE setup is disclosed when present in request_responses."""
    test_results = {
        "test_name": "god_mode_disclosure_test",
        "scenarios": [{"name": "scenario_1", "errors": []}],
    }
    request_responses = [
        {
            "request": {
                "params": {
                    "name": "process_action",
                    "arguments": {
                        "user_input": 'GOD_MODE_UPDATE_STATE:{"debug_mode": true}',
                    },
                }
            }
        }
    ]

    evidence_dir = Path("/tmp/test_evidence_god_mode_disclosure")
    evidence_dir.mkdir(parents=True, exist_ok=True)

    files = create_evidence_bundle(
        evidence_dir=evidence_dir,
        test_name="god_mode_disclosure_test",
        provenance={"git_head": "pqr678", "git_branch": "test"},
        results=test_results,
        request_responses=request_responses,
    )
    bundle_path = Path(files["_bundle_dir"])
    methodology_md = (bundle_path / "methodology.md").read_text()

    assert "GOD_MODE_UPDATE_STATE" in methodology_md, "GOD_MODE disclosure missing"


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def _wait_for_http(port: int, timeout_seconds: float = 3.0) -> None:
    deadline = time.time() + timeout_seconds
    url = f"http://127.0.0.1:{port}"
    last_error: Exception | None = None
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=0.5):
                return
        except Exception as exc:
            last_error = exc
            time.sleep(0.1)
    raise AssertionError(f"HTTP server did not respond on {url}: {last_error}")


def test_capture_provenance_fills_server_pid_when_missing():
    """Verify capture_provenance() infers PID when server_pid is not provided."""
    if shutil.which("lsof") is None:
        pytest.skip("lsof not available on this system")

    port = _find_free_port()
    proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        _wait_for_http(port)
        provenance = capture_provenance(f"http://127.0.0.1:{port}")
        server_pid = provenance.get("server", {}).get("pid")
        assert server_pid, "Expected capture_provenance to populate server pid"
        assert str(server_pid) == str(proc.pid), (
            f"Expected server pid {proc.pid}, got {server_pid}"
        )
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


def test_metadata_includes_evidence_mode_fields():
    """Ensure metadata.json includes evidence_mode fields per evidence standards."""
    test_results = {
        "test_name": "evidence_mode_metadata_test",
        "scenarios": [{"name": "scenario_1", "errors": []}],
    }

    evidence_dir = Path("/tmp/test_evidence_metadata_evidence_mode")
    evidence_dir.mkdir(parents=True, exist_ok=True)

    files = create_evidence_bundle(
        evidence_dir=evidence_dir,
        test_name="evidence_mode_metadata_test",
        provenance={"git_head": "stu901", "git_branch": "test"},
        results=test_results,
        request_responses=[{"request": {}, "response": {}}],
    )
    bundle_path = Path(files["_bundle_dir"])
    metadata = (bundle_path / "metadata.json").read_text()

    assert '"evidence_mode"' in metadata, "metadata.json missing evidence_mode"
    assert '"evidence_mode_notes"' in metadata, (
        "metadata.json missing evidence_mode_notes"
    )


def test_spicy_mode_comprehensive_scenarios_include_campaign_id():
    """Static check: spicy mode comprehensive scenarios should include campaign_id."""
    test_path = (
        Path(__file__).parent.parent.parent
        / "testing_mcp"
        / "test_spicy_mode_comprehensive_real.py"
    )
    content = test_path.read_text()

    # Expect each scenario result dict to include campaign_id for traceability
    expected_min = 21
    actual = content.count('"campaign_id": campaign_id')
    assert actual >= expected_min, (
        f"Expected at least {expected_min} scenario entries with campaign_id, found {actual}"
    )


def test_fix_classification_in_evidence():
    """Ensure fix classification is surfaced in evidence.md when provided."""
    test_results = {
        "test_name": "fix_classification_test",
        "fix_classification": {
            "type": "new_feature",
            "justification": "New endpoint routing for settings",
        },
        "scenarios": [{"name": "scenario_1", "errors": []}],
    }

    evidence_dir = Path("/tmp/test_evidence_fix_classification")
    evidence_dir.mkdir(parents=True, exist_ok=True)

    files = create_evidence_bundle(
        evidence_dir=evidence_dir,
        test_name="fix_classification_test",
        provenance={"git_head": "vwx234", "git_branch": "test"},
        results=test_results,
    )
    bundle_path = Path(files["_bundle_dir"])
    evidence_md = (bundle_path / "evidence.md").read_text()

    assert "Fix Classification" in evidence_md, (
        "evidence.md missing fix classification header"
    )
    assert "new_feature" in evidence_md, "evidence.md missing fix classification type"


def test_base_test_passes_fix_classification_to_bundle(monkeypatch, tmp_path):
    """Ensure MCPTestBase forwards FIX_CLASSIFICATION into evidence bundle results."""
    captured = {}

    class DummyClient:
        def get_captures_as_dict(self):
            return [
                {
                    "request": {"method": "tools/list"},
                    "response": {"result": {"tools": []}},
                }
            ]

        def clear_captures(self):
            return None

    class DummyServer:
        pid = 123
        base_url = "http://dummy"
        env = {}
        log_path = None

        def stop(self):
            return None

    class DummyParser:
        def parse_args(self):
            return SimpleNamespace(
                server=None,
                model="dummy-model",
                work_name="dummy-work",
                no_download=True,
            )

    class DummyTest(base_test_module.MCPTestBase):
        TEST_NAME = "dummy_test"
        MODEL = "dummy-model"
        FIX_CLASSIFICATION = {
            "type": "new_feature",
            "justification": "Settings endpoint routing",
        }

        def run_scenarios(self, ctx):
            return [{"name": "scenario", "passed": True, "errors": []}]

    def fake_create_evidence_bundle(
        evidence_dir,
        test_name,
        provenance,
        results,
        request_responses=None,
        llm_request_responses_path=None,
        http_request_responses_path=None,
        gemini_http_request_responses_path=None,
        campaign_snapshots=None,
        methodology_text=None,
        server_log_path=None,
        has_llm_calls=True,
        require_full_trace_logs=False,
        pre_restart_evidence=None,
        isolation_info=None,
        **kwargs,
    ):
        captured["results"] = results
        return {"_bundle_dir": evidence_dir}

    monkeypatch.setattr(
        base_test_module.MCPTestBase, "create_parser", lambda self: DummyParser()
    )
    monkeypatch.setattr(
        base_test_module.MCPTestBase,
        "start_server",
        lambda self: (DummyClient(), DummyServer()),
    )
    monkeypatch.setattr(base_test_module, "settings_for_model", lambda model: {})
    monkeypatch.setattr(base_test_module, "update_user_settings", lambda *_, **__: None)
    forced_tmp_evidence = Path("/tmp") / f"test_base_fix_classification_{int(time.time())}"
    forced_tmp_evidence.mkdir(parents=True, exist_ok=True)
    # Ensure branch-scoped-root validation passes by pointing it at /tmp
    monkeypatch.setattr(
        base_test_module, "get_branch_scoped_tmp_root", lambda: Path("/tmp")
    )
    monkeypatch.setattr(
        base_test_module, "get_evidence_dir", lambda _: forced_tmp_evidence
    )
    monkeypatch.setattr(base_test_module, "capture_provenance", lambda *_, **__: {})
    monkeypatch.setattr(
        base_test_module, "create_evidence_bundle", fake_create_evidence_bundle
    )

    exit_code = DummyTest().run()

    assert exit_code == 0
    assert captured["results"]["fix_classification"]["type"] == "new_feature"


def test_spicy_mode_comprehensive_declares_fix_classification():
    """Ensure spicy mode comprehensive test declares fix classification."""
    from testing_mcp.test_spicy_mode_comprehensive_real import (
        SpicyModeComprehensiveTest,
    )

    fix_classification = getattr(SpicyModeComprehensiveTest, "FIX_CLASSIFICATION", None)
    assert fix_classification is not None
    assert fix_classification.get("type") == "new_feature"


# Tests for provenance validation (Finding 2)
def test_validate_provenance_fails_on_dirty_tree():
    """Test that validate_provenance fails when working tree is dirty."""
    provenance = {
        "git_head": "abc123def",
        "working_tree_dirty": True,
        "working_tree_changed_files": ["file1.py", "file2.py"],
    }

    is_valid, errors = validate_provenance(
        provenance,
        fail_on_dirty_tree=True,
        fail_on_commit_drift=False,
    )

    assert not is_valid, "Should fail when working tree is dirty"
    assert any("dirty" in err.lower() for err in errors), f"Error should mention dirty: {errors}"


def test_validate_provenance_fails_on_commit_drift():
    """Test that validate_provenance fails when commit changes during run."""
    provenance = {
        "git_head": "newcommit456",
        "working_tree_dirty": False,
    }

    is_valid, errors = validate_provenance(
        provenance,
        start_git_head="oldcommit123",
        fail_on_dirty_tree=False,
        fail_on_commit_drift=True,
    )

    assert not is_valid, "Should fail when commit drift detected"
    assert any("drift" in err.lower() for err in errors), f"Error should mention drift: {errors}"


def test_validate_provenance_passes_with_clean_tree_and_no_drift():
    """Test that validate_provenance passes with clean tree and no drift."""
    provenance = {
        "git_head": "abc123def",
        "working_tree_dirty": False,
    }

    is_valid, errors = validate_provenance(
        provenance,
        start_git_head="abc123def",
        fail_on_dirty_tree=True,
        fail_on_commit_drift=True,
    )

    assert is_valid, f"Should pass with clean tree and no drift, but got errors: {errors}"
    assert len(errors) == 0


# Tests for critical warnings (Finding 4)
def test_has_critical_warnings_detects_dice_integrity():
    """Test that has_critical_warnings detects dice integrity warnings."""
    errors = [
        "Some non-critical warning",
        "Dice integrity warning: dice output could not be verified",
    ]

    has_critical, critical_found = has_critical_warnings(errors)

    assert has_critical, "Should detect dice integrity warning"
    assert len(critical_found) == 1
    assert "dice" in critical_found[0].lower()


def test_has_critical_warnings_detects_contract_violation():
    """Test that has_critical_warnings detects contract violations."""
    errors = [
        "Minor warning",
        "Contract violation detected: missing required field",
    ]

    has_critical, critical_found = has_critical_warnings(errors)

    assert has_critical, "Should detect contract violation"
    assert len(critical_found) == 1


def test_has_critical_warnings_returns_false_for_non_critical():
    """Test that has_critical_warnings returns False for non-critical warnings."""
    errors = [
        "Minor warning",
        "Non-critical issue",
    ]

    has_critical, critical_found = has_critical_warnings(errors)

    assert not has_critical, "Should not detect critical warnings"
    assert len(critical_found) == 0


# Tests for confidence rubric (HIGH/MEDIUM/LOW based on provenance + warnings + artifacts)
def test_confidence_rubric_high_with_clean_provenance_no_warnings():
    """Test confidence is HIGH when provenance is clean and no warnings."""
    # This would be tested in a more comprehensive scenario with actual
    # provenance, warnings, and artifact completeness metrics
    # For now, we verify the components work together
    provenance = {
        "git_head": "abc123",
        "working_tree_dirty": False,
    }
    errors = ["minor note"]

    is_valid, _ = validate_provenance(provenance)
    has_crit, _ = has_critical_warnings(errors)

    # Clean provenance + no critical warnings = HIGH confidence
    assert is_valid and not has_crit


def test_confidence_rubric_low_with_dirty_provenance():
    """Test confidence is LOW when provenance has issues."""
    provenance = {
        "git_head": "abc123",
        "working_tree_dirty": True,
    }

    is_valid, _ = validate_provenance(provenance)

    # Dirty tree = LOW confidence (validation fails)
    assert not is_valid

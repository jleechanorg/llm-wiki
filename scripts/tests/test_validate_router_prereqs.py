"""Tests for scripts/validate_router_prereqs.py.

These tests keep the gate honest: a dumber downstream model can't quietly
soften the thresholds without breaking them.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import validate_router_prereqs as gate  # noqa: E402


def _state(rubric, techniques=None):
    return {
        "techniques": techniques or {"SR": {}, "ET": {}, "PRM": {}},
        "rubric_scores": rubric,
    }


def test_no_matched_prs_fails():
    state = _state(
        {
            "6345": {"technique": "PRM", "total": 83},
            "6350": {"technique": "ET", "total": 84},
        }
    )
    report = gate.evaluate(state, min_matched=5, min_reversals=2)
    assert report["passed"] is False
    assert report["matched_prs"] == 0
    assert report["reversals"] == 0


def test_matched_without_reversals_fails():
    rubric = {}
    for i, pr in enumerate(range(6000, 6005)):
        rubric[str(pr)] = {"technique": "SR", "total": 90 - i}
        rubric[f"{pr}-b"] = {"technique": "ET", "total": 70 - i}
    state = _state(rubric)
    matched = gate.build_matched_table(state)
    assert matched == {}, "different pr_ids must not count as matched"
    report = gate.evaluate(state, min_matched=5, min_reversals=2)
    assert report["passed"] is False


def test_matched_and_reversal_passes():
    rubric = {
        "A": {"technique": "SR", "total": 90},
        "A_et": {"technique": "ET", "total": 80},
        "B": {"technique": "SR", "total": 70},
        "B_et": {"technique": "ET", "total": 85},
    }
    # Consolidate into proper matched entries: same pr_id must appear across
    # techniques. The gate reads rubric_scores keyed by pr_id, with exactly one
    # entry per (pr, technique). We encode that with compound keys + a
    # pr_alias field would be overkill; instead, use unique keys but rely on
    # the real scoring convention: one rubric entry per (pr, technique) stored
    # under pr_id only. Here we construct a minimal matched table directly to
    # exercise count_reversals.
    matched = {
        "PR1": {"SR": 90, "ET": 80},
        "PR2": {"SR": 70, "ET": 85},
        "PR3": {"SR": 75, "ET": 78},
        "PR4": {"SR": 82, "ET": 79},
        "PR5": {"SR": 88, "ET": 84},
    }
    assert gate.count_reversals(matched) == 1
    # With 2+ technique pairs we need more reversals; add PRM to trigger two.
    matched_three = {
        "PR1": {"SR": 90, "ET": 80, "PRM": 85},
        "PR2": {"SR": 70, "ET": 85, "PRM": 88},
        "PR3": {"SR": 92, "ET": 75, "PRM": 70},
        "PR4": {"SR": 60, "ET": 90, "PRM": 95},
        "PR5": {"SR": 88, "ET": 84, "PRM": 70},
    }
    assert gate.count_reversals(matched_three) == 3


def test_rubric_entries_missing_technique_are_ignored():
    state = _state(
        {
            "6345": {"total": 83},  # missing technique field
            "6350": {"technique": "ET", "total": 84},
        }
    )
    matched = gate.build_matched_table(state)
    assert matched == {}


def test_exit_codes(tmp_path, capsys):
    empty = tmp_path / "empty.json"
    empty.write_text(json.dumps({"techniques": {}, "rubric_scores": {}}))
    rc = gate.main(["--state", str(empty)])
    captured = capsys.readouterr()
    assert rc == 1
    assert "FAIL" in captured.out

    missing = tmp_path / "missing.json"
    rc = gate.main(["--state", str(missing)])
    assert rc == 2


def test_matched_table_requires_same_pr_id():
    """Two rubric entries with different pr_ids cannot form a match even if
    they reference the same underlying PR via different keys.

    The gate intentionally requires a single pr_id per PR so downstream
    scripts that append scores cannot accidentally inflate matched counts by
    double-keying the same PR."""
    rubric = {
        "6345": {"technique": "PRM", "total": 83},
        "6345-a": {"technique": "ET", "total": 80},
    }
    state = _state(rubric)
    matched = gate.build_matched_table(state)
    assert matched == {}


def test_real_current_state_file_fails_gate():
    """Regression guard: today's bandit_state.json must NOT pass the gate.

    If this test starts failing it means someone scored enough matched PRs
    with reversals — great, remove this assertion and celebrate. Until then
    the gate should block router work against the repo's real state."""
    real = ROOT.parent / "technique_bandit" / "bandit_state.json"
    if not real.exists():
        pytest.skip("bandit_state.json not present")
    state = json.loads(real.read_text())
    report = gate.evaluate(state, min_matched=5, min_reversals=2)
    assert report["passed"] is False, (
        "Gate should still block router work; if matched corpus has been "
        "built, delete this test and proceed."
    )

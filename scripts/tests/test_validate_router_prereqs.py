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


def test_nested_schema_cell_mean():
    """Nested schema: rubric_scores[pr][tech] = [row1, row2, row3] aggregates to mean."""
    state = _state(
        {
            "PR1": {
                "SR": [{"total": 90}, {"total": 88}, {"total": 92}],
                "ET": [{"total": 80}, {"total": 82}, {"total": 78}],
            }
        }
    )
    matched = gate.build_matched_table(state)
    assert "PR1" in matched
    assert matched["PR1"]["SR"] == pytest.approx(90.0)
    assert matched["PR1"]["ET"] == pytest.approx(80.0)


def test_nested_schema_ignores_cells_without_numeric_totals():
    state = _state(
        {
            "PR1": {
                "SR": [{"total": "not-a-number"}, {"no_total": True}],
                "ET": [{"total": 82}],
                "PRM": [{"total": 70}],
            }
        }
    )
    matched = gate.build_matched_table(state)
    assert set(matched["PR1"].keys()) == {"ET", "PRM"}


def test_nested_schema_five_prs_passes_gate():
    """5 PRs x 3 techniques x n=3 rows each with reversals -> gate passes."""
    rubric = {}
    score_matrix = {
        "PR1": {"SR": [90, 91, 92], "ET": [80, 81, 79], "PRM": [85, 84, 86]},
        "PR2": {"SR": [70, 71, 72], "ET": [85, 86, 84], "PRM": [88, 87, 89]},
        "PR3": {"SR": [92, 91, 93], "ET": [75, 76, 74], "PRM": [70, 71, 69]},
        "PR4": {"SR": [60, 61, 59], "ET": [90, 89, 91], "PRM": [95, 94, 96]},
        "PR5": {"SR": [88, 87, 89], "ET": [84, 85, 83], "PRM": [70, 71, 72]},
    }
    for pr_id, techs in score_matrix.items():
        rubric[pr_id] = {t: [{"total": s} for s in scores] for t, scores in techs.items()}
    state = _state(rubric)
    report = gate.evaluate(state, min_matched=5, min_reversals=2)
    assert report["passed"] is True
    assert report["matched_prs"] == 5
    assert report["reversals"] >= 2


def test_mixed_flat_and_nested_schema():
    """Legacy flat entries and new nested entries can coexist in rubric_scores."""
    state = _state(
        {
            "LEGACY1": {"technique": "SR", "total": 85},  # flat, no match (only 1 tech)
            "PR1": {
                "SR": [{"total": 90}],
                "ET": [{"total": 80}],
            },
        }
    )
    matched = gate.build_matched_table(state)
    assert "LEGACY1" not in matched  # single-technique flat entry dropped
    assert matched["PR1"] == {"SR": 90.0, "ET": 80.0}


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

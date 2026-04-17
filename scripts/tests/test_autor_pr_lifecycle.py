"""Tests for the autor PR lifecycle enforcement pair.

Covers:
  - `scripts/autor_pr.py`:
      - open_draft_autor_pr forces --draft + labels + [autor][<tech>] title
      - close_after_score refuses when score JSON is missing or invalid
  - `scripts/validate_autor_pr_lifecycle.py`:
      - happy path (draft+scored, closed+scored) passes
      - MERGED autor PR -> policy violation
      - OPEN not-draft -> violation
      - OPEN draft without score past grace -> violation
      - CLOSED without score -> violation
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import autor_pr  # noqa: E402
import validate_autor_pr_lifecycle as gate  # noqa: E402


# -------------------------
# autor_pr.py helpers
# -------------------------


def _fake_completed(stdout: str = "", returncode: int = 0):
    cp = mock.Mock()
    cp.stdout = stdout
    cp.stderr = ""
    cp.returncode = returncode
    return cp


def test_open_draft_autor_pr_forces_draft_and_labels(monkeypatch):
    captured = {}

    def fake_run(cmd, check, capture_output, text):  # noqa: ARG001
        captured["cmd"] = cmd
        return _fake_completed(
            stdout="https://github.com/jleechanorg/worldarchitect.ai/pull/9999\n"
        )

    monkeypatch.setattr(autor_pr.subprocess, "run", fake_run)

    pr = autor_pr.open_draft_autor_pr(
        technique="SR",
        title="refactor level-up normalization",
        body="See research-wiki/scores/...",
        branch="autor/sr-6277",
    )

    assert pr == 9999
    cmd = captured["cmd"]
    assert cmd[0] == "gh"
    assert "--draft" in cmd
    # label flags appear as pairs
    label_args = [cmd[i + 1] for i, tok in enumerate(cmd) if tok == "--label"]
    assert "autor" in label_args
    assert "technique:SR" in label_args
    title_idx = cmd.index("--title")
    assert cmd[title_idx + 1].startswith("[autor][SR] ")


def test_open_draft_rejects_unknown_technique(monkeypatch):
    monkeypatch.setattr(
        autor_pr.subprocess, "run", lambda *a, **kw: _fake_completed()
    )
    with pytest.raises(autor_pr.AutorLifecycleError):
        autor_pr.open_draft_autor_pr(
            technique="Oracle",
            title="...",
            body="...",
            branch="autor/x",
        )


def test_close_after_score_requires_artifact(tmp_path, monkeypatch):
    monkeypatch.setattr(
        autor_pr.subprocess, "run", lambda *a, **kw: _fake_completed()
    )
    missing = tmp_path / "nope.json"
    with pytest.raises(FileNotFoundError):
        autor_pr.close_after_score(
            pr=1234, technique="PRM", score=82.0, score_json_path=missing
        )


def test_close_after_score_rejects_invalid_json(tmp_path, monkeypatch):
    monkeypatch.setattr(
        autor_pr.subprocess, "run", lambda *a, **kw: _fake_completed()
    )
    bad = tmp_path / "bad.json"
    bad.write_text("not json{")
    with pytest.raises(autor_pr.AutorLifecycleError):
        autor_pr.close_after_score(
            pr=1234, technique="PRM", score=82.0, score_json_path=bad
        )


def test_close_after_score_calls_gh_pr_close(tmp_path, monkeypatch):
    artifact = tmp_path / "prm_6277_20260417.json"
    artifact.write_text(json.dumps({"total": 82}))
    captured = {}

    def fake_run(cmd, check, capture_output, text):  # noqa: ARG001
        captured["cmd"] = cmd
        return _fake_completed()

    monkeypatch.setattr(autor_pr.subprocess, "run", fake_run)

    autor_pr.close_after_score(
        pr=6277, technique="PRM", score=82.0, score_json_path=artifact
    )

    cmd = captured["cmd"]
    assert cmd[:4] == ["gh", "pr", "close", "6277"]
    comment_idx = cmd.index("--comment")
    assert "PRM" in cmd[comment_idx + 1]
    assert "82.0/100" in cmd[comment_idx + 1]


# -------------------------
# gate helpers
# -------------------------


NOW = datetime(2026, 4, 17, 12, 0, tzinfo=timezone.utc)


def _pr(
    *,
    number: int,
    state: str,
    is_draft: bool = False,
    technique: str = "SR",
    created_hours_ago: int = 1,
    merged: bool = False,
):
    pr = {
        "number": number,
        "state": state,
        "isDraft": is_draft,
        "title": f"[autor][{technique}] change",
        "labels": [{"name": "autor"}, {"name": f"technique:{technique}"}],
        "headRefName": f"autor/{technique.lower()}-{number}",
        "createdAt": (NOW - timedelta(hours=created_hours_ago)).isoformat(),
        "mergedAt": NOW.isoformat() if merged else None,
        "closedAt": NOW.isoformat() if state == "CLOSED" or merged else None,
    }
    return pr


def _with_artifact(score_dir: Path, pr: int, technique: str) -> Path:
    path = score_dir / f"{technique}_{pr}_20260417T000000Z.json"
    path.write_text(json.dumps({"total": 82}))
    return path


def test_gate_happy_path(tmp_path):
    score_dir = tmp_path / "scores"
    score_dir.mkdir()
    _with_artifact(score_dir, 6277, "SR")
    _with_artifact(score_dir, 6278, "PRM")
    prs = [
        _pr(number=6277, state="OPEN", is_draft=True, technique="SR"),
        _pr(number=6278, state="CLOSED", technique="PRM"),
    ]
    violations = gate.evaluate(prs, score_dir, grace_hours=24, now=NOW)
    assert violations == []


def test_gate_flags_merged(tmp_path):
    score_dir = tmp_path / "scores"
    score_dir.mkdir()
    _with_artifact(score_dir, 6279, "ET")
    prs = [_pr(number=6279, state="MERGED", merged=True, technique="ET")]
    violations = gate.evaluate(prs, score_dir, grace_hours=24, now=NOW)
    assert [v.kind for v in violations] == ["MERGED"]


def test_gate_flags_ready_for_review(tmp_path):
    score_dir = tmp_path / "scores"
    score_dir.mkdir()
    _with_artifact(score_dir, 6280, "SR")
    prs = [_pr(number=6280, state="OPEN", is_draft=False, technique="SR")]
    violations = gate.evaluate(prs, score_dir, grace_hours=24, now=NOW)
    assert [v.kind for v in violations] == ["OPEN_NOT_DRAFT"]


def test_gate_flags_open_without_score_past_grace(tmp_path):
    score_dir = tmp_path / "scores"
    score_dir.mkdir()
    prs = [
        _pr(
            number=6281,
            state="OPEN",
            is_draft=True,
            technique="SR",
            created_hours_ago=48,
        )
    ]
    violations = gate.evaluate(prs, score_dir, grace_hours=24, now=NOW)
    assert [v.kind for v in violations] == ["OPEN_NO_SCORE"]


def test_gate_allows_open_without_score_within_grace(tmp_path):
    score_dir = tmp_path / "scores"
    score_dir.mkdir()
    prs = [
        _pr(
            number=6282,
            state="OPEN",
            is_draft=True,
            technique="SR",
            created_hours_ago=1,
        )
    ]
    violations = gate.evaluate(prs, score_dir, grace_hours=24, now=NOW)
    assert violations == []


def test_gate_flags_closed_without_score(tmp_path):
    score_dir = tmp_path / "scores"
    score_dir.mkdir()
    prs = [_pr(number=6283, state="CLOSED", technique="PRM")]
    violations = gate.evaluate(prs, score_dir, grace_hours=24, now=NOW)
    assert [v.kind for v in violations] == ["CLOSED_NO_SCORE"]


def test_gate_technique_from_title_when_label_missing(tmp_path):
    score_dir = tmp_path / "scores"
    score_dir.mkdir()
    _with_artifact(score_dir, 6284, "ET")
    pr = _pr(number=6284, state="CLOSED", technique="ET")
    pr["labels"] = [{"name": "autor"}]
    violations = gate.evaluate([pr], score_dir, grace_hours=24, now=NOW)
    assert violations == []

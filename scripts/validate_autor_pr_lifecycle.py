"""Gate that enforces the autor PR lifecycle (draft -> score -> close, never merge).

Enumerates every PR labeled `autor` via `gh` and flags:
  - MERGED: policy violation (autor PRs are evaluation artifacts, never merged)
  - OPEN + not draft: ready-for-review violation
  - OPEN + draft + no matching score artifact older than grace period
  - CLOSED with no matching score artifact (incomplete evaluation)

Exit codes:
  0 - all autor PRs are compliant
  1 - one or more violations
  2 - input error (gh missing, auth failure, bad args)

This is paired with `scripts/autor_pr.py`. If you bypassed the helpers and
called `gh pr create` directly, expect this gate to fail.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

DEFAULT_REPO = "jleechanorg/worldarchitect.ai"
DEFAULT_SCORE_DIR = Path("research-wiki/scores")
DEFAULT_GRACE_HOURS = 24
TECHNIQUE_LABEL_PREFIX = "technique:"


@dataclass
class Violation:
    pr: int
    kind: str
    detail: str

    def format(self) -> str:
        return f"  - PR #{self.pr}: {self.kind} — {self.detail}"


@dataclass
class GateResult:
    violations: list[Violation] = field(default_factory=list)
    checked: int = 0
    repo: str = DEFAULT_REPO

    @property
    def ok(self) -> bool:
        return not self.violations


def _run_gh(args: list[str]) -> str:
    result = subprocess.run(
        ["gh", *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"gh {' '.join(args)} failed (rc={result.returncode}): {result.stderr.strip()}"
        )
    return result.stdout


def list_autor_prs(repo: str) -> list[dict]:
    raw = _run_gh(
        [
            "pr",
            "list",
            "--repo",
            repo,
            "--label",
            "autor",
            "--state",
            "all",
            "--limit",
            "200",
            "--json",
            "number,state,isDraft,title,labels,headRefName,createdAt,mergedAt,closedAt",
        ]
    )
    return json.loads(raw or "[]")


def technique_of(pr: dict) -> str | None:
    for label in pr.get("labels", []) or []:
        name = label.get("name") if isinstance(label, dict) else label
        if isinstance(name, str) and name.startswith(TECHNIQUE_LABEL_PREFIX):
            return name[len(TECHNIQUE_LABEL_PREFIX):]
    match = re.search(r"\[autor\]\[([^\]]+)\]", pr.get("title", ""))
    return match.group(1) if match else None


def find_score_artifact(
    pr: int,
    technique: str | None,
    score_dir: Path,
) -> Path | None:
    if not score_dir.is_dir():
        return None
    needle = f"_{pr}_"
    candidates = [p for p in score_dir.iterdir() if p.is_file() and needle in p.name]
    if technique:
        tech_lower = technique.lower()
        tech_candidates = [p for p in candidates if p.name.lower().startswith(tech_lower)]
        if tech_candidates:
            return tech_candidates[0]
    return candidates[0] if candidates else None


def _parse_ts(ts: str | None) -> datetime | None:
    if not ts:
        return None
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def evaluate(
    prs: Iterable[dict],
    score_dir: Path,
    grace_hours: int,
    now: datetime | None = None,
) -> list[Violation]:
    now = now or datetime.now(timezone.utc)
    grace = timedelta(hours=grace_hours)
    violations: list[Violation] = []

    for pr in prs:
        number = pr.get("number")
        if not isinstance(number, int):
            continue
        state = (pr.get("state") or "").upper()
        is_draft = bool(pr.get("isDraft"))
        merged_at = _parse_ts(pr.get("mergedAt"))
        created_at = _parse_ts(pr.get("createdAt"))
        technique = technique_of(pr)

        if merged_at is not None or state == "MERGED":
            violations.append(
                Violation(
                    pr=number,
                    kind="MERGED",
                    detail="autor PRs must never be merged (policy violation)",
                )
            )
            continue

        artifact = find_score_artifact(number, technique, score_dir)

        if state == "OPEN":
            if not is_draft:
                violations.append(
                    Violation(
                        pr=number,
                        kind="OPEN_NOT_DRAFT",
                        detail="autor PR must be draft while open",
                    )
                )
            if artifact is None and created_at is not None and (now - created_at) > grace:
                violations.append(
                    Violation(
                        pr=number,
                        kind="OPEN_NO_SCORE",
                        detail=(
                            f"no score artifact in {score_dir} after "
                            f"{grace_hours}h (technique={technique})"
                        ),
                    )
                )
        elif state == "CLOSED":
            if artifact is None:
                violations.append(
                    Violation(
                        pr=number,
                        kind="CLOSED_NO_SCORE",
                        detail=(
                            f"closed without a matching score artifact in {score_dir}"
                            f" (technique={technique})"
                        ),
                    )
                )

    return violations


def run(
    repo: str,
    score_dir: Path,
    grace_hours: int,
) -> GateResult:
    prs = list_autor_prs(repo)
    violations = evaluate(prs, score_dir, grace_hours)
    return GateResult(violations=violations, checked=len(prs), repo=repo)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=DEFAULT_REPO)
    parser.add_argument(
        "--score-dir",
        type=Path,
        default=DEFAULT_SCORE_DIR,
        help="Directory containing per-PR score JSON artifacts",
    )
    parser.add_argument(
        "--grace-hours",
        type=int,
        default=DEFAULT_GRACE_HOURS,
        help="Hours an autor PR may be open without a score artifact",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        result = run(args.repo, args.score_dir, args.grace_hours)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        payload = {
            "ok": result.ok,
            "checked": result.checked,
            "repo": result.repo,
            "violations": [
                {"pr": v.pr, "kind": v.kind, "detail": v.detail}
                for v in result.violations
            ],
        }
        print(json.dumps(payload, indent=2))
    else:
        print(f"autor lifecycle gate — checked {result.checked} PRs on {result.repo}")
        if result.ok:
            print("PASS: every autor PR is compliant")
        else:
            print(f"FAIL: {len(result.violations)} violation(s)")
            for v in result.violations:
                print(v.format())

    return 0 if result.ok else 1


if __name__ == "__main__":
    sys.exit(main())

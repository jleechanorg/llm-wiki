#!/usr/bin/env python3
"""oracle_uplift.py — compute the oracle-vs-baseline uplift for br-v84.

Reads the matched-corpus bandit state and prints the three numbers the
router decision matrix depends on:

    oracle   = mean over PRs of max(cell_mean[tech]) for tech in techniques
    baseline = max over techniques of (mean over PRs of cell_mean[tech])
    uplift   = oracle - baseline

A cell_mean is the mean of the `total` field across all rubric rows stored
under rubric_scores[pr][tech]. Only PRs with cell means for *every* tracked
technique contribute, so the computation is symmetric.

Exit codes:
  0 — printed a full uplift report (caller inspects stdout)
  2 — input error (missing state file, malformed JSON, no eligible PRs)

Pure Python, no external deps. Kept standalone so the dumb-agent prompt does
not need to shell-escape f-string braces inside a heredoc. See
`~/roadmap/2026-04-17-dumb-agent-prompt-matched-corpus.md` Step 2.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path
from typing import Any

DEFAULT_STATE = Path("technique_bandit/bandit_state.json")
DEFAULT_TECHS = ("SR", "ET", "PRM")


def cell_mean(rubric: dict[str, Any], pr: str, tech: str) -> float | None:
    entry = rubric.get(pr)
    if not isinstance(entry, dict):
        return None
    rows = entry.get(tech)
    if not isinstance(rows, list):
        return None
    totals = [
        float(r["total"])
        for r in rows
        if isinstance(r, dict) and isinstance(r.get("total"), (int, float))
    ]
    if not totals:
        return None
    return sum(totals) / len(totals)


def eligible_prs(rubric: dict[str, Any], techniques: tuple[str, ...]) -> list[str]:
    """PRs that have at least one numeric cell mean for every technique."""
    out: list[str] = []
    for pr in rubric:
        if all(cell_mean(rubric, pr, t) is not None for t in techniques):
            out.append(pr)
    return out


def compute(state: dict[str, Any], techniques: tuple[str, ...]) -> dict[str, Any]:
    rubric = state.get("rubric_scores") or {}
    prs = eligible_prs(rubric, techniques)
    if not prs:
        return {
            "eligible_prs": [],
            "per_tech_means": {},
            "per_pr_max": {},
            "oracle": None,
            "baseline": None,
            "uplift": None,
        }

    per_pr_max = {pr: max(cell_mean(rubric, pr, t) for t in techniques) for pr in prs}
    per_tech_means = {
        t: statistics.mean(cell_mean(rubric, pr, t) for pr in prs) for t in techniques
    }

    oracle = statistics.mean(per_pr_max.values())
    baseline = max(per_tech_means.values())
    return {
        "eligible_prs": prs,
        "per_tech_means": per_tech_means,
        "per_pr_max": per_pr_max,
        "oracle": oracle,
        "baseline": baseline,
        "uplift": oracle - baseline,
    }


def format_report(report: dict[str, Any]) -> str:
    if not report["eligible_prs"]:
        return (
            "no eligible PRs (rubric_scores is empty or no PR has a numeric "
            "cell mean for every tracked technique)"
        )
    lines = [
        "oracle-vs-baseline uplift",
        f"  eligible PRs: {len(report['eligible_prs'])} ({', '.join(report['eligible_prs'])})",
        "  per-technique means:",
    ]
    for tech, m in sorted(report["per_tech_means"].items()):
        lines.append(f"    {tech}: {m:.2f}")
    lines.append("  per-PR max (oracle picks):")
    for pr, m in sorted(report["per_pr_max"].items()):
        lines.append(f"    {pr}: {m:.2f}")
    lines.append(f"  oracle   = {report['oracle']:.2f}")
    lines.append(f"  baseline = {report['baseline']:.2f}")
    lines.append(f"  uplift   = {report['uplift']:.2f}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    parser.add_argument(
        "--techniques",
        nargs="+",
        default=list(DEFAULT_TECHS),
        help="Techniques that must all have rubric rows for a PR to count.",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if not args.state.exists():
        print(f"ERROR: bandit state not found: {args.state}", file=sys.stderr)
        return 2
    try:
        state = json.loads(args.state.read_text())
    except json.JSONDecodeError as exc:
        print(f"ERROR: malformed bandit state JSON: {exc}", file=sys.stderr)
        return 2

    report = compute(state, tuple(args.techniques))
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True, default=float))
    else:
        print(format_report(report))
    return 0 if report["eligible_prs"] else 2


if __name__ == "__main__":
    sys.exit(main())

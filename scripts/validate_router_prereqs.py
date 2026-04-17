#!/usr/bin/env python3
"""
validate_router_prereqs.py — structural gate for PR-type → technique router work.

Before any router code is written (br-5bj and successors), this script MUST
return exit 0. It is intentionally dumb and deterministic: it enforces the
empirical precondition that makes a router plausibly useful.

Prerequisite the gate enforces:
  - At least MIN_MATCHED_PRS distinct PRs must be scored by ALL tracked
    techniques (matched evaluations).
  - Among those matched PRs, at least MIN_REVERSALS ranking reversals must
    exist — i.e. technique A beats B on one PR while B beats A on another.

Without matched-PR reversals a router cannot add value over "always pick the
technique with the highest mean", regardless of how clever the routing logic
is. This is the ZFC-compliant structural check: no model-based judgment, just
counts from the bandit corpus.

Inputs:
  --state PATH   Path to bandit_state.json (default: technique_bandit/bandit_state.json)
  --min-matched  Minimum matched-PR count (default: 5)
  --min-reversals Minimum ranking reversals (default: 2)
  --json         Emit machine-readable JSON report instead of human text

Exit codes:
  0  Prerequisites satisfied; router work may proceed.
  1  Prerequisites NOT satisfied; router work is blocked. Prints a fail report.
  2  Input error (missing file, malformed JSON, etc.).

See: research-wiki/syntheses/cycle_phase4_final_synthesis.md and CLAUDE.md
"Router prerequisite gate" section.
"""

from __future__ import annotations

import argparse
import json
import sys
from itertools import combinations
from pathlib import Path
from typing import Any

DEFAULT_STATE = Path("technique_bandit/bandit_state.json")
DEFAULT_MIN_MATCHED = 5
DEFAULT_MIN_REVERSALS = 2


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"bandit state not found: {path}")
    return json.loads(path.read_text())


def build_matched_table(state: dict[str, Any]) -> dict[str, dict[str, float]]:
    """Return {pr_id: {technique: score}} for PRs scored by 2+ techniques.

    A PR "match" requires the same pr_id to appear in the per-technique
    records AND in rubric_scores with a total. Techniques lists raw scores
    without PR mapping, so this gate treats rubric_scores as the authoritative
    matched table: each rubric entry must include a "technique" field for it
    to count. Any rubric entry without an explicit technique is ignored.
    """
    rubric = state.get("rubric_scores", {}) or {}
    table: dict[str, dict[str, float]] = {}
    for pr_id, entry in rubric.items():
        if not isinstance(entry, dict):
            continue
        technique = entry.get("technique")
        total = entry.get("total")
        if not technique or not isinstance(total, (int, float)):
            continue
        table.setdefault(str(pr_id), {})[str(technique)] = float(total)
    return {pr: row for pr, row in table.items() if len(row) >= 2}


def count_reversals(matched: dict[str, dict[str, float]]) -> int:
    """Count ranking reversals across all technique pairs.

    For each unordered pair of techniques (A, B), find PRs where both were
    scored. A reversal exists when there is at least one PR with A > B AND at
    least one PR with B > A. Each pair contributes at most 1 reversal to the
    count — we are measuring pair-level evidence of disagreement, not the
    number of PR-level swaps.
    """
    techniques = sorted({t for row in matched.values() for t in row})
    reversals = 0
    for a, b in combinations(techniques, 2):
        a_wins = b_wins = 0
        for row in matched.values():
            if a in row and b in row:
                if row[a] > row[b]:
                    a_wins += 1
                elif row[b] > row[a]:
                    b_wins += 1
        if a_wins >= 1 and b_wins >= 1:
            reversals += 1
    return reversals


def evaluate(
    state: dict[str, Any],
    min_matched: int,
    min_reversals: int,
) -> dict[str, Any]:
    matched = build_matched_table(state)
    reversals = count_reversals(matched)
    matched_n = len(matched)
    techniques_in_state = sorted((state.get("techniques") or {}).keys())
    passed = matched_n >= min_matched and reversals >= min_reversals
    return {
        "passed": passed,
        "matched_prs": matched_n,
        "min_matched_required": min_matched,
        "reversals": reversals,
        "min_reversals_required": min_reversals,
        "matched_detail": matched,
        "techniques_in_state": techniques_in_state,
    }


def format_report(report: dict[str, Any]) -> str:
    lines = []
    status = "PASS" if report["passed"] else "FAIL"
    lines.append(f"Router prerequisite gate: {status}")
    lines.append(
        f"  matched PRs: {report['matched_prs']} "
        f"(required ≥ {report['min_matched_required']})"
    )
    lines.append(
        f"  ranking reversals: {report['reversals']} "
        f"(required ≥ {report['min_reversals_required']})"
    )
    lines.append(
        f"  techniques in bandit state: {report['techniques_in_state'] or '(none)'}"
    )
    if not report["passed"]:
        lines.append("")
        lines.append("Router work is BLOCKED until:")
        lines.append(
            "  1. At least "
            f"{report['min_matched_required']} PRs are scored by ALL tracked "
            "techniques (matched evaluations recorded in rubric_scores with"
            ' an explicit "technique" field).'
        )
        lines.append(
            "  2. Those matched scores contain at least "
            f"{report['min_reversals_required']} ranking reversals across "
            "technique pairs."
        )
        lines.append("")
        lines.append(
            "Without ranking reversals, a router cannot beat 'always pick the"
            " top-mean technique'. Build the matched corpus first; then this"
            " gate unblocks."
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--min-matched", type=int, default=DEFAULT_MIN_MATCHED)
    parser.add_argument("--min-reversals", type=int, default=DEFAULT_MIN_REVERSALS)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        state = load_state(args.state)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: malformed bandit state JSON: {exc}", file=sys.stderr)
        return 2

    report = evaluate(state, args.min_matched, args.min_reversals)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_report(report))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())

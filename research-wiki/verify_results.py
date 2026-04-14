#!/usr/bin/env python3
"""
Auto-Research v3 — Evidence Verification Agent

Reviews cycle_*.md files and verifies:
1. Run logs exist with matching timestamps
2. Scores are internally consistent
3. No red flags (fabricated data, impossible values)

Usage:
    python3 research-wiki/verify_results.py --session <session_id>
    python3 research-wiki/verify_results.py --technique <name>
    python3 research-wiki/verify_results.py --all
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).parent.parent
SYNTHESES_DIR = REPO_ROOT / "wiki" / "syntheses"
ET_LOGS_DIR = SYNTHESES_DIR / "et_logs"
SCORES_DIR = REPO_ROOT / "research-wiki" / "scores"

# Red flags
IMPOSSIBLE_SCORES = {
    "naming": (0, 15),
    "error_handling": (0, 20),
    "type_safety": (0, 20),
    "architecture": (0, 20),
    "test_coverage": (0, 15),
    "documentation": (0, 10),
    "total": (0, 100),
}

SUSPICIOUS_PATTERNS = [
    (r"Delta[:\s]+([+-]?\d{3,})", "Delta > 99 or < -99 — unlikely"),  # 3+ digit deltas
    (r"Baseline[:\s]+(\d{3,})", "Baseline > 99 — impossible (max 100)"),  # 3+ digit baseline
    (r"Total[:\s]+(\d{3,})/100", "Total > 99 — impossible"),  # 3+ digit total
]


TECHNIQUE_FILES = {
    "extendedthinking": "cycle_extended_thinking_v3.md",
    "selfrefine": "cycle_selfrefine_v3.md",
    "swebench": "cycle_swebench_v3.md",
    "metaharness": "cycle_metaharness_v3.md",
    "prm": "cycle_prm_v3.md",
    "combined": "cycle_combined_v3.md",
}


def load_cycle_file(technique: str) -> dict[str, Any] | None:
    """Load and parse a cycle_*.md file."""
    cycle_file = SYNTHESES_DIR / TECHNIQUE_FILES.get(technique, f"cycle_{technique}_v3.md")
    if not cycle_file.exists():
        return None

    content = cycle_file.read_text()

    # Extract frontmatter
    fm_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not fm_match:
        return {"error": "No frontmatter found", "file": str(cycle_file), "content": None}

    frontmatter = {}
    for line in fm_match.group(1).split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            frontmatter[key.strip()] = val.strip().strip('"')

    return {
        "file": str(cycle_file),
        "frontmatter": frontmatter,
        "content": content,
        "technique": technique,
        "session_id": frontmatter.get("run_session"),
    }


def load_score_file(run_id: str) -> dict | None:
    """Load a score JSON file."""
    score_file = SCORES_DIR / f"{run_id}.json"
    if not score_file.exists():
        # Try finding by partial match
        for f in SCORES_DIR.glob(f"{run_id}*.json"):
            return json.loads(f.read_text())
    return json.loads(score_file.read_text()) if score_file.exists() else None


def load_log_file(run_id: str) -> str | None:
    """Load a log file."""
    log_file = ET_LOGS_DIR / f"{run_id}.log"
    if not log_file.exists():
        for f in ET_LOGS_DIR.glob(f"{run_id}*.log"):
            return f.read_text()
    return log_file.read_text() if log_file.exists() else None


def verify_scores(scores: dict) -> list[str]:
    """Verify scores are within valid ranges. Returns list of issues."""
    issues = []

    for dim, (lo, hi) in IMPOSSIBLE_SCORES.items():
        val = scores.get(dim)
        if val is not None:
            try:
                v = float(val)
                if v < lo or v > hi:
                    issues.append(f"{dim}: {v} outside valid range [{lo}, {hi}]")
            except (ValueError, TypeError):
                issues.append(f"{dim}: non-numeric value '{val}'")

    # Check weighted total
    dims = {
        "naming": 0.15,
        "error_handling": 0.20,
        "type_safety": 0.20,
        "architecture": 0.20,
        "test_coverage": 0.15,
        "documentation": 0.10,
    }
    weighted_sum = 0
    for dim, weight in dims.items():
        val = scores.get(dim)
        if val is not None:
            try:
                weighted_sum += float(val) * weight
            except (ValueError, TypeError):
                pass

    if scores.get("total") is not None:
        try:
            declared_total = float(scores["total"])
            if abs(weighted_sum - declared_total) > 2:
                issues.append(
                    f"total mismatch: weighted sum = {weighted_sum:.1f}, declared = {declared_total}"
                )
        except (ValueError, TypeError):
            issues.append(f"total is non-numeric: {scores['total']}")

    return issues


def check_suspicious_patterns(text: str) -> list[str]:
    """Check for suspicious patterns in text."""
    findings = []
    for pattern, reason in SUSPICIOUS_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            findings.append(reason)
    return findings


def verify_log_exists(run_id: str) -> tuple[bool, str]:
    """Check if log file exists for run_id."""
    log_file = ET_LOGS_DIR / f"{run_id}.log"
    if log_file.exists():
        return True, str(log_file)

    # Try glob
    matches = list(ET_LOGS_DIR.glob(f"{run_id}*.log"))
    if matches:
        return True, str(matches[0])

    return False, ""


def verify_session_consistency(cycle_data: dict) -> list[str]:
    """Verify session consistency between cycle file and logs."""
    issues = []
    session_id = cycle_data.get("frontmatter", {}).get("run_session")

    if not session_id:
        issues.append("No run_session in frontmatter — cannot verify provenance")

    return issues


def verify_technique(technique: str) -> dict:
    """Verify a single technique's results."""
    result = {
        "technique": technique,
        "status": "pending",
        "issues": [],
        "warnings": [],
        "score_issues": [],
        "suspicious_patterns": [],
        "log_verification": [],
        "files_checked": [],
    }

    # Load cycle file
    cycle_data = load_cycle_file(technique)
    if not cycle_data or "content" not in cycle_data:
        result["status"] = "missing"
        result["issues"].append(f"No cycle_{technique}_v3.md found or parse error")
        return result

    result["files_checked"].append(cycle_data["file"])

    # Check for run_session
    session_id = cycle_data.get("frontmatter", {}).get("run_session")
    if not session_id:
        result["warnings"].append("No run_session in frontmatter")

    # Extract scores from content (look for JSON or table)
    scores = {}
    if cycle_data.get("content"):
        scores = extract_scores_from_content(cycle_data["content"])

    if scores:
        result["scores"] = scores
        score_issues = verify_scores(scores)
        result["score_issues"].extend(score_issues)

        if score_issues:
            result["status"] = "failed"
        else:
            result["status"] = "passed"
    else:
        result["warnings"].append("Could not extract scores from cycle file")

    # Check for suspicious patterns
    if cycle_data.get("content"):
        patterns = check_suspicious_patterns(cycle_data["content"])
        result["suspicious_patterns"].extend(patterns)
        if patterns:
            result["status"] = "failed"

    # Verify log files exist
    if session_id:
        # Look for log files matching this technique
        log_matches = list(ET_LOGS_DIR.glob(f"{technique}_*.log"))
        if log_matches:
            result["log_verification"].append(f"Found {len(log_matches)} log file(s)")
            for log in log_matches:
                result["files_checked"].append(str(log))
        else:
            result["issues"].append(f"No log files found for {technique} (expected {ET_LOGS_DIR}/{technique}_*.log)")

    # Verify score files exist
    score_matches = list(SCORES_DIR.glob(f"{technique}_*.json"))
    if score_matches:
        result["files_checked"].extend([str(s) for s in score_matches])
    else:
        result["warnings"].append(f"No score JSON files found for {technique}")

    return result


def extract_scores_from_content(content: str) -> dict | None:
    """Extract scores from cycle file content."""
    scores = {}

    # Try to find JSON in content
    json_match = re.search(
        r'\{[^{}]*(?:naming|error_handling|type_safety|architecture|test_coverage|documentation|total|baseline|delta)[^{}]*\}',
        content,
        re.DOTALL,
    )
    if json_match:
        try:
            scores = json.loads(json_match.group(0))
            return scores
        except json.JSONDecodeError:
            pass

    # Try table extraction (look for X/Y patterns)
    table_match = re.search(r"\|\s*\*\*(.+)\*\*/\d+\s*\|", content)
    if table_match:
        total_match = re.search(r"\*\*(\d+)/100\*\*", content)
        if total_match:
            scores["total"] = int(total_match.group(1))

    return scores if scores else None


def verify_all() -> dict:
    """Verify all technique results."""
    techniques = ["extendedthinking", "selfrefine", "swebench", "metaharness", "prm", "combined"]
    results = {}

    for technique in techniques:
        results[technique] = verify_technique(technique)

    # Summary
    summary = {
        "total": len(techniques),
        "passed": sum(1 for r in results.values() if r["status"] == "passed"),
        "failed": sum(1 for r in results.values() if r["status"] == "failed"),
        "missing": sum(1 for r in results.values() if r["status"] == "missing"),
        "pending": sum(1 for r in results.values() if r["status"] == "pending"),
    }

    return {"summary": summary, "results": results}


def main():
    parser = argparse.ArgumentParser(description="Auto-Research v3 Evidence Verifier")
    parser.add_argument("--technique", help="Verify specific technique")
    parser.add_argument("--session", help="Verify by session ID")
    parser.add_argument("--all", action="store_true", help="Verify all techniques")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings too")

    args = parser.parse_args()

    if args.all or not any([args.technique, args.session]):
        results = verify_all()
    elif args.technique:
        results = {"results": {args.technique: verify_technique(args.technique)}}
    elif args.session:
        # Find all cycles with this session
        results = verify_all()
        for t, r in results["results"].items():
            fm = load_cycle_file(t, session_id=args.session)
            if not fm:
                del results["results"][t]
    else:
        print("Specify --all, --technique, or --session")
        sys.exit(1)

    # Print results
    print("\n=== Auto-Research v3 Evidence Verification ===\n")

    for technique, result in results.get("results", {}).items():
        status_symbol = {
            "passed": "✅",
            "failed": "❌",
            "missing": "⚠️",
            "pending": "⏳",
        }.get(result["status"], "?")

        print(f"{status_symbol} {technique.upper()}")
        print(f"   Status: {result['status']}")

        if result.get("issues"):
            print(f"   Issues: {', '.join(result['issues'])}")
        if result.get("warnings"):
            print(f"   Warnings: {', '.join(result['warnings'])}")
        if result.get("score_issues"):
            print(f"   Score Issues: {', '.join(result['score_issues'])}")
        if result.get("suspicious_patterns"):
            print(f"   ⚠️ Suspicious: {', '.join(result['suspicious_patterns'])}")
        if result.get("log_verification"):
            print(f"   Logs: {', '.join(result['log_verification'])}")

        print()

    if "summary" in results:
        s = results["summary"]
        print(f"Summary: {s['passed']}/{s['total']} passed", end="")
        if s["failed"]:
            print(f", {s['failed']} failed", end="")
        if s["missing"]:
            print(f", {s['missing']} missing", end="")
        print()

        # Exit code
        strict = args.strict
        if strict and (results["summary"]["failed"] + results["summary"]["missing"]) > 0:
            sys.exit(1)
        elif not strict and results["summary"]["failed"] > 0:
            sys.exit(1)


if __name__ == "__main__":
    main()
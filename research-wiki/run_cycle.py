#!/usr/bin/env python3
"""
Auto-Research v3 — Execution Runner

Usage:
    python3 research-wiki/run_cycle.py --technique <name> --prs <pr_list>
    python3 research-wiki/run_cycle.py --technique all --prs all
    python3 research-wiki/run_cycle.py --technique extendedthinking --prs WA-001,WA-004,WA-005

Techniques: extendedthinking, selfrefine, swebench, metaharness, prm, combined
PRs: WA-001 (small), WA-004 (medium), WA-005 (complex), or 'all'
"""

import argparse
import json
import os
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).parent.parent
TEST_PRS_DIR = REPO_ROOT / "test-prs"
ET_LOGS_DIR = REPO_ROOT / "wiki" / "syntheses" / "et_logs"
SCORES_DIR = REPO_ROOT / "research-wiki" / "scores"
SYNTHESES_DIR = REPO_ROOT / "wiki" / "syntheses"
WORKTREE = Path.home() / ".worktrees" / "jleechanorg" / "worldarchitect.ai"

# Ensure directories exist
ET_LOGS_DIR.mkdir(parents=True, exist_ok=True)
SCORES_DIR.mkdir(parents=True, exist_ok=True)

# Techniques
TECHNIQUES = ["extendedthinking", "selfrefine", "swebench", "metaharness", "prm", "combined"]
PR_LIST = ["WA-001", "WA-004", "WA-005"]

# PR descriptions
PR_INFO = {
    "WA-001": {
        "name": "Level-Up RuntimeError",
        "type": "small",
        "size": "1-2 files, <50 lines",
        "description": "_synthesize_generic_rewards_box returns None causing RuntimeError",
        "issue": "#6205",
        "branch": "fix/rewards-box-schema-enforcement",
    },
    "WA-004": {
        "name": "CI-aware schema prompt perf ceiling",
        "type": "medium",
        "size": "3-5 files, 50-200 lines",
        "description": "20ms hard-coded ceiling fails under CI load",
        "issue": "#6261",
        "branch": "fix/ci-aware-schema-prompt",
    },
    "WA-005": {
        "name": "ProxyFix rate-limit regression",
        "type": "complex",
        "size": "5+ files, 200+ lines",
        "description": "level_up_complete=True but rewards_box missing, ASI injection needed",
        "issue": "#6214",
        "branch": "fix/stuck-level-up-completion-rewards-box-20260414",
    },
}


def git_provenance():
    """Capture git provenance for evidence."""
    result = {}
    try:
        result["head"] = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True
        ).strip()
        result["branch"] = subprocess.check_output(
            ["git", "branch", "--show-current"], text=True
        ).strip()
        result["origin_main"] = subprocess.check_output(
            ["git", "rev-parse", "origin/main"], text=True
        ).strip()
        result["commit_timestamp"] = subprocess.check_output(
            ["git", "log", "-1", "--format=%aI"], text=True
        ).strip()
        result["diff_stat"] = subprocess.check_output(
            ["git", "diff", "--stat", "origin/main..HEAD"], text=True
        ).strip()
    except Exception as e:
        result["error"] = str(e)
    return result


def run_technique(technique: str, pr: str, session_id: str) -> dict:
    """
    Run a single technique on a single PR.
    Returns dict with scores, logs, and evidence paths.
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = f"{technique}_{pr}_{timestamp}"

    log_file = ET_LOGS_DIR / f"{run_id}.log"
    score_file = SCORES_DIR / f"{run_id}.json"

    # Git provenance at run start
    provenance = git_provenance()
    provenance["run_id"] = run_id
    provenance["technique"] = technique
    provenance["pr"] = pr
    provenance["session_id"] = session_id

    result = {
        "run_id": run_id,
        "technique": technique,
        "pr": pr,
        "timestamp": timestamp,
        "provenance": provenance,
        "status": "running",
        "scores": {},
        "log_file": str(log_file),
        "score_file": str(score_file),
    }

    with open(log_file, "w") as f:
        f.write(f"=== Auto-Research v3 Run ===\n")
        f.write(f"Technique: {technique}\n")
        f.write(f"PR: {pr}\n")
        f.write(f"Run ID: {run_id}\n")
        f.write(f"Session: {session_id}\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Provenance: {json.dumps(provenance, indent=2)}\n")
        f.write(f"{'='*60}\n\n")

    # Read the PR description
    pr_info = PR_INFO.get(pr, {})
    pr_desc = pr_info.get("description", "")
    pr_type = pr_info.get("type", "unknown")

    # Build the agent prompt based on technique
    prompt = build_prompt(technique, pr, pr_desc, run_id, log_file)

    with open(log_file, "a") as f:
        f.write(f"\n=== Agent Prompt ===\n{prompt}\n")
        f.write(f"{'='*60}\n\n")

    # Execute in worktree via claude --dangerously-skip-permissions
    # Use minimax via claudem() if available, else fallback to claude
    worktree_git = WORKTREE / ".git"
    if not worktree_git.exists():
        result["status"] = "error"
        result["error"] = f"Worktree not found at {WORKTREE}"
        with open(log_file, "a") as f:
            f.write(f"\nERROR: Worktree not found at {WORKTREE}\n")
        return result

    # Run agent in worktree with the technique prompt
    try:
        # Build the agent command
        agent_cmd = f"""
        cd {WORKTREE}
        Use the {technique} technique to fix issue {pr_info.get('issue', pr)}.
        The bug: {pr_desc}
        Working directory: {WORKTREE}

        When done:
        1. Run the relevant tests
        2. Report exact scores for each dimension:
           - Naming (15%): score/15
           - Error Handling (20%): score/20
           - Type Safety (20%): score/20
           - Architecture (20%): score/20
           - Test Coverage (15%): score/15
           - Documentation (10%): score/10
        3. Calculate total: sum of weighted percentages (X/100)
        4. Compare to baseline and report delta

        Save scores to /tmp/scores_{technique}_{pr}.json
        """

        # Run via minimax if claudem available, else regular claude
        use_claudem = os.environ.get("CLAUDEM_PATH") or os.path.exists(
            os.path.expanduser("~/.claudem")
        )

        if use_claudem:
            cmd = ["bash", "-c", f"source ~/.bashrc 2>/dev/null; claudem '{agent_cmd}' 2>&1"]
        else:
            cmd = [
                "claude",
                "--dangerously-skip-permissions",
                "--model",
                "sonnet",
                "-p",
                agent_cmd,
            ]

        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=str(REPO_ROOT),
        )

        output_lines = []
        for line in proc.stdout:
            decoded = line.decode() if isinstance(line, bytes) else line
            output_lines.append(decoded)
            with open(log_file, "a") as f:
                f.write(decoded)

        proc.wait()

        # Parse scores from output
        scores = parse_scores_from_output(output_lines, technique, pr)

        result["scores"] = scores
        result["status"] = "completed"

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        with open(log_file, "a") as f:
            f.write(f"\nERROR: {e}\n")

    # Save scores to JSON
    with open(score_file, "w") as f:
        json.dump(result, f, indent=2)

    return result


def parse_scores_from_output(output_lines: list, technique: str, pr: str) -> dict:
    """Parse scores from agent output. Returns dict with dimension scores."""
    # Try to find JSON scores in output
    full_output = "\n".join(output_lines)

    # Look for score patterns
    scores = {
        "naming": None,
        "error_handling": None,
        "type_safety": None,
        "architecture": None,
        "test_coverage": None,
        "documentation": None,
        "total": None,
        "baseline": None,
        "delta": None,
    }

    # Try JSON extraction
    import re

    # Look for JSON score objects
    json_match = re.search(r'\{[^{]*"(naming|error_handling|type_safety|architecture|test_coverage|documentation|total|baseline|delta)"[^}]*\}', full_output, re.DOTALL)
    if json_match:
        try:
            parsed = json.loads(json_match.group(0))
            scores.update(parsed)
        except:
            pass

    # If no JSON, try text patterns
    if scores["total"] is None:
        # Look for "Total: X/100" pattern
        total_match = re.search(r"Total[:\s]+(\d+)/100", full_output, re.IGNORECASE)
        if total_match:
            scores["total"] = int(total_match.group(1))

        # Look for "Baseline: X" pattern
        baseline_match = re.search(r"Baseline[:\s]+(\d+)", full_output, re.IGNORECASE)
        if baseline_match:
            scores["baseline"] = int(baseline_match.group(1))

        # Look for "Delta: +X" pattern
        delta_match = re.search(r"Delta[:\s]+([+-]?\d+)", full_output, re.IGNORECASE)
        if delta_match:
            scores["delta"] = int(delta_match.group(1))

    return scores


def build_prompt(technique: str, pr: str, pr_desc: str, run_id: str, log_file: Path) -> str:
    """Build the agent prompt based on technique."""

    rubric = """
## Scoring Rubric (Canonical Pattern Compliance)

Score your fix against these dimensions (NOT against existing buggy code):

| Dimension | Weight | What to Look For |
|-----------|--------|------------------|
| Naming | 15% | snake_case functions, PascalCase exceptions, FastAPI patterns |
| Error Handling | 20% | TypedDict exceptions, fail-closed validation, no bare except |
| Type Safety | 20% | TypedDict for data shapes, no Any, math.isfinite checks |
| Architecture | 20% | Single responsibility, composable helpers, domain/presentation separation |
| Test Coverage | 15% | Edge cases, error paths, parametrized tests |
| Documentation | 10% | Docstrings with Args/Returns/Raises |

## Report Format

After implementing the fix, report:
1. Baseline score (before fix): X/100
2. Your score (after fix): X/100
3. Delta: +/-X

Save scores as JSON:
```json
{
  "naming": X/15,
  "error_handling": X/20,
  "type_safety": X/20,
  "architecture": X/20,
  "test_coverage": X/15,
  "documentation": X/10,
  "total": X/100,
  "baseline": Y/100,
  "delta": Z
}
```
"""

    prompts = {
        "extendedthinking": f"""
## Task: Fix issue {pr} using Extended Thinking technique

### Bug Description
{pr_desc}

### Extended Thinking Technique
Before writing any code, think step-by-step about:
1. What is the root cause?
2. What are the edge cases?
3. What canonical pattern (FastAPI, Requests, TanStack) applies here?
4. What is the best approach?
5. How will the fix be structured?

Write your reasoning in a "## Thinking" section, then implement the fix.

{rubric}
""",
        "selfrefine": f"""
## Task: Fix issue {pr} using Self-Refine technique

### Bug Description
{pr_desc}

### Self-Refine Technique
1. Generate an initial fix
2. Self-critique: What are the weaknesses?
3. Revise to address weaknesses
4. Repeat for 3 iterations max

For each iteration, note what you changed and why.

{rubric}
""",
        "swebench": f"""
## Task: Fix issue {pr} using SWE-bench Harness (test-first) technique

### Bug Description
{pr_desc}

### SWE-bench Harness Technique
1. Write failing tests FIRST (before fixing)
2. Run tests to confirm they fail
3. Implement the fix
4. Run tests to confirm they pass

Generate tests that cover:
- Happy path
- Edge cases (empty, None, invalid types)
- Error conditions

{rubric}
""",
        "metaharness": f"""
## Task: Fix issue {pr} using Meta-Harness technique

### Bug Description
{pr_desc}

### Meta-Harness Technique
Optimize the HARNESS around the LLM, not just the code:
1. Selective context: What data shapes does this function need?
2. Explicit typing guidance: "Use TypedDict for all data shapes"
3. Error handling guidance: "Use typed exceptions, not bare except"
4. Tool selection: Which validation functions to use?

Apply these harness optimizations to your fix.

{rubric}
""",
        "prm": f"""
## Task: Fix issue {pr} using Process Reward Model (PRM) technique

### Bug Description
{pr_desc}

### PRM Technique
Break the fix into steps. For each step:
1. Describe the step
2. Score it 1-10 (quality)
3. If score < 7, revise before moving on

Steps to consider:
- Root cause identification
- Guard clause addition
- TypedDict adoption
- Error propagation
- Test coverage

Final score = weighted sum of step scores.

{rubric}
""",
        "combined": f"""
## Task: Fix issue {pr} using Combined Technique

### Bug Description
{pr_desc}

### Combined Technique (SWE-bench + Meta-Harness + ExtendedThinking)
Apply in sequence:
1. SWE-bench: Write failing tests first
2. Meta-Harness: Optimize context + typing + error handling guidance
3. ExtendedThinking: Reason through the architecture before writing code
4. Verify all tests pass

{rubric}
""",
    }

    return prompts.get(technique, prompts["extendedthinking"])


def generate_cycle_file(technique: str, results: list, session_id: str) -> Path:
    """Generate the cycle_*.md file from run results."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Calculate averages
    deltas = [r["scores"].get("delta", 0) for r in results if r["scores"].get("delta")]
    avg_delta = sum(deltas) / len(deltas) if deltas else 0

    sizes = {"WA-001": "small", "WA-004": "medium", "WA-005": "complex"}
    size_deltas = {}
    for r in results:
        pr = r["pr"]
        size = sizes.get(pr, "unknown")
        size_deltas[size] = r["scores"].get("delta", 0)

    # Build markdown
    md = f"""---
title: "{technique.title()} Technique — Auto-Research v3"
type: synthesis
tags: [auto-research, {technique}, extended-thinking, self-refine, swebench, prm]
last_updated: {timestamp}
run_session: {session_id}
---

# {technique.title()} Technique — Auto-Research v3

## Technique
{technique.upper()}

## Run Session
{session_id}

## PRs Tested

| PR | Type | Baseline Score | {technique.title()} Score | Delta |
|----|------|----------------|---------------------------|-------|
"""

    for r in results:
        pr = r["pr"]
        size = sizes.get(pr, "unknown")
        baseline = r["scores"].get("baseline", "TBD")
        score = r["scores"].get("total", "TBD")
        delta = r["scores"].get("delta", "TBD")
        md += f"| {pr} ({size}) | {baseline} | {score} | +{delta} |\n"

    md += f"""
## Detailed Results

### PR Scores

| Dimension | WA-001 (small) | WA-004 (medium) | WA-005 (complex) |
|-----------|----------------|-----------------|------------------|
| Naming | {results[0]['scores'].get('naming', 'TBD')}/15 | {results[1]['scores'].get('naming', 'TBD')}/15 | {results[2]['scores'].get('naming', 'TBD')}/15 |
| Error Handling | {results[0]['scores'].get('error_handling', 'TBD')}/20 | {results[1]['scores'].get('error_handling', 'TBD')}/20 | {results[2]['scores'].get('error_handling', 'TBD')}/20 |
| Type Safety | {results[0]['scores'].get('type_safety', 'TBD')}/20 | {results[1]['scores'].get('type_safety', 'TBD')}/20 | {results[2]['scores'].get('type_safety', 'TBD')}/20 |
| Architecture | {results[0]['scores'].get('architecture', 'TBD')}/20 | {results[1]['scores'].get('architecture', 'TBD')}/20 | {results[2]['scores'].get('architecture', 'TBD')}/20 |
| Test Coverage | {results[0]['scores'].get('test_coverage', 'TBD')}/15 | {results[1]['scores'].get('test_coverage', 'TBD')}/15 | {results[2]['scores'].get('test_coverage', 'TBD')}/15 |
| Documentation | {results[0]['scores'].get('documentation', 'TBD')}/10 | {results[1]['scores'].get('documentation', 'TBD')}/10 | {results[2]['scores'].get('documentation', 'TBD')}/10 |
| **Total** | **{results[0]['scores'].get('total', 'TBD')}/100** | **{results[1]['scores'].get('total', 'TBD')}/100** | **{results[2]['scores'].get('total', 'TBD')}/100** |

## Summary Table

| PR | Size | Delta |
|----|------|-------|
| WA-001 | small | +{size_deltas.get('small', 'TBD')} |
| WA-004 | medium | +{size_deltas.get('medium', 'TBD')} |
| WA-005 | complex | +{size_deltas.get('complex', 'TBD')} |
| **Average** | - | **+{avg_delta:.0f}** |

## Key Findings

(To be filled after manual review of results)

## Run Evidence

- Log files: `wiki/syntheses/et_logs/{technique}_*.log`
- Score files: `research-wiki/scores/{technique}_*.json`
- Session: {session_id}
"""

    cycle_file = SYNTHESES_DIR / f"cycle_{technique}_v3.md"
    with open(cycle_file, "w") as f:
        f.write(md)

    return cycle_file


def main():
    parser = argparse.ArgumentParser(description="Auto-Research v3 Execution Runner")
    parser.add_argument(
        "--technique",
        choices=TECHNIQUES + ["all"],
        default="all",
        help="Technique to run (or 'all')",
    )
    parser.add_argument(
        "--prs",
        default="all",
        help="PRs to test (comma-separated or 'all')",
    )
    parser.add_argument(
        "--session",
        help="Session ID (auto-generated if not provided)",
    )
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Run techniques in parallel (background)",
    )

    args = parser.parse_args()

    session_id = args.session or str(uuid.uuid4())[:8]
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    print(f"=== Auto-Research v3 Runner ===")
    print(f"Session: {session_id}")
    print(f"Timestamp: {timestamp}")
    print(f"Technique: {args.technique}")
    print(f"PRs: {args.prs}")
    print(f"Parallel: {args.parallel}")
    print()

    # Determine which techniques and PRs to run
    techniques = TECHNIQUES if args.technique == "all" else [args.technique]
    prs = PR_LIST if args.prs == "all" else args.prs.split(",")

    all_results = []

    for technique in techniques:
        print(f"\n{'='*60}")
        print(f"Running {technique} on {prs}...")
        print(f"{'='*60}")

        technique_results = []
        for pr in prs:
            print(f"\n  → {pr}...")
            result = run_technique(technique, pr, session_id)
            technique_results.append(result)
            all_results.append(result)

            # Report immediate result
            if result["status"] == "completed":
                delta = result["scores"].get("delta", "TBD")
                total = result["scores"].get("total", "TBD")
                print(f"    Status: COMPLETED | Score: {total}/100 | Delta: +{delta}")
            else:
                print(f"    Status: {result['status']} | Error: {result.get('error', 'N/A')}")

        # Generate cycle file for this technique
        if technique_results:
            cycle_file = generate_cycle_file(technique, technique_results, session_id)
            print(f"\n  Cycle file written: {cycle_file}")

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for r in all_results:
        if r["status"] == "completed":
            print(f"  {r['technique']}/{r['pr']}: +{r['scores'].get('delta', '?')} delta, {r['scores'].get('total', '?')}/100")
        else:
            print(f"  {r['technique']}/{r['pr']}: {r['status']} - {r.get('error', '')}")

    # Save aggregate scores
    scores_file = SCORES_DIR / f"aggregate_{session_id}.json"
    with open(scores_file, "w") as f:
        json.dump(
            {
                "session_id": session_id,
                "timestamp": timestamp,
                "results": all_results,
                "techniques_run": techniques,
                "prs_tested": prs,
            },
            f,
            indent=2,
        )
    print(f"\nAggregate scores: {scores_file}")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Auto-Research v3 — Loop Controller

Runs the auto-research experiment in a 12-hour loop with:
- Parallel technique execution
- Cross-agent verification
- Progress tracking via beads
- Evidence collection per /evidence-standards

Usage:
    python3 research-wiki/loop_controller.py --hours 12
    python3 research-wiki/loop_controller.py --hours 12 --techniques extendedthinking,metaharness
"""

import argparse
import json
import os
import subprocess
import sys
import time
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
ET_LOGS_DIR = REPO_ROOT / "wiki" / "syntheses" / "et_logs"
SCORES_DIR = REPO_ROOT / "research-wiki" / "scores"
SYNTHESES_DIR = REPO_ROOT / "wiki" / "syntheses"
WORKTREE = Path.home() / ".worktrees" / "jleechanorg" / "worldarchitect.ai"

TECHNIQUES = ["extendedthinking", "selfrefine", "swebench", "metaharness", "prm", "combined"]
PR_LIST = ["WA-001", "WA-004", "WA-005"]

# Ensure dirs exist
ET_LOGS_DIR.mkdir(parents=True, exist_ok=True)
SCORES_DIR.mkdir(parents=True, exist_ok=True)


def capture_provenance():
    """Capture git + runtime provenance for evidence bundle."""
    provenance = {}

    # Git provenance
    try:
        subprocess.run(["git", "fetch", "origin", "main"], capture_output=True, timeout=10)
        provenance["git_head"] = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True
        ).strip()
        provenance["git_branch"] = subprocess.check_output(
            ["git", "branch", "--show-current"], text=True
        ).strip()
        provenance["merge_base"] = subprocess.check_output(
            ["git", "merge-base", "HEAD", "origin/main"], text=True
        ).strip()
        provenance["commits_ahead_of_main"] = int(subprocess.check_output(
            ["git", "rev-list", "--count", "origin/main..HEAD"], text=True
        ).strip())
        provenance["diff_stat"] = subprocess.check_output(
            ["git", "diff", "--stat", "origin/main...HEAD"], text=True
        ).strip()
    except Exception as e:
        provenance["git_error"] = str(e)

    # Session info
    provenance["session_start"] = datetime.now(timezone.utc).isoformat()
    provenance["hostname"] = os.environ.get("HOSTNAME", "unknown")

    return provenance


def run_technique_agent(technique: str, pr: str, session_id: str) -> dict:
    """Run a single technique on a single PR using minimax via claudem."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = f"{technique}_{pr}_{timestamp}"
    log_file = ET_LOGS_DIR / f"{run_id}.log"
    score_file = SCORES_DIR / f"{run_id}.json"

    result = {
        "run_id": run_id,
        "technique": technique,
        "pr": pr,
        "timestamp": timestamp,
        "session_id": session_id,
        "status": "pending",
        "scores": {},
        "log_file": str(log_file),
        "score_file": str(score_file),
        "evidence": {},
    }

    # PR info
    pr_info = {
        "WA-001": {"issue": "#6205", "desc": "_synthesize_generic_rewards_box returns None causing RuntimeError"},
        "WA-004": {"issue": "#6261", "desc": "20ms hard-coded ceiling fails under CI load"},
        "WA-005": {"issue": "#6214", "desc": "level_up_complete=True but rewards_box missing, ASI injection needed"},
    }

    with open(log_file, "w") as f:
        f.write(f"=== Auto-Research v3 Run ===\n")
        f.write(f"Technique: {technique}\n")
        f.write(f"PR: {pr}\n")
        f.write(f"Run ID: {run_id}\n")
        f.write(f"Session: {session_id}\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Provenance: {json.dumps(capture_provenance(), indent=2)}\n")
        f.write(f"{'='*60}\n\n")

    # Build prompt based on technique
    rubric = """
## Scoring Rubric

After implementing the fix, score each dimension:

| Dimension | Max | What to Score |
|-----------|-----|---------------|
| Naming | 15 | snake_case, FastAPI patterns |
| Error Handling | 20 | TypedDict exceptions, fail-closed |
| Type Safety | 20 | TypedDict for data shapes, no Any |
| Architecture | 20 | Single responsibility, composable |
| Test Coverage | 15 | Edge cases, error paths |
| Documentation | 10 | Docstrings with Args/Returns |

Report as JSON:
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

IMPORTANT: Save scores to /tmp/scores_{technique}_{pr}.json before finishing.
"""

    prompts = {
        "extendedthinking": f"""
## Task: Fix issue {pr_info[pr]['issue']} using Extended Thinking

### Bug
{pr_info[pr]['desc']}

### Technique: ExtendedThinking
Before writing code, think step-by-step about root cause, edge cases, canonical patterns, architecture.
Write reasoning in a "## Thinking" section, then implement.

{rubric}
""",
        "selfrefine": f"""
## Task: Fix issue {pr_info[pr]['issue']} using Self-Refine

### Bug
{pr_info[pr]['desc']}

### Technique: Self-Refine
1. Generate initial fix
2. Self-critique weaknesses
3. Revise to address weaknesses
4. Repeat for 3 iterations max

{rubric}
""",
        "swebench": f"""
## Task: Fix issue {pr_info[pr]['issue']} using SWE-bench Harness (test-first)

### Bug
{pr_info[pr]['desc']}

### Technique: SWE-bench
1. Write failing tests FIRST
2. Run tests to confirm failure
3. Implement fix
4. Run tests to confirm pass

{rubric}
""",
        "metaharness": f"""
## Task: Fix issue {pr_info[pr]['issue']} using Meta-Harness

### Bug
{pr_info[pr]['desc']}

### Technique: Meta-Harness
Optimize the harness: selective context, explicit typing guidance (TypedDict), error handling patterns, tool selection.

{rubric}
""",
        "prm": f"""
## Task: Fix issue {pr_info[pr]['issue']} using PRM

### Bug
{pr_info[pr]['desc']}

### Technique: PRM (Process Reward Model)
Break fix into steps. Score each step 1-10. If score < 7, revise before moving on.

{rubric}
""",
        "combined": f"""
## Task: Fix issue {pr_info[pr]['issue']} using Combined (SWE-bench + Meta-Harness + ExtendedThinking)

### Bug
{pr_info[pr]['desc']}

### Technique: Combined
Apply in sequence: SWE-bench (test-first) → Meta-Harness (context+typing) → ExtendedThinking (reasoning) → verify

{rubric}
""",
    }

    prompt = prompts.get(technique, prompts["extendedthinking"])

    with open(log_file, "a") as f:
        f.write(f"\n=== Agent Prompt ===\n{prompt}\n")

    # Run via minimax if available
    agent_cmd = prompt.replace('"', '\\"')

    cmd = [
        "bash", "-c",
        f"source ~/.bashrc 2>/dev/null; claudem '{agent_cmd}' 2>&1 | tee -a {log_file}"
    ]

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=str(REPO_ROOT),
        )

        output = proc.communicate(timeout=600)  # 10 min timeout per PR

        with open(log_file, "a") as f:
            f.write(f"\n=== Agent Output ===\n")
            f.write(output[0])

        # Parse scores from output
        scores = parse_scores(output[0], technique, pr)
        result["scores"] = scores
        result["status"] = "completed" if scores.get("total") else "no_scores"

    except subprocess.TimeoutExpired:
        result["status"] = "timeout"
        with open(log_file, "a") as f:
            f.write("\n=== TIMEOUT after 10 minutes ===\n")
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        with open(log_file, "a") as f:
            f.write(f"\n=== ERROR: {e} ===\n")

    # Save score file
    with open(score_file, "w") as f:
        json.dump(result, f, indent=2)

    return result


def parse_scores(output: str, technique: str, pr: str) -> dict:
    """Parse scores from agent output."""
    scores = {}
    import re

    # Look for JSON score object
    json_match = re.search(
        r'\{[^{}]*(?:naming|error_handling|type_safety|architecture|test_coverage|documentation|total|baseline|delta)[^{}]*\}',
        output,
        re.DOTALL,
    )
    if json_match:
        try:
            scores = json.loads(json_match.group(0))
            return scores
        except json.JSONDecodeError:
            pass

    # Look for patterns
    total_match = re.search(r'"total"\s*:\s*(\d+)', output)
    baseline_match = re.search(r'"baseline"\s*:\s*(\d+)', output)
    delta_match = re.search(r'"delta"\s*:\s*([+-]?\d+)', output)

    if total_match:
        scores["total"] = int(total_match.group(1))
    if baseline_match:
        scores["baseline"] = int(baseline_match.group(1))
    if delta_match:
        scores["delta"] = int(delta_match.group(1))

    return scores


def verify_results(technique: str, session_id: str) -> dict:
    """Verify results for a technique have all required evidence."""
    issues = []
    warnings = []

    # Check cycle file exists
    cycle_file = SYNTHESES_DIR / f"cycle_{technique}_v3.md"
    if not cycle_file.exists():
        issues.append(f"Missing cycle file: {cycle_file}")

    # Check log files exist
    log_files = list(ET_LOGS_DIR.glob(f"{technique}_*.log"))
    if not log_files:
        issues.append(f"No log files for {technique}")

    # Check score files exist
    score_files = list(SCORES_DIR.glob(f"{technique}_*.json"))
    if not score_files:
        issues.append(f"No score files for {technique}")

    # Check for suspicious patterns
    if cycle_file.exists():
        content = cycle_file.read_text()
        import re
        suspicious = re.findall(r"Delta[:\s]+([+-]?\d{3,})", content)
        if suspicious:
            issues.append(f"Suspicious delta values: {suspicious}")

    return {
        "technique": technique,
        "issues": issues,
        "warnings": warnings,
        "log_count": len(log_files),
        "score_count": len(score_files),
        "cycle_exists": cycle_file.exists(),
    }


def update_bead(bead_id: str, status: str, notes: str = ""):
    """Update bead status."""
    try:
        subprocess.run(
            ["br", "update", bead_id, "--status", status],
            capture_output=True,
            timeout=10,
        )
        if notes:
            subprocess.run(
                ["br", "update", bead_id, "--notes", notes],
                capture_output=True,
                timeout=10,
            )
    except Exception as e:
        print(f"Warning: Could not update bead {bead_id}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Auto-Research v3 Loop Controller")
    parser.add_argument("--hours", type=float, default=12, help="Hours to run (default: 12)")
    parser.add_argument("--techniques", help="Comma-separated techniques (default: all)")
    parser.add_argument("--session", help="Session ID (auto-generated if not provided)")
    parser.add_argument("--checkpoint-interval", type=int, default=30, help="Minutes between checkpoints")

    args = parser.parse_args()

    session_id = args.session or str(uuid.uuid4())[:8]
    end_time = datetime.now(timezone.utc) + timedelta(hours=args.hours)

    techniques = args.techniques.split(",") if args.techniques else TECHNIQUES

    print(f"=== Auto-Research v3 Loop Controller ===")
    print(f"Session: {session_id}")
    print(f"Start: {datetime.now(timezone.utc).isoformat()}")
    print(f"End: {end_time.isoformat()}")
    print(f"Techniques: {techniques}")
    print(f"PRs: {PR_LIST}")
    print(f"Checkpoint interval: {args.checkpoint_interval} min")
    print()

    # Capture start provenance
    start_provenance = capture_provenance()
    print(f"Start provenance: {start_provenance['git_head'][:8]} on {start_provenance['git_branch']}")

    # Update milestone bead
    update_bead("br-rt7", "in_progress", f"Session {session_id} started at {datetime.now(timezone.utc).isoformat()}")

    all_results = {}
    checkpoint_count = 0

    while datetime.now(timezone.utc) < end_time:
        print(f"\n--- Loop iteration (checkpoint {checkpoint_count}) ---")

        # Run each technique in sequence (can parallelize via background later)
        for technique in techniques:
            elapsed = datetime.now(timezone.utc) - (end_time - timedelta(hours=args.hours))
            remaining = (end_time - datetime.now(timezone.utc)).total_seconds() / 3600

            if remaining < 0.5:
                print(f"  ⚠️ Less than 30 min remaining, stopping {technique}")
                continue

            print(f"\n  → {technique}...")

            # Update task bead
            task_beads = {
                "extendedthinking": "br-rt7.1",
                "selfrefine": "br-rt7.2",
                "swebench": "br-rt7.3",
                "metaharness": "br-rt7.4",
                "prm": "br-rt7.5",
                "combined": "br-rt7.6",
            }
            update_bead(task_beads.get(technique, ""), "in_progress", f"Running {technique}...")

            technique_results = []
            for pr in PR_LIST:
                print(f"     └─ {pr}...")
                result = run_technique_agent(technique, pr, session_id)
                technique_results.append(result)

                delta = result["scores"].get("delta", "?")
                total = result["scores"].get("total", "?")
                print(f"        → {result['status']} | Score: {total}/100 | Delta: +{delta}")

            all_results[technique] = technique_results

            # Generate cycle file
            generate_cycle_file(technique, technique_results, session_id)

            # Verify immediately
            verification = verify_results(technique, session_id)
            if verification["issues"]:
                print(f"     ⚠️ Verification issues: {verification['issues']}")
                update_bead(task_beads.get(technique, ""), "blocked", f"Issues: {verification['issues']}")
            else:
                print(f"     ✅ Verification passed")
                update_bead(task_beads.get(technique, ""), "completed", f"+{technique} complete")

        # Checkpoint
        checkpoint_count += 1
        elapsed_mins = (datetime.now(timezone.utc) - start_provenance.get("session_start", datetime.now(timezone.utc))).total_seconds() / 60

        print(f"\n=== Checkpoint {checkpoint_count} | Elapsed: {elapsed_mins:.0f} min ===")

        for technique, results in all_results.items():
            completed = sum(1 for r in results if r["status"] == "completed")
            total = len(results)
            print(f"  {technique}: {completed}/{total} completed")

        # Save checkpoint
        checkpoint_file = SCORES_DIR / f"checkpoint_{checkpoint_count}_{session_id}.json"
        with open(checkpoint_file, "w") as f:
            json.dump({
                "checkpoint": checkpoint_count,
                "session_id": session_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "elapsed_mins": elapsed_mins,
                "results": all_results,
            }, f, indent=2, default=str)
        print(f"  Checkpoint saved: {checkpoint_file}")

        # Sleep until next checkpoint or end time
        sleep_secs = args.checkpoint_interval * 60
        if datetime.now(timezone.utc) + timedelta(seconds=sleep_secs) > end_time:
            sleep_secs = (end_time - datetime.now(timezone.utc)).total_seconds()
            if sleep_secs <= 0:
                break

        print(f"  Sleeping {sleep_secs/60:.0f} min until next checkpoint...")
        time.sleep(sleep_secs)

    # Final verification
    print("\n=== Final Verification ===")
    verifier_bead = "br-rt7.7"
    update_bead(verifier_bead, "in_progress", "Running cross-verification...")

    all_verifications = {}
    for technique in techniques:
        v = verify_results(technique, session_id)
        all_verifications[technique] = v
        status_icon = "✅" if not v["issues"] else "❌"
        print(f"  {status_icon} {technique}: {v['issues'] or 'OK'}")

    # Update verifier bead
    failed = sum(1 for v in all_verifications.values() if v["issues"])
    if failed == 0:
        update_bead(verifier_bead, "completed", "All techniques verified")
    else:
        update_bead(verifier_bead, "blocked", f"{failed} techniques have verification issues")

    # Summary
    print("\n=== FINAL SUMMARY ===")
    for technique, results in all_results.items():
        for r in results:
            delta = r["scores"].get("delta", "?")
            total = r["scores"].get("total", "?")
            print(f"  {r['technique']}/{r['pr']}: +{delta} delta, {total}/100")

    # Save final aggregate
    final_file = SCORES_DIR / f"final_{session_id}.json"
    with open(final_file, "w") as f:
        json.dump({
            "session_id": session_id,
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "start_provenance": start_provenance,
            "results": all_results,
            "verifications": all_verifications,
        }, f, indent=2, default=str)

    print(f"\nFinal results: {final_file}")

    # Update milestone bead
    update_bead("br-rt7", "completed", f"Session {session_id} complete. {checkpoint_count} checkpoints.")


def generate_cycle_file(technique: str, results: list, session_id: str):
    """Generate cycle_*.md from run results."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    pr_info = {
        "WA-001": "small",
        "WA-004": "medium",
        "WA-005": "complex",
    }

    # Build markdown
    md = f"""---
title: "{technique.title()} Technique — Auto-Research v3"
type: synthesis
tags: [auto-research, {technique}, evidence-required]
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
        size = pr_info.get(pr, "unknown")
        baseline = r["scores"].get("baseline", "TBD")
        score = r["scores"].get("total", "TBD")
        delta = r["scores"].get("delta", "TBD")
        md += f"| {pr} ({size}) | {baseline} | {score} | +{delta} |\n"

    md += """
## Key Findings

(To be filled after manual review)

## Run Evidence
Log files and score files in research-wiki/ directory.
"""

    cycle_file = SYNTHESES_DIR / f"cycle_{technique}_v3.md"
    with open(cycle_file, "w") as f:
        f.write(md)

    print(f"     Cycle file: {cycle_file}")


if __name__ == "__main__":
    main()
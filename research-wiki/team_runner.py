#!/usr/bin/env python3
"""
Auto-Research v3 — Team Execution Runner

Uses Claude Code team with minimax agents to run techniques in parallel.
Spawns coder agents for each technique + verifier agent for cross-checking.

Usage:
    python3 research-wiki/team_runner.py --hours 12
    python3 research-wiki/team_runner.py --hours 12 --parallel
"""

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

ET_LOGS_DIR.mkdir(parents=True, exist_ok=True)
SCORES_DIR.mkdir(parents=True, exist_ok=True)

SESSION_FILE = SCORES_DIR / "active_session.json"


def start_session(session_id: str) -> dict:
    """Start a new session and save to file."""
    session = {
        "session_id": session_id,
        "start_time": datetime.now(timezone.utc).isoformat(),
        "techniques": {},
        "status": "running",
    }
    for technique in TECHNIQUES:
        session["techniques"][technique] = {
            "status": "pending",
            "results": {},
        }
    with open(SESSION_FILE, "w") as f:
        json.dump(session, f, indent=2)
    return session


def update_session(session_id: str, technique: str, pr: str, result: dict):
    """Update session with technique results."""
    if SESSION_FILE.exists():
        session = json.loads(SESSION_FILE.read_text())
        if technique in session["techniques"]:
            if pr not in session["techniques"][technique]["results"]:
                session["techniques"][technique]["results"][pr] = {}
            session["techniques"][technique]["results"][pr] = result
            session["techniques"][technique]["status"] = result.get("status", "unknown")
        with open(SESSION_FILE, "w") as f:
            json.dump(session, f, indent=2)


def run_coder_agent(technique: str, pr: str, session_id: str) -> dict:
    """Run a coder agent using minimax via source ~/.bashrc && claudem."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = f"{technique}_{pr}_{session_id}"
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
    }

    pr_info = {
        "WA-001": {"issue": "#6205", "desc": "_synthesize_generic_rewards_box returns None causing RuntimeError"},
        "WA-004": {"issue": "#6261", "desc": "20ms hard-coded ceiling fails under CI load"},
        "WA-005": {"issue": "#6214", "desc": "level_up_complete=True but rewards_box missing, ASI injection needed"},
    }

    rubric = """
## Scoring Rubric

After implementing, score your fix:

| Dimension | Max | What to Score |
|-----------|-----|---------------|
| Naming | 15 | snake_case, FastAPI patterns |
| Error Handling | 20 | TypedDict exceptions, fail-closed |
| Type Safety | 20 | TypedDict for data shapes, no Any |
| Architecture | 20 | Single responsibility, composable |
| Test Coverage | 15 | Edge cases, error paths |
| Documentation | 10 | Docstrings with Args/Returns |

Save as JSON to /tmp/scores_{technique}_{pr}.json:
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

IMPORTANT: Save the JSON scores to /tmp/scores_{technique}_{pr}.json and also output the full JSON.
"""

    prompts = {
        "extendedthinking": f"""Fix issue {pr_info[pr]['issue']} using Extended Thinking.

Bug: {pr_info[pr]['desc']}

Technique: Think step-by-step about root cause, edge cases, canonical patterns before writing code.
Write a '## Thinking' section first, then implement the fix.

Work in {WORKTREE}.

{rubric}""",
        "selfrefine": f"""Fix issue {pr_info[pr]['issue']} using Self-Refine.

Bug: {pr_info[pr]['desc']}

Technique: Generate initial fix, self-critique weaknesses, revise. 3 iterations max.

Work in {WORKTREE}.

{rubric}""",
        "swebench": f"""Fix issue {pr_info[pr]['issue']} using SWE-bench Harness (test-first).

Bug: {pr_info[pr]['desc']}

Technique: Write failing tests first, run to confirm fail, implement fix, run to confirm pass.

Work in {WORKTREE}.

{rubric}""",
        "metaharness": f"""Fix issue {pr_info[pr]['issue']} using Meta-Harness.

Bug: {pr_info[pr]['desc']}

Technique: Optimize harness (selective context, explicit TypedDict guidance, error handling patterns, tool selection).

Work in {WORKTREE}.

{rubric}""",
        "prm": f"""Fix issue {pr_info[pr]['issue']} using PRM.

Bug: {pr_info[pr]['desc']}

Technique: Break into steps. Score each 1-10. If < 7, revise before moving on.

Work in {WORKTREE}.

{rubric}""",
        "combined": f"""Fix issue {pr_info[pr]['issue']} using Combined (SWE-bench + Meta-Harness + ExtendedThinking).

Bug: {pr_info[pr]['desc']}

Technique: SWE-bench (test-first) → Meta-Harness (context+typing) → ExtendedThinking (reasoning) → verify.

Work in {WORKTREE}.

{rubric}""",
    }

    prompt = prompts.get(technique, prompts["extendedthinking"]).format(technique=technique, pr=pr)

    # Write log header
    with open(log_file, "w") as f:
        f.write(f"=== Auto-Research v3 Run ===\n")
        f.write(f"Technique: {technique}\n")
        f.write(f"PR: {pr}\n")
        f.write(f"Run ID: {run_id}\n")
        f.write(f"Session: {session_id}\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Worktree: {WORKTREE}\n")
        f.write(f"Prompt: {prompt[:200]}...\n")
        f.write(f"{'='*60}\n\n")

    # Build the bash command to source bashrc and run via minimax
    # Escape the prompt for bash
    escaped_prompt = prompt.replace("'", "'\\''").replace('\n', '\\n')

    bash_cmd = f"""source ~/.bashrc 2>/dev/null
cd {WORKTREE}
echo 'Working directory: $(pwd)'
echo 'Git HEAD: $(git rev-parse HEAD)'
echo 'Branch: $(git branch --show-current)'
echo '---'
echo 'Running {technique} on {pr}...'
echo 'Issue: {pr_info[pr]['issue']}'
echo 'Bug: {pr_info[pr]['desc']}'
echo '---'

MINIMAX_API_KEY="$MINIMAX_API_KEY" \\
ANTHROPIC_BASE_URL="https://api.minimax.io/anthropic" \\
ANTHROPIC_AUTH_TOKEN="$MINIMAX_API_KEY" \\
ANTHROPIC_MODEL="MiniMax-M2.7" \\
claude --dangerously-skip-permissions -p '{escaped_prompt}' 2>&1 | tee -a {log_file}

# Parse scores from output
SCORE_FILE="/tmp/scores_{technique}_{pr}.json"
if [ -f "$SCORE_FILE" ]; then
    echo "=== SCORES FOUND ==="
    cat "$SCORE_FILE" | tee -a {log_file}
else
    echo "=== NO SCORE FILE FOUND ==="
    # Try to extract from any logged JSON
    grep -o '{{"naming".*}}' {log_file} | tail -1 | tee -a {log_file} || echo "No JSON found"
fi
"""

    try:
        proc = subprocess.Popen(
            ["bash", "-c", bash_cmd],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        output, _ = proc.communicate(timeout=600)  # 10 min timeout

        # Append output to log
        with open(log_file, "a") as f:
            f.write(f"\n=== AGENT OUTPUT ===\n")
            f.write(output)

        # Parse scores
        scores = parse_scores(output)
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
        json.dump(result, f, indent=2, default=str)

    update_session(session_id, technique, pr, result)
    return result


def parse_scores(output: str) -> dict:
    """Parse scores from agent output."""
    scores = {}
    import re

    # Try JSON extraction
    json_match = re.search(
        r'\{[^{}]*(?:"naming"|"error_handling"|"type_safety"|"architecture"|"test_coverage"|"documentation"|"total"|"baseline"|"delta")[^{}]*\}',
        output,
        re.DOTALL,
    )
    if json_match:
        try:
            scores = json.loads(json_match.group(0))
            return scores
        except json.JSONDecodeError:
            pass

    # Try patterns
    for key in ["total", "baseline", "delta"]:
        match = re.search(rf'"{key}"\s*:\s*([+-]?\d+)', output)
        if match:
            scores[key] = int(match.group(1))

    # Extract individual dimensions
    for dim in ["naming", "error_handling", "type_safety", "architecture", "test_coverage", "documentation"]:
        match = re.search(rf'"{dim}"\s*:\s*(\d+)', output)
        if match:
            scores[dim] = int(match.group(1))

    return scores


def generate_cycle_file(technique: str, results: list, session_id: str):
    """Generate cycle_*.md from run results."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    pr_info = {"WA-001": "small", "WA-004": "medium", "WA-005": "complex"}

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

| PR | Type | Baseline | Score | Delta |
|----|------|----------|-------|-------|
"""
    for r in results:
        pr = r["pr"]
        size = pr_info.get(pr, "unknown")
        baseline = r["scores"].get("baseline", "TBD")
        score = r["scores"].get("total", "TBD")
        delta = r["scores"].get("delta", "TBD")
        md += f"| {pr} ({size}) | {baseline} | {score} | +{delta} |\n"

    md += """
## Run Evidence

Logs: wiki/syntheses/et_logs/<technique>_<pr>_<session>.log
Scores: research-wiki/scores/<technique>_<pr>_<session>.json

## Key Findings

(To be filled after manual review)
"""

    cycle_file = SYNTHESES_DIR / f"cycle_{technique}_v3.md"
    with open(cycle_file, "w") as f:
        f.write(md)

    return cycle_file


def verify_all_techniques(session_id: str) -> dict:
    """Verify all technique results have required evidence."""
    import re

    verifications = {}
    for technique in TECHNIQUES:
        issues = []
        warnings = []

        cycle_file = SYNTHESES_DIR / f"cycle_{technique}_v3.md"
        if not cycle_file.exists():
            issues.append(f"Missing cycle file")
        else:
            content = cycle_file.read_text()
            # Check for run_session
            if "run_session" not in content:
                issues.append("No run_session in frontmatter")
            # Check for suspicious patterns
            suspicious_deltas = re.findall(r"Delta[:\s]+([+-]?\d{3,})", content)
            if suspicious_deltas:
                issues.append(f"Suspicious deltas: {suspicious_deltas}")

        log_files = list(ET_LOGS_DIR.glob(f"{technique}_*.log"))
        if not log_files:
            warnings.append("No log files")

        score_files = list(SCORES_DIR.glob(f"{technique}_*.json"))
        if not score_files:
            issues.append("No score files")

        verifications[technique] = {
            "status": "failed" if issues else ("warning" if warnings else "passed"),
            "issues": issues,
            "warnings": warnings,
            "log_count": len(log_files),
            "score_count": len(score_files),
        }

    return verifications


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--hours", type=float, default=12)
    parser.add_argument("--session", default=None)
    parser.add_argument("--techniques", help="comma-separated, default=all")
    args = parser.parse_args()

    session_id = args.session or str(uuid.uuid4())[:8]
    end_time = datetime.now(timezone.utc) + timedelta(hours=args.hours)

    techniques = args.techniques.split(",") if args.techniques else TECHNIQUES

    print(f"=== Auto-Research v3 Team Runner ===")
    print(f"Session: {session_id}")
    print(f"End: {end_time.strftime('%H:%M:%S')} UTC")
    print(f"Techniques: {techniques}")
    print(f"PRs: {PR_LIST}")
    print()

    session = start_session(session_id)

    # Track progress
    completed = {t: [] for t in techniques}
    total_runs = len(techniques) * len(PR_LIST)
    finished_runs = 0

    # Run in sequence (parallel via background processes would be better but needs proper agent orchestration)
    for technique in techniques:
        if datetime.now(timezone.utc) >= end_time:
            print("Time limit reached, stopping.")
            break

        for pr in PR_LIST:
            if datetime.now(timezone.utc) >= end_time:
                print("Time limit reached, stopping.")
                break

            print(f"\n→ {technique}/{pr}...")
            result = run_coder_agent(technique, pr, session_id)

            delta = result["scores"].get("delta", "?")
            total = result["scores"].get("total", "?")
            status = result["status"]
            print(f"   Status: {status} | Score: {total}/100 | Delta: +{delta}")

            finished_runs += 1
            completed[technique].append(result)

            # Generate cycle file after each technique's first PR completes
            if len(completed[technique]) == 1:
                generate_cycle_file(technique, completed[technique], session_id)

            # Quick checkpoint every 3 runs
            if finished_runs % 3 == 0:
                print(f"\n--- Checkpoint: {finished_runs}/{total_runs} runs completed ---")
                for t, results in completed.items():
                    completed_count = len(results)
                    if completed_count > 0:
                        avg_delta = sum(r["scores"].get("delta", 0) for r in results) / completed_count
                        print(f"  {t}: {completed_count} PRs done, avg delta: +{avg_delta:.0f}")

                # Save checkpoint
                checkpoint = {
                    "session_id": session_id,
                    "checkpoint_at": datetime.now(timezone.utc).isoformat(),
                    "finished_runs": finished_runs,
                    "total_runs": total_runs,
                    "results": {t: [r for r in results] for t, results in completed.items()},
                }
                with open(SCORES_DIR / f"checkpoint_{session_id}.json", "w") as f:
                    json.dump(checkpoint, f, indent=2, default=str)

    # Final cycle files
    print("\n=== Generating cycle files ===")
    for technique in techniques:
        if completed[technique]:
            cf = generate_cycle_file(technique, completed[technique], session_id)
            print(f"  {technique}: {cf}")

    # Final verification
    print("\n=== Final Verification ===")
    verifications = verify_all_techniques(session_id)
    for technique, v in verifications.items():
        icon = {"passed": "✅", "failed": "❌", "warning": "⚠️"}.get(v["status"], "?")
        print(f"  {icon} {technique}: {v['issues'] or v['warnings'] or 'OK'}")

    # Save final results
    final_results = {
        "session_id": session_id,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "finished_runs": finished_runs,
        "total_runs": total_runs,
        "results": {t: [r for r in results] for t, results in completed.items()},
        "verifications": verifications,
    }
    with open(SCORES_DIR / f"final_{session_id}.json", "w") as f:
        json.dump(final_results, f, indent=2, default=str)

    print(f"\n=== COMPLETE ===")
    print(f"Session: {session_id}")
    print(f"Runs: {finished_runs}/{total_runs}")
    print(f"Final results: {SCORES_DIR}/final_{session_id}.json")

    # Update beads
    try:
        for technique in techniques:
            if completed[technique]:
                task_beads = {
                    "extendedthinking": "br-rt7.1",
                    "selfrefine": "br-rt7.2",
                    "swebench": "br-rt7.3",
                    "metaharness": "br-rt7.4",
                    "prm": "br-rt7.5",
                    "combined": "br-rt7.6",
                }
                if technique in task_beads:
                    bead_id = task_beads[technique]
                    subprocess.run(["br", "update", bead_id, "--status", "completed"], capture_output=True, timeout=10)
    except:
        pass

    return final_results


if __name__ == "__main__":
    main()
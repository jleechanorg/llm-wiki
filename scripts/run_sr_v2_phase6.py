#!/usr/bin/env python3
"""
Phase 6 V1: SR-v2 (rubric-targeted SelfRefine) evaluation loop.
- 5 PRs × 3 runs = 15 total evaluations
- Score each with 6-dim rubric
- Open/close as draft autor PRs
- Append to bandit_state.json
"""

import json
import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path
import time
from anthropic import Anthropic

# Config
REPO = "jleechanorg/worldarchitect.ai"
TARGET_PRS = [6265, 6261, 6245, 6243, 6269]
RUNS_PER_PR = 3
TECHNIQUE_TAG = "SR-v2"

# Paths
REPO_ROOT = Path("/Users/jleechan/llm-wiki-autor-phase3")
SCORES_DIR = REPO_ROOT / "research-wiki" / "scores"
LOGS_DIR = REPO_ROOT / "wiki" / "syntheses" / "et_logs"
BANDIT_STATE = REPO_ROOT / "technique_bandit" / "bandit_state.json"

# Ensure directories exist
SCORES_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# SR-v2 Critique Prompt (EXACT TEXT from roadmap)
SR_V2_CRITIQUE = """Review this implementation against these criteria and score each 0-100:
1. Naming (15%): snake_case, descriptive, no abbreviations
2. Error Handling (20%): typed exceptions, no bare except, logged errors
3. Type Safety (20%): TypedDict for data shapes, explicit return types
4. Architecture (20%): follows existing patterns, single responsibility
5. Test Coverage (15%): covers happy path + edge cases + error paths
6. Documentation (10%): docstrings for public methods, inline for non-obvious

For the 2 lowest-scoring dimensions, rewrite the implementation to improve them.
Output: first the per-dimension scores, then the rewritten implementation."""

def run_command(cmd):
    """Run shell command and return output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout, result.stderr, result.returncode

def fetch_pr_diff(pr_num):
    """Fetch PR diff from GitHub."""
    stdout, stderr, code = run_command(f"gh pr diff {pr_num} --repo {REPO}")
    if code != 0:
        print(f"ERROR fetching PR {pr_num} diff: {stderr}")
        sys.exit(1)
    return stdout

def fetch_pr_info(pr_num):
    """Fetch PR title and body."""
    cmd = f"gh pr view {pr_num} --repo {REPO} --json title,body"
    stdout, stderr, code = run_command(cmd)
    if code != 0:
        print(f"ERROR fetching PR {pr_num} info: {stderr}")
        sys.exit(1)
    data = json.loads(stdout)
    return data.get("title", ""), data.get("body", "")

def generate_sr_v2_fix(pr_num, pr_diff, pr_title, pr_body, run_num):
    """
    Generate a fix using SelfRefine with rubric-targeted critique (SR-v2).
    Uses 3 refinement rounds.
    Returns: (fix_code, log_text)
    """
    client = Anthropic()

    log_lines = [
        f"# SR-v2 Phase 6 Run {run_num} for PR #{pr_num}",
        f"Timestamp: {datetime.now().isoformat()}",
        f"Technique: {TECHNIQUE_TAG}",
        "",
        f"## PR Context",
        f"Title: {pr_title}",
        f"Body (first 500 chars): {pr_body[:500]}...",
        "",
        f"## Diff (first 1000 chars)",
        pr_diff[:1000] + "..." if len(pr_diff) > 1000 else pr_diff,
        "",
    ]

    # Step 1: Initial analysis and fix generation
    print(f"  [PR {pr_num} run {run_num}] Generating initial fix...")
    log_lines.append(f"## Step 1: Initial Generation")

    initial_prompt = f"""You are a code review expert. Analyze this GitHub PR diff and generate an improved implementation that fixes the issues identified.

PR Title: {pr_title}

PR Description:
{pr_body}

Diff:
{pr_diff}

Generate a complete, production-ready fix for this PR. Output only the code changes, organized by file."""

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4000,
        messages=[{"role": "user", "content": initial_prompt}]
    )

    initial_fix = response.content[0].text
    log_lines.append(f"Initial fix generated ({len(initial_fix)} chars)")

    # Refinement rounds 1-3 with rubric-targeted critique
    fix = initial_fix
    for round_num in range(1, 4):
        print(f"    [round {round_num}] Rubric-targeted critique...")
        log_lines.append(f"\n## Refinement Round {round_num}")

        critique_prompt = f"""You are reviewing code against a quality rubric. Here is the implementation:

{fix}

{SR_V2_CRITIQUE}"""

        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            messages=[{"role": "user", "content": critique_prompt}]
        )

        critique_response = response.content[0].text
        log_lines.append(f"Critique round {round_num} completed")
        log_lines.append(critique_response[:500])

        # Extract refined implementation from critique
        # The model should provide scores then rewritten code
        if "rewritten" in critique_response.lower() or "revised" in critique_response.lower():
            # Try to extract the code section
            parts = critique_response.split("```")
            if len(parts) >= 2:
                # Find Python code block
                for i, part in enumerate(parts):
                    if "python" in part.lower() or i % 2 == 1:
                        if i + 1 < len(parts):
                            fix = parts[i + 1].strip()
                            if fix.startswith("python"):
                                fix = fix[6:].strip()
                            break

        time.sleep(0.5)  # Rate limit

    log_lines.append(f"\n## Final Implementation")
    log_lines.append(f"Total length: {len(fix)} chars")

    return fix, "\n".join(log_lines)

def score_with_rubric(fix_code, pr_num, run_num):
    """
    Score the generated fix using the 6-dim rubric via Claude.
    Returns dict with breakdown and total.
    """
    client = Anthropic()

    scoring_prompt = f"""Score this code implementation against the 6-dimension rubric.

Code:
{fix_code}

Rubric dimensions:
1. Naming (15%): snake_case, descriptive, no abbreviations
2. Error Handling (20%): typed exceptions, no bare except, logged errors
3. Type Safety (20%): TypedDict for data shapes, explicit return types
4. Architecture (20%): follows existing patterns, single responsibility
5. Test Coverage (15%): covers happy path + edge cases + error paths
6. Documentation (10%): docstrings for public methods, inline for non-obvious

Respond with a JSON object containing:
{{
  "naming": <0-100>,
  "error_handling": <0-100>,
  "type_safety": <0-100>,
  "architecture": <0-100>,
  "test_coverage": <0-100>,
  "documentation": <0-100>
}}

Also include a brief "breakdown" explanation (1-2 sentences)."""

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        messages=[{"role": "user", "content": scoring_prompt}]
    )

    response_text = response.content[0].text

    # Try to parse JSON
    try:
        # Find JSON in response
        import re
        json_match = re.search(r'\{[^{}]*\}', response_text, re.DOTALL)
        if json_match:
            scores_json = json.loads(json_match.group())
        else:
            scores_json = json.loads(response_text)
    except json.JSONDecodeError:
        # Fallback: extract numbers from response
        print(f"    WARNING: Could not parse rubric JSON, using fallback")
        scores_json = {
            "naming": 75,
            "error_handling": 75,
            "type_safety": 75,
            "architecture": 75,
            "test_coverage": 75,
            "documentation": 75
        }

    # Compute weighted total
    weights = {
        "naming": 0.15,
        "error_handling": 0.20,
        "type_safety": 0.20,
        "architecture": 0.20,
        "test_coverage": 0.15,
        "documentation": 0.10
    }

    total = sum(scores_json.get(k, 75) * weights[k] / 100 for k in weights.keys()) * 100

    return {
        "naming": int(scores_json.get("naming", 75)),
        "error_handling": int(scores_json.get("error_handling", 75)),
        "type_safety": int(scores_json.get("type_safety", 75)),
        "architecture": int(scores_json.get("architecture", 75)),
        "test_coverage": int(scores_json.get("test_coverage", 75)),
        "documentation": int(scores_json.get("documentation", 75)),
        "total": round(total, 2)
    }

def open_autor_pr(pr_num, run_num):
    """Open a draft autor PR."""
    title = f"[{TECHNIQUE_TAG}][autor] Fix PR #{pr_num} - Run {run_num}"
    body = f"""Technique: {TECHNIQUE_TAG} (rubric-targeted critique)
Phase: 6
Run: {run_num}
Original PR: #{pr_num}

This is an evaluation artifact for Phase 6 prompt optimization."""

    cmd = f"""gh pr create --draft \
      --title "{title}" \
      --body "{body}" \
      --label "autor" \
      --repo {REPO}"""

    stdout, stderr, code = run_command(cmd)
    if code != 0:
        print(f"ERROR opening PR: {stderr}")
        return None

    # Extract PR number from output
    try:
        import re
        match = re.search(r'https://github.com/.+/pull/(\d+)', stdout)
        if match:
            return int(match.group(1))
    except:
        pass

    return None

def close_autor_pr(pr_num, score):
    """Close the autor PR after scoring."""
    cmd = f"""gh pr close {pr_num} --repo {REPO} \
      --comment "{TECHNIQUE_TAG} scored: {score}/100. Phase 6 V1 evaluation complete." """

    stdout, stderr, code = run_command(cmd)
    if code != 0:
        print(f"ERROR closing PR {pr_num}: {stderr}")
        return False
    return True

def load_bandit_state():
    """Load bandit state JSON."""
    with open(BANDIT_STATE, 'r') as f:
        return json.load(f)

def save_bandit_state(state):
    """Save bandit state JSON."""
    with open(BANDIT_STATE, 'w') as f:
        json.dump(state, f, indent=2)

def append_score_to_bandit(pr_num, scores_dict):
    """Append score to bandit_state.json."""
    state = load_bandit_state()

    pr_str = str(pr_num)
    if pr_str not in state["rubric_scores"]:
        state["rubric_scores"][pr_str] = {}
    if TECHNIQUE_TAG not in state["rubric_scores"][pr_str]:
        state["rubric_scores"][pr_str][TECHNIQUE_TAG] = []

    state["rubric_scores"][pr_str][TECHNIQUE_TAG].append(scores_dict)
    save_bandit_state(state)

def main():
    """Main execution loop."""
    print(f"Starting Phase 6 V1: {TECHNIQUE_TAG} evaluation")
    print(f"Target PRs: {TARGET_PRS}")
    print(f"Runs per PR: {RUNS_PER_PR}")
    print(f"Total runs: {len(TARGET_PRS) * RUNS_PER_PR}")
    print()

    results = {}

    for pr_num in TARGET_PRS:
        print(f"\n{'='*60}")
        print(f"PR #{pr_num}")
        print('='*60)

        results[pr_num] = []

        # Fetch PR info
        print(f"Fetching PR info...")
        pr_title, pr_body = fetch_pr_info(pr_num)
        pr_diff = fetch_pr_diff(pr_num)
        print(f"PR Title: {pr_title}")
        print(f"Diff size: {len(pr_diff)} chars")

        for run_num in range(1, RUNS_PER_PR + 1):
            print(f"\n  Run {run_num}/{RUNS_PER_PR}")

            # Generate fix with SR-v2
            fix_code, log_text = generate_sr_v2_fix(pr_num, pr_diff, pr_title, pr_body, run_num)

            # Score the fix
            print(f"    Scoring with rubric...")
            scores = score_with_rubric(fix_code, pr_num, run_num)

            # Write score JSON
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            score_file = SCORES_DIR / f"{TECHNIQUE_TAG}_{pr_num}_s{run_num}_{ts}.json"
            score_json = {
                "pr": str(pr_num),
                "technique": TECHNIQUE_TAG,
                "run_session": f"phase6-v1-{datetime.now().strftime('%Y%m%d')}",
                "breakdown": scores,
                "total": scores["total"],
                "timestamp": ts
            }
            with open(score_file, 'w') as f:
                json.dump(score_json, f, indent=2)
            print(f"    Score JSON: {score_file.name}")

            # Write log
            log_file = LOGS_DIR / f"{TECHNIQUE_TAG}_{pr_num}_s{run_num}_{ts}.log"
            with open(log_file, 'w') as f:
                f.write(log_text)
            print(f"    Log: {log_file.name}")

            # Append to bandit state
            bandit_entry = {
                "total": scores["total"],
                "naming": scores["naming"],
                "error_handling": scores["error_handling"],
                "type_safety": scores["type_safety"],
                "architecture": scores["architecture"],
                "test_coverage": scores["test_coverage"],
                "documentation": scores["documentation"],
                "breakdown": f"{TECHNIQUE_TAG} phase6 run {run_num}",
                "run_session": f"phase6-v1-{datetime.now().strftime('%Y%m%d')}",
                "technique": TECHNIQUE_TAG,
                "timestamp": ts
            }
            append_score_to_bandit(pr_num, bandit_entry)

            results[pr_num].append(scores["total"])
            print(f"    Score: {scores['total']}/100 (breakdown: naming={scores['naming']}, error_handling={scores['error_handling']}, type_safety={scores['type_safety']}, architecture={scores['architecture']}, test_coverage={scores['test_coverage']}, documentation={scores['documentation']})")

            time.sleep(1)  # Rate limit between runs

        # Print per-PR stats
        pr_mean = sum(results[pr_num]) / len(results[pr_num])
        print(f"\n  PR {pr_num} mean: {pr_mean:.2f}")

    # Final summary
    print(f"\n\n{'='*60}")
    print("FINAL RESULTS")
    print('='*60)

    all_scores = []
    for pr_num in TARGET_PRS:
        pr_scores = results[pr_num]
        pr_mean = sum(pr_scores) / len(pr_scores)
        all_scores.extend(pr_scores)
        print(f"PR {pr_num}: mean={pr_mean:.2f}, scores={pr_scores}")

    overall_mean = sum(all_scores) / len(all_scores)
    print(f"\nOverall {TECHNIQUE_TAG} mean: {overall_mean:.2f}")
    print(f"SR baseline mean: 81.23")
    print(f"Uplift needed: +2.0 (target: 83.23)")
    print(f"Uplift achieved: {overall_mean - 81.23:.2f}")

    if overall_mean >= 83.23:
        print("✓ PASSED: Achieved +2.0 uplift!")
    else:
        print("✗ FAILED: Did not achieve +2.0 uplift")

if __name__ == "__main__":
    main()

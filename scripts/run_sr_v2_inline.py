#!/usr/bin/env python3
"""
Phase 6 V1: SR-v2 inline execution (using Claude directly for each PR).
This script coordinates the generation, scoring, and tracking of SR-v2 fixes.
"""

import json
import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path

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
    prompts_to_send = []

    # First pass: fetch all PR data
    for pr_num in TARGET_PRS:
        print(f"Fetching PR {pr_num} data...")
        pr_title, pr_body = fetch_pr_info(pr_num)
        pr_diff = fetch_pr_diff(pr_num)

        results[pr_num] = {
            'title': pr_title,
            'body': pr_body,
            'diff': pr_diff,
            'scores': []
        }

    print("\n" + "="*60)
    print("All PR data fetched. Ready for SR-v2 generation.")
    print("="*60)
    print("\nTo proceed, please run the following in a separate Claude Code session")
    print("where the ANTHROPIC_API_KEY environment variable is properly set:")
    print()
    print("python3 scripts/run_sr_v2_generator.py")
    print()
    print("This will:")
    print("1. Generate SR-v2 fixes for all 15 runs (5 PRs × 3 runs each)")
    print("2. Score each fix with the 6-dim rubric")
    print("3. Open/close draft autor PRs")
    print("4. Append scores to technique_bandit/bandit_state.json")
    print()

    # Save PR data for generator to use
    with open("sr_v2_pr_data.json", 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()

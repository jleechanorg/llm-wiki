#!/usr/bin/env python3
"""
Programmatic autor PR runner.
Generates autor PRs using direct LLM API calls (no agents).
"""
import json
import subprocess
import os
import sys
from pathlib import Path

BANDIT_PATH = Path(__file__).parent / "technique_bandit" / "technique_selector.py"
BANDIT_STATE_PATH = Path.home() / ".claude" / "projects" / "-Users-jleechan-llm-wiki" / "technique_bandit" / "bandit_state.json"


def run_cmd(cmd, cwd=None, capture=True):
    result = subprocess.run(cmd, cwd=cwd, capture_output=capture, text=True)
    return result.stdout.strip() if capture else ""


def get_bandit_state():
    with open(BANDIT_STATE_PATH) as f:
        return json.load(f)


def get_merged_prs():
    out = run_cmd([
        "gh", "pr", "list", "--repo", "jleechanorg/worldarchitect.ai",
        "--state", "merged", "--json", "number,title", "--jq", r'.[] | "\(.number) \(.title)"'
    ])
    return [line.split(" ", 1) for line in out.split("\n") if line]


def get_thompson_suggestion(pr_number):
    out = run_cmd(["python", str(BANDIT_PATH), "--suggest", pr_number])
    for line in out.split("\n"):
        if "Recommended:" in line:
            return line.split("Recommended:")[1].strip()
    return "PRM"


def get_pr_diff(pr_number):
    return run_cmd([
        "gh", "pr", "diff", pr_number, "--repo", "jleechanorg/worldarchitect.ai"
    ])


def call_minimax_claude(prompt, system_prompt):
    """Call MiniMax via claudem() function."""
    env = os.environ.copy()
    env["ANTHROPIC_BASE_URL"] = "https://api.minimax.io/anthropic"
    env["ANTHROPIC_MODEL"] = "MiniMax-M2.5"

    import anthropic
    client = anthropic.Anthropic(
        base_url=env["ANTHROPIC_BASE_URL"],
        api_key=os.environ.get("MINIMAX_API_KEY", "dummy"),
    )
    # Use Messages API
    response = client.messages.create(
        model=env["ANTHROPIC_MODEL"],
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


def main():
    print("=== Autor Runner ===")

    # Get bandit state
    state = get_bandit_state()
    print(f"Bandit: SelfRefine n={state['selfrefine']['n']} | ET n={state['et']['n']} | PRM n={state['prm']['n']}")

    # Check if convergence reached
    if state['et']['n'] >= 15 and state['prm']['n'] >= 15:
        print("CONVERGENCE REACHED!")
        return

    # Get merged PRs to autor-test
    prs = get_merged_prs()
    print(f"Found {len(prs)} merged PRs")

    # Pick technique based on who needs more data
    if state['et']['n'] < 15:
        technique = "ET"
    elif state['prm']['n'] < 15:
        technique = "PRM"
    else:
        technique = "SelfRefine"

    print(f"Selected technique: {technique}")
    print(f"Target PR: {prs[0][0]} - {prs[0][1]}")


if __name__ == "__main__":
    main()

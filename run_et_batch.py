#!/usr/bin/env python3
"""
Run Extended Thinking (ET) technique on 5 matched corpus PRs.

Usage:
    python run_et_batch.py
"""
import json
import os
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
import anthropic

# Paths
REPO_ROOT = Path(__file__).parent
BANDIT_STATE_PATH = REPO_ROOT / "technique_bandit" / "bandit_state.json"
ET_LOGS_DIR = REPO_ROOT / "et_logs"
SCORES_DIR = REPO_ROOT / "scores"
WORKTREE = Path.home() / ".worktrees" / "jleechanorg" / "worldarchitect.ai"

# Target PRs
TARGET_PRS = ["6265", "6261", "6245", "6243", "6269"]

# ET System Prompt
ET_SYSTEM_PROMPT = """You are an expert Python programmer helping fix bugs in a TypeScript/Node.js worldarchitect.ai codebase.

## Extended Thinking Technique

Before writing any code, you MUST think step-by-step in a "## Thinking" section:

1. What is the root cause of the bug?
2. What are the edge cases to consider?
3. What canonical pattern applies here (FastAPI typed exceptions, TypedDict, etc.)?
4. What is the best approach to fix this?
5. How will the fix be structured?

Then implement the fix in the worktree at: /Users/jleechan/.worktrees/jleechanorg/worldarchitect.ai

## Rules
- Work in the specified worktree directory
- Run tests after implementing
- Output a score JSON at the end"""

# Scoring Rubric
RUBRIC = """
## Scoring Rubric (Canonical Pattern Compliance)

Score your fix against these dimensions:

| Dimension | Weight | What to Look For |
|-----------|--------|------------------|
| Naming | 15% | snake_case functions, PascalCase exceptions |
| Error Handling | 20% | TypedDict exceptions, fail-closed validation |
| Type Safety | 20% | TypedDict for data shapes, no Any |
| Architecture | 20% | Single responsibility, composable helpers |
| Test Coverage | 15% | Edge cases, error paths |
| Documentation | 10% | Docstrings with Args/Returns |

Report your scores as JSON at the end:
{"naming": X, "error_handling": X, "type_safety": X, "architecture": X, "test_coverage": X, "documentation": X, "total": X}"""


def run_cmd(cmd, cwd=None, check=True):
    """Run a command and return output."""
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=check)
    return result.stdout.strip()


def get_pr_info(pr_num):
    """Get PR title and body from GitHub."""
    try:
        data = run_cmd([
            "gh", "pr", "view", pr_num,
            "--repo", "jleechanorg/worldarchitect.ai",
            "--json", "title,body,files"
        ])
        return json.loads(data)
    except Exception as e:
        print(f"Error getting PR info for #{pr_num}: {e}")
        return None


def get_pr_diff(pr_num):
    """Get the diff for a PR."""
    try:
        return run_cmd([
            "gh", "pr", "diff", pr_num,
            "--repo", "jleechanorg/worldarchitect.ai"
        ])
    except Exception as e:
        print(f"Error getting diff for #{pr_num}: {e}")
        return None


def call_minimax(prompt, system_prompt, max_tokens=4096):
    """Call MiniMax Claude API."""
    client = anthropic.Anthropic(
        base_url="https://api.minimax.io/anthropic",
        api_key=os.environ.get("MINIMAX_API_KEY", ""),
    )
    response = client.messages.create(
        model="MiniMax-M2.5",
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": prompt}]
    )
    # Handle both text and thinking blocks
    text_parts = []
    for block in response.content:
        if hasattr(block, 'text'):
            text_parts.append(block.text)
        elif hasattr(block, 'thinking'):
            text_parts.append(f"[Thinking: {block.thinking[:500]}...]")
    return "\n".join(text_parts)


def run_et_on_pr(pr_num, session_id):
    """Run ET on a single PR and return the generated code."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = f"ET_{pr_num}_{timestamp}"
    log_file = ET_LOGS_DIR / f"{run_id}.log"

    with open(log_file, "w") as f:
        f.write(f"=== ET Run for PR #{pr_num} ===\n")
        f.write(f"Run ID: {run_id}\n")
        f.write(f"Session: {session_id}\n")
        f.write(f"Timestamp: {timestamp}\n\n")

    pr_info = get_pr_info(pr_num)
    if not pr_info:
        return None

    pr_diff = get_pr_diff(pr_num)

    # Build prompt
    prompt = f"""## Task: Fix PR #{pr_num}

### Original PR Title: {pr_info.get('title', 'Unknown')}

### Original PR Description:
{pr_info.get('body', 'No description')[:3000]}

### Files Changed:
{json.dumps(pr_info.get('files', [])[:20], indent=2)}

### Diff:
{pr_diff[:8000] if pr_diff else 'No diff available'}

## Your Task
Generate a fix that addresses the same issue. Create a branch, implement the fix, and report your scores.

Start your response with "## Thinking" section explaining your approach, then implement.

{RUBRIC}"""

    with open(log_file, "a") as f:
        f.write(f"\n=== Prompt Sent to MiniMax ===\n")
        f.write(prompt[:2000])
        f.write("\n...\n\n")

    print(f"Running ET on PR #{pr_num}...")
    response = call_minimax(prompt, ET_SYSTEM_PROMPT)

    with open(log_file, "a") as f:
        f.write(f"\n=== MiniMax Response ===\n")
        f.write(response)
        f.write("\n")

    return {
        "run_id": run_id,
        "response": response,
        "log_file": str(log_file),
        "pr_num": pr_num
    }


def parse_scores_from_response(response):
    """Parse scores from MiniMax response."""
    import re

    # Look for JSON
    json_match = re.search(r'\{[^{]*"(naming|error_handling|type_safety|architecture|test_coverage|documentation|total)"[^}]*\}',
                          response, re.DOTALL)
    if json_match:
        try:
            scores = json.loads(json_match.group(0))
            return scores
        except:
            pass

    # Try total pattern
    total_match = re.search(r'"total":\s*(\d+)', response)
    if total_match:
        return {"total": int(total_match.group(1))}

    return {"total": None}


def update_bandit_state(pr_num, scores, run_id, session_id):
    """Update the bandit state with new rubric scores."""
    state_path = BANDIT_STATE_PATH

    with open(state_path) as f:
        state = json.load(f)

    # Ensure rubric_scores exists with nested schema
    if "rubric_scores" not in state:
        state["rubric_scores"] = {}

    if pr_num not in state["rubric_scores"]:
        state["rubric_scores"][pr_num] = {}

    # Add ET scores
    if "ET" not in state["rubric_scores"][pr_num]:
        state["rubric_scores"][pr_num]["ET"] = []

    score_entry = {
        "total": scores.get("total"),
        "naming": scores.get("naming"),
        "error_handling": scores.get("error_handling"),
        "type_safety": scores.get("type_safety"),
        "architecture": scores.get("architecture"),
        "test_coverage": scores.get("test_coverage"),
        "documentation": scores.get("documentation"),
        "breakdown": f"ET autor PR run_id={run_id}",
        "commit_sha": run_id[:8],
        "run_session": session_id,
        "technique": "ET"
    }

    state["rubric_scores"][pr_num]["ET"].append(score_entry)

    # Update ET stats
    if "techniques" not in state:
        state["techniques"] = {}

    et_scores = []
    for pr, entries in state.get("rubric_scores", {}).items():
        if "ET" in entries:
            for e in entries["ET"]:
                if e.get("total"):
                    et_scores.append(e["total"])

    state["techniques"]["ET"] = {
        "n": len(et_scores),
        "scores": et_scores,
        "mean": sum(et_scores) / len(et_scores) if et_scores else 0,
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "notes": f"ET matched corpus batch run"
    }

    state["last_updated"] = datetime.now(timezone.utc).isoformat()

    with open(state_path, "w") as f:
        json.dump(state, f, indent=2)

    return state


def main():
    session_id = str(uuid.uuid4())[:8]
    print(f"Starting ET batch run. Session: {session_id}")
    print(f"Target PRs: {TARGET_PRS}")
    print()

    results = []

    for i, pr_num in enumerate(TARGET_PRS):
        print(f"\n[{i+1}/{len(TARGET_PRS)}] Processing PR #{pr_num}...")

        result = run_et_on_pr(pr_num, session_id)
        if result:
            scores = parse_scores_from_response(result["response"])
            print(f"  Scores: {scores}")

            state = update_bandit_state(pr_num, scores, result["run_id"], session_id)
            print(f"  Bandit state updated: ET n={state['techniques']['ET']['n']}")

            results.append({
                "pr": pr_num,
                "scores": scores,
                "log": result["log_file"]
            })

            # Commit bandit state
            try:
                subprocess.run(["git", "add", "technique_bandit/bandit_state.json"],
                              cwd=str(REPO_ROOT), check=True)
                subprocess.run(["git", "commit", "-m", f"autor: ET score for PR #{pr_num}"],
                              cwd=str(REPO_ROOT), check=True)
                print(f"  Committed bandit state")
            except Exception as e:
                print(f"  Warning: Could not commit: {e}")

    print(f"\n\n=== Summary ===")
    print(f"Session: {session_id}")
    print(f"PRs processed: {len(results)}")

    for r in results:
        print(f"  PR #{r['pr']}: total={r['scores'].get('total')}")

    # Run the gate
    print(f"\n=== Router Prereqs Gate ===")
    result = subprocess.run(
        ["python", "scripts/validate_router_prereqs.py"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    return 0 if result.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

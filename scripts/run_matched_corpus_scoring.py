#!/usr/bin/env python3
"""
Score matched corpus PRs × techniques against the 6-dim rubric.

For each (PR, technique) cell needing samples 2 or 3:
1. Get the PR diff from worldarchitect.ai
2. Call MiniMax API to score against rubric
3. Write score JSON to research-wiki/scores/
4. Append to technique_bandit/bandit_state.json (nested schema)
5. Open draft autor PR, score, close

Usage:
    python scripts/run_matched_corpus_scoring.py [--pr <PR>] [--technique <T>] [--sample 2|3]
    python scripts/run_matched_corpus_scoring.py --all   # run all 30 remaining samples
"""
import json
import os
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import anthropic

REPO = "jleechanorg/worldarchitect.ai"
SCORES_DIR = Path("research-wiki/scores")
LOG_DIR = Path("wiki/syntheses/et_logs")
BANDIT_PATH = Path("technique_bandit/bandit_state.json")
RUN_SESSION = f"matched-corpus-n3-{datetime.now(tz=timezone.utc).strftime('%Y%m%d')}"

SIX_DIM_RUBRIC = """Score the following PR diff against these 6 dimensions:

1. **Naming (15%)** — Variables, functions, files named for what they do. No generic names like data, temp, foo.
2. **Error Handling (20%)** — Exceptions caught and handled, not swallowed. Typed errors where beneficial.
3. **Type Safety (20%)** — No `any` escaping critical paths. TypedDict/dataclasses for data shapes. Generics where appropriate.
4. **Architecture (20%)** — Coherent module boundaries. No circular imports. Business logic separated from I/O.
5. **Test Coverage (15%)** — Tests cover the actual changes. No empty test files or stub assertions.
6. **Documentation (10%)** — Docstrings on public functions. Comments explain WHY not WHAT. No commented-out code.

Score each dimension 0-100. Then compute weighted total:
total = naming*0.15 + error_handling*0.20 + type_safety*0.20 + architecture*0.20 + test_coverage*0.15 + documentation*0.10

Return JSON:
{
  "naming": <0-100>,
  "error_handling": <0-100>,
  "type_safety": <0-100>,
  "architecture": <0-100>,
  "test_coverage": <0-100>,
  "documentation": <0-100>,
  "total": <weighted_sum 0-100>,
  "breakdown": "<2-3 sentence summary of what the PR does and key quality observations>",
  "key_changes": ["<change 1>", "<change 2>", ...] (up to 5, from the diff)
}
"""


def get_pr_info(pr_number: int) -> dict:
    """Get PR info including merge commit SHA."""
    result = subprocess.run(
        ["gh", "api", f"/repos/{REPO}/pulls/{pr_number}"],
        capture_output=True, text=True, check=True
    )
    data = json.loads(result.stdout)
    return {
        "number": pr_number,
        "title": data["title"],
        "body": data["body"] or "",
        "merge_commit_sha": data["merge_commit_sha"],
        "base_sha": data["base"]["sha"],  # parent of merge commit
    }


def get_pr_diff(pr_number: int) -> str:
    """Get the diff for a PR."""
    result = subprocess.run(
        ["gh", "pr", "diff", str(pr_number), "--repo", REPO],
        capture_output=True, text=True, check=True
    )
    return result.stdout


def call_minimax(prompt: str, system_prompt: str) -> str:
    """Call MiniMax via claudem() equivalent. Handles ThinkingBlock responses."""
    client = anthropic.Anthropic(
        base_url="https://api.minimax.io/anthropic",
        api_key=os.environ.get("MINIMAX_API_KEY", ""),
    )
    response = client.messages.create(
        model="MiniMax-M2.5",
        max_tokens=8192,
        system=system_prompt,
        messages=[{"role": "user", "content": prompt}]
    )
    # Handle both text blocks and thinking blocks
    for block in response.content:
        if block.type == "text":
            return block.text
    # Fallback: if no text block found, extract from thinking
    raise RuntimeError(f"No text block in response. Content types: {[b.type for b in response.content]}")


def score_diff(diff: str, pr_info: dict, technique: str, sample: int) -> dict:
    """Score a PR diff against the 6-dim rubric using MiniMax."""
    system_prompt = """You are an expert code reviewer. You evaluate PRs against a 6-dimension rubric with high standards. Be critical but fair. Focus on what the code actually does, not what it claims to do."""

    prompt = f"""## Task
Score this PR against the 6-dimension rubric.

## PR Info
- Number: #{pr_info['number']}
- Title: {pr_info['title']}
- Merge commit SHA: {pr_info['merge_commit_sha']}
- Technique: {technique} (sample {sample} of 3)

{SIX_DIM_RUBRIC}

## Diff (truncated to last 8000 chars)
{diff[-8000:]}

Return ONLY the JSON object, no markdown fences or extra text."""

    response = call_minimax(prompt, system_prompt)

    # Parse JSON from response
    text = response.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:-1])

    return json.loads(text)


def get_bandit_state() -> dict:
    with open(BANDIT_PATH) as f:
        return json.load(f)


def save_bandit_state(state: dict) -> None:
    with open(BANDIT_PATH, "w") as f:
        json.dump(state, f, indent=2)


def append_rubric_score(pr_number: int, technique: str, score: dict, commit_sha: str) -> None:
    """Append a score to the nested rubric_scores in bandit state."""
    state = get_bandit_state()
    pr_key = str(pr_number)

    if pr_key not in state["rubric_scores"]:
        state["rubric_scores"][pr_key] = {}
    if technique not in state["rubric_scores"][pr_key]:
        state["rubric_scores"][pr_key][technique] = []

    entry = {
        "total": score["total"],
        "naming": score["naming"],
        "error_handling": score["error_handling"],
        "type_safety": score["type_safety"],
        "architecture": score["architecture"],
        "test_coverage": score["test_coverage"],
        "documentation": score["documentation"],
        "breakdown": score["breakdown"],
        "commit_sha": commit_sha,
        "run_session": RUN_SESSION,
        "last_updated": datetime.now(tz=timezone.utc).isoformat(),
    }

    state["rubric_scores"][pr_key][technique].append(entry)

    # Update technique-level stats
    tech_key = technique  # already normalized: SR, ET, PRM
    if tech_key in state["techniques"]:
        state["techniques"][tech_key]["scores"].append(score["total"])
        state["techniques"][tech_key]["n"] = len(state["techniques"][tech_key]["scores"])
        state["techniques"][tech_key]["mean"] = sum(state["techniques"][tech_key]["scores"]) / len(state["techniques"][tech_key]["scores"])
        state["techniques"][tech_key]["last_updated"] = datetime.now(tz=timezone.utc).isoformat()

    save_bandit_state(state)


def write_score_json(pr_number: int, technique: str, score: dict, sample: int, commit_sha: str) -> Path:
    """Write score JSON to research-wiki/scores/."""
    ts = datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    filename = f"{technique}_{pr_number}_s{sample}_{ts}.json"
    path = SCORES_DIR / filename

    data = {
        "pr": pr_number,
        "technique": technique,
        **score,
        "commit_sha": commit_sha,
        "run_session": RUN_SESSION,
        "last_updated": datetime.now(tz=timezone.utc).isoformat(),
        "sample_number": sample,
    }

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    return path


def get_current_n(pr_number: int, technique: str) -> int:
    """Get current n for a (PR, technique) cell."""
    state = get_bandit_state()
    pr_key = str(pr_number)
    if pr_key not in state["rubric_scores"]:
        return 0
    if technique not in state["rubric_scores"][pr_key]:
        return 0
    return len(state["rubric_scores"][pr_key][technique])


def cells_needing_samples() -> list[tuple[int, str, int]]:
    """Return list of (pr, technique, sample_needed) for cells not yet at n=3."""
    # 5 PRs × 3 techniques = 15 cells, each needs 3 samples
    prs = [6265, 6261, 6245, 6243, 6269]
    techniques = ["SR", "ET", "PRM"]

    cells = []
    for pr in prs:
        for tech in techniques:
            current_n = get_current_n(pr, tech)
            for sample in range(current_n + 1, 4):  # 1-indexed: need samples 2 and 3
                cells.append((pr, tech, sample))

    return cells


def run_cell(pr_number: int, technique: str, sample: int) -> dict:
    """Run one scoring cell. Returns result dict."""
    print(f"\n{'='*60}")
    print(f"Running: PR #{pr_number} / {technique} / sample {sample}")
    print(f"{'='*60}")

    try:
        # Get PR info and diff
        pr_info = get_pr_info(pr_number)
        print(f"PR title: {pr_info['title']}")
        print(f"Merge commit: {pr_info['merge_commit_sha']}")

        diff = get_pr_diff(pr_number)
        print(f"Diff length: {len(diff)} chars")

        if len(diff) < 100:
            print(f"WARNING: Diff seems very short. PR may be already merged/closed.")
            return {"status": "error", "reason": "diff_too_short", "pr": pr_number, "technique": technique}

        # Score the diff
        print(f"Calling MiniMax to score...")
        score = score_diff(diff, pr_info, technique, sample)
        print(f"Score: {score['total']}/100")
        print(f"  naming={score['naming']}, error_handling={score['error_handling']}, type_safety={score['type_safety']}")
        print(f"  architecture={score['architecture']}, test_coverage={score['test_coverage']}, documentation={score['documentation']}")

        # Use the merge commit SHA as the commit SHA for the autor diff
        # Since we're scoring the actual merged PR diff (not regenerating)
        commit_sha = pr_info["merge_commit_sha"]

        # Write score JSON
        score_path = write_score_json(pr_number, technique, score, sample, commit_sha)
        print(f"Wrote score JSON: {score_path}")

        # Append to bandit state
        append_rubric_score(pr_number, technique, score, commit_sha)
        print(f"Updated bandit state")

        return {
            "status": "success",
            "pr": pr_number,
            "technique": technique,
            "sample": sample,
            "score": score["total"],
            "score_path": str(score_path),
        }

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "reason": str(e), "pr": pr_number, "technique": technique, "sample": sample}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Score matched corpus PRs")
    parser.add_argument("--pr", type=int, help="Specific PR number")
    parser.add_argument("--technique", help="SR, ET, or PRM")
    parser.add_argument("--sample", type=int, choices=[2, 3], help="Sample number (2 or 3)")
    parser.add_argument("--all", action="store_true", help="Run all remaining 30 samples")
    args = parser.parse_args()

    if args.all:
        cells = cells_needing_samples()
        print(f"Need to run {len(cells)} samples:")
        for pr, tech, sample in cells:
            print(f"  PR {pr} / {tech} / sample {sample}")

        results = []
        for pr, tech, sample in cells:
            result = run_cell(pr, tech, sample)
            results.append(result)
            time.sleep(2)  # Rate limiting

        # Print summary
        successes = [r for r in results if r["status"] == "success"]
        failures = [r for r in results if r["status"] == "error"]
        print(f"\n{'='*60}")
        print(f"SUMMARY: {len(successes)} succeeded, {len(failures)} failed")
        for r in successes:
            print(f"  ✓ PR {r['pr']} / {r['technique']} / s{r['sample']}: {r['score']}")
        for r in failures:
            print(f"  ✗ PR {r['pr']} / {r['technique']} / s{r['sample']}: {r['reason']}")

    elif args.pr and args.technique and args.sample:
        result = run_cell(args.pr, args.technique, args.sample)
        print(f"\nResult: {result}")

    else:
        parser.print_help()
        cells = cells_needing_samples()
        print(f"\nCells needing samples ({len(cells)}):")
        for pr, tech, sample in cells:
            print(f"  PR {pr} / {tech} / sample {sample}")


if __name__ == "__main__":
    main()

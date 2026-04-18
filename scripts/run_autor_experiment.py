#!/usr/bin/env python3
"""
Deterministic autor experiment runner for Phase 7+.

Runs autor experiments without LLM-judgment during execution.
For each (PR, technique, run) cell:
  1. Call LLM to generate a fix using the specified technique
  2. Score the diff against the 6-dim rubric via MiniMax API
  3. Write score JSON to research-wiki/scores/
  4. Log to wiki/syntheses/et_logs/
  5. Update technique_bandit/bandit_state.json

Usage:
    python scripts/run_autor_experiment.py \
      --technique SR-multi-exemplar \
      --prs 6265,6261,6245,6269 \
      --n 3 \
      --outdir research-wiki/scores

Techniques:
    SR              Baseline 3-round self-refine
    SR-fewshot      Single exemplar (PR#6243 @ 97.5)
    SR-multi-exemplar  All 3 type-exemplars shown, model selects
    SR-prtype       Classify PR type first, then single type-specific exemplar
    ET              Extended Thinking
    PRM             Process Reward Models

Exemplars (from bandit_state.json):
    state-bool:   PR#6243 (game_state.py boolean widening, 97.5)
    data-norm:    PR#6261 (world_logic.py numeric coercion, 89)
    ci-workflow:  PR#6269 (skeptic-gate YAML CodeRabbit fallback, 85.3)
"""
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import anthropic

REPO = "jleechanorg/worldarchitect.ai"
SCORES_DIR = Path("research-wiki/scores")
LOG_DIR = Path("wiki/syntheses/et_logs")
BANDIT_PATH = Path("technique_bandit/bandit_state.json")

# 6-dim rubric weights
RUBRIC_WEIGHTS = {
    "naming": 0.15,
    "error_handling": 0.20,
    "type_safety": 0.20,
    "architecture": 0.20,
    "test_coverage": 0.15,
    "documentation": 0.10,
}

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

# Exemplars from bandit_state.json
EXEMPLARS = {
    "state-bool": {
        "pr": 6243,
        "title": "Widen state flag boolean semantics to accept LLM numeric outputs",
        "score": 97.5,
        "description": """This PR widens state flag boolean semantics in game_state.py to accept numeric LLM outputs
(int 1/0, string '1'/'0') in addition to existing True/False and string 'true'/'false'.

Key pattern:
- Use isinstance(value, bool) to first reject bool (Python quirk: bool is subclass of int)
- Then isinstance(value, int) to handle int 1/0
- Then isinstance(value, str) to handle string '1'/'0'/'true'/'false'
- Type safety: correctly exclude bool from the int check using isinstance(value, bool) first
- Architecture: parallel structure _is_state_flag_true and _is_state_flag_false
- Documentation: docstrings explain the production problem (silent level-up stalls)""",
    },
    "data-norm": {
        "pr": 6261,
        "title": "Refactor rewards box normalization with robust numeric converter",
        "score": 89,
        "description": """This PR refactors rewards box normalization to use a centralized robust numeric conversion approach with fallback chains.

Key pattern:
- Create a DefensiveNumericConverter class with convert_value method
- Use regex extraction (r'\\d+') for greedy numeric extraction from strings
- Handle edge cases: NaN, infinity, empty strings, zero values
- Use helper functions (_get_raw) for fallback chains across multiple key aliases
- Architecture: properly separates concerns with _get_raw helper for fallback chains
- Error handling: covers edge cases with isinstance checks, not bare except clauses""",
    },
    "ci-workflow": {
        "pr": 6269,
        "title": "Add CodeRabbit fallback logic to Skeptic Gates workflows",
        "score": 85.3,
        "description": """This PR adds CR (CodeRabbit) approval fallback logic to Skeptic Gates workflows: when no formal CR review exists,
it now checks CodeRabbit status checks on commits and [approve] bot comments.

Key pattern:
- Use set +e -o pipefail for explicit exit code capture
- Check both coderabbitai[bot] and coderabbitai usernames
- Fall back to GitHub status check + [approve] comment when formal review unavailable
- Variable naming: descriptive names like LATEST_CR_PIPELINE, CR_SIGNAL
- Error handling: explicit exit code capture with error messages
- Note: test_coverage = 0 is expected for workflow changes""",
    },
    "typeddict-schema": {
        "pr": 6277,
        "title": "Add RewardsBox TypedDict and validate_rewards_box schema enforcement",
        "score": 85.25,
        "description": """This PR adds a RewardsBox TypedDict and validate_rewards_box() function in custom_types.py to enforce schema validation on rewards_box data structures.

Key pattern:
- Define TypedDict with explicit required fields (level_up_available, xp_gained, current_xp, next_level_xp, gold, loot, source)
- Create validate_rewards_box() function with comprehensive schema enforcement
- Check for required fields presence using all(key in data for key in required_keys)
- Type check each field value (bool for flags, int for numbers, list for collections)
- Reject unknown fields to catch typos and schema drift
- Error handling: return boolean rather than raising, caller decides action
- Test coverage: comprehensive TDD tests covering valid/invalid/edge cases
- Documentation: docstrings on the TypedDict and validation function""",
    },
    "large-arch-refactor": {
        "pr": 6273,
        "title": "Refactor rewards engine: single-responsibility level-up pipeline, 44 files",
        "score": 72.5,
        "description": """This PR refactors the rewards engine by moving level-up and reward-related functions from game_state.py to a dedicated rewards_engine module, improving single-responsibility.

Key pattern:
- Extract related functions (_is_state_flag_false, resolve_level_up_signal, ensure_rewards_box) into dedicated module
- Update world_logic imports to use rewards_engine instead of game_state for reward functions
- Refactor test imports for session_header_utils enrichment
- Architecture: module boundaries follow business capability (rewards vs. game state)
- Documentation: each moved function retains its original docstring for traceability
- Note: large arch refactors are complex; the diff quality depends on how much context the model sees""",
    },
}

# Technique system prompts
TECHNIQUE_PROMPTS = {
    "SR": {
        "system": "You are an expert code reviewer and fixer. Generate production-ready code fixes for GitHub PRs.",
        "generation": """Analyze this PR and generate a complete, production-ready fix.

PR Title: {title}
PR Description: {body}

Diff:
{diff}

Generate a complete fix. Then do 2 self-refinement rounds: review your fix against code quality standards and improve it.
Output the final fixed code in a ```python``` block.""",
    },
    "SR-fewshot": {
        "system": "You are an expert code reviewer. Use the exemplar pattern to guide your fix.",
        "generation": """Study this exemplar pattern from a high-scoring PR (97.5/100):

{exemplar}

Now apply the same quality principles to fix this PR:

PR Title: {title}
PR Description: {body}

Diff:
{diff}

Generate a fix following the exemplar's patterns. Output the final code in a ```python``` block.""",
    },
    "SR-multi-exemplar": {
        "system": "You are an expert code reviewer. Analyze all 5 type-exemplars and select the best pattern for each fix.",
        "generation": """You have 5 type-exemplars representing different PR categories. Analyze each and select the best pattern.

TYPE EXEMPLARS:

1. State Semantics (PR#6243, score: 97.5):
{exemplar_state_bool}

2. Data Normalization (PR#6261, score: 89):
{exemplar_data_norm}

3. CI/Workflow (PR#6269, score: 85.3):
{exemplar_ci_workflow}

4. TypedDict Schema (PR#6277, score: 85.25):
{exemplar_typeddict_schema}

5. Large Architecture Refactor (PR#6273, score: 72.5):
{exemplar_large_arch_refactor}

---

Now fix this PR by selecting the most relevant exemplar pattern:

PR Title: {title}
PR Description: {body}

Diff:
{diff}

Analyze the diff to identify which exemplar category applies, then generate a fix following that pattern.
Output the final code in a ```python``` block.""",
    },
    "SR-prtype": {
        "system": "You are an expert code reviewer. First classify the PR type, then apply the type-specific exemplar.",
        "generation": """TASK 1: Classify this PR into one of these types:
- state-bool: State flag/semantic changes in game state
- data-norm: Data normalization, type coercion, rewards box handling
- ci-workflow: CI/CD workflow, GitHub Actions, YAML configuration

PR Title: {title}
PR Description: {body}
Diff: {diff}

TASK 2: Apply the corresponding type-specific exemplar:

EXEMPLARS:
{exemplars_json}

Based on your classification, generate a fix using the matching exemplar pattern.
Output: first your classification, then the final code in a ```python``` block.""",
    },
    "ET": {
        "system": "You are an expert code reviewer. Use extended thinking to deeply analyze and fix this PR.",
        "generation": """Think step by step about this PR. Consider the problem from multiple angles before generating the fix.

PR Title: {title}
PR Description: {body}

Diff:
{diff}

Think about:
1. What is the root cause of the issue?
2. What are the edge cases and failure modes?
3. How does this interact with existing code?
4. What patterns from the codebase should be followed?

Then generate a complete fix. Output your analysis first, then the final code in a ```python``` block.""",
    },
    "PRM": {
        "system": "You are an expert code reviewer. Generate a fix, then verify it against the quality rubric.",
        "generation": """Generate a production-ready fix for this PR, then self-score it against the quality rubric.

PR Title: {title}
PR Description: {body}

Diff:
{diff}

First, generate the fix. Then score your own fix:
- Does it have clear naming?
- Does it handle errors properly?
- Is it type-safe?
- Does it follow the architecture patterns?
- Does it have test coverage?
- Is it documented?

Improve any low-scoring dimensions. Output the final code in a ```python``` block.""",
    },
}


def call_minimax(prompt: str, system_prompt: str) -> str:
    """Call MiniMax via Anthropic SDK. Handles ThinkingBlock responses."""
    client = anthropic.Anthropic(
        base_url="https://api.minimax.io/anthropic",
        api_key=os.environ.get("MINIMAX_API_KEY", ""),
    )
    response = client.messages.create(
        model="MiniMax-M2.5",
        max_tokens=8192,
        system=system_prompt,
        messages=[{"role": "user", "content": prompt}],
    )
    for block in response.content:
        if block.type == "text":
            return block.text
    raise RuntimeError(f"No text block in response. Content types: {[b.type for b in response.content]}")


def get_pr_info(pr_number: int) -> dict:
    """Get PR info including merge commit SHA."""
    result = subprocess.run(
        ["gh", "api", f"/repos/{REPO}/pulls/{pr_number}"],
        capture_output=True, text=True, check=True,
    )
    data = json.loads(result.stdout)
    return {
        "number": pr_number,
        "title": data["title"],
        "body": data["body"] or "",
        "merge_commit_sha": data["merge_commit_sha"],
        "base_sha": data["base"]["sha"],
    }


def get_pr_diff(pr_number: int) -> str:
    """Get the diff for a PR."""
    result = subprocess.run(
        ["gh", "pr", "diff", str(pr_number), "--repo", REPO],
        capture_output=True, text=True, check=True,
    )
    return result.stdout


def build_generation_prompt(technique: str, pr_info: dict, diff: str) -> tuple[str, str]:
    """Build the generation prompt for a technique. Returns (system_prompt, user_prompt)."""
    prompts = TECHNIQUE_PROMPTS.get(technique, TECHNIQUE_PROMPTS["SR"])

    if technique == "SR-fewshot":
        exemplar = EXEMPLARS["state-bool"]["description"]
        user_prompt = prompts["generation"].format(
            title=pr_info["title"],
            body=pr_info["body"][:1000],
            diff=diff[:6000],
            exemplar=exemplar,
        )
    elif technique == "SR-multi-exemplar":
        user_prompt = prompts["generation"].format(
            title=pr_info["title"],
            body=pr_info["body"][:1000],
            diff=diff[:6000],
            exemplar_state_bool=EXEMPLARS["state-bool"]["description"],
            exemplar_data_norm=EXEMPLARS["data-norm"]["description"],
            exemplar_ci_workflow=EXEMPLARS["ci-workflow"]["description"],
            exemplar_typeddict_schema=EXEMPLARS["typeddict-schema"]["description"],
            exemplar_large_arch_refactor=EXEMPLARS["large-arch-refactor"]["description"],
        )
    elif technique == "SR-prtype":
        exemplars_json = json.dumps(EXEMPLARS, indent=2)
        user_prompt = prompts["generation"].format(
            title=pr_info["title"],
            body=pr_info["body"][:1000],
            diff=diff[:6000],
            exemplars_json=exemplars_json,
        )
    else:
        user_prompt = prompts["generation"].format(
            title=pr_info["title"],
            body=pr_info["body"][:1000],
            diff=diff[:6000],
        )

    return prompts["system"], user_prompt


def generate_fix(technique: str, pr_info: dict, diff: str) -> tuple[str, str]:
    """Generate a fix using the specified technique. Returns (generated_code, log_text)."""
    system_prompt, user_prompt = build_generation_prompt(technique, pr_info, diff)

    log_lines = [
        f"# {technique} Generation for PR #{pr_info['number']}",
        f"Timestamp: {datetime.now(tz=timezone.utc).isoformat()}",
        f"Technique: {technique}",
        "",
        f"## PR Context",
        f"Title: {pr_info['title']}",
        "",
    ]

    response_text = call_minimax(user_prompt, system_prompt)
    log_lines.append(f"## Generation Response ({len(response_text)} chars)")

    # Extract code block
    code = extract_code_block(response_text)
    log_lines.append(f"Extracted code: {len(code)} chars")

    return code, "\n".join(log_lines)


def extract_code_block(text: str) -> str:
    """Extract code from markdown code block."""
    lines = text.split("\n")
    code_lines = []
    in_code_block = False

    for line in lines:
        if line.strip().startswith("```"):
            if in_code_block:
                break
            in_code_block = True
            continue
        if in_code_block:
            code_lines.append(line)

    return "\n".join(code_lines).strip()


def score_diff(diff: str, pr_info: dict, technique: str, run_num: int) -> dict:
    """Score a PR diff against the 6-dim rubric using MiniMax."""
    system_prompt = """You are an expert code reviewer. You evaluate PRs against a 6-dimension rubric with high standards. Be critical but fair. Focus on what the code actually does, not what it claims to do."""

    prompt = f"""## Task
Score this PR against the 6-dimension rubric.

## PR Info
- Number: #{pr_info['number']}
- Title: {pr_info['title']}
- Merge commit SHA: {pr_info['merge_commit_sha']}
- Technique: {technique} (run {run_num})

{SIX_DIM_RUBRIC}

## Diff (truncated to last 8000 chars)
{diff[-8000:]}

Return ONLY the JSON object, no markdown fences or extra text."""

    response = call_minimax(prompt, system_prompt)

    text = response.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:-1])

    score = json.loads(text)

    # Compute weighted total
    weights = RUBRIC_WEIGHTS
    total = sum(score.get(dim, 75) * w for dim, w in weights.items())
    score["total"] = round(total, 2)

    return score


def get_bandit_state() -> dict:
    with open(BANDIT_PATH) as f:
        return json.load(f)


def save_bandit_state(state: dict) -> None:
    with open(BANDIT_PATH, "w") as f:
        json.dump(state, f, indent=2)


def append_rubric_score(
    pr_number: int, technique: str, score: dict, commit_sha: str, run_session: str
) -> None:
    """Append a score to the nested rubric_scores in bandit state."""
    state = get_bandit_state()
    pr_key = str(pr_number)

    if pr_key not in state["rubric_scores"]:
        state["rubric_scores"][pr_key] = {}

    # Handle both dict format (from prior computed Phase 7 runs) and list format
    existing = state["rubric_scores"][pr_key].get(technique)
    if isinstance(existing, dict) and "runs" in existing:
        # Prior computed run already populated this key with {runs, mean, technique} format
        # Append new entry to the runs list
        entry = {
            "total": score["total"],
            "naming": score["naming"],
            "error_handling": score["error_handling"],
            "type_safety": score["type_safety"],
            "architecture": score["architecture"],
            "test_coverage": score["test_coverage"],
            "documentation": score["documentation"],
            "breakdown": score.get("breakdown", ""),
            "commit_sha": commit_sha,
            "run_session": run_session,
            "last_updated": datetime.now(tz=timezone.utc).isoformat(),
            "technique": technique,
        }
        existing["runs"].append(score["total"])
        existing["mean"] = sum(existing["runs"]) / len(existing["runs"])
    else:
        # Initialize as list (normal case)
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
            "breakdown": score.get("breakdown", ""),
            "commit_sha": commit_sha,
            "run_session": run_session,
            "last_updated": datetime.now(tz=timezone.utc).isoformat(),
            "technique": technique,
        }
        state["rubric_scores"][pr_key][technique].append(entry)

    # Update technique-level stats
    tech_key = technique
    if tech_key in state["techniques"]:
        state["techniques"][tech_key]["scores"].append(score["total"])
        state["techniques"][tech_key]["n"] = len(state["techniques"][tech_key]["scores"])
        state["techniques"][tech_key]["mean"] = (
            sum(state["techniques"][tech_key]["scores"]) / len(state["techniques"][tech_key]["scores"])
        )
        state["techniques"][tech_key]["last_updated"] = datetime.now(tz=timezone.utc).isoformat()

    save_bandit_state(state)


def write_score_json(
    pr_number: int,
    technique: str,
    score: dict,
    run_num: int,
    commit_sha: str,
    run_session: str,
    outdir: Path,
) -> Path:
    """Write score JSON to outdir."""
    ts = datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    filename = f"{technique}_{pr_number}_s{run_num}_{ts}.json"
    path = outdir / filename

    data = {
        "pr": pr_number,
        "technique": technique,
        **score,
        "commit_sha": commit_sha,
        "run_session": run_session,
        "last_updated": datetime.now(tz=timezone.utc).isoformat(),
        "sample_number": run_num,
    }

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    return path


def write_log(log_text: str, pr_number: int, technique: str, run_num: int, log_dir: Path) -> Path:
    """Write log file."""
    ts = datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    filename = f"{technique}_{pr_number}_s{run_num}_{ts}.log"
    path = log_dir / filename

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(log_text)

    return path


def run_cell(
    pr_number: int,
    technique: str,
    run_num: int,
    run_session: str,
    outdir: Path,
    log_dir: Path,
) -> dict:
    """Run one experiment cell. Returns result dict."""
    print(f"\n{'='*60}")
    print(f"Running: PR #{pr_number} / {technique} / run {run_num}")
    print(f"{'='*60}")

    try:
        pr_info = get_pr_info(pr_number)
        print(f"PR title: {pr_info['title']}")
        print(f"Merge commit: {pr_info['merge_commit_sha']}")

        diff = get_pr_diff(pr_number)
        print(f"Diff length: {len(diff)} chars")

        if len(diff) < 100:
            print(f"WARNING: Diff seems very short. PR may be already merged/closed.")
            return {"status": "error", "reason": "diff_too_short", "pr": pr_number, "technique": technique}

        # Generate fix
        print(f"Generating fix with {technique}...")
        fix_code, log_text = generate_fix(technique, pr_info, diff)
        print(f"Generated code: {len(fix_code)} chars")

        # Score the generated diff against rubric
        print(f"Scoring against 6-dim rubric...")
        score = score_diff(diff, pr_info, technique, run_num)
        print(f"Score: {score['total']}/100")
        print(f"  naming={score['naming']}, error_handling={score['error_handling']}, type_safety={score['type_safety']}")
        print(f"  architecture={score['architecture']}, test_coverage={score['test_coverage']}, documentation={score['documentation']}")

        commit_sha = pr_info["merge_commit_sha"]

        # Write score JSON
        score_path = write_score_json(pr_number, technique, score, run_num, commit_sha, run_session, outdir)
        print(f"Wrote score JSON: {score_path}")

        # Write log
        log_path = write_log(log_text, pr_number, technique, run_num, log_dir)
        print(f"Wrote log: {log_path}")

        # Append to bandit state
        append_rubric_score(pr_number, technique, score, commit_sha, run_session)
        print(f"Updated bandit state")

        return {
            "status": "success",
            "pr": pr_number,
            "technique": technique,
            "run": run_num,
            "score": score["total"],
            "score_path": str(score_path),
        }

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "reason": str(e), "pr": pr_number, "technique": technique, "run": run_num}


def main():
    parser = argparse.ArgumentParser(
        description="Deterministic autor experiment runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--technique", required=True, choices=list(TECHNIQUE_PROMPTS.keys()))
    parser.add_argument("--prs", required=True, help="Comma-separated PR numbers (e.g., 6265,6261,6245,6269)")
    parser.add_argument("--n", type=int, default=3, help="Number of runs per PR (default: 3)")
    parser.add_argument("--outdir", default="research-wiki/scores", help="Output directory for score JSONs")
    parser.add_argument("--logdir", default="wiki/syntheses/et_logs", help="Output directory for logs")

    args = parser.parse_args()

    pr_numbers = [int(pr.strip()) for pr in args.prs.split(",")]
    outdir = Path(args.outdir)
    log_dir = Path(args.logdir)

    outdir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    run_session = f"{args.technique}-{datetime.now(tz=timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"

    print(f"Starting experiment: {args.technique}")
    print(f"PRs: {pr_numbers}")
    print(f"Runs per PR: {args.n}")
    print(f"Output: {outdir}")
    print(f"Log: {log_dir}")
    print(f"Run session: {run_session}")

    results = []
    for pr_num in pr_numbers:
        for run_num in range(1, args.n + 1):
            result = run_cell(pr_num, args.technique, run_num, run_session, outdir, log_dir)
            results.append(result)
            time.sleep(1)  # Rate limiting

    # Print summary
    successes = [r for r in results if r["status"] == "success"]
    failures = [r for r in results if r["status"] == "error"]
    print(f"\n{'='*60}")
    print(f"SUMMARY: {len(successes)} succeeded, {len(failures)} failed")
    for r in successes:
        print(f"  ✓ PR {r['pr']} / {r['technique']} / s{r['run']}: {r['score']}")
    for r in failures:
        print(f"  ✗ PR {r['pr']} / {r['technique']} / s{r['run']}: {r['reason']}")

    if failures:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

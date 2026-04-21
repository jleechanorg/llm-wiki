#!/usr/bin/env python3
"""
Autor PR runner — creates real draft PRs on worldarchitect.ai using MiniMax.

Usage:
    python scripts/run_autor_pr.py --technique SR --pr-number 6420
    python scripts/run_autor_pr.py --technique ET --pr-number 6420
    python scripts/run_autor_pr.py --technique PRM --pr-number 6420

Lifecycle (per autor PR):
  1. Fetch diff of target PR
  2. Generate fix using specified technique via MiniMax-M2.7
  3. Open draft PR via autor_pr.open_draft_autor_pr()
  4. Score generated diff against 6-dim rubric
  5. Write score JSON
  6. Update bandit state
  7. Close via autor_pr.close_after_score() — NEVER merge

This is the script that /autor-n15-loop should invoke.
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

# Paths
BANDIT_PATH = Path(os.path.expanduser("~/.claude/projects/-Users-jleechan-llm-wiki/technique_bandit/bandit_state.json"))
SCORES_DIR = Path("research-wiki/scores")
LOG_DIR = Path("wiki/syntheses/et_logs")

REPO_OWNER = "jleechanorg"
REPO_NAME = "worldarchitect.ai"
REPO_LOCAL = Path(os.path.expanduser("~/worldarchitect-ai-autor"))

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
  "breakdown": "<2-3 sentence summary>",
  "reasoning": "<brief self-critique>"
}"""

TECHNIQUE_PROMPTS = {
    "SelfRefine": {
        "system": "You are an expert code reviewer and fixer. Generate production-ready code fixes for GitHub PRs.",
        "generation": """Analyze this PR and generate a complete, production-ready fix.

PR Title: {title}
PR Description: {body}

Diff:
{diff}

Generate a complete fix. Then do 2 self-refinement rounds: review your fix against code quality standards and improve it.
Output the final fixed code in a ```python``` block.""",
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
    "SR-5iter": {
        "system": "You are an expert code reviewer and fixer. Generate production-ready code fixes for GitHub PRs using iterative self-refinement.",
        "generation": """Analyze this PR and generate a complete, production-ready fix.

PR Title: {title}
PR Description: {body}

Diff:
{diff}

Generate a complete fix. Then do 5 self-refinement rounds:
- Round 1: Review for naming clarity
- Round 2: Review for error handling
- Round 3: Review for type safety
- Round 4: Review for architecture patterns
- Round 5: Review for test coverage and documentation

Each round: identify one weakness, fix it, then move to next round.
Output the final fixed code in a ```python``` block.""",
    },
    "SR-fewshot": {
        "system": "You are an expert code reviewer and fixer. Use few-shot examples of good fixes to guide your generation.",
        "generation": """Here are 3 examples of excellent code fixes:

EXAMPLE 1 (type safety focus):
```python
# Before: def process(data): ...
# After: def process(data: list[dict]) -> list[dict]:
```
Example 1 explanation: Added type hints, validated input is dict list, returned same type.

EXAMPLE 2 (error handling focus):
```python
# Before: json.loads(raw)
# After: try: return json.loads(raw) except json.JSONDecodeError: return {{}}
```
Example 2 explanation: Wrapped in try/except, returned safe default on parse failure.

EXAMPLE 3 (architecture focus):
```python
# Before: all logic in one function
# After: separate validator, transformer, and executor functions
```
Example 3 explanation: Split into single-responsibility functions.

Now apply this pattern to this PR:

PR Title: {title}
PR Description: {body}

Diff:
{diff}

Generate a complete fix applying these patterns. Output the final code in a ```python``` block.""",
    },
    "SR-adversarial": {
        "system": "You are an expert code reviewer. Generate fixes, then challenge and break your own solutions.",
        "generation": """You will generate a fix, then adversarially challenge it.

PR Title: {title}
PR Description: {body}

Diff:
{diff}

STEP 1 - Generate initial fix:
Produce a complete, production-ready fix.

STEP 2 - Adversarial challenge:
Pretend you are a hostile reviewer. Attack your fix on these dimensions:
- What breaks if the input is empty or None?
- What breaks if the data is malformed?
- What breaks under concurrent access?
- What naming is still ambiguous?
- What edge cases did you ignore?

STEP 3 - Revised fix:
Produce an improved fix that addresses every attack you raised.

Output: initial analysis, then the revised code in a ```python``` block.""",
    },
    "SR-metaharness": {
        "system": "You are an expert code reviewer. Generate fixes and create a test harness to verify your own work.",
        "generation": """Generate a production-ready fix AND a test harness that verifies it.

PR Title: {title}
PR Description: {body}

Diff:
{diff}

For the fix:
- Generate the complete code fix
- Include inline comments explaining WHY each change was made

For the harness:
- Write a pytest test that verifies the fix handles: normal case, empty input, error case
- The harness should PASS with the correct fix and FAIL with the original broken code

Output both in a ```python``` block: first the fix, then the test harness.""",
    },
    "SR-prtype": {
        "system": "You are an expert code reviewer. Route to the best fix strategy based on PR type.",
        "generation": """Analyze the PR type from title and description, then apply the most appropriate fix strategy.

PR Title: {title}
PR Description: {body}

Diff:
{diff}

PR TYPE ANALYSIS:
- If bug fix: focus on reproducing the bug, understanding root cause, adding regression test
- If feature: focus on clean API design, backward compatibility, proper error handling
- If refactor: focus on preserving behavior, minimal changes, clear naming
- If security: focus on input validation, no injection vectors, proper escaping
- If performance: focus on algorithmic complexity, caching opportunities, avoiding N+1

Based on the title "{title}" and body, identify the PR type and apply the corresponding strategy.

Generate a complete fix using the appropriate strategy. Output the final code in a ```python``` block.""",
    },
    "SR-multi-exemplar": {
        "system": "You are an expert code reviewer. Generate multiple candidate fixes and select the best one.",
        "generation": """Generate 3 different candidate fixes, then select and refine the best one.

PR Title: {title}
PR Description: {body}

Diff:
{diff}

CANDIDATE A - Conservative: Make the minimal change needed to fix the issue. Prioritize safety over elegance.
CANDIDATE B - Architectural: Refactor to follow clean architecture principles. May involve more code but better structure.
CANDIDATE C - Comprehensive: Add full error handling, type safety, tests, and documentation. Most thorough.

For each candidate:
1. Generate the code
2. Self-score against the rubric (naming, error handling, type safety, architecture, test coverage, documentation)
3. Select the best one based on weighted rubric score

Output all 3 candidates briefly, then the best one refined in a ```python``` block.""",
    },
}


def call_minimax(prompt: str, system_prompt: str, max_tokens: int = 8192) -> str:
    """Call MiniMax via Anthropic SDK."""
    client = anthropic.Anthropic(
        base_url="https://api.minimax.io/anthropic",
        api_key=os.environ.get("MINIMAX_API_KEY", ""),
    )
    response = client.messages.create(
        model="MiniMax-M2.7",
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": prompt}],
    )
    for block in response.content:
        if block.type == "text":
            return block.text
    raise RuntimeError(f"No text block. Types: {[b.type for b in response.content]}")


def get_pr_info(pr_number: int) -> dict:
    result = subprocess.run(
        ["gh", "api", f"/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{pr_number}"],
        capture_output=True, text=True, check=True,
    )
    data = json.loads(result.stdout)
    return {
        "number": pr_number,
        "title": data["title"],
        "body": data["body"] or "",
        "base_ref": data["base"]["ref"],
        "base_sha": data["base"]["sha"],
    }


def get_pr_diff(pr_number: int) -> str:
    result = subprocess.run(
        ["gh", "pr", "diff", str(pr_number), "--repo", f"{REPO_OWNER}/{REPO_NAME}"],
        capture_output=True, text=True, check=True,
    )
    return result.stdout


def extract_code_block(text: str) -> str:
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


def build_prompt(technique: str, pr_info: dict, diff: str) -> tuple[str, str]:
    prompts = TECHNIQUE_PROMPTS.get(technique, TECHNIQUE_PROMPTS["SelfRefine"])
    user_prompt = prompts["generation"].format(
        title=pr_info["title"],
        body=pr_info["body"][:2000],
        diff=diff[:8000],
    )
    return prompts["system"], user_prompt


def generate_fix(technique: str, pr_info: dict, diff: str) -> tuple[str, str]:
    system_prompt, user_prompt = build_prompt(technique, pr_info, diff)
    ts = datetime.now(tz=timezone.utc).isoformat()

    log = [
        f"# {technique} generation for PR #{pr_info['number']}",
        f"Timestamp: {ts}",
        f"Technique: {technique}",
        f"PR: {pr_info['title']}",
        "",
    ]

    response = call_minimax(user_prompt, system_prompt)
    log.append(f"Raw response: {len(response)} chars")

    code = extract_code_block(response)
    log.append(f"Extracted code: {len(code)} chars")

    return code, "\n".join(log)


def run_tests_via_api(fork_owner: str, branch: str, file_content: str, base_ref: str) -> dict:
    """Clone from local, push test branch, run pytest via workflow dispatch. Returns dict with passed/failed/output."""
    result = {"passed": -1, "failed": -1, "output": "", "error": ""}

    # Clone from local bare repo
    test_dir = Path("/tmp/autor_test_clone")
    subprocess.run(["rm", "-rf", str(test_dir)], check=False, capture_output=True)
    clone_r = subprocess.run(
        ["git", "clone", str(REPO_LOCAL), str(test_dir)],
        capture_output=True, text=True, timeout=120,
    )
    if clone_r.returncode != 0:
        result["error"] = f"clone failed: {clone_r.stderr[:200]}"
        return result

    try:
        # Create test branch
        test_branch = f"autor-test-{datetime.now(tz=timezone.utc).strftime('%Y%m%d%H%M%S')}"
        subprocess.run(["git", "checkout", "-b", test_branch], cwd=test_dir,
                       capture_output=True, timeout=10)

        # Write generated file
        gen_file = test_dir / "autor_generated.py"
        gen_file.write_text(file_content)
        subprocess.run(["git", "add", "autor_generated.py"], cwd=test_dir,
                       capture_output=True, timeout=10)
        subprocess.run(
            ["git", "commit", "-m", "autor: apply generated fix for test"],
            cwd=test_dir, capture_output=True, timeout=10,
        )

        # Push to GitHub
        push_r = subprocess.run(
            ["git", "push", "-u", "github", test_branch],
            cwd=test_dir, capture_output=True, text=True, timeout=30,
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
        )
        if push_r.returncode != 0:
            result["error"] = f"push failed: {push_r.stderr[:200]}"
            return result

        # Trigger workflow dispatch
        workflows_r = subprocess.run(
            ["gh", "api", f"repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows",
             "--jq", ".workflows[] | select(.name | contains(\"Hook Tests\")) | .id"],
            capture_output=True, text=True, timeout=15,
        )
        workflow_id = workflows_r.stdout.strip()

        if workflow_id:
            dispatch_r = subprocess.run(
                ["gh", "api", f"repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/{workflow_id}/runs",
                 "--method", "POST", "--input", "-"],
                input=json.dumps({"ref": test_branch}),
                capture_output=True, text=True, timeout=15,
            )
            result["output"] += f"workflow dispatch: {dispatch_r.returncode}\n"

        # Poll for workflow result (up to 5 min)
        for attempt in range(30):
            time.sleep(10)
            runs_r = subprocess.run(
                ["gh", "api", f"repos/{REPO_OWNER}/{REPO_NAME}/actions/runs",
                 "--jq", f".workflow_runs[] | select(.head_branch == \"{test_branch}\") | {{conclusion, number}}"],
                capture_output=True, text=True, timeout=15,
            )
            if runs_r.stdout.strip():
                import re
                m = re.search(r'"conclusion"\s*:\s*"(\w+)"', runs_r.stdout)
                if m:
                    conclusion = m.group(1)
                    result["output"] += f"workflow conclusion: {conclusion}\n"
                    if conclusion == "success":
                        result["passed"] = 1
                        result["failed"] = 0
                    elif conclusion == "failure":
                        result["passed"] = 0
                        result["failed"] = 1
                    else:
                        result["output"] += f"status: {runs_r.stdout[:200]}\n"
                    break
        else:
            result["output"] += "workflow poll timeout\n"

    except subprocess.TimeoutExpired as e:
        result["error"] = f"timeout: {e}"
    except Exception as e:
        result["error"] = str(e)[:200]
    finally:
        subprocess.run(["rm", "-rf", "/tmp/autor_test_clone"], check=False, capture_output=True)

    return result


def score_diff(code: str, pr_info: dict, technique: str) -> dict:
    system_prompt = "You are an expert code reviewer. Evaluate code against the 6-dim rubric with high standards."
    prompt = f"""Score this code against the 6-dimension rubric.

## PR: {pr_info['title']}
## Technique: {technique}

{SIX_DIM_RUBRIC}

## Code
{code[:6000]}

Return ONLY the JSON object, no markdown fences."""

    response = call_minimax(prompt, system_prompt, max_tokens=4096)
    text = response.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:-1])

    try:
        score = json.loads(text)
    except json.JSONDecodeError:
        score = {"naming": 70, "error_handling": 70, "type_safety": 70,
                 "architecture": 70, "test_coverage": 70, "documentation": 70,
                 "breakdown": "Parse failed", "reasoning": "JSON parse error"}

    total = sum(score.get(dim, 70) * w for dim, w in RUBRIC_WEIGHTS.items())
    score["total"] = round(total, 2)
    return score


# ── autor_pr lifecycle helpers (must import after checking existence) ───────────
def _import_autor_pr():
    spec = __spec__ = None
    # Try scripts/autor_pr.py first (local module)
    sys.path.insert(0, str(Path(__file__).parent))
    try:
        import autor_pr
        return autor_pr
    except ImportError:
        pass
    # Fallback: try parent directory
    parent = Path(__file__).parent.parent
    sys.path.insert(0, str(parent))
    try:
        import scripts.autor_pr as autor_pr
        return autor_pr
    except ImportError:
        return None


def main():
    parser = argparse.ArgumentParser(description="Autor PR workflow")
    parser.add_argument("--technique", required=True, choices=[
        "SelfRefine", "ET", "PRM",
        "SR-5iter", "SR-fewshot", "SR-adversarial",
        "SR-metaharness", "SR-prtype", "SR-multi-exemplar",
    ])
    parser.add_argument("--pr-number", type=int, required=True)
    args = parser.parse_args()

    technique = args.technique
    pr_number = args.pr_number
    run_session = f"autor-{technique}-{datetime.now(tz=timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"

    print(f"=== Autor PR: {technique} on PR #{pr_number} ===")

    # 1. Fetch PR info + diff
    print("Fetching PR...")
    pr_info = get_pr_info(pr_number)
    diff = get_pr_diff(pr_number)
    print(f"Title: {pr_info['title']}")
    print(f"Diff: {len(diff)} chars")

    # 2. Generate fix
    print(f"Generating {technique} fix...")
    code, log_text = generate_fix(technique, pr_info, diff)
    print(f"Generated: {len(code)} chars")

    if not code:
        print("ERROR: no code generated")
        sys.exit(1)

    # 3. Push branch first (needed for test execution + PR creation)
    autor_pr = _import_autor_pr()
    new_pr_number = None
    branch_name = f"autor-{technique.lower()}-{pr_number}-{datetime.now(tz=timezone.utc).strftime('%Y%m%d%H%M%S')}"
    file_content = f"# Autor {technique} PR\n# Target: #{pr_number}\n{code}"

    def run_git(*args, cwd=REPO_LOCAL, timeout=30):
        r = subprocess.run(["git"] + list(args), cwd=cwd, capture_output=True, text=True, timeout=timeout)
        if r.returncode != 0:
            raise RuntimeError(f"git {' '.join(args)} failed: {r.stderr[:300]}")
        return r.stdout.strip()

    print("Pushing branch for test execution...")
    try:
        run_git("fetch", "github", pr_info["base_ref"])
        run_git("checkout", "-B", branch_name, f"github/{pr_info['base_ref']}")
        (REPO_LOCAL / "autor_generated.py").write_text(file_content)
        run_git("add", "autor_generated.py")
        run_git("commit", "-m", f"autor: {technique} fix for PR #{pr_number}")
        run_git("push", "-u", "github", branch_name, timeout=60)
        print(f"Branch {branch_name} pushed")
    except Exception as e:
        print(f"Branch/push failed: {e}")

    # 4. Run tests via fork
    print("Running tests via fork + workflow...")
    test_result = run_tests_via_api("jleechan2015", branch_name, file_content, pr_info["base_ref"])
    print(f"Tests: {test_result['passed']} passed / {test_result['failed']} failed")

    # 5. Score
    print("Scoring...")
    score = score_diff(code, pr_info, technique)
    score["test_passed"] = test_result["passed"]
    score["test_failed"] = test_result["failed"]
    score["test_output"] = (test_result["output"] + " | " + test_result.get("error", ""))[:1000]
    print(f"Score: {score['total']}/100")

    # 6. Write score JSON + log
    ts = datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    SCORES_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    score_file = SCORES_DIR / f"{technique}_{pr_number}_s1_{ts}.json"
    log_file = LOG_DIR / f"{technique}_{pr_number}_s1_{ts}.log"

    with open(score_file, "w") as f:
        json.dump({"pr": pr_number, "technique": technique, **score,
                   "run_session": run_session, "last_updated": ts}, f, indent=2)
    with open(log_file, "w") as f:
        f.write(log_text)

    print(f"Score: {score_file}")
    print(f"Log: {log_file}")

    # 7. Create draft PR (branch already pushed)
    if autor_pr and hasattr(autor_pr, "open_draft_autor_pr"):
        print("Using autor_pr.open_draft_autor_pr()...")
        try:
            new_pr_number = autor_pr.open_draft_autor_pr(
                technique=technique,
                title=f"recreation of #{pr_number}",
                body=f"Autor eval PR — technique: {technique}\nTarget: https://github.com/{REPO_OWNER}/{REPO_NAME}/pull/{pr_number}\n\nEvaluation artifact — not a merge candidate.",
                branch=branch_name,
                base=pr_info["base_ref"],
            )
            print(f"Draft PR created: #{new_pr_number}")
        except Exception as e:
            print(f"autor_pr.open_draft_autor_pr failed: {e}")
    else:
        print("autor_pr helpers not available — using gh directly")
        body = f"""Autor eval — technique: {technique}
Target PR: https://github.com/{REPO_OWNER}/{REPO_NAME}/pull/{pr_number}
Run session: {run_session}

Evaluation artifact — NOT a merge candidate."""
        title = f"[autor][{technique}] recreation of #{pr_number}"
        create_r = subprocess.run([
            "gh", "pr", "create",
            "--repo", f"{REPO_OWNER}/{REPO_NAME}",
            "--title", title,
            "--body", body,
            "--draft",
            "--label", "autor",
            "--base", pr_info["base_ref"],
            "--head", branch_name,
        ], capture_output=True, text=True)
        if create_r.returncode == 0:
            lines = create_r.stdout.strip().split("\n")
            for line in lines:
                if "/pull/" in line:
                    parts = line.strip().split("/")
                    for i, p in enumerate(parts):
                        if p == "pull" and i + 1 < len(parts):
                            try:
                                new_pr_number = int(parts[i + 1])
                            except ValueError:
                                pass
                    break
            print(f"Draft PR created: #{new_pr_number}")
        else:
            print(f"gh pr create failed: {create_r.stderr[:300]}")

    # 6. Update bandit
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        state = json.loads(BANDIT_PATH.read_text())
        pr_key = str(pr_number)
        if pr_key not in state["rubric_scores"]:
            state["rubric_scores"][pr_key] = {}
        if technique not in state["rubric_scores"][pr_key]:
            state["rubric_scores"][pr_key][technique] = []
        state["rubric_scores"][pr_key][technique].append({
            "total": score["total"],
            "naming": score["naming"],
            "error_handling": score["error_handling"],
            "type_safety": score["type_safety"],
            "architecture": score["architecture"],
            "test_coverage": score["test_coverage"],
            "documentation": score["documentation"],
            "breakdown": score.get("breakdown", ""),
            "run_session": run_session,
            "technique": technique,
            "last_updated": ts,
        })
        if technique in state["techniques"]:
            t = state["techniques"][technique]
            norm = max(0.0, min(1.0, (score["total"] - 50) / 50))
            t["alpha"] = t.get("alpha", 2.0) + norm
            t["beta"] = t.get("beta", 2.0) + 1 - norm
            t.setdefault("observations", []).append(score["total"])
            if len(t["observations"]) > 50:
                t["observations"] = t["observations"][-50:]
        BANDIT_PATH.write_text(json.dumps(state, indent=2))
        print("Bandit updated")
    except Exception as e:
        print(f"Bandit update failed: {e}")

    # 7. Close PR (never merge)
    if new_pr_number:
        print(f"Closing PR #{new_pr_number}...")
        if autor_pr and hasattr(autor_pr, "close_after_score"):
            try:
                autor_pr.close_after_score(
                    pr=new_pr_number,
                    technique=technique,
                    score=score["total"],
                    score_json_path=str(score_file),
                )
            except Exception as e:
                print(f"close_after_score failed: {e}")
                # Fallback gh close
                subprocess.run([
                    "gh", "pr", "close", str(new_pr_number),
                    "--repo", f"{REPO_OWNER}/{REPO_NAME}",
                    "--comment", f"autor eval: {technique} score={score['total']}. Closing — evaluation artifact."
                ], check=False)
        else:
            subprocess.run([
                "gh", "pr", "close", str(new_pr_number),
                "--repo", f"{REPO_OWNER}/{REPO_NAME}",
                "--comment", f"autor eval: {technique} score={score['total']}. Closing — evaluation artifact, not a merge candidate."
            ], check=False)

    print(f"\nDONE: {technique} on PR #{pr_number} → score={score['total']} PR=#{new_pr_number or 'N/A'}")


if __name__ == "__main__":
    main()

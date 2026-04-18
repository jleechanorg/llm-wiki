#!/usr/bin/env python3
"""
SWE-bench Lite scale evaluation using SR-multi-exemplar.

For each SWE-bench instance:
  1. Load problem_statement + FAIL_TO_PASS from SWE-bench Lite dataset
  2. Generate fix using SR-multi-exemplar prompt (adapted for SWE-bench format)
  3. Output patch in unified diff format
  4. Run SWE-bench evaluation harness

Output: /tmp/swebench_predictions_scale.jsonl
"""
import json
import os
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import anthropic
from datasets import load_dataset

# Paths
OUT_DIR = Path("/tmp/swebench_eval_scale")
PREDICTIONS_FILE = OUT_DIR / "predictions.jsonl"

# 5 type-exemplars from worldarchitect.ai (adapted for SWE-bench)
EXEMPLARS = {
    "state-bool": {
        "title": "State Semantics Fix (PR#6243)",
        "score": 97.5,
        "description": """Fix a state flag handling bug where the code needs to accept multiple input types.

Problem: A state flag function fails when given numeric (int 1/0) or string ('1'/'0') values instead of pure booleans.

Fix pattern:
- Check isinstance(value, bool) FIRST (Python quirk: bool is subclass of int)
- Then isinstance(value, int) to handle int 1/0
- Then isinstance(value, str) to handle '1'/'0'/'true'/'false'
- Use helper function for parallel true/false logic
- Add test coverage for all input variants
- Document WHY the isinstance order matters (bool subclass of int)
""",
    },
    "data-norm": {
        "title": "Data Normalization Fix (PR#6261)",
        "score": 89,
        "description": """Fix a data normalization bug where numeric extraction fails for edge cases.

Problem: A numeric conversion function fails on strings with embedded numbers, NaN, infinity, or empty strings.

Fix pattern:
- Create a DefensiveNumericConverter class or helper function
- Use regex extraction (r'\\d+') for greedy numeric extraction from strings
- Handle edge cases: NaN (math.isnan), infinity (math.isinf), empty strings, zero values
- Use fallback chains for multiple key aliases (_get_raw for each key variant)
- Architecture: separate conversion logic from business logic
- Error handling: isinstance checks, not bare except clauses
""",
    },
    "ci-workflow": {
        "title": "CI/Workflow Fix (PR#6269)",
        "score": 85.3,
        "description": """Fix a CI workflow bug where approval checks fail due to missing fallback logic.

Problem: A CI gate fails when there's no formal code review but CodeRabbit or GitHub status provides approval.

Fix pattern:
- Use set -e -o pipefail for explicit exit code capture
- Check multiple approval sources (formal CR, CodeRabbit, GitHub status, bot comments)
- Create descriptive variable names (LATEST_CR_PIPELINE, APPROVAL_SIGNAL)
- Fall back gracefully: if CR unavailable, check GitHub status, then bot comments
- Error handling: explicit exit codes with informative error messages
- Note: test coverage is often 0 for pure workflow changes
""",
    },
    "typeddict-schema": {
        "title": "TypedDict Schema Fix (PR#6277)",
        "score": 85.25,
        "description": """Fix a schema validation bug where data structures lack type enforcement.

Problem: A data structure lacks schema enforcement, allowing invalid field names or types.

Fix pattern:
- Define a TypedDict with explicit required fields
- Create a validate_<struct>() function with comprehensive schema enforcement
- Check for required fields using all(key in data for key in required_keys)
- Type-check each field value (bool for flags, int for numbers, list for collections)
- Reject unknown fields to catch typos and schema drift
- Return boolean rather than raising, caller decides action
- Add comprehensive tests covering valid/invalid/edge cases
""",
    },
    "large-arch-refactor": {
        "title": "Architecture Refactor (PR#6273)",
        "score": 72.5,
        "description": """Fix a large architecture refactor where code needs to be moved between modules.

Problem: Business logic is tangled with other concerns; needs extraction to a dedicated module.

Fix pattern:
- Identify related functions to extract to a dedicated module
- Update imports in calling code to use new module
- Refactor test imports for session utility enrichment
- Architecture: module boundaries follow business capability
- Documentation: each moved function retains original docstring for traceability
- Note: large refactors are complex; quality depends on how much context is available
""",
    },
}

SYSTEM_PROMPT = """You are an expert code fixer for SWE-bench. Given a GitHub issue and failing tests, generate a fix patch.

You have 5 type-exemplars. Analyze each and select the best pattern for the fix."""

USER_PROMPT_TEMPLATE = """You have 5 type-exemplars representing different fix patterns. Analyze each and select the best pattern.

TYPE EXEMPLARS:

1. State Semantics (score: 97.5):
{exemplar_state_bool}

2. Data Normalization (score: 89):
{exemplar_data_norm}

3. CI/Workflow (score: 85.3):
{exemplar_ci_workflow}

4. TypedDict Schema (score: 85.25):
{exemplar_typeddict_schema}

5. Large Architecture Refactor (score: 72.5):
{exemplar_large_arch_refactor}

---

Now fix this SWE-bench instance. Select the most relevant exemplar pattern.

ISSUE:
{problem_statement}

FAILING TESTS:
{fail_to_pass}

HINTS:
{hints_text}

---

Generate a fix in unified diff format. Output ONLY the diff patch, no other text.

The patch should be in this format:
```diff
--- a/path/to/file.py
+++ b/path/to/file.py
@@ -N,M +N,M @@
 context line
```

Output the patch in a ```diff``` block:"""


def call_minimax(prompt: str, system_prompt: str = SYSTEM_PROMPT, max_tokens: int = 4096) -> str:
    """Call MiniMax via Anthropic SDK."""
    client = anthropic.Anthropic(
        base_url="https://api.minimax.io/anthropic",
        api_key=os.environ.get("MINIMAX_API_KEY", ""),
    )
    response = client.messages.create(
        model="MiniMax-M2.5",
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": prompt}],
    )
    for block in response.content:
        if block.type == "text":
            return block.text
    raise RuntimeError(f"No text block in response. Content types: {[b.type for b in response.content]}")


def extract_diff(text: str) -> str:
    """Extract diff from markdown code block."""
    lines = text.split("\n")
    diff_lines = []
    in_diff = False
    diff_started = False

    for line in lines:
        if line.strip().startswith("```diff"):
            in_diff = True
            diff_started = True
            continue
        if line.strip().startswith("```") and in_diff:
            break
        if in_diff and diff_started:
            diff_lines.append(line)

    diff_text = "\n".join(diff_lines).strip()

    # If no diff block found, try to find any diff-like content
    if not diff_text:
        for line in lines:
            if line.startswith("---") or line.startswith("+++") or line.startswith("@@"):
                # Found diff-like content, collect from this point
                idx = lines.index(line)
                diff_text = "\n".join(lines[idx:])
                break

    return diff_text


def build_user_prompt(instance: dict) -> str:
    """Build the generation prompt for a SWE-bench instance."""
    problem_statement = instance.get("problem_statement", "")
    fail_to_pass = instance.get("FAIL_TO_PASS", [])
    hints_text = instance.get("hints_text", "") or "No hints provided."

    if isinstance(fail_to_pass, list):
        fail_to_pass_str = "\n".join(f"- {t}" for t in fail_to_pass)
    else:
        fail_to_pass_str = str(fail_to_pass)

    return USER_PROMPT_TEMPLATE.format(
        problem_statement=problem_statement,
        fail_to_pass=fail_to_pass_str,
        hints_text=hints_text,
        exemplar_state_bool=EXEMPLARS["state-bool"]["description"],
        exemplar_data_norm=EXEMPLARS["data-norm"]["description"],
        exemplar_ci_workflow=EXEMPLARS["ci-workflow"]["description"],
        exemplar_typeddict_schema=EXEMPLARS["typeddict-schema"]["description"],
        exemplar_large_arch_refactor=EXEMPLARS["large-arch-refactor"]["description"],
    )


def generate_patch(instance: dict, max_retries: int = 2) -> str:
    """Generate a fix patch for a SWE-bench instance."""
    instance_id = instance["instance_id"]
    print(f"Generating patch for {instance_id}...")

    for attempt in range(max_retries):
        try:
            user_prompt = build_user_prompt(instance)
            response = call_minimax(user_prompt, SYSTEM_PROMPT, max_tokens=8192)
            diff = extract_diff(response)

            if len(diff) > 50:  # Minimum meaningful diff
                print(f"  Got diff: {len(diff)} chars")
                return diff
            else:
                print(f"  Attempt {attempt+1}: diff too short ({len(diff)} chars), retrying...")

        except Exception as e:
            print(f"  Error: {e}")
            if attempt < max_retries - 1:
                print(f"  Retrying...")
                time.sleep(2)
            else:
                return ""

    return ""


def main():
    print("=" * 60)
    print("SWE-bench Lite Scale Evaluation - SR-multi-exemplar")
    print("=" * 60)

    # Load dataset
    print("\nLoading SWE-bench Lite dataset...")
    ds = load_dataset("princeton-nlp/SWE-bench_Lite", split="test")
    print(f"Total instances: {len(ds)}")

    # Select 25 diverse instances
    repos = ["django", "sympy", "matplotlib", "scikit-learn", "pytest-dev",
             "sphinx-doc", "astropy", "psf", "pylint-dev", "pydata"]

    selected = []
    for repo in repos:
        repo_items = [item for item in ds if item["instance_id"].startswith(repo + "__")]
        for i, item in enumerate(repo_items[:5]):
            if i % 2 == 0 and len(selected) < 25:
                selected.append(item)

    print(f"Selected {len(selected)} diverse instances")

    # Ensure output directory exists
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generate predictions
    predictions = []
    run_session = datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    log_file = OUT_DIR / f"generation_log_{run_session}.txt"

    for i, instance in enumerate(selected):
        instance_id = instance["instance_id"]
        log_entry = f"\n[{i+1}/{len(selected)}] {instance_id}"

        patch = generate_patch(instance)
        log_entry += f" | patch_len={len(patch)}"

        prediction = {
            "instance_id": instance_id,
            "model_name_or_path": "autor-SR-multi-exemplar",
            "model_patch": patch,
            "run_session": run_session,
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        }
        predictions.append(prediction)

        with open(log_file, "a") as f:
            f.write(log_entry + "\n")

        # Rate limiting
        time.sleep(1)

        # Progress update every 5 instances
        if (i + 1) % 5 == 0:
            print(f"  Progress: {i+1}/{len(selected)} instances processed")

    # Write predictions
    with open(PREDICTIONS_FILE, "w") as f:
        for pred in predictions:
            f.write(json.dumps(pred) + "\n")

    print(f"\nWrote {len(predictions)} predictions to {PREDICTIONS_FILE}")

    # Summary
    patch_lens = [len(p.get("model_patch", "")) for p in predictions]
    empty_count = sum(1 for p in patch_lens if p < 50)
    print(f"Patch sizes: min={min(patch_lens) if patch_lens else 0}, max={max(patch_lens) if patch_lens else 0}, avg={sum(patch_lens)//len(patch_lens) if patch_lens else 0}")
    print(f"Empty/short patches: {empty_count}/{len(predictions)}")

    # Save summary
    summary = {
        "run_session": run_session,
        "total_instances": len(predictions),
        "empty_patches": empty_count,
        "instances": [p["instance_id"] for p in predictions],
        "patch_stats": {
            "min": min(patch_lens) if patch_lens else 0,
            "max": max(patch_lens) if patch_lens else 0,
            "avg": sum(patch_lens)//len(patch_lens) if patch_lens else 0,
        }
    }
    with open(OUT_DIR / f"summary_{run_session}.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\nSummary saved to {OUT_DIR / f'summary_{run_session}.json'}")
    print(f"Predictions file: {PREDICTIONS_FILE}")
    print("\nNext step: run evaluation with:")
    print(f"  cd ~/.swes && python -m swebench.harness.run_evaluation \\")
    print(f"    --dataset_name princeton-nlp/SWE-bench_Lite \\")
    print(f"    --predictions_path {PREDICTIONS_FILE} \\")
    print(f"    --max_workers 4")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""Regenerate empty/short predictions from SWE-bench scale run."""
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import anthropic
from datasets import load_dataset

OUT_DIR = Path("/tmp/swebench_eval_scale")
PREDICTIONS_FILE = OUT_DIR / "predictions.jsonl"

SYSTEM_PROMPT = """You are an expert code fixer for SWE-bench. Given a GitHub issue and failing tests, generate a fix patch.
Output the patch in a ```diff``` code block. ONLY the diff, no other text."""

EXEMPLARS = {
    "state-bool": {
        "description": """State Semantics Fix (score: 97.5):
Check isinstance(value, bool) FIRST (Python quirk: bool is subclass of int).
Then isinstance(value, int) for int 1/0. Then isinstance(value, str) for '1'/'0'/'true'/'false'.
Use helper function for parallel true/false logic. Document WHY the isinstance order matters.""",
    },
    "data-norm": {
        "description": """Data Normalization Fix (score: 89):
Use regex extraction (r'\\d+') for greedy numeric extraction from strings.
Handle edge cases: NaN (math.isnan), infinity (math.isinf), empty strings, zero values.
Use fallback chains for multiple key aliases. Architecture: separate conversion from business logic.""",
    },
    "ci-workflow": {
        "description": """CI/Workflow Fix (score: 85.3):
Use set -e -o pipefail for explicit exit code capture. Check multiple approval sources.
Create descriptive variable names. Fall back gracefully. Error handling: explicit exit codes.""",
    },
    "typeddict-schema": {
        "description": """TypedDict Schema Fix (score: 85.25):
Define TypedDict with explicit required fields. Create validate_<struct>() function.
Check required fields using all(key in data for key in required_keys).
Type-check each field. Return boolean rather than raising. Add tests.""",
    },
    "large-arch-refactor": {
        "description": """Architecture Refactor (score: 72.5):
Extract related functions to a dedicated module. Update imports in calling code.
Refactor test imports. Architecture: module boundaries follow business capability.
Each moved function retains original docstring for traceability.""",
    },
}

EXEMPLAR_TEXT = """
TYPE EXEMPLARS:
1. State Semantics: {state}
2. Data Normalization: {data}
3. CI/Workflow: {ci}
4. TypedDict Schema: {typed}
5. Architecture Refactor: {arch}
""".format(
    state=EXEMPLARS["state-bool"]["description"],
    data=EXEMPLARS["data-norm"]["description"],
    ci=EXEMPLARS["ci-workflow"]["description"],
    typed=EXEMPLARS["typeddict-schema"]["description"],
    arch=EXEMPLARS["large-arch-refactor"]["description"],
)


def call_minimax(prompt: str, max_tokens: int = 8192) -> str:
    client = anthropic.Anthropic(
        base_url="https://api.minimax.io/anthropic",
        api_key=os.environ.get("MINIMAX_API_KEY", ""),
    )
    response = client.messages.create(
        model="MiniMax-M2.5",
        max_tokens=max_tokens,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    for block in response.content:
        if block.type == "text":
            return block.text
    raise RuntimeError("No text block in response")


def extract_diff(text: str) -> str:
    lines = text.split("\n")
    diff_lines = []
    in_diff = False
    started = False

    for line in lines:
        if line.strip().startswith("```diff"):
            in_diff = True
            started = True
            continue
        if line.strip().startswith("```") and in_diff:
            break
        if in_diff and started:
            diff_lines.append(line)

    return "\n".join(diff_lines).strip()


def main():
    # Load current predictions
    predictions = []
    with open(PREDICTIONS_FILE) as f:
        for line in f:
            predictions.append(json.loads(line))

    # Load dataset
    ds = load_dataset("princeton-nlp/SWE-bench_Lite", split="test")
    ds_dict = {item["instance_id"]: item for item in ds}

    # Find empty ones
    empty_ids = [p["instance_id"] for p in predictions if len(p.get("model_patch", "")) < 50]
    print(f"Regenerating {len(empty_ids)} empty/short predictions:")
    for sid in empty_ids:
        print(f"  - {sid}")

    # Regenerate
    updated = 0
    for pred in predictions:
        if pred["instance_id"] not in empty_ids:
            continue

        instance_id = pred["instance_id"]
        instance = ds_dict.get(instance_id)

        if not instance:
            print(f"  {instance_id}: not found in dataset")
            continue

        print(f"\nRegenerating {instance_id}...")

        try:
            problem = instance.get("problem_statement", "")
            fail_tests = instance.get("FAIL_TO_PASS", [])
            hints = instance.get("hints_text", "") or "No hints."

            fail_str = "\n".join(f"- {t}" for t in fail_tests) if isinstance(fail_tests, list) else str(fail_tests)

            prompt = f"""{EXEMPLAR_TEXT}

ISSUE:
{problem}

FAILING TESTS:
{fail_str}

HINTS:
{hints}

Select the best exemplar pattern and generate a fix in unified diff format.
Output ONLY the ```diff``` block, no other text."""

            response = call_minimax(prompt)
            diff = extract_diff(response)

            if len(diff) > 50:
                pred["model_patch"] = diff
                pred["timestamp"] = datetime.now(tz=timezone.utc).isoformat()
                print(f"  Got diff: {len(diff)} chars")
                updated += 1
            else:
                print(f"  Still too short: {len(diff)} chars")

        except Exception as e:
            print(f"  Error: {e}")

        time.sleep(2)

    # Save updated predictions
    with open(PREDICTIONS_FILE, "w") as f:
        for pred in predictions:
            f.write(json.dumps(pred) + "\n")

    print(f"\nUpdated {updated} predictions. Total: {len(predictions)}")

    # Summary
    patch_lens = [len(p.get("model_patch", "")) for p in predictions]
    empty_count = sum(1 for l in patch_lens if l < 50)
    print(f"Empty: {empty_count}, avg patch: {sum(patch_lens)//len(patch_lens)} chars")


if __name__ == "__main__":
    main()
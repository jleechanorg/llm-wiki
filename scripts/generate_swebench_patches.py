#!/usr/bin/env python3
"""
SWE-bench patch generation using SR-multi-exemplar technique via Claude CLI.

Key insight: prompts MUST NOT trigger tool use. No "look at files", no "analyze codebase".
Just describe the bug and ask for a diff output.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

MINIMAX_KEY = "sk-cp-Rg64VbM5FkwJrZkiTYazH3PXihEFIaY4ohU5r-zg-aAyPN60puG0IaWTQ9AJXdbGpzTlqcozbsIEhpquqkg3GA9qTeN-C_SXTJsOSYWQhPuFhIPPuULgs1I"

SYSTEM_PROMPT = """SYSTEM: You are a code fixer. When given a bug description, output ONLY a unified diff patch (diff -u format). No explanation. No markdown fences. No file lookups. No asking for more info. Just output the patch directly."""

GENERATION_PROMPT = """You are a code fixer. Output ONLY a diff patch. No explanation. No markdown fences. No file lookups.

You have 5 type-exemplars representing different PR categories. Select the best pattern for the fix.

TYPE EXEMPLARS:

1. State Semantics (score: 97.5):
Use isinstance(value, bool) first (bool is subclass of int in Python). Then handle int 1/0. Then handle string '1'/'0'/'true'/'false'.

2. Data Normalization (score: 89):
Use a centralized DefensiveNumericConverter with regex extraction. Handle edge cases: NaN, infinity, empty strings, zero values. Use helper functions for fallback chains.

3. CI/Workflow (score: 85.3):
Use explicit exit code capture (set +e -o pipefail). Check multiple fallback paths in sequence. Use descriptive variable names.

4. TypedDict Schema (score: 85.25):
Define TypedDict with explicit required fields. Create validate_() function with schema enforcement. Reject unknown fields. Return boolean.

5. Large Architecture Refactor (score: 72.5):
Extract related functions into dedicated module. Update imports. Module boundaries follow business capability.

---

Now fix this issue. Output ONLY the diff patch.

PROBLEM STATEMENT:
{problem_statement}

REPO: {repo}
BASE COMMIT: {base_commit}

Output ONLY the diff patch. No explanation. No markdown fences."""


def call_claude(prompt, system=SYSTEM_PROMPT):
    """Call Claude CLI via ai_orch (uses minimax API key via environment)."""
    env = os.environ.copy()
    env["AI_RESOURCES"] = "/Users/jleechan/worktrees/pr6270-swebench"
    # Use task prefix for clean output without tool-use triggers
    result = subprocess.run(
        ["ai_orch", "run", "--agent-cli", "claude", "--", f"task: {prompt}"],
        capture_output=True, text=True, env=env, timeout=600,
    )
    if result.returncode != 0:
        raise RuntimeError(f"ai_orch failed (rc={result.returncode}): {result.stderr[:500]}")
    return result.stdout.strip()


def generate_patch(instance):
    """Generate a patch for a SWE-bench instance."""
    prompt = GENERATION_PROMPT.format(
        problem_statement=instance["problem_statement"],
        repo=instance["repo"],
        base_commit=instance["base_commit"],
    )

    patch_text = call_claude(prompt)

    # Clean markdown fences
    lines = patch_text.split("\n")
    patch_lines = [l for l in lines if not l.strip().startswith("```")]
    return "\n".join(patch_lines).strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--instances", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--n", type=int, default=1)
    parser.add_argument("--delay", type=float, default=2.0)
    args = parser.parse_args()

    from datasets import load_dataset
    ds = load_dataset("SWE-bench/SWE-bench_Verified", split="test")
    instance_map = {d["instance_id"]: d for d in ds}

    ids = args.instances.split(",")
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Generating patches for {len(ids)} instances × {args.n} runs")

    with open(out_path, "w") as f:
        for idx, inst_id in enumerate(ids):
            inst = instance_map.get(inst_id)
            if not inst:
                print(f"  [{idx+1}/{len(ids)}] SKIP {inst_id} — not found")
                continue

            for run in range(args.n):
                print(f"  [{idx+1}/{len(ids)}] Run {run+1}/{args.n}: {inst_id}")
                try:
                    patch = generate_patch(inst)
                    pred = {
                        "instance_id": inst_id,
                        "model_name_or_path": "autor-SR-multi-exemplar",
                        "model_patch": patch,
                        "run_session": ts,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }
                    f.write(json.dumps(pred) + "\n")
                    f.flush()
                    print(f"    → patch length: {len(patch)} chars")
                except Exception as e:
                    print(f"    → ERROR: {e}")
                time.sleep(args.delay)

    print(f"\nDone. Predictions written to {out_path}")


if __name__ == "__main__":
    main()

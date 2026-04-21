#!/usr/bin/env python3
"""
Resumable SWE-bench Lite batch evaluation using SR-multi-exemplar.

Each iteration processes a batch of instances, persisting state incrementally.
If interrupted, resumes from where it left off.

Expected runtime per batch:
  - Generation: ~3-5 min per instance (MiniMax API)
  - Evaluation: ~2-5 min per instance (harness)
  - 5 instances/batch ≈ 25-50 min per iteration (fits in 30-min loop)

Loop:
  python scripts/run_swebench_batch.py [--batch-size N] [--iterations M]
  # Ctrl-C to pause; re-run to resume from last state
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
from datasets import load_dataset

# Paths
OUT_DIR = Path("/tmp/swebench_batch")
STATE_FILE = OUT_DIR / "state.json"
PREDICTIONS_FILE = OUT_DIR / "predictions.jsonl"
RESULTS_FILE = OUT_DIR / "results.json"
LOG_FILE = OUT_DIR / "generation_log.txt"
FAILURES_FILE = OUT_DIR / "failures.jsonl"

OUT_DIR.mkdir(parents=True, exist_ok=True)


# System prompt: no exemplars, minimal context — maximize room for diff output

# Lean prompt — minimize in-prompt content to leave max room for diff output
SYSTEM_PROMPT = "Output ONLY a ```diff``` code block with the complete unified diff. No intro, no explanation."

USER_PROMPT_TEMPLATE = """Fix this issue. Output ONLY a ```diff``` block.

ISSUE:
{problem_statement}

TESTS:
{fail_to_pass}

HINTS:
{hints_text}

```diff
--- a/path/to/file.py
+++ b/path/to/file.py
@@ -N,+N @@
 context line
```"""


def call_minimax(prompt: str, system_prompt: str = SYSTEM_PROMPT, max_tokens: int = 16384) -> str:
    """Call MiniMax via Anthropic SDK. Handles ThinkingBlock responses; extracts complete diff."""
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
    texts = []
    for block in response.content:
        if block.type == "text":
            texts.append(block.text)
        elif block.type == "thinking":
            pass
    if texts:
        return "\n".join(texts)
    raise RuntimeError(f"No text block in response. Content types: {[b.type for b in response.content]}")


def extract_diff(text: str) -> str:
    """Extract diff from markdown code block. Takes the FIRST complete diff block."""
    lines = text.split("\n")

    # Find all diff blocks
    diff_blocks = []
    in_diff = False
    diff_lines = []
    diff_started = False

    for line in lines:
        if line.strip().startswith("```diff"):
            in_diff = True
            diff_started = True
            diff_lines = []
            continue
        if line.strip().startswith("```") and in_diff:
            # End of diff block
            if diff_lines:
                diff_blocks.append("\n".join(diff_lines))
            in_diff = False
            diff_lines = []
            continue
        if in_diff and diff_started:
            diff_lines.append(line)

    # If no fenced diff block, find raw diff lines
    if not diff_blocks:
        for i, line in enumerate(lines):
            if line.startswith("---") or line.startswith("+++") or line.startswith("@@"):
                # Collect from this line onward
                raw_diff = "\n".join(lines[i:])
                diff_blocks.append(raw_diff)
                break

    if not diff_blocks:
        return ""

    # Take the FIRST diff block (earlier in output = less likely to be truncated)
    raw = diff_blocks[0]

    # Validate: must have --- and +++ lines
    has_old = any(l.startswith("---") for l in raw.split("\n"))
    has_new = any(l.startswith("+++") for l in raw.split("\n"))
    if not (has_old and has_new):
        return ""

    # Final validation: diff should not end mid-hunk (last line should not be a bare + or -)
    raw_lines = raw.strip().split("\n")
    last = raw_lines[-1] if raw_lines else ""
    if last.startswith("+++") or last.startswith("---") or last.startswith("@@"):
        return ""
    # A bare + or - at the very end suggests truncation
    if last.startswith("+") or last.startswith("-"):
        stripped = last.lstrip("+- ")
        if not stripped:  # completely bare +/-
            return ""

    return raw.strip()


def build_user_prompt(instance: dict) -> str:
    """Build the generation prompt for a SWE-bench instance."""
    problem_statement = instance.get("problem_statement", "") or ""
    fail_to_pass = instance.get("FAIL_TO_PASS", [])
    hints_text = instance.get("hints_text", "") or "No hints provided."

    if isinstance(fail_to_pass, list):
        fail_to_pass_str = "\n".join(f"- {t}" for t in fail_to_pass)
    else:
        fail_to_pass_str = str(fail_to_pass)

    return USER_PROMPT_TEMPLATE.format(
        problem_statement=problem_statement[:4000],
        fail_to_pass=fail_to_pass_str[:1000],
        hints_text=hints_text[:500],
    )


def generate_patch(instance: dict, max_retries: int = 3) -> tuple[str, str]:
    """Generate a fix patch. Returns (patch, error_msg)."""
    instance_id = instance["instance_id"]
    for attempt in range(max_retries):
        try:
            user_prompt = build_user_prompt(instance)
            response = call_minimax(user_prompt, SYSTEM_PROMPT, max_tokens=8192)
            diff = extract_diff(response)

            if len(diff) > 50:
                return diff, ""
            else:
                err = f"diff too short ({len(diff)} chars)"
                print(f"  Attempt {attempt+1}: {err}")
        except Exception as e:
            err = str(e)[:100]
            print(f"  Attempt {attempt+1}: error={err}")

        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)  # Exponential backoff

    return "", f"failed after {max_retries} attempts"


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {
        "started_at": datetime.now(tz=timezone.utc).isoformat(),
        "run_session": datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "completed_instances": [],
        "failed_instances": [],
        "resolved": [],
        "unresolved": [],
        "generation_errors": [],
        "iteration": 0,
        "total_generated": 0,
        "total_resolved": 0,
    }


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2))


def append_prediction(pred: dict) -> None:
    with open(PREDICTIONS_FILE, "a") as f:
        f.write(json.dumps(pred) + "\n")


def log(msg: str) -> None:
    ts = datetime.now(tz=timezone.utc).strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def run_harness_evaluation(instance_ids: list[str]) -> dict:
    """Run SWE-bench harness evaluation on the given instance IDs."""
    if not instance_ids:
        return {}

    pred_path = PREDICTIONS_FILE
    if not pred_path.exists():
        return {}

    # Filter predictions for our instances
    our_preds = []
    with open(pred_path) as f:
        for line in f:
            p = json.loads(line)
            if p["instance_id"] in instance_ids:
                our_preds.append(p)

    if not our_preds:
        return {}

    # Write filtered predictions to temp file
    temp_preds = OUT_DIR / f"preds_batch_{datetime.now(tz=timezone.utc).strftime('%Y%m%dT%H%M%S')}.jsonl"
    with open(temp_preds, "w") as f:
        for p in our_preds:
            f.write(json.dumps(p) + "\n")

    try:
        result = subprocess.run(
            [
                sys.executable, "-m", "swebench.harness.run_evaluation",
                "--dataset_name", "princeton-nlp/SWE-bench_Verified",
                "--predictions_path", str(temp_preds),
                "--max_workers", "2",
                "--timeout", "600",
            ],
            cwd="/Users/jleechan/.swes",
            capture_output=True,
            text=True,
            timeout=900,
        )
        # Parse results from stdout/stderr
        results = {}
        for line in result.stdout.split("\n") + result.stderr.split("\n"):
            if "PASS" in line or "FAIL" in line:
                for iid in instance_ids:
                    if iid in line:
                        results[iid] = "PASS" if "PASS" in line else "FAIL"
        return results
    except subprocess.TimeoutExpired:
        log(f"  HARNESS TIMEOUT for {instance_ids}")
        return {}
    except Exception as e:
        log(f"  HARNESS ERROR: {e}")
        return {}
    finally:
        if temp_preds.exists():
            temp_preds.unlink()


def process_batch(state: dict, instances: list[dict], batch_size: int) -> dict:
    """Process a batch of SWE-bench instances."""
    session = state["run_session"]
    state["iteration"] += 1
    iter_num = state["iteration"]

    batch = instances[:batch_size]
    log(f"=== Iteration {iter_num}: batch of {len(batch)} instances ===")

    generated = []
    failed = []

    for i, instance in enumerate(batch):
        iid = instance["instance_id"]
        if iid in state["completed_instances"]:
            log(f"  {i+1}/{len(batch)} {iid}: already completed, skipping")
            continue

        log(f"  {i+1}/{len(batch)} {iid}: generating...")
        patch, err = generate_patch(instance)

        if patch:
            pred = {
                "instance_id": iid,
                "model_name_or_path": "autor-SR-multi-exemplar-batch",
                "model_patch": patch,
                "run_session": session,
                "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            }
            append_prediction(pred)
            generated.append(iid)
            state["total_generated"] += 1
            log(f"    → patch {len(patch)} chars")
        else:
            failure = {
                "instance_id": iid,
                "error": err,
                "run_session": session,
                "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            }
            with open(FAILURES_FILE, "a") as f:
                f.write(json.dumps(failure) + "\n")
            failed.append(iid)
            state["generation_errors"].append(failure)
            log(f"    → FAILED: {err}")

        # Rate limiting
        time.sleep(1)

    log(f"  Generated: {len(generated)}, Failed: {len(failed)}")

    # Run harness evaluation on generated patches
    if generated:
        log(f"  Running harness on {len(generated)} instances...")
        eval_results = run_harness_evaluation(generated)
        for iid, result in eval_results.items():
            if result == "PASS":
                state["resolved"].append(iid)
                state["total_resolved"] += 1
                log(f"    {iid}: PASS")
            else:
                state["unresolved"].append(iid)
                log(f"    {iid}: FAIL")
        state["completed_instances"].extend(generated)

    # Save state after each iteration
    save_state(state)

    # Print summary
    total = len(state["completed_instances"])
    resolved = len(state["resolved"])
    log(f"  Cumulative: {total} completed, {resolved}/{total} resolved ({100*resolved/max(total,1):.0f}%)")

    return state


def main():
    parser = argparse.ArgumentParser(description="Resumable SWE-bench Lite batch evaluation")
    parser.add_argument("--batch-size", type=int, default=5, help="Instances per iteration (default: 5)")
    parser.add_argument("--max-iterations", type=int, default=24, help="Max iterations (default: 24)")
    parser.add_argument("--start-offset", type=int, default=0, help="Skip first N instances")
    args = parser.parse_args()

    log(f"=== SWE-bench Batch Runner Started ===")
    log(f"Batch size: {args.batch_size}, Max iterations: {args.max_iterations}")

    # Load state
    state = load_state()
    run_session = state["run_session"]
    log(f"Run session: {run_session}")
    log(f"State loaded: {state['total_generated']} generated, {state['total_resolved']} resolved")

    # Load dataset
    log("Loading SWE-bench Verified dataset...")
    ds = load_dataset("princeton-nlp/SWE-bench_Verified", split="test")
    log(f"Total instances in dataset: {len(ds)}")

    # Select diverse instances from multiple repos
    repos = ["django", "sympy", "matplotlib", "scikit-learn", "pytest-dev",
             "sphinx-doc", "astropy", "psf", "pylint-dev", "pydata"]

    selected = []
    for repo in repos:
        repo_items = [item for item in ds if item["instance_id"].startswith(repo + "__")]
        for item in repo_items[:5]:
            selected.append(item)

    # Shuffle for diversity
    import random
    random.seed(42)
    random.shuffle(selected)

    # Apply offset
    if args.start_offset > 0:
        selected = selected[args.start_offset:]
        log(f"Applied start offset {args.start_offset}, {len(selected)} remaining")

    log(f"Selected {len(selected)} diverse instances")

    # Resume from where we left off (skip already completed)
    completed = set(state["completed_instances"])
    remaining = [item for item in selected if item["instance_id"] not in completed]
    log(f"Already completed: {len(completed)}, remaining: {len(remaining)}")

    if not remaining:
        log("All instances already processed!")
        print(f"\nFINAL SUMMARY:")
        print(f"  Total generated: {state['total_generated']}")
        print(f"  Total resolved:  {state['total_resolved']}")
        print(f"  Resolution rate: {100*state['total_resolved']/max(state['total_generated'],1):.1f}%")
        return

    # Process in batches
    for iter_num in range(1, args.max_iterations + 1):
        if iter_num > 1:
            # Check if we need to pause
            pass

        batch = remaining[:args.batch_size]
        if not batch:
            log("All remaining instances processed!")
            break

        state = process_batch(state, remaining, args.batch_size)
        remaining = [item for item in remaining if item["instance_id"] not in set(state["completed_instances"])]

        # Save intermediate results
        RESULTS_FILE.write_text(json.dumps({
            "run_session": run_session,
            "iteration": state["iteration"],
            "total_generated": state["total_generated"],
            "total_resolved": state["total_resolved"],
            "resolved_ids": state["resolved"],
            "unresolved_ids": state["unresolved"],
            "generation_errors": [
                {"instance_id": f["instance_id"], "error": f["error"]}
                for f in state["generation_errors"]
            ],
            "resolution_rate": state["total_resolved"] / max(state["total_generated"], 1),
        }, indent=2))

        log(f"Completed iteration {iter_num}/{args.max_iterations}")

    # Final summary
    print(f"\n{'='*60}")
    print(f"FINAL SUMMARY (run {run_session}):")
    print(f"  Iterations:      {state['iteration']}")
    print(f"  Total generated: {state['total_generated']}")
    print(f"  Total resolved:  {state['total_resolved']}")
    print(f"  Resolution rate: {100*state['total_resolved']/max(state['total_generated'],1):.1f}%")
    print(f"  State file:      {STATE_FILE}")
    print(f"  Predictions:    {PREDICTIONS_FILE}")
    print(f"  Results:        {RESULTS_FILE}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()

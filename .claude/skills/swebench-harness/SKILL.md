# SWE-bench Harness Skill

**Skill**: `~/.claude/skills/swebench-harness/SKILL.md`
**Date**: 2026-04-21

## When to use
Any time you call `swebench.harness.run_evaluation` directly or via a script.

## Required arguments (VERIFIED — do NOT skip)

```
--run_id RUN_ID        # REQUIRED — harness writes report to {run_id}.json
--report_dir DIR      # Where to write the report JSON
--predictions_path    # JSONL predictions file
--dataset_name       # princeton-nlp/SWE-bench_Verified or princeton-nlp/SWE-bench_Lite
--max_workers        # Parallel workers (default 2)
--timeout           # Timeout per instance in seconds (default 600)
```

## Output parsing (JSON report, NOT text)

SWE-bench harness does NOT output PASS/FAIL text. It writes a JSON report:
```python
import json
report_path = Path(report_dir) / f"{run_id}.json"
if report_path.exists():
    with open(report_path) as f:
        report = json.load(f)
    # resolved_ids: list of instance IDs that passed
    # unresolved_ids: list where patch applied but tests failed
    # error_ids: list where patch didn't apply (hunk mismatch etc.)
```

**NEVER parse harness output with `if "PASS" in line`** — this will always fail silently.

## Error handling (mandatory)

```python
# If harness errors, propagate the error, don't silently return {}
# Wrong:
except Exception as e:
    return {}  # SILENT FAILURE

# Correct:
except subprocess.TimeoutExpired:
    log(f"HARNESS TIMEOUT for {instance_ids}")
    raise  # or collect partial results if possible
except Exception as e:
    log(f"HARNESS ERROR: {e}")
    raise  # do not silently swallow
```

## Verification checklist

Before declaring a resolution rate, confirm:
1. Harness actually ran (check report JSON exists)
2. Report JSON has `resolved_ids` field
3. The resolved count matches `len(resolved_ids)`
4. Do NOT trust `state["total_resolved"]` unless the report JSON confirms it

## Why this matters
SWE-bench harness without `--run_id` exits immediately with error. Without JSON report parsing, there's no way to detect this failure mode. Silent `return {}` on error is the most dangerous pattern — it makes failure look like success.

---
title: "autor SR-adversarial Design — 2026-05-13"
type: source
tags: [autor, self-refine, adversarial-testing, technique, sr-adversarial]
sources: []
last_updated: 2026-05-13
---

# autor SR-adversarial Design — 2026-05-13

## Session Overview

2026-05-13 rebase session that resolved divergent main branch. Key design decisions across three files.

## Key Changes

### 1. validate_router_prereqs.py — `observations` → `scores` key fix

**Problem:** The per-technique `n` calculation used `observations` key, which was incorrect.

**Before (broken):**
```python
t: max(len(techniques_state.get(t, {}).get("observations", [])), techniques_state.get(t, {}).get("n", 0))
```

**After (fixed):**
```python
t: len(techniques_state.get(t, {}).get("scores", []))
```

The correct key is `scores` — the list of per-run score totals maintained at the technique level in `bandit_state.json`. Using `observations` caused n to be undercounted, breaking the prerequisite gate's statistical power check.

### 2. run_autor_experiment.py — SR-adversarial technique added

**SR-adversarial:** A Solver+Attacker technique. The generation prompt instructs the model to:
1. Generate a production-ready fix
2. **Actively attack it** — find edge cases, failure modes, bugs in the generated fix
3. Refine until robust

```python
"SR-adversarial": {
    "system": "You are an expert code reviewer. Generate fixes and actively attack them to find weaknesses.",
    "generation": """Generate a production-ready fix for this PR, then ADVERSARIALLY attack it: find edge cases, failure modes, and bugs in your own fix. Refine until robust.

PR Title: {title}
...

Step 1: Generate the fix.
Step 2: ATTACK your fix — what breaks? what edge cases? what fails?
Step 3: Refine the fix to address the weaknesses found.
Output the final code in a ```python``` block.""",
}
```

SR-5iter was removed from the `--technique` choices in run_autor_experiment.py (exists only in batch_sr5iter.py).

### 3. batch_sr5iter.py — resolved to origin version

The batch targeting was resolved to the origin version (2c20d8b1):

```python
# PRs that have only 1 run (need 2 more each for n=3): 6409,6418,6420,6429,6432,6434,6436,6437,6438,6443,6444
# PRs that already have 3 runs: 6243,6245,6261,6265,6269 (already complete)
# For the 15-run batch, target 5 PRs with 3 runs each = 15 total
# Select PRs with only 1 run, adding runs to reach 3 each
prs_need_runs = [6409,6418,6420,6429,6432,6434,6436,6437,6438,6443,6444]
target_prs = prs_need_runs[:5]  # 6409, 6418, 6420, 6429, 6432
```

3 runs per PR, 5 PRs = 15 total runs.

## Merge Conflict Resolution

All three files had merge conflicts resolved by accepting the 2c20d8b1 version (fix branch). This represents:
- The `observations` → `scores` fix for correct per-technique n
- SR-adversarial as the new active technique
- batch_sr5iter.py targeting PRs needing additional runs to reach n=3

## Related

- [[autor-router-prerequisite-gate]]
- [[autor-5iter-technique]]
- [[validate_router_prereqs.py]]
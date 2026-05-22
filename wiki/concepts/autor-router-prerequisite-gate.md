---
title: "autor Router Prerequisite Gate"
type: concept
tags: [autor, router, bandit, prerequisite, gate, zfc]
sources: [autor-sr-adversarial-design-2026-05-13]
last_updated: 2026-05-13
---

# autor Router Prerequisite Gate

## Problem

Before any PR-type → technique router can be built, a structural gate must be cleared. The gate prevents building a router when the evidence base cannot support routing decisions.

## What the gate enforces

`scripts/validate_router_prereqs.py` implements a mandatory prerequisite gate with three conditions:

| Condition | Threshold | Purpose |
|---|---|---|
| Matched PRs | ≥ 5 | PRs scored by ALL tracked techniques (nested rubric_scores entries) |
| Ranking reversals | ≥ 2 | Technique A beats B on PR X, B beats A on PR Y — proves disagreement |
| Per-technique n | ≥ 30 | Statistical power: n=30 needed to detect delta=10 at 80% power |

## Why matched-PR reversals are required

Bandit means on **disjoint** PR sets cannot prove routing value. If SR is tested on PRs 1-5 and ET is tested on PRs 6-10, convergence of means only shows both techniques work on their respective PRs. The variance could be PR-specific, not technique-specific.

A router can only add value over "always pick the top-mean technique" if there exist **ranking reversals** — cases where A beats B on one PR while B beats A on another. Without reversals, always picking the highest mean is provably optimal.

## How reversals are counted

`build_matched_table()` creates a {pr_id: {technique: score}} table from nested rubric_scores entries. `count_reversals()` iterates over all technique pairs and counts a reversal when:
- At least one PR where A > B
- AND at least one PR where B > A

Each pair contributes at most 1 reversal.

## Per-technique n fix

The gate was broken because `per_technique_n` used the `observations` key instead of `scores`:

```python
# Wrong (used observations):
t: max(len(techniques_state.get(t, {}).get("observations", [])), ...)

# Correct (uses scores):
t: len(techniques_state.get(t, {}).get("scores", []))
```

The `scores` list is the per-run totals maintained at the technique level. `observations` was the wrong key, causing n to be undercounted.

## Exit codes

- `0`: All conditions met — router work unblocked
- `1`: Conditions not met — router work blocked, printed report
- `2`: Input error (missing file, malformed JSON)

## See also

- [[autor-5iter-technique]]
- [[autor-sr-adversarial-design-2026-05-13]]
- [[validate_router_prereqs.py]]
---
title: "Router Gate Policy Design"
type: synthesis
tags: [autor, router, bandit, gate]
sources: []
last_updated: 2026-05-13
run_session: rebased-2026-05-13
---

## Context

The router prerequisite gate ensures any PR-type → technique router work is only attempted when there is sufficient matched-corpus evidence to justify routing over flat mean selection.

## Gate mechanics

- **min_matched**: ≥5 PRs must be scored by ALL tracked techniques (explicit `technique` field in rubric_scores)
- **min_reversals**: ≥2 ranking reversals across technique pairs (A beats B on one PR, B beats A on another)
- **min_per_technique_n**: ≥30 observations per technique (statistical power: detect delta=10 at 80% power given sigma~20)

## Why this gate exists

An earlier session recommended "build the router" based on convergent means on disjoint PR sets — a structural fallacy. Two techniques can have identical means on disjoint sets but opposite orderings on overlapping sets. Only matched-PR evaluation (same PR scored by all techniques) can reveal ranking reversals.

## Implementation

`scripts/validate_router_prereqs.py` — deterministic count from `bandit_state.json`. Exit 0 = unblocked, exit 1 = blocked, exit 2 = input error.

## Resolution from 2026-05-13 rebase

Local commit `2c20d8b1` fixed `validate_router_prereqs.py` to use `scores` key instead of `observations` key for per-technique n calculation. The remote origin/main already had this fix, so the rebase took remote's version.
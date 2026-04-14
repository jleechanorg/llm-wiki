---
title: "Auto-Research Loop (Self-Discovering Meta-Research)"
type: source
tags: [auto-research, meta-research, hypothesis-generation]
date: 2026-04-14
source_file: skills/auto_research_loop.md
---

## Summary

A 4-phase self-discovering research loop where an agent generates its own novel, falsifiable hypotheses from historical PR patterns, then tests them against real code using the self-critique verification loop. Closes the gap between published research and actual codebase by grounding every experiment in observed patterns.

## Key Claims

- **Self-Generating Hypotheses**: Agent analyzes PR history to generate 1–3 novel, testable hypotheses per run — not just replaying published papers
- **Grounded in Real Code**: Test-PRs directory contains historical PR descriptions + diffs for replay
- **Rigorous Evaluation**: Baseline (direct generation) vs improved version, scored quantitatively
- **Continuous Wiki Updates**: Results written back to wiki with metrics after every run
- **beads Integration**: Every experiment run tracked as a bead for later analysis

## Phase 0 — Hypothesis Generation

Analyze patterns across `test-prs/` and canonical repos. Generate 1–3 novel, testable hypotheses for improving code quality, architecture, or harness efficiency.

Each hypothesis must be:
- **Specific and falsifiable**: Can be disproven by a test
- **Grounded in observed patterns**: Derived from real PR history
- **Different from existing papers**: Not a restatement of published work

Output format (exact):
```
Hypothesis 1: [short title]
Rationale: [observed patterns]
Predicted improvement: [expected gain]
Test plan: [how to test on next PR]
```

## Phase 1 — Selection

Choose the next historical PR from `test-prs/` or test one of the generated hypotheses.

## Phase 2 — Implementation

Implement the selected paper's technique OR the generated hypothesis using the `self_critique_verification_loop` skill.

## Phase 3 — Evaluation

Run baseline (direct generation) and improved version. Score both using the `canonical_code_scorer` skill. Record full results in `results.md`.

## Phase 4 — Update

- Update the relevant wiki page with a "Results on My Codebase" section
- Create a bead for every experiment run

## Connections

- [[SelfCritiqueVerificationLoop]] — used in Phase 2 for implementation
- [[CanonicalCodeScorer]] — used in Phase 3 for evaluation
- [[AutoResearchExperiment]] — the broader system this skill is part of
- [[auto-product-master-system]] — the full master system containing this skill

## Contradictions

- None

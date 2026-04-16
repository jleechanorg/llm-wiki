---
title: "Auto-Research Convergence Oracle — Concept to Implementation Pipeline"
type: concept
tags: [auto-research, convergence, oracle, paper-selection, technique-selection]
last_updated: 2026-04-16
---

## Vision

The Auto-Research Convergence Oracle is a closed-loop system that programmatically determines **which papers/techniques are worth implementing** in the codebase, based on real empirical evidence from PR outcomes.

```
Papers & Techniques (wiki/sources, wiki/concepts)
    ↓ extract & document
Implementable Techniques (technique_concepts)
    ↓ PR Recreate Pipeline tests each on real PRs
Scores (per technique, per PR type)
    ↓ Thompson Sampling updates beliefs
Belief state (posterior per technique)
    ↓ convergence check
Implemented Techniques (in worldarchitect.ai)
    ↓ measured outcomes
More evidence → back to pipeline
```

## Two-Level Oracle

### Level 1: Paper Relevance Oracle
Given an ingested paper → is the technique it describes **implementable** in worldarchitect.ai?
- Input: paper source page
- Output: implementable (Y/N) + what PR type it applies to + confidence

### Level 2: Technique Selection Oracle (Thompson Sampling)
Given a new PR → which technique should I use?
- Input: PR features (size, type, files touched)
- Output: recommended technique + exploration/exploitation balance

## Convergence Criteria

A technique is **converged** when:
1. n ≥ 10 observations
2. Posterior stddev < 5 (narrow confidence interval)
3. Clear winner with >80% posterior probability of being best

A paper is **validated** when:
1. Technique extracted and documented as concept page
2. Applied to ≥3 real PRs via Recreate Pipeline
3. Mean score ≥ 80 with delta ≥ 5 vs baseline

## Current State

| Technique | n | Posterior Mean | Status |
|-----------|---|---------------|--------|
| SelfRefine | 12 | 83.0 | Converging |
| ET | 11 | 83.7 | Converging |
| PRM | 4 | 81.1 | Needs more data |

## See Also

- [[AutoResearchLoop]] — the research loop
- [[TechniqueSelectionOracle]] — Thompson sampling implementation
- [[PRRecreatePipeline]] — the experiment methodology
- [[AutoResearchExperiment]] — experiment framework
- [[CanonicalCodeScorer]] — scoring rubric

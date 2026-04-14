---
title: "Canonical Code Scorer (Rubric + Diff Metric)"
type: source
tags: [scoring, evaluation, rubric, diff-similarity, code-quality]
date: 2026-04-14
source_file: skills/canonical_code_scorer.md
---

## Summary

A quantitative code scoring engine that combines a 6-dimension weighted rubric (Pass/Fail) with token-level diff similarity against ground-truth canonical code. Overall score = 0.7 × rubric-weighted Pass-rate + 0.3 × diff similarity. Used in the auto-research loop to compare baseline vs improved code versions.

## Key Claims

- **Hybrid Scoring**: Combines human-readable rubric assessment with automated diff similarity
- **6 Rubric Dimensions**: Covers naming, error handling, type safety, tests, docs, evidence standards
- **Token-Level Diff**: Measures edit distance to ground-truth, not just semantic similarity
- **Weighted Overall**: 70% rubric, 30% diff — balances quality against proximity to known-good code

## Rubric Dimensions (Pass/Fail each)

| # | Dimension | Notes |
|---|-----------|-------|
| 1 | Naming & Consistency | Follows project naming conventions |
| 2 | Error Handling & Robustness | Proper exception handling, graceful degradation |
| 3 | Type Safety / Architecture | 30% weight in overall calculation |
| 4 | Test Coverage & Clarity | Unit + integration + edge cases |
| 5 | Documentation & Comments | Inline docs, README updates |
| 6 | Evidence-Standard Adherence | Meets harness evidence standards |

## Diff Similarity

Compute token-level edit distance between the generated file and the ground-truth PR file. Convert to a 0–100 similarity score.

## Overall Score Formula

```
Overall score = 0.7 × rubric-weighted Pass-rate + 0.3 × diff similarity
```

## Output Format

- Overall score (0–100)
- Per-dimension breakdown
- Improvement suggestions

## Connections

- [[SelfCritiqueVerificationLoop]] — outputs verified code that gets scored
- [[AutoResearchLoop]] — uses this in Phase 3 for evaluation
- [[AutoResearchExperiment]] — the broader system this skill is part of

## Contradictions

- None

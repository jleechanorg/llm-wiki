---
title: "CanonicalCodeScorer"
type: concept
tags: [agent-harness, coding-agents, evaluation, scoring]
sources: [auto-product-master-system, auto-research-experiment-v21]
last_updated: 2026-04-14
---

## Definition

A quantitative code quality scoring engine that combines a 6-dimension rubric (Pass/Fail) with a diff similarity metric. Used in [[AutoResearchLoop]] Phase 3 to evaluate baseline vs. improved code versions.

## Rubric Dimensions (Pass/Fail each)

1. **Naming & Consistency** — Variables, functions, files follow consistent naming conventions
2. **Error Handling & Robustness** — Proper exception handling, input validation, edge cases covered
3. **Type Safety / Architecture** (30% weight) — Strong typing, correct data structures, clean architecture
4. **Test Coverage & Clarity** — Tests are readable, cover unit/integration/edge cases
5. **Documentation & Comments** — Docstrings, comments explain *why*, not *what*
6. **Evidence-Standard Adherence** — Output meets harness evidence standards (video, proof, etc.)

## Diff Similarity

Compute token-level edit distance between the generated file and the ground-truth PR file (your actual merged code). Convert to a 0–100 similarity score.

**Formula:**
```
Overall score = 0.7 × rubric-weighted Pass-rate + 0.3 × diff similarity
```

## Scoring Output Format

```
Overall score: 0–100
Per-dimension: Pass/Fail + optional comments
Improvement suggestions (reference concrete wiki pages)
```

## Key Design Choices

- **0.7/0.3 weighting**: Favors rubric quality (human-judged dimensions) over surface similarity
- **Diff similarity against ground truth**: Measures how close the generated code is to what you actually shipped
- **30% weight on Type Safety/Architecture**: Architectural quality matters most for long-term maintainability
- **Evidence-standard dimension**: Ensures outputs meet [[AutoProductMasterSystem]] harness requirements

## Integration Points

- Called by [[AutoResearchLoop]] Phase 3 (Evaluation)
- Canonical patterns sourced from ingested repos: FastAPI, tRPC, Requests, Axum
- Results feed back into the wiki "Results on My Codebase" section

## Related Concepts

- [[AutoResearchLoop]] — the outer loop that invokes the scorer
- [[SelfCritiqueVerificationLoop]] — the loop that produces the code being scored
- [[ReVeal2026]] — the test execution framework the scorer evaluates against
- [[EvidenceStandards]] — the evidence-standard dimension referenced in the rubric

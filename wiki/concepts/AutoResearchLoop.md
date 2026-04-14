---
title: "AutoResearchLoop"
type: concept
tags: [agent-harness, llm-wiki, self-research, meta-learning]
sources: [auto-product-master-system, auto-research-experiment-v21]
last_updated: 2026-04-14
---

## Definition

A self-discovering meta-research loop that runs inside the Karpathy LLM Wiki. The agent analyzes patterns across your historical PRs, generates its own novel falsifiable hypotheses about improving code quality, then tests those hypotheses (and published techniques) against real PRs using the [[SelfCritiqueVerificationLoop]]. Results are recorded in the wiki with full metrics.

## How It Works

**Phase 0 — Hypothesis Generation**
Analyze patterns across your historical PRs and canonical repos. Generate 1–3 novel, testable hypotheses for improving code quality, architecture, or harness efficiency. Each hypothesis must be:
- Specific and falsifiable
- Grounded in observed patterns from your codebase
- Different from existing papers in raw/

Format:
```
Hypothesis 1: [short title]
Rationale: [observed patterns]
Predicted improvement: [expected gain]
Test plan: [how to test on next PR]
```

**Phase 1 — Selection**
Choose the next historical PR from test-prs/ or test one of the generated hypotheses.

**Phase 2 — Implementation**
Implement the selected paper's technique OR the generated hypothesis using [[SelfCritiqueVerificationLoop]] (with real sandboxed test execution).

**Phase 3 — Evaluation**
Run baseline (direct generation) and improved version. Score both using [[CanonicalCodeScorer]]. Record full results in the wiki (pass rate, iterations, token usage, rubric breakdown, diff similarity).

**Phase 4 — Update**
Update the relevant wiki page with "Results on My Codebase" section. Create a bead for every experiment run.

## Key Design Choices

- **Self-discovering**: Agent generates its own hypotheses rather than just replaying published papers
- **Grounded in real PRs**: test-prs/ contains historical PR descriptions + diffs for realistic evaluation
- **Bead tracking**: Every run recorded as a bead for dependency-aware tracking
- **Canonical repos**: High-quality reference repos (FastAPI, tRPC, Requests, Axum) ingested as pattern library

## Integration Points

- Calls [[SelfCritiqueVerificationLoop]] in Phase 2
- Outputs to [[CanonicalCodeScorer]] in Phase 3
- Uses [[AutoProductMasterSystem]] directory structure (raw/, canonical-repos/, test-prs/)
- Creates beads for each experiment run (Phase 4)

## Related Concepts

- [[SelfCritiqueVerificationLoop]] — the inner verification loop called in Phase 2
- [[CanonicalCodeScorer]] — the scoring engine used in Phase 3
- [[ProductTasteLayer]] — the product judgement layer (master system only, not in autocodev2)
- [[KarpathyLLMWiki]] — the wiki infrastructure this loop runs on top of

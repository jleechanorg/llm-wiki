---
title: "AutoResearchExperiment"
type: concept
tags: [auto-research, meta-research, coding-agents, self-improvement]
sources: [auto-research-experiment-v21, auto-product-master-system, auto-research-loop, self-critique-verification-loop, canonical-code-scorer, product-judge, taste-learning-loop]
last_updated: 2026-04-14
---

Self-discovering meta-research system combining LLM wiki + self-critique loop + canonical scoring + product taste. Runs autonomous coding improvement cycles against a real codebase, evaluating each cycle with a structured rubric to discover systematic quality patterns. Version 2.1 (April 2026).

## Problem It Solves

How to systematically improve code quality using historical PR patterns. Rather than relying on manual code review, the system analyzes `test-prs/` for patterns, generates its own novel hypotheses, selects PRs to implement, and scores each attempt against a canonical rubric — building up knowledge of what actually works on YOUR specific codebase.

## Architecture: 5-Layer Stack

```
Layer 5 — Product Taste Layer (human judgment gate)
    ├── [[ProductJudge]] — isolated oracle scoring 5 dimensions
    └── [[TasteLearningLoop]] — negative constraint extraction
Layer 4 — Auto-Research Loop (hypothesis generation + experiment)
Layer 3 — [[CanonicalCodeScorer]] (quantitative comparison)
Layer 2 — [[SelfCritiqueVerificationLoop]] (implementation + verification)
Layer 1 — LLM Wiki (knowledge base — papers + canonical patterns + results)
```

## Key Components

### [[AutoResearchLoop]] — Self-Discovering Meta-Research Loop

4-phase loop that analyzes PR history, generates novel hypotheses, implements via self-critique, scores via canonical scorer, and writes results to wiki + beads.

### [[SelfCritiqueVerificationLoop]] — Self-Critique + Verification Loop

3-iteration-cap verification combining ReVeal (2026) + Self-Correction (2025):
- Phase 0: Chain canonical pattern prompt from wiki
- Phase 1: Step-by-step code generation
- Phase 2: Full test suite + sandboxed execution
- Phase 3: Critique against test results; iterate if needed (max 3)

### [[CanonicalCodeScorer]] — Rubric + Diff Scoring

Hybrid: 6-dimension weighted Pass/Fail rubric (70%) + token-level diff similarity (30%).
Dimensions: Naming, Error Handling, Type Safety (30% weight), Test Coverage, Documentation, Evidence Standards.

### [[ProductJudge]] — Product Taste Oracle

Runs in completely isolated session. Scores 5 dimensions (0–100):
- Strategic Alignment
- UX & Delight
- Simplicity & Clarity
- Long-term Maintainability & Vision Fit
- Edge-case & Business Nuance

Output: Approve / Minor Changes / Major Changes / Reject + concrete changes.

### [[TasteLearningLoop]] — Taste Refinement Loop

Triggered on manual rejection/editing. 4 steps:
1. Extract feedback + original PR
2. Archive to `product-taste/good-bad-examples.md`
3. Update `taste-rubric.md` with positive principles AND explicit "NEVER DO THIS" negative constraints
4. Create bead tracking the learning event

## Results (18 Cycles)

- Score range: 53–86/100
- **Type Safety** — systematically FAIL across all cycles (pervasive `Any` types)
- **Shell CI scripts** — highest scoring at 86/100
- Pattern: iterations that pass tests but still score mid-range due to type safety and documentation gaps

## Key Design Principles

- **Grounded, not hypothetical**: Every technique tested against real PRs, not synthetic benchmarks
- **Evaluator separation**: ProductJudge runs in completely isolated session
- **3-iteration cap**: Balances quality vs token efficiency on self-critique
- **Negative constraints**: Explicit "NEVER DO THIS" rules alongside positive principles
- **Continuous learning**: Every manual correction becomes permanent institutional knowledge via beads

## See Also
- [[SelfCritiqueVerificationLoop]]
- [[AutoResearchLoop]]
- [[CanonicalCodeScorer]]
- [[ProductJudge]]
- [[TasteLearningLoop]]
- [[ProductTasteLayer]]
- [[auto-product-master-system]] — full master system source page
- [[auto-research-experiment-v21]] — streamlined v2.1 source page
- [[Self-Improving Coding Agents]]
- [[LLM-as-Judge Pattern]]

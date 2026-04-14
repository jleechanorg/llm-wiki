---
title: "ProductJudge"
type: concept
tags: [agent-harness, product-judgement, llm-wiki]
sources: [auto-product-master-system]
last_updated: 2026-04-14
---

## Definition

A personal Product Taste Oracle skill that evaluates every PR against codified personal product judgement from the [[ProductTasteLayer]] wiki. Before approving any PR, the Product Judge scores it across 5 dimensions and references specific wiki pages. This ensures PRs match what you actually want — not just technically correct code.

## Product Judgement Rubric (score each 0–100)

1. **Strategic Alignment** — Does this move the product in the direction I actually care about?
2. **User Experience & Delight** — Would I be proud to ship this to users?
3. **Simplicity & Clarity** — Is it over-engineered or unnecessarily complex?
4. **Long-term Maintainability & Vision Fit** — Does it fit the overall architecture and future roadmap I have in mind?
5. **Edge-case & Business Nuance** — Does it handle the subtle product realities I care about?

## Output Format

```
Overall score: 0–100
Per-dimension breakdown
Detailed explanation referencing wiki pages and past decisions
Verdict: Approve / Minor Changes / Major Changes / Reject
Concrete changes to better match my taste
```

## Key Design Choices

- **5-dimension rubric**: Strategic, UX, Simplicity, Maintainability, Business nuance — covers the gap between "correct code" and "right code"
- **Wiki-grounded judgement**: References [[ProductTasteLayer]] pages (principles, good-bad-examples, taste-rubric) so every verdict is traceable
- **4-tier verdict**: Approve / Minor Changes / Major Changes / Reject — forces a decision
- **Verdict-dependent on [[TasteLearningLoop]]**: The taste wiki grows over time as you manually correct the agent

## Integration Points

- Invoked at end of [[AutoResearchLoop]] Phase 3 alongside [[CanonicalCodeScorer]]
- Uses [[ProductTasteLayer]] wiki pages for judgement references
- [[TasteLearningLoop]] feeds new examples back into the taste wiki after manual corrections

## Related Concepts

- [[ProductTasteLayer]] — the full product taste subsystem this skill is part of
- [[TasteLearningLoop]] — the loop that updates the taste wiki after manual corrections
- [[CanonicalCodeScorer]] — runs alongside ProductJudge in the evaluation phase
- [[AutoResearchLoop]] — invokes ProductJudge as part of its evaluation phase

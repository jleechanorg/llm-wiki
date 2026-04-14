---
title: "ProductTasteLayer"
type: concept
tags: [agent-harness, product-judgement, llm-wiki, self-improvement]
sources: [auto-product-master-system]
last_updated: 2026-04-14
---

## Definition

A product judgement subsystem within the [[AutoProductMasterSystem]] that codifies and continuously refines personal product taste. Complements the [[CanonicalCodeScorer]] (which measures code quality) by measuring *product fit* — whether a PR moves the product in the direction you actually want. Runs as part of [[AutoResearchLoop]] Phase 3 alongside scoring.

## Core Components

### wiki/product-taste/index.md
Master index for the subsystem.

### wiki/product-taste/principles.md
High-level personal product values and philosophy. Starter content:
- Simplicity over cleverness
- User delight and intuition first
- Performance and reliability are non-negotiable
- Long-term maintainability and vision fit matter more than short-term speed

### wiki/product-taste/good-bad-examples.md
Concrete past PRs you loved vs. hated, with your actual comments. Auto-populated over time by [[TasteLearningLoop]]. Format:
```
**Good Example** – PR #XXXX
Reason: Why this felt exactly right

**Bad Example** – PR #YYYY
Reason: Technically correct but missed the product nuance I cared about
```

### wiki/product-taste/taste-rubric.md
Scoring dimensions and weights for [[ProductJudge]]. Updated by [[TasteLearningLoop]] when new principles emerge.

### wiki/product-taste/taste-evolution-log.md
Chronological record of how your product taste has changed over time.

## How It Integrates With the Research Loop

1. [[AutoResearchLoop]] Phase 3 runs both [[CanonicalCodeScorer]] AND [[ProductJudge]]
2. [[ProductJudge]] references the product-taste/ wiki pages when scoring
3. When you manually override a verdict, [[TasteLearningLoop]] updates the wiki
4. Future [[ProductJudge]] calls automatically use updated wiki content

## Key Design Choices

- **Separate from code quality**: [[CanonicalCodeScorer]] handles technical quality; ProductTasteLayer handles strategic/UX/maintainability fit
- **Living wiki**: Not static — grows with every manual correction via [[TasteLearningLoop]]
- **Closed feedback loop**: Corrections → updated wiki → better future verdicts
- **Version 2.1 only**: Not present in [[AutoResearchExperimentV21]] (the streamlined autocodev2 version)

## Related Concepts

- [[ProductJudge]] — the oracle skill that uses this subsystem
- [[TasteLearningLoop]] — the feedback loop that updates this subsystem
- [[CanonicalCodeScorer]] — the complementary scoring system (code quality vs. product fit)
- [[AutoResearchLoop]] — the outer loop that invokes ProductJudge
- [[AutoProductMasterSystem]] — the master system this is part of (v2.1 full version)

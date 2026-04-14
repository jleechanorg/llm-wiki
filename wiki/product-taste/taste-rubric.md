---
title: "Taste Rubric"
type: concept
tags: [product-judgement, scoring]
sources: [auto-product-master-system]
last_updated: 2026-04-14
---

## Taste Rubric — [[ProductJudge]] Scoring Dimensions

Each dimension scored 0–100. Overall score is the average.

| Dimension | Weight | What It Measures |
|---|---|---|
| Strategic Alignment | High | Does this move the product in the direction I actually care about? |
| User Experience & Delight | High | Would I be proud to ship this to users? Does it feel right? |
| Simplicity & Clarity | Medium | Is it over-engineered or unnecessarily complex? |
| Long-term Maintainability & Vision Fit | High | Does it fit the overall architecture and future roadmap I have in mind? |
| Edge-case & Business Nuance | Medium | Does it handle the subtle product realities I care about? |

## Verdict Thresholds

- **Approve**: Average ≥ 75 AND no dimension below 50
- **Minor Changes**: Average 60–74 OR one dimension 40–49
- **Major Changes**: Average 50–59 OR any dimension below 40
- **Reject**: Average < 50

## Updating This Rubric

When [[TasteLearningLoop]] detects new principles from manual corrections, update both this file and [[ProductPrinciples]].

## Related

- [[ProductJudge]] — the oracle that uses this rubric
- [[TasteLearningLoop]] — updates this when I override verdicts
- [[GoodBadExamples]] — concrete examples that validate these dimensions

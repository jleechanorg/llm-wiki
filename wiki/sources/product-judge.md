---
title: "Product Judge (Product Taste Oracle)"
type: source
tags: [product-judgement, taste, oracle, evaluator-separation]
date: 2026-04-14
source_file: skills/product_judge.md
---

## Summary

A completely isolated product taste oracle that evaluates any PR or feature against jleechan's personal product judgement rubric. Runs in a separate agent session to ensure evaluation independence. Scores 5 dimensions (Strategic Alignment, UX & Delight, Simplicity, Maintainability, Edge-case Nuance) and outputs a verdict: Approve / Minor Changes / Major Changes / Reject.

## Key Claims

- **Evaluator Separation**: Must run in a completely isolated session — not the same session that generated the code
- **5-Dimension Rubric**: Covers strategic direction, user experience, simplicity, long-term architecture, and business nuance
- **Reference Material**: Consults `~/worldarchitect.ai/wiki/product-taste/` for context
- **Actionable Verdict**: Not just a score — concrete changes required or approval

## Product Judgement Rubric (score each 0–100)

| Dimension | Question |
|-----------|----------|
| Strategic Alignment | Does this move the product in the direction I actually care about? |
| UX & Delight | Would I be proud to ship this to users? |
| Simplicity & Clarity | Is it over-engineered or unnecessarily complex? |
| Long-term Maintainability & Vision Fit | Does it fit the overall architecture and future roadmap? |
| Edge-case & Business Nuance | Does it handle the subtle product realities I care about? |

## Output Format

- Overall score (average or weighted sum of dimensions)
- Per-dimension breakdown with scores
- Detailed explanation
- Verdict: **Approve** / **Minor Changes** / **Major Changes** / **Reject**
- Concrete changes (if not Approve)

## Connections

- [[TasteLearningLoop]] — updates the taste rubric based on Judge verdicts
- [[ProductTasteLayer]] — the full subsystem this oracle is part of
- [[auto-product-master-system]] — the master system containing this skill

## Contradictions

- None

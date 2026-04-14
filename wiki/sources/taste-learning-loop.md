---
title: "Taste Learning Loop (with Negative Constraint Generation)"
type: source
tags: [taste-learning, negative-constraints, self-improvement, product-judgement]
date: 2026-04-14
source_file: skills/taste_learning_loop.md
---

## Summary

A self-improving taste refinement loop triggered whenever jleechan manually rejects, heavily edits, or comments on a PR. Extracts the feedback, archives it in the product-taste wiki, updates the taste rubric with both positive principles and explicit "NEVER DO THIS" negative constraints, and creates a bead to track the learning event. Turns every human correction into permanent institutional knowledge.

## Key Claims

- **Negative Constraint Generation**: Explicitly documents what NOT to do, not just aspirational principles
- **Learning From Rejection**: Manual corrections are the most valuable training signal
- **Permanent Knowledge**: Every correction is stored in the wiki, not lost after the session
- **beads Integration**: Learning events tracked as beads for pattern analysis

## The Loop (4 Steps)

1. **Extract**: Pull the feedback and original PR from the review
2. **Archive**: Add to `~/worldarchitect.ai/wiki/product-taste/good-bad-examples.md`
3. **Update Rubric**: Update `~/worldarchitect.ai/wiki/product-taste/taste-rubric.md` with:
   - Positive principles that were violated
   - Explicit "NEVER DO THIS" negative constraints
4. **Track**: Create a bead recording the learning event

## Key Quotes

> "Whenever jleechan manually rejects, heavily edits, or comments on a PR"

## Connections

- [[ProductJudge]] — generates verdicts that may trigger this loop
- [[ProductTasteLayer]] — the full subsystem this loop is part of
- [[auto-product-master-system]] — the master system containing this skill

## Contradictions

- None

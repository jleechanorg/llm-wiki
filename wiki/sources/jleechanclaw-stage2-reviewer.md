---
title: "jleechanclaw-stage2-reviewer"
type: source
tags: [jleechanclaw, review, skeptic]
date: 2026-04-14
source_file: jleechanclaw/src/orchestration/stage2_reviewer.py
---

## Summary
Second-stage reviewer for the evidence review pipeline. After automated checks pass in stage 1 (evidence_review_gate), stage 2 applies human skeptic judgment to evidence quality and completeness. Part of the two-stage verification system.

## Key Claims
- Skeptic review: human judgment on evidence quality
- Checks evidence against the evidence publication rules
- Verifies scope coverage and completeness

## Connections
- [[jleechanclaw-evidence-review-gate]] — stage 1 of the pipeline
- [[jleechanclaw-pr-review-decision]] — related to review quality gates

## Contradictions
- None identified
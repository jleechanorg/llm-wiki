---
title: "CI trim forward projections underestimate cascade effects 6.5x"
type: source
tags: [ci-trim, worldarchitect-ai, measurement, projection-methodology, cascade-effects]
date: 2026-07-13
source_file: feedback_2026-07-13_ci_trim_actual_vs_projection.md
---

## Summary

Lane F's 37.86 compute-hr/48h CI savings projection (worldarchitect.ai round 1-3 trim) was 6.5x conservative vs actual 246.53h/48h measured 14h post-trim. The envelope model — "X% reduction in Y workflow" — systematically underestimated cascade effects. Removing a trigger eliminates downstream workflows that would have been triggered by those events too. Skip rate can also move (74.0% → 54.9%) when skip-driver workflows are the natural trim targets.

## Key Claims

- Forward projection methodology MUST model cascade effects: removing 1 trigger can cascade into 5-10x reduction on downstream workflows.
- 14h post-trim re-measurement validates rounds 1-3 effectiveness with actual numbers.
- Per-PR cascade analysis: test.yml push trim was 19x larger than projected (#8363); filter:blob:none cascaded 15x into MCP Smoke Tests (#8270).
- Skip rate is NOT a static floor — Lane F's projection assumed it wouldn't move; it moved 19pp because the skip-driver workflows were the natural trim targets.

## Key Quotes

> "Lane F's envelope model was based on: 'X% reduction in Y workflow' instead of 'remove entire trigger category'."

> "Removing 100% of one trigger can cascade into 5-10x reduction on downstream workflows."

> "Per-PR verdict: PRs #8354, #8364, #8363, #8367, #8366, #8365+#8368, #8270 confirmed highly effective (all exceeded projections by 3x-19x)."

## Connections

- [[WorldArchitectAI]] — primary repo context
- [[CommentRouterWorkflow]] — round 1 PR #8354 canonical pattern
- [[EzghaMemoryDetection]] — round 2 PR #77 fix (parallel lesson)
- [[ActionlintPathsMutualExclusion]] — round 3-5 fix pattern
- [[CITrimProjectionMethodology]] — new concept page extracted from this learning

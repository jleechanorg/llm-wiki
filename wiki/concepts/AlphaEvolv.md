---
title: "AlphaEvolv"
type: concept
tags: [AlphaEvolv, text-optimizer, evolutionary, scalar-feedback, meta-harness]
sources: [meta-harness-paper]
last_updated: 2026-04-14
---

## Summary

AlphaEvolv is a text optimizer referenced in the Meta-Harness paper, notable for using scalar score feedback to drive evolutionary optimization of text/prompts. It represents the limitation of prior text optimizers that rely primarily on scalar scores and compressed feedback, which Meta-Harness improves upon by accessing full source code, execution traces, and scores.

## Key Claims

- AlphaEvolv uses scalar scores to guide evolutionary optimization
- Relies primarily on scalar scores, restricting feedback quality
- One of several prior text optimizers that Meta-Harness outperforms
- Like other text optimizers, limited by memoryless operation and compressed feedback
- Meta-Harness demonstrates that full code + trace access enables superior optimization

## Why Scalar Scores Are Insufficient

Prior text optimizers like AlphaEvolv face limitations:
- **Scalar scores lose information**: A single number cannot capture what went wrong
- **Compressed feedback**: Template summaries lose critical details
- **Memoryless operation**: No access to what prior candidates did differently
- **Context limits**: 100-30K tokens prevents rich evaluation

Meta-Harness addresses all these by using filesystem history to access full code, execution traces, and detailed scores.

## Connections

- [[MetaHarness]] — outperforms AlphaEvolv through richer feedback access
- [[ACE]] — another text optimizer comparison
- [[OpenEvolve]] — related evolutionary optimizer
- [[FeedbackLoop]] — Meta-Harness uses richer feedback than scalar scores
- [[ExecutionTraces]] — Meta-Harness accesses traces that AlphaEvolv cannot

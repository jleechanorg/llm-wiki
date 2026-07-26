---
title: "Cheaper-model delegation for WorldArchitect PR repair"
type: source
tags: [model-routing, delegation, code-review, evidence, worldarchitect]
date: 2026-07-11
source_file: ../../raw/2026-07-11-cheaper-model-delegation-pr-repair-report.md
---

## Summary

A five-lane PR repair experiment compared gpt-5.6-luna, gpt-5.6-terra, and gpt-5.4. Luna was effective for bounded TDD and gate operations; Terra handled cross-layer repairs but required stronger process constraints; gpt-5.4 was slow but highly effective as an adversarial reviewer.

## Key Claims

- Cheap authors are safe only when independent review and exact-head evidence remain mandatory.
- Checkpoints must not relax formatting, post-format tests, lint, or normal hooks.
- Review and external evidence latency must be measured separately from author cost.
- Older model names do not guarantee lower end-to-end cost.

## Key Quotes

> "The safe pattern is cheap author plus independent reviewer plus strict exact-head evidence."

## Connections

- [[ModelRouting]] - route by task shape and measured convergence cost.
- [[EvidenceReview]] - exact-head evidence remains independent of author claims.
- [[Parallelization]] - independent PR lanes are safe to parallelize.

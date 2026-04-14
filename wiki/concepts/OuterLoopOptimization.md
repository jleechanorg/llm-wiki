---
title: "OuterLoopOptimization"
type: concept
tags: [outer-loop, inner-loop, loop-distinction, meta-harness, harness-engineering]
sources: [meta-harness-paper]
last_updated: 2026-04-14
---

## Summary

Outer Loop Optimization refers to the distinction between optimizing the harness code (outer loop) versus optimizing the LLM inference itself (inner loop). The outer loop searches over harness code to determine what information to store, retrieve, and present to the model. The inner loop is the LLM inference step. Research demonstrates that harness changes alone (outer loop) can produce a 6x performance gap on a fixed model. Meta-Harness automates the outer loop.

## Key Claims

- Outer loop optimizes harness code; inner loop is LLM inference
- Harness changes (outer loop) produce 6x performance gap on fixed model
- Prior text optimizers operate on the outer loop but with severe limitations: memoryless, scalar scores only, compressed feedback, 100-30K tokens vs 10M tokens
- Meta-Harness enables full outer loop optimization with 10M tokens per evaluation
- 82 files per iteration, 20+ prior candidates referenced per step

## Connections

- [[MetaHarness]] — the system that automates outer loop optimization
- [[HarnessEngineering]] — the practice of outer loop changes
- [[InnerLoop]] — the LLM inference step that outer loop changes affect

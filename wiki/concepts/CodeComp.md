---
title: "CodeComp"
type: concept
tags: [agent-improvement, kv-cache-compression, code-property-graph, static-analysis, memory-efficiency, agentic-coding]
sources: [code-comp-paper]
last_updated: 2026-04-14
---

## Definition

Structural KV cache compression for agentic coding that integrates Code Property Graph (CPG) analysis via Joern into LLM inference. Training-free method that preserves structurally critical code tokens during compression, outperforming attention-only compression baselines.

## Core Insight

Attention-only KV cache compression drops structurally important tokens (function call sites, branch conditions, variable assignments) because they may not have high attention scores at inference time. Using static program analysis (CPGs) to identify structurally critical tokens ensures they survive compression.

## Technical Approach

1. **Extract CPGs** from codebases using Joern static analysis
2. **Identify structurally critical tokens** (function calls, branch conditions, assignments)
3. **Preserve structural tokens** during KV cache compression
4. **Compress non-structural tokens** aggressively
5. No fine-tuning or model modification required

## Key Results

- Outperforms attention-only compression at equivalent memory budgets
- Recovers majority of full-context accuracy under aggressive compression
- Matches full-context quality on patch generation
- Compatible with SGLang-based agentic coding pipelines

## Related Concepts

- [[KVCacheCompression]] — CodeComp is a specific technique within this category
- [[CodePropertyGraph]] — the static analysis structure that drives compression decisions
- [[AgentArchitecture]] — addresses memory/architecture constraints for coding agents
- [[StaticAnalysis]] — Joern/CPG-based static analysis is the compression signal

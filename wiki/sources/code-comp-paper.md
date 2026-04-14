---
title: "CodeComp: Structural KV Cache Compression for Agentic Coding"
type: source
tags: [agent-improvement, kv-cache-compression, code-property-graph, static-analysis, memory-efficiency, agentic-coding]
sources: []
last_updated: 2026-04-14
---

## Summary

CodeComp (arXiv:2604.10235) addresses the KV cache memory bottleneck in agentic coding tasks by integrating static program analysis (via Code Property Graphs extracted with Joern) into LLM inference for training-free KV cache compression. Existing compression methods rely only on attention scores, which drop structurally critical tokens like function call sites, branch conditions, and variable assignments. CodeComp preserves tokens that are structurally important to the code, recovering most full-context accuracy even under aggressive compression and matching full-context quality on patch generation.

## Key Claims

- Training-free: no fine-tuning or model modification required
- Outperforms attention-only compression baselines under equivalent memory budgets
- Recovers majority of full-context accuracy under aggressive KV cache compression
- Matches full-context quality on patch generation tasks
- Compatible with SGLang-based agentic coding pipelines
- Uses Joern for Code Property Graph extraction

## Key Quotes

> "Existing compression methods rely only on attention scores, which causes them to drop structurally critical tokens like function call sites, branch conditions, and variable assignments." — CodeComp paper

## Technical Approach

**Problem**: When LLMs process long codebases for agentic coding (bug localization, patch generation), KV cache dominates memory usage.

**Solution — CodeComp**: Training-free KV cache compression integrating Code Property Graph (CPG) priors:
1. Extract CPGs from codebases using **Joern** static analysis tool
2. Identify structurally critical tokens (function call sites, branch conditions, variable assignments)
3. Preserve these structurally important tokens during KV cache compression
4. Compress non-structural tokens aggressively

**Compatibility**: Works with SGLang-based agentic coding pipelines without modification.

## Connections

- [[AgentArchitecture]] — addresses a core memory/architecture constraint for coding agents
- [[KVCacheCompression]] — CodeComp is a specific technique within this broader category
- [[StaticAnalysis]] — uses program analysis (CPG/Joern) as the compression signal

## Contradictions

- None

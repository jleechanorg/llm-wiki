---
title: "MetaHarness"
type: concept
tags: [meta-harness, outer-loop-optimization, harness-engineering, agentic-proposer]
sources: [meta-harness-paper]
last_updated: 2026-04-14
---

## Summary

Meta-Harness is an outer-loop system that searches over harness code for LLM applications. Unlike prior text optimizers that compress feedback to short templates and summaries, Meta-Harness uses an agentic proposer that accesses full source code, execution traces, and scores through a filesystem interface. It achieves 7.7 point improvement on text classification with 4x fewer tokens, 4.7 point improvement on 200 IMO problems, and ranked #1 on TerminalBench-2 among all Claude Haiku 4.5 agents.

## Key Claims

- The core insight: richer access to prior experience enables automated harness engineering. Full source code + execution traces + scores through filesystem >> compressed summaries
- Prior text optimizers fail on harness engineering because they are memoryless (condition only on current candidate), rely on scalar scores only, restrict feedback to short templates, and operate on 100-30K tokens vs 10M tokens available to harness search
- Agentic proposer reads source code, invokes developer tools, and modifies code directly
- Filesystem-based history stores all prior candidates as files (source, scores, traces) rather than compressed summaries
- Standard filesystem operations (grep/cat) are used rather than ingesting all context as a prompt
- Median 82 files read per iteration, referencing 20+ prior candidates per step
- 10,000,000 tokens per evaluation vs 30K max in prior text optimizers

## Connections

- [[HarnessEngineering]] — the practice of refining code around an LLM that Meta-Harness automates
- [[AgenticProposer]] — the coding agent that searches the harness code space
- [[FilesystemHistory]] — the full history storage pattern enabling selective diagnosis
- [[OuterLoopOptimization]] — the outer-loop vs inner-loop distinction that defines what Meta-Harness optimizes

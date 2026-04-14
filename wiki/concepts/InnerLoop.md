---
title: "Inner Loop"
type: concept
tags: [inner-loop, outer-loop, inference, meta-harness]
sources: [meta-harness-paper]
last_updated: 2026-04-14
---

## Summary

The Inner Loop refers to the LLM inference step itself — the moment when the model generates a response given the current context and harness configuration. This is distinguished from the Outer Loop, which is the process of searching over harness configurations to determine what information to present to the model.

## Key Claims

- Inner loop is the LLM inference step; outer loop searches over harness code
- Harness changes (outer loop) produce a 6x performance gap on a fixed model
- Prior text optimizers fail because they treat the problem as inner loop optimization (adjusting prompts) rather than outer loop (adjusting harness code)
- Meta-Harness demonstrates that automating outer loop changes outperforms manual prompt engineering

## The Core Distinction

| Aspect | Inner Loop | Outer Loop |
|--------|------------|------------|
| What changes | Prompt/query to model | Harness code surrounding the model |
| What it controls | What is sent to the LLM | What information is stored, retrieved, and presented |
| Typical optimization | Prompt engineering | Filesystem history, retrieval strategies, context management |
| Meta-Harness contribution | Not optimized | 10M tokens per evaluation, full source code access |

## Connections

- [[OuterLoopOptimization]] — the outer loop that Meta-Harness automates
- [[MetaHarness]] — the system that achieves superior results by optimizing the outer loop
- [[HarnessEngineering]] — the practice of building harnesses that make outer loop efficient

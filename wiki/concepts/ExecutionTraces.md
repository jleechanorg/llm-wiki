---
title: "Execution Traces"
type: concept
tags: [execution-traces, traces, debugging, feedback, meta-harness]
sources: [meta-harness-paper]
last_updated: 2026-04-14
---

## Summary

Execution traces are records of program execution — the sequence of function calls, inputs, outputs, and state changes that occur when code runs. Meta-Harness uses execution traces as a primary source of feedback, enabling the agentic proposer to understand not just whether something failed, but exactly how and why it failed.

## Key Claims

- Execution traces provide full fidelity information about program behavior
- Meta-Harness stores traces as files in its filesystem-based history
- Traces enable selective diagnosis — agent reads specific trace segments
- Full source code + execution traces + scores >> compressed summaries
- 82 files per iteration median, including trace files
- Prior text optimizers cannot access execution traces — only scalar scores

## Why Execution Traces Matter

| Aspect | Scalar Scores | Execution Traces |
|--------|--------------|------------------|
| Information | Pass/fail | Full execution path |
| Debugging | Limited | Rich diagnostic data |
| Actionability | Just "try again" | Specific failure points |
| Prior candidate analysis | Current only | Detailed history |

## Connections

- [[FilesystemHistory]] — traces are stored as files in Meta-Harness history
- [[AgenticProposer]] — uses traces to diagnose failures
- [[FeedbackLoop]] — traces provide rich feedback for the loop
- [[MetaHarness]] — enables access to full execution traces
- [[AlphaEvolv]] — contrast: AlphaEvolv uses only scalar scores

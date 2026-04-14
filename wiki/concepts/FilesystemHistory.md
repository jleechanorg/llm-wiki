---
title: "FilesystemHistory"
type: concept
tags: [filesystem-history, full-history, storage-pattern, meta-harness]
sources: [meta-harness-paper]
last_updated: 2026-04-14
---

## Summary

Filesystem History is a storage pattern used by Meta-Harness where prior candidates are stored as files (source code, scores, execution traces) rather than compressed summaries. This pattern enables selective diagnosis — the agent can read specific files to understand what worked and what failed without being forced to compress or truncate history. Meta-Harness stores a median of 82 files per iteration using this pattern.

## Key Claims

- Prior candidates stored as files (source code, scores, traces) rather than compressed summaries
- Enables selective diagnosis — agent reads only what it needs rather than processing all history as prompt
- Supports access to full fidelity information: source, scores, and execution traces
- 82 files per iteration median storage overhead
- Full source code + execution traces + scores through filesystem >> compressed summaries
- Enables the agentic proposer to reference 20+ prior candidates per step

## Connections

- [[AgenticProposer]] — the agent that reads from filesystem history to make decisions
- [[MetaHarness]] — the system that uses filesystem history as its memory model

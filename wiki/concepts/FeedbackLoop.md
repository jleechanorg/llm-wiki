---
title: "Feedback Loop"
type: concept
tags: [feedback-loop, iteration, learning, improvement]
sources: [meta-harness-paper]
last_updated: 2026-04-14
---

## Summary

A feedback loop is the iterative process where system outputs are fed back as inputs for future iterations. In the context of Meta-Harness and harness engineering, the feedback loop is the core mechanism enabling iterative improvement. Meta-Harness achieves superior feedback through filesystem-based history that provides full code, execution traces, and scores rather than compressed summaries.

## Key Claims

- Feedback loops enable iterative improvement in optimization systems
- Meta-Harness uses a richer feedback loop than prior text optimizers
- Full source code + execution traces + scores enable better diagnosis
- Filesystem-based history allows selective reading of relevant feedback
- 20+ prior candidates referenced per step — deep feedback history

## Feedback Quality Spectrum

| System | Feedback Type | Tokens per Step | Prior Access |
|--------|--------------|-----------------|--------------|
| Basic iteration | Pass/fail only | N/A | None |
| AlphaEvolv | Scalar scores | 100-30K | Memoryless |
| ACE | Compressed summaries | 100-30K | Memoryless |
| Meta-Harness | Full code + traces + scores | 10M | 20+ candidates |

## Connections

- [[MetaHarness]] — uses the richest feedback loop in harness optimization
- [[DeterministicFeedbackLoops]] — deterministic responses in agent-orchestrator
- [[FilesystemHistory]] — enables rich feedback storage and retrieval
- [[ExecutionTraces]] — component of Meta-Harness feedback
- [[ExperienceReplay]] — similar concept in reinforcement learning

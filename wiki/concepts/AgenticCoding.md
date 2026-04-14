---
title: "Agentic Coding"
type: concept
tags: [agentic-coding, coding-agent, software-development, AI-engineering]
sources: [meta-harness-paper]
last_updated: 2026-04-14
---

## Summary

Agentic Coding is the practice of using AI agents to autonomously perform software development tasks — reading source code, invoking developer tools, and modifying code directly. The Agentic Proposer within Meta-Harness is an example of an agentic coder applied specifically to harness engineering.

## Key Claims

- Agentic coders read source code, invoke developer tools, and modify code directly
- Must decide what to inspect given context window limits are routinely exceeded
- Meta-Harness uses standard filesystem operations (grep/cat) rather than ingesting all context as prompt
- Agentic proposer achieves 10M tokens per evaluation vs 30K max in prior text optimizers
- Reads median 82 files per iteration, referencing 20+ prior candidates per step

## Comparison to Traditional Coding

| Aspect | Traditional Coding | Agentic Coding |
|--------|-------------------|----------------|
| Who writes code | Human | AI agent |
| Context access | Human memory + docs | Full source + traces + scores via filesystem |
| Iteration speed | Slower (human bottleneck) | Faster (agent can iterate autonomously) |
| Optimization scope | Single solution | Searches over solution space |

## Connections

- [[AgenticProposer]] — the specific agentic coder used in Meta-Harness
- [[CodingAgent]] — broader concept of agents that write code
- [[SelfImproving]] — agentic systems that improve through feedback
- [[MetaHarness]] — uses agentic coding to search over harness configurations

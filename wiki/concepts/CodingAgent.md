---
title: "Coding Agent"
type: concept
tags: [coding-agent, software-engineering-agent, autonomous-coding, AI-engineering]
sources: [meta-harness-paper]
last_updated: 2026-04-14
---

## Summary

A coding agent is an AI system capable of autonomously performing software development tasks — reading code, understanding project structure, invoking developer tools, and modifying code. The Agentic Proposer in Meta-Harness is a specialized coding agent that searches over harness configurations to optimize LLM applications.

## Key Claims

- Coding agents can read source code, invoke tools, and modify code directly
- Must handle context limits by using selective retrieval strategies
- Meta-Harness uses filesystem operations (grep/cat) rather than ingesting all code
- Achieves 10M tokens per evaluation despite context limits
- Median 82 files read per iteration, referencing 20+ prior candidates

## Key Capabilities

| Capability | Description |
|------------|-------------|
| Code reading | Parse and understand source code structure |
| Tool invocation | Use grep, cat, and other filesystem tools |
| Code modification | Edit source files to implement changes |
| Selective retrieval | Read only relevant files given context limits |
| History awareness | Learn from prior attempts via experience replay |

## Connections

- [[AgenticCoding]] — the practice coding agents embody
- [[AgenticProposer]] — the specific coding agent in Meta-Harness
- [[TerminalBench]] — benchmark for evaluating coding agents
- [[TerminalBench-2]] — the version where Meta-Harness achieved #1
- [[MetaHarness]] — uses coding agents for harness optimization
- [[SelfImproving]] — coding agents that improve through feedback

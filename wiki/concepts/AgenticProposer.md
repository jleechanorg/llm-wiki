---
title: "AgenticProposer"
type: concept
tags: [agentic-proposer, meta-harness, coding-agent, filesystem-history]
sources: [meta-harness-paper]
last_updated: 2026-04-14
---

## Summary

The Agentic Proposer is the coding agent within Meta-Harness responsible for searching over harness code. It reads source code, invokes developer tools, and modifies code directly. A critical challenge it faces is deciding what to inspect given context window limits are routinely exceeded. The proposer uses standard filesystem operations (grep and cat) rather than ingesting all context as a prompt, enabling it to access full source code, execution traces, and scores.

## Key Claims

- Reads source code, invokes developer tools, and modifies code directly
- Must decide what to inspect since context limits are routinely exceeded
- Uses filesystem operations (grep/cat) rather than ingesting all context as prompt
- Has access to full source code, execution traces, and scores through filesystem interface
- Reads median 82 files per iteration and references 20+ prior candidates per step
- Operates with 10,000,000 tokens per evaluation

## Connections

- [[MetaHarness]] — the system within which the agentic proposer operates
- [[FilesystemHistory]] — the storage pattern that enables the proposer to access prior candidates
- [[AgenticCoding]] — the broader practice of using coding agents for software development tasks

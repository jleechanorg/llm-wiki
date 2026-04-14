---
title: "TerminalBench"
type: concept
tags: [TerminalBench, benchmark, coding-agent, agentic-coding, terminal]
sources: [meta-harness-paper]
last_updated: 2026-04-14
---

## Summary

TerminalBench is a benchmark for evaluating coding agents on terminal-based software engineering tasks. It tests agents' ability to navigate, understand, and modify complex codebases through command-line interfaces. Meta-Harness achieved #1 ranking on TerminalBench-2 among all Claude Haiku 4.5 agents, surpassing Terminus-KIRA.

## Key Claims

- TerminalBench evaluates agents on realistic terminal-based coding tasks
- Tests ability to navigate large codebases, understand structure, and make targeted changes
- Meta-Harness ranked #1 on TerminalBench-2 among all Claude Haoku 4.5 agents
- Outperformed Terminus-KIRA (previous state-of-the-art)
- Demonstrates that outer loop optimization improves agentic coding performance

## Benchmark Structure

TerminalBench typically includes:
- Repository navigation tasks
- Bug identification and fixing
- Feature implementation
- Test writing and execution
- Multi-step code modifications

## Connections

- [[TerminalBench-2]] — the specific benchmark version where Meta-Harness achieved #1
- [[MetaHarness]] — achieved #1 ranking through outer loop optimization
- [[CodingAgent]] — the type of agent evaluated by TerminalBench
- [[AgenticCoding]] — the practice being benchmarked

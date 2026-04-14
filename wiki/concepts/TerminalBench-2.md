---
title: "TerminalBench-2"
type: concept
tags: [TerminalBench-2, benchmark, coding-agent, agentic-coding, terminal]
sources: [meta-harness-paper]
last_updated: 2026-04-14
---

## Summary

TerminalBench-2 is the benchmark on which Meta-Harness achieved #1 ranking among all Claude Haiku 4.5 agents, surpassing Terminus-KIRA. It represents the state-of-the-art evaluation for coding agents on terminal-based software engineering tasks.

## Key Claims

- Meta-Harness achieved #1 ranking on TerminalBench-2 among all Claude Haiku 4.5 agents
- Surpassed Terminus-KIRA (previous state-of-the-art)
- Demonstrates that outer loop optimization (optimizing harness code) improves agentic coding performance
- TerminalBench-2 is specifically mentioned in the paper as the benchmark where Meta-Harness excels
- Combined with IMO math problems (200 problems, +4.7 points improvement)

## Results Summary

| Task | Meta-Harness Result |
|------|---------------------|
| Text classification | +7.7 points over ACE, 4x fewer tokens |
| IMO math (200 problems) | +4.7 points average across 5 models |
| TerminalBench-2 coding | #1 among Claude Haiku 4.5 agents |

## Connections

- [[TerminalBench]] — the broader benchmark family
- [[MetaHarness]] — the system that achieved #1 ranking
- [[CodingAgent]] — the type of agent being evaluated
- [[AgenticCoding]] — the practice improved by Meta-Harness

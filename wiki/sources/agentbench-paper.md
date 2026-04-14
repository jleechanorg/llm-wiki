---
title: "AgentBench: Evaluating LLMs as Agents"
type: source
tags: [benchmark, agent-evaluation, decision-making, reasoning, multi-environment]
sources: []
date: 2023-08-07
source_file: raw/arxiv-2311.05964-agentbench.md
---

## Summary

AgentBench is a multi-dimensional benchmark with 8 distinct environments for assessing LLM-as-Agent's reasoning and decision-making abilities. It evaluates both API-based and open-source LLMs. The study finds commercial LLMs significantly outperform open-source competitors up to 70B, with main obstacles being poor long-term reasoning, decision-making, and instruction following.

## Key Claims

- **Commercial LLMs outperform** many open-source competitors ≤70B on agent tasks
- **Main obstacles**: poor long-term reasoning, decision-making, and instruction following
- Improving instruction following and multi-round alignment data enhances performance
- Training on code shows "ambivalent impacts" on different agent tasks
- 8 distinct evaluation environments covering diverse agent scenarios

## Technique/Method

- Multi-environment benchmark: 8 different task environments (OS, DB, KG, knowledge graphs, etc.)
- Tests both API-accessible (GPT-4, Claude) and open-source models
- Evaluates long-horizon reasoning and multi-step decision making
- Real-world environment interaction vs. synthetic benchmarks

## Connections

- Core benchmark for agent evaluation
- Evidence base for coding agent capability assessment
- Related to EvoEval on benchmark integrity
- Connects to harness engineering: environment design as harness

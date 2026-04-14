---
title: "OpenHands: An Open Platform for AI Software Developers"
type: paper
tags: [open-source, coding-agent, platform, evaluation, SWE-bench]
date: 2024-12-31
arxiv_url: https://arxiv.org/abs/2412.21130
---

## Summary
OpenHands is an open-source platform for AI-powered software development, designed to enable reproducible research and evaluation of coding agents. It provides a standardized environment for running coding agent experiments, with integration for SWE-bench, HumanEval, and other benchmarks. The platform emphasizes reproducibility and extensibility for the research community.

## Key Claims
- Open-source platform for reproducible coding agent research
- Standardized environment for agent evaluation
- Integration with major coding benchmarks (SWE-bench, HumanEval, etc.)
- Emphasis on reproducibility and extensibility
- Enables fair comparison across different agent approaches

## Technique/Method
- Containerized evaluation environments
- Standardized agent interface definition
- Benchmark integration framework
- Action space specification for coding agents
- Sandboxed execution for safety

## Results
- Enables reproducible agent evaluation across research groups
- Standardized comparison of agent approaches
- Growing community adoption and benchmark coverage

## Limitations
- Benchmark coverage may lag behind new agent capabilities
- Container overhead may limit execution speed
- Open-source nature means varied quality across contributions

## Connections
- Core platform for [[PRWatchdog]]-style automated agent evaluation
- Relevant to [[AgentBench]] multi-environment evaluation approach
- Supports open research reproducibility for coding agent evaluation

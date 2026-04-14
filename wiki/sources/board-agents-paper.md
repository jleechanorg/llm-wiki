---
title: "BOAD: Discovering Hierarchical Software Engineering Agents via Bandit Optimization"
type: source
tags: [multi-agent, hierarchy, SWE-bench, bandit-optimization, SWE-agent]
sources: []
date: 2025-12-29
source_file: raw/arxiv-2512.23631-boarding-agents.md
---

## Summary

Discovers hierarchical agent architectures via multi-armed bandit optimization. Decomposes into specialized sub-agents (localization, editing, validation) coordinated by an orchestrator. On SWE-bench-Live, 36B system ranked **2nd on leaderboard**, surpassing GPT-4 and Claude.

## Key Claims

- Single-agent systems cause "spurious correlations and poor generalization"
- Human-inspired decomposition into specialized sub-agents improves performance
- **36B ranked 2nd on SWE-bench-Live**, surpassing GPT-4 and Claude

## Technique/Method

- Frames agent hierarchy discovery as **multi-armed bandit problem**
- Each arm = candidate sub-agent; reward = collaborative helpfulness
- Orchestrator coordinates specialized sub-agents

## Connections

- Related to [[MetaGPT]] — multi-agent role assignment
- Related to [[AgentMentor]] — specialized sub-agent guidance

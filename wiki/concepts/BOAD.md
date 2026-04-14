---
title: "BOAD"
type: concept
tags: [multi-agent, hierarchy, SWE-bench, bandit-optimization]
sources: [board-agents-paper]
last_updated: 2026-04-14
---

Discovers hierarchical agent architectures via multi-armed bandit optimization. Decomposes SWE tasks into specialized sub-agents coordinated by an orchestrator.

## Key Insight

> "Single-agent systems force models to retain irrelevant context, leading to spurious correlations and poor generalization."

## Architecture

```
Orchestrator (MAB)
├── Localization Sub-Agent
├── Editing Sub-Agent
└── Validation Sub-Agent
```

## Results

- **36B ranked 2nd on SWE-bench-Live** leaderboard
- Surpasses GPT-4 and Claude
- Outperforms single-agent and manually-designed multi-agent baselines

## Connections

- Related to [[MetaGPT]] — multi-agent role assignment
- [[AgentMentor]] — specialized sub-agent guidance
- [[RepoNavigator]] — single-tool vs multi-agent tradeoffs

---
title: "RepoNavigator"
type: concept
tags: [coding-agent, RL, SWE-bench, repository-level, tool-use]
sources: [one-tool-is-enough-paper]
last_updated: 2026-04-14
---

SOTA repository-level coding agent using single execution-aware tool with end-to-end RL training. 7B outperforms 14B; 14B surpasses 32B; 32B exceeds GPT-5 on most metrics.

## Key Finding

> "One tool is enough" — single unified tool reflecting actual code execution flow outperforms complex multi-tool approaches.

## Scaling Results

| Model Size | Performance |
|-----------|-------------|
| 7B | Outperforms 14B baselines |
| 14B | Surpasses 32B competitors |
| 32B | Exceeds GPT-5 on most metrics |

## Connections

- Related to [[SWE-Shepherd]] — RL-based step guidance
- [[LargeLanguageMonkeys]] — scaling via repeated sampling
- [[E3-TIR]] — tool-integrated reasoning

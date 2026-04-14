---
title: "One Tool Is Enough: RL for Repository-Level LLM Agents"
type: source
tags: [coding-agent, RL, SWE-bench, repository-level, tool-use]
sources: []
date: 2025-12-24
source_file: raw/arxiv-2512.20957-one-tool-is-enough.md
---

## Summary

RepoNavigator achieves SOTA using a single execution-aware tool with end-to-end RL training. Key finding: 7B outperforms 14B baselines; 14B surpasses 32B competitors; 32B exceeds GPT-5 on most SWE-bench metrics.

## Key Claims

- **RepoNavigator**: single unified tool reflecting actual code execution flow
- End-to-end RL training from base pretrained model (no closed-source distillation)
- **7B** outperforms 14B baselines; **14B** surpasses 32B competitors
- **32B** exceeds GPT-5 on most evaluation metrics

## Technique/Method

- Single execution-aware tool: jumping to symbol definitions
- Reinforcement Learning training from base pretrained model
- Addresses repository-level issue localization in large codebases

## Results

- Strong cross-model-size performance improvements
- Exceeds closed-source models (GPT-5) with 32B parameters
- SOTA on SWE-bench metrics

## Connections

- Related to [[SWE-Shepherd]] — RL-based step guidance
- Related to [[LargeLanguageMonkeys]] — scaling via RL
- [[E3-TIR]] extends tool-integrated reasoning

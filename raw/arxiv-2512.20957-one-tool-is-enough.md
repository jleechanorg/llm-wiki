---
title: "One Tool Is Enough: Reinforcement Learning for Repository-Level LLM Agents"
type: paper
tags: [coding-agent, RL, SWE-bench, repository-level, tool-use]
date: 2025-12-24
arxiv_url: https://arxiv.org/abs/2512.20957
---

## Summary

RepoNavigator achieves SOTA using a single execution-aware tool (jumping to symbol definitions) with end-to-end RL training. Key finding: 7B outperforms 14B baselines; 14B surpasses 32B competitors; 32B exceeds GPT-5 on most SWE-bench metrics.

## Key Claims

- **RepoNavigator**: single unified tool reflecting actual code execution flow
- End-to-end RL training from base pretrained model (no closed-source distillation)
- **7B** outperforms 14B baselines; **14B** surpasses 32B competitors
- **32B** exceeds GPT-5 on most evaluation metrics
- SOTA on repository-level issue localization

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

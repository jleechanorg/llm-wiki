---
title: "Kimi k1.5"
type: concept
tags: [RL, reinforcement-learning, reasoning, coding, multimodal]
sources: [kimi-k1-5-paper]
last_updated: 2026-04-14
---

Multi-modal LLM trained with reinforcement learning. Key finding: scaling RL unlocks new improvement axis beyond pretraining. Simplistic framework — no MCTS, value functions, or process reward models — yet achieves SOTA reasoning.

## Key Results

| Benchmark | Score |
|-----------|-------|
| AIME | 77.5 |
| MATH 500 | 96.2 |
| Codeforces | 94th percentile |
| Matched OpenAI o1 on reasoning benchmarks |

## Long2Short Method

Distilling long-CoT reasoning quality into short-CoT models:
- Outperforms GPT-4o and Claude Sonnet 3.5 by up to +550% on short-CoT benchmarks
- Enables efficient deployment of reasoning-capable models

## Connections

- Evidence for RLVR (Reinforcement Learning with Verifiable Rewards)
- Related to [[RefineRL]] — RL-based refinement
- Long context scaling relevant to [[DeepSeek-Coder-V2]] approach

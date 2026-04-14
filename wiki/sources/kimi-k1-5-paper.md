---
title: "Kimi k1.5: Scaling Reinforcement Learning with LLMs"
type: source
tags: [RL, reinforcement-learning, RLVR, reasoning, coding, multimodal]
sources: []
date: 2025-01-22
source_file: raw/arxiv-2501.12599-kimi-k1-5.md
---

## Summary

Kimi k1.5 is a multi-modal LLM trained with reinforcement learning, demonstrating that scaling RL unlocks a new axis for AI improvement beyond just pretraining. The framework is deliberately simplistic — no Monte Carlo tree search, value functions, or process reward models — yet achieves state-of-the-art reasoning performance across multiple benchmarks. Long context scaling and improved policy optimization are identified as key ingredients.

## Key Claims

- Achieves **77.5 on AIME**, **96.2 on MATH 500**, **94th percentile on Codeforces**, **74.9 on MathVista**
- Matches OpenAI's o1 on reasoning benchmarks
- Long2short methods yield state-of-the-art short-CoT reasoning, outperforming GPT-4o and Claude Sonnet 3.5 by up to **+550%**
- "Simplistic" RL framework — no MCTS, value functions, or process reward models needed
- Long context scaling + improved policy optimization are key ingredients

## Technique/Method

- Long context scaling for RL training
- Improved policy optimization techniques
- Long2short: distilling long-CoT reasoning quality into short-CoT models
- Multimodal training (not just text)
- Rewards drive exploration — no complex planning infrastructure needed

## Connections

- Strong evidence for RLVR (Reinforcement Learning with Verifiable Rewards) approach
- Relevant to chain-of-thought and extended reasoning research
- Long2short insight applicable to coding agent efficiency

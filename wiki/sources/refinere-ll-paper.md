---
title: "RefineRL: Advancing Competitive Programming with Self-Refinement Reinforcement Learning"
type: source
tags: [self-refinement, reinforcement-learning, competitive-programming, llm]
sources: []
last_updated: 2026-04-14
---

## Summary

RefineRL addresses the gap in LLM research on multi-attempt settings for competitive programming — existing methods focus on single-attempt performance while overlooking the capacity for iterative refinement. The paper introduces a Skeptical-Agent that maintains a skeptical attitude toward its own outputs even after initial validation passes, paired with RL training to incentivize self-refinement using only standard RLVR data (problems with verifiable answers). A compact 4B model with this approach surpasses 32B model performance and approaches the single-attempt results of 235B models.

## Key Claims

- Self-refinement holds considerable promise for scaling LLM reasoning beyond single-attempt ceilings
- A skeptical mindset toward one's own outputs is essential — solutions that pass public tests may still harbor hidden flaws
- RL training can incentivize self-refinement without requiring special refinement annotations or multi-turn data
- Compact 4B models integrated with RefineRL approach the single-attempt performance of 235B models
- The Skeptical-Agent uses local execution tools to validate against public test cases while maintaining ongoing skepticism

## Methodology

1. **Skeptical-Agent**: An iterative self-refinement agent that always maintains skepticism toward its own outputs, using local execution tools to validate solutions against public test cases even when initial validation suggests correctness
2. **RL Training**: A reinforcement learning solution to incentivize LLMs to self-refine using only standard RLVR data — problems paired with verifiable answers, no special refinement annotations required

## Results

- Tested on Qwen3-4B and Qwen3-4B-2507 models
- 4B models with Skeptical-Agent surpass 32B model performance
- Performance approaches the single-attempt results of 235B models
- Substantial gains demonstrated on competitive programming benchmarks

## Connections

- [[SelfRefine]] — the general concept of LLM self-refinement that RefineRL builds upon
- [[ThinkTwice]] — another self-refinement approach for reasoning tasks
- [[ReinforcementLearning]] — the RL training methodology used
- [[CompetitiveProgramming]] — the domain of application

## Authors

Shaopeng Fu, Xingxing Zhang, Li Dong, Di Wang, Furu Wei

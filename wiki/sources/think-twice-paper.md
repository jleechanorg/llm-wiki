---
title: "ThinkTwice: Jointly Optimizing Large Language Models for Reasoning and Self-Refinement"
type: source
tags: [self-refinement, reasoning, grpo, joint-optimization, mathematics]
sources: []
last_updated: 2026-04-14
---

## Summary

ThinkTwice is a two-phase framework that jointly optimizes LLMs for both reasoning and self-refinement using Group Relative Policy Optimization (GRPO). Phase 1 optimizes on solving reasoning problems, while Phase 2 optimizes on refining solutions — both using the same binary correctness reward, with no correctness signals or critique annotations required. On Qwen3-4B AIME, it outperforms GRPO by 11.5 percentage points after a single self-refinement step.

## Key Claims

- Joint training of reasoning and self-refinement is an effective methodology for RLVR (Reinforcement Learning from Verifiable Rewards)
- Self-refinement provides substantial additional gains over strong base reasoning — 11.5pp improvement on AIME after one refinement step
- No explicit critique annotations or correctness signals are needed — the binary correctness reward alone is sufficient
- The two-phase approach (solve then refine) enables both tasks to benefit from shared optimization
- GRPO provides a stable training signal for both phases

## Methodology

1. **Phase 1 (Solve)**: Optimizes the model on solving reasoning problems using GRPO with binary correctness reward
2. **Phase 2 (Refine)**: Optimizes the model on refining solutions using the same binary correctness reward — no external critic needed
3. Both phases use GRPO for stable policy optimization
4. The model learns to recognize when its own outputs are incorrect and refine them autonomously

## Results

- Tested on five mathematical reasoning benchmarks
- Models: Qwen3-4B and Olmo3-7B
- On Qwen3-4B AIME: outperforms GRPO by 5pp before refinement and 11.5pp after one self-refinement step (pass@4)
- Substantial improvements on both reasoning and refinement performance

## Connections

- [[SelfRefine]] — the core self-refinement concept ThinkTwice operationalizes
- [[GroupRelativePolicyOptimization]] — GRPO, the RL algorithm used for joint optimization
- [[ChainOfThought]] — reasoning traces that ThinkTwice builds on
- [[RefineRL]] — parallel work on RL-based self-refinement for competitive programming

## Authors

Difan Jiao, Qianfeng Wen, Blair Yang, Zhenwei Tang, Ashton Anderson

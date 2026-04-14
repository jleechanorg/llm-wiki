---
title: "SWE-Shepherd"
type: concept
tags: [process-reward-model, code-agents, swe-bench, step-level-supervision]
sources: [swe-shepherd-paper.md]
last_updated: 2026-04-14
---

## Summary
SWE-Shepherd is a framework that applies Process Reward Models (PRMs) to provide step-level supervision for repository-level code agents. Rather than relying on static prompting or handcrafted heuristics, it trains a lightweight reward model on SWE-Bench trajectories to evaluate intermediate actions during inference, guiding agents toward higher-reward decisions without full reinforcement learning.

## How It Works
1. **Action-level reward dataset**: Constructed from SWE-Bench trajectories capturing real software engineering problem-solving sequences
2. **Lightweight PRM training**: Reward model trained on a base LLM to estimate the usefulness of each intermediate action
3. **Inference-time evaluation**: PRM scores candidate actions at each step and guides the agent toward higher-reward trajectories
4. **No full RL required**: Avoids the complexity of a full reinforcement learning pipeline

## Key Insight
Step-level feedback solves three core problems in code agents: inefficient exploration (agents waste time on dead ends), error propagation (early mistakes compound), and brittle trajectories (agents can't recover when they stray). The PRM acts as a Shepherd, steering the agent away from low-value actions.

## Challenges
Aligning intermediate rewards with final task success is non-trivial — a locally good action may not lead to a globally correct solution, creating reward hacking risk similar to outcome-supervised approaches.

## Connections
- [[ProcessRewardModel]] — the core technique enabling step-level feedback
- [[SWE-Bench]] — benchmark providing training trajectories and evaluation
- [[CodeAgents]] — the target application; long-horizon repository-level tasks
- [[FM-Agent]] — complementary approach: FM-Agent verifies code post-generation, SWE-Shepherd guides generation in real-time

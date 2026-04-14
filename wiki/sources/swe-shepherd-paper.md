---
title: "SWE-Shepherd: Advancing PRMs for Reinforcing Code Agents"
type: source
tags: [process-reward-model, code-agents, swe-bench, step-level-supervision, llm-agents]
sources: []
last_updated: 2026-04-14
---

## Summary
SWE-Shepherd introduces Process Reward Models (PRMs) to provide dense, step-level supervision for repository-level code agents. The framework trains a lightweight reward model on SWE-Bench trajectories to evaluate intermediate actions and guide agents toward better decisions without requiring full reinforcement learning. Evaluated on SWE-Bench Verified, it demonstrates improved interaction efficiency and action quality, while surfacing challenges in aligning intermediate rewards with final task success.

## Key Claims
- PRMs provide fine-grained feedback on intermediate decisions, solving inefficient exploration, error propagation, and brittle solution trajectories
- Action-level reward dataset constructed from SWE-Bench trajectories enables training without full RL
- Lightweight reward model on a base LLM estimates usefulness of intermediate actions at inference time
- Evaluates candidate actions during inference to guide agent toward higher-reward decisions
- Challenges remain in aligning intermediate rewards with final task success

## Key Quotes
> "Existing approaches typically rely on static prompting strategies or handcrafted heuristics to select actions such as code editing, file navigation, and test execution, but they lack fine-grained feedback on intermediate decisions. This leads to inefficient exploration, error propagation, and brittle solution trajectories." — Problem statement

> "SWE-Shepherd introduces Process Reward Models (PRMs) to provide dense, step-level supervision for repository-level code agents." — Core contribution

## Methodology
1. Construct action-level reward dataset from SWE-Bench trajectories (which capture real software engineering problem-solving sequences)
2. Train lightweight reward model on a base LLM to estimate the usefulness of intermediate actions
3. At inference time, PRM evaluates candidate actions and guides the agent toward higher-reward decisions
4. Avoids need for full reinforcement learning pipeline

## Results
- Improved interaction efficiency and action quality on SWE-Bench Verified
- Demonstrates feasibility of step-level guidance for long-horizon code tasks
- Challenges noted in aligning intermediate rewards with final task success (reward hacking/ misalignment)

## Connections
- [[ProcessRewardModel]] — core technique this paper advances
- [[SWE-Bench]] — evaluation benchmark used for training and testing
- [[CodeAgents]] — the target application domain
- [[RLHF]] — PRMs provide an alternative to full RL training for agent guidance

## Paper Info
- **Authors:** Mahir Labib Dihan, Md Ashrafur Rahman Khan
- **arXiv:** 2604.10493
- **GitHub:** https://github.com/mahirlabibdihan/swe-shepherd
- **Submitted:** April 12, 2026
- **Category:** cs.SE

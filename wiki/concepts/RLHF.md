---
title: "RLHF (Reinforcement Learning from Human Feedback)"
type: concept
tags: [RLHF, reinforcement-learning, human-feedback, reward-modeling, alignment]
sources: [external-ai-knowledge-sources]
last_updated: 2026-04-14
---

## Summary

RLHF is a training technique that aligns language models to human preferences by training a reward model from human preference data, then optimizing the policy model against that reward using reinforcement learning (typically PPO). It is the core technique behind InstructGPT, ChatGPT, and Claude's helpfulness training.

## Key Claims

- RLHF significantly improves model helpfulness and harmlessness compared to supervised fine-tuning alone, but the improvement is hard to measure — human preference surveys are the gold standard.
- Reward hacking (reward model exploitation) is a fundamental challenge: models find ways to score high on the reward model without actually being helpful.
- Learning from human feedback at scale requires careful data curation. Preference diversity matters more than sheer volume.
- Constitutional AI (CAI) reduces the need for human labelers by using AI-generated critiques based on a written constitution of principles.
- DPO (Direct Preference Optimization) eliminates the separate reward model and RL step, simplifying the pipeline significantly with comparable results on many tasks.

## The RLHF Pipeline

1. **Supervised Fine-Tuning (SFT)**: Fine-tune base model on curated demonstration data (human-written responses).
2. **Preference Sampling**: Collect human comparisons (which response is better?) for diverse prompts.
3. **Reward Model Training**: Train a reward model on preference data to predict which response humans prefer.
4. **RL Optimization (PPO)**: Optimize the SFT model against the reward model using Proximal Policy Optimization.
5. **Reward Model averaging / early stopping**: Critical to prevent reward hacking — reward model quality degrades as policy improves.

## Challenges and Limitations

- **Reward hacking**: the model learns to exploit reward model weaknesses. KL divergence penalties between policy and SFT model help but don't eliminate it.
- **Human preference noise**: inter-annotator disagreement is high for subjective tasks; this limits reward model quality.
- **Scalar reward sparsity**: most RLHF training signal is negative (model gets low reward for bad responses); positive signal is sparse.
- **Safe reward hacking**: models learn to be sycophantic or evasive rather than genuinely helpful when reward model conflates approval with helpfulness.

## Variants and Alternatives

- **RLAIF**: Replace human preferences with AI-generated preferences (using a stronger model). Scale-friendly but introduces bias.
- **Constitutional AI**: Anthropic's approach where AI critiques its own responses against a written constitution, reducing human labeling cost.
- **DPO**: Direct Preference Optimization — simplifies RLHF by reframing preference learning as a classification task on the policy model itself, eliminating the reward model entirely.
- **PPO with KL constraint**: standard approach, uses KL penalty to keep policy close to SFT baseline.

## Connections

- [[LLM Fine-Tuning]] — RLHF is a specialized fine-tuning technique; understanding fine-tuning fundamentals applies here
- [[Prompt Engineering]] — prompt engineering can often achieve similar results to RLHF for style/format tasks at lower cost
- [[Claude API Best Practices]] — Claude's alignment is achieved through RLHF and Constitutional AI training techniques
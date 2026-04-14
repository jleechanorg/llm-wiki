---
title: "RefineRL"
type: concept
tags: [self-refinement, reinforcement-learning, competitive-programming, skeptical-agent]
sources: [refinere-ll-paper]
last_updated: 2026-04-14
---

## Summary

RefineRL combines a Skeptical-Agent with RL training to enable effective self-refinement for competitive programming. The key insight is that LLMs must maintain skepticism toward their own outputs even after passing public tests, and that RL can incentivize this behavior using only standard problem-answer data without special refinement annotations.

## Key Claims

- Compact 4B models with RefineRL surpass 32B model performance and approach 235B single-attempt results
- Skeptical mindset toward own outputs is essential — correctness signals can be misleading
- RL training generalizes self-refinement without multi-turn data or critique annotations

## How It Works

1. **Skeptical-Agent**: Iterative refinement agent using local execution tools; remains skeptical even when public tests pass
2. **RL Training**: Standard RLVR data (problem + answer pairs) trains the model to self-refine autonomously

## Comparison to Related Concepts

| Aspect | RefineRL | ThinkTwice | Self-Debias |
|---|---|---|---|
| Domain | Competitive programming | Mathematical reasoning | Debiasing |
| Feedback | Public test execution | Binary correctness | Consistency filtering |
| Training | RLVR | GRPO | Trajectory optimization |
| Model scale | 4B surpasses 32B | 4B/7B | Various |

## Related Concepts

- [[SelfRefine]] — general self-refinement framework
- [[ThinkTwice]] — joint reasoning + refinement via GRPO
- [[SelfDebias]] — self-correction for debiasing CoT
- [[AdversarialMCTS]] — adversarial approach to combat pseudo-correctness
- [[ReinforcementLearning]] — RL training methodology

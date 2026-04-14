---
title: "ThinkTwice"
type: concept
tags: [self-refinement, reasoning, grpo, joint-optimization, mathematics]
sources: [think-twice-paper]
last_updated: 2026-04-14
---

## Summary

ThinkTwice is a two-phase GRPO-based framework for jointly optimizing LLMs on reasoning and self-refinement. Phase 1 trains on solving problems, Phase 2 trains on refining incorrect solutions — both using the same binary correctness reward with no critique annotations. Achieves +11.5pp on AIME after one refinement step.

## Key Claims

- Joint training of reasoning and self-refinement is effective for RLVR
- Binary correctness alone is sufficient — no explicit critique signals needed
- One self-refinement step adds 11.5pp on AIME for Qwen3-4B

## How It Works

1. **Phase 1 (Solve)**: GRPO optimization on solving reasoning problems
2. **Phase 2 (Refine)**: GRPO optimization on refining incorrect solutions using same binary reward
3. Model learns to autonomously detect and correct its own errors

## Technique Comparison

| Aspect | ThinkTwice | RefineRL | Self-Debias |
|---|---|---|---|
| Domain | Math reasoning | Competitive programming | Debiasing |
| Algorithm | GRPO | RLVR | Trajectory optimization |
| Feedback | Binary correctness | Public test execution | Consistency filtering |
| Key innovation | Joint optimization | Skeptical agent | Resource redistribution |

## Related Concepts

- [[SelfRefine]] — general self-refinement concept
- [[GroupRelativePolicyOptimization]] — GRPO algorithm
- [[RefineRL]] — RL-based self-refinement for programming
- [[SelfDebias]] — self-correction for debiasing
- [[ChainOfThought]] — reasoning traces being refined

---
title: "SelfDebias"
type: concept
tags: [self-correction, debiasing, chain-of-thought, trajectory-optimization, bias-propagation]
sources: [self-debias-paper]
last_updated: 2026-04-14
---

## Summary

SelfDebias reformulates debiasing as strategic resource redistribution — treating output probability mass as limited resources to be reallocated from biased heuristics to unbiased reasoning paths. It addresses Bias Propagation through CoT reasoning chains via fine-grained trajectory-level optimization with dynamic constraints, achieving superior debiasing with only 20k annotated samples.

## Key Claims

- Bias Propagation through CoT is a distinct problem from static bias — existing methods miss it
- Resource redistribution (probability mass reallocation) outperforms static constraints
- 20k annotated samples is sufficient to activate self-correction
- Selective revision preserves valid prefixes while correcting biased suffixes

## How It Works

1. **Resource Redistribution**: Treat probability mass as limited — reallocate from biased to unbiased paths
2. **Trajectory-Level Optimization**: Fine-grained control at the reasoning-step level, not global
3. **Dynamic Constraints**: Constraints adapt during training, not static rules
4. **Consistency Filtering**: Online self-improvement that synthesizes supervision signals autonomously

## Bias Propagation Problem

Social biases cascade through Chain-of-Thought reasoning:
- Bias in early reasoning steps contaminates all subsequent steps
- Standard debiasing operates on final outputs, missing the propagation
- SelfDebias targets the propagation chain itself

## Related Concepts

- [[SelfRefine]] — general self-correction framework
- [[ChainOfThought]] — the reasoning framework within which bias propagates
- [[TrajectoryOptimization]] — optimization methodology for reasoning traces
- [[ThinkTwice]] — joint reasoning + refinement via GRPO
- [[RefineRL]] — RL-based self-refinement for programming

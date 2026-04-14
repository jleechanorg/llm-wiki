---
title: "Self-Debias: Self-Correcting for Debiasing Large Language Models"
type: source
tags: [self-correction, debiasing, chain-of-thought, trajectory-optimization]
sources: []
last_updated: 2026-04-14
---

## Summary

Self-Debias introduces intrinsic self-correction capabilities for LLMs by reformulating debiasing as strategic resource redistribution — treating output probability mass as a limited resource to be reallocated from biased heuristics to unbiased reasoning paths. Social biases cascade through Chain-of-Thought reasoning, causing continuous "Bias Propagation" that existing static constraint methods fail to address. The framework enables selective revision of biased reasoning suffixes while preserving valid contextual prefixes, achieving superior debiasing with only 20k annotated samples.

## Key Claims

- Social biases cascade through Chain-of-Thought reasoning, causing continuous "Bias Propagation" — a problem existing static methods don't address
- Reformulating debiasing as resource redistribution (probability mass reallocation) is more effective than static constraints
- Fine-grained trajectory-level optimization with dynamic debiasing constraints outperforms global approaches
- Online self-improvement via consistency filtering can autonomously synthesize supervision signals
- Superior debiasing achieved with only 20k annotated samples — efficient activation of self-correction
- Preserves general reasoning capabilities without continuous external oversight

## Methodology

1. **Trajectory-Level Objective**: Fine-grained optimization at the reasoning-step level, subject to dynamic debiasing constraints rather than static rules
2. **Resource Redistribution**: Treats output probability mass as limited resources to be reallocated from biased heuristics to unbiased reasoning paths
3. **Online Self-Improvement**: Uses consistency filtering to autonomously synthesize supervision signals
4. **Selective Revision**: Enables revision of biased reasoning suffixes while preserving valid contextual prefixes

## Results

- Superior debiasing performance compared to baselines
- Maintained general reasoning capabilities after debiasing
- Efficient self-correction activated with limited annotated data (20k samples)
- Reduces bias propagation through CoT reasoning chains

## Connections

- [[ChainOfThought]] — the reasoning framework within which bias propagates
- [[SelfRefine]] — self-correction applied to the debiasing domain
- [[TrajectoryOptimization]] — the optimization methodology for reasoning traces
- [[BiasPropagation]] — the specific problem Self-Debias addresses

## Authors

Xuan Feng, Shuai Zhao, Luwei Xiao, Tianlong Gu, Bo An

---
title: SelfRefine
type: concept
tags: [self-critique, iterative-refinement, multi-aspect-feedback]
date: 2026-04-23
sources: [chimera-p13-findings]
---

## Definition
SelfRefine (Madaan et al., NeurIPS 2023) is an iterative refinement framework where a model generates output, receives multi-dimensional feedback, and revises based on that feedback. The key insight is that a single critique is insufficient — models benefit from multi-aspect feedback that separates concerns (accuracy, clarity, efficiency, etc.).

## Key Mechanism
1. Generate initial output
2. Multi-aspect feedback (not a single critique)
3. Iterative refinement
4. Final output

## Connection to Chimera
Chimera's GNN 3-perspective architecture instantiates the SelfRefine principle as a graph neural network over three critique perspectives, where each perspective processes its own view of the reasoning trace and the GNN aggregates these into a fused signal. This preserves critique diversity during aggregation — unlike simple voting/merging which dilutes perspective-specific signals.

## Key Quote
> "The GNN allows perspectives to selectively reinforce or suppress each other's outputs based on learned graph structure over the reasoning trace"

## Reference
- https://arxiv.org/abs/2303.17760
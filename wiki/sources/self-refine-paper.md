---
title: "Self-Refine: Iterative Refinement with Self-Feedback"
type: source
tags: [self-refine, self-critique, iterative-refinement, self-feedback, Madaan, NeurIPS-2023]
date: 2026-04-14
source_file: arxiv.org/abs/2308.00451
---

## Summary

Self-Refine (Madaan et al., NeurIPS 2023) demonstrates that structured self-critique + revision loops improve code generation by ~20% average across tasks. Agent generates code → critiques itself against criteria → revises → repeat until clean. Foundation for modern self-critique loops in production coding agents.

**Paper:** arxiv.org/abs/2308.00451
**Authors:** Aman Madaan, et al.

## Key Claims

### Framework
1. Generate initial output
2. Critique against explicit criteria (correctness, efficiency, style)
3. Revise based on critique
4. Repeat (typically 3-5 iterations)

### Results
- ~20% average improvement across code generation tasks
- Model identifies its own errors 78.7% of the time in review mode
- Structured feedback > vague "improve this"

### Key Insight
> "Models can identify their own mistakes when given the right critique framework."

## Connections

- [[SelfCritique]] — concept page (builds on Self-Refine)
- [[VerificationLoop]] — the full pipeline this enables
- [[SelfDebugging]] — self-critique applied to bug fixing

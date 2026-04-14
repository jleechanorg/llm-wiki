---
title: "SelfRefine"
type: concept
tags: [self-refine, iterative-refinement, self-revision, generation-then-revise, ma拨]
sources: []
last_updated: 2026-04-14
---

## Summary

SelfRefine (Madaan et al., 2023) is a framework for iterative refinement of AI model outputs using a generate-then-revise pattern. Unlike [[ExtendedThinking]] which reasons before generation, SelfRefine iterates after generation: produce output → critique → revise → repeat. This post-hoc revision distinguishes it from pre-hoc extended thinking.

## Key Claims

- **Critique-driven revision**: A single model (or second model) critiques the output, then the original model incorporates the critique into a revised output
- **No reference needed**: Works without ground-truth labels — the model uses its own internal quality criteria
- **20-40% improvement on code generation**: Reported error reduction on tasks requiring multi-step fixes
- **Converges in 2-3 iterations**: Most gains realized in first two revision passes; diminishing returns after
- **Token overhead**: Each iteration adds substantial token cost; must be weighed against quality gains

## SelfRefine vs Extended Thinking

| Aspect | SelfRefine | Extended Thinking |
|--------|-----------|-------------------|
| Timing | After generation | Before generation |
| Feedback loop | Yes (iterative) | No (one-shot) |
| When to use | Output available, needs improvement | Problem spec available, needs planning |
| Token overhead | High (multiple passes) | Medium (one reasoning prefix) |
| Bottleneck addressed | Output quality | Approach correctness |

## Connections

- [[SelfCritique]] — self-refine uses the critique output from a self-critique pass
- [[SelfDebugging]] — self-refine is the iterative refinement mechanism that underlies self-debugging
- [[ExtendedThinking]] — complementary: Extended Thinking plans before generation, SelfRefine revises after
- [[ProcessRewardModel]] — PRM provides step-level critique signals to guide SelfRefine-like iterations
- [[VerificationLoop]] — self-refine is the "fix" mechanism in the loop, combined with [[SelfCritique]] for evaluation
- [[Reflexion]] — Reflexion adds memory to SelfRefine-like revision, tracking past critiques

## See Also
- [[SelfCritique]]
- [[SelfDebugging]]
- [[ExtendedThinking]]
- [[Reflexion]]

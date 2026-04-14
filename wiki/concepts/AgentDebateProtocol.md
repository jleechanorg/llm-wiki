---
title: "Agent Debate Protocol"
type: concept
tags: [agent-debate, multi-agent, adversarial, code-critique, SWE-bench, reasoning]
sources: [extended-reasoning-frontier, self-refine-paper, swe-bench-2026]
last_updated: 2026-04-14
---

## Summary

Agent Debate Protocol is a multi-agent pattern where two or more coding agents argue opposing positions on code correctness, design, or approach — then a judge (another agent or a formal verifier) resolves the disagreement. [[SelfRefine]] showed that self-critique improves code by ~20%; Agent Debate amplifies this by making critique external and adversarial, surfacing blind spots that a single agent's self-critique misses.

## Key Claims

### Why Self-Critique Has Blind Spots

A single agent critiquing its own code shares the same knowledge base as when it wrote the code. It cannot effectively question its own assumptions because:
- Same training data → same blind spots
- Same context window → same framing biases
- No adversarial pressure → no incentive to find the strongest counterargument

### Agent Debate Architecture

```
Agent A (Proponent): "My implementation is correct because..."
Agent B (Adversary): "Your implementation has flaws because..."
Judge (Agent C or Formal Verifier): Evaluates arguments, rules on correctness
→ Resolution: Fix issues identified by B, or defend against B's objections
```

### Debate as a Form of [[AdversarialTesting]]

| Approach | Adversarial Pressure Source | Coverage |
|----------|----------------------------|----------|
| Self-critique | Self (same model) | Limited by own blind spots |
| Agent debate | Other agent (different context) | Broader, surfaces hidden disagreements |
| Formal verification | SMT/theorem prover | Covers declared properties only |
| Human review | Human engineer | High coverage, slow |

Agent debate is faster than human review and covers more ground than single-agent self-critique.

### Connection to [[SelfRefine]]

[[SelfRefine]] established that iterative self-critique + revision improves code:
> "Models can identify their own mistakes when given the right critique framework."

Agent Debate externalizes this critique:
- Instead of Model A criticizing Model A → Model B criticizes Model A
- Model B brings different framing, different assumptions, different blind spots
- [[SWE-bench]] problems where self-critique fails are often resolved by adversarial debate

### Application to [[VerificationLoop]]

Debate can be the verification step in [[VerificationLoop]]:
```
Code Generated → Agent B attacks →
If attack succeeds: Fix → Agent C judges →
If defense holds: Pass gate
```

## Connections

- [[SelfCritique]] — foundational; Agent Debate externalizes and adversarializes it
- [[SelfRefine]] — the single-agent precursor; Agent Debate multiplies its effect
- [[AdversarialTesting]] — debate is a structured form of adversarial challenge
- [[VerificationLoop]] — debate can serve as the verification step
- [[SkepticAgent]] — the judge in Agent Debate could be a skeptic
- [[SWE-bench]] — Agent Debate improves SWE-bench pass rates on hard problems

## See Also

- [[SelfCritique]] — single-agent critique
- [[VerificationLoop]] — where debate fits in the pipeline
- [[AdversarialTesting]] — broader concept of adversarial challenge

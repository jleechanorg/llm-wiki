---
title: "Autoformalization"
type: concept
tags: [autoformalization, formal-verification, LLM, natural-language, specification-generation]
sources: [formal-verification-frontier]
last_updated: 2026-04-14
---

## Summary

Autoformalization is the use of LLMs to automatically translate natural language descriptions or informal specifications into formal mathematical specifications suitable for proof assistants like [Lean](Lean.md), [Coq](Coq.md), and Isabelle. It is the key enabling technology for making formal verification practical: writing formal specifications by hand is too slow and requires specialized expertise, but autoformalization allows a developer to describe requirements in plain English and receive machine-checkable formal proofs in return.

## Key Claims

- Autoformalization solves the specification bottleneck: formal verification's biggest barrier is the cost of writing formal specifications, not the proof itself
- LLMs can convert natural language requirements into formal statements in proof assistants with increasing accuracy
- AI-assisted autoformalization enables iterative formalization: describe -> formalize -> verify -> iterate on the formal statement
- [Lean](Lean.md) is the most prominent target for autoformalization research due to its declarative style and use in mathematical verification (e.g., Formalized FLT)
- Autoformalization does not replace human expertise — formal specification review remains a human-in-the-loop step

## Connections

- [FormalVerification](FormalVerification.md) — autoformalization is the bridge between informal requirements and formal verification
- [ProofAssistant](ProofAssistant.md) — autoformalization generates input for proof assistants
- [Lean](Lean.md) — the primary target language for autoformalization research
- [LLM-as-Judge-Pattern](LLM-as-Judge-Pattern.md) — autoformalization can be viewed as the LLM formalizing its own informal reasoning
- [ChainOfThought](ChainOfThought.md) — natural language reasoning trace is the input to autoformalization

## Relationships to Other Concepts

The gap between informal specification and formal proof is the central bottleneck in practical formal verification. [Autoformalization](Autoformalization.md) addresses this by automating the translation, similar to how [ChainOfThought](ChainOfThought.md) bridges informal reasoning and formal solution steps. In a [VerificationLoop](VerificationLoop.md), autoformalization would appear as a pre-verification stage: requirements in, formal spec out, ready for proof.

## See Also
- [FormalVerification](FormalVerification.md)
- [ProofAssistant](ProofAssistant.md)
- [Lean](Lean.md)
- [ChainOfThought](ChainOfThought.md)
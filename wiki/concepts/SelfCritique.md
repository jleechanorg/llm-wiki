---
title: "Self Critique"
type: concept
tags: [self-critique, self-revision, reflection, reflexion]
sources: [extended-reasoning-frontier]
last_updated: 2026-04-14
---

## Summary

Self Critique is the capability of a model to evaluate its own output against requirements or expectations before committing to it. Implemented as an internal monologue or reflection pass, self-critique is shown to reduce errors by 20-40% on coding tasks in empirical studies. It is natural to layer self-critique on top of extended thinking: the thinking trace itself becomes the object of critique, allowing the model to identify logical flaws or missing edge cases before the final answer is produced.

## Key Claims

- Self-critique passes catch logical errors, type mismatches, and missing requirements before output is finalized
- Studies on coding tasks report 20-40% error reduction when self-critique is applied, particularly on boundary condition handling
- Architecturally, self-critique can be implemented by prompting the model to generate a critique of its own output, then incorporating the critique into a revised output
- Reflexion (Shinn et al., 2023) formalizes self-critique with verbal reinforcement learning — the model learns from its own critique history
- Self-critique is distinct from self-debugging: critique identifies problems, while debugging additionally proposes and implements fixes

## Connections

- [[ExtendedThinking]] — the thinking trace is the natural surface for self-critique to inspect and evaluate
- [[jeffrey-oracle]] — oracle decision rules encode self-critique quality criteria
- [[SelfDebugging]] — extends self-critique by adding bug diagnosis and fix generation
- [[SkepticGate]] — a formalization of self-critique as a gate: the output must pass its own critique before proceeding
- [[EvidenceReviewPipeline]] — self-critique can serve as the first review stage before human or automated evidence review
- [[TwoStageEvidencePipeline]] — self-critique maps to the automated first-pass review stage
- [[Reflexion]] — memory-enhanced self-critique that learns from past critique history
- [[SelfReflection]] — the meta-cognitive layer of examining one's own reasoning process
- [[LLM-as-Judge-Pattern]] — using a secondary model to evaluate primary model outputs (architectural sibling to self-critique)
- [[SelfCritiqueVerificationLoop]] — specific 3-iteration-cap implementation combining ReVeal test-generation with self-correction refinement, mandating concrete test execution before final output

## Relationships to Other Concepts

In a multi-agent harness, self-critique can be implemented as a dedicated review agent or as a model-internal pass. The key difference from traditional code review is that the critic and the author are the same model, with different system prompts or operational modes. [[LLM-as-Judge-Pattern]] extends this: a separate model performs the critique, which can be more rigorous than self-critique.

## See Also
- [[Reflexion]]
- [[LLM-as-Judge-Pattern]]
- [[SelfReflection]]

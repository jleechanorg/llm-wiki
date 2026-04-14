---
title: "Extended Thinking"
type: concept
tags: [extended-reasoning, chain-of-thought, thinking-tokens, o3, o4]
sources: [extended-reasoning-frontier]
last_updated: 2026-04-14
---

## Summary

Extended Thinking is a mode in which frontier models generate prolonged, structured reasoning traces before producing a final output. Enabled by o3 and o4 class models, this approach treats "thinking tokens" as a new axis of computational scaling, distinct from pre-training compute or inference-time batch size. Rather than one-shot inference, the model spends disproportionate time deliberating, self-correcting, and exploring alternative reasoning paths.

## Key Claims

- Thinking tokens represent a distinct scaling dimension: more reasoning compute yields better task performance, particularly on hard coding, math, and scientific problems
- Extended thinking reduces superficial pattern-matching by forcing the model to externalize reasoning into a readable trace
- Models in extended thinking mode can catch logical errors mid-trace before committing to a flawed answer
- The o3 and o4 modes allocate variable amounts of thinking tokens based on perceived task difficulty, mimicking how humans think longer about harder problems
- Extended thinking is complementary to but architecturally distinct from pure chain-of-thought prompting, which is a prompt engineering technique rather than a built-in model capability

## Connections

- [[ReasoningBudget]] — allocating and optimizing thinking token budgets per task
- [[SelfCritique]] — layered on extended thinking, where the model critiques its own reasoning trace before finalizing
- [[TestTimeCompute]] — the broader category of which extended thinking is a specific implementation
- [[AgenticCoding]] — extended thinking supercharges agentic coders by giving them more time to plan complex refactors
- [[SkepticGate]] — skeptic verification can be applied to extended thinking outputs to catch remaining errors
- [[ChainOfThought]] — CoT is the prompting-technique precursor to built-in extended thinking
- [[ScalingLaws]] — extended thinking represents the new inference-time compute scaling axis
- [[SelfCritiqueVerificationLoop]] — 3-iteration-cap verification loop (ReVeal + Self-Correction) that extends extended thinking with concrete test execution before finalizing output

## Relationships to Other Concepts

Extended thinking is the substrate on which [[SelfCritique]] and [[ReasoningBudget]] build. A coding harness that employs extended thinking can route difficult problems to a high-thinking-token mode while using faster one-shot inference for simple tasks. [[ScalingLaws]] explains why this works: inference-time compute is a viable scaling axis distinct from pre-training compute.

## See Also
- [[ChainOfThought]]
- [[TestTimeCompute]]
- [[ScalingLaws]]

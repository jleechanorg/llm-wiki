---
title: "Verification Loop"
type: concept
tags: [verification-loop, self-verify, closed-loop, pipeline]
sources: [formal-verification-frontier]
last_updated: 2026-04-14
---

## Summary

The Verification Loop is the closed-cycle pipeline that takes a generated code artifact through repeated rounds of verification, adversarial testing, critique, and fix until it passes all checks. Starting from initial code generation, the loop alternates between verification (confirming correctness against requirements), adversarial testing (attempting to break the code), self-critique (identifying weaknesses), and self-debugging (fixing found issues). The loop terminates when the artifact passes verification or a retry budget is exhausted. This is the full pipeline from "generated code" to "verified code" in autonomous coding systems.

## Key Claims

- The minimal verification loop has four stages: generate -> verify -> fix -> repeat, but full implementations include adversarial testing and multi-pass critique
- Each iteration of the loop increases confidence and typically catches a different class of issues: first-pass verification catches specification violations, adversarial passes catch edge cases, critique catches style and intent misalignment
- Loop termination conditions must be explicit: passing verification threshold, exhausting retry budget, or reaching a timeout
- The verification loop is inherently parallelizable at the generate stage (multiple candidate solutions in parallel) but sequential in the verify-fix cycle
- In an orchestration context, the loop maps to distinct pipeline stages with dedicated agents: generator agent, verification agent, adversarial testing agent, and fixer agent

## Connections

- [[SelfDebugging]] — the "fix" component of the loop, which produces corrected code for re-verification
- [[AdversarialTesting]] — the "attack" phase of the loop, which attempts to find bugs the verifier missed
- [[SelfCritique]] — the "evaluate" phase that informs which fixes are most critical
- [[FormalVerification]] — one possible verification implementation within the loop
- [[TwoStageEvidencePipeline]] — the verification loop extends the two-stage evidence pipeline into a multi-pass iterative loop
- [[HarnessEngineering]] — a well-designed harness implements the verification loop as a first-class pipeline abstraction
- [[SkepticGate]] — skeptic gates can serve as loop termination enforcers: if a skeptic gate fails, the loop continues fixing
- [[ExtendedThinking]] — extended thinking enables more thorough verification at each loop stage
- [[ReasoningBudget]] — reasoning budgets can be allocated per loop iteration based on remaining budget and problem difficulty
- [[SelfCritiqueVerificationLoop]] — specific 3-iteration-cap implementation combining ReVeal test-generation with self-correction refinement, used in [[AutoResearchLoop]] Phase 2

## Relationships to Other Concepts

The verification loop is the macro-level pattern that unifies [[ExtendedThinking]], [[ReasoningBudget]], [[SelfCritique]], [[AdversarialTesting]], [[SelfDebugging]], and [[FormalVerification]] into a coherent pipeline. A harness implementing all of these concepts together has a complete autonomous code quality system.

## See Also
- [[ContinuousVerification]]
- [[CI-Gates]]
- [[LLM-as-Judge-Pattern]]

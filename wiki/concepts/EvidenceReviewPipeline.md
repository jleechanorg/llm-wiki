---
title: "EvidenceReviewPipeline"
type: concept
tags: [evidence-review, skeptic-gate, two-stage-review, verification-pipeline]
sources: [formal-verification-frontier]
last_updated: 2026-04-14
---

## Summary

The Evidence Review Pipeline is a two-stage verification system that evaluates code artifacts, test results, and claims before they can proceed to the next stage or merge. Stage 1 is automated self-review (self-critique + test execution), and Stage 2 is an independent LLM skeptic evaluation. The pipeline serves as the enforcement mechanism for merge readiness, catching issues that pass basic CI but fail qualitative review.

## Key Claims

- The two-stage pattern prevents self-review bias: the same model that generates code cannot be the sole judge of its quality
- Stage 1 (automated): runs self-critique, executes test suite, checks evidence bundle consistency
- Stage 2 (skeptic): independent LLM review of claims, evidence quality, and completeness against requirements
- Evidence review operates fail-closed: a missing evidence bundle fails the gate rather than silently passing
- The pipeline integrates with merge readiness contracts: CI green + evidence PASS = mergeable
- Adversarial testing and formal verification both feed into the evidence review pipeline as specialized stages

## Connections

- [[SelfCritique]] — self-critique is the first automated review stage in the pipeline
- [[VerificationLoop]] — the evidence review pipeline is the production deployment of the verification loop concept
- [[TwoStageEvidencePipeline]] — the specific implementation pattern for independent review
- [[SkepticGate]] — the evidence review pipeline is the skeptic gate enforcement mechanism
- [[EvidenceSkepticalReview]] — the skeptic's review criteria and consistency checks
- [[CI-Gates]] — evidence review is a specific CI gate in the pipeline
- [[AdversarialTesting]] — adversarial testing results are inputs to evidence review
- [[FormalVerification]] — formal verification proof artifacts are evidence inputs

## Relationships to Other Concepts

The evidence review pipeline is what turns the abstract [[VerificationLoop]] into a concrete, enforceable quality gate in a CI/CD context. Without a formal pipeline, verification remains aspirational; with it, verification becomes a precondition for deployment. The pipeline is the bridge between "we verify code" (VerificationLoop) and "code cannot merge without verification" (CI-Gates).

## See Also
- [[TwoStageEvidencePipeline]]
- [[CI-Gates]]
- [[ContinuousVerification]]
- [[SkepticGate]]
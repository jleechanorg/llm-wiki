---
title: "CI-Gates"
type: concept
tags: ["ci-gates", "ci-cd", "pipeline", "quality-gates"]
sources: []
last_updated: 2026-04-14
---

CI Gates are automated quality checkpoints in a CI/CD pipeline that must pass before code can proceed to the next stage or be merged. They implement [[ContinuousVerification]] by enforcing verification criteria at specific pipeline points.

## Key Properties
- **Automated enforcement**: No human bypass; gates fail the pipeline if not met
- **Layered**: Multiple gates at different pipeline stages (lint, test, security scan, formal verification)
- **Fast-fail**: Early gates (lint, type check) fail fast to give quick feedback
- **Slow gates**: Formal verification or comprehensive property testing may be later-stage gates

## Connections
- [[ContinuousVerification]] — CI gates are the enforcement mechanism for continuous verification
- [[VerificationLoop]] — each CI gate is a verification step in the loop
- [[LLM-as-Judge-Pattern]] — LLM-as-Judge can be implemented as a CI gate for code quality
- [[FormalVerification]] — formal verification can be a CI gate for safety-critical code

## See Also
- [[ContinuousVerification]]
- [[VerificationLoop]]

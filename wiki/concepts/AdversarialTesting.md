---
title: "Adversarial Testing"
type: concept
tags: [adversarial-testing, adversarial-examples, self-testing, fuzzing]
sources: [formal-verification-frontier]
last_updated: 2026-04-14
---

## Summary

Adversarial Testing is the practice of an AI model actively generating inputs designed to break its own code, then fixing the revealed vulnerabilities. This is distinct from conventional testing in that the model itself writes the adversarial test suite rather than relying on human-authored tests. The closed loop of generate -> attack -> fix -> repeat is the core operational pattern. Fuzzing is a well-established form of adversarial testing; the frontier extension is AI-guided fuzzing where the model reasons about which inputs are most likely to reveal bugs.

## Key Claims

- Self-written adversarial tests catch edge cases that human-written test suites miss, particularly around input boundary conditions and unexpected type combinations
- AI-guided fuzzing uses the model's reasoning to select inputs that are structurally likely to trigger bugs rather than relying purely on random mutation
- The generate-attack-fix loop is closed: a model writes tests, runs them against the code, analyzes failures, modifies the code, and re-tests
- Adversarial testing complements formal verification: it finds bugs in the specification itself, whereas formal verification assumes the specification is correct
- Empirical evidence from coding agent research shows that adversarial self-testing improves reliability on boundary conditions by 15-30% compared to human-written test baselines

## Connections

- [[SelfDebugging]] — adversarial testing feeds into self-debugging: finding bugs is the prerequisite for fixing them
- [[FormalVerification]] — adversarial testing finds gaps in formal specifications that verification cannot catch
- [[VerificationLoop]] — adversarial testing is the "attack" phase within the broader verification loop
- [[SelfCritique]] — the model's critique of its own code informs which adversarial inputs to generate
- [[TwoStageEvidencePipeline]] — adversarial testing can be the second stage of a two-pass evidence pipeline after basic critique
- [[HarnessEngineering]] — harnesses can implement adversarial testing as an automated stage in the pipeline

## Relationships to Other Concepts

A harness that incorporates adversarial testing as a stage would benefit from [[ReasoningBudget]] to allow the model enough compute to think deeply about which edge cases to probe. High-budget thinking enables more creative adversarial input generation.

## See Also
- [[Fuzzing]]
- [[PropertyBasedTesting]]
- [[SWE-bench]]

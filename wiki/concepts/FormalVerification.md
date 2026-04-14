---
title: "Formal Verification"
type: concept
tags: [formal-verification, lean, coq, proof-assistant, verified-code]
sources: [formal-verification-frontier]
last_updated: 2026-04-14
---

## Summary

Formal Verification is the use of mathematical proof systems — such as Lean, Coq, and Agda — to prove that code is correct with respect to a formal specification. Unlike testing or linting, which can only demonstrate the presence of bugs, formal verification demonstrates their absence within the bounds of the specification. The phrase "provably correct vs. probably correct" captures the fundamental distinction: a formally verified program has a machine-checked proof that its implementation matches its specification for all inputs in the defined domain.

## Key Claims

- Formal verification tools (Lean 4, Coq, Isabelle) have reached sufficient maturity that non-trivial programs have been verified end-to-end, including compilers and operating system kernels
- As of 2026, full formal verification of practical application code remains emerging — the overhead of writing formal specifications is still prohibitive for most production codebases
- The key enabler for AI-assisted formal verification is autoformalization: using LLMs to generate formal specifications from natural language descriptions or from existing code comments
- "Probably correct" (testing-based) vs. "provably correct" (formal verification) is a risk-management tradeoff: formal verification is justified for safety-critical, security-critical, or consensus-critical code
- Integration path in AI coding harnesses: a formal verification layer that accepts a code artifact and a natural-language specification, then attempts to produce a machine-checked proof

## Connections

- [[jeffrey-oracle]] — oracle tracks verification completeness and formal proof standards
- [[AdversarialTesting]] — complementary to formal verification: adversarial testing finds bugs that the formal specification did not cover
- [[VerificationLoop]] — formal verification is one possible verification stage within a broader verification pipeline
- [[SelfDebugging]] — verified code is a prerequisite for reliable self-debugging; a model debugging verified code can rely on the specification
- [[Lean]] — specific proof assistant increasingly used in AI-assisted verification contexts
- [[HarnessEngineering]] — a harness can route safety-critical code to a formal verification stage before deployment
- [[CompilerVerification]] — verified compilers (CompCert, CakeML) provide end-to-end guarantees for the compilation chain
- [[ProofAssistant]] — formal verification uses proof assistants (Lean, Coq, Isabelle) as the toolchain for building proofs

## Relationships to Other Concepts

Formal verification represents the highest assurance level in the spectrum from "tested" to "verified." For a coding harness, formal verification is the ultimate skeptic gate for code that must not fail. The tradeoff is speed: formal verification is orders of magnitude slower than compilation.

## See Also
- [[ProofAssistant]]
- [[Lean]]
- [[Coq]]
- [[Isabelle]]
- [[Fuzzing]]
- [[PropertyBasedTesting]]

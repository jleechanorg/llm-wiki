---
title: "PropertyBasedTesting"
type: concept
tags: ["property-based-testing", "testing", "hedgehog", "quickcheck", "fuzzing"]
sources: []
last_updated: 2026-04-14
---

Property-Based Testing (PBT) is a testing methodology where instead of writing individual test cases, you write properties that must hold for all inputs (or for randomly sampled inputs). The testing tool generates many inputs to find counterexamples to your properties.

## Key Properties
- **Properties over cases**: Write "for all X, property(X) holds" instead of individual test cases
- **Automatic input generation**: Tools like Hedgehog, Fast-Check generate inputs that attempt to falsify properties
- **Finds edge cases**: Particularly good at finding edge cases human testers miss
- **Complementary to [[Fuzzing]]**: PBT checks correctness properties; fuzzing checks for crashes/security issues

## Connections
- [[AdversarialTesting]] — PBT is a form of adversarial testing: it attempts to falsify properties
- [[Fuzzing]] — sister technique; fuzzing focuses on crash bugs, PBT on correctness properties
- [[FormalVerification]] — formal verification can prove PBT properties; PBT can find gaps in formal specifications
- [[VerificationLoop]] — PBT can be integrated as a verification stage

## See Also
- [[AdversarialTesting]]
- [[Fuzzing]]

---
title: "Fuzzing"
type: concept
tags: ["fuzzing", "adversarial-testing", "property-testing", "security"]
sources: []
last_updated: 2026-04-14
---

Fuzzing is an automated testing technique that generates random or semi-random inputs to find bugs, crashes, or security vulnerabilities. Modern fuzzing (guided fuzzing) uses coverage feedback to prioritize promising inputs.

## Key Properties
- **Automated**: No human-written test cases required
- **Coverage-guided**: LibFuzzer, AFL and similar tools track code coverage to guide input generation
- **Finds edge cases**: Particularly effective at finding edge cases and security vulnerabilities
- ** [[PropertyBasedTesting]] sister technique**: Fuzzing focuses on crash/security bugs; property testing focuses on correctness properties

## Connections
- [[AdversarialTesting]] — fuzzing is a primary form of adversarial testing
- [[PropertyBasedTesting]] — related technique focused on property verification
- [[ErrorDetection]] — fuzzing is a systematic approach to error detection
- [[SWE-bench]] — SWE-bench uses adversarial test cases somewhat similar to fuzzing inputs

## See Also
- [[AdversarialTesting]]
- [[PropertyBasedTesting]]

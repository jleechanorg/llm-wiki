---
title: "SWE-bench"
type: concept
tags: ["swe-bench", "benchmark", "software-engineering", "adversarial-testing"]
sources: []
last_updated: 2026-04-14
---

SWE-bench (Software Engineering Benchmark) is a benchmark for evaluating LLMs on real-world software engineering tasks from GitHub. It uses adversarial test cases derived from actual GitHub issues — the model must produce a fix that passes the test suite for a real open-source project.

## Key Properties
- **Real-world tasks**: Based on actual GitHub issues and pull requests from popular repositories
- **Adversarial test cases**: The test cases are the ones that failed before the fix and passed after — adversarially selected by the bug existing in the wild
- **Measures [[SelfDebugging]]**: Evaluates whether models can understand the issue, write code, and get tests to pass
- **Challenging**: Even frontier models struggle with many SWE-bench tasks

## Connections
- [[AdversarialTesting]] — SWE-bench uses adversarial test cases from real bugs
- [[SelfDebugging]] — SWE-bench is a benchmark for self-debugging capability
- [[VerificationLoop]] — SWE-bench evaluates whether a model can complete the verification loop autonomously

## See Also
- [[AdversarialTesting]]
- [[SelfDebugging]]

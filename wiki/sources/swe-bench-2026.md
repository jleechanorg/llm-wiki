---
title: "SWE-bench: Software Engineering Benchmark for LLM Coding Agents"
type: source
tags: [SWE-bench, benchmark, coding-agents, software-engineering, evaluation]
date: 2026-04-14
source_file: research/swe-bench-2026
---

## Summary

SWE-bench (Software Engineering Benchmark) evaluates LLMs on real-world GitHub issues from popular open-source projects. Agent receives issue description → generates code → tested against the project's test suite. Gold standard for measuring coding agent quality. 2026 version (SWE-bench Verified) uses harder, more realistic issues.

## Key Claims

### What SWE-bench Measures
- Issue comprehension → code generation → test pass rate
- Tests are the ground truth (from actual project test suites)
- End-to-end: understanding requirements, implementation, passing tests

### Top 2026 Performers
| Model | SWE-bench Verified |
|-------|------------------|
| GLM-4.7 | ~73.8% |
| DeepSeek-R1 | ~68% |
| Claude Sonnet 4 | ~65% |

### Relevance to Verification Loop
- SWE-bench tests serve as the "verification" step
- Agents that self-verify before submission do better
- Your PR test strategy mirrors this: generate → run tests → fix → retest

## Connections

- [[AdversarialTesting]] — generating test cases to break own code
- [[SelfDebugging]] — fixing bugs found in verification
- [[VerificationLoop]] — the full generate → verify → fix loop

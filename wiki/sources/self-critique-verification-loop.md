---
title: "Self-Critique + Verification Loop"
type: source
tags: [self-critique, verification, testing, re-veal, self-correction]
date: 2026-04-14
source_file: skills/self_critique_verification_loop.md
---

## Summary

A 3-iteration-cap verification loop that combines ReVeal (2026) self-critique with Self-Correction (2025) test-driven generation. Every coding task chains a canonical pattern prompt, generates code step-by-step, executes a full test suite in a sandbox, critiques results, and iterates until clean or the cap is reached.

## Key Claims

- **3-Iteration Cap**: Balances quality improvement against token efficiency — stops even if tests aren't fully clean
- **Canonical Prompt Chaining**: Phase 0 injects a relevant wiki pattern before any generation
- **Sandboxed Test Execution**: Real compilation/runtime errors caught, not just static analysis
- **Evidence-Standard Compliance**: Critique explicitly checks evidence standards alongside correctness
- **Exact Output Format**: Reproducible, auditable experiment artifacts

## Phase 0 – Prompt Chaining

Insert a short "canonical pattern" prompt extracted from the wiki (e.g., "FastAPI error handling pattern") before any generation. This grounds the LLM in proven patterns before it starts generating.

## Phase 1 – Generation

Think step-by-step and generate the initial code.

## Phase 2 – Test Generation & Execution

- Generate a full test suite: unit tests, integration tests, edge cases
- Run the tests in a sandbox (Docker/virtualenv)
- Capture any failures, compilation errors, or runtime exceptions

## Phase 3 – Self-Critique

Using concrete test results, critique the code against:
- Correctness vs. PR requirements
- Edge-case coverage
- Efficiency & style
- Security / robustness
- Evidence-standard compliance

**Loop condition**: If any issue is found and fewer than 3 iterations have been performed, go back to Phase 2. If all tests pass and the critique is clean, output ONLY the final verified code.

## Exact Output Format

1. Initial code
2. Tests + execution results
3. Critique
4. Revised code (only if needed)
5. Final verified code only

## Key Quotes

> "If any issue is found and fewer than 3 iterations have been performed, go back to Phase 2."

## Connections

- [[AutoResearchLoop]] — uses this loop in Phase 2 for implementation
- [[CanonicalCodeScorer]] — scores the final verified code
- [[AutoResearchExperiment]] — the broader system this skill is part of

## Contradictions

- None

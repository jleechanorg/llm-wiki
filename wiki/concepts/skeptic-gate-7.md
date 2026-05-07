---
title: "Skeptic Gate 7"
type: concept
tags: [skeptic, gate, llm-evaluation]
date: 2026-04-24
---

## Definition

Skeptic Gate 7 is the LLM-enforced technical review gate in the skeptic agent. It covers "behavior, tests, and merge readiness." It is defined at `skeptic/prompt.ts:172`.

## Scope

Gate 7 is NOT the alignment gate — that is Gate 8. Gate 7 focuses on:
- Code behavior correctness
- Test coverage and quality
- Whether the PR is technically merge-ready
- Rule 1-10 deterministic pre-checks

## See Also

- [[skeptic-gate-8]] — Alignment gate (goals/tenets/scope/diff/evidence)
- [[skeptic-rule-12]] — Goals verification rule
- [[skeptic-agent]]

---
title: "Real Acceptance Verdict"
type: concept
tags: [evidence, PR-automation, acceptance-testing]
last_updated: 2026-07-28
---

A structured, exact-head product-level pass/fail signal (e.g. `real_acceptance_verdict=PASS`) that a merge-ready workflow must require in addition to — not instead of — evidence artifact presence and provenance.

## Why it's needed

Evidence Gate and Green Gate "evidence" checks (e.g. Gate 6) validate that an artifact exists, is fresh, and is provenance-clean (real provider, correct head SHA, checksums). None of that proves the artifact's own assertions passed. In the originating incident, PR 8489's real-AGY browser capture was authentic and current, yet showed the product state failing its own expectations (wrong player level, wrong `review_open` flag, wrong quest status) and the PR body itself stated `Current evidence verdict: FAIL for merge-readiness` — while automated gates passed regardless.

## Rule

Artifact presence, checksums, real-provider provenance, or `/er` (evidence-review) authenticity CANNOT override a failed assertion inside the artifact. A merge-ready workflow must parse/require the structured verdict field itself, not merely confirm the artifact exists.

## Connections

- [[EvidenceTheater]] — the general failure class of gates accepting weaker proof than the claim requires.
- [[BoundedStateMachinePRRecovery]] — state `REAL_ACCEPTANCE_PASS` gates on this verdict.
- [[bounded-pr-convergence-requires-passing-acceptance-evidence]] — origin incident.

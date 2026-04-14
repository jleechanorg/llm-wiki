---
title: "Skeptic Gate Retry"
type: concept
tags: [skepticism, retry, evidence]
sources: []
last_updated: 2026-03-11
---

## Definition

The Skeptic Gate Retry is a pattern where evidence-based tests that fail are re-run with additional diagnostics and retry logic to distinguish transient failures from genuine regressions. The goal is to produce a skeptical evidence verdict that neither overstates pass claims nor prematurely marks failures as permanent.

## Pattern

1. Run evidence-based test against target (preview URL, live endpoint)
2. Parse logs and artifacts for concrete failure signatures
3. Apply minimal targeted fixes (health probe retry, diagnostics enrichment)
4. Re-run test and archive logs under `/tmp/`
5. Validate evidence bundle consistency (logs vs JSON artifacts)

## Evidence Bundle Consistency

A skeptical verdict requires checking that:
- JSON artifacts match the narrative in logs
- Passed tests are not marked with `skipped=true` as a false negative
- Partial proofs are labeled as such (e.g., "preview surface checks passed; full routing not executed")

## Sources

- BD-pr5879-rerun-stability-loop: stabilized remote-preview reruns for gateway and settings tests

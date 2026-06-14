---
title: "2026-06-14 Er Verdict Sub100loc Unit Acceptance"
type: source
tags: ["feedback", "evidence-review", "pr-discipline"]
date: 2026-06-14
source_file: raw/feedback-2026-06-14-er-verdict-sub100loc-unit-acceptance.md
---

## Summary
The /evidence_review (Codex via ai_orch) verdict has two PARTIAL failure modes that look the same: (a) genuine evidence gap — claim class higher than evidence supports; (b) PR body inaccuracy — evidence bundle is fine but the body overclaims. Discovered 2026-06-14 on PR #686: first /er verdict was PARTIAL because the body claimed `test-colima-roundtrip.mjs` ran 3 sessions (it ran 1). The actual evidence was sufficient (25/25 unit tests + multi-worker-colima-test.mjs 3 sessions + runtime round-trip). Rewriting the body to match the actual evidence fixed it on the second pass with no new tests. For sub-100-LOC production changes, the `unit` claim class is the floor; state "Claim floor override: N/A" explicitly in the Evidence section.

## Key Claims
- Two PARTIAL failure modes: genuine evidence gap (build more) vs body overclaim (rewrite body)
- A PARTIAL verdict is often faster to resolve by rewriting the body than by adding new tests
- For sub-100-LOC production changes, unit-test-only proof is acceptable per evidence-standards exception
- Direct plugin invocation (real plugin code, real env) is Layer 2 end-to-end, NOT a unit test
- The 100-LOC threshold is for "delta lines of non-test code", not total PR diff

## Key Quotes
> "Before declaring 'evidence gap' and rebuilding tests, re-read the PR body for overclaims. A PARTIAL verdict is faster to resolve by rewriting the body than by adding new tests."

## Connections
- [[evidence-review]]
- [[EvidenceBasedVerification]]
- [[PR686ColimaFix]]
- [[AOSpawn]]
- [[Layer2EndToEndTesting]]

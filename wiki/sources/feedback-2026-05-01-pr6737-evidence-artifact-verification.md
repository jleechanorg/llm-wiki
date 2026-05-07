---
title: "PR 6737 Evidence Artifact Verification"
type: source
tags: [evidence, worldarchitect, skeptic, mvp_site, ui-video]
date: 2026-05-01
source_file: raw/feedback_2026-05-01_pr6737_evidence_artifact_verification.md
---

## Summary

PR 6737 was blocked because the public PR evidence did not prove the current head. The PR body cited a stale SHA and relied on pasted unit-test and mock-smoke output for a user-visible `mvp_site` behavior claim.

The remediation regenerated current-SHA evidence with a real local server, real service mode, browser proof, checksums, and public artifact links. The reusable rule is that evidence is not fixed until the PR-published artifacts themselves, not local terminal output, satisfy `/es`.

## Key Claims

- Non-test `mvp_site/**` changes need `/es` evidence before they are complete.
- Unit tests, mocked tests, pasted pytest summaries, and mock CI smoke checks are supporting checks only for production behavior claims.
- Evidence must name the current PR HEAD SHA; stale-SHA evidence is invalid even if it passed for an older commit.
- User-visible behavior needs captioned video evidence linked from the PR or evidence bundle.
- Reviewers inspect public PR/release/gist artifacts, so local-only evidence does not count.

## Key Quotes

> "Evidence work is not complete until the PR-published artifacts" - learning summary

> "Rerun skeptic/green gates after artifact publication" - reusable pattern

## Connections

- [[EvidenceShaFreeze]] - Current-head provenance is mandatory for reviewer-trustworthy evidence.
- [[EvidenceSkepticalReview]] - Evidence review must inspect actual public artifacts, not accept pasted summaries.
- [[HarnessEvidenceRules]] - `/es` requires raw artifacts, checksums, and real-mode proof appropriate to the claim.
- [[VideoEvidenceGate]] - UI-visible behavior requires video proof.
- [[WorldArchitectAI]] - Repository where the PR 6737 evidence failure happened.

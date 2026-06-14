---
title: "7-Green Proof Artifact is the github-actions VERDICT Comment"
type: source
tags: [pr-workflow, skeptic-gate, 7-green, evidence, github-actions]
sources: []
last_updated: 2026-05-24
source_file: raw/feedback_2026-05-24_7green_proof_artifact.md
---

## Summary
Proof that a PR is at 7-green is a `github-actions[bot]` comment containing `VERDICT: PASS` plus the marker `<!-- skeptic-head-sha-<HEAD_SHA> -->`. The comment is produced by `skeptic-self-verify.yml` and enumerates all 8 gates. `gh pr checks` showing all SUCCESS is necessary but not sufficient. Green Gate typically runs twice per HEAD — the first run usually FAILS with `GATE-1 FAIL: CI=pending`. Always check the LATEST Green Gate run per HEAD.

## Key Claims
- The binding proof artifact for 7-green is the `github-actions[bot]` "VERDICT: PASS" comment with `<!-- skeptic-head-sha-XXX -->` marker — not `gh pr checks`, not CodeRabbit status, not a check-run.
- The 8 skeptic gates are: CI passing, no merge conflicts, CodeRabbit APPROVED (status+comment), Cursor Bugbot, inline comments resolved, evidence, self-verify, smoke gate.
- Green Gate often runs twice per HEAD — the first run typically FAILS with `GATE-1 FAIL: CI=pending` because it kicks off immediately on push. Always check the LATEST Green Gate run per HEAD.
- To prove 7-green: query `gh pr view <N> --json comments` and filter for both `VERDICT: PASS` AND the current HEAD SHA marker.
- PR #7048 verification (2026-05-24): two valid VERDICT: PASS comments at 06:15:18Z (HEAD 7ea51b546c) and 06:26:10Z (HEAD e979224079). Merged at 07:09:07Z (sha 25cee34d6f).

## Key Quotes
> "The canonical proof artifact for 'PR is at 7-green' is a comment posted by `github-actions[bot]` (not `coderabbitai`, not a check-run status) that literally contains the text `VERDICT: PASS` plus an HTML comment marker `<!-- skeptic-head-sha-<HEAD_SHA> -->`." — feedback_2026-05-24_7green_proof_artifact

> "`Green Gate` itself often **runs twice** per HEAD — the first run typically FAILS with `GATE-1 FAIL: CI=pending` (it kicks off immediately on push, before CI/CR/Skeptic complete). A second `Green Gate` run triggers after the cycle. Always check the LATEST `Green Gate` run per HEAD, not 'any FAILURE'." — feedback_2026-05-24_7green_proof_artifact

## Connections
- [[PR-7048-Location-Centralization-Merged]] — example PR where 7-green was verified twice
- [[Green-Gate-CI-Pattern]] — Green Gate is the upstream workflow that triggers Skeptic
- [[PR-Green-Definition]] — canonical 7-green merge criteria
- [[skeptic-self-verify.yml]] — workflow that emits the VERDICT comment

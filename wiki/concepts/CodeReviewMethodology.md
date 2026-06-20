---
title: "Code Review Methodology"
type: concept
tags: [code-review, methodology, assessment]
sources: ["copilot-analysis-report-pr-1440-documentation-guides"]
last_updated: 2026-04-14
---

## Description
Systematic approach to reviewing code changes, documentation, and project artifacts for quality, security, and compliance.

See also: [jeffrey-oracle](../syntheses/jeffrey-oracle.md) — operationalizes this methodology into automated PR verdicts.

## PR #1440 Analysis Framework
1. **Data Integrity Check**: Verify raw data matches reported conclusions
2. **Security Verification**: Confirm actual code changes implement claimed fixes
3. **Documentation Quality**: Assess structure, coverage, and accuracy
4. **File Organization**: Evaluate maintainability and navigation

## Assessment Scoring
PR #1440 received 45/100 - MAJOR REVISION REQUIRED due to:
- Critical data integrity issues
- Security documentation discrepancies
- Documentation sprawl concerns

## Related Concepts
- [DataIntegrityAnalysis](DataIntegrityAnalysis.md)
- [SecurityAnalysis](SecurityAnalysis.md)
- [DocumentationQualityAssessment](DocumentationQualityAssessment.md)

## Grep-on-PR-diff false positives (beads-tracked repos) — 2026-06-07

When verifying whether a PR's **code** sets/contains/removes a symbol, do **not**
trust `gh pr diff <PR> | grep <symbol>`. The combined diff includes
`.beads/issues.jsonl` (a 1MB+ DB export), and bead-description prose quotes code
symbols verbatim — producing false positives that conflate "mentioned in a bead"
with "changed by this PR." Isolate the production-file hunk
(`awk '/^diff --git.*FILE/{f=1} /^diff --git/&&!/FILE/{f=0} f'`) or read the
PR-head blob directly (`git show <sha>:file | grep`). Verify gate/consumer sides
by reading the file, not the diff. Same error class as `gh pr checks | grep -c
fail` (matches check names, not statuses). Incident: PR #7330 verification —
3 apparent `code_execution_used` matches, all in beads JSON, 0 in production.
Source: [2026-06-07-grep-beads-false-positive-pr-verification](../sources/2026-06-07-grep-beads-false-positive-pr-verification.md) · bead rev-15x97.

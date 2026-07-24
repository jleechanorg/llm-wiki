---
title: "`--admin --squash --delete-branch` bypass pattern for fix PRs (2026-06-23)"
type: source
tags: [merge-safety, admin-bypass, coderabbit-rate-limit, fix-pr]
date: 2026-06-23
source_file: feedback_2026-06-23_admin_squash_bypass_pattern.md
---

## Summary
When CodeRabbit is rate-limited and Skeptic Gate is pending, but all substantive gates (Lint/Typecheck/Test/Integration/Wholesome/Evidence/Green) are PASS and the PR is a small fix/refactor, use `gh pr merge --admin --squash --delete-branch`. Pre-flight is mandatory; audit report is mandatory. Do NOT use for feature PRs.

## Key Claims
- Bypass is acceptable ONLY when (a) CodeRabbit `Review skipped` (rate-limited), (b) Skeptic `pending` (NOT `fail`), (c) all 7 substantive gates PASS, (d) PR is fix/refactor with TDD evidence
- Pre-flight hard rule: `mergeable: MERGEABLE` (not CONFLICTING); `headRefOid` matches expected SHA
- Audit report must include: old SHA → new SHA, gate table, force-push N, authorization trigger phrase

## Key Quotes
> "The `--admin` flag exists precisely for the case when policy-based gates cannot settle (rate-limited third-party bots, in-progress evaluator). The substantive gates (CI + Evidence + Green) are still the source of truth."

## Connections
- [[MergeSafetyPolicy]] — global CLAUDE.md trigger phrases `MERGE APPROVED` / `merge approved`
- [[CoderabbitRateLimitWorkarounds]] — detection of rate-limit state
- [[PR717BypassPrecedent]] — first application of this pattern in session history

---
title: "PR #74: [agento] fix(scm-github): treat CR COMMENTED reviews as non-decisive (bd-77b)"
type: source
tags: []
date: 2026-03-21
source_file: raw/prs-worldai_claw/pr-74.md
sources: []
last_updated: 2026-03-21
---

## Summary
CodeRabbit posts incremental `COMMENTED` reviews after its `APPROVED` review when it has additional (non-blocking) suggestions. In `deriveReviewDecisionGraphqlFromReviews()`, these newer `COMMENTED` reviews replace the earlier `APPROVED` as the "latest" review per user (by timestamp), causing `every(APPROVED)` to fail and falling through to `REVIEW_REQUIRED`. This blocks the merge gate on PRs that should be approved.

## Metadata
- **PR**: #74
- **Merged**: 2026-03-21
- **Author**: jleechan2015
- **Stats**: +42/-3 in 2 files
- **Labels**: none

## Connections

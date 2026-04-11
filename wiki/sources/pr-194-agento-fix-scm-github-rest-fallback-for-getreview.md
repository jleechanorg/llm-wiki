---
title: "PR #194: [agento] fix(scm-github): REST fallback for getReviews and getReviewDecision"
type: source
tags: []
date: 2026-03-25
source_file: raw/prs-worldai_claw/pr-194.md
sources: []
last_updated: 2026-03-25
---

## Summary
When `getReviews` or `getReviewDecision` is called and GraphQL is rate-limited, the function throws with a rate-limit error rather than falling back to REST. This causes lifecycle-worker to lose review state during GraphQL exhaustion windows.

bd-yo1 adds REST fallbacks for both functions using `gh api repos/.../pulls/.../reviews`.

## Metadata
- **PR**: #194
- **Merged**: 2026-03-25
- **Author**: jleechan2015
- **Stats**: +105/-29 in 2 files
- **Labels**: none

## Connections

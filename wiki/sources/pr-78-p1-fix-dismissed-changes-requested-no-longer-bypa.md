---
title: "PR #78: [P1] fix: dismissed CHANGES_REQUESTED no longer bypasses CR merge gate"
type: source
tags: []
date: 2026-03-21
source_file: raw/prs-worldai_claw/pr-78.md
sources: []
last_updated: 2026-03-21
---

## Summary
When CodeRabbit posts `CHANGES_REQUESTED` and someone dismisses the review, GitHub transitions the review state to `"dismissed"`. The previous `getLatestDecisiveReview()` filter skipped dismissed reviews entirely, silently ignoring the `CHANGES_REQUESTED` — potentially letting the gate pass on no real approval.

## Metadata
- **PR**: #78
- **Merged**: 2026-03-21
- **Author**: jleechan2015
- **Stats**: +152/-27 in 3 files
- **Labels**: none

## Connections

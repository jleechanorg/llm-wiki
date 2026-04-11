---
title: "PR #192: [agento] fix(scm-github): REST fallback for getPendingComments when GraphQL exhausted"
type: source
tags: []
date: 2026-03-25
source_file: raw/prs-worldai_claw/pr-192.md
sources: []
last_updated: 2026-03-25
---

## Summary
`getPendingComments` in `scm-github` calls `gh api graphql` to get review threads with `isResolved` status. When GraphQL quota is exhausted (5000/hr), the call fails with no REST fallback -- the lifecycle-worker stalls on `changes-requested` detection, leaving workers idle for up to 1hr.

## Metadata
- **PR**: #192
- **Merged**: 2026-03-25
- **Author**: jleechan2015
- **Stats**: +38/-1 in 1 files
- **Labels**: none

## Connections

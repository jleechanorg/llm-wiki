---
title: "PR #195: [agento] fix(scm-github): REST fallback for getCIChecksFromStatusRollup + getCISummary"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-195.md
sources: []
last_updated: 2026-03-26
---

## Summary
`getCIChecksFromStatusRollup` uses `gh pr view --json statusCheckRollup` — a GraphQL-backed command. When GraphQL is exhausted, the lifecycle-worker loses CI state visibility.

## Metadata
- **PR**: #195
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +185/-53 in 2 files
- **Labels**: none

## Connections

---
title: "PR #79: [agento] fix(scm-github): fallback detectPR when REST head misses fork owner"
type: source
tags: []
date: 2026-03-23
source_file: raw/prs-worldai_claw/pr-79.md
sources: []
last_updated: 2026-03-23
---

## Summary
- GraphQL-first detectPR using gh pr list --head as primary path
- REST pulls head lookup as fallback when GraphQL fails (rate-limit, network error)
- Covers fork-owner branch cases where the REST filter can miss open PRs
- Regression tests for both paths and error cases

## Metadata
- **PR**: #79
- **Merged**: 2026-03-23
- **Author**: jleechan2015
- **Stats**: +302/-258 in 3 files
- **Labels**: none

## Connections

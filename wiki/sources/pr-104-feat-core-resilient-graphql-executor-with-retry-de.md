---
title: "PR #104: feat(core): resilient GraphQL executor with retry + deferral on rate-limits (bd-fy7)"
type: source
tags: []
date: 2026-03-22
source_file: raw/prs-worldai_claw/pr-104.md
sources: []
last_updated: 2026-03-22
---

## Summary
`ao review-check` silently returns `{pendingComments: 0, reviewDecision: null}` on **any** GitHub GraphQL error, including transient rate-limit errors. When GitHub rate-limits the lifecycle manager's session-polling loop, it has no retry or deferral — mutations fail into an errors array and work is silently dropped.

## Metadata
- **PR**: #104
- **Merged**: 2026-03-22
- **Author**: jleechan2015
- **Stats**: +722/-55 in 5 files
- **Labels**: none

## Connections

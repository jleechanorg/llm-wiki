---
title: "PR #118: feat(core): batch GraphQL query for all per-session PR checks (bd-att)"
type: source
tags: []
date: 2026-03-23
source_file: raw/prs-worldai_claw/pr-118.md
sources: []
last_updated: 2026-03-23
---

## Summary
Phase 3 of bd-8y9 API call reduction initiative. Per-session API calls in `determineStatus()` currently require 4-6 separate `gh` CLI invocations (getPRState, getCISummary, getReviewDecision, getMergeability). Each `gh` call costs ~2 GraphQL points.

## Metadata
- **PR**: #118
- **Merged**: 2026-03-23
- **Author**: jleechan2015
- **Stats**: +265/-54 in 4 files
- **Labels**: none

## Connections

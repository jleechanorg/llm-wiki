---
title: "PR #277: Fix backend coverage workflow regressions"
type: source
tags: [codex]
date: 2025-10-13
source_file: raw/prs-/pr-277.md
sources: []
last_updated: 2025-10-13
---

## Summary
- add a validation job that runs lint, build, unit, and integration checks with a live backend so the workflow matches CI expectations
- harden the coverage diff job with base-branch fallbacks, consistent reporters, and artifact paths that surface HTML and JSON coverage data
- normalize the coverage diff script to align file keys across worktrees and improve regression reporting clarity

## Metadata
- **PR**: #277
- **Merged**: 2025-10-13
- **Author**: jleechan2015
- **Stats**: +566/-5 in 5 files
- **Labels**: codex

## Connections

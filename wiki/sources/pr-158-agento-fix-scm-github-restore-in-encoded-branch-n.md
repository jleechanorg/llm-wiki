---
title: "PR #158: [agento] fix(scm-github): restore '/' in encoded branch name for REST ref deletion"
type: source
tags: []
date: 2026-03-24
source_file: raw/prs-worldai_claw/pr-158.md
sources: []
last_updated: 2026-03-24
---

## Summary
Fixes a bug in `scm-github` REST fallback branch deletion where `encodeURIComponent`
encodes `/` as `%2F`, breaking GitHub ref paths for branches containing slashes
(e.g. `feat/bd-pjh`).

## Metadata
- **PR**: #158
- **Merged**: 2026-03-24
- **Author**: jleechan2015
- **Stats**: +30/-3 in 2 files
- **Labels**: none

## Connections

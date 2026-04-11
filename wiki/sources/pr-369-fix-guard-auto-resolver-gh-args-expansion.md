---
title: "PR #369: fix: guard auto resolver gh args expansion"
type: source
tags: [codex]
date: 2025-10-16
source_file: raw/prs-/pr-369.md
sources: []
last_updated: 2025-10-16
---

## Summary
- guard the GitHub CLI metadata lookups against empty repo argument expansion so the auto resolver stays compatible with `set -u`
- preserve the existing repository-aware behavior when `GITHUB_REPOSITORY` is available

## Metadata
- **PR**: #369
- **Merged**: 2025-10-16
- **Author**: jleechan2015
- **Stats**: +6/-2 in 1 files
- **Labels**: codex

## Connections

---
title: "PR #1785: Refine directory-based CI workflow grouping"
type: source
tags: [codex]
date: 2025-09-29
source_file: raw/prs-worldarchitect-ai/pr-1785.md
sources: []
last_updated: 2025-09-29
---

## Summary
- update `.github/workflows/test.yml` to publish selected test groups, label each matrix job, and align dependency handling with the new group names
- enhance `scripts/ci-detect-changes.sh` to map directories to deterministic groups, emit those groups as workflow outputs, and support both include and simple matrix formats

## Metadata
- **PR**: #1785
- **Merged**: 2025-09-29
- **Author**: jleechan2015
- **Stats**: +128/-265 in 3 files
- **Labels**: codex

## Connections

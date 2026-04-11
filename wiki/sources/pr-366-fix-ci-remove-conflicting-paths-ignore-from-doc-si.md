---
title: "PR #366: fix(ci): Remove conflicting paths-ignore from doc-size-check workflow"
type: source
tags: []
date: 2025-07-06
source_file: raw/prs-worldarchitect-ai/pr-366.md
sources: []
last_updated: 2025-07-06
---

## Summary
- Fixed invalid GitHub Actions workflow configuration in `.github/workflows/doc-size-check.yml`
- Removed conflicting `paths-ignore` entries that caused workflow validation error
- GitHub Actions only allows either `paths` OR `paths-ignore` per event, not both

## Metadata
- **PR**: #366
- **Merged**: 2025-07-06
- **Author**: jleechan2015
- **Stats**: +0/-4 in 1 files
- **Labels**: none

## Connections

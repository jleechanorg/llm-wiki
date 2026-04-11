---
title: "PR #539: fix: build shared-libs before backend dependencies in local server"
type: source
tags: []
date: 2025-11-04
source_file: raw/prs-/pr-539.md
sources: []
last_updated: 2025-11-04
---

## Summary
Fix the DEFAULT_MAX_INPUT_TOKENS export error by ensuring shared-libs packages are built before backend npm install. This mirrors the deploy.sh logic for consistency across development and deployment workflows.

## Metadata
- **PR**: #539
- **Merged**: 2025-11-04
- **Author**: jleechan2015
- **Stats**: +94/-1 in 1 files
- **Labels**: none

## Connections

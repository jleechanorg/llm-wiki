---
title: "PR #683: chore: unblock backend auto deploy checkout"
type: source
tags: []
date: 2025-11-13
source_file: raw/prs-/pr-683.md
sources: []
last_updated: 2025-11-13
---

## Summary
- add `contents: read` back to the deploy job so actions/checkout can clone the private repo when the workflow runs
- this was causing the latest auto-deploy runs (e.g., 19320393622) to fail with `repository not found` before we even got to gcloud

## Metadata
- **PR**: #683
- **Merged**: 2025-11-13
- **Author**: jleechan2015
- **Stats**: +1/-0 in 1 files
- **Labels**: none

## Connections

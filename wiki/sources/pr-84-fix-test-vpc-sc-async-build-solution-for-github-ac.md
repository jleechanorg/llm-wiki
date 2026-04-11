---
title: "PR #84: fix: test VPC-SC async build solution for GitHub Actions"
type: source
tags: []
date: 2025-09-29
source_file: raw/prs-/pr-84.md
sources: []
last_updated: 2025-09-29
---

## Summary
Testing VPC-SC async build solution to resolve GitHub Actions deployment failures.

### Problem
GitHub Actions shows "failure" even when deployments succeed due to VPC Service Controls preventing log streaming from `gcloud builds submit`.

### Solution
- Detects CI environment (`CI=true` or `GITHUB_ACTIONS=true`) 
- Uses async build with status polling instead of log streaming
- Avoids VPC-SC restrictions while maintaining deployment verification

### Key Changes
- **deploy.sh**: Added async bui

## Metadata
- **PR**: #84
- **Merged**: 2025-09-29
- **Author**: jleechan2015
- **Stats**: +180/-83 in 2 files
- **Labels**: none

## Connections

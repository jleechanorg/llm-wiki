---
title: "PR #95: fix: ensure PR previews deploy to unique Cloud Run services"
type: source
tags: [codex]
date: 2025-10-01
source_file: raw/prs-/pr-95.md
sources: []
last_updated: 2025-10-01
---

## Summary
- normalize the GitHub Actions preview service name so each PR deploys to a dedicated Cloud Run instance
- sanitize incoming service names to meet Cloud Run requirements while preserving the PR-specific suffix

## Metadata
- **PR**: #95
- **Merged**: 2025-10-01
- **Author**: jleechan2015
- **Stats**: +250/-32 in 3 files
- **Labels**: codex

## Connections

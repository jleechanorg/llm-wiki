---
title: "PR #2211: Centralize Firebase token header management"
type: source
tags: [codex]
date: 2025-12-01
source_file: raw/prs-worldarchitect-ai/pr-2211.md
sources: []
last_updated: 2025-12-01
---

## Summary
- add a shared authTokenManager helper for token refresh scheduling and consistent header generation
- reuse centralized auth headers across API calls, settings loading, and downloads to align handling for test bypass and Firebase tokens

## Metadata
- **PR**: #2211
- **Merged**: 2025-12-01
- **Author**: jleechan2015
- **Stats**: +116/-17 in 4 files
- **Labels**: codex

## Connections

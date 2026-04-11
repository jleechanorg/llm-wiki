---
title: "PR #236: fix: suppress duplicate rate limit toast"
type: source
tags: [codex]
date: 2025-11-13
source_file: raw/prs-/pr-236.md
sources: []
last_updated: 2025-11-13
---

## Summary
- ensure the conversations hook stores the standard `RATE_LIMIT_ERROR_MESSAGE` when rate limit errors occur so the UI recognizes them as informational notifications
- keep non-rate-limit errors unchanged, preventing duplicate toasts while preserving existing error handling

## Metadata
- **PR**: #236
- **Merged**: 2025-11-13
- **Author**: jleechan2015
- **Stats**: +8/-1 in 1 files
- **Labels**: codex

## Connections

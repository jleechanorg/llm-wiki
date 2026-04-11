---
title: "PR #65: fix: respect Cloud Run port"
type: source
tags: [codex]
date: 2025-09-28
source_file: raw/prs-/pr-65.md
sources: []
last_updated: 2025-09-28
---

## Summary
- ensure the Express server respects the Cloud Run PORT environment variable when selecting its bind port
- fall back to the configured port locally while keeping Cloud Run logs accurate
- update logging so proxy and health check URLs reflect the resolved listen port

## Metadata
- **PR**: #65
- **Merged**: 2025-09-28
- **Author**: jleechan2015
- **Stats**: +219/-17 in 10 files
- **Labels**: codex

## Connections

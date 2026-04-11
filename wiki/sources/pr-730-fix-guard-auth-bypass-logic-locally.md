---
title: "PR #730: fix: guard auth bypass logic locally"
type: source
tags: [codex]
date: 2025-11-13
source_file: raw/prs-/pr-730.md
sources: []
last_updated: 2025-11-13
---

## Summary
- ensure the RUN_LOCAL_SERVER_DISABLE_AUTH flag is only honored for non-production, non-Cloud Run environments and lazily construct the FirebaseAuthTool so local runs without Firebase credentials succeed
- keep injectAuthContext consistent by returning null when there are no arguments to trust during a bypass

## Metadata
- **PR**: #730
- **Merged**: 2025-11-13
- **Author**: jleechan2015
- **Stats**: +15/-7 in 1 files
- **Labels**: codex

## Connections

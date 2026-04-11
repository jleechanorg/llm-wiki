---
title: "PR #2093: Fix Render deployment: Docker context + OOM worker config"
type: source
tags: []
date: 2025-11-23
source_file: raw/prs-worldarchitect-ai/pr-2093.md
sources: []
last_updated: 2025-11-23
---

## Summary
- Fixes Render Docker build failure caused by incorrect build context
- Adds render.yaml with explicit dockerContext: . (project root)
- **NEW: Fixes OOM kill by detecting RENDER=true env var for 1-worker default**

## Metadata
- **PR**: #2093
- **Merged**: 2025-11-23
- **Author**: jleechan2015
- **Stats**: +46/-13 in 6 files
- **Labels**: none

## Connections

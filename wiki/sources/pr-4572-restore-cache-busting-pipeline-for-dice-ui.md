---
title: "PR #4572: Restore: cache-busting pipeline for dice UI"
type: source
tags: []
date: 2026-02-08
source_file: raw/prs-worldarchitect-ai/pr-4572.md
sources: []
last_updated: 2026-02-08
---

## Summary
Restores and completes the cache-busting pipeline for frontend assets, fixing production 404s and implementing content-addressed immutable caching.

**Key themes:**
- **Docker-based architecture** - Cache-busting runs during Docker build (not CI), ensuring hashed files are included in production images
- **Content-addressed assets** - MD5-hashed filenames (e.g., `app.c70a7330.js`) enable aggressive 1-year immutable caching
- **Environment-aware serving** - Flask routes handle hashed/non-hashed f

## Metadata
- **PR**: #4572
- **Merged**: 2026-02-08
- **Author**: jleechan2015
- **Stats**: +5386/-34 in 28 files
- **Labels**: none

## Connections

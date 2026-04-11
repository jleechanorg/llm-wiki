---
title: "PR #4079: fix: Enable preload_app to share embedding model across workers"
type: source
tags: []
date: 2026-01-26
source_file: raw/prs-worldarchitect-ai/pr-4079.md
sources: []
last_updated: 2026-01-26
---

## Summary
- Enables `preload_app=True` in Gunicorn to share memory across workers via copy-on-write
- Reduces memory usage by ~1GB (embedding model loaded once instead of 3x)

## Metadata
- **PR**: #4079
- **Merged**: 2026-01-26
- **Author**: jleechan2015
- **Stats**: +5/-0 in 1 files
- **Labels**: none

## Connections

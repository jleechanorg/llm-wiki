---
title: "PR #60: [agento] fix(dockerfile): pre-create data/ and logs/ so non-root user can write"
type: source
tags: []
date: 2026-04-02
source_file: raw/prs-/pr-60.md
sources: []
last_updated: 2026-04-02
---

## Summary
Container exits with EACCES on mkdir 'data/' on Cloud Run because non-root nodeuser cannot write to /app.

## Metadata
- **PR**: #60
- **Merged**: 2026-04-02
- **Author**: jleechan2015
- **Stats**: +2/-0 in 1 files
- **Labels**: none

## Connections

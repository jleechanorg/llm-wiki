---
title: "PR #306: fix: skip optional npm deps to prevent bazelisk cleanup errors"
type: source
tags: [codex]
date: 2025-10-13
source_file: raw/prs-/pr-306.md
sources: []
last_updated: 2025-10-13
---

## Summary
- disable optional npm dependencies in the repo and backend packages so Bazelisk binaries are never installed during CI cleanup
- copy the backend .npmrc into Docker build contexts and document the behavior for developers

## Metadata
- **PR**: #306
- **Merged**: 2025-10-13
- **Author**: jleechan2015
- **Stats**: +1367/-121 in 10 files
- **Labels**: codex

## Connections

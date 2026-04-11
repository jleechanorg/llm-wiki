---
title: "PR #315: fix: shared-libs prep handles dependency freshness and rebase hooks"
type: source
tags: [codex]
date: 2025-10-13
source_file: raw/prs-/pr-315.md
sources: []
last_updated: 2025-10-13
---

## Summary
- restore dependency freshness detection in `prepare-shared-libs.mjs`, including npm install/ci triggers and dependency-order builds
- propagate the Node script exit code to shell callers, document the Node 20 runtime prerequisite, and harden git diff handling
- extend git hook automation with a post-rewrite rebase hook that forces rebuilds when histories are rewritten

## Metadata
- **PR**: #315
- **Merged**: 2025-10-13
- **Author**: jleechan2015
- **Stats**: +214/-18 in 4 files
- **Labels**: codex

## Connections

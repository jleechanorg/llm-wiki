---
title: "PR #294: fix: increment conversation message counts accurately"
type: source
tags: [codex]
date: 2025-10-11
source_file: raw/prs-/pr-294.md
sources: []
last_updated: 2025-10-11
---

## Summary
- increment conversation metadata counts by the number of newly persisted messages instead of relying on sequence numbers
- leave pagination-aware additions untouched while ensuring assistant replies still update the conversation metadata

## Metadata
- **PR**: #294
- **Merged**: 2025-10-11
- **Author**: jleechan2015
- **Stats**: +3/-9 in 1 files
- **Labels**: codex

## Connections

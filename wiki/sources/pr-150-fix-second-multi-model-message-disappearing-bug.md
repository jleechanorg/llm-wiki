---
title: "PR #150: Fix second multi-model message disappearing bug"
type: source
tags: [codex]
date: 2025-11-10
source_file: raw/prs-/pr-150.md
sources: []
last_updated: 2025-11-10
---

## Summary
- merge pending optimistic messages directly in the messages query result while active to avoid refetch overwrites
- skip backend fetches for temp conversation IDs by returning cached optimistic history
- extend regression tests to ensure no temp conversation fetches are issued during new conversation sends

## Metadata
- **PR**: #150
- **Merged**: 2025-11-10
- **Author**: jleechan2015
- **Stats**: +34/-2 in 2 files
- **Labels**: codex

## Connections

---
title: "PR #818: Fix rate-limit provisional identity reuse in send-message"
type: source
tags: [codex]
date: 2025-11-24
source_file: raw/prs-/pr-818.md
sources: []
last_updated: 2025-11-24
---

## Summary
- Reuse the provisional or fallback rate-limit user when no authenticated identity is resolved to avoid unnecessary reconciliation and preserve parallelization
- Remove unreachable anonymous fallback branch in conversation.send-message

## Metadata
- **PR**: #818
- **Merged**: 2025-11-24
- **Author**: jleechan2015
- **Stats**: +11/-10 in 1 files
- **Labels**: codex

## Connections

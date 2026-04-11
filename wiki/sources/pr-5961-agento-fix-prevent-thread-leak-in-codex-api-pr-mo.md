---
title: "PR #5961: [agento] fix: prevent thread leak in codex-api PR monitor"
type: source
tags: []
date: 2026-03-14
source_file: raw/prs-worldarchitect-ai/pr-5961.md
sources: []
last_updated: 2026-03-14
---

## Summary
- Add process tracking and thread safety valve to prevent kernel panics caused by accumulated threads from unsubprocess.Popen calls
- Fixes critical issue where codex-api PR monitor accumulated ~2450 threads over 6+ hours, triggering kernel spinlock deadlocks

## Metadata
- **PR**: #5961
- **Merged**: 2026-03-14
- **Author**: jleechan2015
- **Stats**: +79/-3 in 2 files
- **Labels**: none

## Connections

---
title: "PR #12: Centralize LLM timeout defaults"
type: source
tags: [codex]
date: 2025-09-20
source_file: raw/prs-/pr-12.md
sources: []
last_updated: 2025-09-20
---

## Summary
- centralize the 10-minute LLM timeout defaults in a shared config module to avoid duplicated constants
- update SecondOpinionAgent and the runtime config service to rely on the shared defaults with graceful fallbacks
- align the all-models integration test with the shared timeout constant

## Metadata
- **PR**: #12
- **Merged**: 2025-09-20
- **Author**: jleechan2015
- **Stats**: +59/-26 in 5 files
- **Labels**: codex

## Connections

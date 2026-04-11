---
title: "PR #3746: fix: Session header and resources display improvements"
type: source
tags: []
date: 2026-01-19
source_file: raw/prs-worldarchitect-ai/pr-3746.md
sources: []
last_updated: 2026-01-19
---

## Summary
- **Server-side session header normalization:** Handles dict-as-string format and adds `[SESSION_HEADER]` prefix when missing  
- **Fallback generation:** Creates session_header from `game_state` when LLM omits it (27% of entries had empty headers)
- **Resources display fix:** Changed from USED/MAX to CURRENT/MAX format for player clarity
- **JSON parsing hardening:** Replaced brittle prefix-stripping with robust full-text search for valid JSON candidates
- **Inventory safeguard enhancement:** A

## Metadata
- **PR**: #3746
- **Merged**: 2026-01-19
- **Author**: jleechan2015
- **Stats**: +3408/-575 in 40 files
- **Labels**: none

## Connections

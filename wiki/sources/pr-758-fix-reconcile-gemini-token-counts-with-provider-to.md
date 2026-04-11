---
title: "PR #758: fix: reconcile Gemini token counts with provider totals"
type: source
tags: [codex]
date: 2025-11-17
source_file: raw/prs-/pr-758.md
sources: []
last_updated: 2025-11-17
---

## Summary
- reconcile Gemini prompt and completion token counts against provider totals before logging and cost calculation, deriving any missing counts directly from total usage
- retain defensive total token fallback when provider totals are absent or invalid

## Metadata
- **PR**: #758
- **Merged**: 2025-11-17
- **Author**: jleechan2015
- **Stats**: +14/-5 in 1 files
- **Labels**: codex

## Connections

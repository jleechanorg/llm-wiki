---
title: "PR #190: [agento] fix(prose-polish): preserve indentation + clean filler artifact spaces"
type: source
tags: []
date: 2026-03-25
source_file: raw/prs-worldai_claw/pr-190.md
sources: []
last_updated: 2026-03-25
---

## Summary
Fixes Bugbot finding on PR #186: removing `trim()` from `fixLine()` to preserve intentional line indentation leaves single artifact spaces when filler words are removed from the start or end of a line. The `\s{2,}` regex only collapses runs of 2+ spaces, so a single leftover space after filler removal survives.

### Root cause

`"Just a note"` → filler replaced with `""` → `" a note"` → `\s{2,}` no-op (only 1 space) → `trim()` removed intentionally to preserve indent → artifact `" a note"` writt

## Metadata
- **PR**: #190
- **Merged**: 2026-03-25
- **Author**: jleechan2015
- **Stats**: +21/-4 in 1 files
- **Labels**: none

## Connections

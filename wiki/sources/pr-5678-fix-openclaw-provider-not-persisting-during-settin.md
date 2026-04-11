---
title: "PR #5678: Fix OpenClaw provider not persisting during settings saves"
type: source
tags: []
date: 2026-02-21
source_file: raw/prs-worldarchitect-ai/pr-5678.md
sources: []
last_updated: 2026-02-21
---

## Summary
- Preserve last loaded provider before save to avoid defaulting to Gemini when radios are temporarily unselected.
- Do not let radio read fallback to schema default in readEntryValue.
- Added regression coverage for missing radio selection + cached openclaw provider.

## Metadata
- **PR**: #5678
- **Merged**: 2026-02-21
- **Author**: jleechan2015
- **Stats**: +284/-36 in 5 files
- **Labels**: none

## Connections

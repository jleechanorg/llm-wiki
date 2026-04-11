---
title: "PR #6010: fix(streaming): reject malformed JSON in _classify_raw_narrative to prevent raw JSON stored as story text"
type: source
tags: []
date: 2026-03-18
source_file: raw/prs-worldarchitect-ai/pr-6010.md
sources: []
last_updated: 2026-03-18
---

## Summary
- Fixes `_classify_raw_narrative` to reject any text starting with `{` or `[`, even when JSON parsing fails (e.g. truncated/syntax-error JSON)
- Previously, malformed JSON that raised a parse exception was classified as narrative, causing raw JSON fragments to be persisted as story text

## Metadata
- **PR**: #6010
- **Merged**: 2026-03-18
- **Author**: jleechan2015
- **Stats**: +39/-15 in 3 files
- **Labels**: none

## Connections

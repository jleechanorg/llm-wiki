---
title: "PR #887: refactor: rename usedFallback to hasError for clarity"
type: source
tags: []
date: 2025-12-03
source_file: raw/prs-/pr-887.md
sources: []
last_updated: 2025-12-03
---

## Summary
- Renamed `usedFallback` to `hasError` as the primary field for LLM failure detection
- `usedFallback` is maintained as a deprecated alias for backward compatibility
- Fixed API response to actually return `hasError` at top level (was missing from return statements)
- Updated all test assertions to expect the new `hasError` field

## Metadata
- **PR**: #887
- **Merged**: 2025-12-03
- **Author**: jleechan2015
- **Stats**: +203/-80 in 18 files
- **Labels**: none

## Connections

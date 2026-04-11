---
title: "PR #140: fix(mem0): expose infer param + raise MemoryWriteError on silent drop"
type: source
tags: []
date: 2026-03-14
source_file: raw/prs-worldai_claw/pr-140.md
sources: []
last_updated: 2026-03-14
---

## Summary
- `mem0.add(infer=True)` (default) silently returned `{}` when gpt-4o-mini refused to extract facts — no error, no way to detect the drop
- Added `MemoryWriteError` raised when `infer=True` returns empty results
- Exposed `infer` param on `add_memory()` so callers can opt into guaranteed writes with `infer=False`

## Metadata
- **PR**: #140
- **Merged**: 2026-03-14
- **Author**: jleechan2015
- **Stats**: +242/-46 in 4 files
- **Labels**: none

## Connections

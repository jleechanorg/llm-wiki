---
title: "PR #262: fix: correct Update bot references and refactor bug hunt daily script handle + bug-hunt-daily.sh correctness fixes"
type: source
tags: []
date: 2026-03-17
source_file: raw/prs-worldai_claw/pr-262.md
sources: []
last_updated: 2026-03-17
---

## Summary
- Fix wrong bot handle `@coderabbit` → `@coderabbitai` (missing `ai` suffix means bot never receives the mention)
- Fix 3 correctness bugs in `bug-hunt-daily.sh` that caused aggregation to always report 0 bugs found

## Metadata
- **PR**: #262
- **Merged**: 2026-03-17
- **Author**: jleechan2015
- **Stats**: +207/-136 in 4 files
- **Labels**: none

## Connections

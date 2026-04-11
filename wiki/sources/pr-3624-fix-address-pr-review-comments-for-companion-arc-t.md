---
title: "PR #3624: fix: Address PR review comments for companion arc tests"
type: source
tags: []
date: 2026-01-15
source_file: raw/prs-worldarchitect-ai/pr-3624.md
sources: []
last_updated: 2026-01-15
---

## Summary
Follow-up fixes for issues identified in PR #3235 review comments.

### Changes
- **Import-time side effects fixed**: Moved `mkdir()` and `datetime.now()` calls from module level to `main()` function guards in all 4 test files
- **Inline imports fixed**: Moved `import traceback` and `import shutil` to module level
- **Type mismatch fixed**: Fixed `save_request_responses()` calls that were passing `list[tuple]` instead of `list[dict]`

### Issues Addressed
- Issue #12: Import-time mkdir side effe

## Metadata
- **PR**: #3624
- **Merged**: 2026-01-15
- **Author**: jleechan2015
- **Stats**: +324/-2338 in 9 files
- **Labels**: none

## Connections

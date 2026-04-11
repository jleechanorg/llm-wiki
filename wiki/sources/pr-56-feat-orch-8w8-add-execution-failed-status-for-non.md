---
title: "PR #56: feat(orch-8w8): add EXECUTION_FAILED status for non-zero ai_orch exit"
type: source
tags: []
date: 2026-03-05
source_file: raw/prs-worldai_claw/pr-56.md
sources: []
last_updated: 2026-03-05
---

## Summary
- Add `TaskStatus.EXECUTION_FAILED = "execution_failed"` to distinguish subprocess crashes from logic failures
- `_dispatch_via_ai_orch` includes the status in metadata on non-zero exit
- `_dispatch_task` uses status from metadata when present, falls back to `FAILED` for exceptions

## Metadata
- **PR**: #56
- **Merged**: 2026-03-05
- **Author**: jleechan2015
- **Stats**: +75/-2 in 3 files
- **Labels**: none

## Connections

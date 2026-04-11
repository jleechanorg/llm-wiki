---
title: "PR #217: fix(skeptic-gate): add missing permissions block + improve comment posting"
type: source
tags: []
date: 2026-03-27
source_file: raw/prs-worldai_claw/pr-217.md
sources: []
last_updated: 2026-03-27
---

## Summary
Fixes two bugs in skeptic-gate.yml that prevent skeptic findings from posting as PR comments:

1. **Missing permissions block** — gh pr comment needs pull-requests write permission on ubuntu-latest runners. skeptic-cron.yml already had this; skeptic-gate.yml was missing it, causing silent failure.
2. **head -c truncation** — truncating to 6000 bytes mid-line left orphaned output inside the triple-backtick code block. Added newline before the closing fence.

## Metadata
- **PR**: #217
- **Merged**: 2026-03-27
- **Author**: jleechan2015
- **Stats**: +6/-2 in 1 files
- **Labels**: none

## Connections

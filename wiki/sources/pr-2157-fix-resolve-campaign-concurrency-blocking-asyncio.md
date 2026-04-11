---
title: "PR #2157: fix: Resolve campaign concurrency blocking - asyncio.to_thread() for all blocking I/O"
type: source
tags: []
date: 2025-11-28
source_file: raw/prs-worldarchitect-ai/pr-2157.md
sources: []
last_updated: 2025-11-28
---

## Summary
Fixes critical concurrency bug where loading one campaign blocks while an action is being processed in another campaign (in a different window/tab).

**Bug reported:** "Can't load another campaign while taking an action in different window on another campaign"

## Metadata
- **PR**: #2157
- **Merged**: 2025-11-28
- **Author**: jleechan2015
- **Stats**: +408/-61 in 2 files
- **Labels**: none

## Connections

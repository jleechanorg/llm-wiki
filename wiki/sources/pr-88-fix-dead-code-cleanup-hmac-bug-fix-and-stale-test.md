---
title: "PR #88: fix: dead code cleanup, hmac bug fix, and stale test repair"
type: source
tags: []
date: 2026-03-10
source_file: raw/prs-worldai_claw/pr-88.md
sources: []
last_updated: 2026-03-10
---

## Summary
Full repo review of all 23 Python source files. Fixes 3 code issues + 1 stale test file.

### Bugs Fixed
- **`hmac.new()` → `hmac.HMAC()`** in `webhook_bridge.py`: `hmac.new()` does not exist in Python's `hmac` module. The bug was masked by a broad `except Exception`, causing HMAC webhook signature verification to **silently always fail** — all payloads were accepted when a webhook secret was configured.

### Dead / Duplicate Code Removed
- **Duplicate `_CROSS_REPO_CONTEXT`** in `dispatch_task.p

## Metadata
- **PR**: #88
- **Merged**: 2026-03-10
- **Author**: jleechan2015
- **Stats**: +35/-20 in 2 files
- **Labels**: none

## Connections

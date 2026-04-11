---
title: "PR #370: fix(launchd): point webhook plist at orchestration.webhook module"
type: source
tags: []
date: 2026-03-23
source_file: raw/prs-worldai_claw/pr-370.md
sources: []
last_updated: 2026-03-23
---

## Summary
`webhook_daemon.py` was renamed to `webhook.py` in a prior PR but the launchd plist template was never updated. The daemon survived on a stale inode from the last boot — any restart would silently fail with `No module named 'orchestration'`.

## Metadata
- **PR**: #370
- **Merged**: 2026-03-23
- **Author**: jleechan2015
- **Stats**: +339/-120 in 3 files
- **Labels**: none

## Connections

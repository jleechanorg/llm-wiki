---
title: "PR #316: doctor: make legacy cron non-fatal + AO/MCP checks configurable"
type: source
tags: []
date: 2026-03-21
source_file: raw/prs-worldai_claw/pr-316.md
sources: []
last_updated: 2026-03-21
---

## Summary
- downgrade legacy migrated cron job ID findings from FAIL to WARN (non-fatal)
- make AO dashboard port probe configurable via `OPENCLAW_DOCTOR_AO_DASHBOARD_PORT`
- auto-detect AO dashboard port from launchd plist `--port` arg when available
- skip MCP Agent Mail probe cleanly when MCP adapter is not configured

## Metadata
- **PR**: #316
- **Merged**: 2026-03-21
- **Author**: jleechan2015
- **Stats**: +71/-22 in 1 files
- **Labels**: none

## Connections

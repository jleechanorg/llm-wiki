---
title: "PR #127: fix: notifier normalizers, drain sender, metrics, and supervisor path separator"
type: source
tags: []
date: 2026-03-14
source_file: raw/prs-worldai_claw/pr-127.md
sources: []
last_updated: 2026-03-14
---

## Summary
- Fix `drain_outbox` to retry via `_send_via_mcp_agent_mail` (was using wrong sender, stranding retries)
- Fix dead-letter Slack alert to include `pending_count` and `oldest_age_seconds` fields
- Fix `notify_slack_started`/`notify_slack_done` to route through `_normalize_trigger_ts`/`_normalize_trigger_channel`
- Fix `_send_via_openclaw_agent`: add `or "main"` fallback when `OPENCLAW_NOTIFY_AGENT` is set to empty string
- Fix `supervisor._registry_paths_to_reconcile` to accept comma **or** colon

## Metadata
- **PR**: #127
- **Merged**: 2026-03-14
- **Author**: jleechan2015
- **Stats**: +144/-736 in 9 files
- **Labels**: none

## Connections

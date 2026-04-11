---
title: "PR #232: [agento] feat: periodic MCP mail global inbox poll + heartbeat for AO workers"
type: source
tags: []
date: 2026-03-27
source_file: raw/prs-worldai_claw/pr-232.md
sources: []
last_updated: 2026-03-27
---

## Summary
- Add MCP mail HTTP client to core (packages/core/src/mcp-mail.ts) with register_agent, send_message, fetch_inbox, and lifecycle helpers (sendMcpMailHeartbeat, sendMcpMailSessionStart, sendMcpMailSessionEnd)
- Wire MCP mail into lifecycle manager (packages/core/src/lifecycle-manager.ts): inbox polls every 5 minutes, heartbeat sent per-poll with active session count, session start/end messages sent on lifecycle transitions
- Add notifier-mcp-mail plugin (packages/plugins/notifier-mcp-mail/) — Plu

## Metadata
- **PR**: #232
- **Merged**: 2026-03-27
- **Author**: jleechan2015
- **Stats**: +582/-308 in 11 files
- **Labels**: none

## Connections

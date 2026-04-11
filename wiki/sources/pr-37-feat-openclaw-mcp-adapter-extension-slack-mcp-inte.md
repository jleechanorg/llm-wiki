---
title: "PR #37: feat: openclaw-mcp-adapter extension, Slack MCP integration, and workflow security"
type: source
tags: []
date: 2026-03-04
source_file: raw/prs-worldai_claw/pr-37.md
sources: []
last_updated: 2026-03-04
---

## Summary
- Add `openclaw-mcp-adapter` TypeScript extension: a generic MCP proxy that routes OpenClaw tool calls to multiple downstream MCP servers (stdio or HTTP transport)
- Wire Slack MCP server into the agent via the adapter, enabling 11 Slack tools (channels, conversations, DMs, user groups)
- Fix `replyToModeByChatType.direct="off"` — agent was silently ignoring DMs
- Add 24-test config regression suite protecting openclaw.json invariants
- Fix command injection and JSON payload injection in PR agen

## Metadata
- **PR**: #37
- **Merged**: 2026-03-04
- **Author**: jleechan2015
- **Stats**: +569/-5 in 8 files
- **Labels**: none

## Connections

---
title: "PR #484: docs: Slack MCP setup, HTTP 2064 guidance, SmartClaw audit sync"
type: source
tags: []
date: 2026-04-03
source_file: raw/prs-worldai_claw/pr-484.md
sources: []
last_updated: 2026-04-03
---

## Summary
- **CLAUDE.md**: Operational note for **HTTP 2064** / high load — avoid fan-out attach/diagnose; backoff and lower concurrency (same spirit as WS churn guidance).
- **workspace/TOOLS.md**: Cursor Slack MCP config (`~/.cursor/mcp.json`), restart requirement, redacted example path, usage vs curl fallbacks.
- **docs/examples/cursor-mcp-slack.example.json**: Placeholder-only example for Cursor MCP (no real tokens).
- **agent-orchestrator.yaml**: `defaults.model: claude-sonnet-4-6` aligned with proje

## Metadata
- **PR**: #484
- **Merged**: 2026-04-03
- **Author**: jleechan2015
- **Stats**: +217/-10 in 7 files
- **Labels**: none

## Connections

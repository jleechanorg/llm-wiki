---
title: "MCP Server Port URLs Must Be Updated in BOTH settings.json AND .claude.json"
type: source
tags: [mcp, supergateway, port-config, settings-json, claude-json]
sources: []
last_updated: 2026-05-28
source_file: raw/feedback_2026-05-28_mcp_port_config_two_files.md
---

## Summary
MCP server URL config lives in two separate files that both feed `claude mcp list`: `~/.claude/settings.json` (mcpServers block) and `~/.claude.json` (top-level mcpServers key). The binary reads `.claude.json` first — updating only `settings.json` leaves `claude mcp list` reading the old port. Discovered 2026-05-28 when moving playwright-mcp from 8003→8012.

## Key Claims
- Two separate files feed `claude mcp list`: `~/.claude/settings.json` (mcpServers block) and `~/.claude.json` (top-level mcpServers key). Both must be updated atomically.
- The binary reads `.claude.json` first. If only `settings.json` is updated, `claude mcp list` still reports the old port from `.claude.json` (showing `✗ Failed to connect`).
- Any time an MCP server port or URL is changed, run the python snippet that updates both files, or grep both to verify sync.
- Verification command: `grep -n "playwright-mcp\|<server>" ~/.claude/settings.json ~/.claude.json` to verify both are in sync.

## Key Quotes
> "The binary reads `.claude.json` first. If only `settings.json` is updated, `claude mcp list` still reports the old port from `.claude.json`." — feedback_2026-05-28_mcp_port_config_two_files

> "Discovered 2026-05-28 when moving playwright-mcp from 8003→8012. Updated settings.json, but `claude mcp list` kept showing 8003 and `✗ Failed to connect`. Root cause: `.claude.json` still had the old entry." — feedback_2026-05-28_mcp_port_config_two_files

## Connections
- [[MCP-Daemon-Port-Config-2026-05-28]] — sibling project memory with the full port map
- [[Project-MCP-Daemon-Setup]] — daemon launchd and process management

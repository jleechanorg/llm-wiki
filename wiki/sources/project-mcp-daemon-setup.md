---
title: "MCP HTTP Daemon Setup, Port Map, and Launchd Auto-Start"
type: source
tags: [mcp, supergateway, daemon, launchd, port-config, playwright]
sources: []
last_updated: 2026-05-28
source_file: raw/project_mcp_daemon_setup.md
---

## Summary
MCP HTTP daemons are managed by `~/.config/mcp-daemon/start-mcp-daemons.sh` (restored from `~/projects_other/user_scope/scripts/` backup). Port config lives in TWO places — `~/.claude/settings.json` and `~/.claude.json` — and both must be updated atomically when changing ports. Port 8003 was a conflict (worldarchitect.ai Flask dev server), so playwright-mcp was moved to 8012. Auto-start via launchd plist at `~/Library/LaunchAgents/com.jleechan.mcp-daemon.plist`.

## Key Claims
- Canonical daemon script: `~/.config/mcp-daemon/start-mcp-daemons.sh`. Backup: `~/projects_other/user_scope/scripts/start-mcp-daemons.sh`. If missing, restore from backup, then `launchctl load ~/Library/LaunchAgents/com.jleechan.mcp-daemon.plist`.
- Port map: 8001 context7, 8002 gemini-cli-mcp, 8004 perplexity-ask, 8005 sequential-thinking, 8006 slack (native Go), 8007 memory-mcp, 8008 ddg-search, 8009 filesystem-mcp, 8010 worldarchitect, 8011 google-docs, 8012 playwright-mcp (moved from 8003 — Flask uses 8003), 8765 mcp-agent-mail.
- 8765 mcp-agent-mail has a separate launchd job: `com.mcp.agent.mail`, script at `~/mcp_mail/scripts/run_server_with_token.sh`.
- Port config lives in TWO places (both must update atomically): `~/.claude/settings.json` (mcpServers URL) and `~/.claude.json` (top-level mcpServers URL). If only one is updated, `claude mcp list` reads the old port from the other file.
- Auto-start launchd plist: `~/Library/LaunchAgents/com.jleechan.mcp-daemon.plist` with `KeepAlive=false, RunAtLoad=true`.
- If daemons are down: run `~/.config/mcp-daemon/start-mcp-daemons.sh start`. If stale processes prevent restart: `pkill -f "supergateway"` then restart.

## Key Quotes
> "MCP HTTP daemons are managed by `~/.config/mcp-daemon/start-mcp-daemons.sh` (restored from `~/projects_other/user_scope/scripts/`). If this directory goes missing, restore from that backup." — project_mcp_daemon_setup

> "Port 8003 was a conflict — worldarchitect.ai Flask dev server uses 8003. playwright-mcp moved to 8012." — project_mcp_daemon_setup

> "If daemons are down: Run `~/.config/mcp-daemon/start-mcp-daemons.sh start`. If stale processes prevent restart: `pkill -f 'supergateway'` then restart." — project_mcp_daemon_setup

## Connections
- [[MCP-Daemon-Port-Config-2026-05-28]] — the broader session-merged version with all commands
- [[MCP-Port-Config-Two-Files]] — the "two files" rule for port config
- [[Launchd-Template-Orphan-Prevention]] — template files in repo for cleanup
- [[Start-MCP-Daemons-Script]] — the canonical daemon script

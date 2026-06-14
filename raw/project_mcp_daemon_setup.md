---
name: project_mcp_daemon_setup
description: "MCP HTTP daemon setup — start-mcp-daemons.sh location, port map, launchd auto-start, and playwright port fix"
metadata: 
  node_type: memory
  type: project
  originSessionId: f75604c7-21c6-490b-9412-fc02039959a8
---

MCP HTTP daemons are managed by `~/.config/mcp-daemon/start-mcp-daemons.sh` (restored from `~/projects_other/user_scope/scripts/`). If this directory goes missing, restore from that backup.

**Port map:**
- 8001 context7, 8002 gemini-cli-mcp, 8004 perplexity-ask, 8005 sequential-thinking
- 8006 slack (native Go binary), 8007 memory-mcp, 8008 ddg-search, 8009 filesystem-mcp
- 8010 worldarchitect, 8011 google-docs, **8012 playwright-mcp** (moved from 8003 — Flask uses 8003)
- 8765 mcp-agent-mail (separate launchd: `com.mcp.agent.mail`, script at `~/mcp_mail/scripts/run_server_with_token.sh`)

**Why:** Port 8003 was a conflict — worldarchitect.ai Flask dev server uses 8003. playwright-mcp moved to 8012.

**Port config lives in TWO places** — both must be updated together when changing a port:
1. `~/.claude/settings.json` (mcpServers URL)
2. `~/.claude.json` (top-level mcpServers URL)
If only one is updated, `claude mcp list` still reads the old port from the other file.

**Auto-start:** launchd plist at `~/Library/LaunchAgents/com.jleechan.mcp-daemon.plist` (KeepAlive=false, RunAtLoad=true).

**If daemons are down:** Run `~/.config/mcp-daemon/start-mcp-daemons.sh start`.
If stale processes prevent restart: `pkill -f "supergateway"` then restart.

**How to apply:** When MCP servers show Failed in `claude mcp list`, check this file first before investigating elsewhere.

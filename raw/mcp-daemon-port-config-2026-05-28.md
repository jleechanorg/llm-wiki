# MCP HTTP Daemon Setup & Port Config Fix — 2026-05-28

## Summary

MCP HTTP daemons managed by `~/.config/mcp-daemon/start-mcp-daemons.sh` went missing from disk. Restored from `~/projects_other/user_scope/scripts/` backup. Three stale entries removed from `~/.claude.json`. playwright-mcp moved from port 8003 to 8012 (conflict with worldarchitect Flask). mcp-agent-mail launchd plist path fixed. launchd auto-start plist created.

## Key Learnings

### 1. Port config exists in TWO files
- `~/.claude/settings.json` (mcpServers block)
- `~/.claude.json` (top-level mcpServers key)
- Must update BOTH atomically. Binary reads .claude.json first.

### 2. Port 8003 conflict
- worldarchitect.ai Flask dev server uses port 8003.
- playwright-mcp must use 8012 (or any non-Flask port).

### 3. supergateway SIGTERM on disconnect
- `claude mcp list` sends SIGTERM when it disconnects from MCP servers.
- Daemon script has auto-restart wrapper (3s delay).
- If servers appear down right after `mcp list` probe: wait or `pkill -f supergateway && start`.

### 4. Daemon script location
- Canonical: `~/.config/mcp-daemon/start-mcp-daemons.sh`
- Backup source: `~/projects_other/user_scope/scripts/start-mcp-daemons.sh`
- If missing: restore from backup, then `launchctl load ~/Library/LaunchAgents/com.jleechan.mcp-daemon.plist`

## Port Map
| Port | Server | Transport |
|------|--------|-----------|
| 8001 | context7 | supergateway+stdio |
| 8002 | gemini-cli-mcp | supergateway+stdio |
| 8004 | perplexity-ask | supergateway+stdio (wrapper) |
| 8005 | sequential-thinking | supergateway+stdio |
| 8006 | slack-mcp-server | native HTTP (Go binary) |
| 8007 | memory-mcp | supergateway+stdio |
| 8008 | ddg-search | supergateway+stdio |
| 8009 | filesystem-mcp | supergateway+stdio |
| 8010 | worldarchitect | supergateway+stdio |
| 8011 | google-docs | supergateway+stdio |
| 8012 | playwright-mcp | supergateway+stdio |
| 8765 | mcp-agent-mail | uvicorn HTTP (~/mcp_mail/) |

## Commands
```bash
# Restart all
~/.config/mcp-daemon/start-mcp-daemons.sh restart

# If stale processes block restart
pkill -f "supergateway" && ~/.config/mcp-daemon/start-mcp-daemons.sh start

# Status check
~/.config/mcp-daemon/start-mcp-daemons.sh status
claude mcp list
```

## Files Modified
- `~/.config/mcp-daemon/start-mcp-daemons.sh` (restored + playwright 8012)
- `~/.claude/settings.json` (playwright-mcp 8003→8012)
- `~/.claude.json` (playwright-mcp 8003→8012, removed chrome-superpower/test-user-server/blog-mcp)
- `~/Library/LaunchAgents/com.jleechan.mcp-daemon.plist` (created)
- `~/Library/LaunchAgents/com.mcp.agent.mail.plist` (path fixed)

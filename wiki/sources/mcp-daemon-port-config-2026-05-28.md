---
title: MCP HTTP Daemon Setup & Port Config Fix
date: 2026-05-28
tags: [mcp, supergateway, daemon, launchd, port-config]
source: /Users/jleechan/llm_wiki/raw/mcp-daemon-port-config-2026-05-28.md
---

MCP HTTP daemons managed by `~/.config/mcp-daemon/start-mcp-daemons.sh`. Port config must be updated in BOTH `~/.claude/settings.json` AND `~/.claude.json`. playwright-mcp on 8012 (8003 = Flask). Auto-restart handles SIGTERM from `claude mcp list`. See raw doc for full port map and commands.

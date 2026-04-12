---
title: "Thinclaw MCP Server"
type: concept
tags: [MCP, thinclaw, agent, gateway, tools]
last_updated: 2026-04-08
---

Thinclaw exposes 15 MCP tools via stdio transport — all core tools working (list_agents, get_agent_profile, setup_info, file_read/write, browser, memory, cron, send_message). HTTP /tools/invoke blocked by Gateway auth — stdio works without token.

## Available Tools

1. `list_agents` — proxies Gateway agents_list
2. `get_agent_profile` — fetches agent profile (with fallback)
3. `setup_info` — transport/features
4. `file_read` / `file_write` — file operations
5. `browser` — browser automation
6. `memory` — memory operations
7. `cron` — scheduled task management
8. `send_message` — inter-agent messaging

## HTTP Transport

Gateway HTTP auth now working with `gateway.auth.token` in `~/.openclaw/openclaw.json`. HTTP `/tools/invoke` returns valid response via Bearer token auth.

## Gateway Tools Bug

Gateway tools returning 404 because config used `gateway.tools.allow` instead of `tools.allow` — they're separate pipelines with different behavior.

## Connections

- [[MCProtocol]] — MCP protocol documentation
- [[MCPServerInstructions]] — MCP server setup
- [[MemoryMCP]] — memory MCP server

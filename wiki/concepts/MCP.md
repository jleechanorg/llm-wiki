---
title: "MCP (Model Context Protocol)"
type: concept
tags: [mcp, protocol, ai, tools]
sources: [worldai-tools-mcp-proxy-runtime, worldai-mcp-stdio-adapter]
last_updated: 2026-04-08
---

MCP (Model Context Protocol) is a standardized protocol for AI systems to expose tools and resources to language models. The WorldAI wiki documents two MCP implementations:

1. **WorldAI MCP STDIO Adapter** — stdio-based server reading JSON-RPC from stdin
2. **WorldAI Tools MCP Proxy Runtime** — HTTP server-based with local tool exposure and upstream forwarding

## Key Patterns
- Tool registration with inputSchema definitions
- JSON-RPC 2.0 message format
- Authentication context propagation
- Resource catalog exposure

## Related
- [[JSON-RPC 2.0]]
- [[WorldAI MCP STDIO Adapter]]
- [[WorldAI Tools MCP Proxy Runtime]]

## HTTP Daemon Port Map (Mac — 2026-05-28)

Managed by `~/.config/mcp-daemon/start-mcp-daemons.sh` via `supergateway` (stdio→HTTP).

| Port | Server | Notes |
|------|--------|-------|
| 8001 | context7 | @upstash/context7-mcp |
| 8002 | gemini-cli-mcp | @yusukedev/gemini-cli-mcp |
| 8004 | perplexity-ask | wrapper script |
| 8005 | sequential-thinking | |
| 8006 | slack-mcp-server | native HTTP Go binary |
| 8007 | memory-mcp | |
| 8008 | ddg-search | |
| 8009 | filesystem-mcp | |
| 8010 | worldarchitect | |
| 8011 | google-docs | |
| **8012** | **playwright-mcp** | **8003 = Flask conflict** |
| 8765 | mcp-agent-mail | uvicorn at ~/mcp_mail/ |

**Port config in two files:** `~/.claude/settings.json` + `~/.claude.json` — update both.
**Auto-start:** `~/Library/LaunchAgents/com.jleechan.mcp-daemon.plist`
**Restart:** `pkill -f supergateway && ~/.config/mcp-daemon/start-mcp-daemons.sh start`

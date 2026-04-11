---
title: "MCP Server Context Optimization Analysis"
type: source
tags: [mcp, context, optimization, claude-code]
date: 2026-04-05
source_file: raw/mcp-trim-analysis-2026-04-05.md
---

## Summary
Analysis of 16 configured MCP servers, finding 7 actively connected (74 deferred tools) and 9 failing to connect. ios-simulator-mcp is the only TRIM server actually injecting deferred tools (~240 tokens/turn). Estimated ~920 tokens total savings from trimming, with qualitative benefits of reduced noise, faster startup, and cleaner tool routing.

## Key Claims
- 16 MCP servers configured total; 7 actually connected this session (74 deferred tools)
- ios-simulator-mcp is the ONLY connected TRIM server (12 tools injected ~240 tokens/turn)
- 8 servers fail to start but still occupy config space (sequential-thinking, context7, gemini-cli-mcp, memory-server, grok-mcp, render, serena, chrome-superpower)
- Each deferred tool occupies ~15-25 tokens in every system-reminder block
- Estimated ~920 tokens persistent savings from full trim (~240 deferred + ~600 config one-time)
- Qualitative benefits: reduced system-reminder noise, faster session startup, cleaner tool routing, reduced permission surface

## Classification
**KEEP**: worldai (16 tools), mcp-agent-mail (17 tools), slack (11 tools), ddg-search (3 tools), perplexity-ask (1 tool), filesystem (14 tools)
**TRIM**: ios-simulator-mcp (12 tools, connected), chrome-superpower (0, not connected), sequential-thinking (0), context7 (0), gemini-cli-mcp (0), memory-server (0), grok-mcp (0), render (0), serena (0)

## Connections
- [[WorldArchitect.AI]] — worldai MCP core to campaign engine
- [[MCPServerInstructions]] — MCP server configuration context
- [[ContextBloat]] — deferred tool overhead is part of per-turn context cost
- [[ClaudeCode]]]] — MCP trimming saves tokens per turn

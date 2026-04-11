---
title: "MCP Server Context Optimization Analysis"
type: source
tags: [mcp, context-optimization, tokens, performance, claude-code]
date: 2026-04-05
source_file: /Users/jleechan/Downloads/mcp-trim-analysis-2026-04-05.md
---

## Summary

Analysis of MCP server configuration across Claude Code sessions, identifying ios-simulator-mcp as the only connected non-essential server consuming persistent per-turn context (~240 tokens). KEEP servers total 62 tools across 7 servers (worldai, mcp-agent-mail, slack, ddg-search, perplexity-ask, filesystem, context7). Trim recommendation prioritizes ios-simulator-mcp removal, with estimated savings of ~920 tokens (config + runtime).

## Server Inventory

### Connected Servers (74 deferred tools)

| Server | Tools | Status |
|--------|-------|--------|
| worldai | 16 | KEEP — core project |
| mcp-agent-mail | 17 | KEEP — inter-agent coordination |
| slack | 11 | KEEP — notifications |
| ddg-search | 3 | KEEP — web research |
| perplexity-ask | 1 | KEEP — AI research |
| filesystem | 14 | KEEP — file operations |
| ios-simulator-mcp | 12 | **TRIM** — only non-essential connected server |
| **TOTAL** | **74** | |

### Not Connected (config-only, no runtime cost)

- sequential-thinking (redundant with built-in Think tool)
- context7 (rarely used, built-in WebFetch covers it)
- gemini-cli-mcp (covered by /secondo)
- memory-server (redundant with MEMORY.md + mem0 hooks)
- grok-mcp (requires XAI_API_KEY, covered by /secondo)
- render (cloud deployment, not used)
- serena (code intelligence, not connected)
- mcp-search (thedotmack plugin, not connected)
- chrome-superpower (npx server, not connected)

## Token Impact

Each deferred tool occupies ~15-25 tokens in system-reminder block. ios-simulator-mcp is the only TRIM server actually connected, adding 12 deferred tool entries × ~20 tokens = ~240 tokens/turn persistent overhead.

| Action | Token Savings |
|--------|-------------|
| Remove ios-simulator-mcp | ~240 tokens/turn + ~80 config |
| Remove 8 other non-connecting servers | ~600 tokens (one-time config load) |
| **Total potential** | **~920 tokens** |

## Recommendations

1. **Priority 1**: Remove ios-simulator-mcp from plugin settings — only connected TRIM server
2. **Priority 2**: Remove 8 non-connecting servers from plugin settings — faster startup
3. **Priority 3**: Evaluate filesystem redundancy (14 tools overlap with built-in Read/Write/Glob)
4. **Not recommended to trim**: slack (actively used), mcp-search (different plugin), mcp-agent-mail (core)

## Connections

- [[ClaudeCode]] — MCP servers affect Claude Code CLI context budget
- [[ContextCompaction]] — MCP trim reduces compaction pressure
- [[AdaptiveContextTruncation]] — related to context management

## Contradictions

- None identified

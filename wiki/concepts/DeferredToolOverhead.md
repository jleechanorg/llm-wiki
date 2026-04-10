---
title: "Deferred Tool Overhead"
type: concept
tags: [mcp, context, tokens, claude-code, optimization]
sources: [mcp-trim-analysis-2026-04-05, context-compaction-research-2026-04-05]
last_updated: 2026-04-09
---

## Summary
Deferred tool registration is the persistent per-turn context cost from MCP server tools being listed in every system-reminder block. Each tool occupies ~15-25 tokens, and the cumulative overhead from ios-simulator-mcp alone (~240 tokens/turn) contributed to Claude Code compaction frequency.

## Key Claims
- Each deferred tool: ~15-25 tokens per system-reminder block
- ios-simulator-mcp (12 tools): ~240 tokens/turn persistent overhead
- Total deferred tool count this session: 74 tools from 7 connected servers
- Config definitions add ~50-150 tokens per server on settings file load (one-time)
- ~19K per-turn system-reminder overhead from skills (~15K), hooks (~4K), deferred tools, and MCP descriptions

## Connection to Compaction
Per-turn overhead is the primary driver of compaction frequency. The main session (229 user messages, 54 compactions) had massive overhead, while test sessions (86 messages, 0 compactions) lacked it and never hit the threshold.

## Connections
- [[MCPServerInstructions]] — deferred tool listing in MCP config
- [[ContextBloat]] — deferred tool overhead part of per-turn context cost
- [[Compaction]] — overhead driver of compaction frequency
- [[ClaudeCode]] — where deferred tools appear in system reminders

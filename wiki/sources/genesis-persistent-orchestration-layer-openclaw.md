---
title: "Genesis: Persistent Orchestration Layer for OpenClaw"
type: source
tags: ["openclaw", "genesis", "orchestration", "memory", "mcp"]
date: 2026-04-07
source_file: "raw/llm_wiki-raw-genesis-persistent-orchestration-layer.md"
sources: []
last_updated: 2026-04-07
---

## Summary
Genesis is a configuration and content layer on top of OpenClaw—not a new system. After analyzing OpenClaw docs and source, most proposed Genesis features already exist natively. The real work is filling in existing blank files and tuning configuration. This doc covers what OpenClaw provides, what's genuinely new, and the implementation plan.

## Key Claims
- **Memory System**: OpenClaw uses plain Markdown files as source of truth; SQLite is just an auto-generated search index
- **Workspace Files**: SOUL.md, USER.md, TOOLS.md, MEMORY.md, HEARTBEAT.md structure with specific blank files needing content
- **Session Startup**: Loads today's daily log, yesterday's daily log, SOUL.md, and USER.md automatically
- **Memory Tools**: Built-in memory_search and memory_get for semantic and keyword search
- **Configuration Options**: MemorySearch with hybrid query (vector + text weights), temporal decay, and MMR diversity
- **Cron System**: Native 3x daily Slack check-ins + 4-hourly backups; Genesis uses same format
- **MCP Mail**: Genesis registered as agent #1778 enabling cross-agent coordination

## Key Quotes
> "Genesis is a configuration and content layer on top of OpenClaw — not a new system."

> "The sqlite DB at `~/.openclaw/memory/<agentId>.sqlite` is just an auto-generated index for search."

> "At session startup, OpenClaw loads: today's daily log, yesterday's daily log, SOUL.md, USER.md."

## Connections
- [[OpenClaw]] — underlying platform
- [[worldarchitect.ai]] — user's primary project
- [[MCP Mail]] — Genesis registered for cross-agent coordination
- [[MemorySearch]] — configurable hybrid search system

## Contradictions
- None identified

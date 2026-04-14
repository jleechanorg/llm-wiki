---
title: "mvp_site memory_mcp_real"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/memory_mcp_real.py
---

## Summary
Documentation of architectural limitation: Python cannot directly integrate with Claude Code's MCP tools. MCP tools exist in Claude's execution environment and are NOT Python modules callable from Python runtime. Memory enhancement should be implemented as behavioral protocol in CLAUDE.md.

## Key Claims
- MCP tools (mcp__memory-server__search_nodes) NOT accessible from Python
- MemoryMCPInterface documents the limitation: returns empty list or False
- Architectural correct approach: LLM handles memory searches directly

## Connections
- [[MemoryManagement]] — architectural limitation documentation

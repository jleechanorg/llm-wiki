---
title: "MCP Server Instructions"
type: concept
tags: [mcp, server, integration, claude-code]
sources: [claude-code-system-prompt-captured-via-debug-mode]
last_updated: 2026-04-07
---

MCP Server Instructions are detailed commands that connected MCP (Model Context Protocol) servers provide to Claude Code for tool availability and usage. These instructions are embedded in the system prompt and inform Claude about capabilities like semantic operations (Serena MCP), domain-specific tools, and server-specific behaviors.

## Tool Hierarchy (from system prompt)
1. **Serena MCP** — Semantic operations (preferred)
2. **Read/Edit Tools** — File operations
3. **Bash Tools** — System operations (restricted)
4. **Specialized MCPs** — Domain-specific operations

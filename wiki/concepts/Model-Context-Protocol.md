---
title: "Model Context Protocol (MCP)"
type: concept
tags: [mcp, protocol, ai, tool-calling]
sources: [worldai-mcp-stdio-adapter]
last_updated: 2026-04-08
---

## Description
Model Context Protocol — a standard for AI systems to call tools. The stdio adapter implements MCP 2024-11-05 protocol version.

## Key Components
- **initialize handshake**: Required before tool calls, exchanges protocol version and capabilities
- **tools capability**: Server exposes available tools to the client
- **resources capability**: Server exposes readable resources

## Connections
- [[WorldAI MCP STDIO Adapter]] — Implements MCP as stdio-based server
- [[WorldAIToolsProxy]] — Provides tool implementation backing this MCP server

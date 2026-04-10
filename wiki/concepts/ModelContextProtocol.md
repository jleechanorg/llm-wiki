---
title: "Model Context Protocol (MCP)"
type: concept
tags: [protocol, mcp, ai, json-rpc]
sources: []
last_updated: 2026-04-08
---

## Description
MCP (Model Context Protocol) is a protocol for AI systems to interact with external tools and resources. It uses JSON-RPC 2.0 for communication, enabling AI models to call functions, list available tools, and access resources.

## MCP in WorldArchitect
The WorldArchitect.AI MCP server provides:
- `tools/list` — enumerate available tools
- `resources/list` — enumerate available resources
- Custom tool invocations for database and game operations

## Related
- [[MCP Client Library for WorldArchitect.AI]] — production client implementation
- [[MCP Test Client for WorldArchitect.AI]] — testing utility

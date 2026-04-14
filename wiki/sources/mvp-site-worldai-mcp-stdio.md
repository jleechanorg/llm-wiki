---
title: "mvp_site worldai_mcp_stdio"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/worldai_mcp_stdio.py
---

## Summary
WorldAI MCP STDIO adapter providing stdio-based MCP server that reads JSON-RPC requests from stdin and writes responses to stdout. Wraps WorldAIToolsProxy for handling actual MCP logic.

## Key Claims
- main() runs the stdio MCP adapter reading from stdin, writing to stdout
- WORLDTOOLS_UPSTREAM_MCP_URL for upstream MCP server
- WORLDTOOLS_DEV_MODE for development vs production mode
- Uses firestore_service.json_default_serializer for JSON serialization

## Connections
- [[MCPApi]] — stdio adapter for MCP server

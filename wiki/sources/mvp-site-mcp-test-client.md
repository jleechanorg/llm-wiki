---
title: "mvp_site mcp_test_client"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/mcp_test_client.py
---

## Summary
MCP Test Client for WorldArchitect.AI providing programmatic testing interface for the MCP server. Sends JSON-RPC requests via HTTP and logs request/response pairs.

## Key Claims
- MCPTestClient class for programmatic MCP server testing
- MCP_HTTP_PATH = "/mcp" endpoint
- Supports request/response logging to file
- Request counter for tracking

## Connections
- [[MCPApi]] — test client for MCP server

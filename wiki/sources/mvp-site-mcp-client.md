---
title: "mvp_site mcp_client"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/mcp_client.py
---

## Summary
MCP Client Library for communicating with world_logic.py MCP server. Provides JSON-RPC communication, translation between Flask HTTP and MCP protocol, and error handling with MCP-to-HTTP status code mapping.

## Key Claims
- MCPClient class for JSON-RPC communication with MCP server
- MCP_HTTP_PATH = "/mcp" endpoint
- MCPErrorCode enum for JSON-RPC 2.0 error codes
- MCPError dataclass with code, message, data fields
- Async-compatible design for future async Flask integration

## Connections
- [[MCPApi]] — client for MCP server communication

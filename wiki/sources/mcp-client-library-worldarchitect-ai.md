---
title: "MCP Client Library for WorldArchitect.AI"
type: source
tags: [python, mcp, json-rpc, http, client-library, worldarchitect]
source_file: "raw/mcp-client-library-worldarchitect-ai.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python MCP (Model Context Protocol) client library enabling main.py to communicate with the world_logic.py MCP server. Handles JSON-RPC 2.0 communication over HTTP with translation functions between Flask HTTP requests/responses and MCP protocol. Supports both HTTP and direct module calls, with async-compatible design for future Flask integration.

## Key Claims
- **JSON-RPC 2.0 Communication**: MCPClient class provides structured JSON-RPC communication with the MCP server
- **HTTP-to-MCP Translation**: http_to_mcp_request() and mcp_to_http_response() convert between Flask and MCP formats
- **Error Sanitization**: Prevents internal detail leakage by sanitizing error messages (filters sensitive patterns like "firestore", "credentials", "localhost")
- **Class-Level Event Loop**: Shared event loop singleton for sync operations with performance optimization
- **Flexible Modes**: Supports both HTTP communication and direct skip_http mode for module invocation

## Key Quotes
> MCPClient class for JSON-RPC communication with MCP server
> from mvp_site.mcp_client import MCPClient, http_to_mcp_request, mcp_to_http_response

## Connections
- [[WorldArchitect]] — the application this MCP client serves
- [[FirestoreService]] — referenced for database operations
- [[Flask]] — web framework for HTTP handling
- [[JSON-RPC]] — protocol standard for client-server communication

## Contradictions
- None identified

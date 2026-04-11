---
title: "MCP Test Client for WorldArchitect.AI"
type: source
tags: [python, mcp, testing, json-rpc, http, client]
source_file: "raw/mcp-test-client-worldarchitect-ai.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python test client providing programmatic testing interface for the WorldArchitect.AI MCP server. Offers health checking, JSON-RPC 2.0 request sending, tool/resource listing, and optional request/response logging to JSON files for debugging.

## Key Claims
- **Programmatic Testing Interface**: MCPTestClient class enables automated testing of MCP server endpoints without manual curl/Postman calls
- **JSON-RPC 2.0 Compliance**: Sends proper JSON-RPC 2.0 requests with method, params, id, and jsonrpc version fields
- **Request/Response Logging**: Optional log_file parameter writes all requests/responses to JSON for debugging failed test cases
- **Session Management**: Uses requests.Session for connection pooling and consistent headers across multiple requests

## Key Methods
- `health_check()` - GET /health endpoint for server availability
- `json_rpc_request(method, params, request_id)` - Send arbitrary JSON-RPC method calls
- `list_tools()` - Enumerate available MCP tools via tools/list
- `list_resources()` - Enumerate available MCP resources via resources/list

## Connections
- [[MCP Client Library for WorldArchitect.AI]] — complements this test client; client library is production code while this is testing utility
- [[WorldArchitect.AI]] — the service being tested

## Contradictions
- None identified

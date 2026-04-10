---
title: "JSON-RPC"
type: concept
tags: [json-rpc, protocol, api]
sources: [worldai-tools-mcp-proxy-tests]
last_updated: 2026-04-08
---

## Description
JSON-RPC 2.0 protocol used by MCP for remote procedure calls. The proxy handles requests with format: `{jsonrpc: "2.0", id, method, params}` and returns either result or error objects.

## Error Codes Used
- -32602: Invalid params — missing required fields (reason, ticket_id) or invalid input format
- -32603: Internal error — unexpected processing failures

## Relationship to MCP
MCP uses JSON-RPC as its wire protocol. The proxy validates request shape before passing to tool handlers.

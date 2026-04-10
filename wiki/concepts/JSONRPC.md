---
title: "JSON-RPC 2.0"
type: concept
tags: [protocol, json-rpc, api, http]
sources: []
last_updated: 2026-04-08
---

## Description
JSON-RPC 2.0 is a stateless, lightweight remote procedure call (RPC) protocol that uses JSON for data encoding. Key features include:
- Request objects: `{"jsonrpc": "2.0", "method": "foo", "params": {}, "id": 1}`
- Response objects: `{"jsonrpc": "2.0", "result": {}, "id": 1}`
- Error responses: `{"jsonrpc": "2.0", "error": {"code": -32600, "message": "..."}, "id": 1}`

## Usage in MCP
MCP (Model Context Protocol) uses JSON-RPC 2.0 as its transport layer. MCP clients send requests like:
```json
{"jsonrpc": "2.0", "method": "tools/list", "id": 1}
```

And receive responses with tool/resource listings.

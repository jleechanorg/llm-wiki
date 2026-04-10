---
title: "JSON-RPC 2.0"
type: concept
tags: [json-rpc, protocol, rpc]
sources: [worldai-mcp-stdio-adapter]
last_updated: 2026-04-08
---

## Description
JSON-RPC 2.0 specification used by the WorldAI MCP STDIO Adapter. Key aspects:
- **Notifications**: Requests without `id` field are notifications — server MUST NOT respond
- **Invalid Request**: Payload must be an object, not array or primitive
- **Error Codes**: -32700 (Parse Error), -32600 (Invalid Request), -32603 (Internal Error)

## Connections
- [[WorldAI MCP STDIO Adapter]] — Implements JSON-RPC 2.0 protocol for MCP communication

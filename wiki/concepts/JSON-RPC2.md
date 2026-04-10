---
title: "JSON-RPC 2.0"
type: concept
tags: [json-rpc, protocol, rpc]
sources: [worldai-tools-mcp-proxy-runtime]
last_updated: 2026-04-08
---

JSON-RPC 2.0 is a stateless, lightweight remote procedure call protocol. The WorldAI MCP implementations use it for:
- Request/response message formatting
- Notification handling (no id field = no response)
- Error code propagation

## Related
- [[MCP]]

---
title: "WorldAI MCP STDIO Adapter"
type: source
tags: [python, mcp, json-rpc, stdio, adapter]
source_file: raw/worldai_mcp_stdio_adapter.py
sources: []
last_updated: 2026-04-08
---

## Summary
Python module providing a stdio-based MCP server that reads JSON-RPC requests from stdin and writes responses to stdout. Wraps [[WorldAIToolsProxy]] for handling actual MCP logic, with support for environment-driven configuration and authentication context building.

## Key Claims
- **Stdio I/O**: Uses `readline()` to avoid stdin buffering issues, processing line-by-line
- **MCP Handshake**: Handles `initialize` method with protocol version 2024-11-05, exposing tools and resources capabilities
- **JSON-RPC 2.0**: Properly handles notifications (no id) vs requests (has id), skipping responses to notifications per spec
- **Environment Config**: Reads WORLDAI_DEV_MODE, WORLDTOOLS_UPSTREAM_MCP_URL, TESTING_AUTH_BYPASS, WORLDTOOLS_UNSAFE_SKIP_AUTH
- **Auth Context**: Uses `_build_auth_context_for_stdio(proxy)` to populate roles from allowlists
- **Error Handling**: Returns structured JSON-RPC errors with codes -32600 (Invalid Request), -32700 (Parse Error), -32603 (Internal Error)
- **Dev Mode**: Exposes full stack traces in dev mode, generic messages in production

## Key Functions
- `main()` — Entry point that configures environment, creates proxy, and runs stdin read loop
- `_build_auth_context_for_stdio(proxy)` — Builds auth context with roles from allowlists when WORLDTOOLS_TRUST_ACTOR_EMAIL_HEADERS is set

## Connections
- [[WorldAIToolsProxy]] — Wrapped by this adapter for actual MCP tool handling
- [[Unified API Implementation]] — Shares firestore_service for JSON serialization

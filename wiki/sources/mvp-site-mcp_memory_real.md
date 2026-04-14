---
title: "mcp_memory_real.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
Real Memory MCP integration for production use. Provides fail-fast design where errors propagate to callers rather than silently returning empty data. Replaces mcp_memory_stub.py when ready for production.

## Key Claims
- `MCPMemoryClient` class with dependency injection support for testing
- FAIL-FAST design: all operations raise `MCPMemoryError` on failure instead of returning empty data
- Provides `search_nodes()`, `open_nodes()`, and `read_graph()` functions
- Uses `_get_mcp_function()` to dynamically resolve MCP functions from globals
- Dependency injection via `set_functions()` allows partial overrides for testing
- Module-level functions for backward compatibility with existing code

## Key Quotes
> "FAIL-FAST DESIGN: If MCP functions are not available or fail, errors propagate to the caller rather than silently returning empty data."

## Connections
- [[memory_integration]] — uses these MCP functions to enhance LLM responses
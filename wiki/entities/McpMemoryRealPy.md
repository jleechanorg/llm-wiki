---
title: "McpMemoryReal.py"
type: entity
tags: [python, file, mcp, memory]
sources: ["fallback-behavior-review-mvp-site"]
last_updated: 2026-04-08
---

MCP memory client implementation. Key behaviors:
- `_get_mcp_function` — resolves MCP functions from globals, fails fast if handlers missing
- Public methods — validate function pointers non-None before invocation
- `MCPMemoryError` — explicit error raised when functions unavailable
- `set_functions()` — requires all three MCP functions together, rejects partial injection

## Rationale
Fail-fast behavior surfaces configuration errors immediately rather than masking with fallbacks.

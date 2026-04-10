---
title: "MCPMemoryError"
type: concept
tags: [python, exception, mcp, error-handling]
sources: ["real-memory-mcp-integration"]
last_updated: 2026-04-08
---

## Definition
Custom exception class raised when MCP memory operations fail. Part of the FAIL-FAST design pattern where errors propagate to callers rather than being silently handled.

## Usage
Raised in the following scenarios:
- No MCP functions available at initialization
- search_nodes function not available
- open_nodes function not available
- read_graph function not available

## Related Concepts
- [[Exception Handling]] — Python exception patterns
- [[FAIL-FAST Design]] — error handling philosophy

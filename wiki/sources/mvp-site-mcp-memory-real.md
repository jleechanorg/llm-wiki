---
title: "MCP Memory Real"
type: source
tags: [mcp, memory, production, dependency-injection]
sources: [mvp-site-mcp-memory-real]
last_updated: 2025-01-15
---

## Summary

Production MCP memory integration with fail-fast design. Provides actual MCP client for search_nodes, open_nodes, read_graph operations.

## Key Claims

- **MCPMemoryClient**: Client with dependency injection for testing
- **Fail-fast design**: Raises MCPMemoryError on failure instead of silent empty returns
- **Backward compatible**: Module-level functions delegate to global instance
- **Function injection**: set_functions() for testing with mock functions
- **Globals-based init**: Automatically finds MCP functions from globals

## MCP Functions

- search_nodes(query): Search memory graph
- open_nodes(names): Open specific memory nodes
- read_graph(): Read entire memory graph

## Error Handling

All operations raise MCPMemoryError on failure - callers must handle explicitly.

## Connections

- [[mvp-site-memory-integration]] - Memory integration using this client

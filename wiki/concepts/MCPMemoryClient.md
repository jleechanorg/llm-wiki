---
title: "MCPMemoryClient"
type: concept
tags: [python, mcp, client, memory, error-handling]
sources: ["real-memory-mcp-integration"]
last_updated: 2026-04-08
---

## Definition
MCP Memory client class with dependency injection support. Provides FAIL-FAST error handling where all operations raise MCPMemoryError on failure instead of returning empty data.

## Properties
- `_search_fn`: Callable for search_nodes function
- `_open_fn`: Callable for open_nodes function
- `_read_fn`: Callable for read_graph function
- `_initialized`: Boolean tracking initialization state

## Methods
- `initialize()`: Resolves MCP functions from globals() at startup
- `set_functions()`: Dependency injection for testing (allows partial overrides)
- `search_nodes(query: str)`: Calls MCP search_nodes, raises on failure
- `open_nodes(names: list[str])`: Calls MCP open_nodes, raises on failure
- `read_graph()`: Calls MCP read_graph, raises on failure

## Related Concepts
- [[Dependency Injection]] — pattern used for testability
- [[FAIL-FAST Design]] — error handling philosophy
- [[MCP (Model Context Protocol)]] — underlying protocol

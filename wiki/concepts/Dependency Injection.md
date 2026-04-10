---
title: "Dependency Injection"
type: concept
tags: [design-pattern, testing, python, dependency-management]
sources: ["real-memory-mcp-integration"]
last_updated: 2026-04-08
---

## Definition
Software design pattern where dependencies are provided to a class rather than being created internally. Enables testing by allowing mock/stub implementations to be injected.

## Application in MCPMemoryClient
- `set_functions()` method accepts optional callable overrides
- Allows partial overrides (only inject what needs mocking)
- Bypasses globals lookup after injection
- Supports both real MCP and test doubles

## Related Concepts
- [[MCPMemoryClient]] — class using this pattern
- [[TestServiceProvider Implementation]] — related test infrastructure

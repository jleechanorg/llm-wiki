---
title: "Real Memory MCP Integration"
type: source
tags: [python, mcp, memory, integration, production, fail-fast]
source_file: "raw/real-memory-mcp-integration.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Production MCP integration module replacing mvp_site's stub implementation. Provides MCPMemoryClient class with dependency injection support for testing. Uses FAIL-FAST design where errors propagate to callers instead of silently returning empty data.

## Key Claims
- **FAIL-FAST Design**: All operations raise MCPMemoryError on failure rather than returning empty data; callers must handle errors explicitly
- **Dependency Injection**: set_functions() allows partial overrides of MCP functions for testing without requiring real MCP availability
- **Lazy Initialization**: MCP function references resolved at startup via globals() lookup; raises error if no functions available
- **Backward Compatibility**: Global _mcp_client instance provides backward compatibility with existing code

## Key Quotes
> "FAIL-FAST DESIGN: If MCP functions are not available or fail, errors propagate to the caller rather than silently returning empty data."

## Connections
- [[MCP Client Library for WorldArchitect.AI]] — provides MCP communication layer this module depends on
- [[TestServiceProvider Implementation]] — test infrastructure that may use dependency injection patterns from this module

## Contradictions
- None detected

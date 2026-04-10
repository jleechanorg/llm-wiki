---
title: "MCP Protocol"
type: concept
tags: [mcp, protocol, testing, async]
sources: [campaign-pagination-mcp-integration-test]
last_updated: 2026-04-08
---

## Summary
Model Context Protocol — a standard interface for async tool invocation in testing contexts. Enables language-agnostic tool calling through tools_call_async pattern.

## Key Characteristics
- Async tool invocation via tools_call_async
- Request/response pair capture for evidence
- Pagination support with cursor metadata
- Protocol-agnostic implementation

## Related Concepts
- [[CursorBasedPagination]] — pagination technique
- [[EvidenceBundles]] — evidence capture

---
title: "PR #341: feat: replace fastmcp with direct mcp server"
type: source
tags: [codex]
date: 2025-10-14
source_file: raw/prs-/pr-341.md
sources: []
last_updated: 2025-10-14
---

## Summary
- replace the FastMCP-based server factory with a direct MCP implementation that adds first-class tool registry, protocol handler, session manager, event bus, and HTTP server
- migrate the backend to the new `createMCPServer` entry point, update startup scripts, and remove FastMCP-specific glue code and tests
- add comprehensive unit tests for the new MCP infrastructure and update existing backend tests to reflect the new architecture
- harden backend Jest fetch mocks to respect dynamic local po

## Metadata
- **PR**: #341
- **Merged**: 2025-10-14
- **Author**: jleechan2015
- **Stats**: +58/-20 in 2 files
- **Labels**: codex

## Connections

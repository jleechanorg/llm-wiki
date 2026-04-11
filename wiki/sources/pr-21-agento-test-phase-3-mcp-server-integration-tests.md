---
title: "PR #21: [agento] test: Phase 3 — MCP server integration tests (33 tests)"
type: source
tags: []
date: 2026-03-27
source_file: raw/prs-/pr-21.md
sources: []
last_updated: 2026-03-27
---

## Summary
Phase 3 of the TDD roadmap: 33 integration tests (10 HTTP + 23 tools) for the Blog MCP server.

### tests/blog/server-http.test.ts (10 tests)
Supertest-based HTTP tests against the real Express app from `createBlogApp()`:
- `POST /mcp`: health_check, unknown method (-32601), missing id, malformed JSON (400), invalid jsonrpc (-32600), non-object body (400), no-auth-required
- `GET /health`, `GET /`, `GET /mcp`

### tests/blog/tools-integration.test.ts (23 tests)
Real `MemoryBlogStorage` + `create

## Metadata
- **PR**: #21
- **Merged**: 2026-03-27
- **Author**: jleechan2015
- **Stats**: +2368/-5 in 14 files
- **Labels**: none

## Connections

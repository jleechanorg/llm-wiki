---
title: "PR #224: feat(python-mcp-server-utils): align utilities with ts parity"
type: source
tags: [codex]
date: 2025-10-07
source_file: raw/prs-/pr-224.md
sources: []
last_updated: 2025-10-07
---

## Summary
- allow the FastMCP HTTP proxy helper to accept mapping-style CORS configuration and tolerate partial loggers while keeping parity with the TypeScript implementation
- ensure the server factory relies on inspect for awaitable tool registration to mirror runtime expectations
- add pytest coverage for the HTTP proxy, server factory, and tool helper utilities to lock in behaviour

## Metadata
- **PR**: #224
- **Merged**: 2025-10-07
- **Author**: jleechan2015
- **Stats**: +418/-4 in 5 files
- **Labels**: codex

## Connections

---
title: "Unified API"
type: concept
tags: [architecture, api, pattern]
sources: [unified-api-implementation]
last_updated: 2026-04-08
---

## Description
Architectural pattern where core business logic is centralized in shared functions with consistent JSON input/output, consumed by multiple entry points (Flask and MCP). Eliminates duplication and ensures consistent behavior across different API surfaces.

## Key Benefits
- **Single Source of Truth**: Game logic lives in one place
- **Consistent I/O**: All endpoints use the same JSON structure
- **Centralized Error Handling**: One place for response formatting
- **Flexible Authentication**: Supports both session-based (Flask) and explicit parameter (MCP) user identification

## Implementation
- Async functions use asyncio.to_thread() for blocking I/O
- Enables concurrent request handling (e.g., loading campaigns while actions process)
- Firebase/Gemini calls don't block the shared event loop

---
title: "Unified API Implementation"
type: source
tags: [python, api, flask, mcp, async, firebase]
source_file: raw/unified_api_layer.md
sources: []
last_updated: 2026-04-08
---

## Summary
Python module providing consistent JSON interfaces for both Flask and MCP server usage in WorldArchitect.AI. Extracts shared business logic and standardizes input/output formats across different entry points.

## Key Claims
- **Unified Functions**: Core game logic centralized in shared functions rather than duplicated across Flask/MCP
- **Consistent JSON I/O**: Standardized input/output structures for all API endpoints
- **Async Support**: Uses asyncio.to_thread() for blocking I/O operations to prevent event loop blocking during Gemini/Firestore calls
- **Firebase Integration**: Initializes Firebase with clock skew patch handling for credential issues
- **Service Account Loading**: Supports file-based and environment variable fallback credential loading

## Key Functions
- `is_mock_services_mode()`: Runtime check for mock environment detection
- Firebase initialization with clock skew patch application
- Service account credential loading with fallback logic
- Async-compatible functions for concurrent request handling

## Connections
- [[WorldArchitect.AI]] — the main application this module serves
- [[Firebase]] — backend service for data persistence
- [[Flask]] — web framework entry point
- [[MCP]] — Model Context Protocol server entry point

## Contradictions
- None identified

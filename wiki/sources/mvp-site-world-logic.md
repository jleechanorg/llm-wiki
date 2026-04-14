---
title: "mvp_site world_logic"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/world_logic.py
---

## Summary
Unified API layer for WorldArchitect.AI providing consistent JSON interfaces for both Flask and MCP server usage. Centralizes business logic, error handling, and response formatting. Supports async via asyncio.to_thread() for concurrent requests.

## Key Claims
- Unified functions handle core game logic for both Flask and MCP
- Async functions use asyncio.to_thread() for blocking I/O (Gemini/Firestore)
- Centralized error handling and response formatting
- Consistent user_id extraction across Flask auth and explicit MCP parameters

## Connections
- [[LLMIntegration]] — unified API layer
- [[GameState]] — core game logic

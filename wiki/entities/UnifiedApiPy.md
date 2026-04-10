---
title: "unified_api.py"
type: entity
tags: [python, module, api, architecture]
sources: [unified-api-implementation]
last_updated: 2026-04-08
---

## Description
Python module providing a unified JSON interface layer for WorldArchitect.AI, extracting shared business logic from Flask routes and MCP tools into a single source of truth.

## Attributes
- **File**: `unified_api.py`
- **Type**: Business logic layer
- **Interfaces**: Flask (main.py), MCP (world_logic.py)

## Connections
- Used by [[Flask]] routes and [[MCP Server]] tools
- Depends on [[FirestoreService]], [[LLMService]], [[GameState]]

## Status
Active — serves as single source of truth for campaign creation, action processing, and state management.

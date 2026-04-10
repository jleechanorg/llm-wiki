---
title: "MCP Server"
type: entity
tags: [mcp, server, tools, architecture]
sources: [unified-api-implementation]
last_updated: 2026-04-08
---

## Description
Model Context Protocol server providing tool-based access to WorldArchitect.AI. MCP tools delegate to unified_api.py for business logic.

## Attributes
- **Type**: Tool server
- **File**: world_logic.py
- **Role**: Tool interface for LLM function calling

## Connections
- Tools defined in world_logic.py delegate to [[UnifiedApiPy]]
- Provides function calling interface for campaign management

## Status
Active — tool interface layer.

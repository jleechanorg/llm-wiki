---
title: "mvp_site mcp_api"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/mcp_api.py
---

## Summary
World Logic MCP Server exposing D&D 5e game mechanics as MCP tools. Extracted from monolithic main.py to provide clean API boundaries. Exposes tools for campaign creation, character generation, action processing, and state management.

## Key Claims
- MCP server named "world-logic" with stdio_server transport
- Tools: create_campaign, create_character, process_action, get_campaign_state, update_campaign, export_campaign
- JSON-RPC 2.0 protocol via MCP stdio transport
- Clean separation from HTTP translation layer

## Connections
- [[GameState]] — game mechanics via MCP tools
- [[LLMIntegration]] — MCP server for business logic

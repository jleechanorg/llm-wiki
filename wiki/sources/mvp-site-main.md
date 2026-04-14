---
title: "mvp_site main"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/main.py
---

## Summary
WorldArchitect.AI Flask application serving as pure HTTP-to-MCP translation layer. Zero business logic - all game mechanics delegated to MCP server. Handles authentication, campaign CRUD, interaction processing, and response streaming.

## Key Claims
- Pure API Gateway architecture: HTTP requests translated to MCP tool calls
- MCPClient communicates with world_logic.py MCP server on localhost:8000
- Key routes: GET/POST /api/campaigns, POST /api/campaigns/<id>/interaction
- Streaming support via stream_with_context
- Rate limiting, CORS, compression middleware
- Authentication via Firebase Admin SDK

## Connections
- [[LLMIntegration]] — routes LLM calls through MCP client
- [[GameState]] — game state management via MCP server

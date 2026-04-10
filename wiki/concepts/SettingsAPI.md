---
title: "Settings API"
type: concept
tags: [api, settings, rest]
sources: []
last_updated: 2026-04-08
---

## Summary
REST API endpoints for managing user settings in the application. Includes GET /api/settings for retrieval and POST /api/settings for updates.

## Endpoints
- **GET /settings**: Settings page route
- **GET /api/settings**: Returns current user settings as JSON
- **POST /api/settings**: Updates user settings via JSON payload

## Supported Settings
- gemini_model: Gemini model selection
- debug_mode: Debug flag
- llm_provider: LLM provider selection (including OpenRouter)
- openrouter_model: OpenRouter model selection

## Test Coverage
- Authentication handling with Firebase tokens
- Default constant values (DEFAULT_LLM_PROVIDER, DEFAULT_GEMINI_MODEL)
- Provider-specific settings persistence

## Connections
- [[MCP]] — architecture context
- [[Firebase]] — authentication
- [[Firestore]] — storage backend

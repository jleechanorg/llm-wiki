---
title: "Flask API Pipeline"
type: concept
tags: [flask, api, web, pipeline]
sources: []
last_updated: 2026-04-08
---

The request handling chain from Flask route decorators through business logic to LLM provider calls. The `/api/campaigns/{campaign_id}/interaction` endpoint demonstrates this full pipeline.

## Pipeline Stages
1. **Route**: Flask `@app.route("/api/campaigns/<campaign_id>/interaction")`
2. **Auth**: `verify_id_token` middleware validates request
3. **Data**: Firestore retrieves campaign and game state
4. **LLM**: Selected prompts passed to provider (Gemini, Cerebras, etc.)
5. **Response**: JSON payload returned to client

## Connections
- [[MVPSite]]
- [[Firestore Campaign Storage]]
- [[Gemini Provider]]

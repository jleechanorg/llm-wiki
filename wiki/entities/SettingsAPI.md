---
title: "Settings API"
type: entity
tags: [api, settings, testing]
sources: ["tdd-http-tests-settings-page-ui", "settings-page-api-tests-mcp-architecture"]
last_updated: 2026-04-08
---

Backend API endpoint for persisting and retrieving user settings. Exposed at `/api/settings` with GET (retrieve) and POST (save) methods.

## Tested Behaviors
- GET returns empty `{}` for new users
- POST accepts valid model selections (gemini_model field)
- POST rejects invalid model selections with 400 error
- Settings persist across requests with same user ID

## Connection
- Part of [[SettingsPageUI]] system
- Frontend consumed by [[Settings Page]]

---
title: "Settings Page UI"
type: entity
tags: [ui, settings, frontend]
sources: ["tdd-http-tests-settings-page-ui", "settings-page-api-tests-mcp-architecture"]
last_updated: 2026-04-08
---

User interface for configuring AI model preferences and other settings. Renders at `/settings` route with form elements for model selection.

## Key Features
- AI Model Selection with radio buttons (Gemini Pro 2.5, Gemini Flash 2.5)
- Settings button on homepage with Bootstrap icon
- JavaScript integration via settings.js
- Save message display after settings update

## Connection
- Consumes [[SettingsAPI]] for persistence
- Tested via HTTP in [[TDD HTTP Tests for Settings Page UI Functionality]]

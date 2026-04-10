---
title: "Settings Integration"
type: concept
tags: [architecture, settings, api]
sources: [real-browser-settings-game-integration-test]
last_updated: 2026-04-08
---

Pattern of connecting configuration UI to runtime behavior. The settings integration test proves the settings system works by:
- Exposing /api/settings for model selection
- Persisting gemini_model in user settings
- Having game requests read the setting and route to the correct LLM provider
- Logging model usage for debugging

## Wiki Connections
- [Real Browser Settings Game Integration Test] validates settings integration works end-to-end
- Related to [TestServiceProvider] which mocks services for test isolation

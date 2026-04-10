---
title: "Real Browser Testing"
type: concept
tags: [testing, e2e, browser-automation]
sources: [real-browser-settings-game-integration-test]
last_updated: 2026-04-08
---

E2E testing methodology using real browser automation to verify user-facing workflows. Unlike unit tests with mocks, real browser tests verify the full stack works together (settings UI → API → game logic → logs). The settings game integration test demonstrates this by:
1. Making HTTP requests to the server
2. Creating campaigns
3. Making game requests
4. Reading server logs to verify behavior

## Wiki Connections
- [Real Browser Settings Game Integration Test] is an example of real browser E2E testing
- Differs from [MockServiceProvider] which uses in-memory mocks

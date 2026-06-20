---
title: "Real Browser Testing"
type: concept
tags: [testing, e2e, browser-automation]
sources: [real-browser-settings-game-integration-test]
last_updated: 2026-06-19
---

E2E testing methodology using real browser automation to verify user-facing workflows. Unlike unit tests with mocks, real browser tests verify the full stack works together (settings UI → API → game logic → logs). The settings game integration test demonstrates this by:
1. Making HTTP requests to the server
2. Creating campaigns
3. Making game requests
4. Reading server logs to verify behavior

## Wiki Connections
- [Real Browser Settings Game Integration Test] is an example of real browser E2E testing
- Differs from [MockServiceProvider] which uses in-memory mocks

## Mobile Browser Fidelity

Real browser proof must match the reported browser surface. For mobile auth:

- iOS Simulator Safari is useful for Safari normal/private evidence, but it is not Chrome iOS Incognito.
- Playwright WebKit with an iPhone profile is a closer autonomous WKWebView-shaped signal than Chromium, but it is still not a physical Chrome iOS App Store browser.
- BrowserStack/Sauce/Appium real-device credentials are required for an autonomous physical Chrome iOS lane.
- A passing/failing lower-fidelity browser harness should be labeled `RELATED` unless it shows the exact user-visible phenotype.

Source: [project-2026-06-19-mobile-auth-repro-fidelity](../sources/project-2026-06-19-mobile-auth-repro-fidelity.md).

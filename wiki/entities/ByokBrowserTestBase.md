---
title: "ByokBrowserTestBase"
type: entity
tags: [testing, browser, byok, base-class]
sources: []
last_updated: 2026-04-08
---

Test base class in testing_ui.lib.byok_browser_base for browser testing with BYOK authentication. Provides setup_server, setup_browser, navigate_to_settings, and teardown_browser methods.

## Key Properties
- testing_auth_bypass — enables test authentication mode
- test_user_email — resolved from MCP_TEST_USER_EMAIL or TEST_EMAIL env vars

## Related
- [[GeminiProvider]] — provider being tested
- [[Playwright]] — browser automation framework

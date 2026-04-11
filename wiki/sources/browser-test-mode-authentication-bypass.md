---
title: "Browser Test Mode Authentication Bypass"
type: source
tags: [testing, authentication, browser-testing, playwright, worldarchitect]
source_file: "raw/browser-test-mode-authentication-bypass.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Explains how WorldArchitect.AI browser tests bypass authentication using URL parameters instead of HTTP headers, enabling Playwright-based end-to-end testing without Firebase authentication.

## Key Claims
- **URL Parameter Bypass** — Browser tests use `?test_mode=true&test_user_id=test-user-123` instead of custom HTTP headers
- **Server Requirement** — Backend must be started with `TESTING_AUTH_BYPASS=true` environment variable
- **Frontend Flow** — auth.js detects parameters, api.js injects headers, app.js skips auth checks
- **Backend Validation** — `@check_token` decorator checks `X-Test-Bypass-Auth` header and `X-Test-User-ID`
- **Security** — Test mode only works when explicitly enabled on server; URL parameters ignored in production

## Key Quotes
> "Browser tests cannot set custom HTTP headers like API tests can"

> "Test mode ONLY works when server is started with TESTING_AUTH_BYPASS=true"

## Connections
- [[Firebase]] — Authentication service being bypassed in tests
- [[Firestore]] — Data persistence layer for test user data
- [[Playwright]] — Browser automation framework used for testing
- [[WorldArchitect]] — The application being tested

## Contradictions
- None detected

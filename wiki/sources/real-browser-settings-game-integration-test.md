---
title: "Real Browser Settings Game Integration Test"
type: source
tags: [python, testing, integration-test, e2e, real-browser, settings, gemini]
source_file: "raw/test_real_browser_settings_game_integration.py"
sources: []
last_updated: 2026-04-08
---

## Summary
End-to-end test validating that the settings system integrates with real game functionality. Tests verify model switching (Gemini Flash 2.5 → Gemini Pro 2.5) persists through game requests and is reflected in server logs.

## Key Claims
- **Settings API**: POST /api/settings accepts gemini_model payload and persists the setting.
- **Log verification**: Server logs record which model handled each request for debugging.
- **Model switching**: Users can switch between Gemini Flash 2.5 and Gemini Pro 2.5.
- **Bypass auth**: Test uses X-Test-Bypass-Auth header for isolated testing.
- **Server availability**: Test waits for server startup before executing test scenarios.
- **CI graceful skip**: In CI environments, test skips instead of failing when server unavailable.


## Test Flow
1. Wait for server availability (localhost:8081)
2. Set Gemini Flash 2.5 model via /api/settings
3. Create campaign, make game requests, verify model in logs
4. Switch to Gemini Pro 2.5 model
5. Make more requests, verify Pro model in logs

## Connections
- [[Google]] — provider of Gemini models
- [[mvp_site]] — Flask application with /api/settings endpoint
- [[logging_util]] — provides server log file paths

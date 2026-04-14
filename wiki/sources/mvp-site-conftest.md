---
title: "conftest.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
Global pytest configuration for mvp_site tests. Sets environment variables to force mock/test modes for all tests, preventing real network calls to Gemini/Firebase and clock-skew validation errors.

## Key Claims
- Sets `TESTING_AUTH_BYPASS=true`, `USE_MOCKS=true`, `MOCK_SERVICES_MODE=true`, `WORLDAI_DEV_MODE=true` environment defaults
- Provides dummy API keys (`GEMINI_API_KEY`, `GOOGLE_API_KEY`) to satisfy libraries that check for presence
- Ensures the real Flask module is loaded (some tests monkeypatch sys.modules)
- This configuration is inherited by all tests in the mvp_site test suite
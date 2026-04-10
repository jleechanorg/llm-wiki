---
title: "Test Client Bypass"
type: concept
tags: [testing, bypass, authentication]
sources: []
last_updated: 2026-04-08
---

Testing mechanism that allows tests to run without real API credentials by using a mock client. Enabled via TESTING_AUTH_BYPASS environment variable and triggered when API key matches test pattern.

## Activation Conditions
- TESTING_AUTH_BYPASS="true" in environment
- API key starts with "test-" (e.g., "test-api-key-123")

## Use Cases
- Unit tests without API quota consumption
- CI/CD pipelines without secrets
- Local development without key configuration

## Related
- [[TestClient]] — the mock client used
- [[BYOK]] — pattern being tested

---
title: "TestClient"
type: entity
tags: [testing, mock, client, gemini]
sources: []
last_updated: 2026-04-08
---

Mock Gemini client (_TestClient) used when TESTING_AUTH_BYPASS is enabled and API key matches test pattern. Allows tests to run without real API credentials.

## Usage
Created by gemini_provider.get_client when:
- TESTING_AUTH_BYPASS environment variable is "true"
- API key starts with "test-"

## Related
- [[GeminiProvider]] — creates TestClient instances
- [[BYOK]] — authentication pattern this supports

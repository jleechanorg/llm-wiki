---
title: "BYOK Browser Base Gemini Provider Tests"
type: source
tags: [python, testing, unittest, byok, gemini, api-key, authentication]
source_file: "raw/byok-browser-base-gemini-provider-tests.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python pytest suite validating BYOK (Bring Your Own Key) browser base functionality and Gemini provider API key handling. Tests cover client creation with custom keys, test bypass logic, API key propagation through generate_json_mode_content, and environment variable precedence for test user emails.

## Key Claims
- **Custom API Key**: get_client(api_key=api_key) creates genai.Client with the provided key
- **Test Bypass**: TESTING_AUTH_BYPASS env enables TestClient for keys starting with "test-"
- **Real Key Detection**: Keys not matching test pattern return real genai.Client
- **API Key Propagation**: generate_json_mode_content passes api_key through to get_client
- **Email Precedence**: MCP_TEST_USER_EMAIL takes priority over TEST_EMAIL for test users

## Key Code Patterns
```python
@patch.dict(os.environ, {"TESTING_AUTH_BYPASS": "true"})
def test_get_client_byok_respects_test_bypass_with_test_key():
    api_key = "test-api-key-123"
    client = gemini_provider.get_client(api_key=api_key)
    assert isinstance(client, _TestClient)
```

## Connections
- [[GeminiProvider]] — handles API key and client creation
- [[ByokBrowserTestBase]] — test base class for BYOK browser testing
- [[TestClient]] — mock client for bypassed authentication

## Contradictions
[]

---
title: "HTTP Testing"
type: concept
tags: [testing, http, integration-testing]
sources: ["tdd-http-tests-settings-page-ui"]
last_updated: 2026-04-08
---

Testing methodology that validates application behavior through HTTP requests rather than browser automation. Tests make real HTTP calls to running servers, asserting on response status, headers, and body content.

## Characteristics
- Requires running server (e.g., localhost:8081)
- Uses authentication headers (X-Test-Bypass, X-Test-User-ID)
- Tests API contracts and UI rendering indirectly
- Faster than browser automation, slower than unit tests

## Example
```python
response = requests.get(f"{base_url}/settings")
assert response.status_code == 200
assert b"Settings" in response.content
```

## Connection
- Alternative to [[BrowserAutomationTesting]] and [[UnitTesting]]
- Used in [[TDD HTTP Tests for Settings Page UI]]

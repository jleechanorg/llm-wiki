---
title: "Flask Route Authentication"
type: concept
tags: [flask, authentication, api, security]
sources: []
last_updated: 2026-04-08
---

## Definition
The authentication mechanism for Flask API routes, validating API keys (worldai_ prefix) passed in request headers to control access to protected endpoints.

## Authentication Flow
1. Client includes `Authorization: worldai_xxx` header
2. Flask route validates the key against stored configuration
3. Valid keys allow request processing
4. Invalid/revoked keys return 401 Unauthorized

## Test Coverage
The OpenAI proxy tests validate:
- Valid API keys: Request proceeds normally
- Invalid API keys: 401 response
- Revoked API keys: 401 response
- Missing gateway_url: 400 Bad Request
- Gateway unreachable: 502 Bad Gateway

## Related Concepts
- [[APIKeyValidation]] — the specific validation logic
- [[ErrorHandling]] — response codes for auth failures

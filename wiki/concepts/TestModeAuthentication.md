---
title: "Test Mode Authentication"
type: concept
tags: [testing, authentication, development, bypass, local-dev]
sources: []
last_updated: 2026-04-08
---

Development-only authentication bypass allowing local testing without real Firebase authentication. Enabled via URL parameters (`test_mode`, `test_user_id`, `test_user_email`) and restricted to localhost environments for security.

## Key Features
- **URL Parameters**: `test_mode=true`, `test_user_id`, `test_user_email`
- **Environment Restriction**: Only works on localhost/127.0.0.1/[::1]
- **Header Bypass**: Uses `X-Test-Bypass-Auth`, `X-Test-User-ID`, `X-Test-User-Email` headers
- **Test User Object**: Returns mock user with `uid`, `email`, `isTestUser: true`

## Security Considerations
- Deliberately disabled in production environments
- Console warnings when test mode requested but environment disallowed

## Connections
- [[FirebaseAuthentication]] — Production alternative
- [[WorldArchitectAI]] — Application using test mode

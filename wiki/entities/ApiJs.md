---
title: "ApiJs"
type: entity
tags: [javascript, api, frontend]
sources: ["auth-resilience-clock-skew-tests"]
last_updated: 2026-04-08
---

## Description
Frontend JavaScript module in frontend_v1/ that handles API calls. Implements auto-retry mechanism with retryCount parameter for handling clock skew errors.

## Key Features
- retryCount parameter for tracking retry attempts
- isClockSkewError detection for "Token used too early" errors
- forceRefresh for forcing token refresh on 401 errors
- Recursive retry logic: fetchApi(path, options, retryCount + 1)

## Related Concepts
- [[AutoRetryMechanism]] — the retry logic implementation
- [[AuthenticationResilience]] — overall error handling strategy

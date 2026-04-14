---
title: "test_auth_resilience.py"
type: source
tags: [test, authentication, jwt, resilience]
date: 2026-04-14
source_file: raw/mvp_site_all/test_auth_resilience.py
---

## Summary
Red/Green test suite for authentication resilience features. Tests JWT clock skew auto-retry, user-friendly error messaging, offline campaign caching, and connection status monitoring.

## Key Claims
- JWT clock skew errors trigger automatic retry with fresh token
- User gets helpful error messages instead of generic failures
- Offline campaign data cached in localStorage for offline viewing
- Connection status monitored via navigator.onLine API
- All resilience components properly integrated

## Key Quotes
> "Red test: Verify that clock skew errors trigger auto-retry"
> "Green test: Test the complete resilience workflow end-to-end"

## Connections
- [[AuthenticationResilience]] — JWT clock skew handling
- [[OfflineCaching]] — localStorage campaign caching
- [[ConnectionMonitoring]] — navigator.onLine status tracking

## Contradictions
- None identified in this test file
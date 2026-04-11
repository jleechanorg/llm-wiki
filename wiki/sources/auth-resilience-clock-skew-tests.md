---
title: "Authentication Resilience - JWT Clock Skew Auto-Retry"
type: source
tags: [javascript, testing, unittest, authentication, jwt, resilience]
source_file: "raw/auth-resilience-clock-skew-tests.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest suite validating JWT clock skew error handling in WorldArchitect.AI frontend. Tests verify that "Token used too early" errors trigger automatic retry logic with fresh tokens, and that users receive friendly error messages instead of generic failures.

## Key Claims
- **Auto-Retry Mechanism**: api.js implements retryCount parameter with recursive retry for clock skew errors
- **Clock Skew Detection**: Identifies "Token used too early" errors via isClockSkewError function
- **Token Refresh**: forceRefresh parameter forces token refresh on 401 errors
- **User-Friendly Errors**: Authentication timing issues show "Would you like to try again?" prompt
- **Error Categorization**: Network, authentication, and other error types have specific messages

## Key Test Cases
1. test_clock_skew_auto_retry_mechanism — Validates api.js has retryCount, Token used too early detection, isClockSkewError logic, forceRefresh, and recursive retry call
2. test_user_friendly_error_messages — Validates app.js shows "Authentication timing issue detected", retry option, and categorized error messages
3. test_offline_campaign_caching — Validates campaign data caching for offline access

## Connections
- [[ApiJs]] — implements the auto-retry mechanism
- [[AppJs]] — displays user-friendly error messages
- [[JWT]] — token system experiencing clock skew issues
- [[AuthenticationResilience]] — overall concept of handling auth failures gracefully

## Contradictions
- None identified

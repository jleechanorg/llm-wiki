---
title: "Firebase Authentication with Test Mode Support"
type: source
tags: [firebase, authentication, test-mode, token-refresh, worldarchitect, frontend]
source_file: "raw/firebase-authentication-test-mode-support.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Firebase authentication module for WorldArchitect.AI frontend with development test mode support. Provides Firebase initialization, token refresh scheduling, test user bypass for local development, and unified auth header retrieval. Handles both production Firebase auth and dev-only test mode authentication.

## Key Claims
- **Firebase Initialization**: Immediate initialization on script load to avoid race conditions
- **Test Mode Support**: URL parameter-based test mode (`test_mode`, `test_user_id`, `test_user_email`) for local development with bypass authentication
- **Token Refresh Scheduling**: Automatic token refresh 5 minutes before expiration via `scheduleTokenRefresh`
- **Unified Auth Headers**: Single `getAuthHeaders()` method handles both Firebase and test mode authentication
- **Environment Detection**: Checks hostname to enable test mode only on localhost/127.0.0.1/[::1]

## Key Code Components
- `firebaseConfig`: Firebase configuration object with API key, authDomain, projectId, etc.
- `getBaseAuthHeaders(forceRefresh)`: Returns Firebase auth headers with Bearer token
- `getTestModeParams()`: Extracts test mode parameters from URL
- `window.authTokenManager`: Global API providing `getAuthHeaders()`, `getEffectiveUser()`, `waitForAuthInit()`
- `scheduleTokenRefresh(user)`: Schedules token refresh before expiration
- `canEnableTestMode()`: Validates test mode only allowed on localhost

## Key Quotes
> "Test Mode Params Captured: { enabled, userId, email }" — Console log when test mode activates

## Connections
- [[Firebase]] — Backend authentication service
- [[WorldArchitectAI]] — Frontend application using this auth module
- [[TokenRefresh]] — Automatic token refresh mechanism
- [[TestModeAuthentication]] — Development-only auth bypass

## Contradictions
- None detected

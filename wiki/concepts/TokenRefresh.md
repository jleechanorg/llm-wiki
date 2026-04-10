---
title: "Token Refresh"
type: concept
tags: [authentication, tokens, jwt, refresh, scheduling]
sources: []
last_updated: 2026-04-08
---

Mechanism for maintaining authenticated sessions by refreshing JWT tokens before expiration. Prevents auth failures during long-running sessions by proactively requesting new tokens.

## Key Implementation Details
- **Refresh Buffer**: 5 minutes before expiration (`refreshBufferMs = 5 * 60 * 1000`)
- **Scheduling**: `setTimeout` with calculated delay
- **Force Refresh Option**: `getIdToken(forceRefresh)` parameter for immediate refresh
- **Token Result**: `getIdTokenResult()` provides `expirationTime` for calculations

## WorldArchitect.AI Implementation
- `scheduleTokenRefresh(user)` calculates time until expiration minus buffer
- `clearTokenRefreshTimer()` cancels pending refresh
- Called automatically when user authenticates

## Connections
- [[FirebaseAuthentication]] — Uses token refresh for session maintenance
- [[JWT]] — Token type being refreshed

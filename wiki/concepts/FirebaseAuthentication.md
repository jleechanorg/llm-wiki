---
title: "Firebase Authentication"
type: concept
tags: [authentication, firebase, google, oauth, token-management]
sources: []
last_updated: 2026-04-08
---

Firebase's authentication service providing identity management. Supports email/password, Google OAuth, and custom token authentication. Provides `getIdToken()` for retrieving JWT tokens and `getIdTokenResult()` for token metadata including expiration time.

## Key Features
- **Google Sign-In**: `GoogleAuthProvider` for OAuth flow
- **Token Management**: Automatic token refresh via `getIdToken()`
- **Token Result**: Contains `expirationTime` for scheduling refreshes
- **Current User**: `firebase.auth().currentUser` returns authenticated user

## Connections
- [[Firebase]] — Service provider
- [[TokenRefresh]] — Token refresh scheduling mechanism
- [[TestModeAuthentication]] — Development bypass alternative

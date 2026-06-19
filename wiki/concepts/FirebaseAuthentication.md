---
title: "Firebase Authentication"
type: concept
tags: [authentication, firebase, google, oauth, token-management]
sources: []
last_updated: 2026-06-19
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

## Mobile Redirect Repro Fidelity

For Firebase Google `signInWithRedirect` mobile bugs, distinguish mechanism evidence from exact user-visible repro. The 2026-06-19 mobile auth investigation showed:

- Reaching `worldarchitecture-ai.firebaseapp.com/__/auth/handler` or `accounts.google.com` is only redirect-boundary evidence.
- Evicting Firebase persistence and observing `getRedirectResult()` resolve with `hasUser=false`, `error=null` is a silent-null mechanism signature.
- The exact repro requires return to the app still logged out on the welcome/login UI.
- Simulator Safari normal/private returning authenticated is a `NON-REPRO`, even if the suspected root cause remains plausible for Chrome iOS Incognito.

Source: [[project-2026-06-19-mobile-auth-repro-fidelity]].

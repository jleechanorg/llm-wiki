---
title: "Google OAuth Flow"
type: concept
tags: [oauth, google, firebase, authentication]
sources: [waitlist-gating-account-switching-flow]
last_updated: 2026-06-20
---

## Definition

The Google OAuth Flow is the authentication mechanism that allows users to sign in with their Google account via Firebase Authentication.

## Components

### GoogleAuthProvider
- Firebase's provider for Google Sign-In
- Configured with custom parameters for forced account selection

### Custom Parameters
- `prompt: 'select_account'` — forces Google Account Chooser popup
- Used in [[AccountSwitchingFlow]] to allow waitlist-denied users to choose a different account

### Session Storage Flag
- `worldai_force_google_account_select` — one-shot flag stored in `sessionStorage`
- Read on next sign-in attempt
- Cleared after popup starts

## Flow

1. User clicks "Sign in with Google"
2. Check `sessionStorage` for flag
3. If flag set, configure provider with `prompt: 'select_account'`
4. Call `signInWithRedirect()` or `signInWithPopup()`
5. Firebase handles OAuth redirect
6. On return, dispatch `worldai-auth-ready` event
7. SPA router handles wakeup

## Related Concepts
- [[AccountSwitchingFlow]] — account switching
- [[SPARouting]] — SPA route wakeup
- [[SequenceGuardedCallbacks]] — race condition prevention

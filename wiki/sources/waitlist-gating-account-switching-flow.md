---
title: "Waitlist Gating and Account Switching Flow"
type: source
tags: [worldarchitect, firebase-auth, waitlist, oauth, account-switching, spa-routing]
sources: []
last_updated: 2026-06-20
---

## Summary

The WorldArchitect.AI platform utilizes a waitlist gating mechanism to restrict access to authorized users when waitlist mode is enabled. This document details the account switching flow, prompt enforcement parameters, and client-side routing wake-up sequences designed to handle multi-account sign-in and prevent callback race conditions.

## Key Mechanisms

### 1. Waitlist Gating Mode
- Waitlist mode is enabled site-wide when the environment variable `WAITLIST_MODE_ENABLED` is set to `"true"`, `"1"`, `"yes"`, or `"on"`. By default, it is disabled (`False`).
- Under waitlist mode, all routes check for active user authorization via `/api/waitlist/status`.
- Unauthorized authenticated users are shown the waitlist gate card with a visible option to switch accounts.

### 2. Forced Account Selection ("Use a different account")
- When a user is waitlist-denied, clicking **"Use a different account"** triggers a Firebase sign-out and stores a one-shot flag `worldai_force_google_account_select = "true"` in `sessionStorage`.
- The user is returned to the signed-out splash screen.
- The next Google sign-in request reads this flag. If armed, it sets GoogleAuthProvider's custom parameters (`provider.setCustomParameters({ prompt: 'select_account' })`) to force the Google Account Chooser popup, ensuring the user can choose a different identity instead of auto-logging back into the previously denied Google account.
- The flag is immediately consumed and cleared from `sessionStorage` once the popup starts.

### 3. SPA Route Wakeup (`worldai-auth-ready`)
- Upon successful authentication of a waitlist-allowed account, the auth system dispatches a custom window event: `worldai-auth-ready`.
- The main SPA router in `app.js` listens for this event. Upon trigger, it immediately re-runs route checking (`handleRouteChange()`), clears the auth UI overlay, and loads the dashboard without requiring a manual page refresh.

### 4. Sequence-Guarded Callbacks
- Because Firebase auth state listeners (`onAuthStateChanged`) and waitlist checks (`hasSiteAccess()`) involve asynchronous network requests, they are subject to race conditions (e.g., when a user signs in rapidly after signing out, or on slow network tabs).
- To prevent older callbacks from completing late and clobbering newer state, all async steps in `onAuthStateChanged` check against a monotonic sequence counter (`callbackSeq` / `isCurrentAuthCallback()`). Stale responses are safely discarded.

## Codebase Locations
- **SPA Routing & Gating Integration:** `app.js`
- **Auth, Gating & Account Switching Logic:** `auth.js`
- **Waitlist & Routing Unit Tests:** `waitlist_access.test.js`
- **Auth Watchdog & Event Dispatcher Tests:** `settings_listeners.test.js`
- **Backend Status Resolution:** `firestore_service.py` (specifically `is_waitlist_mode_enabled()` and `get_waitlist_access_status()`)
- **Automated Evidence Capture Script:** `capture_waitlist_auth_followup_pr7705.py`

## Related Wiki Pages
- [[FirebaseAuth]] — authentication backend
- [[SPARouting]] — SPA route handling
- [[OAuthGoogleFlow]] — Google OAuth integration
- [[PR7705]] — related PR

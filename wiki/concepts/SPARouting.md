---
title: "SPA Route Wakeup"
type: concept
tags: [spa, routing, auth, event]
sources: [waitlist-gating-account-switching-flow]
last_updated: 2026-06-20
---

## Definition

SPA Route Wakeup is the mechanism by which the client-side router responds to authentication state changes without requiring a page refresh.

## Mechanism

Upon successful authentication of a waitlist-allowed account, the auth system dispatches a custom window event: `worldai-auth-ready`.

## Handler Behavior

The main SPA router in `app.js` listens for `worldai-auth-ready`. Upon trigger:
1. Immediately re-runs route checking (`handleRouteChange()`)
2. Clears the auth UI overlay
3. Loads the dashboard without manual page refresh

## Why This Matters

Traditional SPA auth flows require page refresh after login. The wakeup event enables:
- Faster perceived load time
- No flash of unauthenticated UI
- Seamless transition from splash to dashboard

## Related Concepts
- [[WaitlistGatingMode]] — access control
- [[AccountSwitchingFlow]] — account switching
- [[SequenceGuardedCallbacks]] — race condition prevention

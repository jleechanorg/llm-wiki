---
title: "Sequence-Guarded Callbacks"
type: concept
tags: [async, race-condition, callback, sequence]
sources: [waitlist-gating-account-switching-flow]
last_updated: 2026-06-20
---

## Definition

Sequence-Guarded Callbacks is a race condition prevention pattern used in the auth state listener and waitlist check flow.

## Problem

Firebase `onAuthStateChanged` and `hasSiteAccess()` involve async network requests. Race conditions occur when:
- User signs in rapidly after signing out
- Slow network tabs process callbacks out of order
- Older callbacks complete late and clobber newer state

## Solution

All async steps check against a monotonic sequence counter:
- `callbackSeq` — global counter incremented on each auth action
- `isCurrentAuthCallback()` — checks if callback's sequence matches current
- Stale responses are safely discarded

## Implementation Pattern

```javascript
let callbackSeq = 0;

function isCurrentAuthCallback(seq) {
  return seq === callbackSeq;
}

function onAuthStateChanged(user) {
  const mySeq = callbackSeq;
  // async operation
  checkWaitlist(user).then(() => {
    if (!isCurrentAuthCallback(mySeq)) return; // stale, discard
    // process response
  });
}

function signOut() {
  callbackSeq++; // increment before async operation
  firebase.signOut();
}
```

## Related Concepts
- [[WaitlistGatingMode]] — access control
- [[AccountSwitchingFlow]] — account switching
- [[SPARouting]] — SPA route wakeup

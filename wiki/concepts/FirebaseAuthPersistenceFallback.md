---
title: "Firebase Auth Persistence Fallback"
type: concept
tags: [firebase-auth, persistence, fallback, web, ios]
sources: [pr7720-ios-webkit-indexeddb-persistence-deadlock]
last_updated: 2026-06-20
---

# Firebase Auth Persistence Fallback

## Persistence tier resolution (Firebase Auth compat SDK 9.6.1)

When `firebase.auth().setPersistence(Persistence.LOCAL)` is requested, the SDK probes backends in order:

1. **`indexedDBLocalPersistence`** — IndexedDB-backed; HANGS on iOS WebKit after OS process suspension (see [[WebKitIndexedDBHangDeadlock]])
2. **`browserLocalPersistence`** — localStorage-backed; safe
3. In-memory fallback — no persistence

The SDK's `_isAvailable()` probe runs once per backend; the first probe returning true wins.

## Why `setPersistence(LOCAL)` alone is not enough

PR #7620 attempted the fix by explicitly calling `setPersistence(Persistence.LOCAL)`. On iOS WebKit, `LOCAL` resolves to `indexedDBLocalPersistence` first — so the explicit call did NOT move off IndexedDB. The fix must happen earlier, before the SDK's first `_isAvailable()` probe, by removing the underlying IndexedDB API.

## Correct fix (from [[PR7720]])

Neutralize `window.indexedDB` BEFORE the first `firebase.auth()` call:

```js
Object.defineProperty(window, 'indexedDB', { configurable: false, value: undefined });
```

This makes step 1's probe fail; the SDK falls through to step 2 (localStorage). The hang is structurally never entered.

## Verification signature

After the fix, on a WebKit environment where IndexedDB is hung:
- `forcedLocalStorage: true`
- `idbOpenCalls: 0`
- Auth callback fires (`authCallbackCount: 1`)

Without the fix:
- `forcedLocalStorage: false`
- IndexedDB opened
- Auth callback never fires (`authCallbackCount: 0`)

## Related

- [[IndexedDBNeutralizationPattern]]
- [[WebKitIndexedDBHangDeadlock]]
- [[FirebaseJSSDK]]
- [[PR7620]]
- [[PR7720]]

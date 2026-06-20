---
title: "Firebase JS SDK"
type: entity
tags: [firebase, sdk, web, auth, indexeddb, webkit-bug, issue-8019]
sources: [pr7720-ios-webkit-indexeddb-persistence-deadlock]
last_updated: 2026-06-20
---

# Firebase JS SDK

**Org:** firebase on GitHub
**Compat version used in worldarchitect.ai prod:** 9.6.1

## Relevant bug

**#8019** — IndexedDB persistence deadlock on iOS WebKit after OS process suspension. Title references "Web-Locks" but the 9.6.1 compat bundle prod ships has zero `navigator.locks` references (verified via `curl -sL --compressed -A "Mozilla/5.0"` against the live 123 KB bundle — bare curl returns a 598 B stub and gives a false 0-count). On 9.6.1 the wedge is the IndexedDB open/read never settling, not Web-Locks coordination (that path is in newer SDK lines).

## Persistence modes (in order of resolution when `LOCAL` is requested)

1. `indexedDBLocalPersistence` — IndexedDB-backed; HANGS on iOS WebKit after suspension
2. `browserLocalPersistence` — localStorage-backed; safe
3. In-memory fallback (no persist)

## Mitigation pattern

Neutralize `window.indexedDB` before any `firebase.auth()` call:

```js
Object.defineProperty(window, 'indexedDB', { configurable: false, value: undefined });
```

This forces step 1's `_isAvailable()` probe to fail, falling back to step 2. See [[PR7720]] for the production usage.

## Related

- [[IndexedDBNeutralizationPattern]]
- [[FirebaseAuthPersistenceFallback]]
- [[WebKitIndexedDBHangDeadlock]]

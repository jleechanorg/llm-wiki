---
title: "IndexedDB Neutralization Pattern"
type: concept
tags: [firebase-auth, web, indexeddb, fallback, pattern]
sources: [pr7720-ios-webkit-indexeddb-persistence-deadlock]
last_updated: 2026-06-20
---

# IndexedDB Neutralization Pattern

## Problem

A library uses `typeof window.indexedDB !== 'undefined'` or an `_isAvailable()` probe to select IndexedDB as its storage backend, but the IndexedDB implementation on the target platform hangs (e.g. iOS WebKit after OS process suspension — see [WebKitIndexedDBHangDeadlock](WebKitIndexedDBHangDeadlock.md)). The hang propagates upward as missing callbacks, blank pages, or stuck loaders.

## Pattern

Neutralize `window.indexedDB` **before** the first library call:

```js
if (typeof window.indexedDB !== 'undefined') {
  Object.defineProperty(window, 'indexedDB', {
    configurable: false,
    value: undefined,
  });
}
```

This makes the library's availability probe fail, forcing a fallback to the next persistence tier (e.g. localStorage).

## Why each detail matters

- **`configurable: false`** locks the override — no later script (third-party SDK, polyfill, ad-injected loader) can re-define the property and undo the fallback. Without this, a race against `defineProperty` on the same property can flip back.
- **Idempotent `typeof` guard** keeps the block safe to include unconditionally; re-running it on a page that already had IndexedDB removed is a no-op.
- **Placed BEFORE any library init call** — once the library has selected a backend and begun using it, neutralizing IndexedDB is too late.

## When to use

- The library has a documented fallback chain and you are stuck on a backend that hangs.
- No other client-side consumer of IndexedDB exists (grep first).
- The fallback tier (localStorage, memory) is acceptable for the use case.

## Trade-off

Clients with existing data in the disabled backend must re-derive state once after deploy. In [PR7720](../entities/PR7720.md) this was a one-shot re-login — strictly better than the previous blank-page cold-restart failure mode.

## Related

- [WebKitIndexedDBHangDeadlock](WebKitIndexedDBHangDeadlock.md)
- [FirebaseAuthPersistenceFallback](FirebaseAuthPersistenceFallback.md)
- [PR7720](../entities/PR7720.md)

---
title: "iOS WebKit IndexedDB Persistence Deadlock — Mobile Game Page Blank Until Cold Restart (PR #7720)"
type: source
tags: [worldarchitect, ios, webkit, firebase-auth, indexeddb, persistence, pr-7720, firebase-js-sdk-8019]
sources: []
last_updated: 2026-06-20
---

# iOS WebKit IndexedDB Persistence Deadlock — PR #7720

**PR:** https://github.com/jleechanorg/worldarchitect.ai/pull/7720
**Component:** `mvp_site/frontend_v1/auth.js` (Firebase Auth web client)
**Date:** 2026-06-20

## The bug (before)

On mobile (iOS Safari/WebKit) the game page rendered blank/hung and only a full cold restart of the browser fixed it — a normal reload did not. Debugged ~1 week.

**Root cause:** the app uses Firebase Auth compat SDK 9.6.1 with `Persistence.LOCAL`. On iOS WebKit that resolves to `indexedDBLocalPersistence`, i.e. the session is stored in IndexedDB. There is a known firebase-js-sdk bug ([#8019](https://github.com/firebase/firebase-js-sdk/issues/8019)): after the OS suspends the browser process, the IndexedDB open/read never settles (hangs forever). Chain reaction:

1. IndexedDB read hangs →
2. Firebase `onAuthStateChanged` never fires →
3. app sees `currentUser == null` →
4. the game-data fetch throws "User not authenticated" →
5. blank page.

A reload reuses the same hung WebKit process + stuck IndexedDB, so it stays broken. Only killing the process (cold restart) clears it. PR #7620's earlier `setPersistence(LOCAL)` did **not** move off IndexedDB.

**Mechanism correction (verified):** #8019's title says "Web-Locks", but the 9.6.1 compat bundle prod ships has **zero** `navigator.locks` references (fetch the live 123 KB bundle with `curl -sL --compressed -A "Mozilla/5.0"`; a bare curl returns a 598 B stub and gives a false 0-count). On 9.6.1 the wedge is the IndexedDB open/read never settling, not Firebase Web-Locks coordination (that path is in newer SDK lines). The fix is unaffected.

## The fix (after)

One change in `mvp_site/frontend_v1/auth.js`, **before** the first `firebase.auth()` call:

```js
Object.defineProperty(window, 'indexedDB', { configurable: false, value: undefined });
```

Deleting `window.indexedDB` makes Firebase's `indexedDBLocalPersistence._isAvailable()` probe fail, so `LOCAL` falls back to `browserLocalPersistence` (localStorage), which does not hang on iOS. The hanging IndexedDB path is structurally never entered; `onAuthStateChanged` fires; the page loads.

- **Safe:** grep confirms no other client-side IndexedDB consumer.
- `configurable: false` locks the override so no later script can undo it; the `typeof window.indexedDB !== 'undefined'` guard keeps the block idempotent.
- **Trade-off:** a client with an existing IndexedDB-stored session re-logs-in once after deploy (self-healing, no cold restart). Strictly better than a blank page.

## How it is proven fixed

Every test simulates the hang (stub `IndexedDB.open` to never settle = the #8019 shape) and checks whether the auth callback still fires. Repro at `testing_ui/mobile_idb_persistence_repro/`. Three real-WebKit surfaces:

- **Playwright WebKit RED/GREEN matrix (6 checks):** RED (no fix) callback never fires + IndexedDB opened; GREEN (fix) callback fires + IndexedDB never opened.
- **Real shipped auth.js in WebKit with IndexedDB hung:** `forcedLocalStorage:true`, `idbOpenCalls:0`, callback fired.
- **Real iOS 18.6 Simulator (MobileSafari):** RED `authCallbackCount:0` (exact prod signature) vs GREEN `authCallbackCount:1`, IndexedDB neutralized. Captioned RED→GREEN GIF.

**Strongest proof:** the DEPLOYED build on a real iOS Simulator renders the sign-in screen (not blank), confirmed by a raw HTTP capture of the served auth.js showing the neutralization block in the shipped bytes.

**Honest limitation:** a 3-lane attempt to reproduce the deadlock **organically** (no stub) failed — the real hang is a device-level OS-process-suspension property, unreachable off a real device from page JS. The deterministic stub is the correct model of its observable shape.

## Not to be confused with

This is the iOS **session-RESTORE** deadlock (already-signed-in user, page won't load). It is DIFFERENT from the Chrome-incognito **SIGN-IN** failure (cross-origin authDomain + third-party-storage blocking), which is PR #7697. #7720 neither causes nor fixes the incognito issue. To test #7720 on a preview use Safari or non-incognito Chrome (incognito on a `*.run.app` preview fails sign-in by design).

## Process learnings (review/merge mechanics)

- A `main`-merge (GitHub "Update branch") pushed onto the PR branch mid-review was based on a pre-fix commit and ORPHANED a later nit-fix commit (it was not an ancestor of the new head), silently reverting `configurable:false` etc. Recovery: `git reset --hard origin/<branch>` to the real head, then `git cherry-pick <orphaned-sha>`. Lesson: **single-writer per branch** while driving to green; verify `git merge-base --is-ancestor` after any external push.
- Green Gate keys off the latest Skeptic Self-Verify VERDICT; dispatch MCP Smoke (real) then Skeptic AFTER it, pinned to the current head SHA. The Skeptic's Gate 8 skips smoke when it can't find the workflow, so smoke is not the true blocker — CI-green + resolved threads + Bugbot-NEUTRAL are.
- Self-hosted CI flakes to expect (NOT regressions): core-mvp shards OOM-`Killed` (...truncated in source...)

## Related entities / concepts

- [[PR7720]] — this PR
- [[FirebaseJSSDK]] — SDK with the #8019 hang bug
- [[WorldArchitectAI]] — host project
- [[IndexedDBNeutralizationPattern]] — the `Object.defineProperty(window, 'indexedDB', ...)` fix idiom
- [[WebKitIndexedDBHangDeadlock]] — the OS-process-suspension phenomenon
- [[FirebaseAuthPersistenceFallback]] — LOCAL → browserLocalPersistence chain
- [[PRMidReviewMergeAncestryCheck]] — git merge-base verification pattern after external pushes
- [[GreenGateWorkflow]] — Skeptic Self-Verify VERDICT keying rules
- [[MobileAuthReproFidelity]] — RED-before-GREEN discipline for mobile browser bugs

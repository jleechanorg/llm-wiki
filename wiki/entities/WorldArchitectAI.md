---
title: "WorldArchitect.AI"
type: entity
tags: [worldarchitect, mvp-site, firebase-auth, frontend, ios, webkit]
sources: [pr7720-ios-webkit-indexeddb-persistence-deadlock]
last_updated: 2026-06-20
---

# WorldArchitect.AI

**Repo:** https://github.com/jleechanorg/worldarchitect.ai
**Org:** jleechanorg
**Component touched by [[PR7720]]:** `mvp_site/frontend_v1/auth.js`

AI-driven worldbuilding platform with Firebase Auth, multiplayer world state, and dice-integrity systems. Mobile clients use Firebase Auth compat SDK 9.6.1, which historically resolves `Persistence.LOCAL` to `indexedDBLocalPersistence` on iOS WebKit, triggering firebase-js-sdk #8019.

The iOS WebKit IndexedDB deadlock (blank game page until cold restart) was debugged ~1 week before [[PR7720]] fixed it via `Object.defineProperty(window, 'indexedDB', {configurable: false, value: undefined})` placed before the first `firebase.auth()` call.

Related: [[FirebaseJSSDK]], [[PR7620]], [[PR7697]].

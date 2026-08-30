---
title: "WorldArchitect.AI"
type: entity
tags: [worldarchitect, mvp-site, firebase-auth, frontend, ios, webkit]
sources: [pr7720-ios-webkit-indexeddb-persistence-deadlock, feedback-2026-07-30-ci-audit-category-and-causal-honesty, feedback-2026-08-30-cloud-run-and-mem0-drift-guardrails]
last_updated: 2026-08-30
---

# WorldArchitect.AI

**Repo:** https://github.com/jleechanorg/worldarchitect.ai
**Org:** jleechanorg
**Component touched by [[PR7720]]:** `mvp_site/frontend_v1/auth.js`

AI-driven worldbuilding platform with Firebase Auth, multiplayer world state, and dice-integrity systems. Mobile clients use Firebase Auth compat SDK 9.6.1, which historically resolves `Persistence.LOCAL` to `indexedDBLocalPersistence` on iOS WebKit, triggering firebase-js-sdk #8019.

The iOS WebKit IndexedDB deadlock (blank game page until cold restart) was debugged ~1 week before [[PR7720]] fixed it via `Object.defineProperty(window, 'indexedDB', {configurable: false, value: undefined})` placed before the first `firebase.auth()` call.

Related: [[FirebaseJSSDK]], [[PR7620]], [[PR7697]].

PR #8675 (July 2026) established the mandatory CI audit methodology requiring exhaustive category-by-category and exact failure-ID reconciliation, with causal honesty (UNKNOWN/NO_VERIFIED_FIX) for uninspected runs. Related: [[AuditIntegrity]], [[CIWorkflowRemediation]], [[CausalHonesty]].

PR #9586 (August 2026) restored exact-name Cloud Run minimum-instance policy: only dev and stable default to one, while preview, staging, ad-hoc, experiment, and unknown services default to zero. The merge did not remediate four already-warm preview services; live enumeration and explicit updates were still required. Related: [[RepositoryDefaultsDoNotRemediateLiveState]], [[CloudRun]].

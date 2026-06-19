---
title: "Mobile auth repro fidelity: boundary evidence is not the exact iOS Chrome symptom"
type: source
date: 2026-06-19
tags: [worldarchitect, firebase-auth, mobile-auth, repro, webkit, chrome-ios, evidence]
bead: rev-g7mp3
source: project_2026-06-19_mobile_auth_repro_fidelity.md
---

# Mobile Auth Repro Fidelity

The 2026-06-19 mobile auth investigation established a reusable repro discipline for Firebase Google sign-in failures on mobile browsers.

## Core Learning

The exact bug phenotype must be written before running tests. For this case, a true repro required the app to return from Google OAuth to `worldarchitect.ai` and remain unauthenticated on the welcome card, matching a silent `getRedirectResult()` null return. Boundary evidence and storage-eviction evidence support root cause, but they are not the original user-visible repro unless that final symptom appears.

## Verdict Classes

| Class | Meaning |
|---|---|
| `REPRO` | Real mobile-ish browser returns to `worldarchitect.ai` after Google OAuth and stays logged out on the welcome card. |
| `RELATED_REDIRECT_BOUNDARY_REACHED` | Browser reaches `worldarchitecture-ai.firebaseapp.com/__/auth/handler` or `accounts.google.com` under the partitioned cross-origin auth flow. |
| `RELATED_SILENT_NULL_SIGNATURE` | Storage eviction makes `getRedirectResult()` settle with `hasUser=false`, `error=null`. |
| `NON-REPRO` | Browser authenticates successfully or fails at an unrelated OAuth error page. |

## Evidence Summary

- iOS 18.6 Simulator Safari normal against production cross-origin Firebase auth returned authenticated as `jleechantest@gmail.com`: `NON-REPRO`.
- iOS 18.6 Simulator Safari Private against production cross-origin Firebase auth returned authenticated: `NON-REPRO`.
- PR #7698 Chromium harness reaches the cross-origin Firebase/Google boundary and reproduces the storage-eviction silent-null mechanism: `RELATED`.
- PR #7698 commit `02c6af2b2cc17f68bf11c7879e01baa2bc5d58b5` added the WebKit/iPhone-context D2c lane. D2c passes with `getRedirectResultAfterEviction.resolved=true`, `hasUser=false`, `error=null`: `RELATED_SILENT_NULL_SIGNATURE`.

## Why Earlier Attempts Were Hard

Chrome iOS is WKWebView-based but is an App Store app, so it is unavailable in local iOS Simulator. Simulator Safari can validate Safari normal/private behavior, but it is not Chrome iOS Incognito. Real OAuth also introduces Google account picker, passkey, password, CAPTCHA/2FA risk, save-password sheets, and redirect URI policy. Without BrowserStack/Sauce/Appium credentials, local no-human work can only prove boundary and mechanism signals, not a physical Chrome iOS Incognito end-to-end symptom.

## Reusable Command

```bash
PATH=/Users/jleechan/.nvm/versions/node/v22.22.0/bin:$PATH \
node --test --test-timeout=90000 testing_ui/mobile_3pc_repro/repro_3pc_auth.spec.mjs
```

Expected current output:

```text
# tests 4
# pass 4
# fail 0
```

## References

- PR #7698: https://github.com/jleechanorg/worldarchitect.ai/pull/7698
- Commit: https://github.com/jleechanorg/worldarchitect.ai/commit/02c6af2b2cc17f68bf11c7879e01baa2bc5d58b5
- Evidence directory: `/tmp/worldarchitectai/prod-ios-crossorigin-20260619T101813Z`
- Codex memory: `/Users/jleechan/.Codex/projects/-Users-jleechan-projects-worktree_mobile_login/memory/project_2026-06-19_mobile_auth_repro_fidelity.md`

[[jeffrey-oracle]]: NO.

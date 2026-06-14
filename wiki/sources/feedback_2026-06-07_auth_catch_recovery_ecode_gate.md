---
title: "Auth Catch Recovery e.code Gate (2026-06-07)"
type: source
tags: [worldarchitect.ai, auth, firebase, root-cause-first, recovery-handler, ecode-gate]
date: 2026-06-07
source_file: raw/feedback_2026-06-07_auth_catch_recovery_ecode_gate.md
---

## Summary
Post-merge review of PR #7321 (mobile auth hang fallback) found the only root-cause-first violation in its incremental delta: a `signInWithPopup` catch block called a recovery handler (which may schedule `window.location.reload()`) unconditionally — including on user-cancellation codes. Fix: gate on `e.code` whitelist (`auth/network-request-failed` / `auth/internal-error` / `auth/timeout` only). Also renamed handler `handleVisibilityRecovery` → `scheduleAuthRecoveryIfStranded` to reflect expanded responsibility across `visibilitychange` + `online` + sign-in-failure paths. Fixed in PR #7349, commit `2fdad5778c`.

## Key Claims
- Never call a recovery handler (especially one that may schedule `window.location.reload()`) unconditionally from a sign-in catch block. Gate on Firebase Auth error code.
- User-cancellation codes (`auth/popup-closed-by-user`, `auth/cancelled-popup-request`, `auth/popup-blocked`) are **user-initiated actions, not hangs** — scheduling a 5-second reload on those cases is symptom-suppression that masks the root cause and degrades UX.
- Whitelist pattern: `e.code === 'auth/network-request-failed' || 'auth/internal-error' || 'auth/timeout'` AND `!authDidInitialize` AND `document.visibilityState === 'visible'`.
- **Heuristic for handler naming:** if a comment on an event-listener teardown line has to be edited to say "and also removes the X listener" (which wasn't in the original), that's a sign the function name lags the responsibility.
- Renames: `handleVisibilityRecovery` → `scheduleAuthRecoveryIfStranded`; `visibilityRecoveryTimer` → `authRecoveryTimer`.

## Key Quotes
> "`auth/popup-closed-by-user`, `auth/cancelled-popup-request`, and `auth/popup-blocked` are all user-initiated actions, not hangs. Scheduling a 5-second page reload on those cases is symptom-suppression that masks the root cause and degrades UX for users who intentionally closed the popup."

> "if a comment on an event-listener teardown line has to be edited to say 'and also removes the X listener' (which wasn't in the original), that's a sign the function name lags the responsibility."

## Connections
- [[RootCauseFirst]] — the violated principle
- [[FirebaseAuthErrorCodes]] — the e.code whitelist
- [[WindowLocationReloadSymptomSuppression]] — anti-pattern
- [[AuthRecoveryHandlerNaming]] — when to rename handlers
- [[WorldArchitectAI]] — repo
- [[SignInWithPopup]] — the call site
- [[VisibilityRecoveryTimer]] — the renamed timer

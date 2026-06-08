---
title: "Authentication"
type: concept
tags: [security, auth, firebase]
sources: [comprehensive-authenticated-api-test-suite, auth-catch-recovery-ecode-gate-2026-06-07]
last_updated: 2026-06-07
---

Authentication verifies user identity before granting access to protected resources. The test suite analyzes API authentication requirements by probing endpoints with and without credentials to understand which endpoints require Firebase authentication.

## Firebase signInWithPopup catch-block pattern

Never call a reload-recovery handler unconditionally from a `signInWithPopup`
catch block. Gate on `e.code` — only fire for genuine network/hang codes:
`auth/network-request-failed`, `auth/internal-error`, `auth/timeout`.
User-cancellation codes (`popup-closed-by-user`, `cancelled-popup-request`,
`popup-blocked`) must fall through to error logging only, not trigger a reload.

See source: [[auth-catch-recovery-ecode-gate-2026-06-07]] | PR #7349

## Handler naming

When an auth-recovery handler is reused across multiple triggers (visibilitychange,
`window 'online'`, sign-in exception), update its name to reflect all responsibilities.
Signal: if teardown comments must be edited to say "and also removes X listener",
the function name lags its scope.

## Connections
- [[Firebase]] — provides authentication backend
- [[API Testing]] — tests auth requirements
- [[root-cause-first]] — catch-block reload-on-any-error is symptom suppression

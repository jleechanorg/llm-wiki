---
name: auth-catch-recovery-ecode-gate
description: signInWithPopup catch block recovery must be gated on e.code (network/hang only); handler renamed scheduleAuthRecoveryIfStranded
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: 25469f06-8a97-4260-9aee-133d0805952a
---

## Rule

In a `signInWithPopup` catch block, never call a recovery handler (especially one
that may schedule `window.location.reload()`) unconditionally. Gate it on the
Firebase Auth error code — only fire for genuine network/hang errors, not for
user-cancellation codes.

**Why:** `auth/popup-closed-by-user`, `auth/cancelled-popup-request`, and
`auth/popup-blocked` are all user-initiated actions, not hangs. Scheduling a
5-second page reload on those cases is symptom-suppression that masks the root
cause and degrades UX for users who intentionally closed the popup.

**How to apply:** Before calling any reload-recovery path from a sign-in catch
block, check `e.code` and whitelist only network/hang codes:

```js
const isNetworkOrHang = e && (
  e.code === 'auth/network-request-failed' ||
  e.code === 'auth/internal-error' ||
  e.code === 'auth/timeout'
);
if (isNetworkOrHang && !authDidInitialize && document.visibilityState === 'visible') {
  scheduleAuthRecoveryIfStranded();
}
```

## Context

PR [#7321](https://github.com/jleechanorg/worldarchitect.ai/pull/7321) — mobile
auth hang fallback (28-commit, Skeptic rounds 1–19) — was reviewed post-merge
and the catch block was identified as the only root-cause-first violation in the
incremental delta `d07a2508f6..HEAD`. All other changes (visibility-recovery timer
guards, `authDidInitialize` flag design) were sound.

Fixed in PR [#7349](https://github.com/jleechanorg/worldarchitect.ai/pull/7349),
commit `2fdad5778c`, branch `fix/auth-recovery-rcf-rename`.

## Structural note — handler naming

When a recovery handler is reused across multiple triggers (tab-focus
`visibilitychange`, network `online` event, sign-in exception), update its name
to reflect the expanded responsibility. `handleVisibilityRecovery` became
misleading when it also handled `online` and sign-in-failure paths.

Renamed: `handleVisibilityRecovery` → `scheduleAuthRecoveryIfStranded`
Renamed: `visibilityRecoveryTimer` → `authRecoveryTimer`

**Heuristic:** if a comment on an event-listener teardown line has to be edited
to say "and also removes the X listener" (which wasn't in the original), that's a
sign the function name lags the responsibility.

## Reusable pattern

```
if (catch block calls recovery handler) {
  → check: does the handler ultimately schedule window.location.reload()?
  → if yes: gate on e.code whitelist (network/hang only)
  → never call on user-cancellation codes (popup-closed, cancelled, blocked)
}
```

## References

- PR #7321 merged: original auth fallback
- PR [#7349](https://github.com/jleechanorg/worldarchitect.ai/pull/7349): fix commit `2fdad5778c`
- File: `mvp_site/frontend_v1/auth.js` catch block ~line 245
- Related: [[root-cause-first]], [[auth-recovery-handler-naming]]

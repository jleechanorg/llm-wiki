# Auth catch-block recovery must gate on e.code (2026-06-07)

**Source**: Claude auto-memory — feedback
**Date**: 2026-06-07
**PR**: [#7349](https://github.com/jleechanorg/worldarchitect.ai/pull/7349)
**Commit**: `2fdad5778c`

## Summary

`signInWithPopup` catch blocks must not call reload-recovery handlers
unconditionally. Gate on `e.code` — only `auth/network-request-failed`,
`auth/internal-error`, `auth/timeout` warrant a recovery schedule.
User-cancellation codes (`popup-closed-by-user`, `cancelled-popup-request`,
`popup-blocked`) must fall through to `console.error` only.

## Pattern

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

## Naming rule

When a recovery handler is wired to additional triggers, rename it to reflect
all responsibilities. `handleVisibilityRecovery` → `scheduleAuthRecoveryIfStranded`
because the handler also serves `window 'online'` and sign-in exception paths.

**Signal**: if a teardown comment must be edited to say "also removes X listener",
the function name lags its responsibility.

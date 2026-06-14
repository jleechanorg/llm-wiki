---
title: "Auth catch recovery must gate on e.code (network/hang only)"
type: source
tags: [auth, catch-block, recovery-gate, ecode, popup-cancelled, worldarchitect-ai]
date: 2026-06-07
source_file: raw/feedback_2026-06-07_auth_catch_recovery_ecode_gate.md
---

## Summary
In a signInWithPopup catch block, never call a recovery handler (especially one that may schedule window.location.reload()) unconditionally. Gate it on the Firebase Auth error code — only fire for genuine network/hang errors (auth/network-request-failed, auth/internal-error, auth/timeout), not for user-cancellation codes (auth/popup-closed-by-user, auth/cancelled-popup-request, auth/popup-blocked). PR #7321 (mobile auth hang fallback) reviewed post-merge; catch block identified as only root-cause-first violation. Fixed in PR #7349 (commit 2fdad5778c, branch fix/auth-recovery-rcf-rename). Handler renamed handleVisibilityRecovery → scheduleAuthRecoveryIfStranded.

## Key Claims
- Rule: in signInWithPopup catch, gate reload-recovery on e.code whitelist (network/hang only) — never call on user-cancellation codes (popup-closed, cancelled, blocked)
- PR #7321 catch block was the only root-cause-first violation in the incremental delta d07a2508f6..HEAD
- Fixed in PR #7349, commit 2fdad5778c, branch fix/auth-recovery-rcf-rename
- Handler renamed: handleVisibilityRecovery → scheduleAuthRecoveryIfStranded; visibilityRecoveryTimer → authRecoveryTimer (when a recovery handler is reused across multiple triggers, update its name)

## Connections
- [[project_2026-06-08_google_sso_login_page_investigation]]
- [[RootCauseFirst]]
- [[AuthRecoveryGate]]

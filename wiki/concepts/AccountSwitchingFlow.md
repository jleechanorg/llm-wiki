---
title: "Account Switching Flow"
type: concept
tags: [auth, oauth, account-switching, firebase]
sources: [waitlist-gating-account-switching-flow]
last_updated: 2026-06-20
---

## Definition

The Account Switching Flow allows waitlist-denied users to sign in with a different Google account without being auto-logged back into the previously denied account.


## Flow

1. **Trigger:** User is waitlist-denied and clicks "Use a different account"
2. **Sign-out:** Firebase sign-out executes
3. **Flag Set:** `worldai_force_google_account_select = "true"` stored in `sessionStorage`
4. **Return to Splash:** User returned to signed-out splash screen
5. **Next Sign-in:** Flag is read; if armed, `provider.setCustomParameters({ prompt: 'select_account' })` is called
6. **Google Account Chooser:** Popup forces user to select account manually
7. **Flag Cleared:** Flag consumed and cleared from `sessionStorage`

## Technical Details

- **Storage:** `sessionStorage` (one-shot, cleared on use)
- **Google Auth Parameter:** `prompt: 'select_account'` forces the account chooser
- **Event:** No custom event; uses Firebase's native `signInWithPopup` flow

## Related Concepts
- [[WaitlistGatingMode]] — access control
- [[OAuthGoogleFlow]] — Google OAuth integration
- [[SequenceGuardedCallbacks]] — race condition prevention

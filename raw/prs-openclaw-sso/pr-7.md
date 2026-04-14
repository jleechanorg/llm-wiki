# PR #7: [antig] feat(client-py): Implement server-side PKCE flow

**Repo:** jleechanorg/openclaw_sso
**Merged:** 2026-04-05
**Author:** jleechan2015
**Stats:** +305/-25 in 7 files

## Summary
(none)

## Raw Body
Implements robust Python server-side PKCE flow utilities

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Adds new PKCE generation/validation and token-exchange behavior in the Python SSO client, which impacts authentication flows and error handling. Risk is moderated by new unit tests and changes being additive/contained to the Python client and examples.
> 
> **Overview**
> Enables a **server-managed PKCE authorization-code flow** in the Python SSO client by adding PKCE verifier/challenge helpers and a new `OpenClawAuthClient.get_authorize_url()` that returns both the redirect URL and verifier to persist in a backend session.
> 
> Updates `OpenClawAuthClient.exchange_code()` to use a timed request and raise a clearer HTTP error on non-2xx responses, and narrows the package surface in `__init__.py` to only export `OpenClawAuthClient`.
> 
> Adds a Flask demo app (`examples/demo-py`) showing session-backed login/callback handling and a token-authenticated inference call, plus new unit tests covering PKCE generation/validation, authorize URL construction, and token exchange success/failure. Also ignores Python `__pycache__/`.
> 
> <sup>Reviewed by [Cursor Bugbot](https://cursor.com/bugbot) for commit 3f3b3cbdc8a2e375b36c29db8bbb71ac5b5d60a7. Bugbot is set up for automated code reviews on this repo. Configure [here](https://www.cursor.com/dashboard/bugbot).</sup>
<!-- /CURSOR_SUMMARY -->

# PR #9: fix: restore oauth verifier regression coverage

**Repo:** jleechanorg/openclaw_sso
**Merged:** 2026-04-09
**Author:** jleechan2015
**Stats:** +68/-1 in 3 files

## Summary
(none)

## Raw Body
### Background
The broader OAuth boundary hardening for `packages/gateway/src/routes/oauth.ts` is already on `main`. After review, PR #9 still carries the follow-up fix that restores the invalid-verifier regression coverage after the token-session binding guard was added, closes the roadmap wording nit, and now includes the PR-specific design artifact that the skeptic/design-alignment workflow expects.

### Goals
- Make the invalid-verifier regression test exercise the PKCE verifier path again.
- Close the remaining review nit in the roadmap note.
- Keep the PR description aligned with the live diff against `main`.
- Provide the PR-specific design doc required for skeptic/design-alignment verification.

### Tenets
- Evidence must match the current diff, not stale branch history.
- Keep the follow-up scoped to the remaining review and process blockers.
- Preserve the shipped OAuth hardening by strengthening the regression test around it.

### High-level description of changes
This PR now contains the follow-up review fix on top of `main`: the invalid-verifier OAuth test fixture stores matching `client_id` and `redirect_uri`, so the request passes the session-binding guard and fails for the intended PKCE verifier reason. It also updates the roadmap wording from `fail-closes` to `fails closed`, and adds `docs/design/pr-designs/pr-9.md` so skeptic/design-alignment checks have a concrete artifact that matches the live diff.

### Testing
- `source ~/.nvm/nvm.sh && nvm use 22 >/dev/null && npm test -- --selectProjects gateway --runInBand`
  Result: PASS, 12 suites / 66 tests passed / 3.595 s.
  Run timestamp: 2026-04-09T00:33Z.
- `source ~/.nvm/nvm.sh && nvm use 22 >/dev/null && npm test -- --selectProjects gateway --coverage --runInBand`
  Result: PASS, 12 suites / 66 tests passed / 5.237 s.
  Coverage: 80.9% statements / 67.37% branches / 79.1% functions / 84.49% lines.
  Run timestamp: 2026-04-09T00:53Z.
- Full command outputs from this session were captured locally at 

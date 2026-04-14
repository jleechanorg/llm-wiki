# Harden preview MCP endpoint access after PR smoke hardening work

**Type:** hardening
**Priority:** 1
**Status:** in_progress
**Labels:** security, ci, gcp, mcp, preview

## GOAL

Prevent unintended external access to PR preview MCP/preview servers while preserving reliable CI smoke testing.

## MODIFICATION

- Update preview deployment in `.github/workflows/pr-preview.yml` to remove public
  unauthenticated access on preview Cloud Run services (remove or gate
  `--allow-unauthenticated`).
- Add an explicit preview access control path for smoke tests, for example:
  - set a CI-only allowlist via secret header or API token, or
  - enforce authenticated IAM Invocation with a dedicated service account and
    allow only the smoke-test workflow identity.
- Add regression checks in `.github/workflows/mcp-smoke-tests.yml` that verify the
  smoke client can only proceed with an explicit, non-empty preview auth credential.
- Document the new gating model in `.github/workflows/pr-preview.yml` and smoke-test
  comments so future maintainers do not regress to unauthenticated previews.
- Implemented in this PR: smoke/CI paths now fail fast if `SMOKE_TOKEN` is missing,
  and preview `/mcp` access no longer honors `X-Test-Bypass-Auth` without a token.
- Current state: `SMOKE_TOKEN` is injected into preview services via Cloud Run
  env var (`secrets.SMOKE_TOKEN`) to avoid Secret Manager runtime permission failures
  during deploy with the current runtime service-account IAM state.
- Remaining follow-up: switch back to `--set-secrets` for `SMOKE_TOKEN` once
  runtime service-account access to `secretmanager.secretAccessor` is granted, then
  remove plaintext token injection.
- Remaining follow-up: tighten preview Cloud Run network/IAM posture (evaluate removing
  `--allow-unauthenticated` or adding invocation-bound IAM constraints).

## NECESSITY

Current preview deployments set `--allow-unauthenticated`, so preview endpoints can be
reached by non-reviewers/unknown traffic. `SMOKE_TOKEN` access is still a follow-up
hardening step because token delivery is currently plaintext in Cloud Run env vars while
Secret Manager-backed injection is blocked by runtime IAM.

## INTEGRATION PROOF

- CI/preview workflow must show no public preview endpoints in logs/Cloud Run
  settings; requests should require an explicit preview credential or IAM invocation.
- `mcp-smoke-tests.yml` run path for preview comments/tests should fail fast when the
  preview auth credential is missing.
- Manual / smoke-triggered access should continue to work only for authorized CI workflow
  and approved test runners.

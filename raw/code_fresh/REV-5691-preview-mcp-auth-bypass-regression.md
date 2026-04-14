# REV-5691: Preview MCP auth bypass allows bypass without smoke token

**Type:** bug  
**Priority:** 1  
**Status:** open  
**Related PR:** #5691  

## Summary

`/mcp` can still be reached in preview by sending only `X-Test-Bypass-Auth` despite the new smoke-token gate logic.

## Root Cause

- `mvp_site/main.py:1069` introduced smoke-token auth for `/mcp`.
- The logic still falls through to the legacy `X-Test-Bypass-Auth` path later in `check_token`.
- Preview is deployed with `PRODUCTION_MODE=true` and `TESTING_AUTH_BYPASS=true` (`deploy.sh:359`), so bypass is active.
- `main.py:1099` contains a comment saying X-Test-Bypass-Auth alone is no longer accepted, but no hard requirement is enforced.

## Impact

- Unauthorized callers can bypass preview MCP auth and interact via the deprecated bypass header.
- This weakens the intended production-preview security hardening for real deployed preview environments.

## Evidence

- `mvp_site/main.py:1099` comment claims one policy.
- Actual behavior in `mvp_site/main.py:1102` still permits header-only bypass when `TESTING_AUTH_BYPASS=true`.

## Acceptance Criteria

- In preview with `PRODUCTION_MODE=true` and `TESTING_AUTH_BYPASS=true`, `/mcp` requires valid `X-MCP-Smoke-Token` regardless of `X-Test-Bypass-Auth`.
- `X-Test-Bypass-Auth` should only be accepted in non-production or explicit safe test flows.
- Add/adjust tests around `/mcp` auth order to verify token-gating precedence.

## Proposed Fix

1. Add explicit preview + production guard before the generic `X-Test-Bypass-Auth` block.
2. Return a clear 401/403 response for bypass-header-only requests that do not include a valid smoke token.

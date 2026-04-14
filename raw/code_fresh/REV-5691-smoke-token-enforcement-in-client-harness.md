# REV-5691: Smoke harness still bypasses token gate for local preview smoke runs

**Type:** bug  
**Priority:** 2  
**Status:** in_progress  
**Related PR:** #5691  

## Summary

`scripts/mcp_smoke_test.sh` forces `TESTING_AUTH_BYPASS=true` whenever `MCP_SERVER_URL` is set, and only requires `SMOKE_TOKEN` in GitHub Actions.

## Root Cause

- `scripts/mcp_smoke_test.sh:171` starts local MCP via Gunicorn when running local checks.
- `scripts/mcp_smoke_test.sh:157` sets `MCP_SERVER_URL` to switch to remote server mode.
- `scripts/mcp_smoke_test.sh:63` only exits for missing token in GH Actions.
- `scripts/mcp_smoke_test.sh` still sets `TESTING_AUTH_BYPASS=true` for remote runs, allowing header-based bypass paths to succeed without smoke-token in non-CI contexts.

## Impact

- Local/manual smoke invocations can pass against preview without `SMOKE_TOKEN`, masking deployment auth-policy gaps.
- Makes it harder to validate the intended production-preview behavior consistently across environments.

## Acceptance Criteria

- Remote (`MCP_SERVER_URL` set) smoke test flow should consistently enforce `SMOKE_TOKEN` before launch in all environments, not only GitHub Actions.
- Confirm `X-MCP-Smoke-Token` is required for `/mcp` in preview when running the canonical smoke test command.

## Status Update

- Local repro confirmed:
  - `scripts/mcp_smoke_test.sh` with `MCP_SERVER_URL` pointing at `https://...a.run.app` and no `SMOKE_TOKEN` previously continued through auth bypass settings for local/manual runs.
  - `scripts/mcp-smoke-tests.mjs` already failed fast with `SMOKE_TOKEN is required for remote /mcp smoke tests.`.
- Fix applied in `scripts/mcp_smoke_test.sh`:
  - Remote HTTP(S) `MCP_SERVER_URL` now requires `SMOKE_TOKEN` in all environments.
  - Loopback URLs keep local auth-bypass behavior.
- Remote runs now force `TESTING_AUTH_BYPASS=false` and `ALLOW_TEST_AUTH_BYPASS=false`, preventing unintended preview bypass.

## Proposed Fix

1. Require `SMOKE_TOKEN` whenever `MCP_SERVER_URL` points to `https://` or `http://` endpoint, outside of tests-only local mode.
2. Keep local-only dev bypass behavior unchanged for local server runs.

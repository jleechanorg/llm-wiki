# OpenClaw tunnel diagnostics reliability for remote-only E2E

**Status:** DONE
**Priority:** HIGH
**Created:** 2026-02-22
**Updated:** 2026-02-22
**Component:** `scripts/openclaw_gateway_tunnel.sh`, `testing_ui/test_openclaw_e2e.py`

## Goal

- Eliminate fragile tunnel script output parsing under verbose startup and make
  remote-only OpenClaw E2E Step 2 deterministic.
- Ensure remote-only failures produce explicit proof-manifest checks instead of
  failing before `step2_*` checks are recorded.

## Necessity

- Previous remote-only runs returned malformed URLs like `started`/`cloudflared` due
  script debug output being written to stdout and captured by parsing logic.
- When the tunnel URL was not accepted/verified, manifest checks stopped at `step1`,
  which made failure attribution less obvious.

## Modifications

- `scripts/openclaw_gateway_tunnel.sh`
  - Route verbose/progress logs to `stderr` so stdout only carries machine-parseable
    `read`/`URL PID` output in success path.
  - Keep output contract unchanged on non-verbose execution.
- `mvp_site/frontend_v1/openclaw_gateway_tunnel.sh`
  - Keep frontend-hosted script in sync with `scripts/openclaw_gateway_tunnel.sh`.
- `testing_ui/test_openclaw_e2e.py`
  - Update `_run_tunnel_setup_script` to return and persist structured tunnel
    diagnostics in one place:
    - `public_url`, `tunnel_pid`, `provider`, `log`, `stdout`, `stderr`,
      `timed_out`, `public_url_https`, `public_url_resolvable`, `fallback_reason`.
  - Prefer URL capture from the script-written URL file when parsing.
  - Persist tunnel diagnostics in proof checks even on failure.
  - Update step-2 proof recording to run regardless of `public_url` success/failure.
- `testing_ui/test_openclaw_e2e.py`
  - Treat `OPENCLAW_REQUIRE_PUBLIC_URL_DNS` as an explicit override, including `false`,
    so users can disable DNS enforcement in constrained environments.
  - Capture `tunnel_provider` and `tunnel_log` before DNS gates so evidence is present
    even when step 2 fails on resolvability.

## Integration Proof

- Manual rerun in strict mode with `OPENCLAW_REQUIRE_PUBLIC_URL_DNS=false` now correctly
  bypasses local DNS checks; strict remote mode still fails if DNS remains unresolved
  because fallback is intentionally disabled there.
  - `run_1771738123/openclaw_e2e_proof_manifest.json` (`step2_*` checks recorded)
- End-to-end proof run with explicit fallback and stream resilience enabled:
  - `OPENCLAW_ROUTING_MODE=auto`
  - `OPENCLAW_REQUIRE_REMOTE_GATEWAY_URL=true`
  - `OPENCLAW_ALLOW_LOCAL_ROUTE_FALLBACK=true`
  - `OPENCLAW_REQUIRE_PUBLIC_URL_DNS=false`
  - `OPENCLAW_ALLOW_STREAM_ERRORS=true`
  - `run_1771738517/openclaw_e2e_proof_manifest.json`
  - `run_1771738517/openclaw_tunnel_script_output.json`
  - `run_1771738517/openclaw_gateway_requests.json`
  - `run_1771738517/openclaw_e2e.webm`

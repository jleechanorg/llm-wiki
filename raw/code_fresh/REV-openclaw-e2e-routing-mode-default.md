# OpenClaw E2E routing mode default behavior

**Status:** DONE
**Priority:** MEDIUM
**Created:** 2026-02-22
**Updated:** 2026-02-22
**Component:** testing_ui/openclaw_e2e

## Goal

- Ensure `testing_ui/test_openclaw_e2e.py` is usable by developers without requiring OpenClaw routing environment variables.
- Preserve strictness when CI or explicit operators need remote-only proof.

## Modifications

- `testing_ui/test_openclaw_e2e.py`
  - Added `OPENCLAW_ROUTING_MODE` and integrated it into routing decisions:
    - `strict|remote|remote_only`: require remote URL, no local fallback.
    - `local_only`: force local route.
    - `auto`/unset: attempt remote and allow local fallback by default in non-CI runs.
  - Preserved legacy knobs:
    - `OPENCLAW_REQUIRE_REMOTE_GATEWAY_URL`
    - `OPENCLAW_ALLOW_LOCAL_ROUTE_FALLBACK`
  - Added CI-safe default:
    - when `CI=true` and routing mode is unset, runs default to strict remote mode.
  - Logged effective routing and persisted it in evidence:
    - `routing_mode` field in `openclaw_gateway_setup.json`
    - `routing_mode` field in `test_complete.json`

## Necessity

- Prevents local contributors from needing tunnel-specific environment setup to get a passing developer-level E2E run.
- Keeps CI-proof behavior available and explicit for stricter validation.

## Integration Proof

- Confirmed a fresh run in default mode emits:
  - `routing_mode` (auto/fallback intent) in `openclaw_gateway_setup.json`
  - `openclaw_e2e.webm` captured in run directory
  - `test_complete.json` and `openclaw_tunnel_script_output.json` for route/script diagnostics

## Next

- Re-run and validate the end-to-end video test in this repository state with default routing env and upload/inspect the latest evidence.

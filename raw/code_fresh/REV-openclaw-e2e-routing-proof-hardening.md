# OpenClaw E2E routing proof hardening (finalize manifest + route checks)

**Status:** DONE
**Priority:** HIGH
**Created:** 2026-02-22
**Updated:** 2026-02-22
**Component:** `testing_ui/test_openclaw_e2e.py`, `roadmap/openclaw-e2e-routing-proof-design.md`

## Goal

- Repair malformed Step 2 routing branch in the OpenClaw lifecycle E2E test.
- Remove inverted/ambiguous Step 8 assumptions around tap vs gateway traffic.
- Ensure proof manifest is always written even on early failure.
- Align the test with shared base-class OpenClaw setup-script capabilities.

## Modifications

- `testing_ui/test_openclaw_e2e.py`
  - Reworked Step 2 routing decision:
    - clear local/remote decision path with explicit branch ordering
    - explicit hard-fail when remote route is required but public URL cannot be verified and fallback is disabled
    - explicit fallback path with URL-clearing for local route modes
    - unverified remote fallback branch retained when configured via explicit flags
    - decision details now recorded in proof checks/evidence.
  - Reworked Step 8:
    - unified tap/gateway traffic verification into deterministic checks
    - added always-recorded `step8_route_traffic_verified`
    - removed remote-vs-local inversion that incorrectly treated tap traffic as a failure.
  - Ensured `execute()` finalizes proof manifest in `finally` using:
    - `route_mode`
    - `success`
    - captured video path.
  - Removed redundant `_download_setup_script` wrapper and reused
    `BrowserTestBase.download_openclaw_setup_script` directly.
  - Added proof check requirements entries for:
    - `step8_gateway_route_expected_local`
    - `step8_tap_capture_local`.

## Necessity

- Without this fix, the current script had malformed indentation in Step 2 and was not reliably enforcing routing intent.
- Step 8 could fail valid proxy/local routes due to incorrect assumptions about where traffic should be visible.
- Missing manifest finalization made evidence generation non-deterministic.

## Integration proof

- `testing_ui/test_openclaw_e2e.py` compiles successfully with `python -m py_compile`.
- Next execution should verify fresh artifacts include `openclaw_e2e_proof_manifest.json` in each run directory and
  `step8_route_traffic_verified` check result in the manifest.

## Rollout

- Run the E2E test with your normal local script-tunnel workflow and collect:
  - `openclaw_e2e_proof_manifest.json`
  - `openclaw_gateway_setup.json`
  - `openclaw_tunnel_script_output.json`
  - `openclaw_gateway_requests.json`
  - `openclaw_e2e.webm`

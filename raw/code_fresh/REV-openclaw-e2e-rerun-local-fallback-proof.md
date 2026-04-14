# OpenClaw settings+script e2e rerun proof (run_1771733433)

**Status:** DONE
**Priority:** HIGH
**Created:** 2026-02-22
**Updated:** 2026-02-22
**Component:** `testing_ui/test_openclaw_e2e.py`

## Goal
- Re-run OpenClaw end-to-end test with settings-script download and routing path capture, and validate the evidence chain for default routing behavior.

## Modification
- Executed:
  - `OPENCLAW_ALLOW_STREAM_ERRORS=true OPENCLAW_STREAM_TIMEOUT_S=120 OPENCLAW_TUNNEL_SCRIPT_TIMEOUT_SECONDS=120 OPENCLAW_USE_TAP_PROXY=true ./vpython testing_ui/test_openclaw_e2e.py`
- Reviewed resulting evidence in `/tmp/worldarchitectai/feat_openclaw-gateway-url-setting/openclaw_e2e/run_1771733433/`.
- No production code changes were made in this rerun cycle.

## Necessity
- Needed a fresh run with updated evidence + video to verify whether routing and stream behavior were truly using the downloaded OpenClaw setup script and OpenClaw tap path.

## Integration Proof
- Run completed with exit code `0` and recorded artifacts under:
  - `/tmp/worldarchitectai/feat_openclaw-gateway-url-setting/openclaw_e2e/run_1771733433/openclaw_e2e.webm`
  - `/tmp/worldarchitectai/feat_openclaw-gateway-url-setting/openclaw_e2e/run_1771733433/openclaw_tunnel_script_output.json`
  - `/tmp/worldarchitectai/feat_openclaw-gateway-url-setting/openclaw_e2e/run_1771733433/openclaw_gateway_setup.json`
  - `/tmp/worldarchitectai/feat_openclaw-gateway-url-setting/openclaw_e2e/run_1771733433/openclaw_gateway_requests.json`
  - `/tmp/worldarchitectai/feat_openclaw-gateway-url-setting/openclaw_e2e/run_1771733433/test_complete.json`
- Step-level outcome evidence:
  - Settings configured and script downloaded (`openclaw_setup_script_downloaded.png`).
  - Script executed (`openclaw_tunnel_script_output.json`) with `public_url=...trycloudflare.com` and tunnel PID `27204`.
  - Public URL was not resolvable in this environment, so routing remained local (`gateway_url_mode: "local_route"`).
  - Campaign creation and continuation passed with explicit stream-error allowance and warnings.
  - Traffic was observed via tap (`tap_requests`: 3).
- Recorded video duration: `147.16s`, proving UI evidence from settings navigation through continuation and final assertions.

## Latest rerun (run_1771734314)

- Executed:
  - `OPENCLAW_ROUTING_MODE=local_only OPENCLAW_USE_TAP_PROXY=true OPENCLAW_STREAM_TIMEOUT_S=90 OPENCLAW_ALLOW_STREAM_ERRORS=true OPENCLAW_ALLOW_MISSING_STREAM_EVENTS=true OPENCLAW_TUNNEL_SCRIPT_TIMEOUT_SECONDS=120 ./vpython testing_ui/test_openclaw_e2e.py`
- Result: exit code `0`.
- Evidence directory:
  - `/tmp/worldarchitectai/feat_openclaw-gateway-url-setting/openclaw_e2e/run_1771734314/`
- Evidence artifacts:
  - `openclaw_e2e_proof_manifest.json` (`proof_passed=true`, `run_success=true`, `meta.video_path` set)
  - `openclaw_gateway_setup.json` (`gateway_url_mode="local_route"`, `public_url` captured, `openclaw_route_mode="tap"`)
  - `openclaw_tunnel_script_output.json` (`public_url=...trycloudflare.com`, `public_url_resolvable=false`, `tunnel_provider="cloudflared"`, `tunnel_pid=22288`)
  - `openclaw_gateway_requests.json` (`tap_requests=3`, `gateway_log_requests=0`)
  - `openclaw_e2e.webm` (recorded lifecycle video)

## Notes from this rerun
- Script-run path is confirmed (`openclaw_setup_script_downloaded.png`, tunnel PID logged).
- OpenClaw still used local route after URL-resolve fallback, with script execution required and verified.
- Stream errors were observed in step 4 and tolerated via `OPENCLAW_ALLOW_STREAM_ERRORS=true`; campaign and routing checks still passed.

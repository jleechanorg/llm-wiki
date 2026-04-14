# BD: PR 5879 rerun stability loop

## Scope
- Stabilize remote-preview reruns for:
  - `testing_mcp/test_openclaw_gateway_url_preview.py`
  - `testing_ui/test_openclaw_gcp_settings.py`
- Keep evidence review skeptical and avoid overstated pass claims.

## Loop plan
1. Run both tests against preview URL.
2. Parse logs/evidence for concrete failure signatures.
3. Apply minimal targeted fixes.
4. Re-run both tests.
5. Validate evidence bundle consistency (logs vs JSON artifacts).

## Current status
- [x] Add health probe retry/backoff in testing_mcp preview test.
- [x] Add preview proof-call retry/diagnostics in testing_ui settings test.
- [x] Execute rerun loop and archive logs under `/tmp/`.
- [x] Summarize skeptical evidence verdict.

## Latest loop run
- Loop dir: `/tmp/pr5879_stabilize_20260311_123939`
- Iterations: 1
- Result:
  - `testing_mcp_exit=0`
  - `testing_ui_exit=0`
- Skeptical note:
  - `testing_mcp` still marks `e2e_gateway_routing` as `passed=true, skipped=true`.
  - Treat this as **partial proof** (preview surface checks passed; full remote->local routing not executed in this run).

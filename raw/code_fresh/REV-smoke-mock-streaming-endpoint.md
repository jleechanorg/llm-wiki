# Bead: Run smoke tests against HTTP app for streaming contract coverage

## GOAL
Restore streaming smoke coverage in `workflow` mock-mode CI where `/interaction/stream` contracts are currently failing with missing/malformed done payload.

## PROBLEM
`testing_mcp/test_smoke.py` validates streaming SSE contracts via
`testing_mcp/lib/campaign_utils.py`, which reads from
`/api/campaigns/<campaign_id>/interaction/stream`.

`testing_mcp/streaming` contract scenarios pass when called against the HTTP app,
but mock smoke runs were starting `mvp_site/mcp_api.py`, which only serves MCP endpoints
(`POST /mcp`) and does not expose the `/api/...` routes.

## MODIFICATION
- Updated `scripts/mcp_smoke_test.sh` `start_server()` to launch `mvp_site.main:app`
  through `gunicorn` instead of `mvp_site/mcp_api.py --http-only`.
- Kept the same bind/host/port and timeout settings while using the SSE-safe
  worker profile:
  - `gthread`
  - `workers=1`
  - `threads=2`
  - `timeout=600`

This ensures mock smoke executes both MCP and HTTP/API scenarios (`/mcp` and
`/api/campaigns/<id>/interaction/stream`) in one server process.

## NECESSITY
Without a server exposing `/api/campaigns/.../interaction/stream`, the stream
collector receives non-stream/malformed payloads and reports
`missing/malformed done payload` for character/think/god contracts.

## INTEGRATION PROOF
- Streaming smoke assertions in `testing_mcp/test_smoke.py` now target an endpoint
  that exists in the same process as `/mcp`, eliminating transport-format false
  negatives.
- No direct production runtime behavior changed; only CI smoke runner wiring was
  corrected.

## STATUS
fixed

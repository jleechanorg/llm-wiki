# REV: Smoke streaming test user_id mismatch causes 404

## Status: done
## Priority: high
## Type: bug

## Summary

Streaming chunk timing contract tests (SCENARIO 7) fail with 404 "Campaign not found"
on preview deployments. Root cause: `collect_route_stream_events` applied `extra_headers`
(from MCP client defaults) AFTER setting the explicit `user_id` parameter, allowing
the client-level `X-Test-User-ID` header to silently override it.

MCP tool calls created the campaign under `user_id=smoke-user`, but the streaming
request sent `user_id=test-smoke-{random}` from `_build_test_identity_headers`.
Firestore lookup at `users/test-smoke-{random}/campaigns/{id}` returned 404.

## Fix

Reversed header merge order in `testing_mcp/lib/campaign_utils.py`: apply
`extra_headers` first as a base layer, then overlay explicit parameters
(`X-Test-User-ID`, `X-Test-Bypass-Auth`, `X-Test-User-Email`) so the caller's
identity always wins. Applied to both `collect_route_stream_events` and
`post_interaction_stream`.

## Evidence

Server-side GCP logs confirmed:
- `SMOKE_TOKEN auth bypass activated for user_id=test-smoke-1772784289 path=/api/campaigns/E62TuTyWjFESjXN7Bh4a/interaction/stream`
- Campaign was created by `user=smoke-user`
- All 4 streaming contracts returned HTTP 404

## Files Changed

- `testing_mcp/lib/campaign_utils.py` (both stream functions)

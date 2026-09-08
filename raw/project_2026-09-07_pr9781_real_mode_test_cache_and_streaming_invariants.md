---
name: project_2026-09-07_pr9781_real_mode_test_cache_and_streaming_invariants
description: "Real-mode Gemini SDK stress testing and Playwright streaming harness invariants: WORLDAI_TEST_CACHE=off, scenario user_id mapping, trace synthesis, and CSP bypass"
type: project
bead: rev-5alwm
---

## Context
During verification of PR #9780 / #9781 (Ironclad Narrative Evidence Contract on bead `rev-5alwm`), four critical runtime failure modes in the `testing_mcp` and `testing_ui` integration harnesses were diagnosed and permanently resolved.

## Technical Details & Invariants

1. **Server Test Cache Isolation (`WORLDAI_TEST_CACHE="off"`)**:
   - In `testing_mcp.lib.server_utils.start_local_mcp_server`, `env.setdefault("WORLDAI_TEST_CACHE", "read_write")` activates the disk-backed server cache (`server_cache.py`).
   - For real Gemini SDK provider tests verifying prompt tokens, circuit breakers, or code execution, repeated runs of identical prompts hit `server_cache.py`, emitting `finish="cache_replay"`, skipping the Gemini HTTP call, omitting `gemini_http_request_responses_*.jsonl`, and zeroing BigQuery prompt tokens.
   - **Rule**: All real-mode Gemini provider test classes must override `get_server_env_overrides()` and explicitly include `"WORLDAI_TEST_CACHE": "off"` alongside `"AGY_PROVIDER_ENABLED": "false"`.

2. **Snapshot Identity Mapping (`"user_id": dest_uid`)**:
   - Post-test campaign state snapshotting in `base_test.py` (`_capture_campaign_snapshot`) builds `candidate_user_ids` from `r.get("user_id")` in scenario result dicts.
   - When tests twin-copy to dedicated secondary test accounts (e.g., `0wf6sCREyLcgynidU5LjyZEfm7D2`), omitting `"user_id": dest_uid` causes the snapshot client to default to `self.ctx.user_id` (the runner's bootstrap user), producing a false 404 "Campaign not found" error during post-processing.
   - **Rule**: Scenario results must always return `"user_id": dest_uid` when operating on non-bootstrap campaign owners.

3. **Streaming Trace Synthesis & `EVIDENCE_SIGNATURE_GUARD`**:
   - `base_test.py` enforces `EVIDENCE_SIGNATURE_GUARD`, which requires `processing_metadata.streaming_response_signature` on response records in `llm_request_responses.jsonl` to have `signed == True`, `algorithm == "hmac-sha256"`, `schema_version == "streaming-response-v1"`, and a 64-char hex digest.
   - Browser/UI turns stream over `/api/campaigns/{id}/interaction/stream`, which writes SSE done events with this signature to `http_request_responses_*.jsonl`, but skips `_log_raw_llm_data`.
   - **Rule**: Custom and UI streaming harnesses must synthesize `llm_request_responses.jsonl` from Gemini transport traces and extract the HMAC signature from the SSE done event into `processing_metadata`.

4. **Headless Playwright CSP Restrictions**:
   - The web app Content Security Policy forbids `'unsafe-eval'`. Calling `page.wait_for_function("...")` raises `EvalError`.
   - **Rule**: Playwright browser contexts must pass `bypass_csp=True` and poll native Playwright properties (`locator.is_enabled()`, `locator.is_visible()`) rather than string-eval scripts.

5. **Video Transcoding Cleanliness**:
   - Chromium video recording can produce 0-byte `.webm` files during quick navigation. Always filter for `f.stat().st_size > 0` and select the latest recording by `st_mtime` before transcoding to `browser_interaction.mp4`.

## References
- PR #9780, PR #9781
- Bead: `rev-5alwm`
- Files: `testing_mcp/CLAUDE.md`, `testing_ui/CLAUDE.md`, `testing_mcp/streaming/test_circuit_breaker_large_campaign_repro_real.py`
- Commits: `18a07a5f500`, `fa24fba13b4`, `dcff189a089`

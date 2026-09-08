---
title: "PR #9780 / #9781 Real-Mode Test Cache and Streaming Invariants"
type: source
tags: [testing, mcp, playwright, streaming, gemini, caching]
date: 2026-09-07
source_file: raw/project_2026-09-07_pr9781_real_mode_test_cache_and_streaming_invariants.md
---

## Summary
During verification of PR #9780 and PR #9781 (Ironclad Narrative Evidence Contract on bead `rev-5alwm`), four critical runtime failure modes in the `testing_mcp` and `testing_ui` integration harnesses were diagnosed and permanently resolved. Real Gemini SDK provider tests require explicit cache bypass (`WORLDAI_TEST_CACHE="off"`), scenario results must return `"user_id": dest_uid` for twin campaigns to prevent snapshot 404s, streaming turns require synthesizing `llm_request_responses.jsonl` with HMAC signatures from SSE done events, and Playwright browser contexts require CSP bypass and non-eval locator polling.

## Key Claims
- Real Gemini provider tests must override `get_server_env_overrides()` with `WORLDAI_TEST_CACHE="off"` to prevent `server_cache.py` replay from zeroing BigQuery prompt tokens and bypassing model execution.
- MCPTestBase scenario results must explicitly return `"user_id": dest_uid` when operating on non-bootstrap twin campaigns, otherwise snapshotting defaults to the runner user ID and 404s.
- `EVIDENCE_SIGNATURE_GUARD` requires response records in `llm_request_responses.jsonl` to have valid HMAC-SHA256 signatures; streaming endpoints emit this in SSE done events, requiring harness synthesis.
- Web app Content Security Policy forbids `"unsafe-eval"`; Playwright contexts must pass `bypass_csp=True` and poll native locators rather than string scripts.

## Key Quotes
> "All real-mode Gemini provider test classes must override get_server_env_overrides() and explicitly include WORLDAI_TEST_CACHE: off alongside AGY_PROVIDER_ENABLED: false." — Technical Details & Invariants
> "Playwright browser contexts must pass bypass_csp=True and poll native Playwright properties (locator.is_enabled(), locator.is_visible()) rather than string-eval scripts." — Technical Details & Invariants

## Connections
- [[WorldArchitectAI]] — core game platform being tested
- [[Gemini]] — LLM provider requiring cache bypass and forensic trace tracking
- [[Playwright]] — browser automation engine subject to CSP restrictions
- [[HarnessEngineering]] — test harness reliability and evidence capture standards
- [[EvidenceStandards]] — requirement for authentic provider telemetry and cryptographic signature guards

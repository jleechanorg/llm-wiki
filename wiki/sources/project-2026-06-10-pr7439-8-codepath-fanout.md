---
title: "Project 2026 06 10 Pr7439 8 Codepath Fanout"
type: source
tags: [memory, ao-worker, codex-worker, 2026-06]
date: 2026-06-10
source_file: .claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/project_2026-06-10_pr7439_8_codepath_fanout.md
---

## Summary

PR #7439 (worktree_bq_loggin) shipped BQ-forensic logging for all LLM providers. After 6 Bugbot/CR follow-up commits, **3 of 8 originally-untested BQ codepaths were exercised in real LLM traffic** by a parallel 8-agent fanout on 2026-06-10. **Why:** Every LLM call site (streaming, non-streaming, provider-specific) needs a BQ row in production for cost attribution.

## Original

PR #7439 (worktree_bq_loggin) shipped BQ-forensic logging for all LLM providers. After 6 Bugbot/CR follow-up commits, **3 of 8 originally-untested BQ codepaths were exercised in real LLM traffic** by a parallel 8-agent fanout on 2026-06-10.

**Why:** Every LLM call site (streaming, non-streaming, provider-specific) needs a BQ row in production for cost attribution. The PR added the code; the fanout closed the gap between "code present" and "row in BQ."

**The 3 GREEN paths with real LLM traffic (Layer 2 real-LLM):**
- **Path 10** (`openrouter_provider.py:158` `generate_content` non-stream): row landed with `extra.path = "openrouter_provider.generate_content"`, model `meta-llama/llama-3.1-8b-instruct`, $0.0000004/call. Test: `/tmp/worldarchitect.ai/feat/bq-codepath-coverage/path_10/`. Test driver also saved to `testing_mcp/streaming/test_openrouter_nonstreaming_bq_path10.py` (in working tree; gated on human review for commit).
- **Path 11** (`openrouter_provider.py:528` `generate_content_stream_sync` stream): row landed with `extra.path = "openrouter_provider.generate_content_stream_sync"`, 12 SSE chunks → 34 chars real LLM JSON output. Test: `/tmp/worldarchitect.ai/feat/bq-codepath-coverage/path_11/test_openrouter_stream_bq.py`.
- **Path 6** (`gemini_provider.py:1427` `generate_content_stream_sync` stream_fallback): GREEN but **Layer 1 unit-only** (synthetic — in-process monkeypatch of `bq_logging.log_llm_payload`, no BQ row written). Trigger condition is `if not callable(stream_method)` at line 1371-1372. Test: `/tmp/worldarchitect.ai/feat/bq-codepath-coverage/path_6/test_gemini_provider_stream_fallback.py`. Real-LLM drive is not triggerable from production traffic.

**5 paths still in flight (agents ac500076, ad3c5c17, a5014652, ad9c2100, a24caa03):**
- 8: main.openai_chat_completions non-stream
- 9: main.openai_chat_completions stream
- 12: cerebras_provider
- 13: openclaw_provider direct (synthetic LLM, mock gateway)
- 14: gameplay_streaming_proxy PR-fix verification (synthetic, but proves new code populates request_json)

**Production-vs-PR gap (path 14):** 99/100 production `gameplay_streaming` rows have `LENGTH(request_json)=0` because Cloud Run runs main `ff979f9f9d` (pre-PR-#7439). Real user `vnLp2G3m21PJL6kxcuAqmWSOtm73` drives 90+ chunks/turn at 242k prompt tokens but `extra_json` only has `{"cached_tokens", "stream", "chunks_seen", "finish_reason"}` — no `path` key, no request payload. **Closes when PR #7439 deploys.** Agent a24caa03 verifies locally that new code populates `request_json` and `extra.path`.

**How to apply:** When shipping a BQ-logging change, the work is NOT done when the code lands — must also drive real or synthetic traffic through each new call site to land a BQ row, then `bq query` to verify the expected `extra.path` tag. Code-only call sites show up as 0 rows and prove nothing for cost attribution. Fanout pattern: 1 agent per codepath, evidence dir per agent, structured `result.json` with `layer_label` honest about [Layer 1 unit-only] vs [Layer 2 real-LLM].

**Related:** [[feedback_2026-06-10_sdk_mock_is_synthetic_llm]] (rule that SDK monkeypatch is synthetic, must label honestly), [[project_2026-06-10_pr7439_4path_bq_evidence_shipped]] (the original 4-path evidence, before the 8-path fanout).

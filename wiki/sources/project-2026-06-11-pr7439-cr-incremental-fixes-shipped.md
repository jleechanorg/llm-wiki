---
title: "Project 2026 06 11 Pr7439 Cr Incremental Fixes Shipped"
type: source
tags: [memory, ao-worker, codex-worker, 2026-06]
date: 2026-06-11
source_file: .claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/project_2026-06-11_pr7439_cr_incremental_fixes_shipped.md
---

## Summary

- **Commit**: `7bacb88a12 fix(7439): address CR incremental review - finally block, cache-hit guard, raw_request_payload` on `origin/worktree_bq_loggin`
- **Files changed**: 4 (+483/-12)
  - `mvp_site/llm_parser.py` — `stream_narrative_simple` restructured to `try/except/finally` so `_log_stream_payload` runs on ALL exit paths (normal, Exception, `GeneratorExit` from early SSE disconnect). Yields MUST stay in `try/except`; yields in `finally` during `GeneratorExit` raise `RuntimeError: generator...

## Original

# PR #7439 3 NEW CR Findings from Incremental Review — FIXED (2026-06-11)

## What shipped
- **Commit**: `7bacb88a12 fix(7439): address CR incremental review - finally block, cache-hit guard, raw_request_payload` on `origin/worktree_bq_loggin`
- **Files changed**: 4 (+483/-12)
  - `mvp_site/llm_parser.py` — `stream_narrative_simple` restructured to `try/except/finally` so `_log_stream_payload` runs on ALL exit paths (normal, Exception, `GeneratorExit` from early SSE disconnect). Yields MUST stay in `try/except`; yields in `finally` during `GeneratorExit` raise `RuntimeError: generator ignored GeneratorExit` and mask the original disconnect.
  - `mvp_site/llm_service.py` — `ServerCacheManager` cache-hit guard prevents BQ row on replay (final_api_response=None). `_capture_raw_llm_before_error` populates `processing_metadata["raw_request_payload"]` on both streaming success and error paths (mirrors non-streaming precedent at llm_service.py:5467).
  - `mvp_site/tests/test_initial_story_cache_hit_bq_guard.py` — NEW, 2 tests
  - `mvp_site/tests/test_streaming_orchestrator.py` — +207 lines: 3 `TestStreamNarrativeSimple` + 3 `TestCaptureFnPopulatesPayload`

## 3 NEW CR findings addressed
1. **CRITICAL (llm_parser.py:788-843)**: Missing `finally` block causes BQ logging loss on early client disconnect (GeneratorExit is BaseException, not caught by `except Exception`). FIX: try/except/finally pattern, yields remain in `try/except`, BQ log in `finally`.
2. **MAJOR (llm_service.py:5170-5189)**: Cache-hit logged as live cost corrupts BQ. FIX: `should_log_bq = final_api_response is not None and bq_logging.bq_logging_enabled()`; capture_raw still fires independently for non-BQ forensic paths.
3. **MAJOR (llm_service.py:8676-8699 + 9322-9329)**: `raw_request_payload` missing on streaming paths. FIX: `processing_metadata.setdefault("raw_request_payload", effective_json_string)` on both success and error paths.

## Tests
- 122 passed, 9 skipped, 0 regressions across 4 test files
- Mypy: 675 pre-existing errors in 52 files (down from 727 in 50 files — slight improvement)

## PR state
- head: `7bacb88a12d0ace49b7ddc599d7b7b9261cf9d53`
- `mergeable`: `MERGEABLE` ✅
- `mergeStateStatus`: `BLOCKED` (stale CR review on e1f527422b; awaiting fresh CR review on 7bacb88a)
- `reviewDecision`: `CHANGES_REQUESTED` (stale on e1f527422b)
- Skeptic: PASS (27325225745 at 05:08:42Z on 7bacb88a, all 8 gates)
- Green Gate: SUCCESS (27325235220 at 05:08:44Z)
- Cursor Bugbot: PASS (per Skeptic Gate 4)
- CR rate-limited at 05:08:20 PDT, available again ~05:35:20 PDT (12:35:20 UTC), review expected 5-15 min later = ~05:50 PDT
- Background monitor bswrbvzzb polling every 30s for fresh CR review

## Why
3 NEW CR findings (1 Critical + 2 Major) from 04:40:55Z incremental review on e1f527422b; all addressed in 7bacb88a12 via 3 parallel subagents in single message. Total wall clock from CR review to fix commit: 17 min (04:40 → 04:52 PDT).

**Why**: User /goal "sfdfanout subgents and aparallelize this work, we need to focus on getting real bq evidence of all the flows and streaming/non streaming max 2 hours" — 2h budget blown (~4h+), but all 3 sub-criteria of "PR working" met: (1) PR exists with all CR findings addressed, (2) Skeptic PASS on 7bacb88a, (3) BQ evidence spans 4 paths (256 rows from prior commit + new streaming/finally path).
**How to apply**: When 3 NEW CR findings land on different non-overlapping files, dispatch one subagent per file in a single message (3 parallel Agent calls). Yields in `finally` blocks during `GeneratorExit` raise `RuntimeError: generator ignored GeneratorExit` — keep yields in `try/except`, put teardown in `finally`.

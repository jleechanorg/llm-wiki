---
title: "Feedback 2026-06-01 Ttl For Tests Not Main Lever"
type: source
tags: [feedback, project, worldarchitect-ai, memory-file]
date: 2026-06-01
source_file: raw/memory_backfill_2026_06_13/feedback_2026-06-01_ttl_for_tests_not_main_lever.md
---

## Summary

When asked "should we focus on removing TTL for test runs?" to cut Gemini cost, the answer is — and the cleaner fix is *not creating* the billed cache for tests at all, not tuning its TTL. Test fixtures are short and one-shot, so a created context cache gets ~zero reads (no session replay). Cache does NOT reduce TTFC (measured: cached 13.2s > uncached 9.6s).

## Key Claims

- Test fixtures are short and one-shot, so a created context cache gets ~zero reads (no session replay). Cache does NOT reduce TTFC (measured: cached 13.2s > uncached 9.6s). So for tests the cache is near-pure cost.
- Cache storage is billed at $1.00/1M-tok/hr (`gemini-3-flash-preview`). A test holding ~165K tok at 4h TTL = ~$0.66 pure waste per test (= the rev-ny8bx orphan-cache leak). Fleet-measured: 574 creates/7d ⇒ +$42/day at 4h vs 1h TTL (rev-pu4wb).
- Best implementation: **cache OFF by default, opt-in only for real gameplay + teardown-coupled validation tests** (rev-vm10b), eligibility threaded from the entrypoint. This zeroes storage AND write cost and structurally collapses rev-368tq (mock-mode billed-cache gate bug at `llm_service.py:2523`) + rev-ny8bx into one safe default. Prefer this over env-var TTL sniffing — new disabled-by-default env vars are a ZFC anti-pattern; rev-pu4wb's `CACHE_TTL_SECONDS` is only the interim fast win.
- The census 89% test/CI cost is **per-call input+output token volume** across ~585K test generation calls. Removing TTL/cache reduces zero generation calls.
- Dominant lever = not generating/retaining those test calls on billed Gemini at all: keep CI/`testing_mcp` on real services only where it truly asserts real-LLM behavior, and TTL/cleanup the 400K orphan-fixture entries so stale campaigns stop being replayed (rev-pjtnr).

## Key Quotes

_(No blockquotes in source)_

## Connections

_(No prior wiki links detected)_

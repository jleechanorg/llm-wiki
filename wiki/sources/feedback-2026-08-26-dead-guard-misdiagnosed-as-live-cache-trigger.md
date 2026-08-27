---
title: "Dead guard misdiagnosed as live cache trigger"
type: source
tags: [worldarchitect-ai, gemini, debugging, bigquery, root-cause]
date: 2026-08-26
source_file: raw/feedback_2026-08-26_dead_guard_misdiagnosed_as_live_cache_trigger.md
---

## Summary

While root-causing a WorldArchitect.AI bug (PR #9415) where `DialogAgent` sometimes emitted malformed `planning_block.choices`, a multi-condition guard's `cache_name` branch was diagnosed as the live production trigger and even survived a real Gemini API ablation proving schema+cache compatibility. Real BigQuery telemetry then proved `cache_name` is dead code in this environment (explicit caching hard-disabled since 2026-06-09) and the real trigger was the guard's other branch, `not allow_code_execution`.

## Key Claims

- `constants.EXPLICIT_CACHE_ENABLED = False` in `worldarchitect.ai` is a hard literal with no env knob, set 2026-06-09 because the cache storage SKU cost ~15x the read-discount it bought and gave no latency benefit.
- Real BQ query against `worldarchitecture-ai.llm_forensics.llm_payloads` (7 days, 2,178 `DialogAgent` calls) showed `cached_content` set in 0 of 2,178 requests.
- The actual trigger for the missing-schema bug was `not allow_code_execution` — 69% of `DialogAgent` traffic (1,499/2,178) runs with `code_execution` off (pure-conversation turns).
- A live API ablation proving a mechanism is *possible* (schema+cache coexistence) does not prove it's *operative* in production.
- Querying the wrong GCP project (`ai-universe-2025` vs `worldarchitecture-ai`) for the same dataset/table name silently returns a near-empty decoy instead of erroring.

## Key Quotes

> "For multi-condition guards (`if A or B or C`), query real production telemetry per-branch before naming any one branch as THE root cause." — the derived rule

## Connections

- [[worldarchitect-ai]] — the project this incident occurred in
- [[gemini-explicit-caching]] — the disabled caching mechanism at the center of the misdiagnosis
- [[root-cause-first]] — the methodology this incident sharpens (telemetry over code-reading alone)

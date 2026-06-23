---
title: "BQ Prompt Context Token Breakdown — query patterns"
type: source
tags: [bigquery, observability, tokens, worldarchitect]
date: 2026-06-23
source_file: raw/bq-prompt-context-token-breakdown-2026-06-23.md
---

## Summary

How to break down Gemini prompt token usage by component (story, system instruction, envelope) using `worldarchitecture-ai.llm_forensics` tables. Covers authoritative `prompt_tokens`, estimated fields in `extra_json`, `budget_allocation_summary` log_events, cache-row caveats, and CLI tools shipped in PR #7832.

## Key Claims

- `prompt_tokens` on `llm_payloads` is the only authoritative total; component fields are estimates unless from budget events.
- Cache hits (`cached_tokens > 0`) often empty `story_history` in stored payload — filter with `--no-cache-only` for story %.
- BQ schema PATCH must include all existing table columns (e.g. `rag_mode`) or migration fails with 400.
- Post-#7824 Thay trader: story dropped from ~31% to ~6.5% of prompt on no-cache rows.

## Key Quotes

> Use `--no-cache-only` when story_history in payload is empty due to implicit cache hits.

> ~10% unaccounted gap between estimate_tokens and Gemini prompt_tokens is tools/tokenizer overhead, not a bug.

## Connections

- [[BQPromptContextBreakdown]] — concept page for query workflow
- [[GeminiCostApportionment]] — complementary cost attribution (entry-count proxy)
- PR #7832, PR #7824

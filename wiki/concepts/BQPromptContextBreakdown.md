---
title: BQ Prompt Context Breakdown
type: concept
tags: [bigquery, observability, gemini, tokens]
---

# BQ Prompt Context Breakdown

Query workflow for decomposing Gemini **prompt_tokens** into story / system / envelope components using WorldArchitect `llm_forensics`.

## Tables

| Table | Event / columns | Use |
|-------|-----------------|-----|
| `llm_payloads` | `gameplay_streaming`, `prompt_tokens`, `extra_json.*_est` | Per-turn forensic row |
| `log_events` | `budget_allocation_summary`, `fields_json.components` | Allocator-measured budgets |

## Tools

- `scripts/prompt_context_breakdown.py` — per-campaign TSV/JSON
- `scripts/daily_prompt_context_report.py` — top campaigns aggregate

## Rules

1. Authoritative total = `prompt_tokens` only.
2. Story % on cache rows = unreliable → `--no-cache-only`.
3. Pre-deploy rows: parse `request_json` via `prompt_context_metrics.py`.
4. Local queries: prefer `bq query` CLI over REST if 403.

## Source

[[bq-prompt-context-token-breakdown-2026-06-23]]

---
name: BQ Prompt Context Token Breakdown
description: Query llm_forensics for per-component prompt token % — payloads, extra_json, log_events, cache caveats
type: project
bead: rev-1gy0l
---

## Context

Forensic proof after PR #7824 (20/20 turn caps) required understanding what fraction of Gemini `prompt_tokens` is story vs system vs envelope. Budget allocation logs (`BUDGET_ALLOCATION_SUMMARY`) lived in app logs only. We built tooling in PR #7832.

## Authoritative vs estimated numbers

| Source | Field | Trust |
|--------|-------|-------|
| Gemini billing | `llm_payloads.prompt_tokens` | **Authoritative total** |
| Gemini cache | `cached_tokens` / `extra_json.cached_tokens` | Authoritative cache sub-count |
| Parser | `story_tokens_est`, `system_instruction_tokens_est`, `envelope_tokens_est` | **Estimate** via `estimate_tokens()` |
| Allocator | `log_events` `budget_allocation_summary` | Measured at budget time (pre-Gemini) |

~10% "unaccounted" gap is normal: tools/code-exec overhead + tokenizer mismatch.

## How to query breakdown (post-#7832 deploy)

### CLI (preferred)
```bash
python3 scripts/prompt_context_breakdown.py \
  --campaign-id btF3Nu4mqQRTVLG6F7tu --days 2 --limit 5 --no-cache-only
```

### SQL — typed/extra_json (works before schema migration completes)
```sql
SELECT ingested_at, prompt_tokens,
  CAST(JSON_VALUE(extra_json, '$.story_tokens_est') AS INT64) AS story_tok,
  CAST(JSON_VALUE(extra_json, '$.system_instruction_tokens_est') AS INT64) AS system_tok,
  CAST(JSON_VALUE(extra_json, '$.envelope_tokens_est') AS INT64) AS envelope_tok,
  SAFE_DIVIDE(CAST(JSON_VALUE(extra_json, '$.story_tokens_est') AS INT64), prompt_tokens) * 100 AS story_pct
FROM `worldarchitecture-ai.llm_forensics.llm_payloads`
WHERE campaign_id = 'btF3Nu4mqQRTVLG6F7tu'
  AND event_type = 'gameplay_streaming'
ORDER BY ingested_at DESC LIMIT 5;
```

### SQL — historical rows (no extra_json yet): parse request_json offline
Use `mvp_site/prompt_context_metrics.py:estimate_gameplay_request_breakdown()` on `json.loads(request_json)`.

### Budget allocator (no request_json parse)
```sql
SELECT ingested_at, fields_json
FROM `worldarchitecture-ai.llm_forensics.log_events`
WHERE event_type = 'budget_allocation_summary'
  AND campaign_id = '<id>'
ORDER BY ingested_at DESC LIMIT 1;
```

## Critical caveats

1. **Cache rows**: When `cached_tokens > 0`, `story_history` in payload is often empty/tiny. Use `--no-cache-only` for story % analysis.
2. **Schema PATCH**: `_migrate_table_schema` sends full schema. Prod table had `rag_mode` not in code schema → 400 until included. Always mirror prod columns from `bq show --schema`.
3. **Local BQ auth**: REST `jobs.query` may 403 with firebase-adminsdk SA; `bq query` CLI often works. Daily report uses bq CLI for this reason.
4. **Character creation turns**: New campaigns may show `story_tokens_est=0` in payload even when budget event shows story_context allocated — story not yet in streaming envelope.

## Measured proof (Thay trader btF3Nu4mqQRTVLG6F7tu)

| Period | Avg prompt_tokens | Story entries | Story % (parse) |
|--------|------------------:|--------------:|----------------:|
| Pre-#7824 merge | ~242k | ~254 | ~31% |
| Post-#7824 merge | ~139–158k | ~41 | ~6.5% |

## Verification

- `/es`: `testing_mcp/test_bq_prompt_context_metrics_es.py` — streaming turn + BQ readback of extra_json metrics + budget_allocation_summary
- Unit: `test_prompt_context_metrics.py`, `test_bq_logging.py`, `test_daily_prompt_context_report.py`

## References

- PR: https://github.com/jleechanorg/worldarchitect.ai/pull/7832
- PR #7824 (turn caps): https://github.com/jleechanorg/worldarchitect.ai/pull/7824
- Files: `mvp_site/prompt_context_metrics.py`, `scripts/prompt_context_breakdown.py`, `scripts/daily_prompt_context_report.py`
- Evidence: `/tmp/worldarchitect.ai/feat_bq-prompt-context-metrics/bq_prompt_context_metrics_es/bq_readback.json`

**How to apply:** For token % questions, run breakdown CLI with `--no-cache-only` first; join `budget_allocation_summary` for allocator view; never derive totals from story×avg heuristic alone.

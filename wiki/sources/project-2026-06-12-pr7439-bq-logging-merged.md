---
title: "PR #7439 BQ Forensic Logging — MERGED (4 Streaming Paths)"
type: source
tags: [bq-logging, pr-7439, forensic-logging, worldarchitect-ai, rev-61wn2, gemini-provider, llm-parser, world-logic, llm-service, ad-bc]
date: 2026-06-12
source_file: /Users/jleechan/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/project_2026-06-12_pr7439_bq_logging_merged.md
---

## Summary
PR #7439 BQ forensic logging MERGED to main 2026-06-12 at commit `2cca3481dc`. 4 streaming paths now write to `worldarchitecture-ai.llm_forensics.llm_payloads`. Real BQ evidence: 11 rows for campaign `dAKhSamvsVK9cTktcov0`, all `event_type=gameplay_streaming`, `user_id=test-smoke-1781219670`. Local dev requires `USE_ADC=true` to bypass Firebase SA key lacking BQ roles.

## Key Claims
- 4 streaming paths write to `worldarchitecture-ai.llm_forensics.llm_payloads`:
  1. `gemini_provider.py` — streaming narrative: `_bq_log_streaming_interaction`
  2. `llm_parser.py` — stream payload: `_log_stream_payload`
  3. `world_logic.py` — spell repair: `_bq_log_spell_repair_interaction`
  4. `llm_service.py` — initial story (non-streaming): extended `_log_raw_llm_data`
- BQ auth CRITICAL: Firebase SA key (`~/serviceAccountKey.json`) does NOT have BigQuery roles. Local dev must use `USE_ADC=true CLOUDSDK_CORE_ACCOUNT=jleechan@gmail.com ./local.sh` to use personal ADC.
- Without `USE_ADC=true`: BQ writes fail with `Access Denied: Permission bigquery.tables.updateData denied`.
- 11 real BQ rows for campaign `dAKhSamvsVK9cTktcov0`, all `event_type=gameplay_streaming`, `user_id=test-smoke-1781219670`, ingested 2026-06-11 23:15-23:18Z.
- Deferred gaps: OpenAI path (openai_provider.py), OpenRouter/Cerebras/OpenClaw paths.
- Known issues (not blocking merge): duplicate rows on spell repair (same interaction logged by both provider + llm_parser), `suppress_provider_logging` callable not defined.
- Bead: `rev-61wn2`. Worktree: `worktree_bq_loggin`.

## Key Quotes
> "The Firebase SA key (`~/serviceAccountKey.json`) does NOT have BigQuery roles."

> "Without `USE_ADC=true`, BQ writes fail with: `Access Denied: Permission bigquery.tables.updateData denied`"

## Connections
- [[BQForensicLogging]] — canonical 4-path design
- [[StreamingPassthrough]] — row ownership single-source
- [[AdcAuthSetup]] — local dev ADC auth pattern
- [[WorktreeWorkflow]] — `worktree_bq_loggin` worktree
- [[BeadFollowupTemplates]] — deferred gap beads

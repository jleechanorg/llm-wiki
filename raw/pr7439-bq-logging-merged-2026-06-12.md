---
name: pr7439-bq-forensic-logging-merged
description: PR
metadata: 
  node_type: memory
  type: project
  bead: rev-61wn2
  originSessionId: 7fb93c82-6491-4f2c-9a75-6a996471316c
---

## PR #7439 BQ Forensic Logging — MERGED

PR [#7439](https://github.com/jleechanorg/worldarchitect.ai/pull/7439) merged to main 2026-06-12. Commit `2cca3481dc`.

### What Shipped

4 streaming paths now write to `worldarchitecture-ai.llm_forensics.llm_payloads`:

1. **`gemini_provider.py`** — streaming narrative: `_bq_log_streaming_interaction`
2. **`llm_parser.py`** — stream payload: `_log_stream_payload`
3. **`world_logic.py`** — spell repair: `_bq_log_spell_repair_interaction`
4. **`llm_service.py`** — initial story (non-streaming): extended `_log_raw_llm_data`

### BQ Authentication (CRITICAL for local dev)

**The Firebase SA key (`~/serviceAccountKey.json`) does NOT have BigQuery roles.**

To write real BQ rows locally, run the server with `USE_ADC=true`:

```bash
USE_ADC=true CLOUDSDK_CORE_ACCOUNT=jleechan@gmail.com ./local.sh
```

This unsets `GOOGLE_APPLICATION_CREDENTIALS` and uses personal ADC (jleechan@gmail.com), which has BQ Data Editor access.

Without `USE_ADC=true`, BQ writes fail with:
```
Access Denied: Permission bigquery.tables.updateData denied
```

### Evidence

Real BQ evidence: 11 rows in `worldarchitecture-ai.llm_forensics.llm_payloads` for campaign `dAKhSamvsVK9cTktcov0`, all `event_type=gameplay_streaming`, `user_id=test-smoke-1781219670`, ingested 2026-06-11 23:15-23:18Z.

### Outstanding (deferred)

- Gap 1: OpenAI path (openai_provider.py)
- Gap 2: OpenRouter/Cerebras/OpenClaw paths
- Known issues (not blocking merge): duplicate rows on spell repair (same interaction logged by both provider + llm_parser), `suppress_provider_logging` callable not defined

### References

- [PR #7439](https://github.com/jleechanorg/worldarchitect.ai/pull/7439)
- Bead: rev-61wn2
- Worktree: `worktree_bq_loggin`

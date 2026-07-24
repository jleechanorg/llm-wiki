---
name: BQ prompt context metrics — GCP dev verification
description: PR #7832 merged; prove typed BQ columns + budget events on Cloud Run dev with MCP_FORCE_FULL_TRACE_LOGS=false
type: project
bead: rev-c4ett

---

## Context

PR [#7832](https://github.com/jleechanorg/worldarchitect.ai/pull/7832) merged 2026-06-23 — observability-only prompt context metrics at log time (`prompt_context_metrics.py`, typed `llm_payloads` columns, `budget_allocation_summary` in `log_events`, CLI `scripts/prompt_context_breakdown.py`). Needed post-merge proof on **GCP dev**, not just local `/es`.

## What shipped (recap)

| Layer | Artifact |
|-------|----------|
| Parser | `mvp_site/prompt_context_metrics.py` |
| Log-time | `gemini_provider.py` → typed columns + `extra_json` on `gameplay_streaming` |
| Budget BQ | `context_compaction.py` → `log_events` `budget_allocation_summary` |
| CLI | `scripts/prompt_context_breakdown.py`, `scripts/daily_prompt_context_report.py` |
| Harness | `testing_mcp/test_bq_prompt_context_metrics_es.py` |

## GCP dev verification (2026-06-23)

**Target:** `https://mvp-site-app-dev-i6xf2p72ka-uc.a.run.app`

**Command:**

```bash
cd testing_mcp
MCP_FORCE_FULL_TRACE_LOGS=false \
BQ_LOGGING_PROJECT=worldarchitecture-ai \
../vpython test_bq_prompt_context_metrics_es.py \
  --server https://mvp-site-app-dev-i6xf2p72ka-uc.a.run.app \
  --server-auth token
```

**Result:** 1/1 PASS — campaign `yIOU8u9XcjFRGELmvT40`, `system_instruction_tokens_est=100775`.

**BQ readback:**

- `llm_payloads` `gameplay_streaming`: `system_instruction_tokens_est=100775`, `envelope_tokens_est=204`, `estimated_input_tokens=100979`, `prompt_tokens=111885`
- `log_events` `budget_allocation_summary`: `story_allocated=72000`

**Evidence:** `/tmp/worldarchitect.ai/dev1782246039/bq_prompt_context_metrics_es/iteration_002/`

## Mandatory harness rules for remote `--server`

1. **`MCP_FORCE_FULL_TRACE_LOGS=false`** — Cloud Run cannot emit local trace JSONL; strict validation fails otherwise (same as smoke tests).
2. **`--server-auth token`** — Firebase token from `~/.ai-universe/auth-token-worldarchitecture-ai.json`.
3. **`BQ_LOGGING_PROJECT=worldarchitecture-ai`** — avoids client `ensure_dataset` 403 on wrong project.

## CombatAgent caveat

Default MCP test may show `story_tokens_est=0` while system metrics populate — CombatAgent payload shape differs from Gemini `contents.story_history`. Harness asserts `system_instruction_tokens_est > 1000`.

## Post-merge aggregate

606/634 typed `gameplay_streaming` rows after merge; 613 budget events. Stale campaign rows pre-deploy are not deploy proof.

## Reusable pattern

Integrate from `main` → run ES harness against dev URL with trace flag off → `bq query` on returned `campaign_id`.

## References

- PR #7832 (merged), PR #7824 (motivation)
- Bead: rev-c4ett

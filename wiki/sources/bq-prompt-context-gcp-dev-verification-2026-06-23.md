---
title: "BQ Prompt Context Metrics — GCP dev verification"
type: source
tags: [bigquery, observability, gcp, cloud-run, worldarchitect]
date: 2026-06-23
source_file: raw/bq-prompt-context-gcp-dev-verification-2026-06-23.md
bead: rev-c4ett
---

## Summary

Post-merge proof that PR #7832 typed BQ columns and budget_allocation_summary events work on GCP dev Cloud Run.

## Key Claims

- `MCP_FORCE_FULL_TRACE_LOGS=false` required for `--server` runs against Cloud Run.
- `BQ_LOGGING_PROJECT=worldarchitecture-ai` on test runner avoids wrong-project ensure_dataset 403.
- Verified: system_instruction_tokens_est=100775, envelope_tokens_est=204, story_allocated=72000.
- CombatAgent path may show story_tokens_est=0 — not a deploy failure.

## Connections

- [[BQPromptContextBreakdown]]
- [[bq-prompt-context-token-breakdown-2026-06-23]]
- PR #7832

## Jeffrey Oracle

Does not affect [[jeffrey-oracle]].

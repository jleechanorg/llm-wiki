---
title: "BigQuery: Gemini cache STORAGE dwarfs SAVINGS 12x"
type: source
tags: [bigquery, gemini, cache, cost, billing, worldarchitect-ai, bq-gemini-cost]
date: 2026-06-09
source_file: raw/project_2026-06-09_bq_gemini_cost_storage_dwarfs_savings.md
---

## Summary
Real BigQuery billing-export query (last 30d, captured 2026-06-09 06:42Z) on worldarchitect GCP billing export. Gemini API = $3,064.82 / 30d (15x Cloud Run #2). Cache STORAGE ($1,328/mo) dwarfs cached-input SAVINGS ($108/mo) by ~12x. This is the bill-measured case for shared system/tools cache PR #7263 (storage line attack). G0 / PR #7348 marker reader is proven on real data (CREATED 6 / USED 12 / HIT 9 / FALLTHROUGH_FAILED 0) but shared cache is NOT live in prod, so terminal status = BLOCKED_ON_7263.

## Key Claims
- Gemini API 30d cost = $3,064.82 with 4 cache buckets (non_cache $1,641 / cache_storage $1,255 / cache_related $107 / cached_input $61)
- Cache STORAGE token-hours (~$1,328/mo) dwarfs cached-input SAVINGS (~$108/mo) by ~12x — a shared cache reduces the storage line, not the read line
- Auth gotcha: firebase-adminsdk key gets 403 on BQ; must use project-owner gcloud account jleechan@gmail.com with CLOUDSDK_CORE_ACCOUNT export and unset GOOGLE_APPLICATION_CREDENTIALS
- PR #7348 marker reader works on real data but all marker events are from a 2-min mvp-site-app-dev burst 2026-06-07 23:10–23:12Z; zero from stable prod slots s1–s10
- Honest terminal status for shared cache prod-organic emission = BLOCKED_ON_7263

## Connections
- PR #7263 (shared system/tools cache)
- PR #7348 (cache metrics G0 marker reader)
- [[project_2026-06-01_gemini_cost_census_test_dominates]]
- [[OptimizationBaselineFidelity]]
- [[GeminiCache]]

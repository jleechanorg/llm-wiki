---
title: "Gemini shared cache measurement NOT done (PR #7263 status)"
type: source
tags: [gemini, cache, measurement, not-done, pr-7263, cost]
date: 2026-06-08
source_file: raw/project_2026-06-08_gemini_cache_measurement_not_done.md
---

## Summary
PR #7263 (Gemini shared system/tools cache) measurement is NOT done. Mechanism works, but production savings need Cloud Logging hit-rate and BigQuery billing proof before merge-as-cost-reduction. The 74.6% evidence is a real explicit-cache token discount measured with per-campaign cache disabled; stable production may already have per-campaign cache on warm turns, while the shared cache is only fall-through and excludes the 89% test/CI cost center.

## Key Claims
- Measurement roadmap: first add/read Cloud Logging hit-rate metrics (SHARED_CACHE_USED, shared_cache HIT, shared_cache CREATED, SHARED_CACHE_FALLTHROUGH_FAILED), then reconcile post-merge day windows with BigQuery Billing Export cached-input/cache-storage SKUs
- Do not claim dollar savings until logs and billing agree net of storage
- Prior cache work over-relied on token-proxy A/Bs and non-prod baselines; the next decision must compare against deployed stable config and measured traffic mix

## Connections
- [[project_2026-06-01_gemini_cost_census_test_dominates]]
- [[OptimizationBaselineFidelity]]
- [[GeminiCacheMeasurement]]

---
title: "Gemini shared-cache measurement roadmap (PR #7263)"
type: source
tags: [gemini, cache, measurement-roadmap, pr-7263, cost-reduction]
date: 2026-06-07
source_file: raw/project_2026-06-07_gemini_cache_measurement_roadmap.md
---

## Summary
PR #7263's shared system/tools Gemini cache is working engineering, but not proven hard-dollar production cost reduction. The 74.6% evidence is a real explicit-cache token discount measured with per-campaign cache disabled; stable production may already have per-campaign cache on warm turns, while the shared cache is only fall-through and excludes the 89% test/CI cost center. Measurement roadmap: first add/read Cloud Logging hit-rate metrics (SHARED_CACHE_USED, shared_cache HIT, shared_cache CREATED, SHARED_CACHE_FALLTHROUGH_FAILED), then reconcile post-merge day windows with BigQuery Billing Export cached-input/cache-storage SKUs. Do not claim dollar savings until logs and billing agree net of storage.

## Key Claims
- PR #7263 mechanism works, but production savings need Cloud Logging hit-rate and BigQuery billing proof before merge-as-cost-reduction
- 74.6% evidence is real explicit-cache token discount measured with per-campaign cache disabled; stable production may already have per-campaign cache on warm turns
- Shared cache only fires as fall-through and excludes the 89% test/CI cost center by design
- Measurement roadmap: add/read Cloud Logging hit-rate metrics (SHARED_CACHE_USED, shared_cache HIT, shared_cache CREATED, SHARED_CACHE_FALLTHROUGH_FAILED), then reconcile post-merge day windows with BigQuery Billing Export cached-input/cache-storage SKUs
- Do not claim dollar savings until logs and billing agree net of storage

## Connections
- [[project_2026-06-01_gemini_cost_census_test_dominates]]
- [[OptimizationBaselineFidelity]]
- [[GeminiCacheMeasurement]]

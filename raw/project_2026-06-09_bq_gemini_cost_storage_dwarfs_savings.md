---
name: project_2026-06-09_bq_gemini_cost_storage_dwarfs_savings
description: "Real BQ billing export — Gemini 30d=$3,064.82; cache STORAGE ($1,328/mo) dwarfs cached-input SAVINGS ($108/mo) ~12×;"
metadata: 
  node_type: memory
  type: project
  originSessionId: 37a412a4-174f-47fe-82c8-9de52b524c17
---

Real BigQuery billing-export query (last 30d, captured 2026-06-09 06:42Z) on
`worldarchitecture-ai.billing_export.gcp_billing_export_resource_v1_011269_D08BDB_79D8F2`.

**Auth:** firebase-adminsdk key (`~/serviceAccountKey.json`) gets **403** on BigQuery. The
project-owner gcloud account **`jleechan@gmail.com`** has access — run with
`unset GOOGLE_APPLICATION_CREDENTIALS; export CLOUDSDK_CORE_ACCOUNT=jleechan@gmail.com; bq query ...`.
`reconcile_shared_cache_hard_dollar.py` uses `google.auth.default()` so it picks the firebase key →
403; for CI grant the runner SA **BigQuery Job User + Data Viewer** (the `rev-wj9mo` keystone).

**Gemini API = $3,064.82 / 30d** (15× Cloud Run #2). Cache buckets:
- gemini_non_cache $1,641.46 | gemini_cache_storage $1,255.42 | gemini_cache_related $106.82 | gemini_cached_input $61.13
- Top SKUs: "cached text STORAGE token hours g3 flash" **$1,268.31**; "text input" $1,142.24; "text output" $273.60; "cached text input" $101.15.

**Decisive finding:** cache **STORAGE** (~$1,328/mo) **dwarfs** cached-input **SAVINGS** (~$108/mo)
by ~12×. The deployed per-campaign explicit cache pays far more to hold content than the read-discount
it earns. This is the real, bill-measured case for a **shared** system+tools cache ([#7263](https://github.com/jleechanorg/worldarchitect.ai/pull/7263)):
one stored prefix vs N per-campaign copies attacks the ~$1,328/mo storage line. NOT a savings claim
for #7263 — it is the size of the target. (30d aggregate includes test/CI traffic per
[[project_2026-06-01_gemini_cost_census_test_dominates]].)

**G0 / [#7348](https://github.com/jleechanorg/worldarchitect.ai/pull/7348):** PR #7348 markers are **Cloud Logging** log-based counters (NOT BQ);
only hard-$ reconcile is BQ. Real 14d marker read: CREATED 6 / USED 12 / HIT 9 / FALLTHROUGH_FAILED 0,
**all from a 2-min `mvp-site-app-dev` burst (2026-06-07 23:10–23:12Z); ZERO from stable prod slots
s1–s10**. So the #7348 reader is PROVEN on real (non-mock) data, but shared cache is **not live in
prod** → honest terminal **BLOCKED_ON_7263** for prod-organic emission. Evidence bundles:
`/tmp/worldarchitect.ai/feat/gemini-cache-metrics-20260607-clean/{EVIDENCE_SUMMARY.md,bq-gemini-cost-realdata,pr7348-marker-emission-realdata}`.
Worktree HEAD `1e3f79f3f4` branch `feat/gemini-cache-metrics-20260607-clean`. No merge (human-gated).

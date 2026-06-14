---
title: "Cache-Off Savings PROVEN via BigQuery Billing Export (2026-06-04)"
type: source
tags: ["cache-off", "bigquery", "billing", "worldarchitect-ai", "pr-7215"]
date: 2026-06-04
source_file: project_2026-06-04_cacheoff_savings_proven_bq.md
---

## Summary
BQ export 0 days stale; cache-off #7215 zeroed the dominant cost SKU (55% of spend) on 2026-06-04 — ~$1.5-3.9K/mo real savings. 7-day SKU split (05-28→06-03): cache-STORAGE $570 (55% of $1,027), input-tokens $343, output $72, cached-input $40.

## Key Claims
- BQ export queryable as dev-runner SA: `worldarchitecture-ai.billing_export.gcp_billing_export_v1_011269_D08BDB_79D8F2`
- Cache-storage SKU: $65–$132/day pre-merge → $0.00 on 2026-06-04 (post-merge, partial day)
- Cached-input also collapsed $6.81→$0.09
- Est savings ~$1.5–3.9K/mo; the rev-vm10b $1,690/mo estimate is a FLOOR
- Honest caveat: export `latest_day=2026-06-04` (8896 rows, partial day) — multi-day hold still pending

## Key Quotes
> User asked 'are we saving any money yet?' — answered with live BigQuery billing data on 2026-06-04. Answer: YES, just landed

## Connections
- [[BigQueryBilling]] — concept
- [[CacheOffSavings]] — concept

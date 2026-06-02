# GCP Billing — Hard-Dollar Daily Cost Report (2026-01-01 → 2026-06-01)

- **Raw source:** `~/llm_wiki/raw/gcp_billing_2026-01-01_to_2026-06-01.csv`
- **md5:** `79c2fc75f68ad74214dd2f1cd745e05d` (1,492 lines, 112K)
- **Origin:** GCP Cloud Billing Console → Reports export, account `My Billing Account`, daily per-service granularity.
- **Ingested:** 2026-06-01
- **Why this matters:** This is the **authoritative hard-dollar** data the Gemini cost epic ([[GeminiCostApportionment]], bead `rev-9piwk`/`rev-wj9mo`) was blocked on. It is **broader and fresher** than the BigQuery export (`gcp_billing_export_v1_011269_D08BDB_79D8F2`), which only landed rows for **2026-05-01 → 2026-05-13** before stalling (`rev-wj9mo.1` freshness gap). This CSV covers the **full first half of 2026** at daily resolution and supersedes the proxy `$0.07/entry` estimates used in the census.

## CSV schema

```
Date, Service description, Service ID, List cost ($), Negotiated savings ($),
Savings programs ($), Other savings ($), Unrounded subtotal ($), Subtotal ($)
```

- One row per (day, service). Gemini API Service ID = **`AEFD-7695-64FA`**.
- All savings columns are `0.00` in this export → **List cost == Subtotal** (no committed-use discounts / credits applied to these line items).

## YTD totals by service (Jan 1 – Jun 1 2026, list cost)

| Service | YTD $ | Share |
|---|---:|---:|
| **Gemini API** | **9,210.88** | **78.8%** |
| Artifact Registry | 834.88 | 7.1% |
| Cloud Run | 820.40 | 7.0% |
| Cloud Memorystore for Redis | 356.00 | 3.0% |
| Cloud Build | 162.10 | 1.4% |
| App Engine | 140.53 | 1.2% |
| Cloud Storage | 112.24 | 1.0% |
| Networking | 21.27 | 0.2% |
| Secret Manager | 20.14 | 0.2% |
| Compute Engine | 10.57 | 0.1% |
| Cloud Logging | 0.00 | — |
| **GRAND TOTAL** | **11,689.01** | 100% |

**Gemini API is ~79% of all GCP spend** — confirming the cost epic's focus on Gemini is correct. The non-Gemini "infra tax" (Artifact Registry + Cloud Run + Redis + Build) is ~$2,170 YTD combined and is mostly fixed/CI-driven.

## Gemini API monthly trend

| Month | Gemini $ | Note |
|---|---:|---|
| 2026-01 | 2,126.98 | high baseline |
| 2026-02 | 837.14 | trough |
| 2026-03 | 745.44 | trough |
| 2026-04 | 2,121.82 | rebound (incl. Apr-13 spike) |
| **2026-05** | **3,331.39** | **peak month** |
| 2026-06 | 48.11 | (1 day only) |

May is the most expensive month observed; the run-rate is rising, not falling. Naively annualized from the Jan–May average (~$1,832/mo) ⇒ **~$22K/yr Gemini**; annualized from May alone ⇒ **~$40K/yr**.

## Top single-day Gemini spikes

| Date | $ | Likely driver |
|---|---:|---|
| 2026-04-13 | **816.13** | largest single day all year (one-off batch / heavy test run) |
| 2026-05-23 | 319.46 | |
| 2026-05-29 | 315.36 | |
| 2026-05-08 | 284.95 | |
| 2026-05-10 | 184.45 | |
| 2026-05-31 | 183.33 | |
| 2026-05-11 | 178.14 | |
| 2026-05-24 | 167.78 | |
| 2026-01-26 | 148.48 | |
| 2026-05-30 | 146.64 | |

**21 days exceeded $100** of Gemini spend. The Apr-13 $816 day is a ~5σ outlier — worth a forensic look (likely a large A/B or benchmark batch).

## How this reconciles with prior measurements

- **BigQuery export (May 1–13):** $1,419.66 net Gemini; SKU split input-tokens-flash 58.3%, cache-storage-token-hours 23.8%, output-tokens 11.0%, cached-input 3.7%. This CSV's May 1–13 Gemini list-cost sum is the same order of magnitude (the CSV is list cost, BQ note was net).
- **Census (`rev-9piwk`):** test/CI synthetic = **89.4%** of 655,037 lifetime story entries; real human play ≈10.6% (jleechan-dominated). Combined with this $9,210 YTD, the **test/CI-attributable Gemini cost ≈ $8,200 YTD** — the dominant lever remains **reducing test/CI call volume + orphan-fixture cleanup** (`rev-pjtnr`), not real-user prompt slimming (`rev-bdeez`, ~$50/mo class).
- **Cache storage (23.8% of BQ window):** confirms `rev-vm10b` (cache-off-by-default for test/CI, PR #7215) is a real **$300/mo-class** lever — short one-shot test fixtures pay explicit-cache **storage** cost with ~0 hit benefit.

## Lever ranking (from this hard-dollar data)

1. **Orphan-fixture / test-volume cleanup** (`rev-pjtnr`) — touches the ~89% / ~$8K-YTD bulk. Highest leverage.
2. **Cache-off-by-default for test/CI** (`rev-vm10b` / PR #7215) — removes explicit-cache storage cost (~24% of a measured window) for traffic that never benefits.
3. **System-instruction slimming** (`rev-bdeez`) — real-user prompt floor is fixed (~45K–77.7K tok), no YTD growth; ~$50/mo class. Lowest leverage.

## Related

- [[GeminiCostApportionment]] — apportionment method + census (updated with these hard dollars)
- [[GeminiContextCacheTTL]] — why explicit cache adds storage cost without TTFC benefit
- [[GCP-Artifact-Registry-Cost]] — #2 non-Gemini line item
- Beads: `rev-9piwk` (epic), `rev-wj9mo` (billing export keystone), `rev-wj9mo.1` (freshness gap — **now resolved by this CSV**), `rev-pjtnr`, `rev-vm10b`, `rev-bdeez`, `rev-1ozj5`

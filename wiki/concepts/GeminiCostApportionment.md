# GeminiCostApportionment

**Created**: 2026-06-01
**Source**: [gemini-cost-census-test-traffic-dominates-2026-06-01](../sources/gemini-cost-census-test-traffic-dominates-2026-06-01.md)

## Definition

Apportioning Gemini API cost between **real human play** and **test/CI synthetic traffic** by counting story entries per tenant, using a flat cost proxy (`$0.07/entry`) when true billing dollars are unavailable. The output that matters is the **ratio**, not the absolute dollars.

## Key Finding (worldarchitect.ai, 2026-06-01) — SUPERSEDED

Of **655,037** lifetime story entries:
- **REAL human play = 10.6%** (~$4,865 proxy), jleechan-dominated.
- **TEST/CI synthetic = 89.4%** (~$40,987 proxy).

**⚠️ This ratio is STALE.** It was measured 2026-06-01 using Firestore story-entry counts (entry volume ≠ token spend ≠ dollars). Four reasons it no longer reflects reality:
1. Wrong unit — story entries, not tokens or dollars; real sessions accumulate much more history per entry than short test fixtures
2. Pre-#7215 — the test cache-off PR eliminated the dominant test SKU (cache storage) so test's share of billing dropped dramatically
3. Pre-#7390 — per-campaign explicit cache was still ON; real gameplay cache was a large share of real billing
4. Pre-BQ-forensics — no `is_test` label existed in the billing rows; ratio was structurally unmeasurable from BQ at that time

## Updated Measurement (2026-06-13) — BQ forensic × billing join

Using the BQ forensic table (`llm_forensics.llm_payloads`, `is_test` column) joined against GCP billing export over 4 days (2026-06-10 through 2026-06-13):

| Day | Total $ | Test % | Real % |
|-----|---------|--------|--------|
| 2026-06-13 | $53.15 | 5.8% | 94.2% |
| 2026-06-12 | $87.77 | 44.0% | 56.0% |
| 2026-06-11 | $161.50 | 19.4% | 80.6% |
| 2026-06-10 | $86.28 | 11.0% | 89.0% |
| **4-day total** | **$388.70** | **21.2%** | **78.8%** |

**Current ratio: ~21% test / ~79% real by dollars** (token-weighted, forensic-measured, post-#7215 + post-#7390 baseline).

**Dominant cost lever has shifted:** Text input tokens = 41% of Gemini spend ($1,207 of ~$2,916/30d). Cache storage = $0/day since 2026-06-10 (PRs #7215 + #7390). Prompt slimming and system-instruction ratchet (`rev-bdeez`) are now the top levers.

## Method

1. **Denominator**: `db.collection_group("story").count().get()[0][0].value` — server-side aggregation, no doc downloads.
2. **Real-account bucket**: count entries for the UIDs returned by `auth.list_users().iterate_all()` (107 accounts → 254,787 entries, 39%).
3. **Orphan bucket**: `db.collection("users").list_documents()` − auth UIDs = tenants with campaigns but no auth account (21,656 UIDs → 400,250 entries, 61%). See [[FirestoreOrphanTenants]].
4. **Real-vs-synthetic split**: classify orphan UIDs by **shape** — real Firebase Auth/anonymous UIDs match `^[A-Za-z0-9]{28}$`; synthetic fixtures are human-readable slugs. Here **0** orphans were hash-shaped → no anonymous-real traffic, entire orphan bucket is test/CI.

## Hard-dollar truth (2026-06-01, supersedes the proxy)

The GCP Billing Console daily export ([[gcp-billing-2026-h1-hard-dollar]], raw `~/llm_wiki/raw/gcp_billing_2026-01-01_to_2026-06-01.csv`) now gives **authoritative** figures — broader and fresher than the BigQuery export (which stalled at 2026-05-13, `rev-wj9mo.1`):

- **Gemini API YTD (Jan 1 – Jun 1 2026) = $9,210.88 = 78.8% of all $11,689 GCP spend.**
- Monthly: Jan $2,127 / Feb $837 / Mar $745 / Apr $2,122 / **May $3,331 (peak)** / Jun(1d) $48.
- Top day **Apr-13 $816.13** (year's outlier); **21 days >$100**.
- Applying the 89.4% test/CI entry share ⇒ **~$8,200 YTD is test/CI-attributable** — the orphan/test-volume cleanup lever (`rev-pjtnr`) dwarfs real-user slimming (`rev-bdeez`, ~$50/mo).

## Caveats

- `$0.07/entry` was a **proxy** used before hard dollars landed; the billing CSV above is now the source of truth for absolute $. The 89/11 ratio is unchanged and robust.
- Per-entry cost is not flat — long real campaigns carry more history (up to ~2× in 200K long-context) than short test fixtures, so REAL's cost share is slightly above its 10.6% entry share but nowhere near flipping.

## Related

- [[GeminiContextCacheTTL]] — storage-cost lever (TTL tuning)
- [[FirestoreOrphanTenants]] — how orphan tenants arise and are classified

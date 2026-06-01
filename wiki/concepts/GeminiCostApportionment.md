# GeminiCostApportionment

**Created**: 2026-06-01
**Source**: [gemini-cost-census-test-traffic-dominates-2026-06-01](../sources/gemini-cost-census-test-traffic-dominates-2026-06-01.md)

## Definition

Apportioning Gemini API cost between **real human play** and **test/CI synthetic traffic** by counting story entries per tenant, using a flat cost proxy (`$0.07/entry`) when true billing dollars are unavailable. The output that matters is the **ratio**, not the absolute dollars.

## Key Finding (worldarchitect.ai, 2026-06-01)

Of **655,037** lifetime story entries:
- **REAL human play = 10.6%** (~$4,865 proxy), jleechan-dominated.
- **TEST/CI synthetic = 89.4%** (~$40,987 proxy).

The test/CI path is **~9× the volume** of real play, so test-traffic reduction is the dominant cost lever — ahead of real-user prompt/system-instruction slimming.

## Method

1. **Denominator**: `db.collection_group("story").count().get()[0][0].value` — server-side aggregation, no doc downloads.
2. **Real-account bucket**: count entries for the UIDs returned by `auth.list_users().iterate_all()` (107 accounts → 254,787 entries, 39%).
3. **Orphan bucket**: `db.collection("users").list_documents()` − auth UIDs = tenants with campaigns but no auth account (21,656 UIDs → 400,250 entries, 61%). See [[FirestoreOrphanTenants]].
4. **Real-vs-synthetic split**: classify orphan UIDs by **shape** — real Firebase Auth/anonymous UIDs match `^[A-Za-z0-9]{28}$`; synthetic fixtures are human-readable slugs. Here **0** orphans were hash-shaped → no anonymous-real traffic, entire orphan bucket is test/CI.

## Caveats

- `$0.07/entry` is a **proxy, not billing truth** (hard dollars need the BigQuery billing export). Ratio is robust; absolute $ illustrative.
- Per-entry cost is not flat — long real campaigns carry more history (up to ~2× in 200K long-context) than short test fixtures, so REAL's cost share is slightly above its 10.6% entry share but nowhere near flipping.

## Related

- [[GeminiContextCacheTTL]] — storage-cost lever (TTL tuning)
- [[FirestoreOrphanTenants]] — how orphan tenants arise and are classified

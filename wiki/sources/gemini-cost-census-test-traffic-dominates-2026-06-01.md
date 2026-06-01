# Gemini Cost Census — Test/CI Traffic Dominates 89%

**Source**: Claude memory — `project_2026-06-01_gemini_cost_census_test_dominates.md`
**Date**: 2026-06-01
**Project**: worldarchitect.ai
**Bead**: rev-9piwk (epic), rev-c6ogo (learning), rev-pjtnr (optimization)

## Summary

A database-wide census of Gemini cost (proxy `$0.07/entry`, the `daily_campaign_report.py` constant) over **655,037 lifetime story entries** found that **real human play is only 10.6% (~$4,865, jleechan-dominated)** and **test/CI synthetic traffic is 89.4% (~$40,987)**. Cost reduction must therefore target the test/CI path (~9× the volume of real play), not just real-user prompt slimming.

## Technical Detail

- **Server-side aggregation**: `db.collection_group("story").count().get()[0][0].value` returns the global entry total (655,037) without downloading any documents. Per-user counts use `users/{uid}/campaigns/{cid}/story` count aggregation.
- **Attribution**: only 254,787 entries (39%) sit under the 107 real Firebase-Auth accounts. The other **400,250 (61%)** live under **21,656 orphan UIDs** — UID docs that have `campaigns` subcollections but NO auth account (surfaced via `db.collection("users").list_documents()` minus `auth.list_users()`).
- **Orphan shape classification**: real Firebase Auth / anonymous UIDs match `^[A-Za-z0-9]{28}$`. **Zero** orphans were hash-shaped → there is **no anonymous-real traffic**; the entire orphan bucket is synthetic. 19,259 are test-marker UIDs (`faction_test_user` alone = 4,917 entries / 2,156 campaigns); 2,388 are slug fixtures (`arc-natural-*`, `benchmark-1776*`, `byok-streaming-browser-1771*`, `bead-validate-*`).
- **Head-to-head**: jleechan 67,153 vs jleechantest 183,906 = real 26.7% — but across the whole DB real is only 10.6%.

## Caveats

1. `$0.07/entry` is a flat **proxy, not billing truth** — hard dollars still need the BigQuery billing export (`rev-wj9mo`, blocked on a manual GCP toggle). The **10.6% / 89.4% ratio is the robust output**; absolute dollars are illustrative.
2. Per-entry cost is not flat: long real campaigns accumulate history → more tokens/call (200K long-context ~2×), while short test fixtures are cheap. So REAL's *cost* share is likely slightly **above** its 10.6% *entry-count* share — but nowhere near flipping the 9:1 ratio.

## Optimization Implication

Weight test-traffic reduction above real-user-only slimming when prioritizing the `rev-9piwk` epic:
- Keep `testing_mcp`/CI off **billed** Gemini wherever real-services aren't strictly required (`rev-vm10b` cache-off-for-tests).
- Add Firestore **TTL/cleanup** for orphan fixture campaigns (`rev-ny8bx` orphan-cache TTL leak; new `rev-pjtnr` fixture cleanup).
- Real-user system-instruction slimming (`rev-bdeez`) is the secondary lever.
- Feed this apportionment into the hard-dollar proof matrix (`rev-1ozj5`).

## Reusable Method

To attribute cost across a Firestore-backed multi-tenant app: (1) global `collection_group().count()` for the denominator; (2) `list_documents()` − `auth.list_users()` to find orphan tenants; (3) classify orphan IDs by **shape** (real auth-UID regex vs human-readable slug) to separate real-anonymous from synthetic — cheaply, before any per-tenant count.

## Related Concepts

- [[GeminiCostApportionment]]
- [[GeminiContextCacheTTL]]
- [[FirestoreOrphanTenants]]

## Artifacts

`/tmp/worldarchitect.ai/cost-census/{FINAL_ANSWER,summary,named_other,gap_sample}.json`; scripts `count_entries.py`, `diag_sample.py`, `inspect_named_other.py`, `final_classify.py`.

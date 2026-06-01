---
name: gemini-cost-census-test-traffic-dominates-2026-06-01
description: 89.4% of lifetime Gemini story-entry volume is test/CI synthetic, only 10.6% real human play (jleechan); optimize test path first
metadata:
  node_type: memory
  bead: rev-9piwk
  type: project
  originSessionId: 855fb6ab-0543-406d-b8ac-2520432d826a
---

Story-entry cost census (cost proxy $0.07/entry, the `daily_campaign_report.py` constant). Counted every `story` subcollection database-wide with **server-side aggregation** `db.collection_group("story").count()` — no doc downloads.

**Headline:** of 655,037 total story entries, **REAL human play = 69,507 (10.6%, ~$4,865)**, **TEST/CI synthetic = 585,530 (89.4%, ~$40,987)**. jleechan alone 67,153; jleechantest alone 183,906. Head-to-head jleechan-vs-jleechantest = real 26.7%, but across the WHOLE DB real is only 10.6%.

**Where the 61% "missing" entries live:** only 254,787 (39%) sit under the 107 real Firebase-Auth accounts. The other **400,250 (61%)** are under **21,656 orphan UIDs** that have campaigns but NO auth account. Classified every orphan UID by shape:
- **0** are 28-char Firebase hash UIDs → there is **no anonymous real-player traffic**.
- 19,259 are test-marker UIDs (`faction_test_user` alone = 4,917 entries / 2,156 campaigns).
- 2,388 are slug fixtures: `arc-natural-2025…`, `arc-hardened-…`, `benchmark-1776…`, `bead-validate-…`, `branchC-…`, `byok-streaming-browser-1771…` (hundreds of BYOK CI runs).
So the entire orphan bucket is test/CI automation; folding it into TEST is correct (no anonymous-vs-test ambiguity).

**Method note (reusable):** orphan UIDs surface via `db.collection("users").list_documents()` (returns UID docs that have subcollections even when the parent doc / auth account is gone). Auth list (`auth.list_users().iterate_all()`) = only 107. Subtraction (cg_total − auth-bucket sum) gives the orphan total without a slow per-doc scan. Classify real-vs-synthetic by UID shape: real Firebase UIDs match `^[A-Za-z0-9]{28}$`; synthetic fixtures are human-readable slugs.

**Caveats:** (1) $0.07/entry is a flat **proxy, not billing truth** — hard dollars still need BigQuery export [[gemini-cost-epic-rev-9piwk-phase-1-2-roi-roadmap-2026-05-31]] keystone `rev-wj9mo` (blocked on manual GCP toggle). The 10.6%/89.4% **ratio is the robust output**. (2) Per-entry cost is not flat — long jleechan campaigns accumulate history → higher tokens/call (200K long-context 2×); short test fixtures are cheaper. So REAL's *cost* share is likely slightly **above** its 10.6% *entry-count* share, but nowhere near flipping.

**Optimization implication:** the test/CI path is **~9× the volume** of real play. Cost reduction must target test fixtures (BYOK CI fixtures, `arc-*`/`benchmark-*` scenario runs, `faction_test_user`) — add Firestore TTL/cleanup for orphan fixture campaigns + don't let testing_mcp/CI hit billed Gemini (real-services only where required, mock elsewhere), in addition to real-user prompt/system-instruction slimming (`rev-bdeez`).

Artifacts: `/tmp/worldarchitect.ai/cost-census/{FINAL_ANSWER,summary,named_other,gap_sample}.json`; scripts `count_entries.py`, `diag_sample.py`, `inspect_named_other.py`, `final_classify.py`, `inspect_named_other.py`.

**Why:** the cost epic was implicitly assuming real-user optimization (prompt slimming) was the main lever; this census proves test/CI volume dominates 9:1, so test-path cost control is the bigger win and must be a first-class workstream.

**How to apply:** when prioritizing `rev-9piwk` children, weight test-traffic reduction (cache-off-for-tests `rev-vm10b`, orphan-cache TTL `rev-ny8bx`, + a new test-fixture Firestore cleanup) above real-user-only slimming; cite this census as the apportionment input for the hard-dollar proof matrix `rev-1ozj5`.

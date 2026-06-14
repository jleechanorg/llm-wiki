---
name: Gemini cache measurement not done
summary: PR #7348 is the current blocker to honest cache-cost measurement; PR #7263 should not be merged as proven savings until measurement is green.
type: project
bead: rev-9piwk.2.1
---

On 2026-06-08, the Gemini cache/cost work was checked and found not done. PR #7348 is OPEN with CHANGES_REQUESTED and failing gates: BigQuery query polling/pagination in `scripts/reconcile_shared_cache_hard_dollar.py`, a non-streaming explicit-cache reuse `UnboundLocalError` concern, missing PR `## Design Decision`, one `core-mvp-1` failure, and downstream Green Gate failure. PR #7263 is also OPEN/red and should not be treated as proven cost reduction until measurement can show real cache hits plus net-dollar impact.

**Why:** The prior shared-cache evidence showed mechanism-level cache behavior, but not production bill reduction. The next work must land the measurement foundation before merging optimization code as a savings claim.

**How to apply:** When resuming this cost epic, start with bead `rev-9piwk.2.1` and PR #7348, then re-evaluate PR #7263 only after the metrics and billing reconciliation path is green.

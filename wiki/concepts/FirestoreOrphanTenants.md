# FirestoreOrphanTenants

**Created**: 2026-06-01
**Source**: [gemini-cost-census-test-traffic-dominates-2026-06-01](../sources/gemini-cost-census-test-traffic-dominates-2026-06-01.md)

## Definition

An **orphan tenant** is a Firestore `users/{uid}` document path that owns subcollections (e.g. `campaigns/.../story`) but has **no corresponding Firebase Auth account**. They are produced by test fixtures, CI runs, and deleted/expired accounts whose data was never garbage-collected.

## How they surface

```python
auth_uids = {u.uid for u in auth.list_users().iterate_all()}
orphan = [d.id for d in db.collection("users").list_documents()
          if d.id not in auth_uids]
```

`list_documents()` returns UID docs that have subcollections even when the parent doc / auth account is gone — so the orphan set is exactly the user-data tenants with no live login.

## worldarchitect.ai census (2026-06-01)

- **21,656** orphan UIDs holding **400,250** story entries — **61%** of all lifetime entries.
- **0** match the real Firebase UID shape `^[A-Za-z0-9]{28}$` → no anonymous-real users; all orphans are synthetic.
- 19,259 carry test markers (`faction_test_user` alone = 4,917 entries / 2,156 campaigns); 2,388 are slug fixtures (`arc-natural-*`, `benchmark-1776*`, `byok-streaming-browser-1771*`, `bead-validate-*`).

## Why they matter

Orphan tenants accumulate billed storage/compute (and Gemini cost when their campaigns are replayed in CI) with no real user behind them. They are the primary target for **TTL/cleanup** automation. See [[GeminiCostApportionment]].

## Classification rule (reusable)

Separate real-anonymous from synthetic cheaply, before any per-tenant count: real Firebase Auth/anonymous UIDs are 28-char `[A-Za-z0-9]` hashes; synthetic fixtures are human-readable slugs or carry test-marker substrings.

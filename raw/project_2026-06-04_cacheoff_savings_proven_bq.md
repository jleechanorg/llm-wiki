---
name: cache-off savings PROVEN via BQ billing export
description: "BQ export current (0 days stale); cache-off #7215 zeroed the dominant cost SKU (55% of spend) on 2026-06-04 — ~$1.5-3.9K/mo real savings"
metadata:
  node_type: memory
  type: project
  originSessionId: 855fb6ab-0543-406d-b8ac-2520432d826a
---

User asked "are we saving any money yet?" — answered with live BigQuery billing data on 2026-06-04. Answer: YES, just landed.

**BQ export status (rev-wj9mo + rev-wj9mo.1 BOTH CLOSED 2026-06-04):**
- `worldarchitecture-ai.billing_export.gcp_billing_export_v1_011269_D08BDB_79D8F2`, queryable as dev-runner SA (BQ access works; local serviceAccountKey 403s — use gcloud/dev-runner).
- MAX(usage_start_time)=2026-06-04, **0 days stale**, 113,411 rows. The "no rows after 05-13" was a stale 06-01 snapshot; ingestion caught up. Report-parse bug (float-epoch TIMESTAMP) fixed in merged PR #7231 (167772b62687).

**Cache-off (#7215, rev-vm10b) PROVEN working:**
- 7-day SKU split (05-28→06-03): cache-STORAGE $570 (**55%** of $1,027), input-tokens $343, output $72, cached-input $40.
- Cache-storage SKU: $65–$132/day pre-merge → **$0.00 on 2026-06-04** (post-merge, partial day). Cached-input also collapsed $6.81→$0.09.
- Est savings ~$1.5–3.9K/mo; the rev-vm10b $1,690/mo estimate is a FLOOR. NEEDS 3–5 full days (→06-07) to confirm $0 holds (06-04 was partial, total only $0.86).

**Run-rate context:** daily Gemini noisy $11–$308; 7-day avg ~$147/day pre-cache-off. Range incl. $229 (05-09), $308 (05-23), $247 (06-03).

**What's next (post-cache-off ranking):**
1. Confirm cache-off holds 06-04→06-07 (free; daily report auto-tracks export_stale + spend).
2. mock-previews-by-default — flip `scripts/determine-smoke-mode.sh:17-18` workflow_run real→mock OR add MOCK_SERVICES_MODE=true to pr-preview.yml:211. ~$7-17/mo, 2-line, zero risk, but it's a CI routing/coverage decision → confirm before flipping.
3. [[rev-bdeez]] prompt slimming (72K→45K floor, ~37.5% input cut): input-tokens (~$1,470/mo) is the #1 line AFTER cache-off; ~$550/mo but needs prompt surgery + real-LLM regression.
- Orphan cleanup (rev-pjtnr) = Firestore storage only, $0 Gemini. Per-PR CI already $0 Gemini (mocked). 5 scheduled crons all $0 Gemini.

Builds on [[pr]] (#7215 merge+verify). rev-1ozj5 hard-dollar proof matrix now UNBLOCKED + seeded with this data.

**2026-06-04 LIVE RE-PROOF (answer to "where is the proof?"):** Re-ran the read-only BQ query (two independent subagents, identical result) on `gcp_billing_export_v1_011269_D08BDB_79D8F2` as dev-runner SA. The cache-STORAGE SKU isn't just $0.00 — it produces **NO billable row at all** on 06-04 (merge day), while running $75.69/$116.50/$65.17/$132.05 on 05-31→06-03; cached-input collapsed $9.49→$0.086. #7215 merged `a6d2e4e570` @ 2026-06-04T03:50:05Z. Together ~**59% of pre-merge spend** now zeroed. **Honest caveat preserved:** export `latest_day=2026-06-04` (8896 rows, partial day) — 06-05/06-06 not yet exported, so multi-day hold (→~06-07) still pending before declaring permanent.

**Remaining ~40% (real-play input tokens) now issue-backed:**
- [[rev-bdeez]] → GH issue [#7243](https://github.com/jleechanorg/worldarchitect.ai/issues/7243) — system-instruction ~45K floor, #1 input-cost driver post-cache-off. Gated/architectural (game_state schema-doc surgery), quality risk.
- [[rev-6m0pt]] → GH issue [#7244](https://github.com/jleechanorg/worldarchitect.ai/issues/7244) — unbounded story_history growth / ~150K context budget cap. Triple-gated on rev-bdeez slim + rev-1ozj5 proof + rev-sx1dq audit.

Proof report: `~/roadmap/nextsteps-2026-06-04-gemini-cost-cacheoff-proof.md`. Honest bottom line: cheap/safe lever PROVEN solved in billing; the two issues are the only levers left on the remaining ~40%, both gated/architectural with quality risk — which is exactly why they're tracked as issues, not quick wins.

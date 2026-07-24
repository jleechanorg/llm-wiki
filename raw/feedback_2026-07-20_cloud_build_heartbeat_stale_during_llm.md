---
name: cloud-build-heartbeat-stale-during-llm
description: "Cloud Build box heartbeat goes STALE during long LLM ops (≥240s) but the box KEEPS WORKING — do NOT abort on heartbeat-stale; use cloud_build_land_result to fetch results when head_sha advances."
metadata:
  node_type: memory
  type: feedback
  bead: rev-2kmm4
  originSessionId: e95a8a49-51ce-4764-882a-687edb3f1351
---

The Superpowers Cloud Build box's heartbeat (`cloud_build_status` / `cloud_build_check_heartbeat`) goes STALE (≥240s) during long LLM operations, but **the box keeps working**. Aborting a run on heartbeat-stale kills runs that are actually succeeding.

**Why:** 2026-07-20 lean-levelup session — follow-loop was polling heartbeat and aborting runs when it went stale (≥240s). But T7's 4 real-AGY scenarios each take ≥180s = ~12min of blocking LLM time, well over the 240s stale window. The box completes the work; it just doesn't update heartbeat mid-LLM-call. Abort-on-stale killed successful runs. The prior memory entries (`feedback_2026-07-20_super_command_never_fallback_local.md:21` and `feedback_2026-07-20_superpowers_cloud_box_not_openrouter.md:16`) said "heartbeat stale ≥240s = wedged, abort" — that was WRONG and is corrected here.

**Correct follow-loop:**
1. Poll `cloud_build_fetch_status` (NOT heartbeat).
2. Read `tasks_completed` and `head_sha` from the `cloud/status` ref.
3. When `head_sha` advances (the box landed a new commit), call `cloud_build_land_result` to fetch the box's commit directly from the run-scoped git URL.
4. The box's push-back to the work branch does NOT always complete on its own — `land_result` fetches it. Use `land_result` whenever `head_sha` advances.

**Key correction to prior memory:**
- `feedback_2026-07-20_super_command_never_fallback_local.md:21` — REMOVE "If the Cloud Build box itself is down (heartbeat stale ≥240s, wedged), STOP and report ... Abort the wedged run and retry the box." Heartbeat-stale ≠ wedged. Only abort if `cloud_build_fetch_status` shows the run FAILED; do not abort on stale heartbeat alone.
- `feedback_2026-07-20_superpowers_cloud_box_not_openrouter.md:16` — the clause "When the Cloud Build box stalls (heartbeat stale ≥240s)" is misleading; stale heartbeat during LLM ops is normal, not a stall.

**Proof:** run `cb-wa-lu3-20260721011459-e71e87` landed 4 real commits (T7 1161-line real-AGY integration test, T9 646-line caption helper, T9-fix, T11 1128-line UI test) over ~48min, heartbeat advancing throughout, each landed via `cloud_build_land_result`. The box executes T7-T13 of the lean level-up plan faithfully.

**Self-contained writeup:** https://gist.github.com/jleechan2015/4df2938c0bb8c85a9fa98e3da81a739e

Related: [[superpowers-cloud-box-not-openrouter]], [[super-command-never-fallback-local]], [[cloud-build-bastion-host-both-machines]], [[superpowers-cloud-vs-dark-factory]].

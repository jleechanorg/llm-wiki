---
title: "Cloud Build box: heartbeat stale during LLM ops is normal — do NOT abort"
type: source
tags: [cloud-build, superpowers, heartbeat, follow-loop, land-result, correction]
date: 2026-07-20
source_file: raw/feedback_2026-07-20_cloud_build_heartbeat_stale_during_llm.md
---

## Summary
The Superpowers Cloud Build box's heartbeat (`cloud_build_status` / `cloud_build_check_heartbeat`) goes STALE (≥240s) during long LLM operations, but the box KEEPS WORKING. Aborting a run on heartbeat-stale kills runs that are actually succeeding. The correct follow-loop polls `cloud_build_fetch_status`, reads `tasks_completed` / `head_sha` from the `cloud/status` ref, and calls `cloud_build_land_result` to fetch the box's commit directly from the run-scoped git URL when `head_sha` advances.

## Key Claims
- The box's heartbeat goes **stale during long LLM operations** (T7's 4 real-AGY scenarios each ≥180s = ~12min of blocking LLM time, well over the 240s stale window) but the box **keeps working**.
- **Do NOT abort runs on heartbeat-stale alone** — that kills runs that are actually succeeding. Only abort if `cloud_build_fetch_status` shows the run FAILED.
- The heartbeat is a **liveness signal, not a progress signal**. Treating it as a progress signal kills successful runs.
- The correct follow-loop: (1) poll `cloud_build_fetch_status` (NOT heartbeat); (2) read `tasks_completed` and `head_sha` from the `cloud/status` ref; (3) when `head_sha` advances, call `cloud_build_land_result` to fetch the box's commit directly from the run-scoped git URL.
- The box's push-back to the work branch **does not always self-complete**. `land_result` fetches the commit when `head_sha` advances. Use `land_result` whenever `head_sha` advances.
- **CORRECTION to prior source page**: `[[CloudBuildInstallEnrollment]]` Key Claim "Heartbeat stale ≥240s = wedged → abort via cloud_build_mk_abort + cloud_build_push_control, start a fresh run" is WRONG. Stale heartbeat during long LLM ops is normal, not a wedge.

## Key Quotes
> "The heartbeat goes stale DURING long LLM operations but the box KEEPS WORKING. Aborting on heartbeat-stale killed runs that were actually succeeding." — 2026-07-20 lean-levelup session

> "Poll cloud_build_fetch_status, read tasks_completed/head_sha from the cloud/status ref, and when head_sha advances, call cloud_build_land_result to fetch the box's commit directly from the run-scoped git URL. The box's result push-back to the work branch doesn't always complete on its own, but land_result fetches it." — correct follow-loop

> "Run cb-wa-lu3-20260721011459-e71e87 on the Cloud Build box: the box landed 4 real commits (T7 1161-line real-AGY integration test, T9 646-line caption helper, T9-fix, T11 1128-line UI test) over ~48min, heartbeat advancing throughout." — proof

## Connections
- [[CloudBuildInstallEnrollment]] — prior source page; CORRECTED by this page (heartbeat-stale ≠ wedge)
- [[SuperCommand]] — `/super` dispatches to the box; must never fall back to local subagents/OpenRouter
- [[CloudBuildBastionHost]] — both machines are enrolled; the box authenticates the shared key
- [[CloudBuildOrphanSnapshotHandoff]] — unblocks the git-secret guard rejection ("run identity conflict")
- [[CloudBuildHeartbeatStaleDuringLLM]] — the core concept: stale heartbeat is normal during long LLM ops
- [[CloudBuildFollowLoop]] — the correct land-result-based follow-loop pattern

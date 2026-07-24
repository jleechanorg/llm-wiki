---
title: "CloudBuildHeartbeatStaleDuringLLM"
type: concept
tags: [cloud-build, heartbeat, liveness, llm-ops]
date: 2026-07-20
---

# CloudBuildHeartbeatStaleDuringLLM

The Superpowers Cloud Build box's heartbeat (`cloud_build_status` / `cloud_build_check_heartbeat`) goes **stale (≥240s) during long LLM operations**, but the box **keeps working**. The heartbeat is a **liveness signal, not a progress signal** — the box does not update heartbeat mid-LLM-call.

## The anti-pattern (DO NOT DO)
Aborting a run when heartbeat goes stale ≥240s. This kills runs that are actually succeeding. T7's 4 real-AGY scenarios each take ≥180s = ~12min of blocking LLM time, well over the 240s stale window. The box completes the work; it just doesn't heartbeat while in an LLM call.

## The correct pattern
1. Poll `cloud_build_fetch_status` (NOT heartbeat).
2. Read `tasks_completed` and `head_sha` from the `cloud/status` ref.
3. When `head_sha` advances, call `cloud_build_land_result` to fetch the box's commit directly from the run-scoped git URL.
4. Only abort if `cloud_build_fetch_status` shows the run FAILED — never on stale heartbeat alone.

## Proof
Run `cb-wa-lu3-20260721011459-e71e87` landed 4 real commits over ~48min, heartbeat advancing throughout, each landed via `cloud_build_land_result`.

## Related
- [[CloudBuild]] — the box service
- [[CloudBuildFollowLoop]] — the land-result-based follow-loop pattern
- [[CloudBuildInstallEnrollment]] — install/enrollment (corrected: heartbeat-stale ≠ wedge)
- Source: [[feedback-2026-07-20-cloud-build-heartbeat-stale-during-llm]]

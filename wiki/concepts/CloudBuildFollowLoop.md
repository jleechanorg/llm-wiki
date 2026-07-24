---
title: "CloudBuildFollowLoop"
type: concept
tags: [cloud-build, follow-loop, land-result, git-fetch]
date: 2026-07-20
---

# CloudBuildFollowLoop

The correct follow-loop for a Superpowers Cloud Build box run. Replaces the broken "poll heartbeat, abort on stale" pattern.

## Steps
1. **Poll `cloud_build_fetch_status`** (NOT `cloud_build_status` / `cloud_build_check_heartbeat`).
2. **Read `tasks_completed` and `head_sha`** from the `cloud/status` ref.
3. **When `head_sha` advances** (the box landed a new commit), call **`cloud_build_land_result`** to fetch the box's commit directly from the **run-scoped git URL**.
4. The box's push-back to the work branch **does not always self-complete**. `land_result` fetches it. Use `land_result` whenever `head_sha` advances.

## Why this matters
- The box's heartbeat goes stale during long LLM ops (see [[CloudBuildHeartbeatStaleDuringLLM]]) — polling heartbeat and aborting on stale kills successful runs.
- The box's push-back to the work branch doesn't always complete on its own. Without `land_result`, the follow-loop would miss commits the box actually landed.

## Proof
Run `cb-wa-lu3-20260721011459-e71e87` — 4 commits landed via `cloud_build_land_result` over ~48min.

## Related
- [[CloudBuildHeartbeatStaleDuringLLM]] — why heartbeat-polling is wrong
- [[CloudBuild]] — the box service
- [[SuperCommand]] — the slash entry that dispatches to the box
- Source: [[feedback-2026-07-20-cloud-build-heartbeat-stale-during-llm]]

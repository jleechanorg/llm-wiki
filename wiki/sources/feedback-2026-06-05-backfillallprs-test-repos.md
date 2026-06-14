---
title: "Test/Harness Repos MUST Set `backfillAllPRs: false`"
type: source
tags: ["ao-config", "backfillAllPRs", "spawn-storm", "mctrl-test", "feedback"]
date: 2026-06-05
source_file: feedback_2026-06-05_backfillallprs_test_repos.md
---

## Summary
Any AO project that is a test harness / not a production codebase MUST have `backfillAllPRs: false` explicitly set. `mctrl_test` storm: 30+ open PRs → 19+ Gemini workers spawned every 5 min → quota stall → DNS starve → system load 104+.

## Key Claims
- `backfillAllPRs` defaults to `true` — if not set, lifecycle-worker spawns new worker for every open PR every 5 min
- mctrl_test had 30+ open PRs (merge-train test PRs)
- 19 stalled sessions manually killed via `ao stop`
- System load reached 104+; DNS became starved

## Key Quotes
> Test repos, proof-of-concept repos, merge-train harnesses → always `false`

## Connections
- [[AOSpawnGate]] — session count hard cap 20 workers
- [[AgentOrchestrator]] — config

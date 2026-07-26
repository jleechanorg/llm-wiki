---
title: "Runner fleet stale-snapshot false alarms during JIT registration"
type: source
tags: [ezgha, github-actions, runner, jit-registration, snapshot, false-alarm]
date: 2026-07-13
source_file: feedback_2026-07-13_runner_fleet_stale_snapshot_jit_registration.md
---

## Summary

GH API runner status snapshots during ezgha JIT registration bursts show "missing" runners that are actually running on the host. ezgha registers 1-2 runners per 20s cycle; a snapshot mid-burst can capture 4-5 of 10 runners. No fix needed — wait 1-2 minutes for registration to complete.

## Key Claims

- ezgha reaper registers runners in batches of 1-2 per cycle (default 20s tick)
- Mid-burst snapshots can show 50%+ of runners as "missing" while they're actually running
- Cross-check with `docker ps --filter label=ezgha=managed` on the actual host to disambiguate
- Mac and Linux fleets have SEPARATE ezgha configs at different paths (NOT shared)

## Key Quotes

> "The 5 'missing' c-runners (c-4, c-5, c-6, c-7, c-9, c-10) are physically running as fresh Docker containers on jeff-ubuntu but haven't completed GitHub registration yet."

## Connections

- [[EzghaMemoryDetection]] — the ezgha binary that does the JIT registration
- [[RunnerHealthCheck]] — the runner health skill that produces structured reports
- [[CITrimForwardProjections]] — the broader CI trim session in which this lesson emerged

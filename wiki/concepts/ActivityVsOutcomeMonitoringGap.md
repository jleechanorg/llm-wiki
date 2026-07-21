---
title: "Activity vs Outcome Monitoring Gap"
type: concept
tags: [monitoring, testing, ci-cd, observability]
date: 2026-07-19
---

## Definition
A health/monitoring probe that only measures whether a system is *active* (running, busy, listening) rather than whether it is *succeeding* (producing correct outcomes) has a structural blind spot: a system that is 100% active and 100% failing reads identically to one that is fully healthy, under that probe.

## Pattern
This gap recurs at every layer of a system if not explicitly guarded against:
- Layer 1: "is the process running" vs "is it doing anything" (a hung process still shows as `Up`).
- Layer 2: "is it doing something" vs "is what it's doing succeeding" — e.g. a GitHub Actions runner fleet that is fully busy executing jobs but failing every one of them reads as healthy if the monitor only checks container activity states.
- Layer 3 (not yet observed but structurally identical): "did the job succeed" vs "did the job produce the CORRECT result" — a job that reports success while silently corrupting output would pass even outcome-level monitoring.

Each layer requires its own explicit signal; none can be inferred from the layer below it.

## Instances
- [[health-probes-report-activity-not-idleness]] (2026-07-09) — a "Listening for Jobs" grep read a fully-busy ezgha fleet as 0/22 healthy, because a busy runner stops printing the idle-listening log line.
- [[feedback-2026-07-19-shipped-without-real-job-validation]] (2026-07-19) — one layer up: `doctor-runner` measured container activity (EXECUTING/IDLE/DOWN) but never job outcome, so a fleet failing 41% of real jobs for 1-2 days read as fully healthy. The fix (`scripts/job_outcome_monitor.py`) added the missing outcome-level signal.

## Applying this concept
Before trusting any health/monitoring dashboard as evidence of "it works," ask explicitly: what layer does this signal measure, and does a maximally-broken-but-still-running system produce the same reading as a healthy one? If yes, a new signal is needed at the next layer down, not just more instrumentation of the existing one.

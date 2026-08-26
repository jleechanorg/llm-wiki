---
title: "Cloud Run autoscaling"
type: concept
tags: [gcp, cloud-run, autoscaling, concurrency]
---

## Summary

Google Cloud Run scales instances based on how close each instance's actual concurrent request count gets to its configured `containerConcurrency`. If an app-level thread cap (e.g. Gunicorn's `GUNICORN_THREADS`) is set lower than `containerConcurrency`, requests can queue/stall inside the app before Cloud Run's autoscaler ever sees enough concurrent load to trigger scale-out — the pod looks "not full" externally while it's actually saturated internally.

## Key Principle

Thread/concurrency config should never be an artificial ceiling that hides true demand from the autoscaler. Real CPU/memory saturation should be what triggers scale-out, not an app-level cap set conservatively below what the pod could actually handle.

## Connections

- [[feedback-2026-08-24-concurrency-gil-and-real-ceiling-principles]] — the source investigation that established this principle for worldarchitect.ai
- [[python-gil]] — the constraint that limits how much a single-worker pod can actually do even with high thread counts
- [[gemini-fake-latency-mode]] — the test harness stub used to load-test this without real API cost

## Update 2026-08-25 — stochastic operating points

Cloud Run's autoscaler should not be described as having one deterministic
scalar trigger from a handful of runs. In the PR #9330 investigation,
identically configured target loads at 165/171 produced both scale and
no-scale outcomes. The correct operational claim is an observed operating
point: five comparable authenticated target-180 trials all reached two
instances with 27/10,066 load-driver terminal failures, while only two events
had direct concurrency-over-CPU attribution.

Use raw revision-scoped instance counts and driver-labelled recommendations;
separate per-instance concurrency from fleet concurrency; and scope aggressive
settings to dev until memory-heavy request classes are measured.

Source: [[project-2026-08-25-autoscaling-operating-point-and-secret-safe-evidence]].

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

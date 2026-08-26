---
title: "Concurrency ceiling: GIL cores vs thread count, real max drives autoscale"
type: source
tags: [concurrency, gil, cloud-run, autoscaling, load-testing, worldarchitect]
date: 2026-08-24
source_file: raw/feedback_2026-08-24_concurrency_gil_and_real_ceiling_principles.md
---

## Summary

Five durable lessons from a real Cloud Run concurrency-ramp investigation on `jleechanorg/worldarchitect.ai` (2026-08-24): the Python GIL caps real CPU parallelism to `GUNICORN_WORKERS`-many cores regardless of thread count; pods should be configured to run at their real max concurrency so CPU/memory saturation (not an artificial thread cap) drives Cloud Run autoscaling; provider (Gemini) API rate limits are an independent concern from app concurrency config; ramp-test load tests need real experimental hygiene (monotonic step order, fresh non-overlapping data per step) or adversarial review will correctly downgrade the conclusion; and `GEMINI_FAKE_LATENCY_MODE` only stubs the network call, never provider-side rate-limit/quota effects.

## Key Claims

- With `GUNICORN_WORKERS=1`, container CPU% (measured against all allocated vCPUs) can read as a deceptively low ~25-39% while representing an actually-saturated single core — divide by `GUNICORN_WORKERS` cores, not total allocated vCPUs, when judging headroom.
- Operator-stated architectural principle: `GUNICORN_THREADS`/`containerConcurrency` should never be the artificial ceiling that hides true demand from Cloud Run's autoscaler; real resource saturation should trigger scale-out, not an app-level thread cap.
- Gemini API rate limits should be probed independently, with small direct payloads, not conflated with the app's own concurrency ceiling.
- A first-draft ramp-test conclusion ("proven non-resource ceiling, likely GIL, CPU ruled out") was downgraded by a `/wa` multi-model adversarial panel (Gemini REJECT; ChatGPT/Perplexity APPROVE WITH CHANGES) and an independent `/advice` Opus review after they caught non-monotonic step order, mutable shared test data reused across concurrent calls, and a CPU-ruled-out claim that ignored the GIL/core-count point above.
- `GEMINI_FAKE_LATENCY_MODE` stubs only the outbound network call (`time.sleep` + canned response) — it never models provider-side rate limiting or quota effects.

## Key Quotes

> "GUNICORN_WORKERS-many cores cap real GIL parallelism regardless of GUNICORN_THREADS count" — feedback memory, 2026-08-24

## Connections

- [[cloud-run-autoscaling]] — the mechanism this principle is about correctly driving
- [[gemini-fake-latency-mode]] — the stub whose scope this source clarifies
- [[worldarchitect-mobile-latency-investigation]] — the broader investigation this ramp test belongs to
- [[python-gil]] — the underlying constraint behind claim #1

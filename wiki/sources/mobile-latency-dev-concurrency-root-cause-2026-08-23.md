---
title: "Mobile latency root cause: dev test-harness concurrency, not a code regression"
type: source
tags: [worldarchitect.ai, cloud-run, latency, concurrency, gemini]
date: 2026-08-23
source_file: raw/project_2026-08-23_mobile_latency_dev_concurrency_root_cause.md
---

## Summary
An operator-reported "mobile latency worse on dev, especially last night" investigation for
jleechanorg/worldarchitect.ai was resolved via two ultracode Workflow reports plus a sidekick-
driven first-party reproduction. Root cause is NOT a code regression in the 67 commits between
the deployed "stable" commit and origin/main — it is automated test-harness traffic saturating
`mvp-site-app-dev`'s single Cloud Run instance with concurrent LLM calls, stalling
`gemini-3-flash-preview` time-to-first-chunk.

## Key Claims
- 99.9% of the >120s tail on `mvp-site-app-dev` is time-to-first-chunk (TTFC) stall inside a
  single Gemini call, 97.9% of it on `gemini-3-flash-preview`.
- TTFC stall rate scales monotonically with concurrent in-flight LLM calls on the shared instance:
  0.4% at 0 concurrency → 100% at 21+ concurrent calls (single gunicorn worker × 16 threads × one
  `genai.Client` under one GIL).
- 85% of the raw slow-call count comes from two Cloud Scheduler jobs (`wa-daily-level-up-test`,
  `wa-daily-dice-audit-scheduler`) round-robin-hammering dev with ~6 concurrent test campaigns.
- Scale-to-zero was killed as a hypothesis: dev and stable both run `minInstanceCount=1`,
  byte-identical Cloud Run config.
- An initial working theory (PR #8985, a code_execution wall-clock circuit breaker) was falsified
  in minutes by resolving the ACTUAL deployed commit from the Cloud Run revision label
  (`commit-sha-full=`) — the PR was already inside the "fast" stable build.
- The operator's own overnight mobile session (5 real requests, 96–150s each) was directly
  interleaved with harness traffic seconds apart, confirmed via a live BigQuery query.
- A user-disputed finding ("I'm sure I used stable") was resolved as BOTH parties being right,
  about two different campaigns 4 minutes apart — one via a stale bookmark to the raw dev Cloud
  Run URL (slow), one via the real `worldarchitect.ai` domain (genuinely fast) — settled with raw
  `resource.labels.service_name` + `httpRequest.referer` fields, not re-assertion.

## Key Quotes
> "Reproduced. NOT a code regression. The slow tail is 99.9% time-to-first-chunk (TTFC) inside a
> single LLM call, concentrated almost entirely (97.9% of all >120s LLM calls, MEASURED n=138/141,
> 7 days) on one model, gemini-3-flash-preview, whose stall rate rises monotonically with the
> number of concurrent in-flight LLM calls." — mobile-latency-slow-request-hunt-2026-08-23.md

## Connections
- [[worldarchitect.ai]] — the product this investigation covers
- [[Concurrency]] — the core mechanism (Cloud Run instance-level request concurrency saturating a
  single-threaded-per-request-slot LLM client)
- [[LatencyOptimization]] — sibling latency work in this codebase
- [[Gemini]] / [[GeminiProvider]] — `gemini-3-flash-preview` is the stalling model
- [[GeminiApiVariance]] — related: model-specific latency behavior differences

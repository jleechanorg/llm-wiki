---
name: mobile-latency-dev-concurrency-root-cause
description: "MEASURED root cause of intermittent mobile latency on mvp-site-app-dev — test-harness concurrency stalls gemini-3-flash-preview TTFC, not a code regression in the 67 stable..main commits"
metadata: 
  node_type: memory
  type: project
  originSessionId: 508d7000-e1f6-4567-bc7b-7841bf5c91be
  modified: 2026-08-23T18:44:45.451Z
---

**2026-08-23 investigation, jleechanorg/worldarchitect.ai.** Operator reported mobile latency
"worse on dev, especially last night" but "seems ok right now" — an intermittent-tail problem.
Root cause is CONFIRMED, not a code regression, via two independent ultracode Workflow reports
(`~/roadmap/mobile-latency-stable-vs-main-pr-audit-2026-08-23.md`,
`~/roadmap/mobile-latency-slow-request-hunt-2026-08-23.md`) plus a sidekick-driven addendum with
a first-party reproduction (`~/roadmap/mobile-latency-last-night-2026-08-22-23-followup.md`).

**Mechanism (MEASURED, n in the thousands):** 99.9% of the >120s tail on `mvp-site-app-dev` is
time-to-first-chunk (TTFC) inside a single Gemini call. 97.9% of it lands on ONE model,
`gemini-3-flash-preview`. Stall rate scales monotonically with concurrent in-flight LLM calls on
the SAME shared Cloud Run instance (single gunicorn worker x 16 threads x one `genai.Client`
under one GIL): 0.4% stalled at 0 concurrency -> 100% at 21+ concurrent calls. 85% of the raw
slow-call COUNT is an automated `is_test=true` test harness that targets dev only (two Cloud
Scheduler jobs, `wa-daily-level-up-test` + `wa-daily-dice-audit-scheduler`, nominally 07:00
America/New_York but ALSO seen firing a second, overlapping/duplicate execution — two
`wa-daily-level-up-test` job executions ran concurrently 11:41-12:20 UTC on 2026-08-23, same
`client.knative.dev/nonce`, worth its own follow-up). The harness round-robins ~6 concurrent
campaigns continuously.

**Scale-to-zero KILLED as a hypothesis**: dev and stable both run `minInstanceCount=1`,
byte-identical Cloud Run config (`containerConcurrency=16` both).

**First-party reproduction**: the operator's own mobile session (5 real requests, 96-150s each,
2026-08-23 04:59-05:11 AM Pacific) was directly interleaved with the harness — raw BQ
`llm_forensics.llm_payloads` query showed the operator's `is_test=false` calls sandwiched between
harness `is_test=true` calls arriving every 15-20s on the same model/service.

**Reconciled a real operator dispute** ("I'm sure I used stable"): both the operator and the
initial finding were right, about two different campaigns 4 minutes apart in the same overnight
session — one via a stale bookmark to the raw `mvp-site-app-dev-*.a.run.app` URL (slow), one via
`worldarchitect.ai` (fast, genuinely stable). Settled with raw `resource.labels.service_name` +
`httpRequest.referer` from Cloud Run request logs, not by re-asserting the earlier conclusion.

**Falsified along the way**: PR #8985 (code_execution circuit breaker) was already inside the
"stable" snapshot itself (merged 2026-08-17, stable cut 2026-08-19) and its wall-clock breaker
caps latency rather than adding it — dead on two independent grounds. See
[[feedback_2026-08-23_resolve_deployed_commit_from_revision_label]].

**Open next steps (not yet executed, need operator approval — config/live-service changes):**
48h A/B setting `WORLDAI_DEFAULT_GEMINI_MODEL=gemini-3.7-flash` on dev only (env-var override,
zero code change); a same-machine N=1/2/4/8/16 concurrency ablation to settle provider-side
throttling vs app-side GIL/thread contention; isolating the test harness onto its own service so
it stops competing with real dev traffic; a Cloud Run autoscaling/concurrency-tuning investigation
(in progress as of this writing — see STATE.md at
`~/roadmap/worldarchitect.ai/sidekick/worktree_mobile_latency/STATE.md`).

---
name: concurrency-gil-and-real-ceiling-principles
description: GIL caps CPU parallelism to GUNICORN_WORKERS cores regardless of thread count; pods should run at real max concurrency so CPU/memory (not an artificial thread cap) drives autoscaling; provider rate limits are a separate concern from app concurrency
metadata: 
  node_type: memory
  type: feedback
  bead: rev-j7vhr
  originSessionId: 508d7000-e1f6-4567-bc7b-7841bf5c91be
  modified: 2026-08-24T21:29:24.484Z
---

Five durable rules from a real Cloud Run concurrency-ramp investigation (mobile-latency-investigation, jleechanorg/worldarchitect.ai, 2026-08-24).

**1. GIL caps real CPU parallelism to `GUNICORN_WORKERS`-many cores, not `GUNICORN_THREADS`-many.**
With `GUNICORN_WORKERS=1` (gthread model), the Python GIL means only one thread executes Python bytecode at a time — more `GUNICORN_THREADS` add concurrency for I/O-bound waiting (e.g. `time.sleep`, network calls that release the GIL) but do NOT add real parallelism for CPU-bound work (prompt assembly, JSON serialization, string building). Container CPU% metrics are measured against *all allocated vCPUs* (e.g. 4), so a genuinely saturated single core can read as a deceptively low ~25-39% and look like there's headroom when there isn't. **How to apply:** when judging CPU headroom under a single-worker gthread config, divide by `GUNICORN_WORKERS` cores, not total allocated vCPUs. If you need real multi-core parallelism, the lever is `GUNICORN_WORKERS>1` (separate processes, separate GILs), not more threads.

**2. Pods should run at their real max concurrency — thread/concurrency caps should never be the artificial ceiling.**
Operator-stated architectural principle (2026-08-24): `GUNICORN_THREADS`/`containerConcurrency` must be set high enough that they never hide true demand from Cloud Run's autoscaler. Real CPU/memory saturation should be what triggers scale-out, not an app-level thread cap. Don't conservatively under-provision threads based on today's observed peak traffic (e.g. "production never exceeds 24 concurrent, so 64 threads is plenty") — real launch volume should be allowed to hit real resource limits and trigger real autoscaling, not be arbitrarily throttled below what the pod could actually handle. **How to apply:** when setting concurrency config, test toward the real CPU/memory ceiling (with threads set deliberately high so they're not the confound), not toward "comfortably above today's average."

**3. Provider (Gemini) API rate limits are independent of the application's own concurrency config — investigate separately.**
Don't conflate "our app's own thread/concurrency ceiling" with "the Gemini API's own rate-limit ceiling" in the same experiment — they're different bottlenecks with different owners. Probe provider rate limits directly with small, cheap payloads outside the full application code path, not by ramping application-level load through `GEMINI_FAKE_LATENCY_MODE` (which doesn't model provider-side effects at all — see #5) or through the full app stack.

**4. A load-test ramp needs real experimental hygiene or an adversarial review will (rightly) downgrade its conclusion.**
A first-draft ramp-test writeup claimed "a real non-resource ceiling exists between N=200 and N=300, likely GIL contention, CPU ruled out" — a `/wa` multi-model adversarial panel (Gemini REJECT; ChatGPT/Perplexity APPROVE WITH CHANGES) and an independent `/advice` Opus review caught real confounds: non-monotonic step order (56→200→**400→300**, not sequential), a small pool of *mutable shared* campaign documents reused/interleaved across concurrent calls, single trial per level, and CPU-headroom claims that ignored rule #1 above (CPU was NOT actually ruled out once correctly interpreted). The corrected, honestly-scoped claim ("a timeout-rate transition exists; cause unconfirmed") was still a valuable finding — just far weaker than the first draft's overclaim. **How to apply:** design ramp tests with monotonic step order, fresh non-overlapping data per step, and multiple trials per level where feasible, before trusting a "ceiling found" conclusion.

**5. `GEMINI_FAKE_LATENCY_MODE` only stubs the outbound network call — it never models provider-side effects.**
It replaces the real Gemini call with `time.sleep(sampled_duration)` + a canned response; everything else in the request path (Firestore reads, prompt assembly, real Cloud Run container limits) is real. It does **not** simulate Gemini's own rate limiting, quota behavior, or concurrency effects. A fake-Gemini load test characterizes only the app's own local resource ceiling — never the provider's ceiling. Don't let a load test using this mode "sound like" it answered the provider-capacity question; it answers a narrower one.

**Verification:** all 5 points were independently confirmed via real Cloud Monitoring queries (CPU/memory/instance_count REST API), real BQ queries (response-body uniformity proving fake-stub usage, zero real Gemini spend), and a real `/wa` + `/advice` review cycle on PR #9334 (`jleechanorg/worldarchitect.ai`) that forced the correction described in #4.

**References:** PR #9334 (docs, ramp-ceiling findings + corrections), PR #9330 (`GUNICORN_THREADS` 16→64, still open), `roadmap/worldarchitect.ai/pr9334-ramp-preview-firestore-goal-ironclad-2026-08-24.md`.

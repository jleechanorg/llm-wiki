---
name: ablation-confound-check-before-accepting-null-result
description: "Before treating a controlled experiment's null result as a refutation, check whether the experiment's own design actually replicated the conditions under investigation"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 508d7000-e1f6-4567-bc7b-7841bf5c91be
  modified: 2026-08-24T01:47:32.723Z
---

**Rule:** A controlled experiment that returns "no effect found" is not automatically evidence
against the hypothesis — check the experiment's own design for confounds that would have
prevented it from testing the real conditions in the first place, especially when the null result
is the more convenient/simpler-sounding conclusion to accept.

**Why:** 2026-08-23 mobile-latency investigation. Production telemetry strongly correlated
`gemini-3-flash-preview` with concurrency-driven TTFC stalls (0.4% at 0 concurrency -> 63% at
N=11-20 -> 100% at N=21+). A real-API concurrency ablation (N=1,2,4,8,16 against both
`gemini-3-flash-preview` and `gemini-3.7-flash`, real dollar cost, real calls) came back with
ZERO measurable degradation for either model — directly contradicting production, including in
the exact same N=11-20 bucket where production saw 63% stalls. Before accepting this as a
refutation of the leading hypothesis, the design was checked for confounds and TWO were found:
(1) the ablation repeated ONE identical prompt across all calls, triggering Gemini's implicit
prompt caching from the second call onward (confirmed via raw `cached_content_token_count` for
one model — constant 118,682 cached tokens every call; genuinely unknown for the other model
since the temp script was already deleted per cleanup instructions) — production's real harness
rotates through 6+ DIFFERENT campaigns concurrently, so essentially no prompt gets cache-reused
the way 31 repeated-identical-prompt calls would; (2) the ablation ran during a 2-minute isolated
window with a fresh BigQuery check confirming `test_calls=0` ambient load, vs production's
sustained multi-hour concurrent harness bursts. Correct verdict: **INCONCLUSIVE — this specific
design didn't test production's actual conditions — not "refuted, downgrade confidence."** See
[[project_2026-08-23_mobile_latency_dev_concurrency_root_cause]].

**How to apply:** Whenever a controlled experiment is designed to settle a correlational finding,
audit the experiment's fidelity to the real conditions (caching, ambient load, repeated vs varied
inputs, time-of-day/global-demand matching) BEFORE trusting either a positive or null result — a
null result deserves the same skepticism as a positive one, not less, especially when it would be
easier to accept.

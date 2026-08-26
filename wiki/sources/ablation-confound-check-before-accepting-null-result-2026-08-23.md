---
title: "Ablation confound check before accepting a null result"
type: source
tags: [worldarchitect.ai, methodology, ablation, root-cause-analysis]
date: 2026-08-23
source_file: raw/feedback_2026-08-23_ablation_confound_check_before_accepting_null_result.md
---

## Summary
A real-API concurrency ablation for the jleechanorg/worldarchitect.ai mobile-latency
investigation returned a null result (no measurable TTFC degradation for either
`gemini-3-flash-preview` or `gemini-3.7-flash` under a concurrency sweep), directly contradicting
strong production telemetry. Rather than accept the null result as a refutation, the experiment's
own design was audited and found to carry two real confounds — implicit prompt caching and
near-zero ambient background load — that meant it never actually tested production's real
conditions. The correct verdict was "inconclusive," not "refuted."

## Key Claims
- A controlled experiment's null result is not automatically evidence against a hypothesis — the
  experiment's design must be checked for confounds before the result is trusted, especially when
  the null result is the more convenient conclusion.
- Repeating one identical prompt across all calls in an LLM-latency ablation risks triggering
  provider-side implicit prompt caching, which tests a fundamentally different regime (warm-cache
  concurrency) than production's varied-prompt concurrent load.
- An ablation run during a quiet window with zero ambient background traffic does not replicate an
  incident that occurred under sustained real-world concurrent demand.

## Key Quotes
> "Correct verdict: INCONCLUSIVE — this specific design didn't test production's actual conditions
> — not 'refuted, downgrade confidence.'"

## Connections
- [[mobile-latency-dev-concurrency-root-cause-2026-08-23]] — the investigation this ablation was
  part of
- [[Gemini TTFC Ablation]] — an earlier, related ablation methodology in this codebase
- [[Root-Cause-First]] — the broader discipline this confirms: investigate mechanism before
  accepting a convenient-looking result in either direction

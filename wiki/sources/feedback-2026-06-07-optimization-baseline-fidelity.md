---
title: "Optimization baseline fidelity — measure vs deployed config, not off"
type: source
tags: [optimization, baseline-fidelity, ab-test, cost-reduction, deployed-config]
date: 2026-06-07
source_file: raw/feedback_2026-06-07_optimization_baseline_fidelity.md
---

## Summary
Before building ANY cost/latency optimization (cache, batching, model swap, prompt slim, dedup): (1) quantify the addressable slice as % of the measured bill using data you already have; (2) the A/B control arm MUST be the currently-deployed prod config — never 'off'/'uncached'/a hand-picked config; (3) a measurement run in a config that doesn't exist in prod is NOT evidence; (4) gate code-start on a stated $-saved-vs-baseline target written before the first commit; (5) for a fall-through mechanism, compute when it actually fires in prod before building. I built PR #7263 shared system/tools Gemini cache whose only savings land when per-campaign cache is cold (a sliver of prod), excluded 89% test/CI cost center by design, and 'proved' it with 74.6% reduction measured with per-campaign cache forced OFF.

## Key Claims
- Triggers at spec/go-no-go stage of any cost/perf work, and again whenever you write an A/B harness
- If the harness disables a competing prod feature to isolate yours, the resulting number is a preview-path number — do not report as prod savings
- If you cannot write 'saves $X/mo vs the deployed config' before coding, the premise is unvalidated; stop
- Personal case: 43 correctness tasks, 0 marginal-$-vs-baseline tasks for PR #7263; user called it 'useless'; root cause = success metric used isolated control instead of deployed baseline (per-campaign explicit cache ON + Gemini implicit caching)

## Connections
- [[project_2026-06-05_shared_cache_default_on_pr7263]]
- [[project_2026-06-01_gemini_cost_census_test_dominates]]
- [[project_2026-05-31_gemini_cost_phase_roadmap]]
- [[OptimizationBaselineFidelity]]

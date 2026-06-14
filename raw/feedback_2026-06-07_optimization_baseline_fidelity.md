---
name: optimization-baseline-fidelity-measure-vs-deployed-config-not-off
description: "Cost/latency optimizations must be scoped + A/B'd against the currently-deployed prod config; \"better than nothing\" is not \"better than what's shipped\""
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 855fb6ab-0543-406d-b8ac-2520432d826a
---

Before building ANY cost/latency optimization (cache, batching, model swap, prompt slim, dedup): (1) quantify the addressable slice as % of the *measured* bill using data you already have; (2) the A/B control arm MUST be the currently-deployed prod config — never "off"/"uncached"/a hand-picked config; (3) a measurement run in a config that doesn't exist in prod is NOT evidence; (4) gate code-start on a stated $-saved-vs-baseline target written before the first commit; (5) for a fall-through mechanism, compute when it actually fires in prod before building — a fall-through behind an already-warm primary is structurally dead.

**Why:** I built the shared system/tools Gemini cache (PR #7263) whose only savings land when the per-campaign cache is cold (a sliver of prod), excluded the 89% test/CI cost center by design, and "proved" it with a 74.6% reduction measured with the per-campaign cache forced OFF (`ENABLE_EXPLICIT_CACHE=false`) — an isolated control that does not exist in stable prod. 43 correctness tasks, 0 marginal-$-vs-baseline tasks. The mechanism worked; the bill did not drop. The user called it "useless." Root cause: the success metric used an isolated control instead of the deployed baseline (per-campaign explicit cache ON + Gemini implicit caching).

**How to apply:** Triggers at the *spec/go-no-go* stage of any cost/perf work, and again whenever you write an A/B harness. If the harness disables a competing prod feature to isolate yours, the resulting number is a preview-path number — do not report it as prod savings. If you cannot write "saves $X/mo vs the deployed config" before coding, the premise is unvalidated; stop. Codified in `~/.claude/CLAUDE.md` → "Optimization baseline fidelity". Relates to the existing [[project_2026-06-05_shared_cache_default_on_pr7263]] (the cache itself), the census [[project_2026-06-01_gemini_cost_census_test_dominates]] (89% test traffic = the real cost center this missed), and the epic roadmap [[project_2026-05-31_gemini_cost_phase_roadmap]].

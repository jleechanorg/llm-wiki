---
title: "Stop the Gemini dice A/B latency experiment after feasibility"
type: source
tags: [worldarchitect-ai, dice, gemini, code-execution, latency, ab-testing, negative-result]
sources: [pilot-abonly-a35b6d34e4-20260827T193528Z]
last_updated: 2026-08-28
---

## Summary
The 2026-08-27 A/B-only feasibility pilot compared Gemini-managed code execution (Arm A) with the streaming typed server-tool path (Arm B) for dice rolls. It did not prove either arm faster: A was mechanism-compliant 3/3 with median/p95 latency 102.3s/112.6s; B was compliant 2/3 (one retained no-tool ITT miss) with median/p95 84.4s/157.4s. The B median hint is outweighed by worse tail latency, worse reliability, and missing decision-grade cost data from only three pairs. Decision: stop before the fixed 60-pair/120-turn cohort and retain Arm A.

## Key Claims
- High latency was not simply an absent-cache artifact: the three Arm A requests were heavily cached (96.67%, 97.09%, 99.15% of reported prompt tokens) yet provider calls still took 46.93s, 57.07s, and 60.98s (end-to-end 73.4s–112.6s).
- The two compliant Arm B turns each made two sequential provider calls. First calls were uncached and took 31.42s and 87.22s; second calls were only 56.82%/57.53% cached and took 25.49s/23.87s. Prompts were ~201k–240k tokens.
- Cache misses contributed to B's latency (especially the 87.22s first phase), but large prompt processing, long provider generation, two-phase serialization, and additional application overhead remained material even after accounting for cache state.
- Decision: stop before the fixed 60-pair/120-turn cohort; retain Arm A (managed code execution) in production. Do not repeat the pilot, add a C arm, claim a causal winner, or change production routing. Reopen only if a new product reason justifies the spend or a materially different architecture reduces prompt size or eliminates Arm B's second sequential Gemini call.
- PR #9370 may preserve the diagnostic harness but is explicitly not rollout evidence.

## Key Quotes
> "Decision: stop before the fixed 60-pair/120-turn cohort and retain Arm A." — the feasibility pilot's stop decision, driven by inconclusive latency + worse Arm B reliability/tail latency, not by a proven winner.

## Verification
Raw `provider_exchanges.jsonl` and `attempts.jsonl` from `pilot-abonly-a35b6d34e4-20260827T193528Z`; exact-head focused contracts passed 3/3 at `9412465babc44a1a90630c3ba5c338c2c2249bde`. The historical source bundle still contains incomplete publication prose, so this record is deliberately limited to feasibility and the stop decision. Bead: `rev-sle47`.

## Connections
- [[LatencyOptimization]] — second dice/prompt-size latency pilot to hit a negative/inconclusive result; joins the 2026-05-12 story-budget A/B null result under "what does NOT reduce TTFC"
- [[DiceProviderFallback]] — related model-tier dice-execution routing decision
- [[DiceExecutionProtocol]] — the protocol both arms must satisfy (mechanism compliance)
- [[mvp-site-dice]] — core dice rolling implementation under test

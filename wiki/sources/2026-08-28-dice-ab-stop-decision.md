---
title: "Stop the Gemini dice A/B latency experiment after feasibility"
type: source
tags: [dice, latency, gemini, ab-testing, decision]
date: 2026-08-28
source_file: raw/project_2026-08-28_dice_ab_stop_decision.md
sources: []
last_updated: 2026-08-28
---

## Summary
A 2026-08-27 A/B-only feasibility pilot compared Gemini-managed code execution (Arm A) against a streaming typed server-tool path (Arm B) for dice latency. Neither arm proved faster; Arm A was more reliable and had better tail latency. The decision is to stop before funding the full 60-pair/120-turn cohort and retain Arm A in production.

## Key Claims
- Arm A was mechanism-compliant 3/3; Arm B was compliant 2/3 with one retained no-tool ITT miss.
- Arm A median/p95 latency was 102.3s/112.6s; Arm B was 84.4s/157.4s — B's median hint is outweighed by worse tail latency and reliability.
- High latency was not simply a cache-miss artifact: the three A requests were 96.67%, 97.09%, and 99.15% cached by prompt tokens, yet provider calls still took 46.93s–60.98s (end-to-end 73.4s–112.6s).
- B's two compliant turns each made two sequential provider calls; first calls were uncached (31.42s, 87.22s), second calls were only 56.82%/57.53% cached (25.49s, 23.87s). Prompts were ~201k–240k tokens.
- Decision: stop before the fixed 60-pair cohort, retain Arm A, do not add a third arm (C), do not claim a causal winner, and do not change production routing. Reopen only with a new product reason or an architecture change that reduces prompt size or removes B's second sequential Gemini call.
- PR #9370 preserves the diagnostic harness but is explicitly not rollout evidence.

## Key Quotes
> "The apparent B median hint is outweighed by worse tail latency, worse reliability, missing decision-grade cost data, and only three pairs." — decision rationale

> "Cache misses contributed to B's latency, especially the 87.22s first phase, but large prompt processing, long provider generation, two-phase serialization, and additional application overhead remained material." — root-cause caveat against attributing latency to caching alone

## Connections
- [[GeminiApiVariance]] — prior TTFC ablation work established API-call variance as a dominant latency lever; this pilot extends that to a managed-code-execution vs typed-server-tool comparison
- [[CodeExecutionSandboxOverhead]] — related sandbox overhead concept for the code-execution arm
- Bead `rev-sle47`; verification via raw `provider_exchanges.jsonl`/`attempts.jsonl` from `pilot-abonly-a35b6d34e4-20260827T193528Z`; exact-head focused contracts passed 3/3 at `9412465babc44a1a90630c3ba5c338c2c2249bde`

---
title: "Latency Optimization"
type: concept
tags: [performance, latency, user-experience, optimization]
sources: [parallel-dual-pass-optimization]
last_updated: 2026-04-08
---

## Definition
Techniques used to reduce the perceived wait time between user input and system response, critical for maintaining engagement in interactive storytelling applications.

## Optimization Techniques Used

### Parallel Execution
Running independent operations concurrently rather than sequentially

### Progressive Enhancement
Showing initial response immediately while background processing completes

### Graceful Degradation
Falling back to original response if enhancement fails or takes too long

### User Feedback
Subtle indicators showing when enhancement completes ("✨ Story enhanced")

## Metrics
- **Target**: 50% latency reduction (4-10s → 2-5s)
- **Actual**: Achieved through parallel Pass 2 execution

## What Does NOT Reduce TTFC (2026-05-12 empirical finding)

**Prompt token count does NOT drive Gemini TTFC.** A/B experiments on a 2942-turn Alexiel campaign:
- A/B1: 50K story token cap → B/A = 1.31× SLOWER (65.4s vs 49.9s median)
- A/B2: 6K story token cap (93.7% story reduction, 47% total prompt reduction from 314K→168K) → B/A = 1.72× SLOWER (66.6s vs 38.7s)
- Gemini API variance (~34–92s) completely dominates token-count differences
- System instructions alone = ~72K tokens / ~288K chars (70–114K billed), setting a hard floor

**Conclusion:** Abandon prompt-size approaches for TTFC. Next candidates: adaptive model tier, request scheduling, Gemini API tier upgrades, direct Gemini variance root-cause measurement.

**Source:** `project_2026-05-12_story_budget_ab_null_result.md` in Claude memory, `/tmp/story_budget_ab2/` evidence.

## Gemini dice code-execution A/B pilot stopped after feasibility (2026-08-27)

A 3-pair feasibility pilot compared Gemini-managed code execution (Arm A) against a streaming typed server-tool path (Arm B) for dice rolls. Neither arm proved faster:
- Arm A: 3/3 mechanism-compliant, median/p95 102.3s/112.6s, despite 96.67–99.15% cached prompt tokens
- Arm B: 2/3 compliant (one no-tool ITT miss), median/p95 84.4s/157.4s, driven by two sequential provider calls (first call uncached, 31.42s–87.22s)
- Cache misses explain part of Arm B's latency, but large prompt size (~201k–240k tokens), long provider generation, and two-phase serialization remained material

**Conclusion:** Stopped before the fixed 60-pair/120-turn cohort; retained Arm A in production. Do not repeat without a new product reason or an architecture change that reduces prompt size or removes Arm B's second sequential call.

**Source:** [[project-2026-08-28-dice-ab-stop-decision]], bead `rev-sle47`.

## Related Concepts
- [ParallelProcessing](ParallelProcessing.md) — implementation technique
- [DualPassVerification](DualPassVerification.md) — the system being optimized
- [[UserExperience]] — the beneficiary of optimization
- [[DiceProviderFallback]] — related dice-execution routing by model tier

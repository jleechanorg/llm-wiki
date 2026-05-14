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

## Related Concepts
- [[ParallelProcessing]] — implementation technique
- [[DualPassVerification]] — the system being optimized
- [[UserExperience]] — the beneficiary of optimization

---
title: "Gemini API Variance"
type: concept
tags: [gemini, latency, variance, caching]
sources: [gemini-ttfc-ablation-2026-05-12, 2026-08-28-dice-ab-stop-decision]
last_updated: 2026-08-28
---

# GeminiApiVariance

**Created**: 2026-05-12
**Source**: [gemini-ttfc-ablation-2026-05-12](../sources/gemini-ttfc-ablation-2026-05-12.md)

## Definition

Within the 65K-78K prompt token range, Gemini TTFC is dominated by API-level variance (time-of-day load, queue position, compute allocation) rather than payload size differences. Ablation tests AB6/8/9 showed 15-45s TTFC spread with identical token counts, driven entirely by when the test ran.

## Implications

- Below 78K tokens, further token reduction will NOT improve TTFC
- A/B tests must control for time-of-day; N=3-5 is minimum
- TTFC comparisons across different API load periods are unreliable
- The irreducible floor is ~65K tokens (game state + character + world data)

## Related

- [CachedSystemInstructionTokens](CachedSystemInstructionTokens.md) — the lever that gets you below 78K
- [CodeExecutionSandboxOverhead](CodeExecutionSandboxOverhead.md) — deterministic ~6s overhead when sandbox fires

## 2026-08-28 update — cache hit rate does not neutralize variance

[Stop the Gemini dice A/B latency experiment after feasibility](../sources/2026-08-28-dice-ab-stop-decision.md) confirms this holds even at very high cache hit rates: three Arm A (managed code execution) requests were 96.67%–99.15% cached by prompt tokens, yet provider calls still took 46.93s–60.98s. High cache hit rate reduces prompt-processing cost but does not bound provider-call latency — consistent with variance being dominated by API-level factors (load, queue position, compute allocation), not payload/cache state.

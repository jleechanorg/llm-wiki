---
title: "Code Execution Sandbox Overhead"
type: concept
tags: [gemini, latency, code-execution, sandbox]
sources: [gemini-ttfc-ablation-2026-05-12, 2026-08-28-dice-ab-stop-decision]
last_updated: 2026-08-28
---

# CodeExecutionSandboxOverhead

**Created**: 2026-05-12
**Source**: [gemini-ttfc-ablation-2026-05-12](../sources/gemini-ttfc-ablation-2026-05-12.md)

## Definition

Gemini's code execution sandbox (used for provably-fair dice in WorldArchitect.AI) adds ~6s median TTFC overhead plus non-deterministic variance. AB4 showed 28% speedup when code execution was disabled (15,825ms vs 21,924ms). The conditional gate (`in_combat OR encounter_active`) ensures sandbox only fires when needed.

## Gate Design

- `in_combat=True OR encounter_active=True` → sandbox fires (provably-fair dice, ~6s overhead)
- Both False → native_two_phase (server-side dice, no sandbox, fast)
- ZFC-compliant: reads structured game state fields, not keyword-matched user input
- 6 locations in `mvp_service.py`

## Related

- [CachedSystemInstructionTokens](CachedSystemInstructionTokens.md) — larger lever than sandbox overhead
- [GeminiApiVariance](GeminiApiVariance.md) — API variance can exceed sandbox overhead

## 2026-08-28 update — A/B feasibility pilot retains managed code execution

[Stop the Gemini dice A/B latency experiment after feasibility](../sources/2026-08-28-dice-ab-stop-decision.md): a 3-pair pilot compared this managed-code-execution path (Arm A) against a streaming typed server-tool alternative (Arm B) that avoids the sandbox. Arm B did not prove faster or more reliable — it was mechanism-compliant only 2/3 vs A's 3/3, and its two compliant turns needed two sequential provider calls (one always uncached) driving worse p95 (157.4s vs A's 112.6s). Decision: retain the code-execution sandbox path in production; do not fund the larger 60-pair cohort.

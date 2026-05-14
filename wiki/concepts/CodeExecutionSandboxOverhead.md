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

- [[CachedSystemInstructionTokens]] — larger lever than sandbox overhead
- [[GeminiApiVariance]] — API variance can exceed sandbox overhead

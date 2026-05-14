# CachedSystemInstructionTokens

**Created**: 2026-05-12
**Source**: [gemini-ttfc-ablation-2026-05-12](../sources/gemini-ttfc-ablation-2026-05-12.md)

## Definition

Gemini API caches system instruction tokens separately from prompt tokens. Full WorldArchitect.AI prompt files (813KB across 26 files) generate ~200K cached system instruction tokens. These cached tokens are the dominant cost for TTFC — reducing them from 200K to ~1K (by summarizing instruction files to 5KB each) delivers 4x TTFC speedup.

## Key Insight

Moderate token reductions (15-47%) that leave cached system instructions intact produce NO TTFC improvement (AB1/AB2 null results). Only drastic reduction of cached system instruction tokens crosses the threshold where TTFC improves.

## Related

- [[GeminiApiVariance]] — below 78K prompt tokens, API variance dominates
- [[CodeExecutionSandboxOverhead]] — additional ~6s when sandbox fires

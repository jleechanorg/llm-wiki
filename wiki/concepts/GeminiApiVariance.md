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

- [[CachedSystemInstructionTokens]] — the lever that gets you below 78K
- [[CodeExecutionSandboxOverhead]] — deterministic ~6s overhead when sandbox fires

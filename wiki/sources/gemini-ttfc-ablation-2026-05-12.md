# Source: Gemini TTFC Token Floor Ablation (2026-05-12)

**Origin**: `/Users/jleechan/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-05-12_gemini_ttfc_token_floor_ablation.md`
**Branch**: `feature-slim-system-instructions`
**Repo**: `jleechanorg/worldarchitect.ai`

## Summary

Ablation analysis of Gemini TTFC identified the irreducible prompt token floor (~65K from game state) and proved that system instruction file size is the dominant TTFC lever. Story size barely matters (+5K tokens for 24K chars). Within 65-78K tokens, Gemini API variance dominates. Production path: quality-preserving prompt summaries (813KB→5-10KB) + conditional code execution gate.

## Key Metrics

| Arm | prompt_tokens | Median TTFC | vs Control |
|-----|--------------|------------|-----------|
| Control (full 813KB) | 255-352K | 64,070ms | 1.0x |
| Slim + 24K + code exec OFF | ~70K | 15,825ms | 4.05x faster |
| ZERO+ZERO floor | 64,922 | 17,399ms | ~3.7x faster |

## Related Concepts

- [[GeminiApiVariance]] — time-of-day load dominates TTFC within 65-78K token range
- [[CachedSystemInstructionTokens]] — ~200K cached tokens from 813KB prompt files; dominant TTFC lever
- [[CodeExecutionSandboxOverhead]] — ~6s median TTFC overhead for provably-fair dice

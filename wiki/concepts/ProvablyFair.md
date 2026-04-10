---
title: "Provably Fair"
type: concept
tags: [provably-fair, randomness, dice, seed, deterministic, game-mechanics]
sources: []
last_updated: 2026-04-08
---

## Summary
Pattern for generating deterministic random dice rolls that can be independently verified. Uses a seed value that, when combined with the same algorithm, produces reproducible results. Critical for RPG games where players want to verify the GM didn't manipulate rolls.

## Key Aspects
- **Seed Override**: PROVABLY_FAIR_SEED_OVERRIDE injected as first content part
- **Hex Seed**: Actual seed value passed as hex string (e.g., random.seed('abc123'))
- **Content Part Injection**: Seed injected in prompt_contents, NOT system_instruction
- **Compatibility**: Must work alongside caching without breaking cache hits

## Related Pages
- [[TDDTestsCacheProvablyFairCompatibility]] — validates seed + cache compatibility
- [[DDSpellcastingStatsUtilities]] — dice rolling utilities

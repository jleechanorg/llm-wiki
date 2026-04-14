---
title: "DiceAuthenticity"
type: concept
tags: [dice, authenticity, fabrication-detection, llm-fabrication, determinism]
sources: [mvp-site-dice, mvp-site-dice-integrity, mvp-site-dice-provably-fair]
last_updated: 2026-04-14
---

## Summary

The core principle that dice rolls in WorldAI campaigns must be genuine executed rolls, not fabricated by the LLM. DiceAuthenticity enforcement detects when an LLM writes dice notation into narrative text without actually calling the dice tool — a form of hallucination that undermines game integrity.

## Key Claims

### Fabrication Detection
- Fabrication = narrative contains dice notation AND `code_execution_used=False`
- If the LLM writes "rolls a 15" in narrative but did not call the dice tool → fabricated
- Detection patterns: `[dice:...]` tags, `\d+d\d+` notation, contextual "rolls a N" phrases

### Deterministic Mode
- `DICE_SEED=<value>` environment variable enables reproducible RNG for test evidence
- Uses `random.Random(_DICE_SEED_VALUE)` instead of global random
- All rolls logged with campaign context when seed is active

### Provably Fair Scheme
- Server generates cryptographic seed, publishes SHA-256 commitment pre-roll
- Seed injected into Gemini code_execution prompt at runtime
- Players can verify rolls post-game via commitment check

### Narrative Dice Pattern Detection
| Pattern | Example | Detection Rule |
|---------|--------|----------------|
| `[dice:...]` tag | `[dice:1d20+5=17]` | Always detected |
| Dice notation | `1d20+5`, `4d6` | Always detected |
| "rolls a N" | "She rolls a 15" | Only if context contains attack/hit/damage/save/skill/check/initiative/AC/DC |

## Connections

- [[mvp-site-dice]] — core dice rolling implementation
- [[mvp-site-dice-integrity]] — fabrication detection pipeline
- [[mvp-site-dice-provably-fair]] — cryptographic commitment scheme
- [[DiceRollDebugRegression]] — frontend gating bug that bypasses authenticity checks
- [[DiceStrategy]] — strategy selection between code_execution and native_two_phase
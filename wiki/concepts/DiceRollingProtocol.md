---
title: "Dice Rolling Protocol"
type: concept
tags: [dice, protocol, verification, code-execution]
sources: ["dice-values-unknowable-code-execution-protocol"]
last_updated: 2026-04-08
---

Dice rolling protocol requiring all dice values to be obtained through code execution using `random.randint()`. Dice results are quantum-random and do not exist until code generates them.


## Core Principles
- **Code Execution Required**: Must use `random.randint()` or similar RNG function
- **DC Before Roll**: Difficulty class set BEFORE random generation
- **Damage on Hit**: Only roll damage dice if attack hits
- **Verification**: Code is inspected for RNG presence

## Roll Types
- Attack Roll: d20 + modifier vs AC
- Damage Roll: Weapon dice + modifier (only on hit)
- Skill Check: d20 + modifier vs DC (with reasoning)
- Saving Throw: d20 + modifier vs DC (with reasoning)
- Advantage/Disadvantage: Roll twice, use higher/lower
- Opposed: Both sides roll, higher total wins

## Related Concepts
- [[CodeExecutionMode]] — Gemini code execution environment
- [[ProvablyFairDiceRolls]] — cryptographic commitment for verifiable rolls
- [[DCOrderingEnforcement]] — ensures fair DC assignment before rolling

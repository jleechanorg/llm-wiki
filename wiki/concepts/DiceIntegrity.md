---
title: "Dice Integrity"
type: concept
tags: [dice, integrity, security, game-mechanics]
sources: ["tdd-tests-dice-integrity-server-field-security"]
last_updated: 2026-04-08
---

Dice Integrity is the system that ensures dice rolls in the narrative game are authentic, properly executed via code, and cannot be fabricated by the LLM. It validates that code execution was actually used for rolls and flags fabrication attempts.

## Components
- **dice_rolls**: Field containing the actual dice roll results
- **dice_integrity**: Metadata about whether rolls were executed legitimately
- **_server_dice_fabrication_correction**: Server-set field indicating fabrication detection results (must be server-controlled only)

## Related Tests
- [[ProvablyFairDiceRollSystemTests]] — foundational dice system tests
- [[DiceIntegrityModuleTests]] — module-level validation tests
- [[TDDTestsDiceIntegrityServerFieldSecurity]] — security tests for server field spoofing prevention

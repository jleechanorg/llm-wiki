---
title: "Dice Execution Protocol"
type: concept
tags: [dice, mechanics, protocol, worldarchitect]
sources: [game-state-management-protocol]
last_updated: 2026-04-08
---

Dice Execution Protocol mandates that ALL combat attacks MUST roll actual dice using tools — never auto-succeed or fabricate results. The protocol enforces that dice values are unknowable until executed.

**Key Rules**:
- All combat attacks use dice tools
- Never auto-succeed or fake dice results
- DC must be set BEFORE rolling
- Post-roll verification supported via commitment scheme

**Related Concepts**:
- [[DiceValuesAreUnknowable]] — code execution requirement
- [[DiceMechanicsUtilitiesModule]] — logging and detection
- [[DiceStrategySelection]] — provider-based strategy
- [[ProvablyFairDiceRollPrimitives]] — SHA-256 commitment scheme

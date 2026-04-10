---
title: "DiceRollResult"
type: concept
tags: [dice, data-structure, dataclass]
sources: []
last_updated: 2026-04-08
---

## Definition
Python dataclass representing the result of a dice roll with full context including individual dice values, modifiers, totals, and special natural roll flags.

## Attributes
- **notation**: Dice notation string (e.g., "1d20+5")
- **individual_rolls**: List of individual die values rolled
- **modifier**: Numeric modifier applied to the roll
- **total**: Final total after adding modifier
- **natural_20**: Boolean flag for critical success
- **natural_1**: Boolean flag for critical failure

## Usage
Used across the dice mechanics system to capture and propagate roll results with full context for display and logging purposes.

## Related Concepts
- [[Dice & Mechanics Tool Requests Protocol]] — protocol for executing rolls
- [[Dice Values Are Unknowable Code Execution Protocol]] — requires actual RNG execution
- [[Provably Fair Dice Rolls]] — cryptographic verification system

---
title: "Dice Mechanics Utilities Module"
type: source
tags: [dice, mechanics, utilities, logging, testing, fabrication-detection]
source_file: "raw/dice-mechanics-utilities-module.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module providing dice rolling utilities for WorldArchitect.AI game system. Includes logging functions for dice fabrication detection, optional deterministic RNG via DICE_SEED environment variable for reproducible test evidence, and a DiceRollResult dataclass for rich roll context.

## Key Claims
- **Fabrication Detection**: Multiple logging functions detect when dice appear in narrative text without proper tool/code execution evidence
- **Deterministic Testing**: DICE_SEED environment variable enables reproducible dice rolls for test evidence
- **RNG Verification**: log_code_exec_fabrication_violation() detects when code ran but random.randint() was not found
- **Narrative Detection**: log_narrative_dice_fabrication_violation() flags dice patterns in narrative without tool execution

## Key Code Components
- DiceRollResult dataclass with notation, individual_rolls, modifier, total, natural_20/1 flags
- Logging utilities with campaign context for dice integrity checks
- Environment-based deterministic RNG switching (_DICE_RNG)

## Connections
- Related to [[Dice & Mechanics Tool Requests Protocol]] — mandatory tool_requests for dice rolls
- Related to [[Dice Values Are Unknowable Code Execution Protocol]] — requires random.randint() execution
- Related to [[Dice Strategy Selection]] — decides between code_execution and tool_requests
- Part of [[Provably Fair Dice Rolls]] system for verifiable randomness

## Contradictions
- None identified

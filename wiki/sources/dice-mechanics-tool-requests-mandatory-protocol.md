---
title: "Dice & Mechanics — Tool Requests Mandatory Protocol"
type: source
tags: [dice, mechanics, tool-requests, protocol, fair-rolls]
source_file: "raw/dice-mechanics-tool-requests-mandatory-protocol.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Critical protocol requiring all dice rolls to be executed via `tool_requests` array. AI cannot fabricate dice results in narrative text — must request roll via tools (roll_dice, roll_attack, roll_skill_check, roll_saving_throw), wait for server execution, then narrate the result. DC must be set BEFORE the roll is requested.

## Key Claims
- **Mandatory Tool Requests**: All dice outcomes require tool_requests array — AI cannot roll in narrative text
- **DC Pre-Assignment**: DC must be set BEFORE requesting the roll; post-roll DC adjustment is forbidden
- **Server Execution**: Server executes the roll and returns result; AI narrates AFTER receiving result
- **Display Format**: Show roll result clearly: `Action: X | Roll: 1d20+Y = [Z]+Y = Total | Result: Success/Failure`
- **Advantage/Disadvantage**: Display both dice, indicate which was used for final result
- **Opposed Checks**: Show both sides' rolls, modifiers, totals, declare winner

## Key Quotes
> "ABSOLUTE RULE: You CANNOT 'roll' dice in your narrative text. You MUST request rolls via the `tool_requests` array."

> "The server's roll is final."

## Connections
- [[DiceValuesAreUnknowableCodeExecutionProtocol]] — related: both enforce server-side dice execution
- [[DiceStrategySelection]] — related: strategy for executing dice rolls across providers
- [[ProvablyFairDiceRollPrimitives]] — related: cryptographic verification of dice fairness

## Contradictions
- None identified

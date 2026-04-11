---
title: "Dice Tools and Execution Unit Tests"
type: source
tags: [python, testing, dice, execution, unit-tests]
source_file: "raw/test_dice_tools_execution.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests validating the dice roll tool definitions and execution logic in mvp_site.dice module without requiring real LLM calls. Tests cover roll_dice, roll_attack, roll_skill_check, and roll_saving_throw tools.


## Key Claims
- **DICE_ROLL_TOOLS Array**: Contains all required tools (roll_dice, roll_attack, roll_skill_check, roll_saving_throw)
- **execute_dice_tool Function**: Handles roll_dice with notation and purpose parameters
- **DC Reasoning**: roll_skill_check and roll_saving_throw include dc_reasoning in results
- **Auto-fill Behavior**: Automatically fills dc_reasoning when missing from input

## Key Test Cases
- test_dice_roll_tools_exist: Verifies DICE_ROLL_TOOLS array contains all required tools
- test_execute_dice_tool_roll_dice: Validates basic dice notation handling
- test_execute_dice_tool_roll_attack: Validates attack roll with AC and hit detection
- test_execute_dice_tool_roll_skill_check: Validates skill check with DC reasoning
- test_execute_dice_tool_skill_check_with_dc_reasoning: Validates custom DC reasoning including "FBI agent, professionally trained to resist manipulation"
- test_skill_check_auto_fills_dc_reasoning_when_missing: Validates auto-fill behavior for missing DC reasoning

## Connections
- [[dice-logging-functions-unit-tests.md]] — Related dice logging tests in same codebase
- [[provably-fair-dice-roll-tests.md]] — Related provably fair dice roll testing

## Contradictions
- None identified

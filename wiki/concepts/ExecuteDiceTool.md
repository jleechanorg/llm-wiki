---
title: "execute_dice_tool Function"
type: concept
tags: [dice, execution, function, game-mechanics]
sources: [dice-tools-execution-unit-tests]
last_updated: 2026-04-08
---

## Definition
Function that executes a named dice tool with given parameters and returns the roll result.


## Function Signature
```python
execute_dice_tool(tool_name: str, parameters: dict) -> dict
```

## Parameters
- tool_name: One of "roll_dice", "roll_attack", "roll_skill_check", "roll_saving_throw"
- parameters: Dictionary of tool-specific parameters

## Return Value
Dictionary containing roll details including:
- notation/damage_notation: The dice notation used
- rolls: Array of individual die values
- total: Total result after modifiers
- purpose/skill_name: Context for the roll
- success: Boolean for DC-based rolls
- dc_reasoning: Narrative justification for DC (if provided)
- formatted: Human-readable string representation

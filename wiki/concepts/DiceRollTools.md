---
title: "Dice Roll Tools"
type: concept
tags: [dice, tools, game-mechanics, dnd]
sources: [dice-tools-execution-unit-tests]
last_updated: 2026-04-08
---

## Definition
Game mechanics for executing dice rolls in an RPG system. The DICE_ROLL_TOOLS array defines four primary dice rolling tools that can be invoked by LLMs during gameplay.

## Tool Types

### roll_dice
Basic arbitrary dice notation roll (e.g., "2d6+3"). Takes notation and purpose parameters.

### roll_attack
Attack roll against target AC. Returns attack_roll, hit boolean, and damage.

### roll_skill_check
Skill check against Difficulty Class (DC). Includes proficiency, attribute modifier, and dc_reasoning for narrative context.


### roll_saving_throw
Saving throw against DC. Similar to skill check but for saves (e.g., DEX save vs fireball).

## DC Reasoning
The dc_reasoning field provides narrative justification for the DC value, allowing the dice roll to include story-relevant context in the output.

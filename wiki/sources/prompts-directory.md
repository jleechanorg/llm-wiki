---
title: "Prompts Directory"
type: source
tags: [prompt-engineering, system-instructions, dice-strategy, gemini, worldarchitect]
source_file: "raw/prompts_directory.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Directory containing AI system instructions that guide the Gemini AI service in generating responses for WorldArchitect.AI RPG experience. Defines prompt hierarchy from master directive to feature-specific instructions, with conditional loading based on campaign configuration and dice strategy.

## Key Claims
- **Instruction Hierarchy** — Master directive → game state → feature-specific → system reference (D&D SRD)
- **Conditional Loading** — Not all prompts loaded for every request; depends on context (character creation, combat, etc.)
- **Dice Strategy Variants** — Separate dice instructions for tool_requests vs code_execution modes
- **Version Control** — All prompts version-controlled with the codebase, requiring careful review for critical prompts

## Prompt Files
| File | Purpose | Authority Level |
|------|---------|-----------------|
| master_directive.md | Core AI personality, instruction precedence | Highest |
| game_state_instruction.md | JSON format, state management, entity schemas | Second |
| narrative_system_instruction.md | Story generation, writing style, planning blocks | Third |
| mechanics_system_instruction.md | D&D 5e rules, combat, character progression | Third |
| dice_system_instruction.md | Dice rolling for tool_requests mode | Third |
| dice_system_instruction_code_execution.md | Dice rolling for code_execution mode | Third |
| character_template.md | Character creation templates | Third |
| dnd_srd_instruction.md | D&D 5e System Reference Document | Lowest (lookup) |

## Loading Order
1. master_directive.md (establishes authority)
2. game_state_instruction.md (data structure authority)
3. Debug instructions (generated dynamically)
4. Selected prompts (based on campaign config)
5. System reference (D&D SRD for rule lookup)

## Dice Strategy Variants
- **tool_requests**: Uses mandatory tool_requests flow with result display format
- **code_execution**: Uses RNG-only dice generation with code inspection enforcement
- **native**: Native LLM dice rolling
- **native_two_phase**: Two-phase native rolling

## Contradictions
- None identified

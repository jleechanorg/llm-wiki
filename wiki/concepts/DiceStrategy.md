---
title: "Dice Strategy"
type: concept
tags: [dice, prompt-engineering, random-number-generation, game-mechanics]
sources: [prompts-directory]
last_updated: 2026-04-08
---

## Definition
The method by which dice rolls are generated in WorldArchitect.AI, affecting how randomness is introduced into game mechanics.

## Variants
| Strategy | Method | Use Case |
|----------|--------|----------|
| code_execution | RNG via code execution | Gemini code_execution mode |
| tool_requests | Mandatory tool_calls | Gemini tool_requests mode |
| native | Direct LLM generation | Standard LLM prompting |
| native_two_phase | Two-phase LLM generation | Complex scenarios |

## Code Execution Requirements
- RNG-only dice generation (no external random sources)
- Code inspection enforcement
- Required roll formats for attacks, damage, checks, saves

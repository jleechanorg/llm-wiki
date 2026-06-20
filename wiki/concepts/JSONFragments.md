---
title: "JSON Fragments"
type: concept
tags: [token-pattern, structured-data, prompt-engineering]
sources: [narrative-sample-token-analysis]
last_updated: 2026-04-08
---

JSON fragments are partial JSON structures embedded within prompts to provide structured data for game state updates. They allow the LLM to output consistent, parseable state changes.

## Related Patterns
- Often wrapped with [MarkupTokens](MarkupTokens.md) for context
- Used in conjunction with [StateCommands](StateCommands.md) for game state manipulation
- Validated against schema defined in [[GameStateInstructionTokens]]

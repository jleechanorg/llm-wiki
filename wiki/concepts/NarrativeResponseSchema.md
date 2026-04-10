---
title: "NarrativeResponse Schema"
type: concept
tags: [schema, response, god-mode, validation]
sources: []
last_updated: 2026-04-08
---

## Summary
Response schema used in the game backend to represent narrative output from LLM responses. Contains `narrative` (story text) and `god_mode_response` (admin command results) fields.

## Key Components
- `narrative`: Main story text to display to user
- `god_mode_response`: Result of god mode admin commands like "HP set to 50"

## Usage
Used by `_check_god_mode_narrative` to validate that god mode responses don't accidentally include narrative prose when they should only contain admin command results.

## Related
- [[GodModePlaceholderValidation]] — validation logic
- [[GODMode]] — god mode functionality

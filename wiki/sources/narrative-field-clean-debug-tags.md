---
title: "Test Narrative Field Clean — removes debug tags from narratives"
type: source
tags: [python, testing, regression, debug-cleanup, narrative-validation]
source_file: "raw/test_narrative_field_clean.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite ensuring narrative fields never contain debug content. Part of the clean debug/narrative separation initiative to prevent debug tags like `[DEBUG_START]`, `[DEBUG_END]`, `[STATE_UPDATES_PROPOSED]` from leaking into player-facing narrative text.

## Key Claims
- **Debug tags in narrative should fail**: Forbidden patterns include `[DEBUG_START]`, `[DEBUG_END]`, `[DEBUG_STATE_START]`, `[DEBUG_STATE_END]`, `[DEBUG_ROLL_START]`, `[DEBUG_ROLL_END]`, `[STATE_UPDATES_PROPOSED]`, `[END_STATE_UPDATES_PROPOSED]`
- **Clean narrative passes validation**: Narrative field should only contain story text, not debug metadata
- **State updates in correct field**: State updates must be in `state_updates` field, not embedded in narrative

## Key Quotes
> "You attack! [DEBUG_START]Roll: 18[DEBUG_END] You hit!" — Example of BAD response with debug tags in narrative

> "You swing your sword with all your might. The blade connects solidly with the goblin's shield, sending it staggering backward." — Example of GOOD clean narrative

## Connections
- [[Debug Events Export]] — related debug event formatting
- [[LLMResponse Structured Fields]] — where narrative, state_updates, and debug_info fields are defined

## Contradictions
- None identified

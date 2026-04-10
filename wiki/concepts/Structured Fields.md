---
title: "Structured Fields"
type: concept
tags: [ui, structured-response, frontend]
sources: [simple-ui-check-test]
last_updated: 2026-04-08
---

Structured fields are UI elements that display parsed components of AI responses, distinct from the narrative text. The wiki tests verify these four field types:

- **.session-header**: Session metadata and context information
- **.planning-block**: Strategic planning content from think mode
- **.dice-rolls**: Dice roll results and RNG outcomes
- **.resources**: Resource tracking (HP, currency, inventory)

## Related Tests
- [[Simple UI Check Test]] — Verifies all four field types render in the UI
- [[Structured Response Fields Display Frontend Tests]] — Validates appendToStory handles nested debug_info
- [[Structured Response Field Extraction Tests]] — Tests schema field extraction

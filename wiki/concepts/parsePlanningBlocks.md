---
title: "parsePlanningBlocks"
type: concept
tags: [javascript, parsing, planning-block, ui]
sources: [planning-block-ui-buttons-tests]
last_updated: 2026-04-08
---

## Definition
JavaScript function that parses planning block JSON data from the server and renders them as clickable buttons in the game UI.

## Key Functionality
- Parses JSON planning block format with choices array
- Extracts choice id and description for button rendering
- Handles data attributes like `data-choice-text="id: description"`
- Preserves special characters without HTML escaping

## Related
- [[PlanningBlock]] — the data structure being parsed
- [[Frontend JSON Planning Block Tests]] — TDD tests for this function

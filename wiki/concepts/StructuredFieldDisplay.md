---
title: "Structured Field Display"
type: concept
tags: [ui, display, structured-data, frontend]
sources: [playwright-ui-display-test]
last_updated: 2026-04-08
---

## Definition
UI pattern where structured data fields (session-header, planning-block, dice-rolls, resources) are rendered as distinct blocks within story entries.

## Displayed Fields
- **session-header**: Session metadata and context
- **planning-block**: AI planning and reasoning
- **dice-rolls**: Dice roll results and outcomes
- **resources**: Character resource changes (HP, mana, etc.)

## Testing Approach
Playwright tests verify these blocks are present in rendered HTML by checking for CSS class or ID selectors within .story-entry elements.

## Related
- [[Playwright]]
- [[StoryEntryRendering]]

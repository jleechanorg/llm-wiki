---
title: "CSS Pointer Events"
type: concept
tags: [css, user-interface, interaction, click-handling]
sources: ["campaign-click-fix-task-005a"]
last_updated: 2026-04-08
---

## Definition
The CSS `pointer-events` property controls whether an element responds to pointer events (clicks, hovers). Values include `auto` (default, responds to events) and `none` (ignores pointer events, allowing clicks to pass through to elements beneath).

## Usage in This Source
Used to isolate clicks so that buttons within campaign items don't interfere with parent element navigation. The campaign list item sets `pointer-events: none` on child divs, then explicitly re-enables `pointer-events: auto` on the title link and buttons.

## Related Concepts
- [[CSS Transitions]] — smooth visual feedback on user interaction
- [[ZIndex Layering]] — stacking context for overlapping UI elements

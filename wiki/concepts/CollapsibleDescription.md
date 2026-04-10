---
title: "Collapsible Description"
type: concept
tags: [ui-pattern, accessibility, user-interface, javascript]
sources: []
last_updated: 2026-04-08
---

## Description
A UI pattern that allows users to expand or collapse content sections, typically controlled by a toggle button. Implementation uses Bootstrap's collapse plugin with aria-expanded attributes for accessibility.

## Key Characteristics
- Toggle button shows "Collapse" when expanded, "Expand" when collapsed
- Container uses `.collapse.show` class to control visibility
- aria-expanded attribute updates to reflect current state
- Graceful handling when target elements are missing

## Connections
- [[UIUtils]] — provides setupCollapsibleDescription() utility function
- [[Campaign Wizard]] — uses collapsible descriptions for campaign setup forms

## Related Patterns
- Accordion patterns for multiple collapsible sections
- Smooth transitions using CSS transitions on height/display

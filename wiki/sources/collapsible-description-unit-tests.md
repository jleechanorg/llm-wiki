---
title: "Collapsible Description Unit Tests"
type: source
tags: [javascript, testing, unit-tests, ui-components, campaign-wizard, collapsible]
source_file: "raw/test_collapsible_description.js"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite validating collapsible description functionality in both static HTML and campaign wizard implementations. Tests verify toggle button behavior, state management (expanded/collapsed), and graceful handling of missing DOM elements.

## Key Claims
- **Initial State**: Collapsible descriptions initialize in expanded state with aria-expanded="true"
- **Toggle Behavior**: Clicking toggle button correctly alternates between show/hide classes
- **Accessibility**: Proper aria-expanded attribute updates on state changes
- **Wizard Support**: Same functionality works with wizard-prefixed element IDs
- **Error Handling**: Missing DOM elements handled gracefully without throwing errors
- **Campaign Pre-filling**: Dragon Knight campaign type pre-fills description field with narrative template

## Key Test Cases
- Static HTML collapsible initialization and toggle
- Wizard-prefixed element handling
- Missing element tolerance
- Dragon Knight campaign pre-fill behavior

## Connections
- [[Campaign Wizard]] — uses collapsible descriptions for campaign setup
- [[UIUtils]] — utility class providing setupCollapsibleDescription function
- [[Dragon Knight]] — campaign type with narrative pre-filling

## Contradictions
- None identified

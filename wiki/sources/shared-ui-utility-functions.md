---
title: "Shared UI Utility Functions"
type: source
tags: [javascript, ui, utilities, collapsible, dom]
source_file: "raw/shared-ui-utility-functions.js"
sources: []
last_updated: 2026-04-08
---

## Summary
JavaScript module providing shared UI utility functions for WorldArchitect.AI, including collapsible description functionality that toggles container visibility with smooth transitions and accessible button states.

## Key Claims
- **Collapsible Descriptions**: setupCollapsibleDescription manages toggle button and container visibility with CSS class toggling
- **Accessibility**: Sets aria-expanded attribute to communicate state to assistive technologies
- **Bootstrap Icons**: Uses Bootstrap Icons (bi-chevron-up/bi-chevron-down) for visual state indication
- **Module Pattern**: Exports via window.UIUtils namespace for cross-module access

## Key Quotes
> "setupCollapsibleDescription(toggleButtonId, containerElementId)"

## Connections
- [[ThemeManager]] — shares UI utility patterns for DOM manipulation
- [[Bootstrap Icons]] — used for toggle button icons

## Contradictions
- []

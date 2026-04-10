---
title: "Editable Preview Pattern"
type: concept
tags: [ui-pattern, editable-preview, inline-editing]
sources: []
last_updated: 2026-04-08
---

## Summary
A UI pattern where inline elements display a preview of content and transform into edit controls when clicked. Common in settings wizards and configuration interfaces where users need quick visual feedback while editing.

## Key Characteristics
- **Dual State**: Elements have preview mode and edit mode
- **Click Activation**: Clicking preview activates edit mode
- **Exit Triggers**: Enter key saves, Escape cancels, click-outside syncs state
- **Preview Sync**: Form input changes reflected in preview immediately

## Use Cases
- Campaign wizard configuration
- Settings panels
- Inline metadata editing

## Related Patterns
- [[ClickOutsideDetection]]
- [[FormStateSynchronization]]

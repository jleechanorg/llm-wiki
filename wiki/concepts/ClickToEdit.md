---
title: "Click-to-Edit"
type: concept
tags: [interaction-pattern, user-experience, inline-editing]
sources: ["inline-editor-component", "inline-editor-styles"]
last_updated: 2026-04-08
---

## Definition
A user interaction pattern where clickable text elements transform into editable input fields in-place, without navigating to a separate edit page or modal.

## How It Works
1. Element displays as static text with hover indicator
2. User clicks to trigger edit mode
3. Text is replaced with input field and controls
4. Save commits changes, cancel reverts to original

## Related Patterns
- [[KeyboardShortcuts]] — Enter/Escape for save/cancel
- [[ValidationAndErrorHandling]] — input validation with visual feedback
- [[VisualTransitions]] — smooth state changes

---
title: "Loading States"
type: concept
tags: [ui-states, loading, feedback, user-experience]
sources: [inline-editor-styles]
last_updated: 2026-04-08
---

## Definition
Visual indicators that communicate to the user that an operation is in progress, typically using spinners or animated elements.

## Implementation
- `.inline-edit-save .spinner-border-sm` — small Bootstrap-style spinner
- Width/height: 0.75rem for compact display
- Disabled button during save operation prevents double-submit

## UX Purpose
- Provides feedback that save action is processing
- Prevents user confusion during network requests
- Reduces likelihood of duplicate submissions

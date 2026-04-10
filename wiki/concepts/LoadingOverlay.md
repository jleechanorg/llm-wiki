---
title: "Loading Overlay"
type: concept
tags: [ui-pattern, loading-state, user-experience]
sources: ["loading-messages-css-task-005b"]
last_updated: 2026-04-08
---

A full-screen semi-transparent overlay that blocks user interaction while asynchronous operations complete. Implemented with CSS `rgba()` background and optional backdrop blur for visual polish.

## Key Characteristics
- **Blocking**: Prevents clicks on underlying elements during loading
- **Visual Feedback**: Provides context about what operation is in progress
- **Accessibility**: Should include `aria-busy` and meaningful loading messages

## Implementation Patterns
- `position: fixed` with full viewport coverage
- `z-index` above normal content
- Semi-transparent background (typically 0.5-0.9 alpha)
- Optional `backdrop-filter: blur()` for frosted glass effect

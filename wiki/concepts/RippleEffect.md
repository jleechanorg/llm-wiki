---
title: "Ripple Effect"
type: concept
tags: [animation, interaction, css, button]
sources: [enhanced-components-css]
last_updated: 2026-04-08
---

## Summary
Visual feedback animation where a circular wave expands from the click point across a button or interactive element. Implemented via CSS `::before` pseudo-element that scales from center.

## Key Details
- **Trigger**: On click/active state
- **Animation**: Width/height scale from 0 to 300px
- **Styling**: Semi-transparent white circle with transition
- **Pointer Events**: Disabled via `pointer-events: none`

## Connections
- [[EnhancedComponentsCSS]] — implements ripple effect for `.btn-enhanced`
- [[LoadingState]] — related button state animation

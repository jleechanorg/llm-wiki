---
title: "Loading State"
type: concept
tags: [ui-state, animation, feedback, user-experience]
sources: [enhanced-components-css]
last_updated: 2026-04-08
---

## Summary
UI state indicating an operation is in progress. Implemented with spinning animation, disabled pointer events, and reduced opacity to provide visual feedback without blocking interaction.

## Key Details
- **Class**: `.loading`
- **Animation**: `@keyframes spin` — 1 second linear infinite
- **Indicator**: 16px border-radius spinner
- **Behavior**: `pointer-events: none`, `opacity: 0.8`

## Connections
- [[EnhancedComponentsCSS]] — implements loading state for enhanced buttons
- [[RippleEffect]] — related interactive feedback mechanism

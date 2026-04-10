---
title: "Glass Morphism"
type: concept
tags: [visual-effect, css, design-pattern, transparency]
sources: [enhanced-components-css]
last_updated: 2026-04-08
---

## Summary
Design pattern creating frosted glass-like visual effects using semi-transparent backgrounds with background blur. Achieved via `backdrop-filter: blur()` and RGBA color values.

## Key Details
- **CSS Property**: `backdrop-filter: blur(8-12px)`
- **Background**: Semi-transparent (`var(--glass-background)`)
- **Border**: Subtle accent borders on hover
- **Usage**: Cards, buttons, form controls

## Connections
- [[EnhancedComponentsCSS]] — applies glass morphism to cards and buttons
- [[WorldArchitectAiDefaultThemeCssVariables]] — defines glass-related variables

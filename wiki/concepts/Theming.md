---
title: "Theming"
type: concept
tags: [css, design, frontend]
sources: [modern-css-foundation-figma-design-system]
last_updated: 2026-04-08
---

## Definition
Theming is the practice of creating multiple visual appearances for an application by swapping out design tokens (colors, fonts, shadows) while maintaining the same underlying structure.

## Context in this source
The CSS uses attribute-based theming:
```css
:root { /* light theme default */ }
[data-theme='fantasy'] { /* overrides for fantasy theme */ }
```

The fantasy theme overrides 20+ variables to create the Arcane Scholar aesthetic with dark navy-purple palette and gold accents.

## Related concepts
- [[CSSCustomProperties]] — the mechanism enabling theming
- [[DesignTokens]] — the values that change per theme
- [[FantasyThemeArcaneScholar]] — the specific theme implemented

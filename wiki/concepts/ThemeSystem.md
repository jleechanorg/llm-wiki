---
title: "Theme System"
type: concept
tags: [frontend, css, theming, design]
sources: [static-assets-directory]
last_updated: 2026-04-08
---

## Overview
A CSS-based theming system using custom properties (variables) to enable runtime theme switching. WorldArchitect.AI implements 5 themes.

## Theme Structure
```
static/themes/
├── base.css      # Base theme variables
├── light.css     # Light theme
├── dark.css      # Dark theme
├── fantasy.css   # Fantasy theme
└── cyberpunk.css # Cyberpunk theme
```

## Implementation Pattern
- Base CSS custom properties define design tokens
- Theme stylesheets override variables for each variant
- Theme manager (js/theme-manager.js) handles switching logic
- CSS cascade applies themed values automatically

## WorldArchitect Themes
1. **base.css** - Core design tokens (colors, spacing, typography)
2. **light.css** - Default light theme
3. **dark.css** - Dark mode variant
4. **fantasy.css** - Fantasy RPG aesthetic
5. **cyberpunk.css** - Cyberpunk/neon aesthetic

## Related Concepts
- [[Single Page Application]] - Enables smooth theme transitions
- [[CSS Custom Properties]] - Underlying technology for theming
- [[Visual Design System]] - Theme Manager module in js/theme-manager.js

---
title: "Modern CSS Foundation - Figma Design System"
type: source
tags: [css, design-system, figma, frontend, theming]
source_file: "raw/modern-css-foundation-figma-design-system.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Comprehensive CSS design system with design tokens as CSS custom properties. Defines core colors, typography scale, spacing, shadows, and border radius for both light theme (default) and fantasy theme (Arcane Scholar dark navy-purple). Includes glass morphism surfaces, backdrop filters, and animation transitions.

## Key Claims
- **Design tokens as CSS variables**: 80+ custom properties defining colors, typography, spacing, shadows, and animations
- **Dual-theme support**: Light theme default with fantasy theme via `[data-theme='fantasy']` attribute selector
- **Fantasy theme palette**: Deep navy-purple (#0d0f1f) base with gold accents (#d4a843) for the Arcane Scholar aesthetic
- **Elevation system**: Four-tier shadow system (sm, base, elevated, glow) for depth hierarchy
- **Glass morphism**: Translucent surfaces with rgba values for backdrop blur effects

## Key Quotes
> "--glass-background: rgba(255, 255, 255, 0.8);"
> "[data-theme='fantasy'] { --primary: #d4a843; }"

## Connections
- Related to [[FantasyThemeCSSVariables]] — previous Arcane Scholar theme implementation
- Enables [[EnhancedComponentsCSS]] — feature-flag controlled enhancements using these tokens
- Powers [[EmberParticleBackground]] — JavaScript canvas animation gated on fantasy theme

## Contradictions
- None identified

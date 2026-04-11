---
title: "Fantasy Theme CSS Variables"
type: source
tags: [css, theming, fantasy, accessibility]
source_file: "raw/fantasy-theme-css-variables.md"
sources: []
last_updated: 2026-04-08
---

## Summary
CSS custom properties defining the "Arcane Scholar" fantasy theme palette with deep purple-black backgrounds, frosted-glass panel effects, gold accent text, and vivid purple borders/glows. Includes ember canvas background animation and WCAG AA compliance.

## Key Claims
- **Purple-Black Palette**: `--primary-bg: #0e0820`, `--panel-bg: #161a35` creating dark fantasy atmosphere
- **Gold Accents**: `--accent-color: #d4a843` for text and links ensuring readability against dark backgrounds
- **Purple Decorative Elements**: `--purple-glow: #a855f7` for borders, glows, and button backgrounds
- **Frosted Glass Effect**: `backdrop-filter: blur(12px)` on modals and cards
- **Ember Canvas**: JavaScript particle animation with 160 floating embers
- **WCAG Compliance**: 3:1 contrast ratio for non-text elements, lifted text colors for AA compliance

## Key CSS Variables
| Category | Key Variables |
|----------|---------------|
| Backgrounds | `--primary-bg`, `--panel-bg`, `--secondary-bg`, `--navbar-bg` |
| Text | `--text-primary`, `--text-secondary`, `--text-muted` |
| Accent | `--accent-color`, `--accent-color-alpha` |
| Decorative | `--purple-glow`, `--purple-border`, `--border-color` |
| Buttons | `--btn-primary-bg`, `--btn-secondary-bg` |

## Connections
- [[Default Theme CSS Variables]] — contrast with default theme palette
- [[Ember Particle Background]] — JavaScript canvas animation for fantasy theme
- [[Enhanced Components CSS]] — feature-flag controlled UI enhancements

## Contradictions
- None

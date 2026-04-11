---
title: "CSS Variable Bridge for Design System Migration"
type: source
tags: [worldarchitect, css, theming, design-system, backward-compatibility, css-variables]
source_file: "raw/css-variable-bridge.md"
sources: []
last_updated: 2026-04-08
---

## Summary
CSS variable bridge that maps legacy CSS custom properties to new design system tokens, ensuring backward compatibility during WorldArchitect.AI's theming system transition. Maps old variables like `--primary-bg`, `--text-primary`, and `--accent-color` to new design tokens `--background`, `--foreground`, and `--primary`.

## Key Claims
- **Legacy Mapping**: Maps 12+ old CSS variables to new design system tokens including `--primary-bg` → `--background`, `--text-primary` → `--foreground`, `--accent-color` → `--primary`
- **Backward Compatibility**: Allows existing components to continue functioning without modification during the design system migration
- **Fantasy Theme Support**: Includes special adjustments for fantasy theme with white story backgrounds and custom accent overrides
- **Alpha Transparency Support**: Provides alpha variants like `--accent-color-alpha` for overlay and backdrop effects

## Key Quotes
> `--primary-bg: var(--background);` — mapping old variable to new design token

## Connections
- [[WorldArchitect.AI Default Theme CSS Variables]] — the new design system being migrated to
- [[WorldArchitect.AI Frontend Base Template]] — template that uses these variables

## Contradictions
- None identified

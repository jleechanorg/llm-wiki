---
title: "WorldArchitect.AI Default Theme CSS Custom Properties"
type: source
tags: [css, theming, design-system, css-custom-properties, worldarchitect]
source_file: "raw/default-theme-css-variables.md"
sources: []
last_updated: 2026-04-08
---

## Summary
CSS custom properties defining the default theme for WorldArchitect.AI, covering backgrounds, text, accents, borders, panel/character info styling, and button colors. Provides theming infrastructure using native CSS variables for consistent styling across the application.

## Key Claims
- **Background Variables**: Defines primary-bg, secondary-bg, navbar-bg, story-bg, input-bg, hover-bg, and overlay-bg for consistent page section styling
- **Text Color System**: text-primary for main content, text-secondary for subtitles/captions, text-on-accent for text on colored backgrounds
- **Accent Colors**: accent-color primary brand color with alpha variant for overlays
- **Panel Styling**: Dedicated variables for character info panels (stats, equipment, spells) including panel-bg, panel-border, panel-text
- **Badge Styling**: Specialized colors for status badges and spell badges with distinct backgrounds and borders
- **Button Colors**: Complete button palette with primary, secondary, success, and danger variants

## Connections
- [[WorldArchitect.AI Frontend Base Template]] — uses these CSS variables for consistent theming
- [[Modern Component Styles with Bootstrap Compatibility]] — builds on top of these design tokens
- [[CSS Variable Bridge for Design System Migration]] — relates to legacy CSS custom property migration

## Contradictions
- None identified

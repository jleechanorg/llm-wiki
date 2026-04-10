---
title: "FantasyTheme"
type: concept
tags: [css, theme, frontend, theming]
sources: []
last_updated: 2026-04-08
---

## Description
A theme variant for the MVP site that uses CSS selectors like [data-theme='fantasy'] .dice-rolls and [data-theme='fantasy'] .resources to apply styling. Theme overrides via selector-based CSS can be blocked by inline styles on HTML elements, as inline styles have higher specificity than CSS class selectors.

## How It Works
When a theme is active (via data-theme attribute on document), CSS rules like `[data-theme='fantasy'] .resources { background-color: ... }` apply. However, if the HTML element itself has `style="background-color: ..."`, that inline style takes precedence and the theme override becomes dead code.

## Connections
- [[AppJs]] — contains the inline styles that may block this theme's overrides

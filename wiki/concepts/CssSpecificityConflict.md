---
title: "CssSpecificityConflict"
type: concept
tags: [css, frontend, theming, regression]
sources: []
last_updated: 2026-04-08
---

## Description
A CSS conflict pattern where inline styles on HTML elements (e.g., `style="background-color: ..."`) have higher specificity than selector-based CSS rules (e.g., `.resources { ... }` or `[data-theme='fantasy'] .resources { ... }`), causing the selector-based rules to be ignored.

## Why It Matters
Theme systems relying on CSS class or attribute selectors can be rendered ineffective if frontend code sets inline styles on the same elements. This is a common regression in theming implementations.

## Connections
- [[FantasyTheme]] — theme affected by this conflict
- [[AppJs]] — source of inline styles causing the conflict

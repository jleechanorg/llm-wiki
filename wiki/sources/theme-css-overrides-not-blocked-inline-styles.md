---
title: "Theme CSS Overrides Not Blocked by Inline Styles"
type: source
tags: [testing, css, theme, regression, frontend]
source_file: "raw/theme-css-overrides-inline-styles-test.py"
sources: []
last_updated: 2026-04-08
---

## Summary
TDD regression test verifying that fantasy.css theme overrides for .dice-rolls, .resources, .system-warnings, and .planning-block classes are not blocked by inline background-color styles in app.js HTML templates. Inline styles always beat selector-based CSS, making any inline background-color on these classes dead code for theme overrides.

## Key Claims
- **No Inline Background on .resources**: Elements with class="resources" must not carry inline style="...background-color..." which would override [data-theme='fantasy'] .resources CSS rules
- **No Inline Background on .dice-rolls**: Elements with class="dice-rolls" must not have inline background-color in HTML or via style.cssText assignments
- **No Inline Background on .system-warnings**: Elements with class="system-warnings" must not carry inline background-color
- **Theme Override Blockers = Regression**: Any inline background-color on these themed classes effectively disables the fantasy.css overrides, breaking theming functionality

## Key Quotes
> "fantasy.css defines [data-theme='fantasy'] .dice-rolls and .resources overrides, but inline style=\"background-color: ...\" in app.js HTML templates always beat selector-based CSS"

## Connections
- [[FantasyTheme]] — the theme that these overrides are meant to enable
- [[AppJs]] — source file containing the inline styles that block theme overrides

## Contradictions
- None identified — this is new regression guard coverage

---
title: "CSS Variable Definition Validation Tests"
type: source
tags: [python, testing, css, frontend, regression, variables]
source_file: "raw/test_css_variable_definitions.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests that validate every CSS variable (`var(--name)`) usage has a corresponding definition somewhere in the CSS file tree. Catches the class of bug where enhanced-components.css references `--glass-background`, `--shadow-elevated`, etc. without any CSS file actually defining them, causing `background: var(--undefined)` to resolve to `transparent` and silently breaking dropdown menus, cards, and other UI components.

## Key Claims
- **Definition Coverage**: Every `var(--name)` in any CSS file must have a `--name:` definition somewhere
- **Regression Guard**: Prevents theme dropdown from becoming transparent due to undefined `--glass-background`
- **Enhanced Components Protection**: Specifically guards enhanced-components.css as the usual offender
- **External Prefix Allowlist**: Variables starting with `--bs-` (Bootstrap) are exempted as they're runtime-defined

## Key Quotes
> "Catches the class of bug where enhanced-components.css (or any other file) references --glass-background, --shadow-elevated, etc. but no CSS file actually defines them — causing `background: var(--undefined)` to resolve to `transparent` and silently breaking dropdown menus, cards, etc."

## Connections
- [[EnhancedComponentsCSS]] — the usual offender file that references undefined variables
- [[ThemeDropdown]] — component that breaks when --glass-background is undefined
- [[GlobalsCSS]] — file that should define --glass-background in :root

## Contradictions
- None identified

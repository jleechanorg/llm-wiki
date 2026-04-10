---
title: "CSS Custom Properties"
type: concept
tags: [css, variables, frontend, styling]
sources: [css-variable-definition-validation-tests]
last_updated: 2026-04-08
---

## Definition
CSS Custom Properties (also known as CSS variables) are user-defined values that can be reused throughout a stylesheet using the `var()` syntax. They follow the pattern `--variable-name: value;` for definition and `var(--variable-name)` for usage.

## Usage Pattern
- **Definition**: `--glass-background: rgba(255, 255, 255, 0.1);`
- **Usage**: `background: var(--glass-background);`
- **With fallback**: `background: var(--undefined, #ffffff);`

## Common Issues
- **Undefined variables**: Using `var(--name)` without a definition resolves to `transparent`
- **Scope leakage**: Variables defined in one component may unintentionally affect others
- **Cascade confusion**: Inheritance and specificity can cause unexpected behavior

## Related Concepts
- [[CSSVariableDefinitionValidation]] — testing for undefined variable usage
- [[ThemeSystem]] — CSS variables enable theme switching via data-theme attributes

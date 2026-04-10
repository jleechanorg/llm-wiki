---
title: "Feature Flags"
type: concept
tags: [feature-management, configuration, toggle]
sources: []
last_updated: 2026-04-08
---

## Description
Configuration mechanism enabling runtime toggling of features without code changes. Implemented via localStorage in InterfaceManager to control progressive enhancement.

## InterfaceManager Implementation
```javascript
localStorage.setItem('feature_interactive_features', 'true');
localStorage.getItem('feature_interactive_features') === 'true' // check
```

## Key Flags Used
- `feature_animations` — toggle CSS animations and animation helpers
- `feature_enhanced_components` — toggle ripple effects, glass morphism, loading states
- `feature_interactive_features` — toggle Campaign Wizard, modals, search/filter
- `interface_mode` — overall interface mode (modern/legacy)

## Related Concepts
- [[ProgressiveEnhancement]] — features build on each other sequentially
- [[LocalStorage]] — persistence layer for flag values

## Examples
- [[EnhancedComponentsCSS]] — feature-flag controlled CSS
- [[InterfaceManagerModernInterfaceSystem]] — implements feature flag system

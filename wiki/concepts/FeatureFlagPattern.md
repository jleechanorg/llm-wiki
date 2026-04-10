---
title: "Feature Flag Pattern"
type: concept
tags: [feature-toggle, configuration, software-pattern]
sources: ["component-enhancer-bootstrap-component-enhancement"]
last_updated: 2026-04-08
---

## Description
A software design pattern that allows code execution paths to be toggled without deploying new code. Typically controlled via configuration or localStorage, enabling gradual rollout or A/B testing of features.

## Example from Component Enhancer
```javascript
isFeatureEnabled() {
  return localStorage.getItem('feature_enhanced_components') === 'true';
}
```

## Related Entities
- [[ComponentEnhancer]]

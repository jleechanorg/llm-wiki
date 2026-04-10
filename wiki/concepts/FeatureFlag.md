---
title: "Feature Flag"
type: concept
tags: [configuration, conditional, rollout, toggles]
sources: [enhanced-components-css]
last_updated: 2026-04-08
---

## Summary
Configuration mechanism that enables or disables functionality without deploying new code. Feature flags allow gradual rollouts, A/B testing, and quick disable capability.

## Key Details
- **Flag Name**: `feature_enhanced_components`
- **Purpose**: Toggle enhanced CSS effects on/off
- **Pattern**: Conditional loading or CSS class application

## Connections
- [[EnhancedComponentsCSS]] — controlled by `feature_enhanced_components` flag
- [[ComponentEnhancerBootstrapComponentEnhancement]] — also feature-flag controlled

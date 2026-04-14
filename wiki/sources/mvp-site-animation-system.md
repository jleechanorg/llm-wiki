---
title: "test_animation_system.py"
type: source
tags: [testing, animation, css, javascript, accessibility]
date: 2026-04-14
source_file: raw/mvp_site_all/test_animation_system.py
---

## Summary
Tests for the animation system including CSS animations, JavaScript helpers, performance properties, and accessibility features. Verifies animation duration variables, keyframe definitions, JavaScript API methods, and reduced motion support.

## Key Claims
- Animation CSS defines duration variables: fast (0.15s), normal (0.3s), slow (0.5s)
- Essential keyframes: btn-spin, slideInUp, typeWriter, pulse
- JavaScript API includes showView, showLoading, hideLoading, addButtonLoading, removeButtonLoading, showStoryLoading, hideStoryLoading
- File size limits: CSS under 50KB, JavaScript under 30KB
- Accessibility: prefers-reduced-motion media query disables animations
- theme-bootstrap.js handles FOUC prevention (not legacy theme-init.js)
- No hardcoded data-theme on html tag (set dynamically)

## Key Quotes
> "Should respect user motion preferences with prefers-reduced-motion"

## Connections
- [[mvp-site-frontend-v1]] — Frontend animation assets
- [[mvp-site-theme-manager]] — Theme system with FOUC prevention

## Contradictions
- None identified in test file
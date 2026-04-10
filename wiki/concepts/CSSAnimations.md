---
title: "CSS Animations"
type: concept
tags: [css, animations, frontend, performance]
sources: [animation-system-tests-milestone-3]
last_updated: 2026-04-08
---

CSS Animations are a way to animate transitions between CSS property values over time. In WorldArchitect, animations are used for:

- Button hover states
- View transitions (between auth, dashboard, new-campaign, game views)
- Theme transitions with smooth opacity changes
- GPU-accelerated transforms for performance

## Key Properties

- **will-change**: Optimizes rendering by hinting which properties will change
- **transform**: GPU-accelerated property for translation, rotation, scaling
- **opacity**: GPU-accelerated property for fade effects
- **transition**: Shorthand for animating property changes over time

## Accessibility

CSS Animations support the `prefers-reduced-motion` media query to respect user system preferences for reduced motion effects.

## Related

- [[JavaScriptAnimation]] — complementary JavaScript animation techniques
- [[PerformanceOptimization]] — frontend performance best practices
- [[ReducedMotionAccessibility]] — accessibility support for motion-sensitive users

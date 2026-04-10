---
title: "Performance Optimization"
type: concept
tags: [performance, css, frontend, optimization]
sources: [animation-system-tests-milestone-3]
last_updated: 2026-04-08
---

Performance Optimization in frontend development involves techniques to ensure smooth, responsive user interfaces. For CSS animations, key optimizations include:

## GPU Acceleration

Certain CSS properties are GPU-accelerated (composited on the GPU rather than CPU):
- **transform**: translation, rotation, scaling
- **opacity**: visibility changes
- **filter**: blur, color adjustments

## will-change Property

The `will-change` CSS property hints to the browser which properties are expected to change, allowing the browser to optimize rendering accordingly.

## Best Practices

- Animate only GPU-accelerated properties when possible
- Use `will-change` sparingly and only when needed
- Respect `prefers-reduced-motion` for accessibility
- Avoid animating layout-triggering properties (width, height, top, left)

## Related

- [[CSSAnimations]] — applies performance optimization techniques
- [[ReducedMotionAccessibility]] — accessibility considerations in performance

---
title: "CSS Animations"
type: concept
tags: [css, animations, keyframes, web-development]
sources: [story-pagination-styles]
last_updated: 2026-04-08
---

## Definition
CSS animations allow you to create multi-step animations using `@keyframes` rules, enabling complex sequences that go beyond simple transitions.

## Usage in Source
Three keyframe animations defined:
- **fadeInUp**: Entry loading animation — fades in while sliding up (opacity 0→1, translateY 10px→0)
- **pulse**: Pagination info update — opacity pulse for visual feedback
- **slideDown**: Error message entry — slides down from above while fading in

## Related Concepts
- [[CSS Transitions]] — simpler, single-state animations
- [[Scroll-Behavior]] — smooth scrolling in content containers
- [[Loading States]] — UI patterns for async content loading

## See Also
- MDN: CSS animations
- [[Story Pagination Styles]] — practical application example

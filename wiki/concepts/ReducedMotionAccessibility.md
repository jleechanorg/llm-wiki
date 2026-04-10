---
title: "Reduced Motion Accessibility"
type: concept
tags: [accessibility, css, user-preferences, frontend]
sources: [animation-system-tests-milestone-3]
last_updated: 2026-04-08
---

Reduced Motion Accessibility is a CSS media query feature that detects when a user has requested reduced motion effects at the operating system level. This supports users with vestibular disorders, motion sensitivity, or who prefer less animation.


## Implementation


```css
@media (prefers-reduced-motion: reduce) {
  /* Disable or reduce animations */
  * {
    animation: none !important;
    transition: none !important;
  }
}
```

## Browser Support

Supported in all modern browsers. The setting is exposed via the `prefers-reduced-motion` media query.

## Best Practices

- Always test animation implementations with reduced motion enabled
- Provide meaningful alternatives (instant transitions vs animated)
- Test on actual devices with accessibility settings enabled

## Related

- [[CSSAnimations]] — animations that should respect reduced motion
- [[JavaScriptAnimation]] — JavaScript animations that should respect reduced motion
- [[PerformanceOptimization]] — performance considerations including accessibility

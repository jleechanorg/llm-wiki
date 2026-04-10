---
title: "Easing Functions"
type: concept
tags: [animation, math, motion, timing]
sources: [animation-helpers-frontend-transitions]
last_updated: 2026-04-08
---

Easing functions define how animation values change over time, creating natural-looking motion.

## Cubic Bezier Easing
- Default: `cubic-bezier(0.4, 0, 0.2, 1)` — Material Design standard
- Bounce: `cubic-bezier(0.68, -0.55, 0.265, 1.55)` — overshoot effect
- Ease-out: `cubic-bezier(0, 0, 0.2, 1)` — decelerate to stop

## Related Concepts
- [[AnimationSystem]] — uses easing functions
- [[KeyframeAnimations]] — often paired with easing

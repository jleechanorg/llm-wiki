---
title: "RequestAnimationFrame"
type: concept
tags: [animation, browser-api, performance]
sources: []
last_updated: 2026-04-08
---

Browser API for efficient animation loops. Requests a callback to be invoked before the next repaint, providing smooth animations synced to the display refresh rate.

## Usage Pattern
```javascript
function animate(timestamp) {
  animationId = requestAnimationFrame(animate);
  // render frame
}
animationId = requestAnimationFrame(animate);
```

## Best Practices
- Cancel with cancelAnimationFrame() when stopping
- Track timestamp for frame-rate throttling
- Handle tab visibility to pause when hidden

## Related Concepts
- [[CanvasAnimation]] — common use case
- [[FrameIntervalThrottling]] — performance optimization
- [[TabVisibilityAPI]] — background pause optimization

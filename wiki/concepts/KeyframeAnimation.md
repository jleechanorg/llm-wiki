---
title: "Keyframe Animation"
type: concept
tags: [css, animation, motion-design]
sources: ["loading-messages-css-task-005b"]
last_updated: 2026-04-08
---

CSS animation technique using `@keyframes` rules to define intermediate states between start and end positions. Used in loading messages to create smooth fade-in/fade-out transitions for rotating message display.

## FadeInOut Pattern
```css
@keyframes fadeInOut {
  0%, 100% { opacity: 0; }
  20%, 80% { opacity: 1; }
}
```

This creates a message that fades in quickly (0→20%), stays visible (20%→80%), then fades out (80%→100%).

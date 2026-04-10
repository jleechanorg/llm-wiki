---
title: "Message Rotation"
type: concept
tags: [pattern, animation, javascript, ui]
sources: ["loading-messages-javascript-class"]
last_updated: 2026-04-08
---

A UI pattern where messages cycle through automatically at fixed intervals. Implemented using setInterval to change the currentIndex modulo the message array length, creating a circular buffer effect.

## Implementation
```javascript
this.currentInterval = setInterval(() => {
  this.currentIndex = (this.currentIndex + 1) % messages.length;
  this.showMessage(element, messages[this.currentIndex]);
}, 3000);
```

## Use Cases
- Loading states where static text feels unresponsive
- Multi-step wizard progress indicators
- Animated feedback during async operations

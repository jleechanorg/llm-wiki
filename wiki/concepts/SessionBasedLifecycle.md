---
title: "Session-Based Lifecycle"
type: concept
tags: [patterns, lifecycle, state-management]
sources: ["avatar-crop-js-drag-to-reposition-avatar-upload.md"]
last_updated: 2026-04-08
---

## Definition
A pattern where async operations include a session identifier that is incremented on each new request. Callbacks check the session ID against current state before proceeding, ensuring only the latest operation's result is used.

## Usage in Avatar Crop
```javascript
let _sessionId = 0;
function show(container, imageSrc, opts) {
    const mySession = ++_sessionId; // Capture current session
    img.onload = () => {
        if (mySession !== _sessionId) return; // Guard: stale callback
        // ... process image
    };
}
```

## Why It Works
- Simple integer increment requires no complex state tracking
- Single comparison at callback time determines relevance
- Handles rapid successive calls (e.g., user changes image quickly)

## Related Concepts
- [[Race Condition Prevention]] — broader category of handling concurrent operations
- [[Callback Guard]] — pattern of validating callback applicability

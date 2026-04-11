---
title: "Avatar Crop UI — Drag-to-Reposition Avatar Upload"
type: source
tags: [javascript, frontend, ui, avatar, image-processing, crop]
source_file: "raw/avatar-crop-js-drag-to-reposition-avatar-upload.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Shared drag-to-reposition crop UI for avatar uploads in WorldArchitect.AI frontend. Provides a circular crop interface where users drag the image to reposition it within a circular viewport before final cropping via Canvas API. Handles session-based lifecycle management to prevent stale callbacks and supports both data URLs and standard image URLs.

## Key Claims
- **Circular Crop UI**: Creates a 50% border-radius container forming a circular viewport for avatar display
- **Drag-to-Reposition**: Pointer event handlers (pointerdown/move/up) enable smooth image repositioning within bounds
- **Session-Based Guard**: Incrementing `_sessionId` prevents stale img.onload callbacks when show() is called multiple times
- **Canvas API Cropping**: Uses hidden canvas element to extract cropped region based on current offset and zone size
- **Auto-Cleanup**: Destroy method removes event listeners and resets state; new show() auto-destroys previous session

## Key Code Components
- `show(container, imageSrc, opts)`: Initialize crop UI in container element with optional size (default 280px)
- `_doCrop(img, offsetX, offsetY, zoneSize, drawW, drawH)`: Canvas-based cropping extraction
- `getCroppedFile()`: Returns the cropped File object after repositioning
- `destroy()`: Cleanup method removing event listeners and resetting state

## Connections
- [[WorldArchitect]] — frontend utility for avatar upload feature
- [[Bootstrap]] — tooltip integration mentioned in other sources
- [[Firebase Authentication]] — user profile context for avatar uploads

## Contradictions
- None identified

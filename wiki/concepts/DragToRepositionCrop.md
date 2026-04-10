---
title: "Drag-to-Reposition Crop"
type: concept
tags: [ui-pattern, crop, interaction]
sources: ["avatar-crop-js-drag-to-reposition-avatar-upload.md"]
last_updated: 2026-04-08
---

## Definition
A UI pattern where users drag an image within a fixed viewport to select the desired crop region. The image moves while the viewport remains stationary.

## Usage in Avatar Crop
- User sees circular viewport with image inside
- Drag gesture moves image position relative to viewport
- Bounded dragging prevents image from leaving viewport entirely
- Final crop extracts region visible through viewport

## Related Patterns
- [[Image Cropping]] — broader concept of extracting sub-regions
- [[Pointer Events]] — unified mouse/touch handling
- [[Session-Based Lifecycle]] — guarding against stale callbacks

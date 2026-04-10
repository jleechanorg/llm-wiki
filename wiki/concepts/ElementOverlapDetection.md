---
title: "Element Overlap Detection"
type: concept
tags: [ui-testing, layout, debugging]
sources: []
last_updated: 2026-04-08
---

## Definition
Algorithm that identifies when two or more DOM elements occupy the same screen space, excluding valid parent-child containment relationships.

## Implementation Pattern
1. Get bounding rectangles for all target elements
2. Check geometric intersection using: `!(rect1.right < rect2.left || rect1.left > rect2.right || rect1.bottom < rect2.top || rect1.top > rect2.bottom)`
3. Filter out parent-child relationships using `.contains()`
4. Highlight violations with colored borders

## Why It Matters
Overlapping elements cause usability issues: buttons that can't be clicked, text that can't be read, modal overlays that don't properly cover content.

## Related Concepts
- [[VisualValidation]] — broader testing category
- [[ZIndexManagement]] — CSS property that often causes overlap issues

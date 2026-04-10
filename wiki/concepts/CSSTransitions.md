---
title: "CSS Transitions"
type: concept
tags: [css, animation, transitions, micro-interactions]
sources: [inline-editor-styles]
last_updated: 2026-04-08
---

## Definition
CSS transitions enable smooth property changes over a specified duration. Used in inline editor styles for hover effects and error message animations.

## Usage in This Source
- `transition: background-color 0.2s ease, box-shadow 0.2s ease` — for hover states
- `transition: opacity 0.2s ease` — for edit indicator emoji
- `animation: fadeIn 0.3s ease-in-out` — for error message appearance
- `animation: slideIn 0.2s ease-out` — for input container entrance

## Properties
- `transition` — smooth property changes
- `animation` — keyframe-based animations
- `@keyframes` — defines animation frames

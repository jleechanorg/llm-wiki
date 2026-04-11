---
title: "Ember Particle Background"
type: source
tags: [javascript, particle-system, canvas, animation, visual-effects, theming]
source_file: "raw/ember-particle-background.js"
sources: []
last_updated: 2026-04-08
---

## Summary
JavaScript module implementing an ember particle background effect for the WorldArchitect.AI fantasy theme. Ported from the worldai_claw AmbientBackground component. Renders floating ember particles with realistic physics, gradient backgrounds, and accessibility support via prefers-reduced-motion.

## Key Claims
- **Particle Count**: 160 embers rendered simultaneously
- **Color Palette**: Six warm ember colors (#ff6820, #ff9500, #ffc000, #ff4000, #e05000, #ff7c10)
- **Physics**: Random horizontal drift and upward velocity with alpha decay
- **FPS Target**: 30 FPS with frame interval throttling
- **Accessibility**: Respects prefers-reduced-motion, renders static gradient when enabled
- **Theme Gating**: Only activates when data-theme="fantasy"
- **Tab Visibility**: Pauses animation when tab is hidden for performance

## Technical Details
- **Rendering**: HTML5 Canvas 2D context with radial particle drawing
- **Background**: Linear gradient from #0a0a12 (top) to #1a1520 (bottom)
- **Particle Properties**: x, y position; r radius (0.3-2.1); vx/vy velocity; a alpha; da alpha decay; c color
- **Event Handling**: Resize events rebuild gradient and reinitialize particles; visibilitychange pauses animation

## Connections
- [[WorldArchitect.AI]] — main project this component belongs to
- [[WorldAI]] — organization that developed the ember effect
- [[DefaultThemeCSSVariables]] — CSS theming system that controls data-theme attribute

## Contradictions
- None

---
title: "Sprite Animation System"
type: concept
tags: [game-development, graphics, animation]
sources: ["animal-movement-web-game-technical-design-document"]
last_updated: 2026-04-07
---

Sprite-based animation system with the following specifications:

- **Frame dimensions**: 64x64px per frame
- **Layout**: 8 frames per row for walk cycle
- **States**: Idle, walk, run, special action (8 total)
- **Directions**: 4-directional (North, East, South, West)

**SpriteAnimator class** provides playAnimation(name, loop), setDirection(angle), updateFrame(deltaTime). Performance optimizations include sprite atlasing (single texture per animal), frame skipping (adaptive FPS), culling (only animate visible sprites), and memory pooling.

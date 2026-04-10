---
title: "Game Engine Architecture"
type: concept
tags: [game-development, engine, architecture]
sources: ["animal-movement-web-game-technical-design-document"]
last_updated: 2026-04-07
---

Core engine structure for the Animal Movement Web Game comprising six main components:

- **InputManager**: Handles keyboard/mouse events and input mapping
- **AnimationEngine**: Sprite management and frame playback
- **PhysicsSystem**: Collision detection and movement physics
- **RenderEngine**: Canvas drawing and rendering pipeline
- **AudioManager**: Sound effects and ambient audio
- **GameStateManager**: Scene management and progression

Uses RequestAnimationFrame for the game loop with object pooling for performance optimization.

---
title: "Collision Detection"
type: concept
tags: [game-development, physics, collision]
sources: ["animal-movement-web-game-technical-design-document"]
last_updated: 2026-04-07
---

AABB (Axis-Aligned Bounding Box) collision detection system:

- **checkTileCollision()**: Sprite vs tile map collision
- **checkSpriteCollision()**: Sprite-to-sprite collision
- **resolveCollision()**: Collision response and resolution

CollisionManager class handles all collision detection. Uses bounding boxes for efficient broad-phase detection before detailed physics resolution.

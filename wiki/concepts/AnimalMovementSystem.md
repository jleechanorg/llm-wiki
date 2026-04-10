---
title: "Animal Movement System"
type: concept
tags: [game-development, movement, physics]
sources: ["animal-movement-web-game-technical-design-document"]
last_updated: 2026-04-07
---

Movement system with three specialized classes extending a base AnimalMovement:

- **AnimalMovement** (base): speed, agility, specialAbility properties, update(), applyPhysics()
- **QuadrupedMovement**: Land-based movement for animals like Lion, Rabbit
- **AerialMovement**: Flight capabilities for Eagle with air resistance
- **AquaticMovement**: Underwater movement for Dolphin with breathing mechanics

Physics implementation uses velocity-based movement (Position += velocity * deltaTime) with acceleration curves for realistic start/stop. Environmental resistance varies by terrain.

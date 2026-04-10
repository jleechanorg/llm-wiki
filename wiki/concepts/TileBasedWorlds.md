---
title: "Tile-Based Worlds"
type: concept
tags: [game-development, world-building, tilemap]
sources: ["animal-movement-web-game-technical-design-document"]
last_updated: 2026-04-07
---

Tile-based world system using a 32x32px grid with multiple layers:

- **Background layer**: Static terrain and decoration
- **Collision layer**: Solid objects and barriers
- **Foreground layer**: Overlays and objects in front of sprites
- **Effects layer**: Weather, particles, and visual effects

**Format**: JSON map data with tile indices supporting chunk streaming (load/unload as player moves). Environmental effects include water zones (slow land animals, speed aquatic), elevation changes (affect movement speed), weather (rain reduces visibility), and day/night cycles affecting animal behavior.

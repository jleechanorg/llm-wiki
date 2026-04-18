---
title: "SpriteSheet.ts - Procedural Sprite Rendering"
type: source
tags: [game-engine, sprites, pixel-art, procedural-generation, canvas-rendering]
date: 2026-04-16
source_file: packages/game-engine/src/renderer/SpriteSheet.ts
---

## Summary
SpriteSheet.ts provides procedural pixel art sprite generation and canvas-based sprite sheet rendering for the WorldAI Claw game engine. It includes a `SpriteSheetRenderer` class for animation playback and a `ProceduralSpriteGenerator` class that creates sprites programmatically without AI dependencies.

## Key Claims
- Procedural sprite generation uses `OffscreenCanvas` for pixel-by-pixel drawing
- Supports multiple animation frames with configurable timing and looping
- Directional sprites (north/south/east/west) with flipX support
- Sprite sheets can be loaded from base64 or URL sources
- Character sprites include configurable body colors, accessories (helmet, sword), and skin tones

## Key Quotes
> "Procedural sprite generation for when AI generation is not available" — ProceduralSpriteGenerator docstring

> "Creates pixel art sprites programmatically" — ProceduralSpriteGenerator purpose

## Connections
- [[sprite-generator-service]] — LLM-based alternative that generates sprites via Grok API
- [[SpriteGenerationSystem]] — Both are part of the dual sprite system
- [[ChronoTriggerStyleSpriteSheets]] — Style inspiration for both systems
- [[16BitSNESStyleSpriteRendering]] — Target rendering style

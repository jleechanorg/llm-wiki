# SpriteSheet.ts

**Type:** Procedural Sprite System  
**Location:** `packages/game-engine/src/renderer/SpriteSheet.ts`  
**Role:** Canvas-based sprite rendering and procedural pixel art generation

## Overview

SpriteSheet.ts is the client-side sprite rendering system in the WorldAI Claw game engine. It provides two main capabilities:

1. **SpriteSheetRenderer** - Renders animated sprites from sprite sheets on HTML5 Canvas
2. **ProceduralSpriteGenerator** - Creates pixel art sprites programmatically without AI

## Components

### SpriteSheetRenderer
- Loads sprite sheets from base64 or URL sources
- Supports frame-based animation with timing and looping
- Direction variants with horizontal flipping
- Scale support for resolution-independent rendering
- Sprite caching via Map data structure

### ProceduralSpriteGenerator
- Uses `OffscreenCanvas` for pixel-by-pixel drawing
- Generates character sprites with configurable:
  - Body color, accent color, skin color
  - Accessories (helmet, sword)
  - Direction (north/south/east/west)
- Creates walk cycle frames
- Converts frames to sprite sheet format

## Use Cases

- Fallback sprite generation when LLM API is unavailable
- Simple character sprites without external dependencies
- Client-side rendering for game engine
- Development/testing without API credentials

## Relationship to Other Systems

- Complements [[sprite-generator-service]] as the procedural alternative
- Both feed into the [[SpriteGenerationSystem]]
- Produces sprites in [[16BitSNESStyleSpriteRendering]] format
- Aligned with [[ChronoTriggerStyleSpriteSheets]] aesthetic

## Technical Details

- **Canvas API:** Uses HTML5 CanvasRenderingContext2D for rendering
- **Image Format:** Supports base64 data URLs and standard image sources
- **Animation:** Frame-index calculation based on elapsed time
- **Pixel Control:** Direct ImageData manipulation for procedural generation

## Tags
#sprite-system #procedural #canvas-rendering #game-engine #fallback

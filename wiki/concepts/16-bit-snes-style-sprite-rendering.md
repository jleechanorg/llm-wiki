# 16-bit SNES-Style Sprite Rendering

**Type:** Rendering Style  
**Inspiration:** Chrono Trigger, Final Fantasy 6, Earthbound  
**Implementation:** [[spritesheet-ts]]

## Overview

16-bit SNES-style sprite rendering refers to pixel art graphics rendered at the quality level of Super Nintendo Entertainment System games. This style is characterized by chunky pixels, limited color palettes, and smooth animations.

## Characteristics

### Pixel Density
- Game pixels rendered at 4x scale (16px game = 64px display)
- Sharp edges, no anti-aliasing or smoothing
- Visible individual pixels

### Color Palette
- Limited to 16-32 colors per sprite
- Bold, saturated colors
- No gradients within shapes
- Hard-edge shadows

### Rendering
- 1-2 pixel dark outlines (#1a1a2e or similar)
- Clear pixel-level detail
- Centered sprites facing viewer
- Expression in 2-3 pixel eyes

### Animation
- 4-8 frames per animation
- 200ms per frame timing
- Clear pose differences between frames
- Smooth loops

## Implementation in WorldAI Claw

### SpriteSheet.ts Rendering

```typescript
// Frame-based animation timing
const frameDuration = animation.durationMs / animation.frames.length;
const frameIndex = Math.floor(elapsedTimeMs / frameDuration) % animation.frames.length;

// Drawing with scaling
context.drawImage(
  spriteSheet.imageData,
  frame.x, frame.y, frame.width, frame.height,
  x * scale, y * scale,
  frame.width * scale, frame.height * scale
);
```

### Sprite Dimensions
| Size | Game Pixels | Display (4x) |
|------|-------------|--------------|
| tiny | 16x16 | 64x64 |
| small | 24x32 | 96x128 |
| medium | 32x48 | 128x192 |
| large | 48x64 | 192x256 |

## Related Concepts

- [[ChronoTriggerStyleSpriteSheets]] - Specific inspiration
- [[SpriteGenerationSystem]] - Production system
- [[sprite-generator-service]] - LLM generation of this style
- [[spritesheet-ts]] - Rendering implementation

## Tag
#rendering-style #pixel-art #snes #retro-gaming #canvas

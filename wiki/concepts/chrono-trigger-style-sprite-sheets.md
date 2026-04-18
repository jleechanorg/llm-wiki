# Chrono Trigger Style Sprite Sheets

**Type:** Art Style  
**Source:** [[sprite-generator-service]]  
**Inspiration:** Chrono Trigger (1995 SNES RPG)

## Overview

Chrono Trigger-style sprite sheets refer to pixel art created in the aesthetic of Square's classic 1995 SNES RPG. This style is the target for both the LLM-based [[sprite-generator-service]] and serves as inspiration for the [[spritesheet-ts]] procedural generation.

## Visual Characteristics

### Sprite Design
- Heroic character poses with personality
- Distinct silhouette per character class
- Visible equipment/weapons
- Expressive faces despite low resolution

### Animation Frames
Typical animation sheet layout:
```
[Frame 1][Frame 2][Frame 3][Frame 4][Frame 5][Frame 6]
```

Animation types:
- **idle** - Subtle breathing/ready stance
- **walk** - 4-frame walk cycle
- **attack** - Weapon swing or spell cast
- **magic** - Glow effect + pose change
- **hurt** - Recoil pose
- **death** - Collapse animation

### Color Usage

Pre-defined palettes in [[sprite-generator-service]]:

| Class | Primary Colors | Special |
|-------|---------------|---------|
| Knight | #1a1a2e, #16213e, #0f3460 | Metal gold (#ffd700) |
| Mage | #1a1a2e, #4a148c, #e040fb | Magic cyan (#00bcd4) |
| Rogue | #2d3436, #636e72, #dfe6e9 | Bright accents |
| Beast | #6c5ce7, #a29bfe | Fur browns |

### Direction System
- South-facing: default, sprite faces down
- North-facing: sprite faces up
- East/West: sprite faces side
- West sprites may use flipX for efficiency

## Sprite Sheet Format

### Layout
- Frames arranged horizontally
- Each frame: 16-48 game pixels wide
- Consistent height per direction
- Transparent background (PNG)

### Example Structure
```
┌────┬────┬────┬────┐
│ 1  │ 2  │ 3  │ 4  │  ← Walk cycle (south)
├────┼────┼────┼────┤
│ 5  │ 6  │ 7  │ 8  │  ← Walk cycle (west)
└────┴────┴────┴────┘
```

## System Prompt for LLM Generation

The [[sprite-generator-service]] uses detailed prompts:

> "CHRONO TRIGGER PIXEL ART STYLE (SNES 16-bit era):
> - Sharp pixel edges, NO anti-aliasing or smoothing
> - Limited palette: 16-32 colors max per sprite
> - Bold outlines: 1-2 pixels, dark color
> - Character sprites: centered, facing viewer for south direction
> - Smooth animation frames with clear pose differences"

## Relationship to Other Concepts

- [[16BitSNESStyleSpriteRendering]] - Technical rendering
- [[SpriteGenerationSystem]] - Production system
- [[spritesheet-ts]] - Procedural fallback
- [[GrokImageAPIIntegrationForGameAssets]] - API used for generation

## Tag
#art-style #chronotrigger #pixel-art #jrpg #sprite-sheet

# Sprite Generation System

**Type:** Game Asset Generation  
**Components:** [[spritesheet-ts]], [[sprite-generator-service]]  
**Style Target:** [[ChronoTriggerStyleSpriteSheets]], [[16BitSNESStyleSpriteRendering]]

## Overview

The WorldAI Claw sprite generation system is a dual-approach architecture that provides two methods for generating game sprites:

1. **LLM-Based Generation** (primary) - [[sprite-generator-service]] uses Grok image API
2. **Procedural Generation** (fallback) - [[spritesheet-ts]] creates sprites programmatically

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Sprite Generation System               │
├─────────────────────────┬───────────────────────────────┤
│   LLM-Based (Primary)   │    Procedural (Fallback)      │
├─────────────────────────┼───────────────────────────────┤
│ spriteGenerator.ts     │ SpriteSheet.ts                │
│ Grok API (x.ai)         │ OffscreenCanvas               │
│ High quality, creative  │ Simple, deterministic         │
│ Requires API key        │ No external dependencies      │
│ Slower (network)        │ Fast (local)                  │
│ Cached results          │ Always fresh                  │
└─────────────────────────┴───────────────────────────────┘
```

## Use Cases

| Scenario | Recommended System |
|----------|-------------------|
| Character sprites with unique designs | [[sprite-generator-service]] |
| Environment tiles, simple objects | [[sprite-generator-service]] |
| API unavailable / offline | [[spritesheet-ts]] |
| Development without credentials | [[spritesheet-ts]] |
| Quick prototyping | [[spritesheet-ts]] |

## Key Differences

| Aspect | LLM-Based | Procedural |
|--------|-----------|------------|
| **Quality** | High, artistic | Simple, basic |
| **Variety** | Unlimited | Limited patterns |
| **Consistency** | Prompt-dependent | Always consistent |
| **Speed** | Network latency | Instant |
| **Cost** | API calls | Free |
| **Customization** | Rich descriptions | Code parameters |

## Animation Support

Both systems support:
- Multiple animation frames
- Frame timing and looping
- Directional variants (north/south/east/west)
- Scaling for different resolutions

## SpriteSheetRenderer

The rendering pipeline uses [[16BitSNESStyleSpriteRendering]]:
- Canvas 2D API for drawing
- Sprite sheet layout: frames arranged horizontally
- Time-based frame selection
- Horizontal flip for direction variants
- Scale parameter for resolution independence

## Tag
#sprite-system #dual-approach #grok-api #procedural #fallback

# spriteGenerator.ts (Grokmage LLM Sprite Service)

**Type:** LLM-Powered Sprite Generation Service  
**Location:** `packages/backend/src/services/spriteGenerator.ts`  
**Role:** Generates Chrono Trigger-style 16-bit sprites via Grok image API

## Overview

The spriteGenerator.ts service is a backend component that generates high-quality 16-bit pixel art sprites using the Grok image generation API (x.ai). It produces Chrono Trigger-level sprite sheets with animations, directional variants, and consistent color palettes.

## API Integration

- **Endpoint:** `https://api.x.ai/v1/images/generations`
- **Model:** `grok-imagine-image`
- **Auth:** Uses `AI_UNIV_GROK_KEY` environment variable
- **Pattern:** Follows worldai_claw CLAUDE.md gateway pattern (not direct OpenAI keys)

## Features

### Character Types
- Knight (armored warrior)
- Mage (mystical spellcaster)
- Rogue (shadow warrior)
- Beast (creature or companion)
- Boss (intimidating enemy)
- NPC (village person)

### Animation Types
- idle, walk, attack, magic, hurt, death

### Sprite Configurations
| Size | Dimensions | Scale | Frames | Directions |
|------|-----------|-------|--------|------------|
| tiny | 16x16 | 4x | 4 | 4 |
| small | 24x32 | 4x | 4 | 4 |
| medium | 32x48 | 4x | 6 | 4 |
| large | 48x64 | 4x | 8 | 4 |

### Color Palettes
Pre-defined palettes inspired by Chrono Trigger SNES sprites:
- Knight: dark blues with red accents
- Mage: purples with cyan magic effects
- Rogue: grays with bright accent colors
- Beast: earth tones with expressive eye colors

## Caching
- In-memory cache prevents redundant API calls
- Cache key based on request + config JSON
- Singleton pattern for service instance

## Additional Generation Methods
- `generateTile()` - Environment tiles (floor, wall, door, chest, etc.)
- `generatePortrait()` - Character portraits (64x64 game pixels)

## Relationship to Other Systems

- Provides LLM-generated sprites vs [[spritesheet-ts]] procedural fallback
- Part of [[SpriteGenerationSystem]] dual approach
- Produces [[ChronoTriggerStyleSpriteSheets]] output
- Uses [[GrokImageAPIIntegrationForGameAssets]] for API calls

## Tags
#sprite-system #llm-generation #grok-api #backend-service #chronotrigger

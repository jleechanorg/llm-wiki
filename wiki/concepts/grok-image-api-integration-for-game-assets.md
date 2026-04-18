# Grok Image API Integration for Game Assets

**Type:** API Integration  
**Provider:** x.ai (Grok)  
**Implementation:** [[sprite-generator-service]]

## Overview

The WorldAI Claw backend uses the Grok image generation API to create 16-bit style game sprites. This integration follows the worldai_claw CLAUDE.md pattern of using a gateway environment variable rather than direct API keys.

## API Details

### Endpoint
```
POST https://api.x.ai/v1/images/generations
```

### Authentication
- Uses `AI_UNIV_GROK_KEY` environment variable
- Falls back to `GROK_API_KEY` if not set
- Follows worldai_claw gateway pattern

### Model
- **Model Name:** `grok-imagine-image`
- **Purpose:** High-quality image generation

### Request Format
```typescript
const response = await fetch('https://api.x.ai/v1/images/generations', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${GROK_API_KEY}`,
  },
  body: JSON.stringify({
    model: 'grok-imagine-image',
    prompt: prompt,
    n: 1,
  }),
});
```

### Response Format
```typescript
const data = await response.json() as { data: Array<{ url: string }> };
const imageUrl = data.data[0]?.url;
```

## Response Handling

### URL vs Base64
- Grok API returns a **URL** (not base64 directly)
- Image must be downloaded separately
- Converted to base64 for sprite sheet storage

```typescript
// Download and convert to base64
const imageResponse = await fetch(imageUrl);
const imageBuffer = Buffer.from(await imageResponse.arrayBuffer());
const imageData = imageBuffer.toString('base64');
```

## Integration Architecture

```
┌─────────────────────┐
│ SpriteGenerator     │
│ (spriteGenerator.ts)│
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐     ┌─────────────────┐
│ buildSpritePrompt() │────▶│ LLM Prompt      │
└─────────────────────┘     └────────┬────────┘
                                     │
                                     ▼
┌─────────────────────┐     ┌─────────────────┐
│ Style Guide +       │◀────│ Grok API        │
│ Metadata            │     │ (api.x.ai)      │
└──────────┬──────────┘     └────────┬────────┘
           │                          │
           │                          ▼
           │                 ┌─────────────────┐
           └─────────────────▶│ Image URL       │
                             └────────┬────────┘
                                      │
                                      ▼
                             ┌─────────────────┐
                             │ Download +     │
                             │ Convert to     │
                             │ Base64         │
                             └─────────────────┘
```

## Sprite Generation Prompt

Prompts are structured to ensure:
1. **Style specification:** Chrono Trigger SNES aesthetic
2. **Technical specs:** Dimensions, scale, format
3. **Character details:** Type, colors, animation
4. **Output format:** Sprite sheet layout

## Caching Strategy

Results are cached to minimize API calls:
- Cache key: JSON of request + config
- In-memory Map storage
- Singleton service instance

## Error Handling

- Missing API key: Throws `AI_UNIV_GROK_KEY not configured`
- API errors: Returns full error with status code
- No image returned: Throws `No image URL returned`

## Fallback

When Grok API is unavailable, [[spritesheet-ts]] provides procedural sprite generation as a fallback.

## Relationship to Other Concepts

- [[sprite-generator-service]] - Main implementation
- [[SpriteGenerationSystem]] - System context
- [[ChronoTriggerStyleSpriteSheets]] - Target style
- [[16BitSNESStyleSpriteRendering]] - Technical style

## Tag
#api-integration #grok #xai #image-generation #game-assets

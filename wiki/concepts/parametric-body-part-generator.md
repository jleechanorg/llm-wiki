---
title: "Parametric Body Part Generator"
type: concept
tags: [sprite-generation, procedural, pixel-art, body-parts, failed-approach]
date: 2026-04-28
last_updated: 2026-05-01
---

## Summary

ParametricBodyPartGenerator.ts generates pixel art body parts (head, body, arms, legs) from configuration parameters. Uses silhouette masks + shading patterns + detail layers to produce consistent, varied body parts without external AI. Output: 32×32 scaled parts (2× from base 16×16/16×24/12×24 sizes).

**Status as of 2026-05-01**: The TypeScript implementation exists as a concept only. The LLM-based body-parts pipeline (using Pollinations + Grok) **failed** — generated parts had washed-out colors, misaligned anatomy, and didn't form coherent characters when composited.

## Interface

```typescript
interface BodyPartParams {
  partType: 'head' | 'body' | 'arms' | 'legs';
  bodyType: 'slim' | 'medium' | 'stocky' | 'muscular';
  skinTone: string;
  equipmentStyle: 'naked' | 'light' | 'medium' | 'heavy';
  palette: { primary: string; secondary: string; accent: string };
}
```

## Pipeline

1. Generate silhouette mask (oval for head, rounded rect for body, etc.)
2. Fill silhouette with skin/equipment colors + shading
3. Add detail features (eyes, armor plates, clothing lines)
4. Nearest-neighbor upscale to 2× (base→scaled sizes)

## Base/Scaled Sizes

| Part | Base | Scaled (2×) |
|------|------|-------------|
| head | 16×16 | 32×32 |
| body | 16×24 | 32×48 |
| arms | 12×24 | 24×48 |
| legs | 12×24 | 24x48 |

## Equipment Style Details

- **naked**: skin color fill, no armor
- **light**: collar line, sleeve lines, pants seam
- **medium**: belt, collar, armor plates on chest
- **heavy**: helmet top bar, gauntlet line, boot tops

## Key Functions

- `generateSilhouette()` — Boolean mask per body type
- `shouldDither()` — Checkerboard dithering for pixel art shading
- `addDetails()` — Equipment-specific features (eyes, belt, gauntlets)
- `nearestNeighborUpscale()` — Crisp 2× scale for pixel art
- `generateBodyPart()` — Main pipeline function returning ImageData

## Why LLM Body Parts Failed (2026-05-01)

1. **Pollinations ignores style prompts** — "16-bit pixel art" gets smooth gradients instead
2. **Grok generates malformed figures** — Body parts arrive as floating shapes, not sprites
3. **Corner background removal fails on AI art** — Soft edges, inconsistent corners
4. **K-means washes colors** — Reduces 92-color sprites to 33 gray-blue colors
5. **Fixed-position compositing breaks anatomy** — Parts at y=4/36/64 don't align

## Recommendation

The **procedural parametric approach** is correct — generate pixel art programmatically via code, not via LLM image generation. The concept exists but needs actual implementation in TypeScript.

## Connections
- [[K-means Post-Processing]] — k-means destroys AI-generated art; works on photography
- [[Body Parts Pipeline Failure|sources/body-parts-pipeline-failure-2026-05-01]] — Full failure analysis
